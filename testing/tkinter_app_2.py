import tkinter as tk
from chromadb.config import Settings
import chromadb
from transformers import pipeline

# 1. Hugging Face Modell laden
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# 2. ChromaDB initialisieren
client = chromadb.Client(Settings(persist_directory=r"data\chroma"))
collection = client.get_or_create_collection("chroma_data")

# 3. Funktion für die Abfrage in ChromaDB
# def query_chromadb(query_text):
#     results = collection.query(
#         query_texts=[query_text],
#         n_results=1
#     )
#     print(results)
#     if results["documents"]:
#         return results["documents"][0]  # Erster Treffer
#     return None

# # 4. Hugging Face Modell für Antwortgenerierung
# def generate_response(context, query_text):
#     # Prompt für das Sprachmodell
#     prompt = (
#         f"Kontext (Deutsch): {context}\n"
#         f"Frage (Deutsch): {query_text}\n"
#         f"Antwort (auf Deutsch):"
#     )
#     print("context: ", context)
#     print("Query: ", query_text)
#     response = generator(prompt, max_length=100, num_return_sequences=1)
#     return response[0]['generated_text'] if response else "Es konnte keine Antwort generiert werden."


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


# 5. Funktion für den Chatbot-Flow
def handle_chat():
    user_input = user_input_var.get()
    if not user_input.strip():
        return
    
    # Benutzer-Input anzeigen
    chat_output.config(state=tk.NORMAL)
    chat_output.insert(tk.END, f"Du: {user_input}\n")
    chat_output.config(state=tk.DISABLED)
    
    # Kontext aus ChromaDB abrufen
    response = generate_response(user_input)

    # context = query_chromadb(user_input)
    # if context is None:
    #     response = "Ich konnte keine passende Antwort finden."
    # else:
    #     # Antwort mit Sprachmodell generieren
    #     response = generate_response(context, user_input)
    
    # Bot-Antwort anzeigen
    chat_output.config(state=tk.NORMAL)
    chat_output.insert(tk.END, f"Bot: {response}\n\n")
    chat_output.config(state=tk.DISABLED)
    
    # Eingabefeld leeren
    user_input_var.set("")

# 6. GUI erstellen
root = tk.Tk()
root.title("ChromaDB + Hugging Face Chatbot")

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
