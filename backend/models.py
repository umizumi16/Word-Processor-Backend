from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class FormatStyle(str, Enum):
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"

class AlignmentType(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"

class Document(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    word_count: Optional[int] = 0
    char_count: Optional[int] = 0

class DocumentCreate(BaseModel):
    title: str = "Untitled Document"
    content: str = ""
    template_id: Optional[str] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class SpellCheckRequest(BaseModel):
    text: str

class SpellCheckResponse(BaseModel):
    errors: List[Dict[str, Any]]
    suggestions: Dict[str, List[str]]

class GrammarCheckRequest(BaseModel):
    text: str

class GrammarCheckResponse(BaseModel):
    errors: List[Dict[str, Any]]

class FormatRequest(BaseModel):
    text: str
    format_type: str
    value: str

class FindReplaceRequest(BaseModel):
    content: str
    find: str
    replace: str
    replace_all: bool = False

class ExportRequest(BaseModel):
    document_id: str
    format: str  # html, pdf, docx

class AutoSaveRequest(BaseModel):
    document_id: str
    content: str

class TableInsert(BaseModel):
    rows: int = Field(ge=1, le=50)
    columns: int = Field(ge=1, le=20)

class ImageInsert(BaseModel):
    file_path: str
    alt_text: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

class TrackChange(BaseModel):
    type: str  # insert, delete, format
    content: str
    user: str
    timestamp: datetime
    position: int

class Comment(BaseModel):
    id: Optional[str] = None
    content: str
    user: str
    timestamp: datetime
    position: int
    resolved: bool = False
