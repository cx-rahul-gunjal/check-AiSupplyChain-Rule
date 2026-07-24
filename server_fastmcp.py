#!/usr/bin/env python3
"""
MCP Server using FastMCP Framework - Lightweight and simple.
Demonstrates tools and resources with minimal boilerplate.
"""

from fastmcp import FastMCP

# Create FastMCP app instance
app = FastMCP("simple-mcp-fastmcp")


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
    return f"Hello, {name}! Welcome to the FastMCP Server."


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
    return "Hello! Welcome to the FastMCP Server.\n\nThis is a lightweight MCP implementation using FastMCP framework."


@app.resource("config://server")
def server_config() -> str:
    """Server configuration and metadata."""
    return """{
  "server_name": "Simple MCP FastMCP Server",
  "version": "2.0.0",
  "framework": "FastMCP",
  "description": "A lightweight MCP server using FastMCP framework",
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
    return """# Available Tools in FastMCP Server

## add(a: float, b: float)
Adds two numbers together and returns the result as a formatted string.

Example: add(5, 3) → "5 + 3 = 8"

## multiply(x: float, y: float)
Multiplies two numbers together and returns the result as a formatted string.

Example: multiply(4, 7) → "4 * 7 = 28"

## greet(name: str)
Greets someone by their name.

Example: greet("Alice") → "Hello, Alice! Welcome to the FastMCP Server."

## concatenate(text1: str, text2: str)
Concatenates two text strings together.

Example: concatenate("Hello", "World") → "'Hello' + 'World' = 'HelloWorld'"

## power(base: float, exponent: float)
Raises a number to a power (exponentiation).

Example: power(2, 3) → "2 ^ 3 = 8"
"""


@app.resource("docs://framework")
def framework_documentation() -> str:
    """Information about FastMCP framework."""
    return """# FastMCP Framework

FastMCP is a lightweight Python framework for building MCP servers with a simple, 
decorator-based API inspired by FastAPI.

## Key Features:

- **Decorator-based API**: Use @app.tool() and @app.resource() decorators
- **Minimal Boilerplate**: Simple and clean code
- **Automatic Schema Generation**: Infers schemas from function signatures
- **Built on Official SDK**: Leverages the official MCP protocol implementation
- **Pythonic**: Familiar patterns for Python developers

## Advantages:

1. Less verbose than official SDK
2. Similar to FastAPI (familiar to many Python developers)
3. Quick to prototype and develop
4. Automatic documentation generation
5. Built-in type hints support

## How It Works:

The @app.tool() decorator automatically:
- Registers the function as an MCP tool
- Generates input schema from function parameters
- Creates documentation from docstrings
- Handles async execution

Similarly, @app.resource(uri) decorators:
- Register resources with specific URIs
- Automatically handle resource listing and reading
"""


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Run the server (uses stdio transport by default)
    app.run()
