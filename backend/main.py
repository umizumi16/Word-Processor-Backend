# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.staticfiles import StaticFiles
# # import uvicorn
# # import os

# # from routes import document, formatting, spellcheck, export

# # # Create necessary directories
# # os.makedirs("static/uploads", exist_ok=True)
# # os.makedirs("data/documents", exist_ok=True)
# # os.makedirs("data/autosave", exist_ok=True)
# # os.makedirs("data/templates", exist_ok=True)

# # app = FastAPI(
# #     title="Word Processor API",
# #     description="Backend API for Word Processor Web Application",
# #     version="1.0.0"
# # )

# # # CORS middleware configuration
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:3000"],  # React dev server
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Mount static files
# # app.mount("/static", StaticFiles(directory="static"), name="static")

# # # Include routers
# # app.include_router(document.router, prefix="/api/document", tags=["document"])
# # app.include_router(formatting.router, prefix="/api/format", tags=["formatting"])
# # app.include_router(spellcheck.router, prefix="/api/spellcheck", tags=["spellcheck"])
# # app.include_router(export.router, prefix="/api/export", tags=["export"])

# # @app.get("/api/health")
# # def health_check():
# #     """Health check endpoint to verify API is running"""
# #     return {
# #         "status": "ok",
# #         "message": "Word Processor API is running",
# #         "version": "1.0.0"
# #     }

# # @app.get("/")
# # def root():
# #     return {
# #         "message": "Word Processor API",
# #         "docs": "/docs",
# #         "health": "/api/health"
# #     }

# # if __name__ == "__main__":
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# import uvicorn
# import os

# from routes import document, formatting, spellcheck, export, templates, comments

# # Create necessary directories
# os.makedirs("static/uploads", exist_ok=True)
# os.makedirs("static/exports", exist_ok=True)
# os.makedirs("data/documents", exist_ok=True)
# os.makedirs("data/autosave", exist_ok=True)
# os.makedirs("data/templates", exist_ok=True)
# os.makedirs("data/comments", exist_ok=True)

# app = FastAPI(
#     title="Word Processor API",
#     description="Backend API for Word Processor Web Application",
#     version="1.0.0"
# )

# # CORS middleware configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Include routers
# app.include_router(document.router, prefix="/api/document", tags=["document"])
# app.include_router(formatting.router, prefix="/api/format", tags=["formatting"])
# app.include_router(spellcheck.router, prefix="/api/spellcheck", tags=["spellcheck"])
# app.include_router(export.router, prefix="/api/export", tags=["export"])
# app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
# app.include_router(comments.router, prefix="/api/comments", tags=["comments"])

# @app.get("/api/health")
# def health_check():
#     """Health check endpoint to verify API is running"""
#     return {
#         "status": "ok",
#         "message": "Word Processor API is running",
#         "version": "1.0.0"
#     }

# @app.get("/")
# def root():
#     return {
#         "message": "Word Processor API",
#         "docs": "/docs",
#         "health": "/api/health"
#     }

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from routes import (
    document, 
    formatting, 
    spellcheck, 
    export, 
    templates, 
    comments,
    track_changes,
    images
)

# Create necessary directories
directories = [
    "static/uploads",
    "static/uploads/images",
    "static/exports",
    "data/documents",
    "data/autosave",
    "data/templates",
    "data/comments",
    "data/track_changes"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

app = FastAPI(
    title="Word Processor API",
    description="Backend API for Word Processor Web Application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(document.router, prefix="/api/document", tags=["document"])
app.include_router(formatting.router, prefix="/api/format", tags=["formatting"])
app.include_router(spellcheck.router, prefix="/api/spellcheck", tags=["spellcheck"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
app.include_router(track_changes.router, prefix="/api/track-changes", tags=["track-changes"])
app.include_router(images.router, prefix="/api/images", tags=["images"])

@app.get("/api/health")
def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "ok",
        "message": "Word Processor API is running",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    return {
        "message": "Word Processor API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
