from ..util import ControlDict
from pathlib import Path

def build(user_in, args):
    
    cwd = Path.cwd()
    
    converter = ControlDict()
    m, p, i, c = args
    model = converter.convert( 'm', m )
    pre_prompt = open((cwd / converter.convert( 'p', p )).resolve(), 'r').read()
    instruction_set = open((cwd / converter.convert( 'i', i )).resolve(), 'r').read()

    if "gpt" in model:
        prompt = open((cwd / 'prompt_text/prompt_openai.md').resolve(), 'r').read()
    elif "claude" in model:
        prompt = open((cwd / 'prompt_text/prompt_anthropic.md').resolve(), 'r').read()
    elif "gemini" in model:
        prompt = open((cwd / 'prompt_text/prompt_gemini.md').resolve(), 'r').read()
    elif "mistral" in model:
        prompt = open((cwd / 'prompt_text/prompt_mistral.md').resolve(), 'r').read()
    else:
        prompt = open((cwd / 'prompt_text/prompt.md').resolve(), 'r').read()
        
    prompt = prompt.replace('`{preprompt}`', pre_prompt)
    prompt = prompt.replace('`{instructions}`', instruction_set)
    prompt = prompt.replace('`{user_question}`', user_in)
    prompt = prompt.replace('{table_metadata_string}', c)
    
    return prompt