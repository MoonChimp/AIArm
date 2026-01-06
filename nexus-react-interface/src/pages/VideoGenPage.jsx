import { useState, useRef, useEffect } from 'react';
import './VideoGenPage.css';
import { VIDEO_API } from '../config/api';

export default function VideoGenPage() {
  const [prompt, setPrompt] = useState('');
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('checking');
  const [progress, setProgress] = useState(null);
  const [settings, setSettings] = useState({
    num_frames: 49,  // CogVideoX-5B default: ~6 seconds at 8fps
    fps: 8,          // CogVideoX native fps (fixed)
    guidance: 6.0,   // Optimal guidance for CogVideoX-5B
    inference_steps: 50  // Higher for better quality
  });
  const galleryRef = useRef(null);

  useEffect(() => {
    checkHealthAndActivate();
  }, []);

  const checkHealthAndActivate = async () => {
    try {
      const response = await fetch(`${VIDEO_API}/health`);
      if (response.ok) {
        setStatus('ready');
      } else {
        setStatus('error');
      }
    } catch (error) {
      console.error('Video service not available:', error);
      setStatus('offline');
    }
  };

  const generateVideo = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || loading || status !== 'ready') return;

    setLoading(true);
    setProgress({ stage: 'Initializing video generation...', percent: 0 });

    try {
      const response = await fetch(`${VIDEO_API}/generate/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: prompt.trim(),
          num_frames: settings.num_frames,
          fps: settings.fps,
          guidance_scale: settings.guidance,
          num_inference_steps: settings.inference_steps
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));

              if (data.type === 'status') {
                setProgress({ stage: data.message, percent: 50 });
              } else if (data.type === 'complete') {
                setVideos(prev => [{
                  base64: data.video_base64,
                  filename: data.filename,
                  prompt: prompt.trim(),
                  time: data.generation_time
                }, ...prev]);
                setProgress(null);
              } else if (data.type === 'error') {
                console.error('Generation error:', data.message);
                setProgress({ stage: `Error: ${data.message}`, percent: 0 });
              }
            } catch (e) {
              console.error('Parse error:', e);
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

  const downloadVideo = (video) => {
    const link = document.createElement('a');
    link.href = `data:video/mp4;base64,${video.base64}`;
    link.download = video.filename;
    link.click();
  };

  return (
    <div className="videogen-page">
      <div className="videogen-header">
        <div className="header-content">
          <h1>NeXus Video Gen</h1>
          <p>AI-powered video creation from text prompts</p>
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

      <div className="videogen-content">
        <div className="generation-panel">
          <form onSubmit={generateVideo} className="prompt-form">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the video you want to generate..."
              disabled={loading || status !== 'ready'}
              rows={3}
            />

            <div className="settings-row">
              <div className="setting">
                <label>Duration</label>
                <select
                  value={settings.num_frames}
                  onChange={(e) => setSettings(s => ({ ...s, num_frames: Number(e.target.value) }))}
                >
                  <option value="25">~3 seconds (Fast)</option>
                  <option value="49">~6 seconds (Default)</option>
                  <option value="81">~10 seconds (Long)</option>
                </select>
              </div>

              <div className="setting">
                <label>Quality Steps: {settings.inference_steps}</label>
                <input
                  type="range"
                  min="30"
                  max="75"
                  step="5"
                  value={settings.inference_steps}
                  onChange={(e) => setSettings(s => ({ ...s, inference_steps: Number(e.target.value) }))}
                />
              </div>

              <div className="setting">
                <label>Guidance: {settings.guidance}</label>
                <input
                  type="range"
                  min="3"
                  max="9"
                  step="0.5"
                  value={settings.guidance}
                  onChange={(e) => setSettings(s => ({ ...s, guidance: Number(e.target.value) }))}
                />
              </div>

              <button
                type="submit"
                disabled={loading || !prompt.trim() || status !== 'ready'}
                className="generate-button"
              >
                {loading ? 'Generating...' : 'Generate Video'}
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
              {loading && (
                <div className="progress-hint">
                  Video generation may take several minutes
                </div>
              )}
            </div>
          )}
        </div>

        <div className="gallery-panel" ref={galleryRef}>
          <h2>Generated Videos</h2>
          {videos.length === 0 ? (
            <div className="empty-gallery">
              <p>Your generated videos will appear here</p>
            </div>
          ) : (
            <div className="video-grid">
              {videos.map((vid, idx) => (
                <div key={idx} className="video-card">
                  <video
                    src={`data:video/mp4;base64,${vid.base64}`}
                    controls
                    loop
                    muted
                    playsInline
                  />
                  <div className="video-info">
                    <p className="video-prompt">{vid.prompt}</p>
                    <button
                      className="download-button"
                      onClick={() => downloadVideo(vid)}
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
