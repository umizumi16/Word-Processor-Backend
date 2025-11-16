from fastapi import APIRouter, HTTPException
from typing import List, Dict
import json
import os
from datetime import datetime
import uuid
from difflib import SequenceMatcher

from models import TrackChange

router = APIRouter()

CHANGES_DIR = "data/track_changes"
os.makedirs(CHANGES_DIR, exist_ok=True)

@router.post("/enable")
async def enable_tracking(document_id: str):
    """Enable track changes for document (FR-11)"""
    tracking_file = os.path.join(CHANGES_DIR, f"{document_id}_tracking.json")
    
    tracking_data = {
        "document_id": document_id,
        "enabled": True,
        "enabled_at": datetime.now().isoformat(),
        "changes": []
    }
    
    with open(tracking_file, 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    return {"message": "Track changes enabled", "document_id": document_id}

@router.post("/disable")
async def disable_tracking(document_id: str):
    """Disable track changes for document"""
    tracking_file = os.path.join(CHANGES_DIR, f"{document_id}_tracking.json")
    
    if not os.path.exists(tracking_file):
        raise HTTPException(status_code=404, detail="Tracking not found")
    
    with open(tracking_file, 'r') as f:
        tracking_data = json.load(f)
    
    tracking_data["enabled"] = False
    tracking_data["disabled_at"] = datetime.now().isoformat()
    
    with open(tracking_file, 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    return {"message": "Track changes disabled"}

@router.post("/record")
async def record_change(
    document_id: str,
    change_type: str,
    content: str,
    user: str,
    position: int
):
    """Record a change (FR-11)"""
    tracking_file = os.path.join(CHANGES_DIR, f"{document_id}_tracking.json")
    
    if not os.path.exists(tracking_file):
        raise HTTPException(status_code=404, detail="Tracking not enabled")
    
    with open(tracking_file, 'r') as f:
        tracking_data = json.load(f)
    
    if not tracking_data.get("enabled", False):
        raise HTTPException(status_code=400, detail="Tracking is disabled")
    
    change = {
        "id": str(uuid.uuid4()),
        "type": change_type,
        "content": content,
        "user": user,
        "timestamp": datetime.now().isoformat(),
        "position": position,
        "status": "pending"
    }
    
    tracking_data["changes"].append(change)
    
    with open(tracking_file, 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    return change

@router.get("/{document_id}")
async def get_changes(document_id: str):
    """Get all tracked changes (FR-11)"""
    tracking_file = os.path.join(CHANGES_DIR, f"{document_id}_tracking.json")
    
    if not os.path.exists(tracking_file):
        return {"enabled": False, "changes": []}
    
    with open(tracking_file, 'r') as f:
        tracking_data = json.load(f)
    
    return tracking_data

@router.post("/{change_id}/accept")
async def accept_change(document_id: str, change_id: str):
    """Accept a tracked change (FR-11)"""
    tracking_file = os.path.join(CHANGES_DIR, f"{document_id}_tracking.json")
    
    if not os.path.exists(tracking_file):
        raise HTTPException(status_code=404, detail="Tracking not found")
    
    with open(tracking_file, 'r') as f:
        tracking_data = json.load(f)
    
    for change in tracking_data["changes"]:
        if change["id"] == change_id:
            change["status"] = "accepted"
            change["resolved_at"] = datetime.now().isoformat()
            break
    
    with open(tracking_file, 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    return {"message": "Change accepted"}

@router.post("/{change_id}/reject")
async def reject_change(document_id: str, change_id: str):
    """Reject a tracked change (FR-11)"""
    tracking_file = os.path.join(CHANGES_DIR, f"{document_id}_tracking.json")
    
    if not os.path.exists(tracking_file):
        raise HTTPException(status_code=404, detail="Tracking not found")
    
    with open(tracking_file, 'r') as f:
        tracking_data = json.load(f)
    
    for change in tracking_data["changes"]:
        if change["id"] == change_id:
            change["status"] = "rejected"
            change["resolved_at"] = datetime.now().isoformat()
            break
    
    with open(tracking_file, 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    return {"message": "Change rejected"}

@router.post("/compare")
async def compare_versions(original: str, modified: str):
    """Compare two versions of content"""
    matcher = SequenceMatcher(None, original, modified)
    differences = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            differences.append({
                "type": "replace",
                "original": original[i1:i2],
                "modified": modified[j1:j2],
                "position": i1
            })
        elif tag == 'delete':
            differences.append({
                "type": "delete",
                "content": original[i1:i2],
                "position": i1
            })
        elif tag == 'insert':
            differences.append({
                "type": "insert",
                "content": modified[j1:j2],
                "position": i1
            })
    
    return {"differences": differences}

@router.post("/accept-all")
async def accept_all_changes(document_id: str):
    """Accept all tracked changes (FR-11)"""
    tracking_file = os.path.join(CHANGES_DIR, f"{document_id}_tracking.json")
    
    if not os.path.exists(tracking_file):
        raise HTTPException(status_code=404, detail="Tracking not found")
    
    with open(tracking_file, 'r') as f:
        tracking_data = json.load(f)
    
    for change in tracking_data["changes"]:
        if change["status"] == "pending":
            change["status"] = "accepted"
            change["resolved_at"] = datetime.now().isoformat()
    
    with open(tracking_file, 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    return {"message": "All changes accepted"}

@router.post("/reject-all")
async def reject_all_changes(document_id: str):
    """Reject all tracked changes (FR-11)"""
    tracking_file = os.path.join(CHANGES_DIR, f"{document_id}_tracking.json")
    
    if not os.path.exists(tracking_file):
        raise HTTPException(status_code=404, detail="Tracking not found")
    
    with open(tracking_file, 'r') as f:
        tracking_data = json.load(f)
    
    for change in tracking_data["changes"]:
        if change["status"] == "pending":
            change["status"] = "rejected"
            change["resolved_at"] = datetime.now().isoformat()
    
    with open(tracking_file, 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    return {"message": "All changes rejected"}
