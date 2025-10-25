import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import './SystemMonitor.css'

export default function SystemMonitor() {
  const [systemData, setSystemData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchSystemData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/system')
        setSystemData(response.data)
        setLoading(false)
      } catch (err) {
        setError('Failed to fetch system data')
        setLoading(false)
      }
    }

    fetchSystemData()
    const interval = setInterval(fetchSystemData, 2000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="system-monitor">
        <div className="loading-spinner"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="system-monitor">
        <div className="error-message">{error}</div>
      </div>
    )
  }

  return (
    <div className="system-monitor">
      <h2 className="monitor-title">System Monitor</h2>

      <div className="monitor-grid">
        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="stat-icon">🖥️</div>
          <div className="stat-content">
            <h3>CPU Usage</h3>
            <div className="progress-bar">
              <motion.div
                className="progress-fill"
                initial={{ width: 0 }}
                animate={{ width: `${systemData?.cpu || 0}%` }}
                style={{
                  backgroundColor: systemData?.cpu > 80 ? '#ec4899' : '#7c3aed'
                }}
              />
            </div>
            <p className="stat-value">{systemData?.cpu?.toFixed(1) || 0}%</p>
          </div>
        </motion.div>

        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="stat-icon">💾</div>
          <div className="stat-content">
            <h3>Memory Usage</h3>
            <div className="progress-bar">
              <motion.div
                className="progress-fill"
                initial={{ width: 0 }}
                animate={{ width: `${systemData?.memory || 0}%` }}
                style={{
                  backgroundColor: systemData?.memory > 80 ? '#ec4899' : '#7c3aed'
                }}
              />
            </div>
            <p className="stat-value">{systemData?.memory?.toFixed(1) || 0}%</p>
          </div>
        </motion.div>

        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="stat-icon">🌐</div>
          <div className="stat-content">
            <h3>Platform</h3>
            <p className="stat-value">{systemData?.platform || 'Unknown'}</p>
          </div>
        </motion.div>

        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div className="stat-icon">🤖</div>
          <div className="stat-content">
            <h3>Nexus Status</h3>
            <div className={`status-indicator ${systemData?.nexus_online ? 'online' : 'offline'}`}>
              {systemData?.nexus_online ? 'Online' : 'Offline'}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
