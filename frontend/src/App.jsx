import { useState, useRef, useCallback } from 'react';
import ImageComparison from './components/ImageComparison';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || '/api';

const RESTORATION_TYPES = [
  {
    value: 'denoise',
    label: 'Noise Removal',
    icon: '✨',
    description: 'Remove Gaussian & impulse noise',
  },
  {
    value: 'deblur',
    label: 'Image Deblurring',
    icon: '🔍',
    description: 'Sharpen and restore blurry images',
  },
  {
    value: 'super_resolution',
    label: 'Super Resolution',
    icon: '🔬',
    description: 'Upscale image resolution by 2×',
  },
];

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [restoredUrl, setRestoredUrl] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingTime, setProcessingTime] = useState(null);
  const [methodUsed, setMethodUsed] = useState(null);
  const [restorationType, setRestorationType] = useState('denoise');
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = useCallback((file) => {
    if (!file) return;

    const validTypes = ['image/png', 'image/jpeg', 'image/bmp', 'image/tiff', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setError('Invalid file type. Please upload PNG, JPG, BMP, TIFF, or WebP.');
      return;
    }

    if (file.size > 16 * 1024 * 1024) {
      setError('File too large. Maximum size is 16 MB.');
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setRestoredUrl(null);
    setProcessingTime(null);
    setMethodUsed(null);
    setError(null);
  }, []);

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files?.[0];
      handleFileSelect(file);
    },
    [handleFileSelect]
  );

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleRestore = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setError(null);
    setRestoredUrl(null);
    setProcessingTime(null);
    setMethodUsed(null);

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('type', restorationType);

    try {
      const response = await fetch(`${API_URL}/restore`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Processing failed');
      }

      setRestoredUrl(`${API_URL}/image/${data.output_id}/output`);
      setProcessingTime(data.processing_time);
      setMethodUsed(data.method);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = async () => {
    if (!restoredUrl) return;
    try {
      const response = await fetch(restoredUrl);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `restored_${selectedFile.name}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch {
      setError('Failed to download image');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setRestoredUrl(null);
    setProcessingTime(null);
    setMethodUsed(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-glow" />
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <defs>
                  <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#8b5cf6" />
                    <stop offset="100%" stopColor="#06b6d4" />
                  </linearGradient>
                </defs>
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                <circle cx="8.5" cy="8.5" r="1.5" />
                <polyline points="21 15 16 10 5 21" />
              </svg>
            </div>
            <h1>AI Image Restoration</h1>
          </div>
          <p className="header-subtitle">
            Restore your images with AI-powered denoising, deblurring, and super resolution
          </p>
        </div>
      </header>

      <main className="main">
        {/* Upload Section */}
        <section className="upload-section" style={{ animation: 'fadeIn 0.5s ease' }}>
          <div
            id="upload-dropzone"
            className={`upload-zone ${isDragging ? 'dragging' : ''} ${previewUrl ? 'has-image' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => !previewUrl && fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              id="file-input"
              type="file"
              accept="image/png,image/jpeg,image/bmp,image/tiff,image/webp"
              onChange={(e) => handleFileSelect(e.target.files?.[0])}
              hidden
            />

            {!previewUrl ? (
              <div className="upload-placeholder">
                <div className="upload-icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="17 8 12 3 7 8" />
                    <line x1="12" y1="3" x2="12" y2="15" />
                  </svg>
                </div>
                <p className="upload-text">
                  <span className="upload-text-main">Drop your image here</span>
                  <span className="upload-text-sub">or click to browse · PNG, JPG, BMP, TIFF, WebP · Max 16 MB</span>
                </p>
              </div>
            ) : (
              <div className="preview-container">
                <img src={previewUrl} alt="Preview" className="preview-image" />
                <button id="btn-change-image" className="change-image-btn" onClick={(e) => { e.stopPropagation(); handleReset(); }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                  Change Image
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Controls Section */}
        {previewUrl && (
          <section className="controls-section" style={{ animation: 'slideUp 0.4s ease' }}>
            <div className="controls-card">
              <div className="control-group">
                <label className="control-label" htmlFor="restoration-type">Restoration Type</label>
                <div className="type-selector">
                  {RESTORATION_TYPES.map((type) => (
                    <button
                      key={type.value}
                      id={`btn-type-${type.value}`}
                      className={`type-option ${restorationType === type.value ? 'active' : ''}`}
                      onClick={() => setRestorationType(type.value)}
                    >
                      <span className="type-icon">{type.icon}</span>
                      <span className="type-label">{type.label}</span>
                      <span className="type-desc">{type.description}</span>
                    </button>
                  ))}
                </div>
              </div>

              <button
                id="btn-restore"
                className={`restore-btn ${isProcessing ? 'processing' : ''}`}
                onClick={handleRestore}
                disabled={isProcessing}
              >
                {isProcessing ? (
                  <>
                    <span className="spinner" />
                    Processing…
                  </>
                ) : (
                  <>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M12 2L2 7l10 5 10-5-10-5z" />
                      <path d="M2 17l10 5 10-5" />
                      <path d="M2 12l10 5 10-5" />
                    </svg>
                    Restore Image
                  </>
                )}
              </button>
            </div>
          </section>
        )}

        {/* Error Display */}
        {error && (
          <div className="error-toast" style={{ animation: 'slideUp 0.3s ease' }}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            <span>{error}</span>
            <button className="error-dismiss" onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {/* Results Section */}
        {restoredUrl && (
          <section className="results-section" style={{ animation: 'slideUp 0.5s ease' }}>
            {/* Stats Bar */}
            <div className="stats-bar">
              <div className="stat">
                <span className="stat-label">Processing Time</span>
                <span className="stat-value">{processingTime}s</span>
              </div>
              <div className="stat">
                <span className="stat-label">Method</span>
                <span className="stat-value">{methodUsed}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Type</span>
                <span className="stat-value">
                  {RESTORATION_TYPES.find((t) => t.value === restorationType)?.label}
                </span>
              </div>
              <button id="btn-download" className="download-btn" onClick={handleDownload}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                Download
              </button>
            </div>

            {/* Comparison Slider */}
            <ImageComparison originalUrl={previewUrl} restoredUrl={restoredUrl} />
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>Built with React, Flask, OpenCV & PyTorch</p>
      </footer>
    </div>
  );
}
