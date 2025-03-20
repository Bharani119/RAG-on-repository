import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-small-1",
    # Set the flag to False for models which do not support token ids in inputs
    check_embedding_ctx_length=False,
)

llm = AzureChatOpenAI(
    # azure_deployment="gpt-4o-mini-2024-07-18",
    azure_deployment="gpt-4o",
)

db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

## Design ChatPrompt Template
prompt = ChatPromptTemplate.from_template(
    """
Answer the following question based only on the provided context.
<context>
{context}
</context>
Question: {input}"""
)

## Create Stuff Document Chain
document_chain = create_stuff_documents_chain(llm, prompt)

## create retriever
retriever = db.as_retriever()

# create chain
retrieval_chain = create_retrieval_chain(retriever, document_chain)
