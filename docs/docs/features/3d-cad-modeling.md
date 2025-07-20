---
sidebar_position: 1
---

# 3D CAD Modeling

genx3D provides powerful browser-based 3D CAD modeling capabilities through Cascade Studio integration.

## Overview

The 3D CAD modeling system in genx3D offers:

- **Parametric Design**: Create models with parameters that can be easily modified
- **Real-time Visualization**: See your models rendered in real-time
- **Multiple File Formats**: Export to STL, STEP, and other standard formats
- **Web-based Interface**: No software installation required

## Getting Started with Modeling

### Basic Shapes

Start with fundamental geometric shapes:

```javascript
// Create a cube
var cube = CSG.cube({
  center: [0, 0, 0],
  radius: [10, 10, 10]
});

// Create a cylinder
var cylinder = CSG.cylinder({
  start: [0, 0, 0],
  end: [0, 0, 20],
  radius: 5
});

// Create a sphere
var sphere = CSG.sphere({
  center: [0, 0, 0],
  radius: 8
});
```

### Transformations

Apply transformations to your shapes:

```javascript
// Translate (move)
var movedCube = cube.translate([10, 0, 0]);

// Rotate
var rotatedCube = cube.rotateX(45);

// Scale
var scaledCube = cube.scale([2, 1, 1]);
```

### Boolean Operations

Combine shapes using boolean operations:

```javascript
// Union (combine)
var combined = cube.union(cylinder);

// Subtraction (cut)
var cutShape = cube.subtract(cylinder);

// Intersection
var intersection = cube.intersect(cylinder);
```

## Advanced Modeling Techniques

### Parametric Design

Create models that can be easily modified:

```javascript
function createGear(teeth, radius, thickness) {
  var gear = CSG.cylinder({
    start: [0, 0, 0],
    end: [0, 0, thickness],
    radius: radius
  });
  
  for (var i = 0; i < teeth; i++) {
    var angle = (i * 360) / teeth;
    var tooth = CSG.cube({
      center: [radius * Math.cos(angle * Math.PI / 180), 
               radius * Math.sin(angle * Math.PI / 180), thickness/2],
      radius: [2, 2, thickness/2]
    });
    gear = gear.union(tooth);
  }
  
  return gear;
}

// Create gears with different parameters
var smallGear = createGear(12, 20, 5);
var largeGear = createGear(24, 40, 8);
```

### Complex Geometries

Build more complex shapes:

```javascript
// Loft between profiles
var profile1 = CSG.circle({center: [0, 0, 0], radius: 10});
var profile2 = CSG.circle({center: [0, 0, 20], radius: 5});
var lofted = CSG.loft([profile1, profile2]);

// Sweep along path
var path = CSG.circle({center: [0, 0, 0], radius: 30});
var profile = CSG.circle({center: [0, 0, 0], radius: 2});
var swept = profile.sweep(path);
```

## File Export

### STL Export

Export your models for 3D printing:

```javascript
// Export current model as STL
var stlData = main().toSTL();

// Download the file
download(stlData, "model.stl", "application/octet-stream");
```

### STEP Export

Export for CAD software compatibility:

```javascript
// Export as STEP format
var stepData = main().toSTEP();

// Download the file
download(stepData, "model.step", "application/octet-stream");
```

## Best Practices

### Performance Optimization

- Use simple shapes when possible
- Avoid excessive boolean operations
- Optimize parameter ranges for your use case

### Design Guidelines

- Maintain proper tolerances for manufacturing
- Use parametric design for flexibility
- Test your models with different parameters

### File Management

- Use descriptive names for your models
- Organize complex models into functions
- Document your design parameters

## Integration with AI Assistant

The AI assistant can help you with:

- **Code Generation**: Generate CAD code from natural language descriptions
- **Design Suggestions**: Get recommendations for improving your models
- **Troubleshooting**: Debug issues with your CAD code
- **Optimization**: Find ways to improve model performance

Example AI interaction:
```
User: "Create a gear with 20 teeth and 30mm diameter"
AI: Generates complete gear code with parameters
```

## Examples

### Mechanical Components

```javascript
// Bearing housing
function createBearingHousing(outerRadius, innerRadius, height) {
  var outer = CSG.cylinder({
    start: [0, 0, 0],
    end: [0, 0, height],
    radius: outerRadius
  });
  
  var inner = CSG.cylinder({
    start: [0, 0, 0],
    end: [0, 0, height],
    radius: innerRadius
  });
  
  return outer.subtract(inner);
}
```

### Architectural Elements

```javascript
// Parametric arch
function createArch(width, height, thickness) {
  var base = CSG.cube({
    center: [0, 0, 0],
    radius: [width/2, thickness/2, height/2]
  });
  
  var arch = CSG.cylinder({
    start: [-width/2, 0, height/2],
    end: [width/2, 0, height/2],
    radius: height/2
  });
  
  return base.union(arch);
}
```

## Next Steps

- [AI Chat Assistant](./ai-chat-assistant) - Learn how to use AI for modeling assistance
- [Model Generation](./model-generation) - Generate models automatically
- [Model Analysis](./model-analysis) - Analyze your models for manufacturing
- [Tutorials](../tutorials/first-model) - Step-by-step modeling tutorials 