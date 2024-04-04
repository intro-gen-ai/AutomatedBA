from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain



"""
Original chain needs to pass "original_chain.memory.chat_memory.messages", 

where memory is declared:
original_chain = ConversationChain(
    llm=ChatOpenAI(temperature=0, model_name=''),
    memory=ConversationBufferMemory()
)
    
"""
def get_efficiency(chat):
    history = ChatMessageHistory(messages=chat)
    memory = ConversationBufferMemory(chat_memory=history)
    llm = ChatOpenAI(temperature=0, model_name='')
    
    n_chain = ConversationChain(
        llm=llm,
        verbose=False,
        memory=memory)
    res = n_chain.run('Provide a "Yes" or "No" as response. Is the generated SQL query the most efficient option?')
    if res == "Yes":
        return None
    else:
        res = n_chain.run('Provide a more efficient SQL query.')
        return res