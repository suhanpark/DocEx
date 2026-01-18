import React, { useRef, useState } from 'react';
import './FileUpload.css';

const FileUpload = ({ onFileSelect, selectedFile, isProcessing }) => {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (file) => {
    if (file && file.type.startsWith('image/')) {
      onFileSelect(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleInputChange = (e) => {
    const file = e.target.files[0];
    handleFileChange(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFileChange(file);
  };

  const handleClick = () => {
    if (!isProcessing) {
      fileInputRef.current?.click();
    }
  };

  const clearFile = (e) => {
    e.stopPropagation();
    onFileSelect(null);
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="file-upload-container">
      <div
        className={`drop-zone ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''} ${isProcessing ? 'disabled' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleInputChange}
          className="file-input"
          disabled={isProcessing}
        />

        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Preview" className="preview-image" />
            {!isProcessing && (
              <button className="clear-button" onClick={clearFile}>
                ×
              </button>
            )}
          </div>
        ) : (
          <div className="upload-prompt">
            <div className="upload-icon">📄</div>
            <p className="upload-text">
              Drag and drop your ID document here
            </p>
            <p className="upload-subtext">or click to browse</p>
            <p className="upload-formats">
              Supports: PNG, JPG, JPEG, GIF, BMP
            </p>
          </div>
        )}
      </div>

      {selectedFile && (
        <div className="file-info">
          <span className="file-name">{selectedFile.name}</span>
          <span className="file-size">
            {(selectedFile.size / 1024).toFixed(1)} KB
          </span>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
