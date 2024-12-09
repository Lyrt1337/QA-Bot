import sqlite3
import pandas as pd

# Verbindung zu SQLite-Datenbank herstellen
conn = sqlite3.connect('documents.db')
cursor = conn.cursor()

# Tabelle erstellen (falls sie noch nicht existiert)
cursor.execute('''
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
)
''')

# Beispiel-Daten (Anleitungen/Reglemente) einfügen
documents = [
    ("Studienordnung", "Die Prüfungsanmeldung erfolgt über das Online-Portal. Beachten Sie die Fristen."),
    ("Prüfungsordnung", "Die Abgabe der Hausarbeiten erfolgt digital."),
    ("Reglement zur Anwesenheit", "Die Anwesenheitspflicht gilt für alle Vorlesungen und Seminare.")
]

# Daten in die SQLite-Datenbank einfügen
cursor.executemany('INSERT INTO documents (title, content) VALUES (?, ?)', documents)

conn.commit()  # Änderungen speichern

# -----------------------------------------------------
# Daten aus der SQLite-Datenbank abrufen
df = pd.read_sql_query("SELECT * FROM documents", conn)
print(df)