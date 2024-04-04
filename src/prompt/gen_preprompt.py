import openai

openai.api_key = ""

def gen_preprompt(RAG, user_in):
    response = openai.ChatCompletion.create(model="gpt-4",
                                            temperature=0, 
                                            top_p=0,
                                            frequency_penalty=0,
                                            messages=[{"role": "user",
                                                       "content": "Given these relevant definitions: " + str(RAG) 
                                                       + " and this user question \"" + str(user_in) + 
                                                       ", generate a pre-prompt for a GPT model designed to produce the correct SQL query."}])
    return response