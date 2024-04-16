from ..util import ControlDict
from pathlib import Path
from src.semantic_layer import SemanticContext
import sys
import os

# if __name__ == '__main__':
    # current_dir = Path(__file__).parent.absolute()
    # project_root = current_dir.parent.parent
    # sys.path.insert(0, str(project_root))

def build_prompt(user_in, args):
    
    cwd = Path.cwd()

    converter = ControlDict()
    m, p, i, s, r = args
    # m = model number 
    # p = preprompt number
    # i =  instruction set number
    # s = database name in all caops
    # r = RAG as a string (hopefully)
    dict ={}
    dict['database']=s
    semantics = SemanticContext().run(dict)
    #test = semantics
    print(semantics)
    model = converter.convert( 'm', m )

    pre_prompt = open(os.path.join(cwd,converter.convert( 'p', p )), 'r').read()
    instruction_set = open(os.path.join(cwd,converter.convert( 'i', i )), 'r').read()
    
    if "Gpt" in model or "gpt" in model:
        prompt = open(os.path.join(cwd,'src/prompt/prompt_text/prompt_openai.md')).read()
        system_message = "Your task is to convert a text question to a SQL query that runs on Snowflake, given a database schema."
    elif "claude" in model:
        prompt = open(os.path.join(cwd,'src/prompt/prompt_text/prompt_anthropic.md')).read()
        system_message = "Your task is to convert a text question to a SQL query that runs on Snowflake, given a database schema. Return the SQL as a markdown string, nothing else."
    elif "gemini" in model:
        prompt = open(os.path.join(cwd,'src/prompt/prompt_text/prompt_gemini.md')).read()
        system_message = "Your task is to convert a text question to a SQL query that runs on Snowflake given a database schema. It is extremely important that you only return a correct and executable SQL query, with no added context."
    elif "mistral" in model:
        prompt = open(os.path.join(cwd,'src/prompt/prompt_text/prompt_mistral.md')).read()
        system_message = "Your task is to convert a text question to a SQL query that runs on Snowflake given a database schema. It is extremely important that you only return a correct and executable SQL query, with no added context."
    else:
        prompt = open(os.path.join(cwd,'src/prompt/prompt_text/prompt.md')).read()
        system_message = "Your task is to convert a text question to a SQL query that runs on Snowflake given a database schema. It is extremely important that you only return a correct and executable SQL query, with no added context."
        
    prompt = prompt.replace('`{preprompt}`', pre_prompt)
    prompt = prompt.replace('`{user_question}`', user_in)
    prompt = prompt.replace('`{instruction_set}`', instruction_set)
    prompt = prompt.replace('`{rag}`', r)
    prompt = prompt.replace('{table_metadata_string}', s)
    
    return (prompt, user_in)