from flask import Flask, request, jsonify
from chromadb.config import Settings
import chromadb

# Flask-App initialisieren
app = Flask(__name__)

# Verbindung zu ChromaDB herstellen
client = chromadb.Client(Settings(
    persist_directory=r"data\chroma"  # Verzeichnis mit der gespeicherten DB
))

# Collection laden
collection_name = "pdf_chunks"  # Name deiner Collection
collection = client.get_or_create_collection(collection_name)

@app.route('/query', methods=['POST'])
def query_chromadb():
    """
    API-Endpunkt für eine Abfrage an ChromaDB.
    Erwartet ein JSON-Objekt mit 'query' und optional 'n_results'.
    """
    try:
        # JSON-Daten aus der Anfrage lesen
        data = request.json
        query_text = data.get("query", "")
        n_results = data.get("n_results", 5)  # Standardmäßig 5 Ergebnisse
        
        if not query_text:
            return jsonify({"error": "Query text is required."}), 400
        
        # Abfrage an ChromaDB
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Ergebnisse zurückgeben
        return jsonify({
            "query": query_text,
            "results": [
                {"document": doc, "distance": dist}
                for doc, dist in zip(results["documents"], results["distances"])
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)

