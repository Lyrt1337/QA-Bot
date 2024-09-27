import sqlite3
import pandas as pd
from rank_bm25 import BM25Okapi
import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

nltk_data_path = r"data\nltk"
stopwords_data_path = r"data\stopwords"
print(nltk_data_path)
if not os.path.exists(nltk_data_path):
    os.mkdir(nltk_data_path)

# Lade punkt-Paket und stopwords in den spezifischen Ordner
nltk.download("punkt_tab", download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=stopwords_data_path)

# NLTK konfigurieren, den Ordner für alle zukünftigen NLTK-Daten zu nutzen
nltk.data.path.append(nltk_data_path)

# Schritt 1: SQLite-Datenbank und Dokumente initialisieren
conn = sqlite3.connect('documents.db')
cursor = conn.cursor()

# Daten abrufen
df = pd.read_sql_query("SELECT * FROM documents", conn)


# stopwords
stop_words = set(stopwords.words('german'))
stemmer = SnowballStemmer("german")
# Schritt 2: BM25 für die Suche nutzen
# Tokenisiere den Inhalt der Dokumente
tokenized_corpus = [
    [stemmer.stem(word) for word in word_tokenize(doc.lower()) if word not in stop_words]
    for doc in df['content']
]

# BM25-Modell initialisieren
bm25 = BM25Okapi(tokenized_corpus)

# Beispiel-Suchanfrage
query = "Wie melde ich mich für eine Prüfung an?"
tokenized_query = word_tokenize(query.lower())

# BM25 Scores berechnen
scores = bm25.get_scores(tokenized_query)

# Scores dem DataFrame hinzufügen
df['score'] = scores

# Schritt 3: Ergebnisse sortieren und anzeigen
df_sorted = df.sort_values(by='score', ascending=False)
print("Top-Ergebnisse:")
print(df_sorted[['title', 'content', 'score']])

# Top-Ergebnis abrufen
top_result = df_sorted.iloc[0]
print(f"Beste Übereinstimmung: {top_result['title']}\nInhalt: {top_result['content']}")




# ------------------------------------------------
def answer_question(query):
    tokenized_query = word_tokenize(query.lower())
    scores = bm25.get_scores(tokenized_query)
    df['score'] = scores
    df_sorted = df.sort_values(by='score', ascending=False)
    top_result = df_sorted.iloc[0]
    return f"Beste Übereinstimmung: {top_result['title']}\nInhalt: {top_result['content']}"

# Benutzerfrage
frage = input("Stelle eine Frage: ")
print(answer_question(frage))