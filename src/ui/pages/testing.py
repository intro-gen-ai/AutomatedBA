import sys
from pathlib import Path

if __name__ == '__main__':
    # Get the absolute path to the directory containing cmdline.py
    current_dir = Path(__file__).parent.absolute()

    # Get the project root directory by going up two levels from the current directory
    # Adjust the number of parents based on your project structure
    project_root = current_dir.parent.parent.parent

    # Add the project root directory to sys.path
    sys.path.insert(0, str(project_root))

from src.util import ControlDict


# optionset = ControlDict()
# data_dict = optionset.data_dict

# for option_group, options in data_dict.items():
#     # Create a select box for each option group
#     # The key parameter is important to ensure each selectbox is unique
#     # selected_option = container.selectbox(
#     #     label=option_group,
#     #     options=list(options.keys()),
#     #     key=option_group
#     # )
#     print(option_group)
#     print(options)

import streamlit as st

# Top Component with Select Boxes Side-by-Side
col1, col2 = st.columns(2)  # Create two columns

with col1:  # First select box in the first column
    option1 = st.selectbox('Select Option 1:', ('Option 1', 'Option 2', 'Option 3'))

with col2:  # Second select box in the second column
    option2 = st.selectbox('Select Option 2:', ('A', 'B', 'C'))

# Middle Component for Messages and Responses
with st.container():
    for i in range(10):  # Example range, adjust based on your array of messages
        st.text(f"Message {i}: Hello!")
        st.text(f"Response {i}: Hi there!")
        st.write("---")  # Separator line

# Bottom Component with a Text Box
user_message = st.text_input("Type your message here:")
if st.button("Send"):
    st.write(f"Your message: {user_message}")
    # Here you would add the functionality to send/display the message
