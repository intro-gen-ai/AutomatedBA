from ..util import ControlDict
from src import model
from src.prompt import BasePrompt
from src.get_instance import get_instance
from src.util import decrypt_externally
from ..step import Step
from src.encoding.encoding import KnowledgeInjectionStep
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from src import semantic_layer
from src.prompt import prompt_builder
from src.util import SnowflakeManager
import pandas as pd

def make_user_prompt():
    return input("Input your prompt: ") 

def layoutProcess(e_set, m_set, p_set, i_set, s_set, text_prompt = None, database = None):
    converter = ControlDict()
    steps = list()
    p_s = list()
    i_s = list()
    temp = ""
    database = "ACADEMIC"

    if not text_prompt:
        text_prompt = make_user_prompt()
    # TODO DOUBLE CHECK IMPLEMENTATION
    # Apr 11: 02:16
    for i in e_set:
        config_entry = converter.convert('e', i)
        step_instance = KnowledgeInjectionStep(
                client=OpenAI(api_key = decrypt_externally('.openai_secret')),
                collection_name=f"{config_entry}",
                file_path=f"src/encoding/data/{config_entry}.txt",  # Example dynamic path based on identifier
                model="text-embedding-3-small",  # Customize as needed
                top_k=5,
                order=int(i),
                prompt = text_prompt)  # Example, setting order based on identifier 
        
        steps.append(step_instance)

    for i in m_set:
        temp = converter.convert( 'm', i )
        steps.append(get_instance(model, temp) )

    for i in p_set:
        i_s.append(converter.convert('p', i))

    for i in i_set:
        p_s.append(converter.convert('i', i))

    for i in s_set:
        steps.append(get_instance(semantic_layer, converter.convert('s', i) ))

    steps.append(BasePrompt())
    # 
    order_steps = sorted(steps, key=lambda x: x.getOrder())
    # snowflake is not set up so we cannot do that set yet.
    # TODO ananth once u build the integrations for this tell me and I will insert it
    if len(s_set) < 1:
        return "SEMANTICS REQUIRED" 




    bdict = {'user_input' : text_prompt, "database" : database}
    if not i_s == list():
        bdict['instructions_file'] = i_s[0]
    if not p_s == list():
        bdict['preprompt_file'] = p_s[0]
    if not temp == "":
        bdict['model_name'] = temp

    return runProcess(order_steps, bdict)

def runProcess(steps, args):
    # we can add looping later
    snowflake = SnowflakeManager()
    print("Running Process")
    k = args
    for i in steps:
        print(i.getOrder())
        j=i.run(k)
        k = j
        print(k)
        
    if k["response_execution_time"] is not None:
        print(k["response_execution_time"])
    if k["response_code"] is not None:
        print(k["response_code"]) 
    if k["response_message"] is not None:
        print(k["response_message"])
    if k["response_confidence"] is not None:
        print(k["response_confidence"]) 
    if k["response_log"] is not None:
        print(k["response_log"])
    print(k)

    if k["response_message"] is None:
        raise KeyError("Model Failed")
    if k["response_code"] is not None:
        snowflake.connect()
        try:
            query_result = snowflake.query_df(k["response_code"])
            print(query_result.head(10))
            return k["response_message"], query_result
        except Exception as err:
            error_df = pd.DataFrame({"Snowflake Return": [str(err)]})
            return k["response_message"], error_df
    else:
        return k["response_message"], None

    

# layoutProcess(None, None, list(1), None, None)