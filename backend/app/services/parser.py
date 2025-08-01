import os

# Import PyMuPDF with error handling
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError as e:
    print(f"Warning: PyMuPDF not available: {e}")
    PYMUPDF_AVAILABLE = False

# Import python-docx with error handling
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError as e:
    print(f"Warning: python-docx not available: {e}")
    DOCX_AVAILABLE = False

def extract_text_from_pdf(file_path: str) -> str:
    if not PYMUPDF_AVAILABLE:
        raise Exception("PyMuPDF not available for PDF processing")
    
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
    if not DOCX_AVAILABLE:
        raise Exception("python-docx not available for DOCX processing")
    
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def parse_files(file_paths: list[str]) -> list[dict]:
    extracted_texts = []
    for file_path in file_paths:
        try:
            if file_path.endswith('.pdf'):
                if PYMUPDF_AVAILABLE:
                    text = extract_text_from_pdf(file_path)
                else:
                    text = f"PDF processing not available for {file_path}"
            elif file_path.endswith('.docx'):
                if DOCX_AVAILABLE:
                    text = extract_text_from_docx(file_path)
                else:
                    text = f"DOCX processing not available for {file_path}"
            else:
                continue
            extracted_texts.append({"file_path": file_path, "text": text})
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            extracted_texts.append({"file_path": file_path, "text": f"Error: {str(e)}"})
    return extracted_texts