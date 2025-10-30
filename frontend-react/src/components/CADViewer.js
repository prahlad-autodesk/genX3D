import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { ModelLoader } from './STEPLoader';
import * as THREE from 'three';
import { EnhancedMesh } from './EnhancedMeshSystem';

const ViewerContainer = styled.div`
  width: 100%;
  height: 100%;
  position: relative;
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 20px;
  border-radius: 8px;
  z-index: 10;
`;



// Component for loading and displaying STL files
function STLModel({ url, color = '#4CAF50' }) {
  return (
    <ModelLoader 
      url={url} 
      type="stl" 
      color={color}
      onLoad={(geometry, type) => {
        console.log(`${type.toUpperCase()} model loaded successfully!`);
      }}
      onError={(error, type) => {
        console.error(`Failed to load ${type.toUpperCase()} model: ${error.message}`);
      }}
    />
  );
}

// Component for loading and displaying GLTF/GLB files
function GLTFModel({ url }) {
  return (
    <ModelLoader 
      url={url} 
      type="gltf" 
      color="#4CAF50"
      onLoad={(geometry, type) => {
        console.log(`${type.toUpperCase()} model loaded successfully!`);
      }}
      onError={(error, type) => {
        console.error(`Failed to load ${type.toUpperCase()} model: ${error.message}`);
      }}
    />
  );
}

