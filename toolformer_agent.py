"""
ToolFormer agent implementation.
Agent framework focused on learning and optimizing tool usage.
"""

from typing import Any, Dict, List, Callable
import json

class Tool:
    """Represents a tool that an agent can use."""
    
    def __init__(self, name: str, description: str, func: Callable, params: List[str]):
        self.name = name
        self.description = description
        self.func = func
        self.params = params
        self.usage_count = 0
        self.success_count = 0
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute the tool."""
        self.usage_count += 1
        try:
            result = self.func(*args, **kwargs)
            self.success_count += 1
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_effectiveness_score(self) -> float:
        """Calculate tool effectiveness score."""
        if self.usage_count == 0:
            return 0.0
        return self.success_count / self.usage_count

class ToolFormerAgent:
    """Agent that learns optimal tool usage patterns."""
    
    def __init__(self, name: str, model: str = "gpt-4"):
        self.name = name
        self.model = model
        self.tools: Dict[str, Tool] = {}
        self.tool_usage_history = []
        self.learned_tool_sequences = {}
    
    def register_tool(self, tool: Tool):
        """Register a tool with the agent."""
        self.tools[tool.name] = tool
    
    def execute_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """Execute a tool and track usage."""
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found"
        
        tool = self.tools[tool_name]
        result = tool.execute(*args, **kwargs)
        
        # Log tool usage
        self.tool_usage_history.append({
            "tool": tool_name,
            "args": args,
            "success": isinstance(result, str) and not result.startswith("Error")
        })
        
        return result
    
    def get_tool_effectiveness_rankings(self) -> List[Dict]:
        """Get tools ranked by effectiveness."""
        rankings = []
        for tool_name, tool in self.tools.items():
            rankings.append({
                "tool": tool_name,
                "description": tool.description,
                "usage_count": tool.usage_count,
                "success_count": tool.success_count,
                "effectiveness": tool.get_effectiveness_score()
            })
        
        # Sort by effectiveness
        rankings.sort(key=lambda x: x["effectiveness"], reverse=True)
        return rankings
    
    def learn_tool_sequence(self, sequence_name: str, tools: List[str]) -> bool:
        """Learn an optimal sequence of tools."""
        self.learned_tool_sequences[sequence_name] = {
            "sequence": tools,
            "learned_at": len(self.tool_usage_history),
            "usage_count": 0
        }
        return True
    
    def apply_tool_sequence(self, sequence_name: str) -> List[str]:
        """Apply a learned tool sequence."""
        if sequence_name not in self.learned_tool_sequences:
            return []
        
        sequence = self.learned_tool_sequences[sequence_name]["sequence"]
        self.learned_tool_sequences[sequence_name]["usage_count"] += 1
        return sequence
    
    def suggest_tool(self, task_description: str) -> str:
        """Suggest the best tool for a task based on learned patterns."""
        effectiveness_rankings = self.get_tool_effectiveness_rankings()
        if effectiveness_rankings:
            return effectiveness_rankings[0]["tool"]
        return "No tools available"
    
    def generate_tool_report(self) -> Dict:
        """Generate report on tool usage and learning."""
        return {
            "agent_name": self.name,
            "total_tools": len(self.tools),
            "tool_effectiveness": self.get_tool_effectiveness_rankings(),
            "total_executions": sum(tool.usage_count for tool in self.tools.values()),
            "total_successes": sum(tool.success_count for tool in self.tools.values()),
            "learned_sequences": len(self.learned_tool_sequences)
        }

# Tool implementations
def database_query(query: str) -> str:
    return f"Query results: {query}"

def api_call(endpoint: str, params: dict) -> str:
    return f"API response from {endpoint}"

def file_operation(filename: str, operation: str) -> str:
    return f"File operation {operation} on {filename}"

def data_processing(data: str) -> str:
    return f"Processed data: {len(data)} chars"

def run_toolformer_agent():
    """Run a ToolFormer agent with tool learning."""
    # Create agent
    agent = ToolFormerAgent(name="ToolFormerAgent", model="gpt-4")
    
    # Register tools
    agent.register_tool(Tool(
        name="database_query",
        description="Query the database",
        func=database_query,
        params=["query"]
    ))
    
    agent.register_tool(Tool(
        name="api_call",
        description="Make API calls",
        func=api_call,
        params=["endpoint", "params"]
    ))
    
    agent.register_tool(Tool(
        name="file_operation",
        description="Perform file operations",
        func=file_operation,
        params=["filename", "operation"]
    ))
    
    agent.register_tool(Tool(
        name="data_processing",
        description="Process data",
        func=data_processing,
        params=["data"]
    ))
    
    # Execute tools
    print("=== Tool Execution Phase ===")
    agent.execute_tool("database_query", "SELECT * FROM users")
    agent.execute_tool("api_call", "/users", {"limit": 10})
    agent.execute_tool("data_processing", "sample data")
    agent.execute_tool("file_operation", "data.csv", "read")
    
    # Learn sequences
    print("\n=== Learning Phase ===")
    agent.learn_tool_sequence("data_pipeline", ["database_query", "data_processing", "file_operation"])
    print("Learned: data_pipeline sequence")
    
    # Generate report
    print("\n=== Tool Effectiveness Report ===")
    report = agent.generate_tool_report()
    print(json.dumps(report, indent=2))
    
    # Get suggestions
    print("\n=== Tool Suggestions ===")
    suggested_tool = agent.suggest_tool("process some data")
    print(f"Suggested tool for 'process some data': {suggested_tool}")
    
    return report

if __name__ == "__main__":
    result = run_toolformer_agent()
