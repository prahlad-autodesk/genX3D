import React, { useState, useEffect } from 'react';
import * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';

// Cascade Studio style matcap material hook
function useMatcapMaterial() {
  const [matcapMaterial, setMatcapMaterial] = useState(null);

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

  return matcapMaterial;
}

// Robust STEP parser (simplified but effective)
class RobustSTEPParser {
  constructor() {
    this.entities = new Map();
    this.vertices = [];
    this.faces = [];
  }

  async parse(stepContent) {
    try {
      console.log('RobustSTEPParser: Starting to parse STEP content...');
      console.log('RobustSTEPParser: Content length:', stepContent.length);
      
      // Check if content looks like a STEP file
      if (!stepContent.includes('ISO-10303-21') && !stepContent.includes('STEP')) {
        console.warn('RobustSTEPParser: Content does not appear to be a STEP file');
      }
      
      this.parseContent(stepContent);
      console.log('RobustSTEPParser: Content parsed, entities found:', this.entities.size);
      
      const geometry = await this.buildGeometry();
      console.log('RobustSTEPParser: Geometry built:', geometry ? 'success' : 'failed');
      
      return geometry;
    } catch (error) {
      console.error('RobustSTEPParser: Error parsing STEP file:', error);
      return null;
    }
  }

  parseContent(stepContent) {
    try {
      const lines = stepContent.split('\n');
      console.log('RobustSTEPParser: Total lines:', lines.length);
      
      let entityCount = 0;
      let cartesianPointCount = 0;
      
      // First pass: collect all entities
      for (const line of lines) {
        const trimmed = line.trim();
        
        if (trimmed.startsWith('#')) {
          const match = trimmed.match(/#(\d+)\s*=\s*([^(]+)\(([^)]*)\)/);
          if (match) {
            const [, id, type, params] = match;
            const entity = { 
              id: parseInt(id), 
              type, 
              params: this.parseParams(params),
              raw: trimmed
            };
            this.entities.set(parseInt(id), entity);
            entityCount++;
            
            if (type === 'CARTESIAN_POINT') {
              cartesianPointCount++;
            }
          }
        }
      }
      
      console.log('RobustSTEPParser: Total entities found:', entityCount);
      console.log('RobustSTEPParser: CARTESIAN_POINT entities found:', cartesianPointCount);
      
    } catch (error) {
      console.error('RobustSTEPParser: Error parsing STEP content:', error);
    }
  }

  parseParams(params) {
    const result = [];
    let current = '';
    let depth = 0;
    let inString = false;
    
    for (let i = 0; i < params.length; i++) {
      const char = params[i];
      
      if (char === "'" && (i === 0 || params[i-1] !== "'")) {
        inString = !inString;
        current += char;
      } else if (!inString) {
        if (char === '(') {
          depth++;
          current += char;
        } else if (char === ')') {
          depth--;
          current += char;
        } else if (char === ',' && depth === 0) {
          result.push(current.trim());
          current = '';
        } else {
          current += char;
        }
      } else {
        current += char;
      }
    }
    
    if (current.trim()) {
      result.push(current.trim());
    }
    
    return result;
  }

  extractCartesianPoint(entity) {
    try {
      if (entity.type === 'CARTESIAN_POINT') {
        // Try to find coordinates in the raw entity string first
        const rawMatch = entity.raw.match(/CARTESIAN_POINT\('[^']*',\(([^)]+)\)\)/);
        if (rawMatch) {
          const coords = rawMatch[1].split(',').map(c => parseFloat(c.trim())).filter(c => !isNaN(c));
          if (coords.length >= 3) {
            return coords.slice(0, 3);
          }
        }
        
        // Fallback: try to parse from params
        if (entity.params && entity.params.length >= 1) {
          const coordsStr = entity.params[0];
          if (coordsStr) {
            const coordsMatch = coordsStr.match(/\(([^)]+)\)/);
            if (coordsMatch) {
              const coords = coordsMatch[1].split(',').map(c => parseFloat(c.trim())).filter(c => !isNaN(c));
              if (coords.length >= 3) {
                return coords.slice(0, 3);
              }
            }
          }
        }
      }
      return null;
    } catch (error) {
      console.error('RobustSTEPParser: Error extracting cartesian point:', error);
      return null;
    }
  }

  async buildGeometry() {
    try {
      console.log('RobustSTEPParser: Starting buildGeometry...');
      
      const vertices = [];
      
      // Extract all CARTESIAN_POINT entities
      for (const [, entity] of this.entities) {
        if (entity.type === 'CARTESIAN_POINT') {
          const coords = this.extractCartesianPoint(entity);
          if (coords) {
            vertices.push(coords);
          }
        }
      }
      
      console.log('RobustSTEPParser: Found vertices:', vertices.length);
      
      // If we have vertices, create geometry based on bounding box
      if (vertices.length > 0) {
        // Calculate bounding box
        const minX = Math.min(...vertices.map(v => v[0]));
        const maxX = Math.max(...vertices.map(v => v[0]));
        const minY = Math.min(...vertices.map(v => v[1]));
        const maxY = Math.max(...vertices.map(v => v[1]));
        const minZ = Math.min(...vertices.map(v => v[2]));
        const maxZ = Math.max(...vertices.map(v => v[2]));
        
        const width = maxX - minX;
        const height = maxY - minY;
        const depth = maxZ - minZ;
        const center = [(minX + maxX) / 2, (minY + maxY) / 2, (minZ + maxZ) / 2];
        
        console.log('RobustSTEPParser: Bounding box:', { width, height, depth, center });
        
        if (width > 0 && height > 0 && depth > 0) {
          // Create geometry based on proportions
          const maxDim = Math.max(width, height, depth);
          const aspectRatio = [width / maxDim, height / maxDim, depth / maxDim];
          
          // Determine geometry type based on proportions
          if (aspectRatio.every(ratio => Math.abs(ratio - 1) < 0.1)) {
            // Cube-like
            const geometry = new THREE.BoxGeometry(width, height, depth);
            geometry.translate(center[0], center[1], center[2]);
            console.log('RobustSTEPParser: Created cube geometry');
            return geometry;
          } else if (aspectRatio[0] < 0.2 && aspectRatio[1] < 0.2) {
            // Cylinder-like (tall and thin)
            const radius = Math.max(width, height) / 2;
            const geometry = new THREE.CylinderGeometry(radius, radius, depth, 32);
            geometry.translate(center[0], center[1], center[2]);
            console.log('RobustSTEPParser: Created cylinder geometry');
            return geometry;
          } else if (aspectRatio[2] < 0.2) {
            // Flat object
            const geometry = new THREE.BoxGeometry(width, height, Math.max(depth, 0.1));
            geometry.translate(center[0], center[1], center[2]);
            console.log('RobustSTEPParser: Created flat box geometry');
            return geometry;
          } else {
            // Generic box
            const geometry = new THREE.BoxGeometry(width, height, depth);
            geometry.translate(center[0], center[1], center[2]);
            console.log('RobustSTEPParser: Created generic box geometry');
            return geometry;
          }
        } else {
          // Fallback to sphere for very small or degenerate cases
          const radius = Math.max(width, height, depth) / 2 || 1;
          console.log('RobustSTEPParser: Using fallback sphere with radius:', radius);
          return new THREE.SphereGeometry(radius, 32, 32);
        }
      }
      
      console.log('RobustSTEPParser: No vertices found, returning null');
      return null;
    } catch (error) {
      console.error('RobustSTEPParser: Error building geometry:', error);
      return null;
    }
  }
}

// STL Loader Hook
function useSTLLoader(url) {
  const [geometry, setGeometry] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) {
      setLoading(false);
      setError(null);
      setGeometry(null);
      return;
    }

