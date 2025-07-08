import json
import asyncio
from uuid import uuid4
from typing import Dict, Any, Union, List, Optional

from llama_index.core.schema import BaseNode
from llama_index.core.storage import StorageContext
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.indices import PropertyGraphIndex
from llama_index.core.indices.property_graph.transformations import ImplicitPathExtractor
from llama_index.core.graph_stores.types import (
    LabelledNode,
    Relation,
    EntityNode,
    ChunkNode,
)

from evoagentx.rag.schema import Chunk
from evoagentx.core.logging import logger
from .base import BaseIndexWrapper, IndexType
from evoagentx.models.base_model import BaseLLM
from evoagentx.storages.base import StorageHandler
from evoagentx.rag.transforms.graph_extract import BasicGraphExtractLLM

class GraphIndexing(BaseIndexWrapper):
    """Wrapper for LlamaIndex PropertyGraphIndex."""
    
    def __init__(
        self,
        embed_model: BaseEmbedding,
        storage_handler: StorageHandler,
        llm: BaseLLM,
        index_config: Dict[str, Any] = None
    ) -> None:
        super().__init__()
        self.index_type = IndexType.GRAPH
        self._embed_model = embed_model
        self.storage_handler = storage_handler
        # create a storage_context for llama_index
        self._create_storage_context()
        # for caching llama_index node
        self.id_to_node = dict()

        self.index_config = index_config or {}
        # initlize the kg_extractor
        assert isinstance(llm, BaseLLM), f"The LLM model should be an instance class."
        kg_extractor = BasicGraphExtractLLM(
            llm=llm, 
            num_workers=self.index_config.get("num_workers", 4),
        )
        try:
            # check if a vector store is initilized in storageHandler,
            # then use the hybrid-search.
            vector_store = self.storage_handler.vector_store.get_vector_store() if self.storage_handler.vector_store is not None else None
            
            self.index = PropertyGraphIndex(
                nodes=[],
                kg_extractors=[kg_extractor, ImplicitPathExtractor()],  # 'ImplicitPathExtractor' for node basic relation(tree structure and so on).
                embed_model=self._embed_model,
                vector_store=vector_store if (not self.storage_handler.graph_store.supports_vector_queries) else None,  # if graph database support vector query, disable the vector database.,
                property_graph_store=self.storage_context.graph_store,
                storage_context=self.storage_context,
                show_progress=self.index_config.get("show_progress", False),
                use_async=self.index_config.get("use_async", True),
            )
        except Exception as e:
            logger.error(f"Failed to initialize {self.__class__}: {str(e)}")
            raise

    def get_index(self) -> PropertyGraphIndex:
        return self.index

    def _create_storage_context(self):
        """Create the LlamaIndex-compatible storage context."""
        super()._create_storage_context()
        # Construct a storage_context for llama_index
        assert self.storage_handler.graph_store is not None, "GraphIndexing must init a graph backend in 'storageHandler'"

        self.storage_context = StorageContext.from_defaults(
            graph_store=self.storage_handler.graph_store.get_graph_store()
        )

    def insert_nodes(self, nodes: List[Union[Chunk, BaseNode]]):
        """
        Insert or update nodes into the graph index.

        Converts Chunk objects to LlamaIndex nodes, serializes metadata as JSON strings,
        and inserts them into the PropertyGraphIndex. Nodes are cached in id_to_node for
        quick access.

        Args:
            nodes (List[Union[Chunk, BaseNode]]): List of nodes to insert, either Chunk or BaseNode.
        """
        try:
            filtered_nodes = [node.to_llama_node() if isinstance(node, Chunk) else node for node in nodes]

            # Convert dict to string
            for node in filtered_nodes:
                node.metadata = {"metadata": json.dumps(node.metadata)}
            
            nodes = self.index._insert_nodes(filtered_nodes)
            logger.info(f"Inserted {len(nodes)} nodes into PropertyGraphIndex")

            return list([node.node_id for node in nodes])
        except Exception as e:
            logger.error(f"Failed to insert nodes: {str(e)}")
            return []

    def delete_nodes(self, node_ids: Optional[List[str]] = None, metadata_filters: Optional[Dict[str, Any]] = None):
        """
        Delete nodes from the graph index based on node IDs or metadata filters.

        Removes specified nodes from the index and the id_to_node cache. If metadata_filters
        are provided, nodes matching the filters are deleted.

        Args:
            node_ids (Optional[List[str]]): List of node IDs to delete. Defaults to None.
            metadata_filters (Optional[Dict[str, Any]]): Metadata filters to select nodes for deletion. Defaults to None.
        """
        try:
            if node_ids:
                for node_id in node_ids:
                    if node_id in self.id_to_node:
                        self.index.delete_nodes([node_id])
                        self.id_to_node.pop(node_id)
                        logger.info(f"Deleted node {node_id} from PropertyGraphIndex")
            elif metadata_filters:
                nodes_to_delete = []
                for node_id, node in self.id_to_node.items():
                    if all(node.metadata.get(k) == v for k, v in metadata_filters.items()):
                        nodes_to_delete.append(node_id)
                if nodes_to_delete:
                    self.index.delete_nodes(nodes_to_delete)
                    for node_id in nodes_to_delete:
                        self.id_to_node.pop(node_id)
                    logger.info(f"Deleted {len(nodes_to_delete)} nodes matching metadata filters from PropertyGraphIndex")
            else:
                logger.warning("No node_ids or metadata_filters provided for deletion")
        except Exception as e:
            logger.error(f"Failed to delete nodes: {str(e)}")
            raise

    async def aload(self, nodes: List[Union[Chunk, BaseNode, LabelledNode, Relation, EntityNode, ChunkNode]]) -> None:
        """
        Asynchronously load nodes into the graph index and its backend stores.

        Caches nodes in the id_to_node dictionary and loads them into the graph and optionally
        vector stores, ensuring no duplicates by relying on the backend's duplicate checking.

        Args:
            nodes (List[Union[Chunk, BaseNode]]): List of nodes to load, either Chunk or BaseNode.
        """
        try:
            filtered_nodes = [node.to_llama_node() if isinstance(node, Chunk) else node for node in nodes]

            tasks = []
            for node in filtered_nodes:
                # Load into kv cache
                self.id_to_node[node.id] = node.model_copy()

                # load into vector database
                if (self.storage_handler.vector_store is not None) and \
                    (not self.storage_handler.graph_store.supports_vector_queries):

                    tasks.append(
                        self.storage_handler.vector_store.aload(node)
                    )

                # load into graph database
                tasks.extend([self.storage_handler.graph_store.aload(node)])

            # Async load
            await asyncio.gather(*tasks, return_exceptions=True)
            logger.info(f"Loaded {len(filtered_nodes)} nodes into cache and graph store.")

        except Exception as e:
            logger.error(f"Failed to load nodes: {str(e)}")

    def load(self, nodes: List[Union[Chunk, BaseNode]]) -> None:
        """
        Synchronously load nodes into the graph index.

        Wraps the asynchronous aload method to provide a synchronous interface for loading nodes.

        Args:
            nodes (List[Union[Chunk, BaseNode]]): List of nodes to load, either Chunk or BaseNode.

        """
        asyncio.run(self.aload(nodes))

    def build_kv_store(self) -> None:
        """
        Match all the nodes and relations into python Dict.
        """
        for node in self.storage_handler.graph_store.build_kv_store():
            self.id_to_node[str(uuid4())] = node

    def clear(self):
        """
        Clear all nodes from the graph index and its cache.

        Deletes all nodes from the PropertyGraphIndex and clears the id_to_node cache.
        """
        try:
            self.storage_handler.graph_store.clear()
            self.id_to_node.clear()
            logger.info("Cleared all nodes from PropertyGraphIndex")
        except Exception as e:
            logger.error(f"Failed to clear index: {str(e)}")
            raise