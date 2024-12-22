# from langchain_community.vectorstores.chroma import Chroma
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter # Importing text splitter from Langchain
from langchain_community.document_loaders import PyPDFLoader # Importing PDF loader from Langchain


# from langchain_community.embeddings import OpenAIEmbeddings # Importing OpenAI embeddings from Langchain
# from langchain.schema import Document # Importing Document schema from Langchain


loaders = [PyPDFLoader("data\pdf\FHGR-Bachelorstudium-Computational_and_Data_Science-Studienbroschuere.pdf")]

docs = []

for file in loaders:
    docs.extend(file.load())

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(docs)
embedding_function = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                             model_kwargs={"device": "cpu"})

vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory=r"data\chroma")

print(vectorstore._collection.count())
