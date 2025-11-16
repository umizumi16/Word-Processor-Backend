// // import React, { useState } from 'react';
// // import './FormatToolbar.css';

// // function FormatToolbar() {
// //   const [fontSize, setFontSize] = useState('16px');
// //   const [fontFamily, setFontFamily] = useState('Calibri');

// //   const applyFormat = (command, value = null) => {
// //     document.execCommand(command, false, value);
// //   };

// //   const handleFontSizeChange = (e) => {
// //     const size = e.target.value;
// //     setFontSize(size);
// //     applyFormat('fontSize', size);
// //   };

// //   const handleFontFamilyChange = (e) => {
// //     const font = e.target.value;
// //     setFontFamily(font);
// //     applyFormat('fontName', font);
// //   };

// //   return (
// //     <div className="format-toolbar">
// //       <div className="toolbar-group">
// //         <select 
// //           className="font-family-select"
// //           value={fontFamily}
// //           onChange={handleFontFamilyChange}
// //         >
// //           <option value="Arial">Arial</option>
// //           <option value="Calibri">Calibri</option>
// //           <option value="Times New Roman">Times New Roman</option>
// //           <option value="Georgia">Georgia</option>
// //           <option value="Verdana">Verdana</option>
// //           <option value="Courier New">Courier New</option>
// //           <option value="Comic Sans MS">Comic Sans MS</option>
// //         </select>

// //         <select 
// //           className="font-size-select"
// //           value={fontSize}
// //           onChange={handleFontSizeChange}
// //         >
// //           <option value="8px">8</option>
// //           <option value="9px">9</option>
// //           <option value="10px">10</option>
// //           <option value="11px">11</option>
// //           <option value="12px">12</option>
// //           <option value="14px">14</option>
// //           <option value="16px">16</option>
// //           <option value="18px">18</option>
// //           <option value="20px">20</option>
// //           <option value="22px">22</option>
// //           <option value="24px">24</option>
// //           <option value="26px">26</option>
// //           <option value="28px">28</option>
// //           <option value="36px">36</option>
// //           <option value="48px">48</option>
// //           <option value="72px">72</option>
// //         </select>
// //       </div>

// //       <div className="toolbar-divider"></div>

// //       <div className="toolbar-group">
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('bold')}
// //           title="Bold (Ctrl+B)"
// //         >
// //           <strong>B</strong>
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('italic')}
// //           title="Italic (Ctrl+I)"
// //         >
// //           <em>I</em>
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('underline')}
// //           title="Underline (Ctrl+U)"
// //         >
// //           <u>U</u>
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('strikeThrough')}
// //           title="Strikethrough"
// //         >
// //           <s>S</s>
// //         </button>
// //       </div>

// //       <div className="toolbar-divider"></div>

// //       <div className="toolbar-group">
// //         <input 
// //           type="color"
// //           className="color-picker"
// //           onChange={(e) => applyFormat('foreColor', e.target.value)}
// //           title="Text Color"
// //         />
// //         <input 
// //           type="color"
// //           className="color-picker"
// //           onChange={(e) => applyFormat('hiliteColor', e.target.value)}
// //           title="Highlight Color"
// //         />
// //       </div>

// //       <div className="toolbar-divider"></div>

// //       <div className="toolbar-group">
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('justifyLeft')}
// //           title="Align Left"
// //         >
// //           ☰
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('justifyCenter')}
// //           title="Align Center"
// //         >
// //           ☰
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('justifyRight')}
// //           title="Align Right"
// //         >
// //           ☰
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('justifyFull')}
// //           title="Justify"
// //         >
// //           ☰
// //         </button>
// //       </div>

// //       <div className="toolbar-divider"></div>

// //       <div className="toolbar-group">
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('insertUnorderedList')}
// //           title="Bullet List"
// //         >
// //           • List
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('insertOrderedList')}
// //           title="Numbered List"
// //         >
// //           1. List
// //         </button>
// //       </div>

// //       <div className="toolbar-divider"></div>

// //       <div className="toolbar-group">
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('indent')}
// //           title="Increase Indent"
// //         >
// //           →
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('outdent')}
// //           title="Decrease Indent"
// //         >
// //           ←
// //         </button>
// //       </div>

// //       <div className="toolbar-divider"></div>

// //       <div className="toolbar-group">
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('formatBlock', 'H1')}
// //           title="Heading 1"
// //         >
// //           H1
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('formatBlock', 'H2')}
// //           title="Heading 2"
// //         >
// //           H2
// //         </button>
// //         <button 
// //           className="toolbar-btn"
// //           onClick={() => applyFormat('formatBlock', 'H3')}
// //           title="Heading 3"
// //         >
// //           H3
// //         </button>
// //       </div>
// //     </div>
// //   );
// // }

// // export default FormatToolbar;

// import React, { useState } from 'react';
// import './FormatToolbar.css';

// function FormatToolbar() {
//   const [fontSize, setFontSize] = useState('16px');
//   const [fontFamily, setFontFamily] = useState('Calibri');

