# This file reads the words out of an uploaded PDF resume.

from pypdf import PdfReader
import io

# Opens the PDF bytes, joins the text from every page, and complains if the file has no readable words.
def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text_parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)
    full_text = "\n".join(text_parts)
    if not full_text.strip():
        raise ValueError("No extractable text found in PDF. It may be a scanned image.")
    return full_text
