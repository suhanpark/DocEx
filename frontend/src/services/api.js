const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/extract`
  : '/api/extract';

export async function submitDocument(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/submit`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to submit document');
  }

  return response.json();
}

export async function checkJobStatus(jobId) {
  const response = await fetch(`${API_BASE}/status/${jobId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to check status');
  }

  return response.json();
}

export function pollUntilComplete(jobId, onStatusChange, interval = 1500) {
  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        const status = await checkJobStatus(jobId);
        onStatusChange(status);

        if (status.status === 'completed') {
          resolve(status);
        } else if (status.status === 'failed') {
          reject(new Error(status.error || 'Extraction failed'));
        } else {
          setTimeout(poll, interval);
        }
      } catch (error) {
        reject(error);
      }
    };

    poll();
  });
}
