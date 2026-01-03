import { Link } from 'react-router-dom';
import './AgentsPage.css';

// All available agents
const AGENTS = [
  { id: 'chat', name: 'NeXus Chat', icon: '💬', description: 'Conversational AI for general queries' },
  { id: 'code', name: 'Code Development', icon: '👨‍💻', description: 'Full-stack development assistance' },
  { id: 'website', name: 'Website Builder', icon: '🌐', description: 'Professional website and web app development' },
  { id: 'cinematic', name: 'Cinematic Generation', icon: '🎬', description: 'Professional photo generation' },
  { id: 'video', name: 'Video Generation', icon: '🎥', description: 'AI-powered video creation' },
  { id: 'music', name: 'Music Creation', icon: '🎵', description: 'Original music composition' },
  { id: 'story', name: 'Story Writing', icon: '📖', description: 'Creative storytelling' },
  { id: 'research', name: 'Web Research', icon: '🔍', description: 'Deep web research and analysis' },
  { id: 'smartcontract', name: 'Smart Contract Builder', icon: '📜', description: 'Solidity smart contract development' },
  { id: 'nft', name: 'NFT Studio', icon: '🎨', description: 'NFT creation and deployment' },
  { id: 'vision', name: 'Vision Analysis', icon: '👁️', description: 'Image and visual content analysis' },
];

export default function AgentsPage() {
  return (
    <div className="agents-page">
      <div className="agents-header">
        <h1>NeXus Agents</h1>
        <p>Select an AI agent to start a conversation</p>
      </div>

      <div className="agents-grid">
        {AGENTS.map((agent) => (
          <Link key={agent.id} to={`/agent/${agent.id}`} className="agent-card">
            <div className="agent-icon">{agent.icon}</div>
            <h3>{agent.name}</h3>
            <p>{agent.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
