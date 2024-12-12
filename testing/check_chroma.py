import chromadb
from chromadb.config import Settings
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# Initialisiere ChromaDB Client
client = chromadb.PersistentClient(path=r"data\chroma")




# # Bestehende Collections in ChromaDB abrufen
# collections = client.list_collections()

# # Liste der existierenden Collections ausgeben
# for collection in collections:
#     print(f"Collection: {collection.name}")

# # Überprüfen, ob 'pdf_chunks' existiert
# collection_name = "pdf_chunks"
# if not any(c.name == collection_name for c in collections):
#     print(f"Collection '{collection_name}' existiert nicht.")
# else:
#     print(f"Collection '{collection_name}' existiert.")




# Verbindung zu ChromaDB und Abruf der gespeicherten Chunks
def check_stored_chunks():
    
    # Überprüfen, ob die Collection existiert
    collection = client.get_collection("chroma_data")

    # Abfrage der ersten 5 gespeicherten Chunks
    stored_chunks = collection.get()
    print(f"Anzahl gespeicherter Chunks: {len(stored_chunks['documents'])}")
    
    for i, doc in enumerate(stored_chunks['documents'][:5]):
        print(f"Chunk {i+1}: {doc}")
        print(f"Metadaten: {stored_chunks['metadatas'][i]}")
    
# check_stored_chunks()


def abfrage():
    
    # ChromaDB-Client und Collection abrufen
    client = chromadb.Client(Settings(persist_directory=r"data\chroma"))
    collection = client.get_collection("chroma_data")

    # Testabfrage
    result = collection.query(query_text="wie lange dauert das studium?")
    print("Testabfrageergebnis:", result)

# abfrage()

collections = client.list_collections()
print("Verfügbare Collections:", collections)


# collection = client.get_collection("chroma_data")
# result = collection.query(query_texts=["wie lange dauert das studium?"])
# print("Testabfrageergebnis:", result)