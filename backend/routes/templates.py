from fastapi import APIRouter, HTTPException
from typing import List
import json
import os
from datetime import datetime
import uuid

from models import Document

router = APIRouter()

TEMPLATES_DIR = "data/templates"

# Predefined templates
DEFAULT_TEMPLATES = {
    "blank": {
        "name": "Blank Document",
        "content": ""
    },
    "business_letter": {
        "name": "Business Letter",
        "content": """
<div style="margin-bottom: 20px;">[Your Name]</div>
<div style="margin-bottom: 20px;">[Your Address]</div>
<div style="margin-bottom: 20px;">[Date]</div>

<div style="margin-bottom: 20px;">
[Recipient Name]<br/>
[Recipient Title]<br/>
[Company Name]<br/>
[Address]
</div>

<div style="margin-bottom: 20px;">Dear [Recipient Name],</div>

<p>[Body of letter]</p>

<div style="margin-top: 20px;">
Sincerely,<br/><br/>
[Your Name]
</div>
        """
    },
    "resume": {
        "name": "Resume",
        "content": """
<h1 style="text-align: center;">[Your Name]</h1>
<p style="text-align: center;">[Email] | [Phone] | [LinkedIn]</p>

<h2>Professional Summary</h2>
<p>[Brief professional summary]</p>

<h2>Experience</h2>
<h3>[Job Title] - [Company]</h3>
<p><em>[Start Date] - [End Date]</em></p>
<ul>
<li>[Achievement/Responsibility]</li>
<li>[Achievement/Responsibility]</li>
</ul>

<h2>Education</h2>
<h3>[Degree] - [University]</h3>
<p><em>[Graduation Year]</em></p>

<h2>Skills</h2>
<ul>
<li>[Skill]</li>
<li>[Skill]</li>
</ul>
        """
    },
    "report": {
        "name": "Report",
        "content": """
<h1 style="text-align: center;">[Report Title]</h1>
<p style="text-align: center;"><em>[Date]</em></p>

<h2>Executive Summary</h2>
<p>[Brief overview of the report]</p>

<h2>Introduction</h2>
<p>[Introduction content]</p>

<h2>Methodology</h2>
<p>[Methodology content]</p>

<h2>Results</h2>
<p>[Results content]</p>

<h2>Conclusion</h2>
<p>[Conclusion content]</p>

<h2>References</h2>
<p>[References]</p>
        """
    }
}

@router.get("/list")
async def list_templates():
    """List all available templates (FR-12)"""
    templates = []
    
    # Add default templates
    for template_id, template in DEFAULT_TEMPLATES.items():
        templates.append({
            "id": template_id,
            "name": template["name"],
            "type": "default"
        })
    
    # Add custom templates from file system
    if os.path.exists(TEMPLATES_DIR):
        for filename in os.listdir(TEMPLATES_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(TEMPLATES_DIR, filename), 'r') as f:
                    template_data = json.load(f)
                    templates.append({
                        "id": filename.replace('.json', ''),
                        "name": template_data.get("name", "Custom Template"),
                        "type": "custom"
                    })
    
    return templates

@router.get("/{template_id}")
async def get_template(template_id: str):
    """Get template content (FR-12)"""
    # Check default templates
    if template_id in DEFAULT_TEMPLATES:
        return DEFAULT_TEMPLATES[template_id]
    
    # Check custom templates
    filepath = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
    raise HTTPException(status_code=404, detail="Template not found")

@router.post("/create")
async def create_template(name: str, content: str):
    """Create custom template (FR-12)"""
    template_id = str(uuid.uuid4())
    template_data = {
        "id": template_id,
        "name": name,
        "content": content,
        "created_at": datetime.now().isoformat()
    }
    
    filepath = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
    with open(filepath, 'w') as f:
        json.dump(template_data, f, indent=2)
    
    return template_data

@router.delete("/{template_id}")
async def delete_template(template_id: str):
    """Delete custom template"""
    if template_id in DEFAULT_TEMPLATES:
        raise HTTPException(status_code=400, detail="Cannot delete default templates")
    
    filepath = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Template not found")
    
    os.remove(filepath)
    return {"message": "Template deleted successfully"}
