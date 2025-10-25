import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import './ChatInterface.css'

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Welcome to Nexus AI. I\'m your intelligent personal assistant. Ask me anything or try one of these:',
      suggestions: [
        'What can you help me with today?',
        'Tell me about your capabilities',
        'Create a task for me',
        'Show me system status'
      ]
    }
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (messageText) => {
    const userMessage = messageText || input
    if (!userMessage.trim()) return

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setInput('')
    setIsTyping(true)

    try {
      // Call Nexus Actionable backend
      const response = await axios.post('http://localhost:5000/api/chat', {
        message: userMessage
      })

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.response || 'I processed your request.'
      }])
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'I\'m having trouble connecting to my backend. Please make sure the Nexus server is running.'
      }])
    } finally {
      setIsTyping(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        <AnimatePresence>
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className={`message message-${message.role}`}
            >
              <div className="message-avatar">
                {message.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                <p>{message.content}</p>
                {message.suggestions && (
                  <div className="message-suggestions">
                    {message.suggestions.map((suggestion, i) => (
                      <button
                        key={i}
                        className="suggestion-button"
                        onClick={() => sendMessage(suggestion)}
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="message message-assistant"
          >
            <div className="message-avatar">🤖</div>
            <div className="message-content typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Message Nexus AI..."
            rows="1"
          />
          <button
            className="send-button"
            onClick={() => sendMessage()}
            disabled={!input.trim()}
          >
            <span>▶</span>
          </button>
        </div>
      </div>
    </div>
  )
}
