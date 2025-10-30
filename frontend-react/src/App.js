import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import styled from 'styled-components';
import CADViewer from './components/CADViewer';
import ChatAssistant from './components/ChatAssistant';
import Toolbar from './components/Toolbar';
import Sidebar from './components/Sidebar';
import './App.css';

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  background: #1a1a1a;
  color: #ffffff;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
`;

const ViewerContainer = styled.div`
  flex: 1;
  position: relative;
  background: #0a0a0a;
`;

function App() {
  return (
    <Router>
      <AppContainer>
        <Sidebar />
        <MainContent>
          <Toolbar />
          <ViewerContainer>
            <CADViewer />
          </ViewerContainer>
          <ChatAssistant />
        </MainContent>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#333',
              color: '#fff',
              border: '1px solid #555',
            },
          }}
        />
      </AppContainer>
    </Router>
  );
}

export default App; 