"""
MCP Server implementation using FastMCP with tools, resources, and external services.
Provides comprehensive set of tools and resources for AI agents to use.
"""

from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, List, Optional
import httpx
import asyncio
from datetime import datetime
import json
import os

# Initialize FastMCP server
mcp = FastMCP("AI-BOM-POC-Server", "1.0.0")


# ====================
# TOOL: Text Analysis
# ====================

@mcp.tool()
def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyze text and return detailed statistics.
    
    Args:
        text: The text to analyze
    
    Returns:
        Dictionary containing word count, character count, sentence count, etc.
    """
    words = text.split()
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    return {
        "character_count": len(text),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "unique_words": len(set(word.lower() for word in words)),
        "timestamp": datetime.now().isoformat()
    }


# ====================
# TOOL: Mathematical Operations
# ====================

@mcp.tool()
def calculate_sum(numbers: List[float]) -> float:
    """Calculate the sum of a list of numbers."""
    return sum(numbers)


@mcp.tool()
def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    return sum(numbers) / len(numbers) if numbers else 0


@mcp.tool()
def calculate_statistics(numbers: List[float]) -> Dict[str, float]:
    """Calculate comprehensive statistics for a list of numbers."""
    if not numbers:
        return {}
    
    sorted_nums = sorted(numbers)
    n = len(numbers)
    
    return {
        "sum": sum(numbers),
        "average": sum(numbers) / n,
        "min": min(numbers),
        "max": max(numbers),
        "median": sorted_nums[n // 2],
        "count": n,
        "std_dev": (sum((x - (sum(numbers) / n)) ** 2 for x in numbers) / n) ** 0.5
    }


# ====================
# TOOL: External API Calls
# ====================

@mcp.tool()
async def fetch_weather_data(city: str) -> Dict[str, Any]:
    """
    Fetch weather data for a given city from external API.
    
    Args:
        city: Name of the city
    
    Returns:
        Weather data including temperature, conditions, humidity, and wind
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.weatherapi.com/v1/current.json",
                params={"q": city, "key": "demo"},
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
    
    # Return simulated data for demo
    return {
        "location": {"name": city},
        "current": {
            "temp_c": 22.5,
            "condition": {"text": "Partly cloudy"},
            "humidity": 65,
            "wind_kph": 15.2
        },
        "simulated": True
    }


@mcp.tool()
async def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for information.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of search results with title, URL, and snippet
    """
    await asyncio.sleep(0.2)  # Simulate API delay
    return [
        {
            "title": f"Result {i+1}: {query}",
            "url": f"https://example.com/result{i+1}",
            "snippet": f"Relevant information about {query}...",
            "rank": i+1
        }
        for i in range(max_results)
    ]


@mcp.tool()
async def call_external_api(
    endpoint: str, 
    method: str = "GET", 
    data: Optional[Dict] = None,
    headers: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Make calls to external APIs.
    
    Args:
        endpoint: Full API endpoint URL
        method: HTTP method (GET, POST, PUT, DELETE)
        data: JSON data for POST/PUT requests
        headers: Custom HTTP headers
    
    Returns:
        API response with status code and data
    """
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(endpoint, headers=headers, timeout=10.0)
            elif method.upper() == "POST":
                response = await client.post(endpoint, json=data, headers=headers, timeout=10.0)
            elif method.upper() == "PUT":
                response = await client.put(endpoint, json=data, headers=headers, timeout=10.0)
            elif method.upper() == "DELETE":
                response = await client.delete(endpoint, headers=headers, timeout=10.0)
            else:
                return {"error": f"Unsupported method: {method}", "success": False}
            
            is_json = "application/json" in response.headers.get("content-type", "")
            
            return {
                "status_code": response.status_code,
                "data": response.json() if is_json else response.text,
                "success": response.status_code < 400,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "success": False}


# ====================
# TOOL: Data Processing
# ====================

@mcp.tool()
def process_data(data: Dict[str, Any], operation: str) -> Dict[str, Any]:
    """
    Process data with specified operation.
    
    Args:
        data: Dictionary to process
        operation: Operation type (transform, filter, aggregate, sort)
    
    Returns:
        Processed data based on operation
    """
    operations = {
        "transform": lambda d: {k: str(v).upper() if isinstance(v, str) else v for k, v in d.items()},
        "filter": lambda d: {k: v for k, v in d.items() if v is not None},
        "aggregate": lambda d: {
            "count": len(d), 
            "keys": list(d.keys()), 
            "has_values": bool(d),
            "total_items": sum(1 for _ in d.items())
        },
        "sort": lambda d: dict(sorted(d.items()))
    }
    
    if operation in operations:
        try:
            result = operations[operation](data)
            result["operation"] = operation
            result["success"] = True
            return result
        except Exception as e:
            return {"error": str(e), "success": False}
    else:
        return {"error": f"Unknown operation: {operation}", "success": False}


@mcp.tool()
def filter_data(
    data: List[Dict[str, Any]], 
    field: str, 
    value: Any
) -> List[Dict[str, Any]]:
    """
    Filter a list of dictionaries by field and value.
    
    Args:
        data: List of dictionaries
        field: Field name to filter by
        value: Value to match
    
    Returns:
        Filtered list of dictionaries
    """
    return [item for item in data if item.get(field) == value]


