import fitz

pdf_memory = ""

def extract_text_from_pdf(pdf_bytes):
    global pdf_memory
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pdf_memory = "\n".join(page.get_text("text") for page in doc)
        return pdf_memory[:500]
    except Exception as e:
        pdf_memory = ""
        return f"⚠️ Error extracting text: {str(e)}"
