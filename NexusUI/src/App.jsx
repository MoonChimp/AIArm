import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'
import SphereHome from './components/SphereHome'
import ChatInterface from './components/ChatInterface'
import SystemMonitor from './components/SystemMonitor'
import MindView from './components/MindView'
import Settings from './components/Settings'

function App() {
  const [currentView, setCurrentView] = useState('home')
  const [nexusOnline, setNexusOnline] = useState(false)
  const [currentTime, setCurrentTime] = useState(new Date())

  useEffect(() => {
    // Check if Nexus backend is online
    const checkNexusStatus = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/status')
        setNexusOnline(response.ok)
      } catch (error) {
        setNexusOnline(false)
      }
    }

    checkNexusStatus()
    const interval = setInterval(checkNexusStatus, 10000)

    // Update time
    const timeInterval = setInterval(() => setCurrentTime(new Date()), 1000)

    return () => {
      clearInterval(interval)
      clearInterval(timeInterval)
    }
  }, [])

  const views = {
    home: <SphereHome onNavigate={setCurrentView} />,
    chat: <ChatInterface />,
    monitor: <SystemMonitor />,
    mind: <MindView />,
    settings: <Settings />
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <div className="nexus-logo">
            <span className="logo-n">N</span>
          </div>
          <h1>NEXUS AI</h1>
        </div>

        <div className="header-center">
          <span className="time">{currentTime.toLocaleTimeString()}</span>
          <span className="date">
            {currentTime.toLocaleDateString('en-US', {
              weekday: 'long',
              month: 'long',
              day: 'numeric'
            })}
          </span>
        </div>

        <div className="header-right">
          <div className={`status-indicator ${nexusOnline ? 'online' : 'offline'}`}>
            <span className="status-dot"></span>
            <span className="status-text">
              {nexusOnline ? 'Nexus AI Online' : 'Offline'}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentView}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.3 }}
            className="view-container"
          >
            {views[currentView]}
          </motion.div>
        </AnimatePresence>
      </main>

      {/* Bottom Navigation */}
      <nav className="bottom-nav">
        <NavButton
          icon="🏠"
          label="Home"
          active={currentView === 'home'}
          onClick={() => setCurrentView('home')}
        />
        <NavButton
          icon="💬"
          label="Chat"
          active={currentView === 'chat'}
          onClick={() => setCurrentView('chat')}
        />
        <NavButton
          icon="🎯"
          label="Control"
          active={currentView === 'control'}
          onClick={() => setCurrentView('home')}
          special
        />
        <NavButton
          icon="🧠"
          label="Mind"
          active={currentView === 'mind'}
          onClick={() => setCurrentView('mind')}
        />
        <NavButton
          icon="⚙️"
          label="Settings"
          active={currentView === 'settings'}
          onClick={() => setCurrentView('settings')}
        />
      </nav>
    </div>
  )
}

function NavButton({ icon, label, active, onClick, special }) {
  return (
    <motion.button
      className={`nav-button ${active ? 'active' : ''} ${special ? 'special' : ''}`}
      onClick={onClick}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
    >
      <span className="nav-icon">{icon}</span>
      <span className="nav-label">{label}</span>
    </motion.button>
  )
}

export default App
