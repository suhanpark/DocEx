import React from 'react';
import './ResultView.css';

const ResultView = ({ result, onClear }) => {
  if (!result) return null;

  const { document_type, fields, raw_response } = result;

  const formatFieldName = (name) => {
    return name
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (l) => l.toUpperCase());
  };

  return (
    <div className="result-container">
      <div className="result-header">
        <h2 className="result-title">Extraction Results</h2>
        <button className="clear-result-button" onClick={onClear}>
          New Extraction
        </button>
      </div>

      {document_type && (
        <div className="document-type-badge">
          {formatFieldName(document_type)}
        </div>
      )}

      <div className="fields-grid">
        {Object.entries(fields).map(([key, value]) => (
          <div key={key} className="field-card">
            <span className="field-label">{formatFieldName(key)}</span>
            <span className="field-value">
              {value !== null && value !== undefined && value !== ''
                ? String(value)
                : '—'}
            </span>
          </div>
        ))}
      </div>

      {raw_response && (
        <details className="raw-response">
          <summary>View Raw Response</summary>
          <pre>{raw_response}</pre>
        </details>
      )}
    </div>
  );
};

export default ResultView;
