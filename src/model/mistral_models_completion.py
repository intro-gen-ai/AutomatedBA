from .base_model import BaseModel
from .model_result import ModelResult
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from src.util import decrypt_externally
import time
import mistralai

class MistralModels(BaseModel):
    def __init__(self, args=None):
        super().__init__(args)
        self.token_location = '.mistral_secret'

    def getToken(self):
        # In Mistral, API key is used directly without decryption
        return decrypt_externally(self.token_location)


    def query_model(self, system_message, user_message, temp=-1, count=0):
        if not self.checkRequirements:
            return {"error" : f"missing {self.getRequirements}"}
        mistralai.api_key = self.getToken()
        client = MistralClient(api_key=mistralai.api_key)
        
        messages = []
        if system_message:  # Add system message if it exists
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": user_message})
        response_list = list()
        while count < 3:
            if temp > -1:
                response = client.chat(
                    model=self.model_name,
                    messages=messages,
                    temperature=temp
                )
            else:
                 response = client.chat(
                    model=self.model_name,
                    messages=messages,
                )

            finish_reason = response.choices[0].finish_reason
            response_list.append(response)
            if finish_reason == "stop":

                return response_list
            else:

                count += 1
        
       
        print("Failed to get a complete response after 3 attempts")
        return response_list
    
    def getRequirements(self):
        return [self.token_location]