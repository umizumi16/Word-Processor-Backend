from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from models import FormatRequest

router = APIRouter()

@router.post("/apply")
async def apply_formatting(request: FormatRequest):
    """Apply text formatting (FR-2)"""
    text = request.text
    format_type = request.format_type
    value = request.value
    
    # Return formatted text with HTML tags
    formatting_map = {
        "bold": f"<strong>{text}</strong>",
        "italic": f"<em>{text}</em>",
        "underline": f"<u>{text}</u>",
        "strikethrough": f"<s>{text}</s>",
        "superscript": f"<sup>{text}</sup>",
        "subscript": f"<sub>{text}</sub>",
    }
    
    if format_type in formatting_map:
        formatted_text = formatting_map[format_type]
    elif format_type == "font-family":
        formatted_text = f'<span style="font-family: {value}">{text}</span>'
    elif format_type == "font-size":
        formatted_text = f'<span style="font-size: {value}">{text}</span>'
    elif format_type == "color":
        formatted_text = f'<span style="color: {value}">{text}</span>'
    elif format_type == "background-color":
        formatted_text = f'<span style="background-color: {value}">{text}</span>'
    elif format_type == "align":
        formatted_text = f'<div style="text-align: {value}">{text}</div>'
    else:
        raise HTTPException(status_code=400, detail="Invalid format type")
    
    return {"formatted_text": formatted_text}

@router.post("/heading")
async def apply_heading(text: str, level: int):
    """Apply heading format (FR-2)"""
    if level < 1 or level > 6:
        raise HTTPException(status_code=400, detail="Heading level must be 1-6")
    
    return {"formatted_text": f"<h{level}>{text}</h{level}>"}

@router.post("/list")
async def create_list(items: list, ordered: bool = False):
    """Create bulleted or numbered list (FR-2)"""
    list_tag = "ol" if ordered else "ul"
    list_items = "".join([f"<li>{item}</li>" for item in items])
    
    return {"formatted_text": f"<{list_tag}>{list_items}</{list_tag}>"}

@router.post("/indent")
async def apply_indent(text: str, direction: str):
    """Apply indentation (FR-2)"""
    if direction == "increase":
        return {"formatted_text": f'<div style="margin-left: 40px">{text}</div>'}
    elif direction == "decrease":
        return {"formatted_text": f'<div style="margin-left: 0px">{text}</div>'}
    else:
        raise HTTPException(status_code=400, detail="Invalid direction")

@router.post("/line-spacing")
async def apply_line_spacing(text: str, spacing: float):
    """Apply line spacing (FR-2)"""
    return {"formatted_text": f'<div style="line-height: {spacing}">{text}</div>'}
