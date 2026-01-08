import { useState, useRef, useEffect, useMemo } from 'react';
import Editor from '@monaco-editor/react';
import './DeepSitePage.css';
import { API_URL } from '../config/api';

export default function DeepSitePage() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [status, setStatus] = useState('ready');
  const [pages, setPages] = useState([{ path: 'index.html', html: '' }]);
  const [currentPage, setCurrentPage] = useState('index.html');
  const [messages, setMessages] = useState([]);
  const editorRef = useRef(null);
  const previewRef = useRef(null);

  // Get current page data
  const currentPageData = useMemo(() => {
    return pages.find(p => p.path === currentPage) || { path: 'index.html', html: '' };
  }, [pages, currentPage]);

  // Determine editor language based on file extension
  const editorLanguage = useMemo(() => {
    const path = currentPageData.path;
    if (path.endsWith('.css')) return 'css';
    if (path.endsWith('.js')) return 'javascript';
    if (path.endsWith('.json')) return 'json';
    return 'html';
  }, [currentPageData.path]);

  // Parse streaming content into pages
  const parseStreamingContent = (content) => {
    const newPages = [];

    // Check for file markers
    const hasMarkers = content.includes('<<<<<<< NEW_FILE_START');

    if (!hasMarkers) {
      // Handle raw HTML without markers
      let htmlContent = content.trim();

      // Extract from markdown code block if present
      const htmlCodeBlockMatch = htmlContent.match(/```html\s*([\s\S]*?)(?:```|$)/i);
      if (htmlCodeBlockMatch && htmlCodeBlockMatch[1]) {
        htmlContent = htmlCodeBlockMatch[1].trim();
      } else if (!htmlContent.startsWith('<!DOCTYPE') && !htmlContent.startsWith('<html')) {
        // Try to find HTML content
        const doctypeMatch = htmlContent.match(/(<!DOCTYPE[\s\S]*)/i);
        const htmlTagMatch = htmlContent.match(/(<html[\s\S]*)/i);
        htmlContent = doctypeMatch?.[1] || htmlTagMatch?.[1] || htmlContent;
      }

      if (htmlContent.includes('<') && htmlContent.includes('>')) {
        newPages.push({ path: 'index.html', html: ensureCompleteHtml(htmlContent) });
      }
      return newPages;
    }

    // Parse marked files
    const fileRegex = /<<<<<<< NEW_FILE_START ([\w\/.]+) >>>>>>> NEW_FILE_END\s*([\s\S]*?)(?=<<<<<<< NEW_FILE_START|$)/g;
    let match;

    while ((match = fileRegex.exec(content)) !== null) {
      const filePath = match[1].trim();
      let fileContent = match[2].trim();

      // Clean up code blocks
      if (filePath.endsWith('.css')) {
        const cssMatch = fileContent.match(/```css\s*([\s\S]*?)\s*```/);
        fileContent = cssMatch ? cssMatch[1] : fileContent.replace(/```css\s*/i, '').replace(/```/g, '');
      } else if (filePath.endsWith('.js')) {
        const jsMatch = fileContent.match(/```(?:javascript|js)\s*([\s\S]*?)\s*```/);
        fileContent = jsMatch ? jsMatch[1] : fileContent.replace(/```(?:javascript|js)\s*/i, '').replace(/```/g, '');
      } else {
        const htmlMatch = fileContent.match(/```html\s*([\s\S]*?)\s*```/);
        fileContent = htmlMatch ? htmlMatch[1] : fileContent.replace(/```html\s*/i, '').replace(/```/g, '');
        fileContent = ensureCompleteHtml(fileContent);
      }

      if (fileContent.trim()) {
        newPages.push({ path: filePath, html: fileContent.trim() });
      }
    }

    return newPages;
  };

  const ensureCompleteHtml = (html) => {
    let completeHtml = html;
    if (completeHtml.includes('<head>') && !completeHtml.includes('</head>')) {
      completeHtml += '\n</head>';
    }
    if (completeHtml.includes('<body') && !completeHtml.includes('</body>')) {
      completeHtml += '\n</body>';
    }
    if (completeHtml.includes('<html') && !completeHtml.includes('</html>')) {
      completeHtml += '\n</html>';
    }
    return completeHtml;
  };

  // Generate website using streaming API
  const generateWebsite = async (e) => {
    e?.preventDefault();
    if (!prompt.trim() || isGenerating) return;

    setIsGenerating(true);
    setStatus('generating');
    setPages([{ path: 'index.html', html: '<!-- Generating... -->' }]);
    setMessages(prev => [...prev, { role: 'user', content: prompt }]);

    try {
      const response = await fetch(`${API_URL}/api/website/generate/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: prompt.trim(),
          model: 'auto'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);

            if (data === '[DONE]') {
              continue;
            }

            try {
              const parsed = JSON.parse(data);

              if (parsed.type === 'chunk' && parsed.content) {
                fullContent += parsed.content;
                const parsedPages = parseStreamingContent(fullContent);
                if (parsedPages.length > 0) {
                  setPages(parsedPages);
                  // Auto-select first HTML page for preview
                  const htmlPage = parsedPages.find(p => p.path.endsWith('.html'));
                  if (htmlPage && currentPage !== htmlPage.path) {
                    setCurrentPage(htmlPage.path);
                  }
                }
              } else if (parsed.type === 'complete') {
                setStatus('ready');
                setMessages(prev => [...prev, {
                  role: 'assistant',
                  content: `Website generated successfully! ${pages.length} file(s) created.`
                }]);
              } else if (parsed.type === 'error') {
                throw new Error(parsed.message);
              }
            } catch (parseError) {
              // If not JSON, treat as raw content
              if (!data.startsWith('{')) {
                fullContent += data;
                const parsedPages = parseStreamingContent(fullContent);
                if (parsedPages.length > 0) {
                  setPages(parsedPages);
                }
              }
            }
          }
        }
      }

      // Final parse
      const finalPages = parseStreamingContent(fullContent);
      if (finalPages.length > 0) {
        setPages(finalPages);
      }

      setStatus('ready');
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Website generated! ${finalPages.length} file(s) created.`
      }]);

    } catch (error) {
      console.error('Generation error:', error);
      setStatus('error');
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error.message}`,
        isError: true
      }]);
    } finally {
      setIsGenerating(false);
      setPrompt('');
    }
  };

  // Update page content from editor
  const handleEditorChange = (value) => {
    setPages(prev => prev.map(page =>
      page.path === currentPage ? { ...page, html: value || '' } : page
    ));
  };

  // Copy code to clipboard
  const copyCode = () => {
    navigator.clipboard.writeText(currentPageData.html);
  };

  // Download current file
  const downloadFile = () => {
    const blob = new Blob([currentPageData.html], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = currentPageData.path;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Download all files as zip (simplified - just downloads index.html)
  const downloadAll = () => {
    // Combine all files into a single HTML with embedded CSS/JS
    let combinedHtml = pages.find(p => p.path === 'index.html')?.html || '';

    const cssPage = pages.find(p => p.path === 'style.css' || p.path === 'styles.css');
    const jsPage = pages.find(p => p.path === 'script.js' || p.path === 'main.js');

    if (cssPage && !combinedHtml.includes(cssPage.html)) {
      combinedHtml = combinedHtml.replace('</head>', `<style>\n${cssPage.html}\n</style>\n</head>`);
    }
    if (jsPage && !combinedHtml.includes(jsPage.html)) {
      combinedHtml = combinedHtml.replace('</body>', `<script>\n${jsPage.html}\n</script>\n</body>`);
    }

    const blob = new Blob([combinedHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'website.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Get combined HTML for preview
  const previewHtml = useMemo(() => {
    let html = pages.find(p => p.path === 'index.html')?.html || currentPageData.html || '';

    // Inject CSS if separate file exists
    const cssPage = pages.find(p => p.path === 'style.css' || p.path === 'styles.css');
    if (cssPage && !html.includes('<link') && !html.includes(cssPage.html.substring(0, 50))) {
      html = html.replace('</head>', `<style>\n${cssPage.html}\n</style>\n</head>`);
    }

    // Inject JS if separate file exists
    const jsPage = pages.find(p => p.path === 'script.js' || p.path === 'main.js');
    if (jsPage && !html.includes('<script src') && !html.includes(jsPage.html.substring(0, 50))) {
      html = html.replace('</body>', `<script>\n${jsPage.html}\n</script>\n</body>`);
    }

    return html;
  }, [pages, currentPageData]);

  return (
    <div className="deepsite-page">
      {/* Header */}
      <header className="deepsite-header">
        <div className="header-left">
          <span className="logo">🌐</span>
          <h1>NeXus Website Builder</h1>
          <span className="subtitle">AI-powered website generation</span>
        </div>
        <div className="header-right">
          <span className={`status-badge ${status}`}>
            {status === 'generating' ? '⏳ Generating...' : status === 'ready' ? '● Ready' : '● Error'}
          </span>
        </div>
      </header>

      {/* Main Content - Split View */}
      <main className="deepsite-main">
        {/* Left Panel - Code Editor */}
        <div className="editor-panel">
          {/* File Tabs */}
          <div className="file-tabs">
            {pages.map(page => (
              <button
                key={page.path}
                className={`file-tab ${currentPage === page.path ? 'active' : ''}`}
                onClick={() => setCurrentPage(page.path)}
              >
                {page.path.endsWith('.html') ? '📄' : page.path.endsWith('.css') ? '🎨' : '⚡'}
                {page.path}
              </button>
            ))}
          </div>

          {/* Editor Toolbar */}
          <div className="editor-toolbar">
            <button onClick={copyCode} title="Copy Code">📋 Copy</button>
            <button onClick={downloadFile} title="Download File">⬇️ Download</button>
            <button onClick={downloadAll} title="Download All">📦 Export</button>
          </div>

          {/* Monaco Editor */}
          <div className="monaco-container">
            <Editor
              height="100%"
              language={editorLanguage}
              theme="vs-dark"
              value={currentPageData.html}
              onChange={handleEditorChange}
              onMount={(editor) => { editorRef.current = editor; }}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                wordWrap: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
                readOnly: isGenerating,
                lineNumbers: 'on',
                folding: true,
                bracketPairColorization: { enabled: true }
              }}
              loading={<div className="editor-loading">Loading editor...</div>}
            />
          </div>

          {/* Prompt Input */}
          <form onSubmit={generateWebsite} className="prompt-form">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the website you want to build..."
              disabled={isGenerating}
              className="prompt-input"
            />
            <button
              type="submit"
              disabled={isGenerating || !prompt.trim()}
              className="generate-btn"
            >
              {isGenerating ? '⏳' : '✨'} Generate
            </button>
          </form>
        </div>

        {/* Right Panel - Live Preview */}
        <div className="preview-panel">
          <div className="preview-toolbar">
            <span className="preview-title">Live Preview</span>
            <div className="preview-actions">
              <button onClick={() => previewRef.current?.contentWindow?.location.reload()} title="Refresh">
                🔄
              </button>
            </div>
          </div>
          <div className="preview-container">
            <iframe
              ref={previewRef}
              srcDoc={previewHtml}
              title="Website Preview"
              sandbox="allow-scripts allow-same-origin"
              className="preview-iframe"
            />
          </div>
        </div>
      </main>
    </div>
  );
}
