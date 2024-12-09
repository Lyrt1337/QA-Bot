from transformers import pipeline
import chromadb

# ChromaDB-Client initialisieren
client = chromadb.PersistentClient(path=r"data\chroma")

# Mit der Collection "chroma_data" verbinden
collection = client.get_collection("chroma_data")

# Modell für die Antwortgenerierung
# generator = pipeline("text2text-generation", model="google/mt5-small")
generator = pipeline("text2text-generation", model="google/flan-t5-base")


def generate_response(query_text):
    # Suche nach dem Kontext in der ChromaDB
    result = collection.query(query_texts=query_text, n_results=3)  # Hole bis zu 3 Ergebnisse
    if not result["documents"]:
        return "Es wurden keine relevanten Informationen gefunden. Bitte versuche es mit einer anderen Frage."
    
    context = result["documents"][0]  # Nimm das erste Ergebnis
    
    # Generiere den Antwortprompt
    prompt = f"Kontext (Deutsch): {context}\nFrage (Deutsch): {query_text}\nAntwort (auf Deutsch):"
    
    # Modell zur Antwortgenerierung aufrufen
    response = generator(prompt, max_length=100, num_return_sequences=1)
    
    return response[0]['generated_text'].strip() if response else "Es konnte keine Antwort generiert werden."

# Beispielaufruf
response = generate_response("wie lange dauert das studium?")
print(response)