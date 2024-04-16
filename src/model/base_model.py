from abc import ABC, abstractmethod
from .model_result import ModelResult
from src.step import Step

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

    def run(self, args):
        temp = self.call_model(args)
        args['response_log'] = temp.log
        args['response_confidence'] = temp.confidence
        args['response_message'] = temp.message
        args['response_code'] = temp.code
        args['response_execution_time'] = temp.execution_time
        return args

    def get_sql(self, msg):
        return