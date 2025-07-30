#!/usr/bin/env python3
"""
Test script for the code cleaning logic in GenX3D
This script tests how the system cleans LLM responses to extract valid Python code.
"""

def test_code_cleaning():
    """Test the code cleaning logic with various LLM responses"""
    print("🧪 Testing Code Cleaning Logic")
    print("=" * 40)
    
    # Test cases with different LLM response formats
    test_cases = [
        {
            "name": "Markdown with explanations",
            "input": """Here is the corrected Python code to generate a sphere using CADQuery:

```python
import cadquery as cq

# Create a sphere with radius 10
result = cq.Sphere(10)

# Export the result to STEP format
step_file_path = "sphere.step"
cq.exporters.export(result, step_file_path, exportType='STEP')
```

You can adjust the radius value to create a sphere of a different size.""",
            "expected_contains": ["import cadquery", "cq.Sphere", "cq.exporters.export"]
        },
        {
            "name": "Plain text with explanations",
            "input": """Here is the Python code to create a cylinder:

import cadquery as cq
result = cq.Workplane("XY").circle(5).extrude(10)
cq.exporters.export(result, step_file_path, exportType='STEP')

This will create a cylinder with radius 5 and height 10.""",
            "expected_contains": ["import cadquery", "cq.Workplane", "cq.exporters.export"]
        },
        {
            "name": "Mixed format with multiple explanations",
            "input": """The code below creates a simple cube:

import cadquery as cq
from cadquery import Workplane

# Create a cube
result = cq.Workplane("XY").box(10, 10, 10)

# Export to STEP
cq.exporters.export(result, step_file_path, exportType='STEP')

Note: You can modify the dimensions by changing the box parameters.
Example: box(5, 5, 5) creates a smaller cube.""",
            "expected_contains": ["import cadquery", "cq.Workplane", "cq.exporters.export"]
        },
        {
            "name": "Pure code (ideal case)",
            "input": """import cadquery as cq
from cadquery import Workplane

result = cq.Workplane("XY").sphere(5)
cq.exporters.export(result, step_file_path, exportType='STEP')""",
            "expected_contains": ["import cadquery", "cq.Workplane", "cq.exporters.export"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print(f"Input:\n{test_case['input']}")
        
        # Apply the same cleaning logic as in the code_gen_node
        generated_code = test_case['input'].strip()
        
        # Remove markdown code blocks
        if "```python" in generated_code:
            start_marker = "```python"
            end_marker = "```"
            start_idx = generated_code.find(start_marker)
            if start_idx != -1:
                start_idx += len(start_marker)
                end_idx = generated_code.find(end_marker, start_idx)
                if end_idx != -1:
                    generated_code = generated_code[start_idx:end_idx].strip()
                else:
                    generated_code = generated_code[start_idx:].strip()
        elif "```" in generated_code:
            start_marker = "```"
            end_marker = "```"
            start_idx = generated_code.find(start_marker)
            if start_idx != -1:
                start_idx += len(start_marker)
                end_idx = generated_code.find(end_marker, start_idx)
                if end_idx != -1:
                    generated_code = generated_code[start_idx:end_idx].strip()
                else:
                    generated_code = generated_code[start_idx:].strip()
        
        # Remove explanatory text
        lines = generated_code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip lines that are clearly explanatory text
            if (line.startswith("Here is") or 
                line.startswith("This code") or 
                line.startswith("The code") or
                line.startswith("You can") or
                line.startswith("To create") or
                line.startswith("This will") or
                line.startswith("The result") or
                line.startswith("Note:") or
                line.startswith("Example:") or
                line.startswith("Output:") or
                line.startswith("Result:") or
                line.startswith("Code:") or
                line.startswith("Python code:") or
                line.startswith("CADQuery code:")):
                continue
            
            # Keep lines that look like Python code
            if (line.startswith('import') or 
                line.startswith('from') or
                line.startswith('#') or
                line.startswith('result') or
                line.startswith('cq.') or
                line.startswith('step_file_path') or
                line.startswith('def ') or
                line.startswith('class ') or
                line.startswith('if ') or
                line.startswith('for ') or
                line.startswith('while ') or
                line.startswith('try:') or
                line.startswith('except:') or
                line.startswith('finally:') or
                line.startswith('with ') or
                line.startswith('return ') or
                line.startswith('print(') or
                line.startswith('assert ') or
                '=' in line or
                '(' in line or
                '[' in line or
                '{' in line or
                '.' in line):
                cleaned_lines.append(line)
        
        generated_code = '\n'.join(cleaned_lines)
        generated_code = generated_code.strip()
        
        print(f"\nCleaned output:\n{generated_code}")
        
        # Validate the result
        is_valid = True
        missing_elements = []
        
        for expected in test_case['expected_contains']:
            if expected not in generated_code:
                is_valid = False
                missing_elements.append(expected)
        
        if is_valid:
            print(f"✅ PASS - All expected elements found")
        else:
            print(f"❌ FAIL - Missing elements: {missing_elements}")
        
        # Check if it looks like valid Python code
        if not generated_code:
            print(f"❌ FAIL - No code extracted")
        elif not any(keyword in generated_code.lower() for keyword in ['import', 'cq.', 'result', 'step_file_path']):
            print(f"❌ FAIL - Doesn't look like valid CADQuery code")
        else:
            print(f"✅ PASS - Valid CADQuery code structure")

def main():
    """Main function"""
    print("🤖 GenX3D Code Cleaning Test")
    print("=" * 30)
    test_code_cleaning()

if __name__ == "__main__":
    main() 