@mcp.tool()
def transform_data(
    data: List[Dict[str, Any]], 
    mapping: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Transform data by mapping fields.
    
    Args:
        data: List of dictionaries
        mapping: Field mapping dictionary
    
    Returns:
        Transformed list of dictionaries
    """
    result = []
    for item in data:
        new_item = {}
        for old_key, new_key in mapping.items():
            if old_key in item:
                new_item[new_key] = item[old_key]
        result.append(new_item)
    return result


# ====================
# RESOURCES
# ====================

@mcp.resource("config://system")
def get_system_config() -> str:
    """Return system configuration as a resource."""
    config = {
        "server_name": "AI-BOM-POC-Server",
        "version": "1.0.0",
        "capabilities": ["tools", "resources", "external_apis"],
        "max_connections": 100,
        "timeout": 30,
        "features": {
            "text_analysis": True,
            "weather_lookup": True,
            "web_search": True,
            "data_processing": True,
            "api_calls": True,
            "math_operations": True
        }
    }
    return json.dumps(config, indent=2)


@mcp.resource("data://sample/{dataset_name}")
def get_sample_data(dataset_name: str) -> str:
    """Return sample datasets as resources."""
    datasets = {
        "users": [
            {"id": 1, "name": "Alice", "role": "Engineer", "active": True, "department": "Engineering"},
            {"id": 2, "name": "Bob", "role": "Designer", "active": True, "department": "Design"},
            {"id": 3, "name": "Charlie", "role": "Manager", "active": False, "department": "Management"}
        ],
        "products": [
            {"id": 101, "name": "Widget A", "price": 29.99, "stock": 150, "category": "Electronics"},
            {"id": 102, "name": "Widget B", "price": 49.99, "stock": 75, "category": "Electronics"},
            {"id": 103, "name": "Widget C", "price": 19.99, "stock": 200, "category": "Accessories"}
        ],
        "metrics": {
            "daily_active_users": 1250,
            "conversion_rate": 0.034,
            "average_session_time": 420,
            "bounce_rate": 0.42,
            "revenue": 15420.50
        }
    }
    
    data = datasets.get(dataset_name, {"error": f"Dataset '{dataset_name}' not found"})
    return json.dumps(data, indent=2)


@mcp.resource("docs://api/{endpoint}")
def get_api_documentation(endpoint: str) -> str:
    """Return API documentation as resources."""
    docs = {
        "weather": """
Weather API Endpoint
====================
Fetches current weather data for a given city.

Parameters:
- city (str): City name

Returns: Weather data including temperature, conditions, humidity, and wind.
Example: fetch_weather_data('London')
        """,
        "search": """
Search API Endpoint
===================
Performs web search and returns relevant results.

Parameters:
- query (str): Search query
- max_results (int): Maximum number of results (default: 5)

Returns: List of search results with title, URL, and snippet.
Example: search_web('artificial intelligence', max_results=10)
        """,
        "process": """
Data Processing Endpoint
========================
Processes data with specified operations.

Parameters:
- data (dict): Data to process
- operation (str): Operation type (transform, filter, aggregate, sort)

Returns: Processed data based on operation.
Example: process_data({'name': 'test'}, 'aggregate')
        """
    }
    
    doc = docs.get(endpoint, f"No documentation found for endpoint: {endpoint}")
    return doc


@mcp.resource("stats://server")
def get_server_stats() -> str:
    """Return server statistics as a resource."""
    stats = {
        "uptime": "24h 35m",
        "requests_served": 15420,
        "active_connections": 12,
        "cache_hit_rate": 0.87,
        "average_response_time_ms": 145,
        "timestamp": datetime.now().isoformat()
    }
    return json.dumps(stats, indent=2)


# ====================
# PROMPTS
# ====================

@mcp.prompt()
def analysis_prompt(topic: str) -> str:
    """Generate a prompt for analyzing a topic."""
    return f"""You are an expert analyst. Please analyze the following topic in detail:

Topic: {topic}

Provide:
1. Overview and context
2. Key components and their relationships
3. Potential challenges and opportunities
4. Recommendations for next steps

Be thorough and data-driven in your analysis."""


@mcp.prompt()
def research_prompt(question: str, context: str = "") -> str:
    """Generate a prompt for research tasks."""
    base = f"""You are a research assistant. Please investigate the following question:

Question: {question}
"""
    if context:
        base += f"\nAdditional Context: {context}\n"
    
    base += """
Please provide:
1. Direct answer to the question
2. Supporting evidence and sources
3. Related considerations
4. Confidence level in the answer
"""
    return base


@mcp.prompt()
def coding_prompt(task: str, language: str = "python") -> str:
    """Generate a prompt for coding tasks."""
    return f"""You are an expert {language} programmer. Complete the following task:

Task: {task}

Requirements:
1. Write clean, well-documented code
2. Follow {language} best practices
3. Include error handling
4. Add type hints where applicable
5. Provide example usage
"""


if __name__ == "__main__":
    mcp.run()
