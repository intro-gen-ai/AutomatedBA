from abc import ABC, abstractmethod
from .model_result import ModelResult
from step import Step

# abstract class for all models to inherit from

class BaseModel(Step):
    def __init__(self, args=None):
        if args is None:
            args = dict()  # Ensure args is a set, even if None is passed
        size = args.pop('size', 0)
        self.order = 30+size
        self.args = args

    @abstractmethod
    def call_model(self, input) -> ModelResult:
        pass  # No need to raise NotImplementedError here due to @abstractmethod

    def run(self, arg):
        return self.call_model(arg)
