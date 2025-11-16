from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
from PIL import Image
import uuid

from utils.file_handler import FileHandler

router = APIRouter()

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload image to document (FR-6)"""
    # Check file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Save file
    try:
        file_info = await FileHandler.save_upload_file(file, subfolder="images")
        
        # Get image dimensions
        img = Image.open(file_info["path"])
        width, height = img.size
        
        file_info["width"] = width
        file_info["height"] = height
        file_info["format"] = img.format
        
        return file_info
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@router.post("/upload-multiple")
async def upload_multiple_images(files: List[UploadFile] = File(...)):
    """Upload multiple images (FR-6)"""
    uploaded_files = []
    errors = []
    
    for file in files:
        try:
            file_info = await upload_image(file)
            uploaded_files.append(file_info)
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "uploaded": uploaded_files,
        "errors": errors,
        "total": len(files),
        "success": len(uploaded_files),
        "failed": len(errors)
    }

@router.post("/resize")
async def resize_image(
    filename: str,
    width: int = None,
    height: int = None
):
    """Resize an uploaded image"""
    file_path = os.path.join("static/uploads/images", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        img = Image.open(file_path)
        
        # Calculate new dimensions maintaining aspect ratio
        if width and not height:
            ratio = width / img.width
            height = int(img.height * ratio)
        elif height and not width:
            ratio = height / img.height
            width = int(img.width * ratio)
        elif not width and not height:
            raise HTTPException(status_code=400, detail="Provide width or height")
        
        # Resize
        resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # Save with new name
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_resized_{width}x{height}{ext}"
        new_path = os.path.join("static/uploads/images", new_filename)
        
        resized_img.save(new_path)
        
        return {
            "filename": new_filename,
            "url": f"/static/uploads/images/{new_filename}",
            "width": width,
            "height": height
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resize image: {str(e)}")

@router.delete("/{filename}")
async def delete_image(filename: str):
    """Delete an uploaded image"""
    file_path = os.path.join("static/uploads/images", filename)
    
    if FileHandler.delete_file(file_path):
        return {"message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")

@router.get("/list")
async def list_images():
    """List all uploaded images"""
    images_dir = "static/uploads/images"
    
    if not os.path.exists(images_dir):
        return []
    
    images = FileHandler.list_files(images_dir)
    
    # Add image-specific info
    for img in images:
        try:
            image = Image.open(img["path"])
            img["width"], img["height"] = image.size
            img["format"] = image.format
            img["url"] = f"/static/uploads/images/{img['filename']}"
        except:
            pass
    
    return images
