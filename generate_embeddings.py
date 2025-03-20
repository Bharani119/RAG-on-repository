import git
import os
import sys
from dotenv import load_dotenv
from tqdm import tqdm
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings


load_dotenv()


repo_url = "https://github.com/vanna-ai/vanna.git"
repo_dir = "./repo"

if not os.path.exists(repo_dir) and not os.path.exists("faiss_index/"):
    git.Repo.clone_from(repo_url, repo_dir)
else:
    print("Embeddings exist")
    sys.exit()

loader = GenericLoader.from_filesystem(
    "./repo",
    glob="**/[!.]*",
    suffixes=[".py", ".md", ".txt"],
    parser=LanguageParser(),
    show_progress=True,
)

documents = loader.load()
# pprint(documents[::-1])
print("Number of files", len(documents))
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)

print("splitting documents")
docs = text_splitter.split_documents(documents)
# pprint(docs[::-1])
print("Number of Documents:", len(docs))


embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-small-1",
    # Set the flag to False for models which do not support token ids in inputs
    check_embedding_ctx_length=False,
)

print("creating embeddings")
db = None
with tqdm(total=len(docs), desc="Ingesting documents") as pbar:
    for d in docs:
        if db:
            db.add_documents([d])
        else:
            db = FAISS.from_documents([d], embeddings)
        pbar.update(1)
# db = FAISS.from_documents(docs, embeddings)
print("Storing embeddings in faiss_index")
db.save_local("faiss_index")
