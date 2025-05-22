import os
import tempfile
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

vectorstore_path = "data/faiss_index"

def extract_text(content: bytes, filename: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_path = tmp_file.name

    if filename.endswith(".pdf"):
        reader = PdfReader(tmp_path)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    else:
        image = Image.open(tmp_path)
        return pytesseract.image_to_string(image)

def process_and_store_document(content: bytes, filename: str):
    text = extract_text(content, filename)

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.create_documents([text])
    
    embedding = OpenAIEmbeddings()
    
    if os.path.exists(vectorstore_path):
        db = FAISS.load_local(vectorstore_path, embeddings=embedding)
        db.add_documents(docs)
    else:
        db = FAISS.from_documents(docs, embedding)
        db.save_local(vectorstore_path)

    return {"chunks": len(docs)}