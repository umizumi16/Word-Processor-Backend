import React, { useRef, useEffect, useState } from 'react';
import { Rnd } from 'react-rnd';
import './Editor.css';

const PAGE_HEIGHT = 1056;

function Editor({ content, onChange, onPageCountChange }) {
  const editorRef = useRef(null);
  const [showTableDialog, setShowTableDialog] = useState(false);
  const [tableRows, setTableRows] = useState(3);
  const [tableCols, setTableCols] = useState(3);
  const [pageCount, setPageCount] = useState(1);
  const [selectedImg, setSelectedImg] = useState(null);

  // Only set content on first mount or external change
  useEffect(() => {
    // Only update if the content prop changed for reasons *other* than typing
    if (editorRef.current && content !== editorRef.current.innerHTML) {
      editorRef.current.innerHTML = content || '';
      enforceImageIds(editorRef.current);
      updatePageCount();
    }
    // eslint-disable-next-line
  }, [content]);

  // Give each image a unique data-imgid, style
  function enforceImageIds(editor) {
    if (!editor) return;
    let idCounter = 1;
    editor.querySelectorAll('img').forEach(img => {
      if (!img.dataset.imgid) {
        img.dataset.imgid = 'img-' + Date.now() + '-' + idCounter++;
      }
      img.classList.add('resizable-img');
      img.style.background = '#fff';
      img.tabIndex = 0;
      img.setAttribute('draggable', false);
    });
  
  }

  // -- Table insertion logic unchanged --
  const insertTable = () => {
    let tableHTML = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; margin: 10px 0;">';
    for (let i = 0; i < tableRows; i++) {
      tableHTML += '<tr>';
      for (let j = 0; j < tableCols; j++) {
        tableHTML += '<td style="border: 1px solid #ccc; padding: 8px; min-width: 50px;">&nbsp;</td>';
      }
      tableHTML += '</tr>';
    }
    tableHTML += '</table>';
    document.execCommand('insertHTML', false, tableHTML);
    setShowTableDialog(false);
    setTimeout(() => enforceImageIds(editorRef.current), 50);
  };

  useEffect(() => {
    const handleInsertTableEvent = () => setShowTableDialog(true);
    window.addEventListener('insertTable', handleInsertTableEvent);
    return () => window.removeEventListener('insertTable', handleInsertTableEvent);
  }, []);

  // -- Image drag/resize logic unchanged --
  useEffect(() => {
    const editor = editorRef.current;
    if (!editor) return;
    function handleClick(e) {
      if (e.target.tagName === 'IMG') {
        const img = e.target;
        const parent = editor;
        const rect = img.getBoundingClientRect();
        const parentRect = parent.getBoundingClientRect();
        setSelectedImg({
          id: img.dataset.imgid,
          src: img.src,
          x: rect.left - parentRect.left + parent.scrollLeft,
          y: rect.top - parentRect.top + parent.scrollTop,
          width: img.width,
          height: img.height
        });
      } else {
        setSelectedImg(null);
      }
    }
    editor.addEventListener('mousedown', handleClick, true);
    const handleDocClick = (e) => { if (!editor.contains(e.target)) setSelectedImg(null); };
    window.addEventListener('mousedown', handleDocClick);
    window.addEventListener('keydown', e => { if (e.key === 'Escape') setSelectedImg(null); });
    return () => {
      editor.removeEventListener('mousedown', handleClick, true);
      window.removeEventListener('mousedown', handleDocClick);
    };
  }, []);

  // Update image after resize/drag
  const handleImageDragResizeStop = (e, d, ref) => {
    if (!selectedImg) return;
    const editor = editorRef.current;
    if (!editor) return;
    const img = editor.querySelector(`img[data-imgid="${selectedImg.id}"]`);
    if (img) {
      img.style.position = "absolute";
      img.style.left = d.x + "px";
      img.style.top = d.y + "px";
      img.style.width = ref.offsetWidth + "px";
      img.style.height = ref.offsetHeight + "px";
      img.setAttribute("width", ref.offsetWidth);
      img.setAttribute("height", ref.offsetHeight);
    }
    onChange(editor.innerHTML);
    updatePageCount();
    setSelectedImg(img
      ? { ...selectedImg, x: d.x, y: d.y, width: ref.offsetWidth, height: ref.offsetHeight }
      : null
    );
  };

  // The *important* part: do not set innerHTML or rerender contentEditable, just pass new HTML to parent and run helpers
  const handleInput = e => {
    enforceImageIds(e.currentTarget);
    onChange(e.currentTarget.innerHTML);    // <-- Parent must NOT reset content on every keypress!
    updatePageCount();
  };

  // On paste: ensure images get IDs/styles
  useEffect(() => {
    const editor = editorRef.current;
    const handlePaste = () => setTimeout(() => enforceImageIds(editor), 0);
    editor && editor.addEventListener('paste', handlePaste);
    return () => editor && editor.removeEventListener('paste', handlePaste);
  }, []);
  useEffect(() => {
    const editor = editorRef.current;
    if (!editor) return;
    function handleLinkClick(e) {
      // Allow only Ctrl+Click (or Cmd+Click) to open the link
      if (e.target.tagName === 'A' && (e.ctrlKey || e.metaKey)) {
        window.open(e.target.href, "_blank");
        e.preventDefault();
      }
    }
    editor.addEventListener('click', handleLinkClick);
    return () => editor.removeEventListener('click', handleLinkClick);
  }, []);


  // Page overlays from your requirements
  const updatePageCount = () => {
    if (editorRef.current) {
      const h = editorRef.current.scrollHeight;
      const count = Math.max(1, Math.ceil(h / PAGE_HEIGHT));
      setPageCount(count);
      if (typeof onPageCountChange === "function") onPageCountChange(count);
    }
  };

  const renderPageOverlays = () => {
    const overlays = [];
    for (let i = 0; i < pageCount; i++) {
      overlays.push(
        <div
          key={i}
          className="editor-page-bg"
          style={{
            position: 'absolute',
            top: `${i * PAGE_HEIGHT}px`,
            left: 0,
            width: '100%',
            height: PAGE_HEIGHT,
            background: '#fff',
            border: '1px solid #ddd',
            zIndex: 0,
            boxSizing: 'border-box',
            pointerEvents: 'none'
          }}
        >
          <div
            className="page-number-overlay"
            style={{
              position: 'absolute',
              bottom: 8,
              left: 0,
              right: 0,
              textAlign: 'center',
              color: '#aaa',
              fontSize: 16,
              pointerEvents: 'none'
            }}
          >
            Page {i + 1}
          </div>
        </div>
      );
    }
    return overlays;
  };

  function renderImageRnd() {
    if (!selectedImg) return null;
    return (
      <Rnd
        key={selectedImg.id}
        size={{ width: selectedImg.width, height: selectedImg.height }}
        position={{ x: selectedImg.x, y: selectedImg.y }}
        bounds=".editor"
        minWidth={32}
        minHeight={32}
        maxWidth={720}
        maxHeight={880}
        style={{
          zIndex: 1002,
          border: "2px solid #2e7ffc",
          background: "#fff",
          boxShadow: "0 0 0 2px #bed7ff",
          pointerEvents: "auto"
        }}
        onDragStop={(e, d) => handleImageDragResizeStop(e, d, e.target)}
        onResizeStop={(e, dir, ref, delta, pos) => handleImageDragResizeStop(e, pos, ref)}
        dragHandleClassName=""
        enableResizing={{
          top: true, right: true, bottom: true, left: true,
          topRight: true, bottomRight: true, bottomLeft: true, topLeft: true
        }}
      >
        <img
          src={selectedImg.src}
          style={{ width: "100%", height: "100%", pointerEvents: "none", userSelect: "none" }}
          alt="Selected"
        />
      </Rnd>
    );
  }

  return (
    <div className="editor-wrapper">
      <div className="page-container" style={{ position: 'relative', minHeight: PAGE_HEIGHT }}>
        {renderPageOverlays()}
        {renderImageRnd()}
        <div
          ref={editorRef}
          className="editor"
          contentEditable={true}
          spellCheck={true}
          onInput={handleInput}
          suppressContentEditableWarning={true}
          style={{
            minHeight: PAGE_HEIGHT * pageCount,
            background: 'transparent',
            position: 'relative',
            zIndex: 1,
            outline: 'none'
          }}
        />
      </div>
      {showTableDialog && (
        <div className="table-dialog">
          <div className="dialog-content">
            <h3>Insert Table</h3>
            <div className="dialog-row">
              <label>Rows:</label>
              <input
                type="number"
                min="1"
                max="20"
                value={tableRows}
                onChange={e => setTableRows(parseInt(e.target.value))}
              />
            </div>
            <div className="dialog-row">
              <label>Columns:</label>
              <input
                type="number"
                min="1"
                max="10"
                value={tableCols}
                onChange={e => setTableCols(parseInt(e.target.value))}
              />
            </div>
            <div className="dialog-actions">
              <button onClick={insertTable}>Insert</button>
              <button onClick={() => setShowTableDialog(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
export default Editor;














