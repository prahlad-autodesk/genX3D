import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';

// Enhanced mesh system inspired by Cascade Studio's CADWorker implementation
export class EnhancedMeshBuilder {
  constructor() {
    this.vertices = [];
    this.normals = [];
    this.uvs = [];
    this.indices = [];
    this.faceIndex = 0;
    this.edgeVertices = [];
    this.edgeIndices = [];
  }

  // Create high-quality triangulated geometry from vertices and faces
  createTriangulatedGeometry(vertices, faces, options = {}) {
    const {
      enableUVs = true,
      enableNormals = true
    } = options;

    this.vertices = [];
    this.normals = [];
    this.uvs = [];
    this.indices = [];
    this.faceIndex = 0;

    // Process each face
    faces.forEach((face, faceIndex) => {
      this.processFace(face, faceIndex, enableUVs, enableNormals);
    });

    // Create the geometry
    const geometry = new THREE.BufferGeometry();
    
    // Set attributes
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(this.vertices, 3));
    
    if (enableNormals && this.normals.length > 0) {
      geometry.setAttribute('normal', new THREE.Float32BufferAttribute(this.normals, 3));
    }
    
    if (enableUVs && this.uvs.length > 0) {
      geometry.setAttribute('uv', new THREE.Float32BufferAttribute(this.uvs, 2));
    }

    // Set indices
    if (this.indices.length > 0) {
      geometry.setIndex(this.indices);
    }

    // Compute missing attributes
    if (!enableNormals || this.normals.length === 0) {
      geometry.computeVertexNormals();
    }

    geometry.computeBoundingSphere();
    geometry.computeBoundingBox();

    return geometry;
  }

  // Process a single face with proper triangulation
  processFace(face, faceIndex, enableUVs, enableNormals) {
    const faceVertices = face.vertices || [];
    const faceUVs = face.uvs || [];
    const faceNormals = face.normals || [];

    if (faceVertices.length < 3) return;

    // Triangulate the face (simple fan triangulation for now)
    const baseVertex = 0;
    for (let i = 1; i < faceVertices.length - 1; i++) {
      const v1 = baseVertex;
      const v2 = i;
      const v3 = i + 1;

      // Add vertices
      this.addVertex(faceVertices[v1]);
      this.addVertex(faceVertices[v2]);
      this.addVertex(faceVertices[v3]);

      // Add UVs if available
      if (enableUVs && faceUVs.length >= faceVertices.length) {
        this.addUV(faceUVs[v1] || [0, 0]);
        this.addUV(faceUVs[v2] || [0, 0]);
        this.addUV(faceUVs[v3] || [0, 0]);
      }

      // Add normals if available
      if (enableNormals && faceNormals.length >= faceVertices.length) {
        this.addNormal(faceNormals[v1] || [0, 1, 0]);
        this.addNormal(faceNormals[v2] || [0, 1, 0]);
        this.addNormal(faceNormals[v3] || [0, 1, 0]);
      }

      // Add indices
      const baseIndex = this.faceIndex * 3;
      this.indices.push(baseIndex, baseIndex + 1, baseIndex + 2);
      this.faceIndex++;
    }
  }

  // Create adaptive geometry based on shape characteristics
  createAdaptiveGeometry(shapeData, options = {}) {
    const {
      quality = 'high',
      maxSegments = 64,
      minSegments = 8
    } = options;

    const { type, dimensions, center = [0, 0, 0] } = shapeData;

    switch (type) {
      case 'box':
        return this.createAdaptiveBox(dimensions, center, quality, maxSegments, minSegments);
      case 'sphere':
        return this.createAdaptiveSphere(dimensions, center, quality, maxSegments, minSegments);
      case 'cylinder':
        return this.createAdaptiveCylinder(dimensions, center, quality, maxSegments, minSegments);
      default:
        return this.createAdaptiveBox(dimensions, center, quality, maxSegments, minSegments);
    }
  }

  // Create adaptive box with quality-based segmentation
  createAdaptiveBox(dimensions, center, quality, maxSegments, minSegments) {
    const [width, height, depth] = dimensions;
    const maxDim = Math.max(width, height, depth);
    
    let segments = Math.max(minSegments, Math.min(maxSegments, Math.floor(maxDim / 2)));
    
    // Adjust segments based on quality
    switch (quality) {
      case 'low':
        segments = Math.max(2, Math.floor(segments / 2));
        break;
      case 'medium':
        segments = Math.max(4, Math.floor(segments / 1.5));
        break;
      case 'high':
        segments = Math.max(8, segments);
        break;
      case 'ultra':
        segments = Math.max(16, Math.floor(segments * 1.5));
        break;
      default:
        segments = Math.max(8, segments);
        break;
    }

    const geometry = new THREE.BoxGeometry(width, height, depth, segments, segments, segments);
    geometry.translate(center[0], center[1], center[2]);
    
    this.enhanceGeometry(geometry, quality);
    return geometry;
  }

  // Create adaptive sphere with quality-based segmentation
  createAdaptiveSphere(dimensions, center, quality, maxSegments, minSegments) {
    const radius = Array.isArray(dimensions) ? dimensions[0] : dimensions;
    
    let segments = Math.max(minSegments, Math.min(maxSegments, Math.floor(radius * 8)));
    
    // Adjust segments based on quality
    switch (quality) {
      case 'low':
        segments = Math.max(8, Math.floor(segments / 2));
        break;
      case 'medium':
        segments = Math.max(16, Math.floor(segments / 1.5));
        break;
      case 'high':
        segments = Math.max(32, segments);
        break;
      case 'ultra':
        segments = Math.max(64, Math.floor(segments * 1.5));
        break;
      default:
        segments = Math.max(8, segments);
        break;
    }

    const geometry = new THREE.SphereGeometry(radius, segments, segments);
    geometry.translate(center[0], center[1], center[2]);
    
    this.enhanceGeometry(geometry, quality);
    return geometry;
  }

  // Create adaptive cylinder with quality-based segmentation
  createAdaptiveCylinder(dimensions, center, quality, maxSegments, minSegments) {
    const [radius, height] = Array.isArray(dimensions) ? dimensions : [dimensions, dimensions];
    
    let segments = Math.max(minSegments, Math.min(maxSegments, Math.floor(radius * 8)));
    
    // Adjust segments based on quality
    switch (quality) {
      case 'low':
        segments = Math.max(8, Math.floor(segments / 2));
        break;
      case 'medium':
        segments = Math.max(16, Math.floor(segments / 1.5));
        break;
      case 'high':
        segments = Math.max(32, segments);
        break;
      case 'ultra':
        segments = Math.max(64, Math.floor(segments * 1.5));
        break;
      default:
        segments = Math.max(8, segments);
        break;
    }

    const geometry = new THREE.CylinderGeometry(radius, radius, height, segments);
    geometry.translate(center[0], center[1], center[2]);
    
    this.enhanceGeometry(geometry, quality);
    return geometry;
  }

  // Enhance geometry with additional attributes and optimizations
  enhanceGeometry(geometry, quality) {
    // Ensure proper normals
    geometry.computeVertexNormals();
    
    // Optimize for rendering
    geometry.computeBoundingSphere();
    geometry.computeBoundingBox();
    
    // Add quality-based optimizations
    if (quality === 'ultra') {
      // Add tangent space for advanced materials
      geometry.computeTangents();
    }
  }

  // Create edge geometry for wireframe rendering
  createEdgeGeometry(baseGeometry, options = {}) {
    const {
      thresholdAngle = 15,
      color = 0x444444,
      opacity = 0.5
    } = options;

    const edges = new THREE.EdgesGeometry(baseGeometry, thresholdAngle);
    const material = new THREE.LineBasicMaterial({
      color: color,
      opacity: opacity,
      transparent: true
    });

    return { geometry: edges, material };
  }

  // Helper methods
  addVertex(vertex) {
    this.vertices.push(...vertex);
  }

  addNormal(normal) {
    this.normals.push(...normal);
  }

  addUV(uv) {
    this.uvs.push(...uv);
  }
}

