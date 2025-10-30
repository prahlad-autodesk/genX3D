// Configuration for different environments
const config = {
  // API base URL - automatically detect environment
  API_BASE_URL: window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://prahlad.blog',
  
  // WebSocket URL (if needed)
  WS_BASE_URL: window.location.hostname === 'localhost'
    ? 'ws://localhost:8000'
    : 'wss://prahlad.blog',
  
  // Environment detection
  isDevelopment: window.location.hostname === 'localhost',
  isProduction: window.location.hostname !== 'localhost',
  
  // API endpoints
  endpoints: {
    chat: '/graph_chat',
    health: '/health',
    apiInfo: '/api/info',
    models: '/list_generated_models',
    cleanupStats: '/cleanup/stats',
    cleanupManual: '/cleanup/manual'
  }
};

// Helper function to get full API URL
export const getApiUrl = (endpoint) => {
  return `${config.API_BASE_URL}${endpoint}`;
};

// Helper function to get model URL
export const getModelUrl = (modelPath) => {
  if (modelPath.startsWith('http')) {
    return modelPath; // Already a full URL
  }
  return `${config.API_BASE_URL}${modelPath}`;
};

export default config;
