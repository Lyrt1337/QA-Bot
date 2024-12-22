# FHGR QA-Bot Projekt

## 🌐 Beschreibung
Dieses Projekt implementiert einen Frage-Antwort-Bot (QA-Bot) basierend auf Informationen, die aus mehreren PDF-Dokumenten extrahiert wurden. Die Dokumente werden in einer persistenten Chroma-Datenbank gespeichert, und ein Transformer-Modell wird verwendet, um relevante Antworten auf Benutzeranfragen zu generieren. Die Anwendung bietet eine benutzerfreundliche GUI mit Tkinter und nutzt Huggin Face, um embeddings zu erzeugen und die Dokumente effizient abzufragen.

---

## 🔧 Technologien
- **Programmiersprache:** Python
- **Bibliotheken:**
  - Transformers
  - ChromaDB
  - Tkinter
  - SentenceTransformers
  - Pillow
  - PyMuPDF
  - NLTK

---

## 🔍 Hauptfunktionen
1. **Datenbankerstellung**:
   - Extrahiert Text aus PDF-Dokumenten und speichert sie in einer Chroma-Collection.
   - Nutzt LangChain zur Erstellung von embeddings mit SentenceTransformer.
2. **Frage-Antwort-Logik**:
   - Findet relevante Kontexte mit „similarity search“ in der Chroma-Datenbank.
   - Generiert Antworten mit Transformer-Modell Google Gemini.
3. **Benutzeroberfläche**:
   - Ermöglicht Benutzern, Fragen einzugeben und die Antworten in einem scrollbaren Chatfenster anzuzeigen.
   - Anzeige von Fehlermeldungen, wenn keine passenden Informationen gefunden werden.

---

## ⚙️ Einrichtung und Installation

### Voraussetzungen
- Python >= 3.8
- Installierte Abhängigkeiten (siehe unten)

### Schritte zur Installation
**Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```
**Datenbank initialisieren**:
   - Platziere alle PDF-Dateien im Ordner `data/pdfs`.
   - Starte das Skript zur Indexierung:
     ```bash
     python index_pdfs.py
     ```

---

## ⚛️ Verwendung

1. **Anwendung starten**:
   ```bash
   python app.py
   ```
2. **Fragen stellen**:
   - Gib im Eingabefeld eine Frage ein und drücke Enter oder den Senden-Button.
   - Der Bot sucht relevante Informationen in der Datenbank und gibt eine Antwort aus.
3. **Datenbank verwalten**:
   - Um neue PDFs hinzuzufügen, speichere sie im Ordner `data/pdfs` und starte das Skript `index_pdfs.py` erneut.

---

## 🔎 Wichtige Dateien
- **app.py**: Hauptskript für die Tkinter-Anwendung.
- **index_pdfs.py**: Skript zum Verarbeiten und Indexieren der PDF-Dateien in ChromaDB.
- **data/**: Verzeichnis für PDF-Dateien und persistente Datenbank.
- **requirements.txt**: Liste der Python-Abhängigkeiten.
- **img/**: Ressourcen für die Benutzeroberfläche (Icons, Hintergrundbilder).

---

## ⚡ Tipps zur Optimierung
1. **Antwortlänge anpassen**:
   - Passe die maximale Länge `k` in der Antwortgenerierungslogik an, um abgeschnittene Antworten zu vermeiden. **vector_db.similarity_search_with_score(query, k=6)**

2. **Kontextgröße begrenzen**:
   - Passe die `chunk_size` und den `overlap` in **index_pdfs.py** an.

---