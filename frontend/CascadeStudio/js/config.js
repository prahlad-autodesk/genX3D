// Configuration for CascadeStudio frontend
const config = {
  // API base URL - change this based on environment
  API_BASE_URL: window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://prahlad.blog',
  
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
const getApiUrl = (endpoint) => {
  return `${config.API_BASE_URL}${endpoint}`;
};

// Helper function to get model URL
const getModelUrl = (modelPath) => {
  if (modelPath.startsWith('http')) {
    return modelPath; // Already a full URL
  }
  return `${config.API_BASE_URL}${modelPath}`;
};

// Make config available globally
window.genx3dConfig = config;
window.getApiUrl = getApiUrl;
window.getModelUrl = getModelUrl;
