import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd

if __name__ == '__main__':
    current_dir = Path(__file__).parent.absolute()
    project_root = current_dir.parent.parent.parent
    sys.path.insert(0, str(project_root))

from src.util import ControlDict
from src.core import layoutProcess

def response_generator(selection, prompt):
    # return "hi"
    # response = random.choice(
    #     [
    #         "Hello there! How can I assist you today?",
    #         "Hi, human! Is there anything I can help you with?",
    #         "Do you need help?",
    #     ]
    # )
    # for word in response.split():
    #     yield word + " "
    #     time.sleep(0.05)
    m_set = selection['m']
    e_set = selection['e']
    p_set = selection['p']
    i_set = selection['i']
    s_set = selection['s']
    response, result = layoutProcess(e_set, m_set, p_set, i_set, s_set, prompt)
    if not isinstance(result, pd.DataFrame):
            # raise ValueError("Query did not return a DataFrame.")
            return response, None
    else:
        return response, result

multiselect = ['e']

convert = {
    'm': "Model",
    'e': "Context Injection",
    'p': "Pre-Prompt",
    'i': "Instruction Set",
    's': "Semantics Layer"
}

st.set_page_config(
    page_title="Query",
    page_icon="👋",
    layout="wide",
)

optionset = ControlDict()
selected_keys = {}

columns = st.columns(len(optionset.data_dict.keys()))
# container = st.container()

for i, (option_group, options) in enumerate(optionset.data_dict.items()):
    if not option_group in selected_keys:
        selected_keys[option_group] = []
    
    if option_group in multiselect:
        inverted_options = {v: k for k, v in options.items()}
        options_list = list(inverted_options.keys())
        with columns[i]:
            selected_values = st.multiselect(
                label= convert[option_group],
                options= options_list,
                # index = 0,
                key=option_group
            )
        for j in selected_values:
            selected_keys[option_group].append(inverted_options[j])

    else:
        placeholder = ["Choose a " + convert[option_group]]
        inverted_options = {v: k for k, v in options.items()}
        if option_group == "s":
            options_list = list(inverted_options.keys())
        else:
            options_list = placeholder + list(inverted_options.keys())
        with columns[i]:
            selected_value = st.selectbox(
                label= convert[option_group],
                options= options_list,
                index = 0,
                key=option_group
            )
        if selected_value not in placeholder:
            selected_keys[option_group].append(inverted_options[selected_value])
#         selected_keys[option_group] = inverted_options[selected_value]


#     if selected_value not in placeholder:
#         selected_keys[option_group] = inverted_options[selected_value]
#     else:
#         selected_keys[option_group] = None
if "messages" not in st.session_state:
    st.session_state.messages = []

tot = 0
for option_group, selected_key in selected_keys.items():
    # st.write(f"In {option_group}, you selected an option with the key: {selected_key}")
    if len(selected_key) > 0:
        tot += 1

with st.chat_message("assistant"):
    st.write("You must choose a model for me to be able to help you write SQL!")

allow_input = len(selected_keys['m']) > 0
bottomText = "Input Your Choices Then Prompt the Model"
if tot > 5 and allow_input:
    bottomText = "Ask Something"
elif allow_input:
    bottomText = "You can still add some features if you want!"
elif not allow_input and len(st.session_state.messages) > 0:
    bottomText = "You must choose a model!"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if allow_input:
    if prompt := st.chat_input(bottomText):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        response, result = response_generator(selected_keys, prompt)
        with st.chat_message("assistant"):
            st.write(response)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
else:
    if prompt := st.chat_input(bottomText):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = "You must choose a model for me to be able to assist!"
        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})