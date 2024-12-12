import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk, Image
from transformers import T5Tokenizer, pipeline
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

# initialize ChromaDB-Client
client = chromadb.PersistentClient(path=r"data\chroma")

# connect to "chroma_data" collection
# collection = client.get_collection("chroma_data")
collection = client.get_collection("langchain")

# answer generation model
# model_name = "google/mt5-base"
model_name = "google/flan-t5-base"
# model_name = "dbmdz/bert-base-german-cased"
# model_name = "deepset/gbert-base"
# model_name = "deepset/mt5-small-german-finetune-qa"
# model_name = "deepset/roberta-base-squad2"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# generator = pipeline("text2text-generation", model="google/flan-t5-base")
# generator = pipeline("text2text-generation", model="dbmdz/bert-base-german-cased")
# generator = pipeline("text2text-generation", model="deepset/gbert-base")
# generator = pipeline("text2text-generation", model="google/mt5-base")
# generator = pipeline("text2text-generation", model="deepset/mt5-small-german-finetune-qa")
generator = pipeline("text2text-generation", model=model_name)
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")

# generator = pipeline("question-answering", model=model_name)


def generate_response(query_text):
    # ChromaDB query
    result = collection.query(query_texts=query_text, n_results=3)
    if not result["documents"]:
        return "Es wurden keine relevanten Informationen gefunden. Bitte versuche es mit einer anderen Frage."
    
    context = result["documents"][0]  # take first result
    
    # generate prompt to be answered
    prompt = f"Bitte beantworte die Frage auf Deutsch: Kontext (Deutsch): {context}\nFrage (Deutsch): {query_text}\nAntwort (bitte auf Deutsch):"
    print(prompt)
    # call model for answer generation
    # response = generator(prompt, max_length=150, eos_token_id=tokenizer.eos_token_id, num_return_sequences=1)
    response = generator(prompt,
                         max_length=150,
                         min_length=50,
                        #  no_repeat_ngram_size=2,
                         num_return_sequences=1,
                         eos_token_id=tokenizer.eos_token_id,
                        #  top_p=0.9,
                        #  temperature=0.7,
                        #  do_sample=True
                         )
    response_text = response[0]['generated_text'].strip()
    response_text = response_text.rstrip("[]'\"")
    cleaned_response = response_text.split(".")
    response_text = cleaned_response[0]
    return response_text if response_text else "Es konnte keine Antwort generiert werden."


# callback function for results
def on_submit():
    # get input from text-field
    query_text = entry.get("1.0", tk.END)
    if not query_text.strip():
        return

    # show user input
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"Du: \n{query_text}\n\n")
    output_text.config(state=tk.DISABLED)

    # generate response
    response = generate_response(query_text)

    # show bot answer
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"Bot: \n{response}\n\n\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)  # Scroll to the end
    
    # empty entry field
    entry.delete("1.0", tk.END)


# initialize tkinter window
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


# frames
chat_frame = tk.Frame(root, bd=0, bg=window_color)
chat_frame.place(relwidth=0.7, relheight=0.6, relx=0.15, rely=0.1)

prompt_frame = tk.Frame(root, bd=0, bg=window_color)
prompt_frame.place(relwidth=0.64, relheight=0.1, relx=0.15, rely=0.75)

send_frame = tk.Frame(root, bd=0, bg=window_color)
send_frame.place(relwidth=0.06, relheight=0.1, relx=0.79, rely=0.75)


# text box for conversation
output_text = scrolledtext.ScrolledText(chat_frame,
                                        wrap=tk.WORD,
                                        fg=font_color,
                                        font=font,
                                        borderwidth=0,
                                        width=60,
                                        height=35)

output_text.pack(fill=tk.BOTH, expand=True)
output_text.config({"background": window_color})

# input box for prompts
user_input_var = tk.StringVar()
entry = tk.Text(prompt_frame,
                 fg=font_color,
                 font=font,
                 borderwidth=0,
                 width=60)
entry.place(relwidth=1, relheight=1)

entry.config({"background": window_color})

# send button
submit_button = tk.Button(send_frame,
                          image=send_button_image,
                          borderwidth=0,
                          bg = window_color,
                          highlightcolor = window_color,
                          activebackground= window_color,
                          bd = 0,
                          highlightbackground = window_color,
                          command=on_submit)

submit_button.pack(side="left")
# bind the Enter key to the send_message function
entry.bind("<Return>", lambda event=None: on_submit())


# Tkinter mainloop
root.mainloop()
