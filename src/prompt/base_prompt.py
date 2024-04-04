from src.step import Step
from src.get_instance import get_instance
from . import prompt_text 

def make_user_prompt():
    return input("Input your prompt: ") 


class BasePrompt(Step):
    """
    Requires args as a dictionary can include instruction set, pre-prompt information, pre-prompt, user prompt, and a mask
    all other arguements will be tacked onto self.args 
    """
    def __init__(self, args=None):
        
        i = args.pop('instruction_set', None)
        pp = args.pop('pre_prompt_info', None)

        if i is not None:
            self.instruction_set = get_instance(prompt_text, i)
        else:
            self.instruction_set = None
        if pp is not None:
            self.pre_prompt_info = get_instance(prompt_text, pp)
        else:
            self.pre_prompt_info = None

        self.pre_prompt = args.pop('pre_prompt', None)
        self.user_prompt = make_user_prompt()
        # self.mask = self.args.pop('mask', None)
        self.order = args.pop('size', 0) + 10
        self.args = args or {}

    def run(self, arg):
        return form_prompt(self)


def form_prompt(prompt):
    if not isinstance(prompt, BasePrompt):
        raise TypeError("Input must be an instance of BasePrompt")
    
    data = {
    'system_message': prompt.instruction_set,
    'user_message': f"{prompt.pre_prompt}\n{prompt.user_prompt}"
    }
    # TODO add something here w/ some way you determined to input pre_prompt_info once we insert it
    return data
    
