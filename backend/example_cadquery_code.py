#!/usr/bin/env python3
"""
Example CADQuery code snippets for testing RAG functionality
"""

def create_cuboid():
    """Create a simple cuboid"""
    # Create a cuboid
    result = cq.Workplane("XY").box(10, 5, 3)
    
    # Export to STEP file
    cq.exporters.export(result, step_file_path, exportType='STEP')
    return result

def create_cylinder():
    """Create a simple cylinder"""
    # Create a cylinder
    result = cq.Workplane("XY").circle(5).extrude(10)
    
    # Export to STEP file
    cq.exporters.export(result, step_file_path, exportType='STEP')
    return result

def create_sphere():
    """Create a simple sphere"""
    # Create a sphere
    result = cq.Workplane("XY").sphere(5)
    
    # Export to STEP file
    cq.exporters.export(result, step_file_path, exportType='STEP')
    return result

def create_cube():
    """Create a simple cube"""
    # Create a cube
    result = cq.Workplane("XY").box(8, 8, 8)
    
    # Export to STEP file
    cq.exporters.export(result, step_file_path, exportType='STEP')
    return result

def create_hollow_cylinder():
    """Create a hollow cylinder"""
    # Create outer cylinder
    outer = cq.Workplane("XY").circle(8).extrude(12)
    # Create inner cylinder
    inner = cq.Workplane("XY").circle(4).extrude(12)
    # Cut inner from outer
    result = outer.cut(inner)
    
    # Export to STEP file
    cq.exporters.export(result, step_file_path, exportType='STEP')
    return result

# Example usage:
if __name__ == "__main__":
    import cadquery as cq
    from cadquery import exporters
    
    # Test creating a cuboid
    print("Creating cuboid...")
    create_cuboid()
    print("Cuboid created successfully!") 