//   const applyFormat = (command, value = null) => {
//     // Apply formatting
//     document.execCommand(command, false, value);
    
//     // Restore focus to editor immediately
//     const editor = document.querySelector('.editor');
//     if (editor) {
//       editor.focus();
//     }
//   };

//   const handleFontSizeChange = (e) => {
//     const size = e.target.value;
//     setFontSize(size);
//     applyFormat('fontSize', size);
//   };

//   const handleFontFamilyChange = (e) => {
//     const font = e.target.value;
//     setFontFamily(font);
//     applyFormat('fontName', font);
//   };

//   return (
//     <div className="format-toolbar">
//       <div className="toolbar-group">
//         <select 
//           className="font-family-select"
//           value={fontFamily}
//           onChange={handleFontFamilyChange}
//         >
//           <option value="Arial">Arial</option>
//           <option value="Calibri">Calibri</option>
//           <option value="Times New Roman">Times New Roman</option>
//           <option value="Georgia">Georgia</option>
//           <option value="Verdana">Verdana</option>
//           <option value="Courier New">Courier New</option>
//         </select>

//         <select 
//           className="font-size-select"
//           value={fontSize}
//           onChange={handleFontSizeChange}
//         >
//           <option value="8px">8</option>
//           <option value="10px">10</option>
//           <option value="12px">12</option>
//           <option value="14px">14</option>
//           <option value="16px">16</option>
//           <option value="18px">18</option>
//           <option value="20px">20</option>
//           <option value="24px">24</option>
//           <option value="28px">28</option>
//           <option value="36px">36</option>
//         </select>
//       </div>

//       <div className="toolbar-divider"></div>

//       <div className="toolbar-group">
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault(); // Prevent focus loss
//             applyFormat('bold');
//           }}
//           title="Bold (Ctrl+B)"
//         >
//           <strong>B</strong>
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('italic');
//           }}
//           title="Italic (Ctrl+I)"
//         >
//           <em>I</em>
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('underline');
//           }}
//           title="Underline (Ctrl+U)"
//         >
//           <u>U</u>
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('strikeThrough');
//           }}
//           title="Strikethrough"
//         >
//           <s>S</s>
//         </button>
//       </div>

//       <div className="toolbar-divider"></div>

//       <div className="toolbar-group">
//         <input 
//           type="color"
//           className="color-picker"
//           onChange={(e) => applyFormat('foreColor', e.target.value)}
//           onMouseDown={(e) => e.preventDefault()}
//           title="Text Color"
//         />
//         <input 
//           type="color"
//           className="color-picker"
//           onChange={(e) => applyFormat('hiliteColor', e.target.value)}
//           onMouseDown={(e) => e.preventDefault()}
//           title="Highlight Color"
//         />
//       </div>

//       <div className="toolbar-divider"></div>

//       <div className="toolbar-group">
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('justifyLeft');
//           }}
//           title="Align Left"
//         >
//           ☰
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('justifyCenter');
//           }}
//           title="Align Center"
//         >
//           ☰
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('justifyRight');
//           }}
//           title="Align Right"
//         >
//           ☰
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('justifyFull');
//           }}
//           title="Justify"
//         >
//           ☰
//         </button>
//       </div>

//       <div className="toolbar-divider"></div>

//       <div className="toolbar-group">
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('insertUnorderedList');
//           }}
//           title="Bullet List"
//         >
//           • List
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('insertOrderedList');
//           }}
//           title="Numbered List"
//         >
//           1. List
//         </button>
//       </div>

//       <div className="toolbar-divider"></div>

//       <div className="toolbar-group">
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('indent');
//           }}
//           title="Increase Indent"
//         >
//           →
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('outdent');
//           }}
//           title="Decrease Indent"
//         >
//           ←
//         </button>
//       </div>

//       <div className="toolbar-divider"></div>

//       <div className="toolbar-group">
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('formatBlock', 'H1');
//           }}
//           title="Heading 1"
//         >
//           H1
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('formatBlock', 'H2');
//           }}
//           title="Heading 2"
//         >
//           H2
//         </button>
//         <button 
//           className="toolbar-btn"
//           onMouseDown={(e) => {
//             e.preventDefault();
//             applyFormat('formatBlock', 'H3');
//           }}
//           title="Heading 3"
//         >
//           H3
//         </button>
//       </div>
//     </div>
//   );
// }

// export default FormatToolbar;

import React, { useState } from 'react';
import './FormatToolbar.css';

