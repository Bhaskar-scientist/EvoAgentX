import numpy as np
import random
import copy
from tqdm import tqdm
from typing import List, Any, Optional, Callable
from pydantic import Field

from evoagentx.core.module import BaseModule
from evoagentx.models.base_model import BaseLLM
from evoagentx.benchmark.benchmark import Benchmark
from evoagentx.optimizers import MiproOptimizer
from evoagentx.utils.mipro_utils.register_utils import MiproRegistry
from evoagentx.workflow.operators import Predictor


class MassOptimiser(BaseModule):
    workflow: Optional[list[Any]] = Field(default=None, description="The workflow to optimize.")
    optimizer_llm: Optional[BaseLLM] = Field(default=None, description="The LLM to use for optimization.")
    max_bootstrapped_demos: int = Field(default=4, description="The number of bootstrapped demos to use for optimization.")
    max_labeled_demos: int = Field(default=16, description="The number of labeled demos to use for optimization.")
    auto: str = Field(default="medium", description="The auto mode to use for optimization.")
    eval_rounds: int = Field(default=1, description="The number of rounds to evaluate the workflow.")
    num_threads: int = Field(default=1, description="The number of threads")
    save_path: Optional[str] = Field(default=None, description="Directory for saving logs, None means no saving")

    def init_module(self, **kwargs):
        self.rng = None
        
        if self.executor_llm is None and self.optimizer_llm is None:
            raise ValueError("Optimizer llm is required")

        if self.executor_llm is None:
            self.executor_llm = self.optimizer_llm


    def optimize(self, 
                 *,
                 benchmark: Benchmark,
                 softmax_temperature: float = 1.0,
                 agent_budget: int = 10):

        self.benchmark = benchmark
        selection_probability = self._softmax_with_temperature(softmax_temperature)

        best_score = 0
        for _ in range(self.max_steps):
            registry = MiproRegistry()
            u = np.random.uniform(0, 1, size=selection_probability.shape)

            total = 0
            for ui, pi, blocki in zip(u, selection_probability, self.workflow.blocks):
                if ui <= pi:
                    blocki.n = blocki.search_space[0]
                    total += blocki.n
                else:
                    space = blocki.search_space
                    idx = random.randint(0, len(space) - 1)
                    blocki.n = space[idx]
                    total += blocki.n
                
                if blocki.n > 0:
                    registry.track(blocki, blocki.get_registry(), input_names=['problem', 'context'], output_names=['answer'])

            if total > agent_budget:
                continue
        
            optimizer = MiproOptimizer(
                registry = registry,
                program = self.workflow,
                optimizer_llm = self.optimizer_llm,
                max_bootstrapped_demos = self.max_bootstrapped_demos,
                max_labeled_demos = self.max_labeled_demos,
                num_threads= self.num_threads,
                eval_rounds= self.eval_rounds,
                auto= self.auto,
                save_path= self.save_path
            )

            score = optimizer.evaluate(dataset = self.benchamrk, eval_mode = "test")       

            if score > best_score:
                best_score = score
                best_workflow = copy.deepcopy(optimizer)

        best_workflow.optimize(dataset = self.benchmark)
        return best_workflow.restore_best_program()

    def _softmax_with_temperature(self, temperature):        
        logits = []
        for block in self.workflow.blocks:
            logits.append(block.influence_score)

        logits = np.array(logits, dtype=np.float32)
        logits = logits / temperature
        exps = np.exp(logits- np.max(logits))

        return exps / np.sum(exps)

    def _random_sample_searchSpace(self, workflow, agent_budget):
        values = []
        total = 0
        for block in workflow.blocks:
            space = block.search_space
            idx = random.randint(0, len(space) - 1)
            val = space[idx]
            total += val
            values.append(val)

            if total >= agent_budget:
                return [-1]
        return values
