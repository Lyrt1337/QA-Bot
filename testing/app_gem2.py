import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk, Image
from transformers import T5Tokenizer, pipeline
import chromadb

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import google.generativeai as genai


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
collection_name = "chroma_data_L12_cos"

# connect to "chroma_data" collection
collection = client.get_collection(collection_name)

# answer generation model
GEMINI_API_KEY = "AIzaSyBS9jeD7MMPwm_kaoBaYfdoAyAnC7AtETE"

def generate_rag_prompt(query, context):
    # escaped = context.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = (f"""
              Du bist ein hilfsbereiter Assistent der auf Fragen aus dem unten stehenden\
              Text beantwortet. Antworte immer mit einem Vollständigen Satz, drücke dich\
              verständlich aus und verwende alle wichtigen Informationen aus dem Text.\
              Wenn möglich, fasse dich kurz.\
              Falls der Text auch Informationen enthält, die für die Frage irrelevant sind,\
              kannst du diese Ignorieren.\
QUESTION: {query}
CONTEXT: {context}
""")
    return prompt

def get_relevant_context_from_db(query):
    context = ""
    # embedding_function = HuggingFaceBgeEmbeddings(model_name="T-Systems-onsite/cross-en-de-roberta-sentence-transformer",
    #                                          model_kwargs={"device": "cpu"})

    embedding_function = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2",
                                             model_kwargs={"device": "cpu"})
    
    
    vector_db = Chroma(collection_name = collection_name,
                       persist_directory=r"data\chroma",
                       embedding_function=embedding_function)
    # search_results = vector_db.similarity_search(query, k=6)

    # for result in search_results:
    #     context += result.page_content + "\n"

    search_results = vector_db.similarity_search_with_score(query, k=6)
    similarity_scores = []
    for result, score in search_results:
        context += result.page_content + "\n"
        corrected_score = 1 - score / 2
        print("result: ", result)
        print("score: ", corrected_score)
        similarity_scores.append(corrected_score)
    print("all scores: ", similarity_scores)

    
    return context

def generate_response(query_text):
    genai.configure(api_key=GEMINI_API_KEY)
    model =genai.GenerativeModel(model_name="gemini-pro")
    answer= model.generate_content(query_text)
    return answer.text


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

    # query DB
    context = get_relevant_context_from_db(query_text)
    prompt = generate_rag_prompt(query_text, context)
    # generate response
    response = generate_response(prompt)

    # show bot answer
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"FHGR Bot: \n{response}\n\n\n")
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
                                        height=35,
                                        )

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

# welcome message
welcome_message= "Hallo. Wie kann ich behilflich sein?"
output_text.config(state=tk.NORMAL)
output_text.insert(tk.END, f"FHGR Bot: \n{welcome_message}\n\n\n")
output_text.config(state=tk.DISABLED)
output_text.see(tk.END)  # Scroll to the end

# Tkinter mainloop
root.mainloop()