// Main 3D scene component - Cascade Studio style
function Scene({ currentModel, onModelError }) {
  const controlsRef = useRef();
  const sceneRef = useRef();
  const [matcapMaterial, setMatcapMaterial] = useState(null);

  // Load Cascade Studio matcap material
  useEffect(() => {
    const loader = new THREE.TextureLoader();
    loader.setCrossOrigin('');
    
    loader.load('/dullFrontLitMetal.png', (texture) => {
      const material = new THREE.MeshMatcapMaterial({
        color: new THREE.Color(0xf5f5f5),
        matcap: texture,
        polygonOffset: true,
        polygonOffsetFactor: 2.0,
        polygonOffsetUnits: 1.0
      });
      setMatcapMaterial(material);
    }, undefined, (error) => {
      console.warn('Failed to load matcap texture:', error);
      // Fallback to basic matcap material
      const material = new THREE.MeshMatcapMaterial({
        color: new THREE.Color(0xf5f5f5),
        polygonOffset: true,
        polygonOffsetFactor: 2.0,
        polygonOffsetUnits: 1.0
      });
      setMatcapMaterial(material);
    });
  }, []);

  useFrame(() => {
    if (controlsRef.current) {
      controlsRef.current.update();
    }
  });

  // Fit model to view (Cascade Studio style) - Fixed version
  const fitToView = useCallback(() => {
    if (!controlsRef.current || !sceneRef.current) {
      console.log('Controls or scene not ready');
      return;
    }
    
    const controls = controlsRef.current;
    const scene = sceneRef.current;
    
    // Find all mesh objects in the scene (excluding ground and grid)
    const meshes = [];
    scene.traverse((child) => {
      if (child.type === 'Mesh' && 
          child !== scene.children.find(c => c.type === 'Mesh' && c.geometry?.type === 'PlaneGeometry') && // Skip ground
          child !== scene.children.find(c => c.type === 'GridHelper')) { // Skip grid
        meshes.push(child);
      }
    });
    
    if (meshes.length === 0) {
      console.log('No model meshes found - fitToView skipped');
      return;
    }
    
    // Compute bounding box of all meshes
    const box = new THREE.Box3();
    meshes.forEach(mesh => {
      box.expandByObject(mesh);
    });
    
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    
    // Set camera to frame the bounding box
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = controls.object.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
    cameraZ *= 1.5; // Add some padding
    
    controls.object.position.set(center.x, center.y, cameraZ + center.z);
    controls.object.lookAt(center.x, center.y, center.z);
    controls.target.copy(center);
    controls.update();
    
    console.log('Fit to view completed', { size, center, cameraZ });
  }, []);

  // Set specific view (Cascade Studio style) - Fixed version
  const setView = useCallback((view) => {
    if (!controlsRef.current) {
      console.log('Controls not ready');
      return;
    }
    
    const camera = controlsRef.current.object;
    const controls = controlsRef.current;
    const target = controls.target.clone();
    
    // Compute current distance from camera to target
    const distance = camera.position.clone().sub(target).length();
    console.log('Current distance:', distance);

    // Define direction vectors for each view
    let dir;
    switch(view) {
      case 'top':    dir = new THREE.Vector3(0, 1, 0); break;
      case 'front':  dir = new THREE.Vector3(0, 0, 1); break;
      case 'side':   dir = new THREE.Vector3(1, 0, 0); break;
      case 'iso':    dir = new THREE.Vector3(1, 1, 1).normalize(); break;
      default:       dir = camera.position.clone().sub(target).normalize(); break;
    }

    // Set camera position at the same distance in the new direction
    camera.position.copy(target).add(dir.multiplyScalar(distance));
    camera.lookAt(target);
    controls.target.copy(target);
    controls.update();
    
    console.log('View set to:', view, 'position:', camera.position);
  }, []);

  // Auto-fit when model changes
  useEffect(() => {
    if (currentModel) {
      // Longer delay to ensure model is fully loaded
      setTimeout(() => {
        console.log('Auto-fitting model:', currentModel);
        fitToView();
      }, 500);
    }
  }, [currentModel, fitToView]);

  // Expose functions globally for toolbar access
  useEffect(() => {
    window.fitToView = fitToView;
    window.setView = setView;
    window.controlsRef = controlsRef;
    return () => {
      delete window.fitToView;
      delete window.setView;
      delete window.controlsRef;
    };
  }, [fitToView, setView]);

  return (
    <group ref={sceneRef}>
      {/* Cascade Studio Lighting */}
      <hemisphereLight position={[0, 200, 0]} intensity={1} color={0xffffff} groundColor={0x444444} />
      <directionalLight position={[6, 50, -12]} intensity={1} color={0xbbbbbb} castShadow />

      {/* Cascade Studio Grid and Ground */}
      <mesh position={[0, -0.1, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[2000, 2000]} />
        <meshPhongMaterial color={0x080808} depthWrite={true} dithering={true} />
      </mesh>
      
      <gridHelper 
        args={[2000, 20, 0xcccccc, 0xcccccc]} 
        position={[0, -0.01, 0]}
        material={new THREE.LineBasicMaterial({ 
          color: 0xcccccc, 
          opacity: 0.3, 
          transparent: true 
        })}
      />

      {/* Model */}
      {currentModel && (
        <>
          {currentModel.type === 'stl' && (
            <STLModel url={currentModel.url} color={currentModel.color} />
          )}
          {currentModel.type === 'step' && (
            <ModelLoader 
              url={currentModel.url} 
              type="step" 
              color={currentModel.color}
              onLoad={(geometry, type) => {
                console.log(`${type.toUpperCase()} model loaded successfully!`);
              }}
              onError={(error, type) => {
                console.error(`Failed to load ${type.toUpperCase()} model: ${error.message}`);
                // Don't set fallback model - let user handle the error
                console.error(`Model loading error:`, error);
              }}
            />
          )}
          {currentModel.type === 'gltf' && (
            <GLTFModel url={currentModel.url} />
          )}
          {currentModel.type === 'auto' && currentModel.url && (
            <ModelLoader 
              url={currentModel.url} 
              type="auto" 
              color={currentModel.color}
              onLoad={(geometry, type) => {
                console.log(`${type.toUpperCase()} model loaded successfully!`);
              }}
              onError={(error, type) => {
                console.error(`Failed to load ${type.toUpperCase()} model: ${error.message}`);
                // Don't set fallback model - let user handle the error
                console.error(`Model loading error:`, error);
              }}
            />
          )}
          {currentModel.type === 'primitive' && (
            <>
              {currentModel.shape === 'box' && matcapMaterial && (
                <EnhancedMesh
                  shapeData={{
                    type: 'box',
                    dimensions: currentModel.dimensions || [1, 1, 1],
                    center: [0, 0, 0]
                  }}
                  quality="high"
                  showEdges={true}
                  material={matcapMaterial}
                />
              )}
              {currentModel.shape === 'sphere' && matcapMaterial && (
                <EnhancedMesh
                  shapeData={{
                    type: 'sphere',
                    dimensions: [currentModel.radius || 0.5],
                    center: [0, 0, 0]
                  }}
                  quality="high"
                  showEdges={true}
                  material={matcapMaterial}
                />
              )}
              {currentModel.shape === 'cylinder' && matcapMaterial && (
                <EnhancedMesh
                  shapeData={{
                    type: 'cylinder',
                    dimensions: [currentModel.radius || 0.5, currentModel.height || 1],
                    center: [0, 0, 0]
                  }}
                  quality="high"
                  showEdges={true}
                  material={matcapMaterial}
                />
              )}
            </>
          )}
        </>
      )}

      {/* Cascade Studio Controls - No distance limits */}
      <OrbitControls 
        ref={controlsRef}
        target={[0, 45, 0]}
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        panSpeed={2}
        zoomSpeed={1}
        screenSpacePanning={true}
        enableDamping={true}
        dampingFactor={0.05}
      />
    </group>
  );
}

const CADViewer = () => {
  const [currentModel, setCurrentModel] = useState(null);
  const [loading, setLoading] = useState(false);

  // Listen for model loading events from the chat assistant
  useEffect(() => {
    const handleModelLoad = (event) => {
      if (event.detail && event.detail.model) {
        const model = event.detail.model;
        console.log('CADViewer received model load event:', model);
        
        setLoading(true);
        
        // Use the actual model URL to load the real CAD model
        setCurrentModel({
          type: model.type || 'auto',
          url: model.url,
          color: '#4CAF50',
          metadata: {
            url: model.url,
            modelId: model.modelId,
            prompt: model.prompt,
            modelType: model.modelType,
            similarityScore: model.similarityScore
          }
        });
        
        setLoading(false);
        toast.success(`Loading ${model.modelType || '3D'} model from backend!`);
      } else {
        console.log('CADViewer received model load event but no model data:', event.detail);
      }
    };

    window.addEventListener('loadModel', handleModelLoad);
    return () => window.removeEventListener('loadModel', handleModelLoad);
  }, []);

  // Function to load model from URL
  const loadModelFromURL = (url, type = 'stl') => {
    setLoading(true);
    setCurrentModel({ url, type });
    setLoading(false);
  };

  // Expose the function globally for the chat assistant
  useEffect(() => {
    window.loadModelFromURL = loadModelFromURL;
  }, []);

  return (
    <ViewerContainer>
      {loading && (
        <LoadingOverlay>
          Loading model...
        </LoadingOverlay>
      )}

      <Canvas
        camera={{ position: [50, 100, 150], fov: 45, near: 1, far: 5000 }}
        style={{ background: '#222222' }}
        shadows
        gl={{ antialias: true, webgl2: false }}
      >
        <fog attach="fog" args={[0x222222, 200, 600]} />
        <Scene 
          currentModel={currentModel} 
        />
      </Canvas>
    </ViewerContainer>
  );
};

export default CADViewer; 