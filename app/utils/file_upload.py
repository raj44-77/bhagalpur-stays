"""File upload validation"""
import os
import magic
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif", "pdf", "avif"}
ALLOWED_MIME_TYPES = {
    "image/jpeg", "image/png", "image/webp", 
    "image/gif", "image/avif", "application/pdf"
}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_file(file: UploadFile) -> str:
    """Validate uploaded file and return safe filename"""
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check extension
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type .{ext} not allowed")
    
    # Check size
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")
    
    # Check MIME type
    content = file.file.read(2048)
    file.file.seek(0)
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"MIME type {mime} not allowed")
    
    # Generate safe filename
    import uuid
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    return safe_name