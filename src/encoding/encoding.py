from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

import configparser
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility


def connect_milvus():
    # Connect to Milvus server and return the connection object
    cfp = configparser.RawConfigParser()
    cfp.read('./config_serverless.ini')
    milvus_uri = cfp.get('prior-knowledge', 'uri')
    token = cfp.get('prior-knowledge', 'token')
    connections.connect("default",
                        uri=milvus_uri,
                        token=token)
    print(f"Connecting to DB: {milvus_uri}")

# Inject prior knowledge into vectorized database
