import React from 'react';
import './StatusBar.css';

function StatusBar({ wordCount, charCount, pageCount }) {
  return (
    <div className="status-bar">
      <span className="stat">Page {pageCount || 1}</span>
      <span className="stat">Words: {wordCount || 0}</span>
      <span className="stat">Characters: {charCount || 0}</span>
      <span className="stat">Auto-save: Active</span>
    </div>
  );
}
export default StatusBar;
