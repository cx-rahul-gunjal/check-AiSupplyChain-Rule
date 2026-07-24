"""
MCP Clients implementation using stdio_client to connect to various MCP servers.
Provides high-level interfaces for different service domains.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

# Note: Import statements would be:
# from mcp.client.stdio import stdio_client
# from mcp import ClientSession
# These would be imported when the module is used


class MCPClientManager:
    """Manager for multiple MCP client connections."""
    
    def __init__(self):
        self.clients: Dict[str, Any] = {}
        self.sessions: Dict[str, Any] = {}
    
    @asynccontextmanager
    async def create_client(
        self, 
        name: str, 
        command: str, 
        args: List[str], 
        env: Optional[Dict] = None
    ):
        """
        Create and manage an MCP client connection.
        
        Args:
            name: Client name/identifier
            command: Command to run the MCP server
            args: Arguments for the command
            env: Environment variables
        """
        try:
            # Import here to avoid hard dependencies
            from mcp.client.stdio import stdio_client
            from mcp import ClientSession
            
            async with stdio_client(command, args, env=env) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    self.clients[name] = session
                    self.sessions[name] = {"read": read, "write": write}
                    
                    print(f"✓ Connected to MCP server: {name}")
                    yield session
        except Exception as e:
            print(f"✗ Failed to connect to {name}: {e}")
            raise
        finally:
            if name in self.clients:
                del self.clients[name]
            if name in self.sessions:
                del self.sessions[name]
            print(f"✓ Disconnected from MCP server: {name}")


class WeatherMCPClient:
    """Client for weather-related MCP services."""
    
    def __init__(self, manager: MCPClientManager):
        self.manager = manager
        self.client_name = "weather_service"
    
    async def get_weather(self, city: str) -> Dict[str, Any]:
        """Get weather data for a city."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            # List available tools
            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            print(f"Available tools: {tool_names}")
            
            # Call the fetch_weather_data tool
            result = await session.call_tool("fetch_weather_data", {"city": city})
            if result.content:
                return json.loads(result.content[0].text)
            return {}
    
    async def get_weather_batch(self, cities: List[str]) -> Dict[str, Any]:
        """Get weather data for multiple cities."""
        results = {}
        for city in cities:
            try:
                results[city] = await self.get_weather(city)
            except Exception as e:
                results[city] = {"error": str(e)}
        return results


class DataProcessingMCPClient:
    """Client for data processing MCP services."""
    
    def __init__(self, manager: MCPClientManager):
        self.manager = manager
        self.client_name = "data_service"
    
    async def process_data(self, data: Dict[str, Any], operation: str) -> Dict[str, Any]:
        """Process data using MCP server tools."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.call_tool("process_data", {
                "data": data,
                "operation": operation
            })
            if result.content:
                return json.loads(result.content[0].text)
            return {}
    
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text using MCP server tools."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.call_tool("analyze_text", {"text": text})
            if result.content:
                return json.loads(result.content[0].text)
            return {}
    
    async def filter_data(
        self,
        data: List[Dict[str, Any]],
        field: str,
        value: Any
    ) -> List[Dict[str, Any]]:
        """Filter data using MCP server tools."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.call_tool("filter_data", {
                "data": data,
                "field": field,
                "value": value
            })
            if result.content:
                return json.loads(result.content[0].text)
            return []


class SearchMCPClient:
    """Client for search-related MCP services."""
    
    def __init__(self, manager: MCPClientManager):
        self.manager = manager
        self.client_name = "search_service"
    
    async def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Perform web search using MCP server."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.call_tool("search_web", {
                "query": query,
                "max_results": max_results
            })
            if result.content:
                return json.loads(result.content[0].text)
            return []


class CalculationMCPClient:
    """Client for mathematical calculation services."""
    
    def __init__(self, manager: MCPClientManager):
        self.manager = manager
        self.client_name = "calculation_service"
    
    async def calculate_sum(self, numbers: List[float]) -> float:
        """Calculate sum of numbers."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.call_tool("calculate_sum", {"numbers": numbers})
            if result.content:
                return float(result.content[0].text)
            return 0.0
    
    async def calculate_statistics(self, numbers: List[float]) -> Dict[str, float]:
        """Calculate statistics for numbers."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.call_tool("calculate_statistics", {"numbers": numbers})
            if result.content:
                return json.loads(result.content[0].text)
            return {}


