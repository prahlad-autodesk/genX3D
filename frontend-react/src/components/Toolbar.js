import React, { useState } from 'react';
import styled from 'styled-components';
import {
  Box,
  Circle,
  RotateCcw,
  ZoomIn,
  ZoomOut,
  Grid,
  Settings,
  Download,
  Upload,
  Eye,
  Maximize
} from 'lucide-react';

const ToolbarContainer = styled.div`
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 10;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
`;

const ToolButton = styled.button`
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 4px;
  padding: 8px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  width: 36px;
  height: 36px;

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.05);
  }

  &:active {
    transform: scale(0.95);
  }

  &.active {
    background: rgba(76, 175, 80, 0.3);
    border: 1px solid rgba(76, 175, 80, 0.5);
  }
`;

const ViewDropdown = styled.div`
  position: relative;
  display: inline-block;
`;

const DropdownContent = styled.div`
  position: absolute;
  top: 100%;
  left: 0;
  background: rgba(0, 0, 0, 0.9);
  border-radius: 4px;
  padding: 4px;
  display: ${props => props.isOpen ? 'block' : 'none'};
  min-width: 120px;
  z-index: 1000;
  border: 1px solid rgba(255, 255, 255, 0.1);
`;

const DropdownItem = styled.button`
  background: none;
  border: none;
  color: white;
  padding: 8px 12px;
  width: 100%;
  text-align: left;
  cursor: pointer;
  border-radius: 2px;
  font-size: 12px;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
`;

const Toolbar = () => {
  const [viewDropdownOpen, setViewDropdownOpen] = useState(false);
  const [activeView, setActiveView] = useState('iso');

  const handleZoomIn = () => {
    if (window.controlsRef && window.controlsRef.current) {
      const controls = window.controlsRef.current;
      const camera = controls.object;
      const target = controls.target;
      
      // Zoom in by moving camera closer to target
      const direction = camera.position.clone().sub(target).normalize();
      const distance = camera.position.distanceTo(target);
      const newDistance = Math.max(0.1, distance * 0.8); // Zoom in by 20%
      
      camera.position.copy(target).add(direction.multiplyScalar(newDistance));
      controls.update();
      console.log('Zoomed in, new distance:', newDistance);
    } else {
      console.log('Controls not available for zoom');
    }
  };

  const handleZoomOut = () => {
    if (window.controlsRef && window.controlsRef.current) {
      const controls = window.controlsRef.current;
      const camera = controls.object;
      const target = controls.target;
      
      // Zoom out by moving camera away from target
      const direction = camera.position.clone().sub(target).normalize();
      const distance = camera.position.distanceTo(target);
      const newDistance = distance * 1.25; // Zoom out by 25%
      
      camera.position.copy(target).add(direction.multiplyScalar(newDistance));
      controls.update();
      console.log('Zoomed out, new distance:', newDistance);
    } else {
      console.log('Controls not available for zoom');
    }
  };

  const handleFitToView = () => {
    if (window.fitToView && typeof window.fitToView === 'function') {
      console.log('Calling fitToView');
      window.fitToView();
    } else {
      console.log('fitToView function not available');
    }
  };

  const handleSetView = (view) => {
    if (window.setView && typeof window.setView === 'function') {
      console.log('Setting view to:', view);
      window.setView(view);
      setActiveView(view);
      setViewDropdownOpen(false);
    } else {
      console.log('setView function not available');
    }
  };

  const handleBox = () => {
    console.log('Box tool selected');
  };

  const handleCircle = () => {
    console.log('Circle tool selected');
  };

  const handleRotate = () => {
    console.log('Rotate tool selected');
  };

  const handleGrid = () => {
    console.log('Grid toggle');
  };

  const handleSettings = () => {
    console.log('Settings opened');
  };

  const handleDownload = () => {
    console.log('Download model');
  };

  const handleUpload = () => {
    console.log('Upload model');
  };

  return (
    <ToolbarContainer>
      {/* View Controls */}
      <ViewDropdown>
        <ToolButton
          onClick={() => setViewDropdownOpen(!viewDropdownOpen)}
          className={viewDropdownOpen ? 'active' : ''}
          title="View Presets"
        >
          <Eye size={16} />
        </ToolButton>
        <DropdownContent isOpen={viewDropdownOpen}>
          <DropdownItem onClick={() => handleSetView('iso')}>
            {activeView === 'iso' ? '✓ ' : ''}Isometric
          </DropdownItem>
          <DropdownItem onClick={() => handleSetView('top')}>
            {activeView === 'top' ? '✓ ' : ''}Top View
          </DropdownItem>
          <DropdownItem onClick={() => handleSetView('front')}>
            {activeView === 'front' ? '✓ ' : ''}Front View
          </DropdownItem>
          <DropdownItem onClick={() => handleSetView('side')}>
            {activeView === 'side' ? '✓ ' : ''}Side View
          </DropdownItem>
        </DropdownContent>
      </ViewDropdown>

      {/* Zoom Controls */}
      <ToolButton onClick={handleZoomIn} title="Zoom In">
        <ZoomIn size={16} />
      </ToolButton>
      <ToolButton onClick={handleZoomOut} title="Zoom Out">
        <ZoomOut size={16} />
      </ToolButton>
      <ToolButton onClick={handleFitToView} title="Fit to View">
        <Maximize size={16} />
      </ToolButton>

      {/* CAD Tools */}
      <ToolButton onClick={handleBox} title="Box Tool">
        <Box size={16} />
      </ToolButton>
      <ToolButton onClick={handleCircle} title="Circle Tool">
        <Circle size={16} />
      </ToolButton>
      <ToolButton onClick={handleRotate} title="Rotate Tool">
        <RotateCcw size={16} />
      </ToolButton>

      {/* Utility Tools */}
      <ToolButton onClick={handleGrid} title="Toggle Grid">
        <Grid size={16} />
      </ToolButton>
      <ToolButton onClick={handleSettings} title="Settings">
        <Settings size={16} />
      </ToolButton>
      <ToolButton onClick={handleDownload} title="Download">
        <Download size={16} />
      </ToolButton>
      <ToolButton onClick={handleUpload} title="Upload">
        <Upload size={16} />
      </ToolButton>
    </ToolbarContainer>
  );
};

export default Toolbar; 