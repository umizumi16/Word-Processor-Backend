import React, { useState } from 'react';
import './MenuBar.css';

function MenuBar({ 
  onNew, 
  onOpen, 
  onSave, 
  onExport, 
  onPrint,
  onUndo,
  onRedo,
  onInsertTable,
  onInsertImage,
  onInsertPageBreak
}) {
  const [activeMenu, setActiveMenu] = useState(null);

  const toggleMenu = (menu) => {
    setActiveMenu(activeMenu === menu ? null : menu);
  };

  const closeMenu = () => {
    setActiveMenu(null);
  };

  return (
    <div className="menu-bar">
      <div className="menu-item">
        <button 
          className="menu-button" 
          onClick={() => toggleMenu('file')}
        >
          File
        </button>
        {activeMenu === 'file' && (
          <div className="dropdown-menu">
            <button onClick={() => { onNew(); closeMenu(); }}>
              New <span className="shortcut">Ctrl+N</span>
            </button>
            <button onClick={() => { onOpen(); closeMenu(); }}>
              Open <span className="shortcut">Ctrl+O</span>
            </button>
            <button onClick={() => { onSave(); closeMenu(); }}>
              Save <span className="shortcut">Ctrl+S</span>
            </button>
            <button onClick={() => { onSave(); closeMenu(); }}>
              Save As...
            </button>
            <div className="menu-divider"></div>
            <button onClick={() => { onPrint(); closeMenu(); }}>
              Print <span className="shortcut">Ctrl+P</span>
            </button>
            <button onClick={() => { onExport('pdf'); closeMenu(); }}>
              Export as PDF
            </button>
            <button onClick={() => { onExport('docx'); closeMenu(); }}>
              Export as DOCX
            </button>
            <button onClick={() => { onExport('html'); closeMenu(); }}>
              Export as HTML
            </button>
          </div>
        )}
      </div>

      <div className="menu-item">
        <button 
          className="menu-button" 
          onClick={() => toggleMenu('edit')}
        >
          Edit
        </button>
        {activeMenu === 'edit' && (
          <div className="dropdown-menu">
            <button onClick={() => { onUndo(); closeMenu(); }}>
              Undo <span className="shortcut">Ctrl+Z</span>
            </button>
            <button onClick={() => { onRedo(); closeMenu(); }}>
              Redo <span className="shortcut">Ctrl+Y</span>
            </button>
            <div className="menu-divider"></div>
            <button onClick={() => { document.execCommand('cut'); closeMenu(); }}>
              Cut <span className="shortcut">Ctrl+X</span>
            </button>
            <button onClick={() => { document.execCommand('copy'); closeMenu(); }}>
              Copy <span className="shortcut">Ctrl+C</span>
            </button>
            <button onClick={() => { document.execCommand('paste'); closeMenu(); }}>
              Paste <span className="shortcut">Ctrl+V</span>
            </button>
            <div className="menu-divider"></div>
            <button onClick={() => { document.execCommand('selectAll'); closeMenu(); }}>
              Select All <span className="shortcut">Ctrl+A</span>
            </button>
            <button onClick={closeMenu}>
              Find & Replace <span className="shortcut">Ctrl+F</span>
            </button>
          </div>
        )}
      </div>

      <div className="menu-item">
        <button 
          className="menu-button" 
          onClick={() => toggleMenu('insert')}
        >
          Insert
        </button>
        {activeMenu === 'insert' && (
          <div className="dropdown-menu">
            <button onClick={() => { onInsertTable(); closeMenu(); }}>
              Table
            </button>
            <button onClick={() => { onInsertImage(); closeMenu(); }}>
              Image
            </button>
            <button onClick={() => { onInsertPageBreak(); closeMenu(); }}>
              Page Break
            </button>
            <div className="menu-divider"></div>
            <button onClick={() => { document.execCommand('createLink'); closeMenu(); }}>
              Hyperlink
            </button>
          </div>
        )}
      </div>

      <div className="menu-item">
        <button 
          className="menu-button" 
          onClick={() => toggleMenu('format')}
        >
          Format
        </button>
        {activeMenu === 'format' && (
          <div className="dropdown-menu">
            <button onClick={() => { document.execCommand('bold'); closeMenu(); }}>
              Bold <span className="shortcut">Ctrl+B</span>
            </button>
            <button onClick={() => { document.execCommand('italic'); closeMenu(); }}>
              Italic <span className="shortcut">Ctrl+I</span>
            </button>
            <button onClick={() => { document.execCommand('underline'); closeMenu(); }}>
              Underline <span className="shortcut">Ctrl+U</span>
            </button>
            <div className="menu-divider"></div>
            <button onClick={() => { document.execCommand('insertUnorderedList'); closeMenu(); }}>
              Bullet List
            </button>
            <button onClick={() => { document.execCommand('insertOrderedList'); closeMenu(); }}>
              Numbered List
            </button>
            <div className="menu-divider"></div>
            <button onClick={() => { document.execCommand('justifyLeft'); closeMenu(); }}>
              Align Left
            </button>
            <button onClick={() => { document.execCommand('justifyCenter'); closeMenu(); }}>
              Align Center
            </button>
            <button onClick={() => { document.execCommand('justifyRight'); closeMenu(); }}>
              Align Right
            </button>
            <button onClick={() => { document.execCommand('justifyFull'); closeMenu(); }}>
              Justify
            </button>
          </div>
        )}
      </div>

      <div className="menu-item">
        <button 
          className="menu-button" 
          onClick={() => toggleMenu('tools')}
        >
          Tools
        </button>
        {activeMenu === 'tools' && (
          <div className="dropdown-menu">
            <button onClick={closeMenu}>
              Spelling & Grammar
            </button>
            <button onClick={closeMenu}>
              Word Count
            </button>
            <div className="menu-divider"></div>
            <button onClick={closeMenu}>
              Track Changes
            </button>
            <button onClick={closeMenu}>
              Comments
            </button>
          </div>
        )}
      </div>

      <div className="menu-item">
        <button 
          className="menu-button" 
          onClick={() => toggleMenu('help')}
        >
          Help
        </button>
        {activeMenu === 'help' && (
          <div className="dropdown-menu">
            <button onClick={closeMenu}>
              Documentation
            </button>
            <button onClick={closeMenu}>
              Keyboard Shortcuts
            </button>
            <div className="menu-divider"></div>
            <button onClick={closeMenu}>
              About
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default MenuBar;
