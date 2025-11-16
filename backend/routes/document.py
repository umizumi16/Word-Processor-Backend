from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import json
import os
from datetime import datetime
import uuid

from models import (
    Document, DocumentCreate, DocumentUpdate, 
    AutoSaveRequest, FindReplaceRequest
)

router = APIRouter()

DOCUMENTS_DIR = "data/documents"
AUTOSAVE_DIR = "data/autosave"

@router.post("/create", response_model=Document)
async def create_document(doc: DocumentCreate):
    """Create a new document (FR-1)"""
    doc_id = str(uuid.uuid4())
    document = Document(
        id=doc_id,
        title=doc.title,
        content=doc.content,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        word_count=len(doc.content.split()),
        char_count=len(doc.content)
    )
    
    # Save to file
    file_path = os.path.join(DOCUMENTS_DIR, f"{doc_id}.json")
    with open(file_path, 'w') as f:
        json.dump(document.dict(), f, default=str)
    
    return document

@router.get("/{document_id}", response_model=Document)
async def get_document(document_id: str):
    """Retrieve a document by ID (FR-1)"""
    file_path = os.path.join(DOCUMENTS_DIR, f"{document_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    with open(file_path, 'r') as f:
        doc_data = json.load(f)
    
    return Document(**doc_data)

@router.put("/{document_id}", response_model=Document)
async def update_document(document_id: str, doc_update: DocumentUpdate):
    """Update an existing document (FR-1)"""
    file_path = os.path.join(DOCUMENTS_DIR, f"{document_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    with open(file_path, 'r') as f:
        doc_data = json.load(f)
    
    document = Document(**doc_data)
    
    if doc_update.title:
        document.title = doc_update.title
    if doc_update.content:
        document.content = doc_update.content
        document.word_count = len(doc_update.content.split())
        document.char_count = len(doc_update.content)
    
    document.updated_at = datetime.now()
    
    # Save updated document
    with open(file_path, 'w') as f:
        json.dump(document.dict(), f, default=str)
    
    return document

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document (FR-1)"""
    file_path = os.path.join(DOCUMENTS_DIR, f"{document_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    os.remove(file_path)
    return {"message": "Document deleted successfully"}

@router.get("/list/all")
async def list_documents():
    """List all documents"""
    documents = []
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(DOCUMENTS_DIR, filename), 'r') as f:
                doc_data = json.load(f)
                documents.append(Document(**doc_data))
    
    return documents

@router.post("/autosave")
async def autosave_document(request: AutoSaveRequest):
    """Auto-save document (FR-9)"""
    file_path = os.path.join(AUTOSAVE_DIR, f"{request.document_id}_autosave.json")
    
    autosave_data = {
        "document_id": request.document_id,
        "content": request.content,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(file_path, 'w') as f:
        json.dump(autosave_data, f)
    
    return {"message": "Document auto-saved", "timestamp": autosave_data["timestamp"]}

@router.post("/find-replace")
async def find_replace(request: FindReplaceRequest):
    """Find and replace text in document (FR-8)"""
    content = request.content
    
    if request.replace_all:
        updated_content = content.replace(request.find, request.replace)
        count = content.count(request.find)
    else:
        updated_content = content.replace(request.find, request.replace, 1)
        count = 1 if request.find in content else 0
    
    return {
        "updated_content": updated_content,
        "replacements_made": count
    }

@router.get("/stats/{document_id}")
async def get_document_stats(document_id: str):
    """Get document statistics (FR-10)"""
    file_path = os.path.join(DOCUMENTS_DIR, f"{document_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    with open(file_path, 'r') as f:
        doc_data = json.load(f)
    
    document = Document(**doc_data)
    content = document.content
    
    words = content.split()
    paragraphs = content.split('\n\n')
    
    return {
        "word_count": len(words),
        "character_count": len(content),
        "character_count_no_spaces": len(content.replace(" ", "")),
        "paragraph_count": len([p for p in paragraphs if p.strip()]),
        "line_count": len(content.split('\n'))
    }
