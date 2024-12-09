import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk, Image
from transformers import pipeline
import chromadb


# general settings
# colors
window_color = "#3d3c39"
font_color = "white"
font = "Arial"
# image-paths
icon_path = r"img\fhgr_logo.ico"
background_path = r"img\bg2.png"
send_button_path = r"img\send2.png"
# ChromaDB-Client initialisieren
client = chromadb.PersistentClient(path=r"data\chroma")

# Mit der Collection "chroma_data" verbinden
collection = client.get_collection("chroma_data")

# Modell für die Antwortgenerierung
generator = pipeline("text2text-generation", model="google/flan-t5-base")
# generator = pipeline("text2text-generation", model="t5-large-generation-squad-QuestionAnswer")

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
    query_text = entry.get("1.0", tk.END)
    if not query_text.strip():
        return

    # Benutzer-Input anzeigen
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"Du: {query_text}\n\n")
    output_text.config(state=tk.DISABLED)

    # Antwort generieren
    response = generate_response(query_text)

    # Antwort im Ausgabebereich anzeigen
    # output_text.delete(1.0, tk.END)  # Löscht vorherige Antwort
    # output_text.insert(tk.END, response)  # Setzt die neue Antwort ein

    # Bot-Antwort anzeigen
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"Bot: {response}\n\n\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)  # Scroll to the end
    
    # Eingabefeld leeren
    entry.delete("1.0", tk.END)

# Tkinter Fenster initialisieren
width, height = 1080, 720
root = tk.Tk()
root.title("FHGR - QA-Bot")
root.iconbitmap(icon_path)
root.geometry(f"{width}x{height}")
root.resizable(False, False)

# Images
# Background Label
img_open_bg = Image.open(background_path)
resized_bg = img_open_bg.resize((width, height), resample=Image.Resampling.LANCZOS)
bg = ImageTk.PhotoImage(resized_bg)
background_label = tk.Label(root, image=bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# send Button
img_open_send = Image.open(send_button_path)
resized_send = img_open_send.resize((50, 50), resample=Image.Resampling.LANCZOS)
send_button_image = ImageTk.PhotoImage(resized_send)


# Frames
chat_frame = tk.Frame(root, bd=0, bg=window_color)
chat_frame.place(relwidth=0.7, relheight=0.6, relx=0.15, rely=0.1)

prompt_frame = tk.Frame(root, bd=0, bg=window_color)
prompt_frame.place(relwidth=0.64, relheight=0.1, relx=0.15, rely=0.75)

send_frame = tk.Frame(root, bd=0, bg=window_color)
send_frame.place(relwidth=0.06, relheight=0.1, relx=0.79, rely=0.75)

# options_frame = tk.Frame(root, bd=3,)
# options_frame.place(relwidth=0.1, relheight=0.1, relx=0.01, rely=0.9)
# options_frame.config(background="#03071e")

# Textfeld zur Anzeige der Antwort
output_text = scrolledtext.ScrolledText(chat_frame,
                                        wrap=tk.WORD,
                                        fg=font_color,
                                        font=font,
                                        borderwidth=0,
                                        width=60,
                                        height=35)
# output_text.pack(padx=10, pady=10)
output_text.pack(fill=tk.BOTH, expand=True)
output_text.config({"background": window_color})

# Eingabefeld für die Frage
user_input_var = tk.StringVar()
entry = tk.Text(prompt_frame,
                #  textvariable=user_input_var,
                 fg=font_color,
                 font=font,
                 borderwidth=0,
                 width=60)
entry.place(relwidth=1, relheight=1)
# entry.pack(padx=10, pady=10)
entry.config({"background": window_color})

# Button zum Absenden der Frage
submit_button = tk.Button(send_frame,
                          image=send_button_image,
                          borderwidth=0,
                          bg = window_color,
                          highlightcolor = window_color,
                          activebackground= window_color,
                          bd = 0,
                          highlightbackground = window_color,
                          command=on_submit)
# submit_button.pack(pady=10)
submit_button.pack(side="left")
# bind the Enter key to the send_message function
entry.bind("<Return>", lambda event=None: on_submit())



# Tkinter-Schleife starten
root.mainloop()
