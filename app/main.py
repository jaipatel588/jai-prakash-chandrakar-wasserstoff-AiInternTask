
from fastapi import FastAPI, UploadFile, File, Body
import pytesseract
from PIL import Image
import fitz
import os

from backend.app.services.vector_store import create_vector_store, save_vector_store, load_vector_store
from backend.app.services.load_docs import load_documents_from_dir

app = FastAPI()

UPLOAD_DIR = "backend/data/"
VECTOR_PATH = "backend/data/vector_store"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = extract_text_from_image(file_path)
    else:
        return {"error": "Unsupported file type"}

    txt_path = os.path.join(UPLOAD_DIR, file.filename + ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    return {"filename": file.filename, "extracted_text_snippet": text[:300]}

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(img_path):
    img = Image.open(img_path)
    return pytesseract.image_to_string(img)

@app.post("/build_index/")
def build_index():
    docs = load_documents_from_dir(UPLOAD_DIR)
    vs = create_vector_store(docs)
    save_vector_store(vs, VECTOR_PATH)
    return {"message": "Vector store created."}

@app.post("/query/")
def query_search(query: str = Body(...)):
    vs = load_vector_store(VECTOR_PATH)
    results = vs.similarity_search(query, k=3)
    return [{
        "source": doc.metadata["source"],
        "answer": doc.page_content[:300]
    } for doc in results]

@app.post("/synthesize/")
def synthesize(query: str = Body(...)):
    vs = load_vector_store(VECTOR_PATH)
    results = vs.similarity_search(query, k=10)
    themes = {}
    for r in results:
        source = r.metadata["source"]
        if source not in themes:
            themes[source] = []
        themes[source].append(r.page_content[:200])
    return themes
