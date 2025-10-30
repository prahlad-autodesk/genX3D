#!/usr/bin/env python3
"""
Fixed CAD Geometry MCP Server
Addresses the MCP initialization issues and provides better error handling.
"""

import json
import tempfile
import os
import traceback
from typing import Dict, Any, Optional, List
from pathlib import Path

# MCP imports - with error handling
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
    print("✅ MCP imports successful")
except ImportError as e:
    print(f"❌ MCP import error: {e}")
    print("Install with: pip install mcp")
    exit(1)

# CAD imports - with error handling
try:
    import cadquery as cq
    from cadquery import exporters
    print("✅ CadQuery imports successful")
except ImportError as e:
    print(f"❌ CadQuery import error: {e}")
    print("Install with: conda install -c conda-forge cadquery")
    exit(1)

class CADModelBuilder:
    """Builder pattern for CAD model construction"""
    
    def __init__(self):
        self.workplane = cq.Workplane("XY")
        self.operations = []
        
    def add_box(self, length: float, width: float, height: float) -> 'CADModelBuilder':
        self.operations.append(("box", {"length": length, "width": width, "height": height}))
        self.workplane = self.workplane.box(length, width, height)
        return self
        
    def add_cylinder(self, radius: float, height: float) -> 'CADModelBuilder':
        self.operations.append(("cylinder", {"radius": radius, "height": height}))
        self.workplane = self.workplane.cylinder(height, radius)
        return self
        
    def build(self) -> cq.Workplane:
        return self.workplane

class CADExporter:
    """Strategy pattern for different export formats"""
    
    @staticmethod
    def export_stl(model: cq.Workplane, filepath: str) -> bool:
        try:
            exporters.export(model, filepath, exportType=exporters.ExportTypes.STL)
            return True
        except Exception as e:
            print(f"STL export failed: {e}")
            return False
            
    @staticmethod
    def export_step(model: cq.Workplane, filepath: str) -> bool:
        try:
            exporters.export(model, filepath, exportType=exporters.ExportTypes.STEP)
            return True
        except Exception as e:
            print(f"STEP export failed: {e}")
            return False

# Global model storage
current_models: Dict[str, cq.Workplane] = {}
temp_dir = tempfile.mkdtemp()

print(f"📁 Temporary directory: {temp_dir}")

app = Server("cad-geometry-server")

