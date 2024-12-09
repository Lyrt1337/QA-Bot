# Langchain dependencies
from langchain_community.document_loaders import PyPDFLoader # Importing PDF loader from Langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter # Importing text splitter from Langchain
from langchain_community.embeddings import OpenAIEmbeddings # Importing OpenAI embeddings from Langchain
from langchain.schema import Document # Importing Document schema from Langchain
from langchain_community.vectorstores.chroma import Chroma # Importing Chroma vector store from Langchain
# from dotenv import load_dotenv # Importing dotenv to get API key from .env file
# from langchain.chat_models import ChatOpenAI # Import OpenAI LLM
import os # Importing os module for operating system functionalities
import glob
import shutil # Importing shutil module for high-level file operations

# Directory to your pdf files:
DATA_PATH = r"data\pdf\*.*"
PDF_FILE_PATHS = glob.glob(DATA_PATH)

def load_documents():
  """
  Load PDF documents from the specified directory using DirectoryLoader.
  Returns:
  List of Document objects: Loaded PDF documents represented as Langchain
                                                          Document objects.
  """
  # Initialize PDF loader with specified directory
  documents = []
  for i in PDF_FILE_PATHS:
    document_loader = PyPDFLoader(i)
    documents.append(document_loader.load())
  # Load PDF documents and return them as a list of Document objects
  return documents

documents = load_documents() # Call the function
# Inspect the contents of the first document as well as metadata
# print(documents[3])


def split_text(documents: list[Document]):
  """
  Split the text content of the given list of Document objects into smaller chunks.
  Args:
    documents (list[Document]): List of Document objects containing text content to split.
  Returns:
    list[Document]: List of Document objects representing the split text chunks.
  """
  # Initialize text splitter with specified parameters
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, # Size of each chunk in characters
    chunk_overlap=100, # Overlap between consecutive chunks
    length_function=len, # Function to compute the length of the text
    add_start_index=True, # Flag to add start index to each chunk
  )

  # Split documents into smaller chunks using text splitter
  chunks = text_splitter.split_documents(documents)
  print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

  # Print example of page content and metadata for a chunk
  document = chunks[0]
  print(document.page_content)
  print(document.metadata)

  return chunks # Return the list of split text chunks

split_text(documents)
