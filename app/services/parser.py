import pdfplumber
import tempfile

async def extract_text(upload_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await upload_file.read()
        tmp.write(content)
        tmp_path = tmp.name

    text = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text.strip()