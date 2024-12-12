import os
import signal
import sys
import google.generativeai as genai

# from langchain_community.vectorstores.chroma import Chroma
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

GEMINI_API_KEY = "AIzaSyBS9jeD7MMPwm_kaoBaYfdoAyAnC7AtETE"

def signal_handler(sig, frame):
    print("\nThanks for using Gemini. :)")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_rag_prompt(query, context):
    escaped = context.replace("'", "").replace('"', "").replace("\n", " ")
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
    embedding_function = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                             model_kwargs={"device": "cpu"})
    vector_db = Chroma(persist_directory=r"data\chroma", embedding_function=embedding_function)
    search_results = vector_db.similarity_search(query, k=6)

    for result in search_results:
        context += result.page_content + "\n"
    
    return context


def generate_answer(prompt):
    genai.configure(api_key=GEMINI_API_KEY)
    model =genai.GenerativeModel(model_name="gemini-pro")
    answer= model.generate_content(prompt)
    return answer.text

welcome_text = generate_answer("Kannst du dich kurz vorstellen?")
print(welcome_text)


while True:
    print("-------------------------------")
    print("Was möchtest du fragen?")
    query = input("Query: ")
    print(query)
    context = get_relevant_context_from_db(query)
    # print(context)
    prompt = generate_rag_prompt(query, context)
    # print(prompt)
    answer = generate_answer(prompt)
    print(answer)

