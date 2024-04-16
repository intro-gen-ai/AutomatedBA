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

    def get_sql(self, msg):
        # Convert the entire string to lower case
        lower_case_string = msg.lower()

        # Find the starting index of the substring "select"
        start_index = lower_case_string.find("select")
        if start_index == -1:
            return "The keyword 'select' was not found."

        # Find the index of the next semicolon after "select"
        end_index = lower_case_string.find(";", start_index)
        if end_index == -1:
            return "No terminating semicolon (';') found after 'select'."


        # Extract the substring from "select" to the next ";"
        substring = lower_case_string[start_index:end_index + 1]


        # Append the found substring to the result string
        return substring

    def run(self, args):
        temp = self.call_model(args)
        args['response_log'] = temp.log
        args['response_confidence'] = temp.confidence
        args['response_message'] = temp.message
        args['response_code'] = self.get_sql(temp.message)
        args['response_execution_time'] = temp.execution_time
        return args