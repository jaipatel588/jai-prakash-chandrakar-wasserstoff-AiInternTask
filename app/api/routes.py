from fastapi import APIRouter, File, UploadFile, Form
from app.services.vector_service import process_and_store_document
from app.services.query_service import query_documents

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename
    result = process_and_store_document(content, filename)
    return {"message": "Document processed and stored.", "result": result}

@router.get("/query/")
async def query(q: str):
    result = query_documents(q)
    return {"response": result}