from src.step import Step
from src.get_instance import get_instance
from . import prompt_text 
from pathlib import Path
import os

def make_user_prompt():
    return input("Input your prompt: ") 


class BasePrompt(Step):
    """
    Requires args as a dictionary can include instruction set, pre-prompt information, pre-prompt, user prompt, and a mask
    all other arguements will be tacked onto self.args 
    """
    def __init__(self, args=None):
        
        """i = args.pop('instruction_set', None)
        pp = args.pop('pre_prompt_info', None)
        user_p = args.pop('user_prompt', None)
        if i is not None:
            self.instruction_set = get_instance(prompt_text, i)
        else:
            self.instruction_set = None
        if pp is not None:
            self.pre_prompt_info = get_instance(prompt_text, pp)
        else:
            self.pre_prompt_info = None

        self.pre_prompt = args.pop('pre_prompt', None)
        if user_p is not None:
            self.user_prompt = user_p
        else:
            self.user_prompt = make_user_prompt()
        # self.mask = self.args.pop('mask', None)"""
        self.order = args.pop('size', 0) + 10
        self.args = args or {}


        self.prompt = args.pop('prompt', None)
        self.instruction_set = args.pop('instruction_set',None)
        

    def run(self, args):
        self.args = args
        return form_prompt(self)

    def getRequirements(self):
        return []
    
def form_prompt(base_prompt):
    cwd = Path.cwd()
    # m = model number 
    # p = preprompt number
    # i =  instruction set number
    # s = database name in all caops
    # r = RAG as a string (hopefully)
    instruction = ""
    pre_prompt = ""
    try:
        instruction = open(os.path.join(cwd, base_prompt.args['instructions_file']), 'r').read()
        base_prompt.args['instruction'] = instruction
    except:
        print("no instructions")

    try:
        pre_prompt = open(os.path.join(cwd, base_prompt.args['preprompt_file']), 'r').read()
        base_prompt.args['pre_prompt'] = pre_prompt
    except:
        print("no pre-prompt")
    try:
        model = base_prompt.args['model_name']
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
        user_in = ""
        try:
            user_in = base_prompt.args['user_input']
        except:
            raise ValueError("No user message!!!")

        prompt = prompt.replace('`{preprompt}`', pre_prompt)
        prompt = prompt.replace('`{user_question}`', user_in)
        prompt = prompt.replace('`{instruction_set}`', instruction)
        try:
            a = base_prompt.args['rag_set']
            rag = ""
            for i in a:
                # TODO ananth fix this when you get it
                b = b + " | " + i
            prompt = prompt.replace('`{rag}`', rag)
        except:
            prompt = prompt.replace('`{rag}`', "We don't have an relevant information to insert")
        
        try:
            s = base_prompt.args['semantics_context']
            prompt = prompt.replace('{table_metadata_string}', str(s))
            base_prompt.args['user_message'] = user_in
            base_prompt.args['system_message'] = system_message
        except:
            ValueError("No semantics layer included - cannot view database schema")
    except:
        raise ValueError("No model in prompt")
   

    return base_prompt.args

# def form_prompt(prompt):
#     if not isinstance(prompt, BasePrompt):
#         raise TypeError("Input must be an instance of BasePrompt")
#     # m = model number 
#     # p = preprompt number
#     # i =  instruction set number
#     # s = database name in all caops
#     # r = RAG as a string (hopefully)


#     data = {
#     'system_message': prompt.system_message,
#     #'user_message': f"{prompt.pre_prompt}\n{prompt.user_prompt}"
#     'user_message': prompt.user_message
#     }


#     # TODO add something here w/ some way you determined to input pre_prompt_info once we insert it
#     return data
    
