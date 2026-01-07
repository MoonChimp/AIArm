// NeXus AGI API Configuration
// Supports both local development and remote access via ngrok

// Check for custom API URL in localStorage (for remote access)
const getStoredApiUrl = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('nexus_api_url');
  }
  return null;
};

// Lambda server URL (public IP)
const LAMBDA_URL = 'http://129.213.16.11';

// Main NeXus Flask API (orchestrator, chat, agents)
// Uses stored URL if available, otherwise defaults to Lambda server
export const API_URL = getStoredApiUrl() || `${LAMBDA_URL}:5001`;

// Individual service URLs
// All services run on Lambda server with different ports
const baseUrl = getStoredApiUrl() || LAMBDA_URL;
export const FLUX_API = `${baseUrl}:8000`;  // Lambda GPU Manager handles FLUX
export const VIDEO_API = `${baseUrl}:8000/cogvideo`;  // Lambda GPU Manager handles video
export const DEEPSITE_API = `${baseUrl}:5001/api`;  // Through main API
export const CONTRACT_BUILDER_API = `${baseUrl}:5001/api`;  // Through main API
export const OLLAMA_API = 'http://localhost:11434';    // Ollama (local only, not exposed remotely)

// For backward compatibility
export const API_BASE = API_URL;

// Helper function to set remote API URL
export const setRemoteApiUrl = (url) => {
  if (typeof window !== 'undefined') {
    if (url) {
      localStorage.setItem('nexus_api_url', url);
    } else {
      localStorage.removeItem('nexus_api_url');
    }
    // Reload to apply new URL
    window.location.reload();
  }
};

// Helper function to check if using remote
export const isRemoteMode = () => {
  return getStoredApiUrl() !== null;
};

// Helper to get current API URL
export const getCurrentApiUrl = () => API_URL;

export default {
  API_URL,
  API_BASE,
  FLUX_API,
  VIDEO_API,
  DEEPSITE_API,
  CONTRACT_BUILDER_API,
  OLLAMA_API,
  setRemoteApiUrl,
  isRemoteMode,
  getCurrentApiUrl
};
