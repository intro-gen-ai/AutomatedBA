import openai
from src.util import decrypt_externally

class PreMask():
    def __init__(self):
        self.model_name = "gpt-3.5-turbo"
        self.token_location = '.openai_secret'

    def getToken(self):
        return decrypt_externally(self.token_location)
    
    def select_terms(self, original_prompt, terms_list, temp=0.5):
        openai.api_key = self.getToken()
        client = openai.OpenAI(api_key=openai.api_key)

        # Updated prompt to comply with the new API format
        messages = [{
        "role": "system",
        "content": f"Select relevant elements from the following list related to '{original_prompt}': {', '.join(terms_list)}. Relevant means any element from {', '.join(terms_list)} that directly relates to or is associated with '{original_prompt}'. It is acceptable to include all provided elements from {', '.join(terms_list)} if they are pertinent to '{original_prompt}'. Please ensure your response includes only elements from {', '.join(terms_list)}, without introducing any new information or terms not already present in {', '.join(terms_list)}."
        }]
        
        # Adjusted method call to comply with OpenAI's updated API
        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temp
        )
        selected_terms_text = response.choices[0].message.content.strip()
        selected_terms = selected_terms_text.split(', ')  # Simple parsing
        return [original_prompt, selected_terms]

# Example usage
selector = PreMask()
original_prompt = "I want a SQL function for joinining two named Hello and Goodbye"
terms_list = ["join", "create", "colon", "soccer"]
result = selector.select_terms(original_prompt, terms_list)
print(result)
