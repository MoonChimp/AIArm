import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import './SphereHome.css'

export default function SphereHome({ onNavigate }) {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 20 - 10,
        y: (e.clientY / window.innerHeight) * 20 - 10
      })
    }

    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  return (
    <div className="sphere-home">
      {/* Central Sphere */}
      <motion.div
        className="central-sphere"
        animate={{
          rotateY: mousePosition.x,
          rotateX: -mousePosition.y
        }}
        transition={{ type: 'spring', stiffness: 50, damping: 20 }}
      >
        <div className="sphere-inner">
          <div className="sphere-glow"></div>
          <div className="sphere-ring ring-1"></div>
          <div className="sphere-ring ring-2"></div>
          <div className="sphere-ring ring-3"></div>

          <div className="sphere-core">
            <span className="core-text">NEXUS</span>
          </div>
        </div>
      </motion.div>

      {/* Floating Action Cards */}
      <div className="action-cards">
        <ActionCard
          icon="💬"
          title="Chat"
          subtitle="Start a conversation with Nexus AI"
          position="left"
          onClick={() => onNavigate('chat')}
        />

        <ActionCard
          icon="📊"
          title="Monitor"
          subtitle="System performance and stats"
          position="top"
          onClick={() => onNavigate('monitor')}
        />

        <ActionCard
          icon="🧠"
          title="Mind"
          subtitle="Inner Life thought stream"
          position="right"
          onClick={() => onNavigate('mind')}
        />

        <ActionCard
          icon="⚡"
          title="Quick Actions"
          subtitle="Execute commands and tasks"
          position="bottom"
          onClick={() => onNavigate('chat')}
        />
      </div>

      {/* Particle Effect */}
      <div className="particles">
        {[...Array(50)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${5 + Math.random() * 10}s`
            }}
          />
        ))}
      </div>
    </div>
  )
}

function ActionCard({ icon, title, subtitle, position, onClick }) {
  return (
    <motion.div
      className={`action-card action-${position}`}
      whileHover={{ scale: 1.05, y: -5 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
    >
      <div className="card-icon">{icon}</div>
      <h3 className="card-title">{title}</h3>
      <p className="card-subtitle">{subtitle}</p>
    </motion.div>
  )
}
