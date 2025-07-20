---
sidebar_position: 2
---

# Quick Start Guide

Get up and running with genx3D in under 5 minutes!

## Prerequisites

- Docker installed on your system
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/genx3D.git
cd genx3D

# Create environment file
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
```

## Step 2: Run with Docker

```bash
# Build and run
docker build -t genx3d .
docker run -d --env-file .env -p 8000:8000 genx3d
```

## Step 3: Access the Application

Open your browser and go to:
- **Main App**: [http://localhost:8000/app/](http://localhost:8000/app/)

## Step 4: Create Your First Model

1. **Open the CAD Interface**
   - Navigate to the 3D modeling area
   - You'll see the Cascade Studio interface

2. **Try Basic Modeling**
   ```javascript
   // Create a simple cube
   var cube = CSG.cube({
     center: [0, 0, 0],
     radius: [10, 10, 10]
   });
   ```

3. **Use the AI Assistant**
   - Click on the chat icon
   - Ask: "Create a simple gear with 20 teeth"
   - The AI will help you generate the code

## Step 5: Export Your Model

1. **Generate STL File**
   ```javascript
   // Export as STL
   cube.toSTL();
   ```

2. **Download the File**
   - The STL file will be available for download
   - You can also export as STEP format

## What's Next?

Now that you've created your first model, explore:

- [3D CAD Modeling Features](../features/3d-cad-modeling) - Learn advanced modeling techniques
- [AI Assistant Usage](../features/ai-chat-assistant) - Master the AI-powered features
- [API Integration](../api/endpoints) - Integrate with your own applications

## Troubleshooting

**App not loading?**
- Check if Docker container is running: `docker ps`
- Verify port 8000 is available: `lsof -i :8000`

**AI features not working?**
- Verify your OpenRouter API key in the `.env` file
- Check the logs: `docker logs <container_id>`

**Need help?**
- Check our [troubleshooting guide](./installation#troubleshooting)
- [Report an issue](https://github.com/yourusername/genx3D/issues)

## Example Projects

Try these examples to get familiar with genx3D:

### Simple Gear
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

var myGear = createGear(20, 30, 10);
```

### Parametric Box
```javascript
function createBox(width, height, depth, wallThickness) {
  var outer = CSG.cube({
    center: [0, 0, 0],
    radius: [width/2, height/2, depth/2]
  });
  
  var inner = CSG.cube({
    center: [0, 0, 0],
    radius: [width/2 - wallThickness, height/2 - wallThickness, depth/2 - wallThickness]
  });
  
  return outer.subtract(inner);
}

var box = createBox(50, 30, 20, 2);
```

Ready to dive deeper? Check out our [comprehensive tutorials](../tutorials/first-model)! 