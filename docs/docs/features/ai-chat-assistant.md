---
sidebar_position: 2
---

# AI Chat Assistant

The AI Chat Assistant in genx3D provides intelligent assistance for 3D modeling tasks using advanced language models.

## Overview

The AI assistant helps you with:

- **Code Generation**: Convert natural language descriptions to CAD code
- **Design Guidance**: Get suggestions for improving your models
- **Troubleshooting**: Debug issues with your CAD code
- **Learning**: Understand modeling concepts and techniques

## Getting Started

### Accessing the Assistant

1. Open the genx3D application
2. Click on the chat icon in the interface
3. Start typing your questions or requests

### Basic Usage

Ask the assistant to help you with modeling tasks:

```
User: "Create a simple cube with 20mm sides"
AI: Generates JavaScript code for a 20mm cube
```

## Common Use Cases

### Code Generation

Generate CAD code from descriptions:

```
User: "Make a gear with 16 teeth and 40mm diameter"
AI: function createGear(teeth, radius, thickness) {
  // Generated gear code...
}
```

### Design Modifications

Modify existing models:

```
User: "Add a hole in the center of my cube"
AI: var hole = CSG.cylinder({...});
    var result = cube.subtract(hole);
```

### Troubleshooting

Get help with errors:

```
User: "My model isn't showing up, what's wrong?"
AI: Checks your code and suggests fixes
```

## Advanced Features

### Context Awareness

The assistant remembers your current model and can reference it:

```
User: "Make the gear teeth longer"
AI: Modifies the existing gear code to increase tooth length
```

### Parameter Suggestions

Get recommendations for design parameters:

```
User: "What's a good wall thickness for 3D printing?"
AI: Provides guidelines based on material and print settings
```

### Optimization Tips

Improve your models:

```
User: "How can I make this print faster?"
AI: Suggests optimizations like reducing complexity or adjusting settings
```

## Best Practices

### Writing Good Prompts

- **Be Specific**: "Create a gear with 20 teeth" vs "Make a gear"
- **Include Dimensions**: Specify sizes when relevant
- **Mention Constraints**: "Must be 3D printable" or "For injection molding"

### Iterative Design

- Start with simple requests
- Build complexity gradually
- Ask for modifications to existing code

### Learning from Responses

- Study the generated code
- Ask for explanations of complex parts
- Request alternative approaches

## Examples

### Simple Shapes

```
User: "Create a cylinder with 10mm radius and 30mm height"
AI: var cylinder = CSG.cylinder({
  start: [0, 0, 0],
  end: [0, 0, 30],
  radius: 10
});
```

### Complex Assemblies

```
User: "Design a simple bearing with inner and outer races"
AI: function createBearing(innerRadius, outerRadius, height) {
  var outer = CSG.cylinder({...});
  var inner = CSG.cylinder({...});
  return outer.subtract(inner);
}
```

### Parametric Designs

```
User: "Make a parametric box that can be customized"
AI: function createBox(width, height, depth, wallThickness) {
  // Parametric box code...
}
```

## Integration with Modeling

### Seamless Workflow

1. **Design**: Use the assistant to generate initial code
2. **Modify**: Ask for adjustments and improvements
3. **Optimize**: Get suggestions for better performance
4. **Export**: Generate code for file export

### Real-time Assistance

- Get help while modeling
- Ask questions about techniques
- Learn new approaches

## Configuration

### Model Selection

Choose different AI models in your configuration:

```env
# Use GPT-4 for complex tasks
AI_MODEL=gpt-4o

# Use GPT-4o Mini for faster responses
AI_MODEL=gpt-4o-mini

# Use Claude for alternative perspective
AI_MODEL=anthropic/claude-3.5-sonnet
```

### Response Settings

Adjust AI behavior:

```env
# More creative responses
AI_TEMPERATURE=0.9

# More focused responses
AI_TEMPERATURE=0.3

# Longer responses
AI_MAX_TOKENS=4000
```

## Troubleshooting

### Common Issues

**Assistant not responding**
- Check your API key configuration
- Verify internet connection
- Restart the application

**Incorrect code generation**
- Be more specific in your request
- Provide context about your current model
- Ask for clarification

**Slow responses**
- Use a faster AI model
- Simplify your requests
- Check your network connection

## Tips and Tricks

### Efficient Communication

- Use clear, concise language
- Reference existing code when relevant
- Ask for step-by-step explanations

### Learning Strategy

- Start with simple requests
- Gradually increase complexity
- Study generated code patterns
- Ask for explanations of techniques

### Advanced Usage

- Combine multiple requests
- Ask for design alternatives
- Request optimization suggestions
- Get manufacturing advice

## Next Steps

- [Model Generation](./model-generation) - Learn about automated model generation
- [Model Analysis](./model-analysis) - Analyze your models for manufacturing
- [API Reference](../api/chat) - Integrate AI features into your applications
- [Tutorials](../tutorials/ai-assistant-usage) - Step-by-step AI assistant tutorials 