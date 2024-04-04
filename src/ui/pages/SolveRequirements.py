import streamlit as st
import sys
import os
from pathlib import Path
from src import model
from src.prompt import BasePrompt
from src.get_instance import get_instance
from src.util import create_requirement_file, get_requirement_file

if __name__ == '__main__':
    current_dir = Path(__file__).parent.absolute()
    project_root = current_dir.parent.parent.parent
    sys.path.insert(0, str(project_root))

from src.util import ControlDict

def get_req(type, value):
    dict = {}
    dict['user_prompt'] = "this is some garbage"
    step = None
    if type == 'm':
        step = get_instance(model, internal.convert(type, value))
    elif type == 'e':
        print("tbd")
    elif type == 'p':
        dict['pre_prompt'] = internal.convert(type, value)
        step = BasePrompt(dict)
    elif type == 'i':
        dict['instruction_set'] = internal.convert(type, value)
        step = BasePrompt(dict)
    elif type == 's':
        print("tbd")
    if step != None:

        return step.getRequirements(), step.checkRequirements
    return [], True

converter = {
    'm': "Model",
    'e': "Context Injection",
    'p': "Pre-Prompt",
    'i': "Instruction Set",
    's': "Semantics Layer"
}

internal = ControlDict()

data = internal.data_dict

st.set_page_config(
    page_title="Setup Requirements",
    page_icon="👋",
    layout="wide",
)

option_list = {"Choose A Method" : "N/A"}

for i, j in data.items():
    for k, l in j.items():
        option_list[converter[i] + ": " + l] = [i,k]

options = list(option_list.keys())
selected_value = st.selectbox(
                label= "Choose A Method You Want to Configure or Setup",
                options= options,
                index = 0,
            )

# print(selected_value)
# print(option_list)
# print(" PRINTING OPTIONS ")
# print(options)

if not selected_value == options[0]:
    type, value = option_list[selected_value]
    st.write(f"Printing type: {type} and printing value: {value}")
    reqs, passed = get_req(type, value)

    if not reqs == []:
        if passed:
            st.write("Requirements all exist for this Method")
        reqs = ['Choose a file to add'] + reqs
        select = st.selectbox(
                    label= "Choose A Requirement To Configure",
                    options= reqs,
                    index = 0,
                )
        if not reqs[0] == select:
            text_input = st.text_area("Enter text:", value = get_requirement_file(select))
            submit_button = st.button("Submit")
            if submit_button:
                try:
                    create_requirement_file(select, text_input)
                except ValueError as e:
                    st.write("Improper submission: ", e)

    else:
        st.write("No Requirements for this Method")