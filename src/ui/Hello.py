import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("Welcome to Automated BA!")

st.sidebar.success("Select from out options above!")

st.markdown(
    """
    Automated BA is a project to run tests of multiple different configurations 
    around models to build more efficient ways to encode BA operations into
    Sql and to display the output data effectively!
    ** Choose the Tutorial to begin!
    The tutorial will walk you through setting up the proper interface on your snowflake account
    then walk you through testing it with prompts and getting SQL outputs
    ### Configurations Page
    Will walk through your database and allow access and require documenting what each row in 
    allowed tables is. Remember to save this at the end so that it can be used!
    ### Query Page
    This is how you interact with the product!
    """
)