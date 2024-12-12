import os
import random
import matplotlib.pyplot as plt
import fitz
import os
import re
import nltk
from nltk.corpus import stopwords
from transformers import BertTokenizer
from sklearn.model_selection import train_test_split
import random
import torch
from torch.utils.data import Dataset
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from transformers import BertForSequenceClassification, AdamW
import json
# import pytesseract
# from pdf2image import convert_from_path
#Variablen deklaration
nltk.download('stopwords')
german_stopwords = set(stopwords.words('german'))


def save_texts_and_labels_json(texts, labels, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump({"texts": texts, "labels": labels}, file, ensure_ascii=False, indent=4)
    print(f"Texts and labels saved to {file_path}")

def load_texts_and_labels_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    print(f"Texts and labels loaded from {file_path}")
    return data["texts"], data["labels"]
#Funktion zum extrahieren der Texte
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    metadata = doc.metadata

    for page in doc:
        page_text = page.get_text()  # Get the text of the page
        text += page_text

    # Cleanup extracted text
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # Removes hyphen and joins words
    text = re.sub(r'\n+', ' ', text)  # Removes line breaks
    text = re.sub(r'\s+', ' ', text).strip()  # Removes extra spaces

    doc.close()
    
    return text

    # with pdfplumber.open(pdf_path) as pdf:
    #     text = ""
    #     for page in pdf.pages:
    #         page_text = page.extract_text()
    #         if page_text:  # If text is successfully extracted
    #             text += page_text
            # else:  # Use OCR as a fallback
            #     images = convert_from_path(pdf_path, first_page=page.page_number, last_page=page.page_number)
            #     ocr_text = pytesseract.image_to_string(images[0], lang='deu')  # German language OCR
            #     text += ocr_text
    # return text

import re

def clean_text(text):
   
    # Step 1: Remove CID entries in parentheses (e.g., (CID:1234) or (CID))
    text = re.sub(r"\(CID:\d+\)", "", text)  # Remove patterns like (CID:1234)
    text = re.sub(r"\(CID\)", "", text)  # Remove standalone (CID)

    # Step 2: Remove excess whitespace introduced by CID removal
    text = re.sub(r"\s+", " ", text).strip()

    # Step 3: (Optional) Remove non-German characters (retain punctuation and umlauts)
    # Customizable based on dataset specifics
    text = re.sub(r"[^a-zA-ZäöüßÄÖÜ .,!?;0-9\s-]", "", text)

    return text


#Preprocessing
def preprocess_text(text):

    text = text.lower()
    # Remove special characters
    text = re.sub(r"[^a-zäöüß0-9\s]", "", text)


    # text = re.sub(r'"cid\d+"', '', text)


    # Step 2: Remove excess whitespace introduced by CID removal
    # text = re.sub(r"\s+", " ", text).strip()

    # Tokenize and remove stopwords
    words = text.split()
    words = [word for word in words if word not in german_stopwords]
    return " ".join(words)

# Specify the folder path
# folder_path = "d:/School/QA/DataPrep/Files/full"
folder_path = r"data\pdf"


texts = []


files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

print(f"Found {len(files)} PDF files in {folder_path}.")

count = 0
for file_name in files:
    file_path = os.path.join(folder_path, file_name)

    text = preprocess_text(extract_text_from_pdf(file_path))
    texts.append(text)
    count += 1

    if count >= 100:
        break

print(f"Collected {len(texts)} samples from {folder_path}.")

# Calculate document lengths
document_lengths = [len(text.split()) for text in texts]  # Length based on word count


plt.figure(figsize=(10, 6))
plt.hist(document_lengths, bins=30, color='blue', edgecolor='black', alpha=0.7)
plt.title('Histogram of Document Lengths')
plt.xlabel('Number of Words')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)


plt.show()
plt.savefig('Histograms.png')

zero_length_files = [file_name for text, file_name in zip(texts, files) if len(text.split()) == 0]
print(f"Files with zero length content: {zero_length_files}")
