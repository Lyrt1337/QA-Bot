import chromadb
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path=r"data\chroma")

collection_name = "pdf_chunks"
try:
    collection = client.get_collection(collection_name)
except Exception:
    collection = client.create_collection(collection_name)


# Funktion, um Text in Chunks mit Overlap zu teilen
def create_chunks(text, chunk_size=300, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# PDF-Datei laden und Text extrahieren
def extract_pdf_content(file_path):
    reader = PdfReader(file_path)
    pdf_content = ""
    for page in reader.pages:
        pdf_content += page.extract_text()
    return pdf_content

# Embeddings für Chunks erstellen und in ChromaDB speichern
def store_in_chromadb(pdf_content, metadata, chunk_size=300, overlap=100):
    # ChromaDB Collection laden (oder erstellen)
    collection = client.get_collection("pdf_chunks")

    # SentenceTransformer Model laden
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Chunks erstellen
    chunks = create_chunks(pdf_content, chunk_size, overlap)

    # Chunks durchgehen und Embeddings erstellen
    for i, chunk in enumerate(chunks):
        chunk_id = f"{metadata['title']}_chunk_{i+1}"  # ID für den Chunk
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

# Beispiel zur Speicherung mit Persistenz
pdf_path = r"data\pdf\A Comparative Study on TF-IDF feature Weighting Method and its Analysis using Unstructured Dataset.pdf"
metadata = {
    "title": "Beispiel PDF",
    "author": "John Doe",
    "page_number": 1  # Beispiel Metadaten, anpassen nach Bedarf
}

# PDF-Inhalt extrahieren (wie zuvor)
pdf_content = extract_pdf_content(pdf_path)

# Speichern in ChromaDB mit Persistenz
store_in_chromadb(pdf_content, metadata)
