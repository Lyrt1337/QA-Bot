from transformers import pipeline
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk, Image
import chromadb

# General settings
# Colors
window_color = "#3d3c39"
font_color = "white"
font = "Arial"

# Image paths
icon_path = r"img\fhgr_logo.ico"
background_path = r"img\bg2.png"
send_button_path = r"img\send2.png"

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=r"data\chroma")

# Connect to "chroma_data" collection
collection = client.get_collection("chroma_data")

# Answer generation model
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def generate_response(query_text):
    # Suche nach Kontext in ChromaDB
    result = collection.query(query_texts=query_text, n_results=5)
    if not result["documents"]:
        return "Es wurden keine relevanten Informationen gefunden."
    
    context = ' '.join([str(doc).strip() for doc in result["documents"][:5]]) # first 3 documents
    
    # Überprüfen, ob der Kontext ein gültiger String ist
    if not isinstance(context, str) or not context.strip():
        return "Kontext konnte nicht verarbeitet werden."
    
    # Begrenze den Kontext auf 512 Zeichen
    context = context[:1024]
    print(context)
    
    # Frage-Antwort-Modell aufrufen
    try:
        response = qa_pipeline({
            "question": query_text,
            "context": context
        }, max_answer_len=100)
        return response["answer"] if response else "Es konnte keine Antwort generiert werden."
    except Exception as e:
        return f"Fehler bei der Antwortgenerierung: {str(e)}"


# Callback function for results
def on_submit():
    # Abfrage von der Eingabe im Textfeld holen
    query_text = entry.get("1.0", tk.END).strip()
    if not query_text:
        return

    # Show user input
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"Du: {query_text}\n\n")
    output_text.config(state=tk.DISABLED)

    # Generate response
    response = generate_response(query_text)

    # Show bot answer
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"Bot: \n{response}\n\n\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)  # Scroll to the end
    
    # Empty entry field
    entry.delete("1.0", tk.END)

# Initialize tkinter window
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

# Send Button
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

# Text box for conversation
output_text = scrolledtext.ScrolledText(chat_frame,
                                        wrap=tk.WORD,
                                        fg=font_color,
                                        font=font,
                                        borderwidth=0,
                                        width=60,
                                        height=35)

output_text.pack(fill=tk.BOTH, expand=True)
output_text.config({"background": window_color})

# Input box for prompts
entry = tk.Text(prompt_frame,
                fg=font_color,
                font=font,
                borderwidth=0,
                width=60)
entry.place(relwidth=1, relheight=1)
entry.config({"background": window_color})

# Send button
submit_button = tk.Button(send_frame,
                          image=send_button_image,
                          borderwidth=0,
                          bg=window_color,
                          highlightcolor=window_color,
                          activebackground=window_color,
                          bd=0,
                          highlightbackground=window_color,
                          command=on_submit)

submit_button.pack(side="left")
# Bind the Enter key to the send_message function
entry.bind("<Return>", lambda event=None: on_submit())

# Tkinter mainloop
root.mainloop()