// React hook for enhanced mesh building
export function useEnhancedMesh() {
  const meshBuilderRef = useRef(new EnhancedMeshBuilder());
  
  const createMesh = (shapeData, options = {}) => {
    return meshBuilderRef.current.createAdaptiveGeometry(shapeData, options);
  };

  const createTriangulatedMesh = (vertices, faces, options = {}) => {
    return meshBuilderRef.current.createTriangulatedGeometry(vertices, faces, options);
  };

  const createEdgeMesh = (baseGeometry, options = {}) => {
    return meshBuilderRef.current.createEdgeGeometry(baseGeometry, options);
  };

  return {
    createMesh,
    createTriangulatedMesh,
    createEdgeMesh,
    meshBuilder: meshBuilderRef.current
  };
}

// Enhanced mesh component with quality controls
export function EnhancedMesh({ 
  shapeData, 
  quality = 'high', 
  showEdges = true, 
  material,
  onLoad,
  ...props 
}) {
  const { createMesh, createEdgeMesh } = useEnhancedMesh();
  const [geometry, setGeometry] = useState(null);
  const [edgeGeometry, setEdgeGeometry] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!shapeData) return;

    setLoading(true);
    
    try {
      // Create main geometry
      const mainGeometry = createMesh(shapeData, { quality });
      setGeometry(mainGeometry);

      // Create edge geometry if requested
      if (showEdges) {
        const edgeData = createEdgeMesh(mainGeometry);
        setEdgeGeometry(edgeData);
      }

      onLoad?.(mainGeometry);
    } catch (error) {
      console.error('Error creating enhanced mesh:', error);
    } finally {
      setLoading(false);
    }
  }, [shapeData, quality, showEdges, createMesh, createEdgeMesh, onLoad]);

  if (loading) {
    return null;
  }

  return (
    <group {...props}>
      {geometry && (
        <mesh geometry={geometry} material={material} castShadow />
      )}
      {edgeGeometry && (
        <lineSegments geometry={edgeGeometry.geometry} material={edgeGeometry.material} />
      )}
    </group>
  );
} 