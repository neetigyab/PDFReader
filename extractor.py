import pdfplumber

def extract_pdf_text(pdf_path):
    """Extract all text lines from a PDF."""
    try:
        lines = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                page_lines = text.splitlines()
                lines.extend(page_lines)
        return lines
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []
