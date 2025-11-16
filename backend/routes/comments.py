from fastapi import APIRouter, HTTPException
from typing import List
import json
import os
from datetime import datetime
import uuid

from models import Comment

router = APIRouter()

COMMENTS_DIR = "data/comments"
os.makedirs(COMMENTS_DIR, exist_ok=True)

@router.post("/add")
async def add_comment(document_id: str, comment: Comment):
    """Add comment to document (FR-11)"""
    comment.id = str(uuid.uuid4())
    comment.timestamp = datetime.now()
    
    comments_file = os.path.join(COMMENTS_DIR, f"{document_id}_comments.json")
    
    # Load existing comments
    comments = []
    if os.path.exists(comments_file):
        with open(comments_file, 'r') as f:
            comments = json.load(f)
    
    # Add new comment
    comments.append(comment.dict())
    
    # Save comments
    with open(comments_file, 'w') as f:
        json.dump(comments, f, indent=2, default=str)
    
    return comment

@router.get("/{document_id}")
async def get_comments(document_id: str):
    """Get all comments for document (FR-11)"""
    comments_file = os.path.join(COMMENTS_DIR, f"{document_id}_comments.json")
    
    if not os.path.exists(comments_file):
        return []
    
    with open(comments_file, 'r') as f:
        comments = json.load(f)
    
    return comments

@router.put("/{comment_id}/resolve")
async def resolve_comment(document_id: str, comment_id: str):
    """Mark comment as resolved (FR-11)"""
    comments_file = os.path.join(COMMENTS_DIR, f"{document_id}_comments.json")
    
    if not os.path.exists(comments_file):
        raise HTTPException(status_code=404, detail="Comments not found")
    
    with open(comments_file, 'r') as f:
        comments = json.load(f)
    
    # Find and resolve comment
    for comment in comments:
        if comment['id'] == comment_id:
            comment['resolved'] = True
            break
    
    # Save updated comments
    with open(comments_file, 'w') as f:
        json.dump(comments, f, indent=2)
    
    return {"message": "Comment resolved"}

@router.delete("/{comment_id}")
async def delete_comment(document_id: str, comment_id: str):
    """Delete comment (FR-11)"""
    comments_file = os.path.join(COMMENTS_DIR, f"{document_id}_comments.json")
    
    if not os.path.exists(comments_file):
        raise HTTPException(status_code=404, detail="Comments not found")
    
    with open(comments_file, 'r') as f:
        comments = json.load(f)
    
    # Remove comment
    comments = [c for c in comments if c['id'] != comment_id]
    
    # Save updated comments
    with open(comments_file, 'w') as f:
        json.dump(comments, f, indent=2)
    
    return {"message": "Comment deleted"}
