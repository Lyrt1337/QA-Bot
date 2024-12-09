import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline
import chromadb

# ChromaDB-Client initialisieren
client = chromadb.PersistentClient(path=r"data\chroma")

# Mit der Collection "chroma_data" verbinden
collection = client.get_collection("chroma_data")

# Modell für die Antwortgenerierung
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# Funktion zur Generierung der Antwort
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

# Callback-Funktion für die Eingabe
def on_submit():
    # Abfrage von der Eingabe im Textfeld holen
    query_text = entry.get()

    # Antwort generieren
    response = generate_response(query_text)

    # Antwort im Ausgabebereich anzeigen
    output_text.delete(1.0, tk.END)  # Löscht vorherige Antwort
    output_text.insert(tk.END, response)  # Setzt die neue Antwort ein

# Tkinter Fenster initialisieren
root = tk.Tk()
root.title("Chat-Bot")


# Textfeld zur Anzeige der Antwort
output_text = scrolledtext.ScrolledText(root, width=60, height=10)
output_text.pack(padx=10, pady=10)
# Eingabefeld für die Frage
entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)

# Button zum Absenden der Frage
submit_button = tk.Button(root, text="Frage stellen", command=on_submit)
submit_button.pack(pady=10)



# Tkinter-Schleife starten
root.mainloop()
