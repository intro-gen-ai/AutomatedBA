from .gpt_models_completion import GptModels
from .model_result import ModelResult
import time

class Gpt_3_5_Turbo(GptModels):

    def __init__(self, args=None):
        super().__init__(args=args)  # Pass args to the base class constructor
        self.model_name = "gpt-3.5-turbo"

    def call_model(self, input, temp=-1) -> ModelResult:
        # responses is required to be a dictionary - system_message is optional for gpt 3.5 but user_message is not
        start_time = time.time()
        responses = self.query_model(input.get('system_message', None), input.get('user_message'), temp=temp)
        end_time = time.time()

        if responses is not None and len(responses) > 0:
            # Process the last response in the list, assuming it's the most complete
            last_response = responses[-1]
            # content = last_response[1]["choices"][0]["message"]["content"]
            # finish_reason = last_response["choices"][0]["finish_reason"]
            # print(last_re)
            content = last_response.choices[0].message.content  # Changed from ["message"]["content"] to .text
            finish_reason = last_response.choices[0].finish_reason 
            # responses.choices[0].text # Direct attribute access
            # You might want to implement a better confidence estimation
            confidence = 1.0 if finish_reason == "stop" else 0.0
            log = responses
            response_time = end_time - start_time
            return ModelResult(message=content, confidence=confidence, log=log, execution_time=response_time)
        # elif len(responses):
        #     print('break point')
        else:
            return ModelResult.empty()
    
