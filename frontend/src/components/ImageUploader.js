import React, { useState, useRef } from 'react';
import './ImageUploader.css';

function ImageUploader({ onImageInsert }) {
  const [uploading, setUploading] = useState(false);
  const [uploadedImages, setUploadedImages] = useState([]);
  const fileInputRef = useRef(null);

  const handleFileSelect = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    setUploading(true);

    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/api/images/upload-multiple', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      
      if (result.uploaded && result.uploaded.length > 0) {
        setUploadedImages([...uploadedImages, ...result.uploaded]);
        alert(`Successfully uploaded ${result.success} image(s)`);
      }

      if (result.errors && result.errors.length > 0) {
        console.error('Upload errors:', result.errors);
        alert(`Failed to upload ${result.failed} image(s)`);
      }
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to upload images');
    }

    setUploading(false);
    fileInputRef.current.value = '';
  };

  const insertImage = (imageInfo) => {
    const imgHTML = `<img src="http://localhost:8000${imageInfo.url}" 
                          style="max-width: 100%; height: auto;" 
                          alt="${imageInfo.original_filename}" />`;
    
    document.execCommand('insertHTML', false, imgHTML);
    
    if (onImageInsert) {
      onImageInsert(imageInfo);
    }
  };

  return (
    <div className="image-uploader">
      <div className="upload-section">
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          multiple
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        
        <button 
          className="upload-btn"
          onClick={() => fileInputRef.current.click()}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : '📷 Upload Images'}
        </button>
      </div>

      {uploadedImages.length > 0 && (
        <div className="images-gallery">
          <h4>Uploaded Images</h4>
          <div className="gallery-grid">
            {uploadedImages.map((img, index) => (
              <div key={index} className="gallery-item">
                <img 
                  src={`http://localhost:8000${img.url}`} 
                  alt={img.original_filename}
                  onClick={() => insertImage(img)}
                />
                <div className="image-info">
                  <p className="image-name">{img.original_filename}</p>
                  <p className="image-size">{img.width}×{img.height}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ImageUploader;
