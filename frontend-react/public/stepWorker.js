// STEP Parser Web Worker
// This worker handles STEP file parsing using OpenCascade.js

let oc = null;

// Initialize OpenCascade.js
async function initializeOpenCascade() {
  try {
    // Try to load from local node_modules first
    importScripts('./opencascade.wasm.js');
    
    // Initialize OpenCascade
    oc = await new opencascade({
      locateFile(path) {
        if (path.endsWith('.wasm')) {
          return './opencascade.wasm.wasm';
        }
        return path;
      }
    });
    
    postMessage({ type: 'initialized' });
  } catch (error) {
    console.error('Failed to load local OpenCascade.js, trying CDN...');
    
    try {
      // Fallback to CDN
      importScripts('https://unpkg.com/opencascade.js@1.1.1/dist/opencascade.wasm.js');
      
      oc = await new opencascade({
        locateFile(path) {
          if (path.endsWith('.wasm')) {
            return 'https://unpkg.com/opencascade.js@1.1.1/dist/opencascade.wasm.wasm';
          }
          return path;
        }
      });
      
      postMessage({ type: 'initialized' });
    } catch (cdnError) {
      console.error('Failed to load OpenCascade.js from CDN:', cdnError);
      postMessage({ type: 'error', error: 'Failed to initialize OpenCascade.js: ' + cdnError.message });
    }
  }
}

// Parse STEP content
function parseSTEP(stepContent) {
  try {
    if (!oc) {
      postMessage({ type: 'error', error: 'OpenCascade.js not initialized' });
      return;
    }
    
    console.log('Worker: Starting STEP parsing...');
    
    // Write STEP file to virtual filesystem
    const fileName = 'temp_model.step';
    oc.FS.createDataFile("/", fileName, stepContent, true, true);
    
    // Use OpenCascade's STEP reader
    const reader = new oc.STEPControl_Reader();
    const readResult = reader.ReadFile(fileName);
    
    if (readResult === 1) {
      console.log('Worker: STEP file read successfully');
      reader.TransferRoots();
      const stepShape = reader.OneShape();
      
      if (!stepShape.IsNull()) {
        console.log('Worker: Shape obtained, converting to mesh...');
        // Convert shape to mesh
        const meshData = shapeToMesh(stepShape);
        
        // Clean up
        oc.FS.unlink("/" + fileName);
        
        console.log('Worker: Mesh conversion completed');
        postMessage({ type: 'success', meshData });
      } else {
        console.error('Worker: Shape is null');
        oc.FS.unlink("/" + fileName);
        postMessage({ type: 'error', error: 'Shape is null' });
      }
    } else {
      console.error('Worker: Failed to read STEP file');
      oc.FS.unlink("/" + fileName);
      postMessage({ type: 'error', error: 'Failed to read STEP file' });
    }
  } catch (error) {
    console.error('Worker: Error parsing STEP file:', error);
    postMessage({ type: 'error', error: error.message });
  }
}

// Convert OpenCascade shape to mesh
function shapeToMesh(shape, maxDeviation = 0.1) {
  try {
    console.log('Worker: Converting shape to mesh with deviation:', maxDeviation);
    
    // Set up incremental mesh builder
    new oc.BRepMesh_IncrementalMesh(shape, maxDeviation, false, maxDeviation * 5);
    
    const vertices = [];
    const indices = [];
    
    // Iterate through faces
    const explorer = new oc.TopExp_Explorer(shape, oc.TopAbs_FACE);
    
    while (explorer.More()) {
      const face = oc.TopoDS.Face(explorer.Current());
      const location = new oc.TopLoc_Location();
      const triangulation = oc.BRep_Tool.prototype.Triangulation(face, location);
      
      if (!triangulation.IsNull()) {
        const nodes = triangulation.get().Nodes();
        const triangles = triangulation.get().Triangles();
        
        // Extract vertices
        for (let i = 0; i < nodes.Length(); i++) {
          const node = nodes.Value(i + 1);
          const transformedNode = node.Transformed(location.Transformation());
          vertices.push(transformedNode.X(), transformedNode.Y(), transformedNode.Z());
        }
        
        // Extract triangles
        for (let i = 0; i < triangles.Length(); i++) {
          const triangle = triangles.Value(i + 1);
          indices.push(triangle.Value(1) - 1, triangle.Value(2) - 1, triangle.Value(3) - 1);
        }
      }
      
      explorer.Next();
    }
    
    console.log('Worker: Created mesh with', vertices.length / 3, 'vertices and', indices.length / 3, 'triangles');
    return { vertices, indices };
  } catch (error) {
    throw new Error('Failed to convert shape to mesh: ' + error.message);
  }
}

// Handle messages from main thread
onmessage = function(e) {
  if (e.data.type === 'initialize') {
    initializeOpenCascade();
  } else if (e.data.type === 'parse') {
    parseSTEP(e.data.content);
  }
};

// Initialize on worker start
initializeOpenCascade(); 