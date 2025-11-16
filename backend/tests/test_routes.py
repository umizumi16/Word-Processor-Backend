import pytest
from fastapi.testclient import TestClient
from main import app
import json
import os

client = TestClient(app)

class TestHealthCheck:
    def test_health_endpoint(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

class TestDocumentRoutes:
    def test_create_document(self):
        response = client.post(
            "/api/document/create",
            json={"title": "Test Document", "content": "Test content"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Document"
        assert data["content"] == "Test content"
        assert "id" in data
        
        # Store document ID for cleanup
        self.doc_id = data["id"]
    
    def test_get_document(self):
        # First create a document
        create_response = client.post(
            "/api/document/create",
            json={"title": "Test Get", "content": "Content"}
        )
        doc_id = create_response.json()["id"]
        
        # Now get it
        response = client.get(f"/api/document/{doc_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == doc_id
        assert data["title"] == "Test Get"
    
    def test_update_document(self):
        # Create document
        create_response = client.post(
            "/api/document/create",
            json={"title": "Original", "content": "Original content"}
        )
        doc_id = create_response.json()["id"]
        
        # Update it
        response = client.put(
            f"/api/document/{doc_id}",
            json={"title": "Updated", "content": "Updated content"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["content"] == "Updated content"
    
    def test_delete_document(self):
        # Create document
        create_response = client.post(
            "/api/document/create",
            json={"title": "To Delete", "content": "Delete me"}
        )
        doc_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/api/document/{doc_id}")
        assert response.status_code == 200
        
        # Verify it's deleted
        get_response = client.get(f"/api/document/{doc_id}")
        assert get_response.status_code == 404
    
    def test_list_documents(self):
        response = client.get("/api/document/list/all")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_autosave(self):
        # Create document first
        create_response = client.post(
            "/api/document/create",
            json={"title": "Autosave Test", "content": "Initial"}
        )
        doc_id = create_response.json()["id"]
        
        # Test autosave
        response = client.post(
            "/api/document/autosave",
            json={"document_id": doc_id, "content": "Autosaved content"}
        )
        assert response.status_code == 200
        assert "timestamp" in response.json()
    
    def test_find_replace(self):
        content = "Hello world, hello universe"
        response = client.post(
            "/api/document/find-replace",
            json={
                "content": content,
                "find": "hello",
                "replace": "hi",
                "replace_all": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "hi" in data["updated_content"].lower()
        assert data["replacements_made"] > 0
    
    def test_document_stats(self):
        # Create document
        create_response = client.post(
            "/api/document/create",
            json={"title": "Stats Test", "content": "Word word word.\n\nParagraph two."}
        )
        doc_id = create_response.json()["id"]
        
        # Get stats
        response = client.get(f"/api/document/stats/{doc_id}")
        assert response.status_code == 200
        data = response.json()
        assert "word_count" in data
        assert "character_count" in data
        assert "paragraph_count" in data

class TestSpellCheckRoutes:
    def test_spell_check(self):
        response = client.post(
            "/api/spellcheck/check",
            json={"text": "Thiss is a testt with erors"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data
        assert "suggestions" in data
    
    def test_grammar_check(self):
        response = client.post(
            "/api/spellcheck/grammar",
            json={"text": "this is a sentence without capital. another  with double spaces"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "errors" in data

class TestFormattingRoutes:
    def test_apply_formatting(self):
        response = client.post(
            "/api/format/apply",
            json={"text": "Hello", "format_type": "bold", "value": ""}
        )
        assert response.status_code == 200
        data = response.json()
        assert "<strong>" in data["formatted_text"]
    
    def test_apply_heading(self):
        response = client.post(
            "/api/format/heading",
            params={"text": "Heading", "level": 1}
        )
        assert response.status_code == 200
        data = response.json()
        assert "<h1>" in data["formatted_text"]
    
    def test_create_list(self):
        response = client.post(
            "/api/format/list",
            json=["Item 1", "Item 2", "Item 3"],
            params={"ordered": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert "<ul>" in data["formatted_text"]
        assert "<li>" in data["formatted_text"]

class TestExportRoutes:
    def test_export_to_html(self):
        # Create document first
        create_response = client.post(
            "/api/document/create",
            json={"title": "Export Test", "content": "<p>Test content</p>"}
        )
        doc_id = create_response.json()["id"]
        
        # Export to HTML
        response = client.post(
            "/api/export/html",
            json={"document_id": doc_id, "format": "html"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "filename" in data
        assert "path" in data
    
    def test_print_preview(self):
        # Create document
        create_response = client.post(
            "/api/document/create",
            json={"title": "Print Test", "content": "<p>Print me</p>"}
        )
        doc_id = create_response.json()["id"]
        
        # Generate print preview
        response = client.post(
            "/api/export/print-preview",
            json={"document_id": doc_id}
        )
        assert response.status_code == 200
        data = response.json()
        assert "html" in data

# Run tests with: pytest tests/test_routes.py -v
