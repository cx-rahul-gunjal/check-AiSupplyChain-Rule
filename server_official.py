#!/usr/bin/env python3
"""
MCP Server using the Official MCP Python SDK.
This is the comprehensive, production-grade implementation.
"""

import asyncio
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
import mcp.types as types

# Create server instance
server = Server("simple-mcp-official")


# ============================================================================
# TOOLS - Async functions with automatic schema generation
# ============================================================================

@server.call_tool()
async def add(a: float, b: float) -> str:
    """Add two numbers together."""
    result = a + b
    return f"{a} + {b} = {result}"


@server.call_tool()
async def multiply(x: float, y: float) -> str:
    """Multiply two numbers together."""
    result = x * y
    return f"{x} * {y} = {result}"


@server.call_tool()
async def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Welcome to the Official SDK Server."


@server.call_tool()
async def concatenate(text1: str, text2: str) -> str:
    """Concatenate two text strings."""
    result = text1 + text2
    return f"'{text1}' + '{text2}' = '{result}'"


@server.call_tool()
async def subtract(a: float, b: float) -> str:
    """Subtract two numbers."""
    result = a - b
    return f"{a} - {b} = {result}"


# ============================================================================
# RESOURCES - Static data with metadata
# ============================================================================

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available resources."""
    return [
        types.Resource(
            uri="greeting://welcome",
            name="Greeting Message",
            mimeType="text/plain",
            description="A simple welcome message"
        ),
        types.Resource(
            uri="config://server",
            name="Server Configuration",
            mimeType="application/json",
            description="Server configuration and metadata"
        ),
        types.Resource(
            uri="docs://tools",
            name="Available Tools Documentation",
            mimeType="text/markdown",
            description="Documentation of all available tools"
        ),
        types.Resource(
            uri="docs://framework",
            name="Official SDK Information",
            mimeType="text/markdown",
            description="Information about the Official MCP SDK"
        ),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI."""
    if uri == "greeting://welcome":
        return "Hello! Welcome to the Official MCP SDK Server.\n\nThis is a comprehensive MCP implementation using the official Python SDK."
    
    elif uri == "config://server":
        return """{
  "server_name": "Simple MCP Official SDK Server",
  "version": "2.0.0",
  "framework": "Official MCP Python SDK",
  "description": "A comprehensive MCP server using the official SDK",
  "tools": {
    "add": "Add two numbers",
    "multiply": "Multiply two numbers",
    "greet": "Greet someone by name",
    "concatenate": "Concatenate two text strings",
    "subtract": "Subtract two numbers"
  },
  "resources": [
    "greeting://welcome",
    "config://server",
    "docs://tools",
    "docs://framework"
  ]
}"""
    
    elif uri == "docs://tools":
        return """# Available Tools - Official SDK Server

## add(a: float, b: float)
Adds two numbers together and returns the result as a formatted string.

Example: add(5, 3) → "5 + 3 = 8"

## multiply(x: float, y: float)
Multiplies two numbers together and returns the result as a formatted string.

Example: multiply(4, 7) → "4 * 7 = 28"

## greet(name: str)
Greets someone by their name.

Example: greet("Bob") → "Hello, Bob! Welcome to the Official SDK Server."

## concatenate(text1: str, text2: str)
Concatenates two text strings together.

Example: concatenate("Hello", "World") → "'Hello' + 'World' = 'HelloWorld'"

## subtract(a: float, b: float)
Subtracts one number from another.

Example: subtract(10, 3) → "10 - 3 = 7"
"""
    
    elif uri == "docs://framework":
        return """# Official MCP Python SDK

The Official MCP Python SDK is the comprehensive, production-grade framework 
for building MCP servers.

## Key Features:

- **Async/await support**: Full async Python integration
- **Type hints**: Complete type annotation support
- **Protocol compliance**: Full MCP specification compliance
- **Error handling**: Comprehensive error handling
- **Extensible**: Designed for complex use cases

## Advantages:

1. Official specification compliance
2. Best for production systems
3. Comprehensive documentation
4. Full protocol control
5. Enterprise-grade stability

## How It Works:

The @server.call_tool() decorator:
- Registers async functions as tools
- Generates schema from type hints
- Handles async execution
- Provides full protocol control

The @server.list_resources() and @server.read_resource() decorators:
- Define resource listing behavior
- Handle resource retrieval
- Support URI-based addressing
- Include metadata (name, MIME type, etc.)

## When to Use:

- Production MCP servers
- Complex use cases requiring full control
- Systems requiring high reliability
- Large-scale deployments
"""
    
    else:
        raise ValueError(f"Resource not found: {uri}")


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Start the MCP server."""
    async with server:
        print("Official MCP Server running on stdio...")
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
