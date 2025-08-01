import fitz  # PyMuPDF
from docx import Document
import os

def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def parse_files(file_paths: list[str]) -> list[dict]:
    extracted_texts = []
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            continue
        extracted_texts.append({"file_path": file_path, "text": text})
    return extracted_texts