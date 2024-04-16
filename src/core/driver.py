from ..util import ControlDict
from src import model
from src.prompt import BasePrompt
from src.get_instance import get_instance
from src.util import decrypt_externally
from ..step import Step
from src.encoding.encoding import KnowledgeInjectionStep
from langchain_openai import OpenAIEmbeddings
from src import semantic_layer
from src.prompt import prompt_builder
from src.util import SnowflakeManager

def make_user_prompt():
    return input("Input your prompt: ") 

def layoutProcess(e_set, m_set, p_set, i_set, s_set, text_prompt = None, database = None):
    converter = ControlDict()
    steps = list()
    p_s = list()
    i_s = list()
    temp = ""
    # TODO DOUBLE CHECK IMPLEMENTATION
    # Apr 11: 02:16
    for i in e_set:
        config_entry = converter.convert('e', i)
        step_instance = KnowledgeInjectionStep(
                client=OpenAIEmbeddings(api_key = decrypt_externally('.openai_secret')),
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

    steps.append(BasePrompt(dict))
    # 
    order_steps = sorted(steps, key=lambda x: x.getOrder())
    # snowflake is not set up so we cannot do that set yet.
    # TODO ananth once u build the integrations for this tell me and I will insert it
    if len(s_set) < 1:
        return "SEMANTICS REQUIRED" 


    if not text_prompt:
        text_prompt = make_user_prompt()

    bdict = {'user_input' : text_prompt, "database" : database}
    if not i_s == list():
        bdict['instructions_file'] = i_s[0]
    if not p_s == list():
        bdict['preprompt_file'] = p_s[0]
    if not temp == "":
        bdict['model_name'] == temp

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
        
    if k.execution_time is not None:
        print(k.execution_time)
    if k.code is not None:
        print(k.code) 
    if k.message is not None:
        print(k.message)
    if k.confidence is not None:
        print(k.confidence) 
    if k.log is not None:
        print(k.log)
    print(k)

    if k.message is None:
        raise KeyError("Model Failed")
    if k.code is not None:
        query_result = snowflake.query_df(k.code)
        print(query_result.head(10))
        return k.message, query_result
    else:
        return k.message, None

    

# layoutProcess(None, None, list(1), None, None)