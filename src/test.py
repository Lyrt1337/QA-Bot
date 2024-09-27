import nltk
import os

# Setze explizit den Download-Pfad
nltk_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nltk_data")

# Füge den Download-Pfad zu den NLTK-Datenpfaden hinzu
nltk.data.path.append(nltk_data_path)

# Lade punkt in diesen Pfad herunter
nltk.download("punkt_tab", download_dir=nltk_data_path)

# Teste, ob der Tokenizer funktioniert
from nltk.tokenize import word_tokenize

text = "Dies ist ein einfacher Test."
print(word_tokenize(text))
