# genx3D React Frontend

A modern React-based frontend for the genx3D AI-powered CAD modeling application, built with Three.js and React Three Fiber.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation
```bash
cd frontend-react
npm install
```

### Development
```bash
npm start
```
The app will open at [http://localhost:3000](http://localhost:3000)

### Production Build
```bash
npm run build
```

## 🏗️ Architecture

### Core Technologies
- **React 18.2.0** - UI framework
- **Three.js 0.129.0** - 3D graphics library (same version as original Cascade Studio)
- **React Three Fiber 6.0.13** - React renderer for Three.js
- **React Three Drei 6.1.3** - Useful helpers for React Three Fiber
- **Styled Components 6.1.1** - CSS-in-JS styling
- **Axios 1.6.2** - HTTP client for API communication

### Additional Libraries (from original Cascade Studio)
- **Tweakpane 3.0.5** - UI controls library
- **Golden Layout 1.5.9** - Advanced layout management
- **jQuery 3.5.1** - DOM manipulation
- **Monaco Editor 0.20.0** - Code editor (for future use)

## 📁 Project Structure

```
frontend-react/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── App.js              # Main application component
│   │   ├── CADViewer.js        # 3D model viewer
│   │   ├── ChatAssistant.js    # AI chat interface
│   │   ├── Sidebar.js          # Model explorer & properties
│   │   └── Toolbar.js          # CAD tools & controls
│   ├── App.css                 # Global styles
│   └── index.js                # Application entry point
├── package.json
└── README.md
```

## 🎯 Features

### ✅ Implemented
- **3D Viewer**: Interactive 3D scene with Three.js
- **Camera Controls**: Orbit controls for model navigation
- **Primitive Shapes**: Box, Sphere, Cylinder rendering
- **Chat Interface**: AI assistant communication
- **Responsive Design**: Mobile-friendly layout
- **Modern UI**: Clean, professional interface

### 🚧 In Development
- **STL/GLTF Loading**: Model file import
- **File Upload**: Direct model upload
- **Advanced Controls**: Tweakpane integration
- **Code Editor**: Monaco editor integration
- **Layout Management**: Golden Layout integration

## 🔧 Configuration

### Backend Connection
The frontend is configured to connect to the backend at `http://localhost:8000`. Update the proxy in `package.json` if needed:

```json
{
  "proxy": "http://localhost:8000"
}
```

### Environment Variables
Create a `.env` file for environment-specific configuration:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

## 🎨 Customization

### Styling
The app uses Styled Components for styling. Main theme colors and styles can be modified in individual component files.

### 3D Scene
The 3D scene configuration is in `CADViewer.js`. You can customize:
- Lighting setup
- Grid appearance
- Camera controls
- Model rendering

### Chat Interface
The chat interface in `ChatAssistant.js` handles:
- Message display
- API communication
- Model loading events

## 🧪 Testing

```bash
npm test
```

## 📦 Build & Deploy

### Production Build
```bash
npm run build
```

### Docker Deployment
The frontend is included in the main Dockerfile and will be built automatically.

## 🔗 Integration

### Backend API
The frontend communicates with the backend through:
- `/graph_chat` - AI chat endpoint
- `/temp_models/{filename}` - Model file serving
- `/api/info` - System information
- `/health` - Health check

### Model Loading
Models are loaded through custom events:
```javascript
// Dispatch model load event
window.dispatchEvent(new CustomEvent('loadModel', {
  detail: { url: '/temp_models/model.step', type: 'step' }
}));
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   lsof -ti:3000 | xargs kill -9
   ```

2. **Build Errors**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Backend Connection Issues**
   - Ensure backend is running on port 8000
   - Check CORS configuration
   - Verify proxy settings

### Development Tips

- Use React Developer Tools for debugging
- Check browser console for Three.js warnings
- Monitor network tab for API calls
- Use React Three Fiber's built-in debugging

## 📚 Resources

- [React Three Fiber Documentation](https://docs.pmnd.rs/react-three-fiber)
- [Three.js Documentation](https://threejs.org/docs/)
- [Styled Components Documentation](https://styled-components.com/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the genx3D application and follows the same license terms. 