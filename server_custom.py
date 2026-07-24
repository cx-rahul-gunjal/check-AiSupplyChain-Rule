#!/usr/bin/env python3
"""
MCP Server using a Custom Lightweight Wrapper.
This demonstrates building a minimal MCP server with custom abstractions.
"""

import json
import sys
import asyncio
from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


# ============================================================================
# CUSTOM LIGHTWEIGHT FRAMEWORK
# ============================================================================

@dataclass
class ToolInput:
    """Tool input schema."""
    type: str
    properties: Dict[str, Any]
    required: list


@dataclass
class ToolDefinition:
    """Tool definition for MCP."""
    name: str
    description: str
    inputSchema: ToolInput


class CustomMCPServer:
    """A minimal custom MCP server framework."""

    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, tuple[Callable, ToolDefinition]] = {}
        self.resources: Dict[str, str] = {}
        self.resource_metadata: Dict[str, Dict[str, str]] = {}

    def tool(self, **schema_props):
        """Decorator to register a tool."""
        def decorator(func: Callable):
            properties = {}
            required = []
            
            # Extract parameters from function
            import inspect
            sig = inspect.signature(func)
            for param_name, param in sig.parameters.items():
                annotation = param.annotation
                if annotation == float or annotation == int:
                    properties[param_name] = {
                        "type": "number" if annotation == float else "integer",
                        "description": f"Parameter {param_name}"
                    }
                elif annotation == str:
                    properties[param_name] = {
                        "type": "string",
                        "description": f"Parameter {param_name}"
                    }
                required.append(param_name)
            
            input_schema = ToolInput(
                type="object",
                properties=properties,
                required=required
            )
            
            tool_def = ToolDefinition(
                name=func.__name__,
                description=func.__doc__ or "",
                inputSchema=input_schema
            )
            
            self.tools[func.__name__] = (func, tool_def)
            return func
        
        return decorator

    def resource(self, uri: str, mime_type: str = "text/plain"):
        """Decorator to register a resource."""
        def decorator(func: Callable):
            self.resources[uri] = func
            self.resource_metadata[uri] = {
                "name": func.__name__.replace("_", " ").title(),
                "mimeType": mime_type,
                "description": func.__doc__ or ""
            }
            return func
        
        return decorator

    async def list_tools(self) -> list:
        """List all tools."""
        return [
            {
                "name": tool_def.name,
                "description": tool_def.description,
                "inputSchema": {
                    "type": tool_def.inputSchema.type,
                    "properties": tool_def.inputSchema.properties,
                    "required": tool_def.inputSchema.required
                }
            }
            for _, tool_def in self.tools.values()
        ]

    async def call_tool(self, name: str, arguments: dict) -> str:
        """Call a tool."""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        
        func, _ = self.tools[name]
        result = func(**arguments)
        
        # Handle async functions
        if asyncio.iscoroutine(result):
            result = await result
        
        return str(result)

    async def list_resources(self) -> list:
        """List all resources."""
        return [
            {
                "uri": uri,
                "name": metadata["name"],
                "mimeType": metadata["mimeType"],
                "description": metadata["description"]
            }
            for uri, metadata in self.resource_metadata.items()
        ]

    async def read_resource(self, uri: str) -> str:
        """Read a resource."""
        if uri not in self.resources:
            raise ValueError(f"Resource '{uri}' not found")
        
        func = self.resources[uri]
        result = func()
        
        # Handle async functions
        if asyncio.iscoroutine(result):
            result = await result
        
        return str(result)


