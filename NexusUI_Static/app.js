const { useState, useEffect } = React;

const API_BASE = 'http://localhost:5000';

function SphereHome({ onNavigate }) {
  return (
    <div className="sphere-home">
      <div className="central-sphere">
        <div className="sphere-inner">
          <div className="sphere-core">
            <span className="core-text">NEXUS</span>
          </div>
        </div>
      </div>

      <div className="action-cards">
        <div className="action-card" onClick={() => onNavigate('chat')}>
          <div className="icon">💬</div>
          <h3>Chat</h3>
          <p>Converse with Nexus AI</p>
        </div>

        <div className="action-card" onClick={() => onNavigate('monitor')}>
          <div className="icon">📊</div>
          <h3>System Monitor</h3>
          <p>View system metrics</p>
        </div>

        <div className="action-card" onClick={() => onNavigate('mind')}>
          <div className="icon">🧠</div>
          <h3>Mind View</h3>
          <p>Explore AI consciousness</p>
        </div>

        <div className="action-card">
          <div className="icon">⚡</div>
          <h3>Quick Actions</h3>
          <p>Common commands</p>
        </div>
      </div>
    </div>
  );
}

function ChatInterface() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am Nexus. Select an agent below or chat with me directly.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const messagesEndRef = React.useRef(null);

  const agents = [
    { id: 'chat', name: 'Nexus', icon: '💬', color: '#7c3aed' },
    { id: 'code', name: 'Code', icon: '💻', color: '#10b981' },
    { id: 'music', name: 'Music', icon: '🎵', color: '#f59e0b' },
    { id: 'photo', name: 'Photo', icon: '📸', color: '#ec4899' },
    { id: 'story', name: 'Story', icon: '📖', color: '#8b5cf6' },
    { id: 'video', name: 'Video', icon: '🎬', color: '#3b82f6' },
    { id: 'websearch', name: 'Search', icon: '🔍', color: '#14b8a6' }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (agentOverride = null) => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    const targetAgent = agentOverride || selectedAgent;

    setInput('');
    setMessages(prev => [...prev, {
      role: 'user',
      content: userMessage,
      agent: targetAgent
    }]);
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/api/chat`, {
        message: userMessage,
        agent: targetAgent
      });
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.response,
        agent: targetAgent
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Error: Unable to connect to Nexus backend.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleAgentClick = (agentId) => {
    setSelectedAgent(agentId);
    setMessages(prev => [...prev, {
      role: 'system',
      content: `Switched to ${agents.find(a => a.id === agentId).name} agent`
    }]);
  };

  return (
    <div className="chat-interface">
      <div className="agent-selector">
        {agents.map(agent => (
          <button
            key={agent.id}
            className={`agent-button ${selectedAgent === agent.id ? 'active' : ''}`}
            onClick={() => handleAgentClick(agent.id)}
            style={{
              '--agent-color': agent.color
            }}
          >
            <span className="agent-icon">{agent.icon}</span>
            <span className="agent-name">{agent.name}</span>
          </button>
        ))}
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-label">
              {msg.role === 'user' ? 'You' : msg.role === 'system' ? 'System' :
               agents.find(a => a.id === msg.agent)?.name || 'Nexus'}
            </div>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          placeholder={`Message ${selectedAgent ? agents.find(a => a.id === selectedAgent)?.name : 'Nexus'}...`}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button
          className="send-button"
          onClick={() => sendMessage()}
          disabled={loading}
        >
          {loading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}

function SystemMonitor() {
  const [systemData, setSystemData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSystemData = async () => {
      try {
        const response = await axios.get(`${API_BASE}/api/system`);
        setSystemData(response.data);
        setLoading(false);
      } catch (error) {
        setLoading(false);
      }
    };

    fetchSystemData();
    const interval = setInterval(fetchSystemData, 2000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="system-monitor">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="system-monitor">
      <h2 className="monitor-title">System Monitor</h2>

      <div className="monitor-grid">
        <div className="stat-card">
          <div className="stat-icon">🖥️</div>
          <div className="stat-content">
            <h3>CPU Usage</h3>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${systemData?.cpu || 0}%`,
                  backgroundColor: (systemData?.cpu || 0) > 80 ? '#ec4899' : '#7c3aed'
                }}
              />
            </div>
            <p className="stat-value">{systemData?.cpu?.toFixed(1) || 0}%</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💾</div>
          <div className="stat-content">
            <h3>Memory Usage</h3>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${systemData?.memory || 0}%`,
                  backgroundColor: (systemData?.memory || 0) > 80 ? '#ec4899' : '#7c3aed'
                }}
              />
            </div>
            <p className="stat-value">{systemData?.memory?.toFixed(1) || 0}%</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🌐</div>
          <div className="stat-content">
            <h3>Platform</h3>
            <p className="stat-value">{systemData?.platform || 'Unknown'}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🤖</div>
          <div className="stat-content">
            <h3>Nexus Status</h3>
            <div className={`status-indicator ${systemData?.nexus_online ? 'online' : 'offline'}`}>
              {systemData?.nexus_online ? 'Online' : 'Offline'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function MindView() {
  return (
    <div style={{ padding: '2rem', color: '#fff' }}>
      <h2>Mind View</h2>
      <p>AI consciousness visualization coming soon...</p>
    </div>
  );
}

function Settings() {
  return (
    <div style={{ padding: '2rem', color: '#fff' }}>
      <h2>Settings</h2>
      <p>Configuration options coming soon...</p>
    </div>
  );
}

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [nexusOnline, setNexusOnline] = useState(false);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await axios.get(`${API_BASE}/api/status`);
        setNexusOnline(response.data.status === 'online');
      } catch (error) {
        setNexusOnline(false);
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const views = {
    home: <SphereHome onNavigate={setCurrentView} />,
    chat: <ChatInterface />,
    monitor: <SystemMonitor />,
    mind: <MindView />,
    settings: <Settings />
  };

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <span className={`status-dot ${nexusOnline ? 'online' : 'offline'}`}></span>
          <span>Nexus {nexusOnline ? 'Online' : 'Offline'}</span>
        </div>
        <div>{new Date().toLocaleTimeString()}</div>
      </header>

      <main className="app-main">
        {views[currentView]}
      </main>

      <nav className="bottom-nav">
        <button
          className={`nav-button ${currentView === 'home' ? 'active' : ''}`}
          onClick={() => setCurrentView('home')}
        >
          Home
        </button>
        <button
          className={`nav-button ${currentView === 'chat' ? 'active' : ''}`}
          onClick={() => setCurrentView('chat')}
        >
          Chat
        </button>
        <button
          className={`nav-button ${currentView === 'monitor' ? 'active' : ''}`}
          onClick={() => setCurrentView('monitor')}
        >
          Monitor
        </button>
        <button
          className={`nav-button ${currentView === 'mind' ? 'active' : ''}`}
          onClick={() => setCurrentView('mind')}
        >
          Mind
        </button>
        <button
          className={`nav-button ${currentView === 'settings' ? 'active' : ''}`}
          onClick={() => setCurrentView('settings')}
        >
          Settings
        </button>
      </nav>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
