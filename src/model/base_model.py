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
        # Convert the entire string to lower case to ensure case insensitivity
        lower_case_string = msg.lower()

        # Initialize an empty string to collect all found substrings
        result_string = ""

        # Start searching from the beginning of the string
        start_index = 0

        # Loop until there are no more "select" keywords
        while True:
            # Find the starting index of the substring "select"
            start_index = lower_case_string.find("select", start_index)
            if start_index == -1:
                break  # Break the loop if "select" is not found

            # Find the index of the next semicolon after "select"
            end_index = lower_case_string.find(";", start_index)
            if end_index == -1:
                break  # Break the loop if there is no semicolon after "select"

            # Extract the substring from "select" to the next ";"
            substring = lower_case_string[start_index:end_index + 1]

            # Append the found substring to the result string, add a newline for separation
            result_string += substring + "\n"

            # Move start index past the current semicolon to search for the next "select"
            start_index = end_index + 1

        return result_string.strip()

    def run(self, args):
        temp = self.call_model(args)
        args['response_log'] = temp.log
        args['response_confidence'] = temp.confidence
        args['response_message'] = temp.message
        args['response_code'] = self.get_sql(temp.message)
        args['response_execution_time'] = temp.execution_time
        return args