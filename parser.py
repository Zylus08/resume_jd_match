import pdfplumber
from docx import Document

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return " ".join(p.text for p in doc.paragraphs)

    else:
        raise ValueError("Unsupported file type")
