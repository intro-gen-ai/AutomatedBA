from converter import ControlDict
# import os
# import sys
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
# print(current_dir)
import model 
from prompt import BasePrompt
from get_instance import get_instance


def layoutProcess(e_set, m_set, p_set, i_set, s_set):
    converter = ControlDict()
    steps = list()
    p_s = list()
    i_s = list()

# TODO not implemented
    # for i in e_set:
    #     e.append(converter.convert( ('e', i) ))

    for i in m_set:
        steps.append(get_instance(model, converter.convert( f"('m', {i})" ) ))

    for i in p_set:
        i_s.append(converter.convert( ('p', i) ))

    for i in i_set:
        p_s.append(converter.convert( ('p', i) ))

# TODO not implemeneted
    # for i in s_set:
    #     s.append(converter.convert( ('s', i) ))
    # if len(i_set) > 1:
        # TODO we need to talk about what to do here to combine them so for now its just an empty case
        # i implemented the single form case
    dict = {}
    
    if len(i_s) > 1:
        dict['instruction_set']= i_s[0]
    if len(p_s) > 1:
        dict['pre_prompt'] = p_s[0]
    steps.append(BasePrompt(dict))
    # 

    order_steps = sorted(steps, key=lambda x: x.getOrder())
    # snowflake is not set up so we cannot do that set yet.
    # TODO ananth once u build the integrations for this tell me and I will insert it
    runProcess(order_steps)

def runProcess(steps):
    # we can add looping later
    k = None
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

# layoutProcess(None, None, list(1), None, None)