class ResourceMCPClient:
    """Client for accessing MCP server resources."""
    
    def __init__(self, manager: MCPClientManager):
        self.manager = manager
        self.client_name = "resource_service"
    
    async def get_system_config(self) -> Dict[str, Any]:
        """Get system configuration from MCP server resources."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            resources = await session.list_resources()
            resource_uris = [res.uri for res in resources.resources]
            print(f"Available resources: {resource_uris}")
            
            result = await session.read_resource("config://system")
            if result.contents:
                return json.loads(result.contents[0].text)
            return {}
    
    async def get_sample_data(self, dataset_name: str) -> Any:
        """Get sample data from MCP server resources."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.read_resource(f"data://sample/{dataset_name}")
            if result.contents:
                return json.loads(result.contents[0].text)
            return {}
    
    async def get_api_docs(self, endpoint: str) -> str:
        """Get API documentation from MCP server resources."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.read_resource(f"docs://api/{endpoint}")
            if result.contents:
                return result.contents[0].text
            return ""
    
    async def get_server_stats(self) -> Dict[str, Any]:
        """Get server statistics from MCP server resources."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.read_resource("stats://server")
            if result.contents:
                return json.loads(result.contents[0].text)
            return {}


class APICallMCPClient:
    """Client for making external API calls through MCP server."""
    
    def __init__(self, manager: MCPClientManager):
        self.manager = manager
        self.client_name = "api_service"
    
    async def call_api(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Call external API through MCP server."""
        async with self.manager.create_client(
            self.client_name,
            "python",
            ["-m", "mcp_server"]
        ) as session:
            result = await session.call_tool("call_external_api", {
                "endpoint": endpoint,
                "method": method,
                "data": data,
                "headers": headers
            })
            if result.content:
                return json.loads(result.content[0].text)
            return {}


class UnifiedMCPClient:
    """Unified client providing access to all MCP services."""
    
    def __init__(self):
        self.manager = MCPClientManager()
        self.weather = WeatherMCPClient(self.manager)
        self.data = DataProcessingMCPClient(self.manager)
        self.search = SearchMCPClient(self.manager)
        self.calculate = CalculationMCPClient(self.manager)
        self.resources = ResourceMCPClient(self.manager)
        self.api = APICallMCPClient(self.manager)
    
    async def execute_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a complex workflow using multiple MCP services."""
        results = {}
        
        try:
            # Search workflow
            if "search_query" in workflow_config:
                search_results = await self.search.search_web(
                    workflow_config["search_query"],
                    workflow_config.get("max_results", 3)
                )
                results["search"] = search_results
            
            # Text analysis workflow
            if "text_to_analyze" in workflow_config:
                analysis = await self.data.analyze_text(
                    workflow_config["text_to_analyze"]
                )
                results["analysis"] = analysis
            
            # Weather workflow
            if "cities" in workflow_config:
                weather_data = await self.weather.get_weather_batch(
                    workflow_config["cities"]
                )
                results["weather"] = weather_data
            
            # Data processing workflow
            if "data_to_process" in workflow_config:
                processed = await self.data.process_data(
                    workflow_config["data_to_process"],
                    workflow_config.get("operation", "aggregate")
                )
                results["processed"] = processed
            
            # Calculation workflow
            if "numbers_to_calculate" in workflow_config:
                stats = await self.calculate.calculate_statistics(
                    workflow_config["numbers_to_calculate"]
                )
                results["statistics"] = stats
            
            results["status"] = "success"
            results["timestamp"] = str(asyncio.get_event_loop().time())
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
        
        return results


# Demo functions for testing

async def demo_unified_client():
    """Demonstrate unified client with complex workflow."""
    client = UnifiedMCPClient()
    
    print("\n=== Unified MCP Client Demo ===\n")
    
    workflow_config = {
        "search_query": "artificial intelligence trends 2024",
        "max_results": 3,
        "text_to_analyze": "AI and machine learning are transforming industries globally.",
        "cities": ["London", "Tokyo", "New York"],
        "data_to_process": {"category": "tech", "year": 2024, "region": "APAC"},
        "operation": "transform",
        "numbers_to_calculate": [10, 20, 30, 40, 50, 60, 70, 80, 90]
    }
    
    results = await client.execute_workflow(workflow_config)
    print(f"Workflow Results:\n{json.dumps(results, indent=2)}")


if __name__ == "__main__":
    asyncio.run(demo_unified_client())
