from PyPDF2 import PdfReader

path = r"data\pdf\A_probabilistic_justification_for_using_tfidf_term.pdf"
try:
    reader = PdfReader(path)
    print(reader.pdf_header)
    for page in reader.pages:
        print(page.extract_text())
except Exception as e:
    print(f"Fehler beim Laden der PDF: {e}")