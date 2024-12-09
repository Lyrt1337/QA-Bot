import tkinter as tk
from chromadb.config import Settings
import chromadb

# 1. ChromaDB initialisieren
client = chromadb.Client(Settings(persist_directory=r"data\chroma"))
collection = client.get_or_create_collection("chroma_data")

# 2. Funktion für die Abfrage
def query_chromadb(query_text):
    results = collection.query(
        query_texts=[query_text],
        n_results=1
    )
    if results["documents"]:
        return results["documents"][0]  # Erster Treffer
    return "Keine passende Antwort gefunden."

# 3. Funktion für den Chatbot-Flow
def handle_chat():
    user_input = user_input_var.get()
    if not user_input.strip():
        return
    
    # Benutzer-Input anzeigen
    chat_output.config(state=tk.NORMAL)
    chat_output.insert(tk.END, f"Du: {user_input}\n")
    chat_output.config(state=tk.DISABLED)
    
    # Antwort von ChromaDB abrufen
    response = query_chromadb(user_input)
    chat_output.config(state=tk.NORMAL)
    chat_output.insert(tk.END, f"Bot: {response}\n\n")
    chat_output.config(state=tk.DISABLED)
    
    # Eingabefeld leeren
    user_input_var.set("")

# 4. GUI erstellen
root = tk.Tk()
root.title("ChromaDB Chatbot")

# Chat-Ausgabe-Box
chat_output = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, height=20, width=50)
chat_output.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Eingabefeld
user_input_var = tk.StringVar()
user_input_entry = tk.Entry(root, textvariable=user_input_var, width=40)
user_input_entry.grid(row=1, column=0, padx=10, pady=5)

# Senden-Button
send_button = tk.Button(root, text="Senden", command=handle_chat)
send_button.grid(row=1, column=1, padx=10, pady=5)

# GUI starten
root.mainloop()
