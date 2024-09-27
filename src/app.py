from flask import Flask, request, jsonify
import nltk
from rank_bm25 import BM25Okapi
import sqlite3
import pandas as pd
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# BM25 und Datenbank laden
conn = sqlite3.connect('documents.db', check_same_thread=False)
df = pd.read_sql_query("SELECT * FROM documents", conn)
tokenized_corpus = [word_tokenize(doc.lower()) for doc in df['content']]
bm25 = BM25Okapi(tokenized_corpus)

@app.route('/answer', methods=['POST'])
def answer_question():
    query = request.json.get('query', '')
    tokenized_query = word_tokenize(query.lower())
    scores = bm25.get_scores(tokenized_query)
    df['score'] = scores
    df_sorted = df.sort_values(by='score', ascending=False)
    top_result = df_sorted.iloc[0]
    return jsonify({
        "title": top_result['title'],
        "content": top_result['content'],
        "score": top_result['score']
    })

if __name__ == '__main__':
    app.run(debug=True)