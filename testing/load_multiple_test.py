import re
import os
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
import chromadb
from sentence_transformers import SentenceTransformer

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

# Funktion, um Text in Chunks mit Overlap zu teilen
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
    sentences = sent_tokenize(text)  # Separate text in sentences
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

# PDF-Inhalt und Metadaten extrahieren
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
        page_text = page.get_text()  # Get the text of the page
        text += page_text
    
    # Cleanup extracted text
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # Removes hyphen and joins words
    text = re.sub(r'\n+', ' ', text)  # Removes line breaks
    text = re.sub(r'\s+', ' ', text).strip()  # Removes extra spaces

    doc.close()
    
    return text, metadata

# Chunks in ChromaDB speichern
def store_in_chromadb(pdf_content, metadata, chunk_size=chunk_size, overlap=overlap):
    collection = client.get_collection("chroma_data")
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Lade SentenceTransformer

    # Chunks erstellen
    chunks = create_chunks(pdf_content, chunk_size, overlap)

    # Chunks iterieren und in ChromaDB speichern
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
            }],
            ids=[chunk_id]
        )
        print(f"Chunk {chunk_id} gespeichert.")
    
    print("Alle Chunks erfolgreich in ChromaDB gespeichert.")


# Load all PDF's
folder_path = r"data\pdf"
# files_path = [os.path.abspath(x) for x in os.listdir(folder_path)]
for i in os.listdir(folder_path):
    pdf_path = os.path.join(folder_path, i)
    print(pdf_path)
    pdf_content, metadata = extract_pdf_content_with_metadata(pdf_path)
    store_in_chromadb(pdf_content, metadata)
