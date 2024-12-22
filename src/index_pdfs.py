import re
import os
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime

# Settings
chunk_size = 500
overlap = 200

# NLTK
nltk_data_path = r"data\nltk"
stopwords_data_path = r"data\stopwords"

# create folder, if it does not exist
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# check for existing nltk packages and download if needed
nltk.data.path.append(nltk_data_path)

# check "punkt"
try:
    nltk.data.find("tokenizers/punkt")
    print("Punkt ist bereits vorhanden.")
except LookupError:
    print("Lade Punkt herunter...")
    nltk.download("punkt", download_dir=nltk_data_path)

# check "stopwords"
try:
    nltk.data.find("corpora/stopwords")
    print("Stopwords sind bereits vorhanden.")
except LookupError:
    print("Lade Stopwords herunter...")
    nltk.download("stopwords", download_dir=stopwords_data_path)


# ChromaDB Client
client = chromadb.PersistentClient(path=r"data\chroma")
collection_name = "chroma_data"
try:
    collection = client.get_collection(collection_name)
except Exception:
    collection = client.create_collection(collection_name)


def create_chunks(text, max_chunk_size=chunk_size, overlap_size=overlap):
    """
    Creates chunks for given text, with full sentences only and adds an overlap.
    
    Args:
        text (str): Text that needs to be chunked.
        max_chunk_size (int): Maximal chunk length in characters.
        overlap_size (int): Overlap between two adjacent chunks in characters.
    
    Returns:
        list: List of chunks.
    """
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        
        # If the current chunk is "full", add it
        if current_length + sentence_length > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            
            # Start a new chunk, include the overlap
            overlap = " ".join(current_chunk)[-overlap_size:]
            current_chunk = [overlap] if overlap else []
            current_length = len(overlap)
        
        # Add the current sentence to the chunk
        current_chunk.append(sentence)
        current_length += sentence_length + 1  # +1 for spaces

    # Add final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# extract PDF content and metadata
def extract_pdf_content_with_metadata(file_path):
    """
    Extracts text and metadata from a PDF using PyMuPDF.

    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        tuple: (text, metadata) - The extracted text and a metadata dictionary.
    """
    doc = fitz.open(file_path)
    text = ""
    metadata = doc.metadata

    # Iterate over all pages to extract text
    for page in doc:
        page_text = page.get_text()
        text += page_text
    
    # Cleanup extracted text
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    doc.close()
    
    return text, metadata

# save Chunks to ChromaDB
def store_in_chromadb(pdf_content, metadata, doc_count, total_num_docs, chunk_size=chunk_size, overlap=overlap):
    collection = client.get_collection(collection_name)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    chunks = create_chunks(pdf_content, chunk_size, overlap)

    # itterate chunks, encode, and save to chromaDB
    for i, chunk in enumerate(chunks):
        chunk_id = f"{metadata.get('title', 'unknown')}_chunk_{i+1}"
        embedding = model.encode(chunk)
        
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "chunk_id": chunk_id,
                "title": metadata.get("title", "unknown"),
                "author": metadata.get("author", "unknown"),
                "creation_date": metadata.get("creationDate", "unknown"),
                "mod_date": metadata.get("modDate", "unknown"),
                # "hnsw:space": "cosine" # toggle for cosine similarity
            }],
            ids=[chunk_id]
        )
        print(f"[{doc_count}/{total_num_docs}] Chunk {chunk_id} gespeichert.")



start_time = datetime.now()
print(f"start time: {start_time}")

# Load all PDF's
folder_path = r"data\pdf"
all_docs = []
for path, subdirs, files in os.walk(r"data\pdf"):
    for name in files:
        file = os.path.join(path, name)
        all_docs.append(file)
doc_count = 0
for i in all_docs:
    total_num_docs = len(all_docs)
    doc_count += 1
    pdf_content, metadata = extract_pdf_content_with_metadata(i)
    store_in_chromadb(pdf_content, metadata, doc_count, total_num_docs)

end_time = datetime.now()
duration = end_time - start_time
print("[DONE] Alle Chunks erfolgreich in ChromaDB gespeichert.")
print(f"Duration: {duration}")