    setLoading(true);
    setError(null);

    const loader = new STLLoader();
    
    loader.load(
      url,
      (geometry) => {
        geometry.computeVertexNormals();
        setGeometry(geometry);
        setLoading(false);
      },
      (progress) => {
        console.log('Loading progress:', (progress.loaded / progress.total * 100) + '%');
      },
      (error) => {
        console.error('STL loading error:', error);
        setError(error);
        setLoading(false);
      }
    );
  }, [url]);

  return { geometry, loading, error };
}

// STEP Loader Hook with robust parser
function useSTEPLoader(url) {
  const [geometry, setGeometry] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) {
      setLoading(false);
      setError(null);
      setGeometry(null);
      return;
    }

    setLoading(true);
    setError(null);

    const loadSTEP = async () => {
      try {
        console.log('useSTEPLoader: Loading STEP file from:', url);
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const stepContent = await response.text();
        console.log('useSTEPLoader: STEP content loaded, length:', stepContent.length);
        
        const parser = new RobustSTEPParser();
        const geometry = await parser.parse(stepContent);
        
        if (geometry) {
          console.log('useSTEPLoader: STEP parsing successful');
          setGeometry(geometry);
        } else {
          throw new Error('Failed to parse STEP file');
        }
      } catch (error) {
        console.error('useSTEPLoader: STEP loading error:', error);
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    loadSTEP();
  }, [url]);

  return { geometry, loading, error };
}

