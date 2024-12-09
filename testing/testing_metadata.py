from PyPDF2 import PdfReader

# def get_pdf_metadata(file_path):
#     # PDF einlesen
#     reader = PdfReader(file_path)
#     metadata = reader.metadata  # Metadaten auslesen
    
#     # Ergebnisse anzeigen
#     if metadata:
#         print("PDF-Metadaten:")
#         for key, value in metadata.items():
#             print(f"{key}: {value}")
#     else:
#         print("Keine Metadaten gefunden.")
    
#     return metadata

# # Beispiel
# file_path = r"data\pdf\FHGR-Bachelorstudium-Computational_and_Data_Science-Studienbroschuere.pdf"
# metadata = get_pdf_metadata(file_path)


import chromadb
from chromadb.config import Settings


# Initialisiere die ChromaDB-Verbindung
client = chromadb.PersistentClient(path=r"data\chroma")

# Collection laden
collection_name = "chroma_data"
collection = client.get_collection(collection_name)

# Abfrage mit Metadaten
query_text = "Was ist Computational Science?"
results = collection.query(
    query_texts=[query_text],
    n_results=5  # Anzahl der gewünschten Ergebnisse
)

# Ergebnisse mit Metadaten ausgeben
for i, metadata in enumerate(results["metadatas"]):
    # print(f"Ergebnis {i+1}:")
    # print(f"Dokument-ID: {results['ids'][i]}")
    print(f"Metadaten: {metadata}")
    # print(f"Text: {results['documents'][i]}")
    # print("-" * 40)