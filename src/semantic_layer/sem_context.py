from src.step import Step
from abc import ABC, abstractmethod
from src.semantic_layer import BaseSemantics

class SemanticContext(BaseSemantics):
    def __init__(self, args=None):
        super().__init__(args=args)
        

    def Run(self):
        return {"semantics_context": self.schema}