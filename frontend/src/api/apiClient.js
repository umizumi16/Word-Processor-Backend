const API_BASE_URL = 'http://localhost:8000/api';

// Health Check
export const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error('Backend health check failed');
  }
  return response.json();
};

// Document Operations
export const createDocument = async (title, content = '') => {
  const response = await fetch(`${API_BASE_URL}/document/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content })
  });
  return response.json();
};

export const getDocument = async (documentId) => {
  const response = await fetch(`${API_BASE_URL}/document/${documentId}`);
  return response.json();
};

export const updateDocument = async (documentId, updates) => {
  const response = await fetch(`${API_BASE_URL}/document/${documentId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });
  return response.json();
};

export const deleteDocument = async (documentId) => {
  const response = await fetch(`${API_BASE_URL}/document/${documentId}`, {
    method: 'DELETE'
  });
  return response.json();
};

export const listDocuments = async () => {
  const response = await fetch(`${API_BASE_URL}/document/list/all`);
  return response.json();
};

export const autoSave = async (documentId, content) => {
  const response = await fetch(`${API_BASE_URL}/document/autosave`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: documentId, content })
  });
  return response.json();
};

export const getDocumentStats = async (documentId) => {
  const response = await fetch(`${API_BASE_URL}/document/stats/${documentId}`);
  return response.json();
};

export const findReplace = async (content, find, replace, replaceAll = false) => {
  const response = await fetch(`${API_BASE_URL}/document/find-replace`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, find, replace, replace_all: replaceAll })
  });
  return response.json();
};

// Spell Check Operations
export const spellCheck = async (text) => {
  const response = await fetch(`${API_BASE_URL}/spellcheck/check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return response.json();
};

export const grammarCheck = async (text) => {
  const response = await fetch(`${API_BASE_URL}/spellcheck/grammar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return response.json();
};

// Formatting Operations
export const applyFormatting = async (text, formatType, value) => {
  const response = await fetch(`${API_BASE_URL}/format/apply`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, format_type: formatType, value })
  });
  return response.json();
};

// Export Operations
export const exportToHTML = async (documentId) => {
  const response = await fetch(`${API_BASE_URL}/export/html`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: documentId, format: 'html' })
  });
  return response.json();
};

export const exportToPDF = async (documentId) => {
  const response = await fetch(`${API_BASE_URL}/export/pdf`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: documentId, format: 'pdf' })
  });
  return response.json();
};

export const exportToDOCX = async (documentId) => {
  const response = await fetch(`${API_BASE_URL}/export/docx`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: documentId, format: 'docx' })
  });
  return response.json();
};

export const generatePrintPreview = async (documentId) => {
  const response = await fetch(`${API_BASE_URL}/export/print-preview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: documentId })
  });
  return response.json();
};