// Main Model Loader Component
export function ModelLoader({ url, type = 'auto', color = '#4CAF50', onLoad, onError }) {
  const [detectedType, setDetectedType] = useState(type);
  const matcapMaterial = useMatcapMaterial();
  
  // Auto-detect file type from URL
  useEffect(() => {
    if (type === 'auto' && url) {
      const extension = url.split('.').pop()?.toLowerCase();
      if (extension === 'stl') {
        setDetectedType('stl');
      } else if (extension === 'step' || extension === 'stp') {
        setDetectedType('step');
      } else {
        setDetectedType('unknown');
      }
    }
  }, [url, type]);

  // Use appropriate loader based on file type
  const stlResult = useSTLLoader(detectedType === 'stl' ? url : null);
  const stepResult = useSTEPLoader(detectedType === 'step' ? url : null);

  const { geometry, loading, error } = detectedType === 'stl' ? stlResult : stepResult;

  // Handle loading states
  useEffect(() => {
    if (loading) {
      console.log(`Loading ${detectedType.toUpperCase()} file...`);
    }
  }, [loading, detectedType]);

  // Handle successful load
  useEffect(() => {
    if (geometry && !loading) {
      console.log(`${detectedType.toUpperCase()} file loaded successfully!`);
      onLoad?.(geometry, detectedType);
    }
  }, [geometry, loading, detectedType, onLoad]);

  // Handle errors
  useEffect(() => {
    if (error) {
      console.error(`${detectedType.toUpperCase()} loading error:`, error);
      onError?.(error, detectedType);
    }
  }, [error, detectedType, onError]);

  // Don't render anything if there's no URL
  if (!url) {
    return null;
  }

  // Render the loaded geometry with Cascade Studio style
  if (geometry && !loading && matcapMaterial) {
    return (
      <group>
        <mesh geometry={geometry} castShadow material={matcapMaterial} />
        <lineSegments>
          <edgesGeometry args={[geometry]} />
          <lineBasicMaterial color={0x444444} opacity={0.5} transparent />
        </lineSegments>
      </group>
    );
  }

  // Show loading state
  if (loading) {
    return (
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="#666" transparent opacity={0.5} />
      </mesh>
    );
  }

  // Show error state
  if (error) {
    console.error(`Model loading error:`, error);
    return null;
  }

  return null;
}

// Export the parser for direct use
export { RobustSTEPParser };

// Utility function to convert STEP to STL (placeholder)
export async function convertSTEPtoSTL(stepUrl) {
  try {
    await fetch(stepUrl);
    
    // This is a placeholder - in a real implementation, you would:
    // 1. Parse the STEP file
    // 2. Extract geometry data
    // 3. Convert to STL format
    // 4. Return STL content
    
    console.log('STEP to STL conversion not implemented yet');
    return null;
  } catch (error) {
    console.error('STEP to STL conversion error:', error);
    return null;
  }
}

// Utility function to validate STEP file
export function validateSTEPFile(content) {
  const lines = content.split('\n');
  const hasHeader = lines.some(line => line.includes('ISO-10303-21'));
  const hasEntities = lines.some(line => line.startsWith('#'));
  const hasEnd = lines.some(line => line.includes('ENDSEC'));
  
  return hasHeader && hasEntities && hasEnd;
}

export default ModelLoader; 