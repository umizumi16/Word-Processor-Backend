import React from 'react';
import './Toolbar.css';

function Toolbar({ documentId, content }) {
  const applyFormat = (command, value = null) => {
    document.execCommand(command, false, value);
  };

  return (
    <div className="toolbar">
      <button onClick={() => applyFormat('bold')} title="Bold (Ctrl+B)">
        <strong>B</strong>
      </button>
      <button onClick={() => applyFormat('italic')} title="Italic (Ctrl+I)">
        <em>I</em>
      </button>
      <button onClick={() => applyFormat('underline')} title="Underline (Ctrl+U)">
        <u>U</u>
      </button>
      
      <div className="separator"></div>
      
      <button onClick={() => applyFormat('justifyLeft')} title="Align Left">
        ≡
      </button>
      <button onClick={() => applyFormat('justifyCenter')} title="Align Center">
        ≡
      </button>
      <button onClick={() => applyFormat('justifyRight')} title="Align Right">
        ≡
      </button>
      
      <div className="separator"></div>
      
      <select onChange={(e) => applyFormat('fontSize', e.target.value)} defaultValue="3">
        <option value="1">Small</option>
        <option value="3">Normal</option>
        <option value="5">Large</option>
        <option value="7">Huge</option>
      </select>
      
      <input 
        type="color" 
        onChange={(e) => applyFormat('foreColor', e.target.value)}
        title="Text Color"
      />
    </div>
  );
}

export default Toolbar;
