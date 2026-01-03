import { useState, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './ChatPage.css';
import { API_URL } from '../config/api';

// Agent configuration
const AGENT_CONFIG = {
  chat: {
    name: 'NeXus Chat',
    icon: '💬',
    endpoint: 'general',
    description: 'Conversational AI for general queries'
  },
  cinematic: {
    name: 'Cinematic Generation',
    icon: '🎬',
    endpoint: 'photo',
    description: 'Professional photo and video generation'
  },
  music: {
    name: 'Music Creation',
    icon: '🎵',
    endpoint: 'music',
    description: 'Original music composition'
  },
  code: {
    name: 'Code Development',
    icon: '👨‍💻',
    endpoint: 'code',
    description: 'Full-stack development assistance'
  },
  story: {
    name: 'Story Writing',
    icon: '📖',
    endpoint: 'story',
    description: 'Creative storytelling'
  },
  research: {
    name: 'Web Research',
    icon: '🔍',
    endpoint: 'websearch',
    description: 'Deep web research and analysis'
  },
  website: {
    name: 'Website Builder',
    icon: '🌐',
    endpoint: 'website',
    description: 'Professional website and web app development'
  },
  nft: {
    name: 'NFT Studio',
    icon: '🎨',
    endpoint: 'nft',
    description: 'NFT creation and smart contract deployment'
  },
  smartcontract: {
    name: 'Smart Contract Builder',
    icon: '📜',
    endpoint: 'smartcontract',
    description: 'Solidity smart contract development'
  },
  video: {
    name: 'Video Generation',
    icon: '🎥',
    endpoint: 'video',
    description: 'AI-powered video creation'
  },
  vision: {
    name: 'Vision Analysis',
    icon: '👁️',
    endpoint: 'vision',
    description: 'Image and visual content analysis'
  }
};

export default function AgentChatPage() {
  const { agentId } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [agentStatus, setAgentStatus] = useState('initializing');
  const messagesEndRef = useRef(null);

  const agentConfig = AGENT_CONFIG[agentId];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMessage]);

  // Initialize agent on mount
  useEffect(() => {
    if (!agentConfig) {
      navigate('/');
      return;
    }

    // Check/initialize agent
    initializeAgent();
  }, [agentId]);

  const initializeAgent = async () => {
    try {
      setAgentStatus('initializing');
      const response = await fetch(`${API_URL}/api/agent/init/${agentConfig.endpoint}`, {
        method: 'POST'
      });

      if (response.ok) {
        const data = await response.json();
        setAgentStatus(data.status || 'ready');

        // Add welcome message
        setMessages([{
          role: 'assistant',
          content: `${agentConfig.name} is ready! ${agentConfig.description}. How can I help you today?`
        }]);
      } else {
        setAgentStatus('error');
      }
    } catch (error) {
      console.error('Agent initialization error:', error);
      setAgentStatus('error');
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading || agentStatus !== 'ready') return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsLoading(true);
    setStreamingMessage('');

    try {
      const response = await fetch(`${API_URL}/api/agent/chat/${agentConfig.endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });

      if (!response.ok) throw new Error('Failed to connect to agent');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullText = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);

            if (data === '[DONE]') {
              setMessages(prev => [...prev, {
                role: 'assistant',
                content: fullText
              }]);
              setStreamingMessage('');
              break;
            }

            try {
              const parsed = JSON.parse(data);

              if (parsed.done) {
                setMessages(prev => [...prev, {
                  role: 'assistant',
                  content: fullText
                }]);
                setStreamingMessage('');
                break;
              }

              if (parsed.type === 'text' && parsed.content) {
                fullText += parsed.content;
                setStreamingMessage(fullText);
              } else if (parsed.error) {
                setMessages(prev => [...prev, {
                  role: 'assistant',
                  content: `Error: ${parsed.error}`,
                  isError: true
                }]);
                break;
              }
            } catch (e) {
              console.error('Failed to parse SSE data:', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Agent chat error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Sorry, I'm having trouble connecting. Please ensure the ${agentConfig.name} is initialized.`,
        isError: true
      }]);
    } finally {
      setIsLoading(false);
      setStreamingMessage('');
    }
  };

  if (!agentConfig) {
    return <div className="chat-page">Agent not found</div>;
  }

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="chat-header">
          <h2>
            <span className="agent-icon-large">{agentConfig.icon}</span>
            {agentConfig.name}
          </h2>
          <p>{agentConfig.description}</p>
          <div className="agent-status-indicator">
            <span className={`status-dot ${agentStatus}`}></span>
            {agentStatus === 'initializing' && 'Initializing...'}
            {agentStatus === 'ready' && 'Ready'}
            {agentStatus === 'error' && 'Error - Please refresh'}
          </div>
        </div>

        <div className="messages-area">
          {messages.length === 0 && !isLoading && agentStatus === 'ready' && (
            <div className="empty-state">
              <h3>Welcome to {agentConfig.name}</h3>
              <p>{agentConfig.description}</p>
              <p>Start a conversation by typing a message below</p>
            </div>
          )}

          {agentStatus === 'initializing' && messages.length === 0 && (
            <div className="empty-state">
              <div className="loading-spinner">⚙️</div>
              <h3>Initializing {agentConfig.name}...</h3>
              <p>Loading AI models and preparing the agent</p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role} ${msg.isError ? 'error' : ''}`}>
              <div className="message-avatar">
                {msg.role === 'user' ? '👤' : agentConfig.icon}
              </div>
              <div className="message-content">
                <div className="message-header">
                  {msg.role === 'user' ? 'You' : agentConfig.name}
                </div>
                <div className="message-text">{msg.content}</div>
              </div>
            </div>
          ))}

          {streamingMessage && (
            <div className="message assistant streaming">
              <div className="message-avatar">{agentConfig.icon}</div>
              <div className="message-content">
                <div className="message-header">{agentConfig.name}</div>
                <div className="message-text">{streamingMessage}<span className="cursor">|</span></div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendMessage} className="chat-input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Message ${agentConfig.name}...`}
            disabled={isLoading || agentStatus !== 'ready'}
            className="chat-input"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim() || agentStatus !== 'ready'}
            className="send-button"
          >
            {isLoading ? '⏳' : '➤'}
          </button>
        </form>
      </div>
    </div>
  );
}
