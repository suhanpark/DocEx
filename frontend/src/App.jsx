import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResultView from './components/ResultView';
import Toast from './components/Toast';
import { submitDocument, pollUntilComplete } from './services/api';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [toast, setToast] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    setResult(null);
  };

  const handleSubmit = async () => {
    if (!file) return;

    setIsProcessing(true);
    setResult(null);
    setToast({ type: 'loading', message: 'Uploading...', status: 'pending' });

    try {
      // Submit the document
      const submitResponse = await submitDocument(file);
      const { job_id } = submitResponse;

      // Start polling for status
      setToast({ type: 'loading', message: 'Processing...', status: 'processing' });

      const finalStatus = await pollUntilComplete(job_id, (status) => {
        setJobStatus(status.status);
        setToast({
          type: 'loading',
          message: `Status: ${status.status}`,
          status: status.status,
        });
      });

      // Success - show result
      setResult(finalStatus.result);
      setToast({ type: 'success', message: 'Extraction complete!' });
    } catch (error) {
      console.error('Extraction failed:', error);
      setToast({
        type: 'error',
        message: error.message || 'Extraction failed. Please try again.',
      });
    } finally {
      setIsProcessing(false);
      setJobStatus(null);
    }
  };

  const handleCloseToast = () => {
    setToast(null);
  };

  const handleClearResult = () => {
    setResult(null);
    setFile(null);
  };

  return (
    <div className="app">
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          status={toast.status}
          onClose={handleCloseToast}
        />
      )}

      <header className="app-header">
        <h1>DocEx</h1>
        <p>Document Information Extraction</p>
      </header>

      <main className="app-main">
        {!result ? (
          <div className="upload-section">
            <FileUpload
              onFileSelect={handleFileSelect}
              selectedFile={file}
              isProcessing={isProcessing}
            />

            <button
              className="submit-button"
              onClick={handleSubmit}
              disabled={!file || isProcessing}
            >
              {isProcessing ? 'Processing...' : 'Extract Information'}
            </button>
          </div>
        ) : (
          <ResultView result={result} onClear={handleClearResult} />
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by Fireworks AI - Qwen3 VL 8B</p>
      </footer>
    </div>
  );
}

export default App;