function FormatToolbar() {
  const [fontSize, setFontSize] = useState('16px');
  const [fontFamily, setFontFamily] = useState('Calibri');

  const applyFormat = (command, value = null) => {
    document.execCommand(command, false, value);
    const editor = document.querySelector('.editor');
    if (editor) {
      editor.focus();
    }
  };

  const applyHeading = (level) => {
    const selection = window.getSelection();
    if (!selection.rangeCount) return;

    const range = selection.getRangeAt(0);
    
    // Get the selected text or current line
    let selectedText = selection.toString();
    
    // If nothing is selected, select the current line/paragraph
    if (!selectedText) {
      const node = selection.anchorNode;
      if (node.nodeType === Node.TEXT_NODE) {
        range.selectNode(node);
        selectedText = node.textContent;
      }
    }

    // Check if already a heading
    const parentElement = range.commonAncestorContainer.parentElement;
    const isHeading = /^H[1-6]$/.test(parentElement.tagName);
    
    if (isHeading) {
      // Remove heading - convert back to paragraph
      const p = document.createElement('p');
      p.innerHTML = parentElement.innerHTML;
      parentElement.parentNode.replaceChild(p, parentElement);
    } else {
      // Apply heading
      document.execCommand('formatBlock', false, `H${level}`);
    }

    // Restore focus
    const editor = document.querySelector('.editor');
    if (editor) {
      editor.focus();
    }
  };

  const handleFontSizeChange = (e) => {
    const size = e.target.value;
    setFontSize(size);
    applyFormat('fontSize', size);
  };

  const handleFontFamilyChange = (e) => {
    const font = e.target.value;
    setFontFamily(font);
    applyFormat('fontName', font);
  };

  return (
    <div className="format-toolbar">
      <div className="toolbar-group">
        <select 
          className="font-family-select"
          value={fontFamily}
          onChange={handleFontFamilyChange}
        >
          <option value="Arial">Arial</option>
          <option value="Calibri">Calibri</option>
          <option value="Times New Roman">Times New Roman</option>
          <option value="Georgia">Georgia</option>
          <option value="Verdana">Verdana</option>
          <option value="Courier New">Courier New</option>
        </select>

        <select 
          className="font-size-select"
          value={fontSize}
          onChange={handleFontSizeChange}
        >
          <option value="8px">8</option>
          <option value="10px">10</option>
          <option value="12px">12</option>
          <option value="14px">14</option>
          <option value="16px">16</option>
          <option value="18px">18</option>
          <option value="20px">20</option>
          <option value="24px">24</option>
          <option value="28px">28</option>
          <option value="36px">36</option>
          <option value="48px">48</option>
        </select>
      </div>

      <div className="toolbar-divider"></div>

      <div className="toolbar-group">
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('bold');
          }}
          title="Bold (Ctrl+B)"
        >
          <strong>B</strong>
        </button>
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('italic');
          }}
          title="Italic (Ctrl+I)"
        >
          <em>I</em>
        </button>
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('underline');
          }}
          title="Underline (Ctrl+U)"
        >
          <u>U</u>
        </button>
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('strikeThrough');
          }}
          title="Strikethrough"
        >
          <s>S</s>
        </button>
      </div>

      <div className="toolbar-divider"></div>

      <div className="toolbar-group">
        <input 
          type="color"
          className="color-picker"
          onChange={(e) => applyFormat('foreColor', e.target.value)}
          onMouseDown={(e) => e.preventDefault()}
          title="Text Color"
        />
        <input 
          type="color"
          className="color-picker"
          onChange={(e) => applyFormat('hiliteColor', e.target.value)}
          onMouseDown={(e) => e.preventDefault()}
          title="Highlight Color"
        />
      </div>

      <div className="toolbar-divider"></div>

      <div className="toolbar-group">
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('justifyLeft');
          }}
          title="Align Left"
        >
          ☰
        </button>
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('justifyCenter');
          }}
          title="Align Center"
        >
          ☰
        </button>
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('justifyRight');
          }}
          title="Align Right"
        >
          ☰
        </button>
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('justifyFull');
          }}
          title="Justify"
        >
          ☰
        </button>
      </div>

      <div className="toolbar-divider"></div>

      <div className="toolbar-group">
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('insertUnorderedList');
          }}
          title="Bullet List"
        >
          • List
        </button>
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('insertOrderedList');
          }}
          title="Numbered List"
        >
          1. List
        </button>
      </div>

      <div className="toolbar-divider"></div>

      <div className="toolbar-group">
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('indent');
          }}
          title="Increase Indent"
        >
          →
        </button>
        <button 
          className="toolbar-btn"
          onMouseDown={(e) => {
            e.preventDefault();
            applyFormat('outdent');
          }}
          title="Decrease Indent"
        >
          ←
        </button>
      </div>

      <div className="toolbar-divider"></div>

      <div className="toolbar-group">
        <button 
          className="toolbar-btn toolbar-heading"
          onMouseDown={(e) => {
            e.preventDefault();
            applyHeading(1);
          }}
          title="Heading 1 (32pt)"
        >
          H1
        </button>
        <button 
          className="toolbar-btn toolbar-heading"
          onMouseDown={(e) => {
            e.preventDefault();
            applyHeading(2);
          }}
          title="Heading 2 (24pt)"
        >
          H2
        </button>
        <button 
          className="toolbar-btn toolbar-heading"
          onMouseDown={(e) => {
            e.preventDefault();
            applyHeading(3);
          }}
          title="Heading 3 (18pt)"
        >
          H3
        </button>
      </div>
    </div>
  );
}

export default FormatToolbar;