class SimpleJSONRPCHandler:
    """Handle JSON-RPC requests for the custom server."""

    def __init__(self, server: CustomMCPServer):
        self.server = server
        self.request_id = 0

    async def handle_request(self, request: dict) -> dict:
        """Handle a JSON-RPC request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id", 0)

        try:
            if method == "tools/list":
                result = await self.server.list_tools()
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = await self.server.call_tool(tool_name, arguments)
            elif method == "resources/list":
                result = await self.server.list_resources()
            elif method == "resources/read":
                uri = params.get("uri")
                result = await self.server.read_resource(uri)
            else:
                raise ValueError(f"Unknown method: {method}")

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }


# ============================================================================
# MCP SERVER IMPLEMENTATION
# ============================================================================

server = CustomMCPServer("simple-mcp-custom")


# Tools
@server.tool()
def add(a: float, b: float) -> str:
    """Add two numbers together."""
    result = a + b
    return f"{a} + {b} = {result}"


@server.tool()
def multiply(x: float, y: float) -> str:
    """Multiply two numbers together."""
    result = x * y
    return f"{x} * {y} = {result}"


@server.tool()
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Welcome to the Custom MCP Server."


@server.tool()
def concatenate(text1: str, text2: str) -> str:
    """Concatenate two text strings."""
    result = text1 + text2
    return f"'{text1}' + '{text2}' = '{result}'"


@server.tool()
def divide(numerator: float, denominator: float) -> str:
    """Divide two numbers."""
    if denominator == 0:
        return "Error: Cannot divide by zero"
    result = numerator / denominator
    return f"{numerator} / {denominator} = {result}"


# Resources
@server.resource("greeting://welcome", "text/plain")
def greeting_welcome() -> str:
    """Welcome greeting message."""
    return "Hello! Welcome to the Custom MCP Server.\n\nThis is a minimal MCP implementation using a custom lightweight wrapper."


@server.resource("config://server", "application/json")
def server_config() -> str:
    """Server configuration."""
    return """{
  "server_name": "Simple MCP Custom Wrapper Server",
  "version": "2.0.0",
  "framework": "Custom Lightweight Wrapper",
  "description": "A minimal MCP server using a custom abstraction",
  "tools": {
    "add": "Add two numbers",
    "multiply": "Multiply two numbers",
    "greet": "Greet someone by name",
    "concatenate": "Concatenate two text strings",
    "divide": "Divide two numbers"
  },
  "resources": [
    "greeting://welcome",
    "config://server",
    "docs://implementation",
    "docs://framework"
  ]
}"""


@server.resource("docs://implementation", "text/markdown")
def implementation_docs() -> str:
    """Documentation about the custom implementation."""
    return """# Custom Lightweight MCP Implementation

This server demonstrates building an MCP server using a custom, minimal framework.

## Architecture:

1. **CustomMCPServer**: Core server class with tool and resource management
2. **SimpleJSONRPCHandler**: Protocol handler for JSON-RPC communication
3. **Decorators**: Simple @server.tool() and @server.resource() decorators

## Advantages:

- Minimal dependencies (only stdlib)
- Full control over protocol handling
- Easy to understand and modify
- No external framework overhead
- Suitable for learning and custom use cases

## How to Extend:

Simply add new functions with decorators:

```python
@server.tool()
def my_function(param: str) -> str:
    return f"Result: {param}"

@server.resource("custom://resource")
def my_resource() -> str:
    return "Resource content"
```
"""


@server.resource("docs://framework", "text/markdown")
def framework_docs() -> str:
    """Documentation about the framework."""
    return """# Custom Lightweight Framework

This custom framework provides:

## Core Features:

- **Minimal abstraction** over MCP protocol
- **Decorator-based registration** for tools and resources
- **Automatic schema generation** from function signatures
- **JSON-RPC handling** built-in
- **Type hint support** for parameters

## Protocol Details:

The server uses JSON-RPC 2.0 over stdio:

### Request Format:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

### Response Format:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [...]
}
```

## Methods Supported:

- `tools/list` - List all tools
- `tools/call` - Call a specific tool
- `resources/list` - List all resources
- `resources/read` - Read a specific resource
"""


# ============================================================================
# MAIN SERVER LOOP
# ============================================================================

async def main():
    """Main server loop."""
    handler = SimpleJSONRPCHandler(server)
    
    print("Custom MCP Server running on stdio...", file=sys.stderr)
    
    try:
        while True:
            # Read JSON-RPC request from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            try:
                request = json.loads(line.strip())
                response = await handler.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}", file=sys.stderr)
    
    except KeyboardInterrupt:
        print("Server shutting down...", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
