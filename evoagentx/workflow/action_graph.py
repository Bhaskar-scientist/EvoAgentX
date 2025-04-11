import json
from pydantic import Field
from typing import Dict, Any, List

from ..core.logging import logger
from ..core.module import BaseModule
from ..core.registry import MODEL_REGISTRY, MODULE_REGISTRY
from ..models.model_configs import LLMConfig
from .operators import Operator, AnswerGenerate, ScEnsemble


class ActionGraph(BaseModule):

    name: str = Field(description="The name of the ActionGraph.")
    description: str = Field(description="The description of the ActionGraph.")
    llm_config: LLMConfig = Field(description="The config of LLM used to execute the ActionGraph.")

    def init_module(self):
        if self.llm_config:
            llm_cls = MODEL_REGISTRY.get_model(self.llm_config.llm_type)
            self._llm = llm_cls(config=self.llm_config)
    
    def __call__(self, *args: Any, **kwargs: Any) -> dict:
        return self.execute(*args, **kwargs)
    
    def execute(self, *args, **kwargs) -> dict:
        raise NotImplementedError(f"The execute function for {type(self).__name__} is not implemented!")
    
    def get_graph_info(self, **kwargs) -> dict:
        """
        Get the information of the action graph, including all operators from the instance.
        """
        operators = {}
        # the extra fields are the fields that are not defined in the Pydantic model 
        for extra_name, extra_value in self.__pydantic_extra__.items():
            if isinstance(extra_value, Operator):
                operators[extra_name] = extra_value

        config = {
            "class_name": self.__class__.__name__,
            "name": self.name,
            "description": self.description,
            "llm_config": self.llm_config.to_dict(exclude_none=True) \
                if self.llm_config is not None else \
                    self._llm.config.to_dict(exclude_none=True),
            "operators": {
                operator_name: {
                    "class_name": operator.__class__.__name__,
                    "name": operator.name,
                    "description": operator.description,
                    "interface": operator.interface,
                    "prompt": operator.prompt
                }
                for operator_name, operator in operators.items()
            }
        }
        return config
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ActionGraph":
        """
        Create an ActionGraph from a dictionary.
        """
        class_name = data.get("class_name", None)
        if class_name:
            cls = MODULE_REGISTRY.get_module(class_name)
        operators_info = data.pop("operators", None)
        module = cls._create_instance(data)
        if operators_info:
            for extra_name, extra_value in module.__pydantic_extra__.items():
                if isinstance(extra_value, Operator) and extra_name in operators_info:
                    extra_value.set_operator(operators_info[extra_name])
        return module
    
    def save_module(self, path: str, ignore: List[str] = [], **kwargs):
        """
        Save the workflow graph to a module file.
        """
        logger.info("Saving {} to {}", self.__class__.__name__, path)
        config = self.get_graph_info()
        for ignore_key in ignore:
            config.pop(ignore_key, None)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        return path


class QAActionGraph(ActionGraph):

    def __init__(self, llm_config: LLMConfig, **kwargs):

        name = kwargs.pop("name") if "name" in kwargs else "Simple QA Workflow"
        description = kwargs.pop("description") if "description" in kwargs else \
            "This is a simple QA workflow that use self-consistency to make predictions."
        super().__init__(name=name, description=description, llm_config=llm_config, **kwargs)
        self.answer_generate = AnswerGenerate(self._llm)
        self.sc_ensemble = ScEnsemble(self._llm)
        
    def execute(self, problem: str) -> dict:

        solutions = [] 
        for _ in range(3):
            response = self.answer_generate(input=problem)
            answer = response["answer"]
            solutions.append(answer)
        ensemble_result = self.sc_ensemble(solutions=solutions)
        best_answer = ensemble_result["response"]
        return {"answer": best_answer}
    