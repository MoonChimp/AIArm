import { useState, useRef, useEffect } from 'react';
import './FluxPage.css';
import { FLUX_API } from '../config/api';

export default function FluxPage() {
  const [prompt, setPrompt] = useState('');
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('checking');
  const [progress, setProgress] = useState(null);
  const [settings, setSettings] = useState({
    width: 1024,
    height: 1024,
    steps: 4,
    guidance: 0.0
  });
  const galleryRef = useRef(null);

  useEffect(() => {
    checkHealthAndActivate();
  }, []);

  const checkHealthAndActivate = async () => {
    try {
      const response = await fetch(`${FLUX_API}/health`);
      if (response.ok) {
        setStatus('ready');
      } else {
        setStatus('error');
      }
    } catch (error) {
      console.error('Image service not available:', error);
      setStatus('offline');
    }
  };

  const generateImage = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || loading || status !== 'ready') return;

    setLoading(true);
    setProgress({ stage: 'Connecting...', percent: 0 });

    try {
      const response = await fetch(`${FLUX_API}/generate/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: prompt.trim(),
          width: settings.width,
          height: settings.height,
          num_inference_steps: settings.steps,
          guidance_scale: settings.guidance
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';  // Buffer for incomplete SSE messages

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Split on double newline (SSE message separator)
        const messages = buffer.split('\n\n');
        // Keep the last incomplete message in buffer
        buffer = messages.pop() || '';

        for (const message of messages) {
          const lines = message.split('\n');
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));

                if (data.type === 'status') {
                  setProgress({ stage: data.message, percent: 50 });
                } else if (data.type === 'complete') {
                  console.log('Received complete, image_base64 length:', data.image_base64?.length || 0);
                  setImages(prev => [{
                    base64: data.image_base64,
                    filename: data.filename,
                    prompt: prompt.trim(),
                    source: data.source,
                    time: data.generation_time
                  }, ...prev]);
                  setProgress(null);
                } else if (data.type === 'error') {
                  console.error('Generation error:', data.message);
                  setProgress({ stage: `Error: ${data.message}`, percent: 0 });
                }
              } catch (e) {
                console.error('Parse error:', e, 'Line:', line.substring(0, 100));
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Generation failed:', error);
      setProgress({ stage: 'Connection failed', percent: 0 });
    } finally {
      setLoading(false);
      setTimeout(() => setProgress(null), 2000);
    }
  };

  const downloadImage = (image) => {
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${image.base64}`;
    link.download = image.filename;
    link.click();
  };

  return (
    <div className="flux-page">
      <div className="flux-header">
        <div className="header-content">
          <h1>NeXus Image Gen</h1>
          <p>High-quality AI image generation from text descriptions</p>
        </div>
        <div className="service-status">
          <span className={`status-indicator ${status}`}></span>
          <span className="status-text">
            {status === 'checking' && 'Connecting...'}
            {status === 'loading' && 'Initializing...'}
            {status === 'ready' && 'Ready'}
            {status === 'offline' && 'Offline'}
            {status === 'error' && 'Error'}
          </span>
        </div>
      </div>

      <div className="flux-content">
        <div className="generation-panel">
          <form onSubmit={generateImage} className="prompt-form">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the image you want to generate..."
              disabled={loading || status !== 'ready'}
              rows={3}
            />

            <div className="settings-row">
              <div className="setting">
                <label>Size</label>
                <select
                  value={`${settings.width}x${settings.height}`}
                  onChange={(e) => {
                    const [w, h] = e.target.value.split('x').map(Number);
                    setSettings(s => ({ ...s, width: w, height: h }));
                  }}
                >
                  <option value="512x512">512x512</option>
                  <option value="768x768">768x768</option>
                  <option value="1024x1024">1024x1024</option>
                  <option value="1024x768">1024x768 (Landscape)</option>
                  <option value="768x1024">768x1024 (Portrait)</option>
                </select>
              </div>

              <div className="setting">
                <label>Steps: {settings.steps}</label>
                <input
                  type="range"
                  min="1"
                  max="8"
                  value={settings.steps}
                  onChange={(e) => setSettings(s => ({ ...s, steps: Number(e.target.value) }))}
                />
              </div>

              <button
                type="submit"
                disabled={loading || !prompt.trim() || status !== 'ready'}
                className="generate-button"
              >
                {loading ? 'Generating...' : 'Generate'}
              </button>
            </div>
          </form>

          {progress && (
            <div className="progress-section">
              <div className="progress-label">{progress.stage}</div>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: loading ? '100%' : `${progress.percent}%` }}
                />
              </div>
            </div>
          )}
        </div>

        <div className="gallery-panel" ref={galleryRef}>
          <h2>Generated Images</h2>
          {images.length === 0 ? (
            <div className="empty-gallery">
              <p>Your generated images will appear here</p>
            </div>
          ) : (
            <div className="image-grid">
              {images.map((img, idx) => (
                <div key={idx} className="image-card">
                  <img
                    src={`data:image/png;base64,${img.base64}`}
                    alt={img.prompt}
                  />
                  <div className="image-overlay">
                    <div className="image-info">
                      <p className="image-prompt">{img.prompt}</p>
                    </div>
                    <button
                      className="download-button"
                      onClick={() => downloadImage(img)}
                    >
                      Download
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
