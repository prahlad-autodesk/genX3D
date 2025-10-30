#!/usr/bin/env python3
"""
CAD Agent Demo Client
Demonstrates the MCP CAD server by creating a flange and exporting it.
"""

import asyncio
import json
from typing import List, Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class CADAgentClient:
    """Client for interacting with the CAD Geometry MCP server"""
    
    def __init__(self):
        self.session = None
        
    async def connect(self, server_path: str):
        """Connect to the MCP server"""
        server_params = StdioServerParameters(
            command="python3",
            args=[server_path],
            env=None
        )
        
        self.session = await stdio_client(server_params).__aenter__()
        
        # Initialize the session
        await self.session.initialize()
        
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.session:
            await self.session.__aexit__(None, None, None)
            
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the MCP server"""
        if not self.session:
            raise RuntimeError("Not connected to server")
            
        result = await self.session.call_tool(name, arguments)
        
        # Extract text content from the result
        if result.content and len(result.content) > 0:
            return result.content[0].text
        return "No response"
        
    async def list_available_tools(self) -> List[str]:
        """Get list of available tools"""
        if not self.session:
            raise RuntimeError("Not connected to server")
            
        tools = await self.session.list_tools()
        return [tool.name for tool in tools.tools]

class FlangeGenerator:
    """Generates flanges with specified parameters"""
    
    def __init__(self, client: CADAgentClient):
        self.client = client
        
    async def create_standard_flange(self, name: str, specs: Dict[str, Any]) -> str:
        """Create a standard flange with given specifications"""
        
        # Validate specifications
        required_params = ['outer_diameter', 'inner_diameter', 'thickness', 
                          'bolt_circle_diameter', 'bolt_hole_diameter']
        
        for param in required_params:
            if param not in specs:
                raise ValueError(f"Missing required parameter: {param}")
                
        # Set defaults
        specs.setdefault('num_bolts', 6)
        
        # Create the flange
        arguments = {
            'name': name,
            **specs
        }
        
        result = await self.client.call_tool('create_flange', arguments)
        return result
        
    async def apply_finishing(self, name: str, fillet_radius: float = 2.0) -> str:
        """Apply finishing operations to the flange"""
        
        result = await self.client.call_tool('apply_fillet', {
            'name': name,
            'radius': fillet_radius
        })
        
        return result
        
    async def export_flange(self, name: str, formats: List[str] = None) -> List[str]:
        """Export flange in specified formats"""
        
        if formats is None:
            formats = ['stl', 'step']
            
        results = []
        for fmt in formats:
            result = await self.client.call_tool('export_model', {
                'name': name,
                'format': fmt
            })
            results.append(result)
            
        return results
        
    async def get_properties(self, name: str) -> Dict[str, Any]:
        """Get mass properties of the flange"""
        
        result = await self.client.call_tool('get_mass_properties', {
            'name': name
        })
        
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": result}

async def demo_basic_operations():
    """Demonstrate basic CAD operations"""
    
    print("🛠️  CAD Agent Demo - Basic Operations")
    print("=" * 50)
    
    client = CADAgentClient()
    
    try:
        # Connect to server
        print("📡 Connecting to CAD Geometry Server...")
        await client.connect("servers/cad_geometry_server.py")
        
        # List available tools
        print("\n🔧 Available Tools:")
        tools = await client.list_available_tools()
        for tool in tools:
            print(f"  - {tool}")
            
        print("\n" + "=" * 50)
        
        # Create basic shapes
        print("📦 Creating basic shapes...")
        
        # Create a box
        result = await client.call_tool('create_box', {
            'name': 'test_box',
            'length': 20,
            'width': 15,
            'height': 10
        })
        print(f"Box: {result}")
        
        # Create a cylinder  
        result = await client.call_tool('create_cylinder', {
            'name': 'test_cylinder',
            'radius': 5,
            'height': 25
        })
        print(f"Cylinder: {result}")
        
        # List models
        result = await client.call_tool('list_models', {})
        print(f"\nCurrent models:\n{result}")
        
        # Export models
        print("\n💾 Exporting models...")
        
        for model_name in ['test_box', 'test_cylinder']:
            result = await client.call_tool('export_model', {
                'name': model_name,
                'format': 'stl'
            })
            print(f"Export: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        await client.disconnect()

async def demo_flange_generation():
    """Demonstrate advanced flange generation"""
    
    print("\n🔩 CAD Agent Demo - Flange Generation")
    print("=" * 50)
    
    client = CADAgentClient()
    flange_gen = FlangeGenerator(client)
    
    try:
        # Connect to server
        await client.connect("servers/cad_geometry_server.py")
        
        # Define flange specifications
        flange_specs = {
            'outer_diameter': 100,     # 100mm outer diameter
            'inner_diameter': 40,      # 40mm bore
            'thickness': 12,           # 12mm thick
            'bolt_circle_diameter': 80, # 80mm bolt circle
            'bolt_hole_diameter': 8,   # 8mm bolt holes
            'num_bolts': 6            # 6 bolt holes
        }
        
        print("⚙️  Creating flange with specifications:")
        for key, value in flange_specs.items():
            print(f"   {key}: {value}")
            
        # Create the flange
        result = await flange_gen.create_standard_flange('demo_flange', flange_specs)
        print(f"\n✅ {result}")
        
        # Apply finishing
        print("\n🔄 Applying finishing operations...")
        result = await flange_gen.apply_finishing('demo_flange', fillet_radius=2.0)
        print(f"✅ {result}")
        
        # Get mass properties
        print("\n📊 Getting mass properties...")
        properties = await flange_gen.get_properties('demo_flange')
        
        if 'error' not in properties:
            print(f"   Volume: {properties['volume']:.2f} cubic units")
            dims = properties['bounding_box']['dimensions']
            print(f"   Dimensions: {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f}")
        else:
            print(f"   {properties['error']}")
        
        # Export in multiple formats
        print("\n💾 Exporting flange...")
        export_results = await flange_gen.export_flange('demo_flange', ['stl', 'step'])
        for result in export_results:
            print(f"✅ {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        await client.disconnect()

async def demo_batch_operations():
    """Demonstrate batch operations for multiple flanges"""
    
    print("\n🏭 CAD Agent Demo - Batch Operations")
    print("=" * 50)
    
    client = CADAgentClient()
    flange_gen = FlangeGenerator(client)
    
    # Define multiple flange sizes
    flange_series = [
        {
            'name': 'flange_DN25',
            'specs': {
                'outer_diameter': 85,
                'inner_diameter': 27,
                'thickness': 11,
                'bolt_circle_diameter': 65,
                'bolt_hole_diameter': 6,
                'num_bolts': 4
            }
        },
        {
            'name': 'flange_DN50',
            'specs': {
                'outer_diameter': 125,
                'inner_diameter': 53,
                'thickness': 14,
                'bolt_circle_diameter': 100,
                'bolt_hole_diameter': 8,
                'num_bolts': 4
            }
        },
        {
            'name': 'flange_DN100',
            'specs': {
                'outer_diameter': 190,
                'inner_diameter': 107,
                'thickness': 18,
                'bolt_circle_diameter': 160,
                'bolt_hole_diameter': 10,
                'num_bolts': 8
            }
        }
    ]
    
    try:
        await client.connect("servers/cad_geometry_server.py")
        
        print("🏭 Creating flange series...")
        
        for flange_data in flange_series:
            name = flange_data['name']
            specs = flange_data['specs']
            
            print(f"\n⚙️  Creating {name}...")
            
            # Create flange
            result = await flange_gen.create_standard_flange(name, specs)
            print(f"   ✅ {result}")
            
            # Apply finishing
            result = await flange_gen.apply_finishing(name, fillet_radius=1.5)
            print(f"   ✅ Finishing applied")
            
            # Export as STL
            export_results = await flange_gen.export_flange(name, ['stl'])
            print(f"   ✅ {export_results[0]}")
        
        # List all created models
        print("\n📋 Final model inventory:")
        result = await client.call_tool('list_models', {})
        print(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        await client.disconnect()

async def main():
    """Main demo function"""
    
    print("🚀 CAD Agent System Demo")
    print("Using MCP (Model Context Protocol) + CadQuery + LLM Architecture")
    print("=" * 70)
    
    # Run all demos
    await demo_basic_operations()
    await demo_flange_generation() 
    await demo_batch_operations()
    
    print("\n" + "=" * 70)
    print("✨ Demo completed! Check the output files in the temporary directory.")
    print("📁 Next steps:")
    print("   1. Run the web client for 3D visualization")
    print("   2. Add more CAD operations (chamfer, assembly, etc.)")
    print("   3. Integrate with LLM agents for natural language input")

if __name__ == "__main__":
    asyncio.run(main())