@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available CAD tools"""
    return [
        Tool(
            name="create_box",
            description="Create a rectangular box/cube",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Model name/identifier"},
                    "length": {"type": "number", "description": "Length (X dimension)"},
                    "width": {"type": "number", "description": "Width (Y dimension)"},
                    "height": {"type": "number", "description": "Height (Z dimension)"},
                },
                "required": ["name", "length", "width", "height"],
            },
        ),
        Tool(
            name="create_cylinder",
            description="Create a cylinder",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Model name/identifier"},
                    "radius": {"type": "number", "description": "Cylinder radius"},
                    "height": {"type": "number", "description": "Cylinder height"},
                },
                "required": ["name", "radius", "height"],
            },
        ),
        Tool(
            name="create_flange",
            description="Create a standard flange with bolt holes",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Model name/identifier"},
                    "outer_diameter": {"type": "number", "description": "Outer diameter of flange"},
                    "inner_diameter": {"type": "number", "description": "Inner diameter (bore)"},
                    "thickness": {"type": "number", "description": "Flange thickness"},
                    "bolt_circle_diameter": {"type": "number", "description": "Bolt circle diameter"},
                    "bolt_hole_diameter": {"type": "number", "description": "Bolt hole diameter"},
                    "num_bolts": {"type": "integer", "description": "Number of bolt holes", "default": 6},
                },
                "required": ["name", "outer_diameter", "inner_diameter", "thickness", "bolt_circle_diameter", "bolt_hole_diameter"],
            },
        ),
        Tool(
            name="export_model",
            description="Export model to file",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Model name to export"},
                    "format": {"type": "string", "enum": ["stl", "step"], "description": "Export format"},
                    "filename": {"type": "string", "description": "Output filename (optional)"},
                },
                "required": ["name", "format"],
            },
        ),
        Tool(
            name="list_models",
            description="List all current models in memory",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    
    try:
        print(f"🔧 Executing tool: {name} with args: {arguments}")
        
        if name == "create_box":
            model_name = arguments["name"]
            length = float(arguments["length"])
            width = float(arguments["width"])
            height = float(arguments["height"])
            
            builder = CADModelBuilder()
            model = builder.add_box(length, width, height).build()
            current_models[model_name] = model
            result = f"Created box '{model_name}': {length} x {width} x {height}"
            
            return [TextContent(type="text", text=result)]
            
        elif name == "create_cylinder":
            model_name = arguments["name"]
            radius = float(arguments["radius"])
            height = float(arguments["height"])
            
            builder = CADModelBuilder()
            model = builder.add_cylinder(radius, height).build()
            current_models[model_name] = model
            result = f"Created cylinder '{model_name}': r={radius}, h={height}"
            
            return [TextContent(type="text", text=result)]
            
        elif name == "create_flange":
            model_name = arguments["name"]
            outer_d = float(arguments["outer_diameter"])
            inner_d = float(arguments["inner_diameter"])
            thickness = float(arguments["thickness"])
            bolt_circle_d = float(arguments["bolt_circle_diameter"])
            bolt_hole_d = float(arguments["bolt_hole_diameter"])
            num_bolts = int(arguments.get("num_bolts", 6))
            
            # Validation
            if inner_d >= outer_d:
                return [TextContent(type="text", text="Error: Inner diameter must be less than outer diameter")]
            if bolt_circle_d >= outer_d:
                return [TextContent(type="text", text="Error: Bolt circle diameter must be less than outer diameter")]
                
            # Create flange
            print(f"Creating flange: OD={outer_d}, ID={inner_d}, thickness={thickness}")
            flange = (cq.Workplane("XY")
                     .circle(outer_d/2)
                     .circle(inner_d/2)  # Inner hole
                     .extrude(thickness)
                     .faces(">Z")  # Top face
                     .workplane()
                     .polarArray(bolt_circle_d/2, 0, 360, num_bolts)
                     .circle(bolt_hole_d/2)
                     .cutThruAll())
            
            current_models[model_name] = flange
            result = f"Created flange '{model_name}': OD={outer_d}, ID={inner_d}, thickness={thickness}, {num_bolts} bolt holes"
            
            return [TextContent(type="text", text=result)]
            
        elif name == "export_model":
            model_name = arguments["name"]
            export_format = arguments["format"].lower()
            filename = arguments.get("filename", f"{model_name}.{export_format}")
            
            if model_name not in current_models:
                return [TextContent(type="text", text=f"Error: Model '{model_name}' not found")]
                
            filepath = os.path.join(temp_dir, filename)
            model = current_models[model_name]
            
            print(f"Exporting {model_name} as {export_format} to {filepath}")
            
            success = False
            if export_format == "stl":
                success = CADExporter.export_stl(model, filepath)
            elif export_format == "step":
                success = CADExporter.export_step(model, filepath)
                
            if success:
                result = f"Exported '{model_name}' to {filepath}"
            else:
                result = f"Failed to export '{model_name}' as {export_format}"
                
            return [TextContent(type="text", text=result)]
            
        elif name == "list_models":
            if not current_models:
                return [TextContent(type="text", text="No models currently loaded")]
                
            model_list = []
            for name in current_models.keys():
                model_list.append(f"- {name}")
                
            result = f"Current models:\n" + "\n".join(model_list)
            return [TextContent(type="text", text=result)]
            
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
            
    except Exception as e:
        error_msg = f"Error executing {name}: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ {error_msg}")
        return [TextContent(type="text", text=error_msg)]

async def main():
    """Main server function with better error handling"""
    
    print("🚀 Starting CAD Geometry MCP Server...")
    print(f"Server name: cad-geometry-server")
    print(f"Version: 0.1.0")
    
    try:
        # Run the MCP server with simplified initialization
        async with stdio_server() as (read_stream, write_stream):
            print("📡 MCP server started successfully")
            
            # Simplified initialization - remove problematic imports
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="cad-geometry-server",
                    server_version="0.1.0",
                    capabilities=app.get_capabilities(),
                ),
            )
            
    except Exception as e:
        print(f"❌ Server error: {e}")
        print(traceback.format_exc())
        raise

if __name__ == "__main__":
    import asyncio
    
    print("=" * 60)
    print("🛠️  CAD Geometry MCP Server")
    print("   MCP + CadQuery + Design Patterns")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print(traceback.format_exc())