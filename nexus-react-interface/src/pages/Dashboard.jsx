import { Link } from 'react-router-dom';
import nexusLogo from '../assets/images/nexus-logo.png';
import './Dashboard.css';

export default function Dashboard() {
  const agents = [
    {
      id: 'chat',
      name: 'NeXus Chat',
      description: 'Intelligent conversational AI for queries, analysis, and assistance',
      status: 'online',
      icon: '💬',
      path: '/chat',
      external: false,
      capabilities: ['Natural Language', 'Code Assistance', 'Research']
    },
    {
      id: 'image-gen',
      name: 'NeXus Image Gen',
      description: 'High-quality AI image generation from text descriptions',
      status: 'online',
      icon: '🎨',
      path: '/image-gen',
      external: false,
      capabilities: ['Text-to-Image', 'Style Transfer', 'HD Output']
    },
    {
      id: 'video-gen',
      name: 'NeXus Video Gen',
      description: 'AI-powered video creation from text prompts',
      status: 'online',
      icon: '🎬',
      path: '/video-gen',
      external: false,
      capabilities: ['Text-to-Video', 'Cinematic', 'Animation']
    },
    {
      id: 'music',
      name: 'NeXus Music Gen',
      description: 'Generate original music compositions and soundtracks',
      status: 'online',
      icon: '🎵',
      path: '/music',
      external: false,
      capabilities: ['Composition', 'Soundtracks', 'Audio Effects']
    },
    {
      id: 'website',
      name: 'NeXus Website Builder',
      description: 'AI-powered website generation and development',
      status: 'online',
      icon: '🌐',
      path: '/deepsite',
      external: false,
      capabilities: ['Full Stack', 'Responsive', 'Modern UI']
    },
    {
      id: 'crypto',
      name: 'NeXus Crypto Agency',
      description: 'Token deployment, NFT studio, and blockchain solutions',
      status: 'online',
      icon: '🔗',
      path: '/agent/trading',
      external: false,
      capabilities: ['Token Launch', 'NFT Studio', 'Smart Contracts']
    },
    {
      id: 'finance',
      name: 'NeXus Financial Analytics',
      description: 'Market analysis, predictions, and trading intelligence',
      status: 'online',
      icon: '📈',
      path: '/finance',
      external: false,
      capabilities: ['Market Analysis', 'Predictions', 'Signals']
    },
    {
      id: 'contracts',
      name: 'NeXus Smart Contract Builder',
      description: 'Automated smart contract generation for Solana & EVM',
      status: 'online',
      icon: '📜',
      path: '/agent/contracts',
      external: false,
      capabilities: ['Solidity', 'Rust/Anchor', 'Auditing']
    },
    {
      id: 'coder',
      name: 'NeXus Coder',
      description: 'Full-stack development, debugging, and code generation',
      status: 'online',
      icon: '💻',
      path: '/agent/code',
      external: false,
      capabilities: ['Full Stack', 'Debugging', 'Architecture']
    },
    {
      id: 'research',
      name: 'NeXus DeepWeb Search',
      description: 'Advanced web research, data gathering, and analysis',
      status: 'online',
      icon: '🔍',
      path: '/agent/research',
      external: false,
      capabilities: ['Deep Search', 'Data Mining', 'Analysis']
    },
    {
      id: 'intelligence',
      name: 'NeXus Intelligence',
      description: 'Shared system control with security-first design',
      status: 'online',
      icon: '🧠',
      path: '/intelligence',
      external: false,
      capabilities: ['File Operations', 'Commands', 'Git', 'Secure Access']
    }
  ];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <img src={nexusLogo} alt="NeXus AI" className="dashboard-logo" />
        <h1>NeXus AI Platform</h1>
        <p>Autonomous Multi-Agent Intelligence System</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🤖</div>
          <div className="stat-content">
            <h3>{agents.filter(a => a.status === 'online').length}</h3>
            <p>Active Agents</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-content">
            <h3>Online</h3>
            <p>System Status</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>{agents.reduce((sum, agent) => sum + (agent.capabilities?.length || 0), 0)}</h3>
            <p>Capabilities</p>
          </div>
        </div>
      </div>

      <div className="agents-section">
        <h2>NeXus Agents</h2>
        <div className="agents-grid">
          {agents.map(agent => (
            <Link
              key={agent.id}
              to={agent.path}
              className={`agent-card ${agent.status}`}
            >
              <div className="agent-icon">{agent.icon}</div>
              <h3>{agent.name}</h3>
              <p>{agent.description}</p>
              {agent.capabilities && (
                <div className="agent-capabilities">
                  {agent.capabilities.map((cap, idx) => (
                    <span key={idx} className="capability-badge">{cap}</span>
                  ))}
                </div>
              )}
              <div className="agent-status">
                <span className={`status-badge ${agent.status}`}>
                  {agent.status === 'online' ? 'Online' : 'Coming Soon'}
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
