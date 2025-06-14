import PyPDF2

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

