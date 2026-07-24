#!/usr/bin/env python3
"""
MCP Server using FastMCP Framework with SSE Transport
Exposes HTTP endpoint instead of stdio for remote connections.
"""

from fastmcp import FastMCP

# Create FastMCP app instance
app = FastMCP("simple-mcp-fastmcp-sse")


# ============================================================================
# TOOLS - Decorated functions automatically converted to MCP tools
# ============================================================================

@app.tool()
def add(a: float, b: float) -> str:
    """Add two numbers together."""
    result = a + b
    return f"{a} + {b} = {result}"


@app.tool()
def multiply(x: float, y: float) -> str:
    """Multiply two numbers together."""
    result = x * y
    return f"{x} * {y} = {result}"


@app.tool()
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! Welcome to the FastMCP SSE Server."


@app.tool()
def concatenate(text1: str, text2: str) -> str:
    """Concatenate two text strings."""
    result = text1 + text2
    return f"'{text1}' + '{text2}' = '{result}'"


@app.tool()
def power(base: float, exponent: float) -> str:
    """Raise a number to a power."""
    result = base ** exponent
    return f"{base} ^ {exponent} = {result}"


# ============================================================================
# RESOURCES - Static data accessible via URI
# ============================================================================

@app.resource("greeting://welcome")
def greeting_welcome() -> str:
    """Welcome greeting message."""
    return "Hello! Welcome to the FastMCP SSE Server.\n\nThis server uses HTTP/SSE transport instead of stdio."


@app.resource("config://server")
def server_config() -> str:
    """Server configuration and metadata."""
    return """{
  "server_name": "Simple MCP FastMCP SSE Server",
  "version": "2.0.0",
  "framework": "FastMCP",
  "transport": "SSE (Server-Sent Events over HTTP)",
  "description": "A lightweight MCP server using FastMCP framework with SSE transport",
  "tools": {
    "add": "Add two numbers",
    "multiply": "Multiply two numbers",
    "greet": "Greet someone by name",
    "concatenate": "Concatenate two text strings",
    "power": "Raise a number to a power"
  },
  "resources": [
    "greeting://welcome",
    "config://server",
    "docs://tools",
    "docs://framework"
  ]
}"""


@app.resource("docs://tools")
def tools_documentation() -> str:
    """Documentation of all available tools."""
    return """
# Available Tools

## add(a: float, b: float) -> str
Add two numbers together.

## multiply(x: float, y: float) -> str
Multiply two numbers together.

## greet(name: str) -> str
Greet someone by name.

## concatenate(text1: str, text2: str) -> str
Concatenate two text strings.

## power(base: float, exponent: float) -> str
Raise a number to a power.
"""


@app.resource("docs://framework")
def framework_documentation() -> str:
    """Information about FastMCP framework."""
    return """
# FastMCP Framework

FastMCP is a lightweight Python framework for building Model Context Protocol servers.

## Key Features:
- Simple decorator-based API (@app.tool(), @app.resource())
- Automatic schema generation from Python types
- Built on top of the official MCP SDK
- Support for both stdio and SSE transports
- Minimal boilerplate code

## Transport Options:
- stdio: For local subprocess communication
- SSE: For HTTP-based remote connections

This server uses SSE transport for web-based clients.
"""


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Run the server with SSE transport on HTTP endpoint
    # Default: http://localhost:8000/sse
    app.run(transport="sse")
    
    # You can customize the port:
    # app.run(transport="sse", port=8080)
    
    # Or specify host and port:
    # app.run(transport="sse", host="0.0.0.0", port=8000)
