import re
import os
import nltk
from nltk.tokenize import sent_tokenize
import chromadb
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# settings
chunk_size = 500
overlap = 200
# nltk
nltk_data_path = r"data\nltk"
stopwords_data_path = r"data\stopwords"
print(nltk_data_path)
if not os.path.exists(nltk_data_path):
    os.mkdir(nltk_data_path)

# Load punkt and stopwords in specified folder
nltk.download("punkt_tab", download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=stopwords_data_path)

# configure NLTK for future use
nltk.data.path.append(nltk_data_path)

# db client
client = chromadb.PersistentClient(path=r"data\chroma")

collection_name = "chroma_data"
try:
    collection = client.get_collection(collection_name)
except Exception:
    collection = client.create_collection(collection_name)


# Funktion, um Text in Chunks mit Overlap zu teilen
# def create_chunks(text, chunk_size=300, overlap=100):
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = min(start + chunk_size, len(text))
#         chunk = text[start:end]
#         chunks.append(chunk)
#         start += chunk_size - overlap
#     return chunks

def create_chunks(text, max_chunk_size=chunk_size, overlap_size=overlap):
    """
    Creates chunks for given text, with full sentences only and adds an overlap.
    
    Args:
        text (str): Text that needs to be chunked.
        max_chunk_size (int): Maximal chunk lenght in characters.
        overlap_size (int): Overlap betwen two adjacent chunks in characters.
    
    Returns:
        list: List of chunks.
    """
    sentences = sent_tokenize(text)  # Separate text in sentences
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        
        # if the current chunk is "full" add it
        if current_length + sentence_length > max_chunk_size:
            # Füge den aktuellen Chunk hinzu
            chunks.append(" ".join(current_chunk))
            
            # start a new chunk, start with the overlap
            overlap = " ".join(current_chunk)[-overlap_size:]
            current_chunk = [overlap] if overlap else []
            current_length = len(overlap)
        
        # add the current sentence to the chunk
        current_chunk.append(sentence)
        current_length += sentence_length + 1  # +1 spr spaces

    # add final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# load PDF and extract text
def extract_pdf_content(file_path):
    reader = PdfReader(file_path)
    pdf_content = ""
    for page in reader.pages:
        pdf_content += page.extract_text()
    
    # removes hyphen and joins separated words
    pdf_content = re.sub(r'(\w)-\n(\w)', r'\1\2', pdf_content)
    # removes line-breaks
    pdf_content = re.sub(r'\n+', ' ', pdf_content)
    # removes double-spaces
    pdf_content = re.sub(r'\s+', ' ', pdf_content).strip()
    return pdf_content

# create embeddings for chunks and save to ChromaDB
def store_in_chromadb(pdf_content, metadata, chunk_size=chunk_size, overlap=overlap):
    # load or create ChromaDB Collection laden
    collection = client.get_collection("chroma_data")

    # load SentenceTransformer Model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # create Chunks
    chunks = create_chunks(pdf_content, chunk_size, overlap)

    # itterate chunks and create embeddings
    for i, chunk in enumerate(chunks):
        chunk_id = f"{metadata['title']}_chunk_{i+1}"
        embedding = model.encode(chunk)
        
        # Chunk in ChromaDB speichern
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "chunk_id": chunk_id, 
                "page_number": metadata.get("page_number", "unknown"), 
                "title": metadata.get("title", "unknown"),
                "author": metadata.get("author", "unknown")
            }],
            ids=[chunk_id]
        )
        print(f"Chunk {chunk_id} gespeichert.")
        
    print("Alle Chunks erfolgreich in ChromaDB gespeichert.")

# define data (PDF's) to be read and add metadata
pdf_path = r"data\pdf\FHGR-Bachelorstudium-Computational_and_Data_Science-Studienbroschuere.pdf"
metadata = {
    "title": "Beispiel PDF",
    "author": "John Doe",
    "page_number": 1
}

# extract PDF-contents
pdf_content = extract_pdf_content(pdf_path)

# save to ChromaDB with persistence
store_in_chromadb(pdf_content, metadata)


