import os
import uuid
import shutil
from typing import Optional
from fastapi import UploadFile
from datetime import datetime
import json

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileHandler:
    @staticmethod
    async def save_upload_file(file: UploadFile, subfolder: str = "") -> dict:
        """
        Save uploaded file to server
        Returns file information including path and URL
        """
        # Create subfolder if specified
        target_dir = os.path.join(UPLOAD_DIR, subfolder) if subfolder else UPLOAD_DIR
        os.makedirs(target_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(target_dir, unique_filename)
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        finally:
            file.file.close()
        
        # Return file info
        relative_path = os.path.join(subfolder, unique_filename) if subfolder else unique_filename
        
        return {
            "filename": unique_filename,
            "original_filename": file.filename,
            "path": file_path,
            "url": f"/static/uploads/{relative_path}",
            "size": os.path.getsize(file_path),
            "uploaded_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete a file from server"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    @staticmethod
    def get_file_info(file_path: str) -> Optional[dict]:
        """Get information about a file"""
        if not os.path.exists(file_path):
            return None
        
        return {
            "path": file_path,
            "size": os.path.getsize(file_path),
            "created": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
            "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
        }
    
    @staticmethod
    def list_files(directory: str = UPLOAD_DIR) -> list:
        """List all files in a directory"""
        files = []
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                files.append({
                    "filename": filename,
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                })
        return files
