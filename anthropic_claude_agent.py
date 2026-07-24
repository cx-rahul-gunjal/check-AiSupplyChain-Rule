"""
Anthropic Claude SDK agent implementation.
Uses Claude's tool use capabilities for agent patterns.
"""

import anthropic
import json

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

# Define tools for Claude
tools = [
    {
        "name": "search_database",
        "description": "Search the database for information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "execute_query",
        "description": "Execute a database query",
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "SQL query to execute"
                }
            },
            "required": ["sql"]
        }
    }
]

def search_database(query: str) -> str:
    """Search the database."""
    return f"Search results for '{query}': Found 5 matching records"

def execute_query(sql: str) -> str:
    """Execute a database query."""
    return f"Query executed successfully. Returned 10 rows."

def run_claude_agent(user_message: str):
    """Run the Claude agent with tool use."""
    messages = [
        {"role": "user", "content": user_message}
    ]
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            # Find the tool use block
            tool_use_block = next(
                (block for block in response.content if block.type == "tool_use"),
                None
            )
            
            if tool_use_block:
                tool_name = tool_use_block.name
                tool_input = tool_use_block.input
                
                # Execute the tool
                if tool_name == "search_database":
                    result = search_database(tool_input["query"])
                elif tool_name == "execute_query":
                    result = execute_query(tool_input["sql"])
                else:
                    result = "Unknown tool"
                
                # Add assistant response and tool result to messages
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use_block.id,
                            "content": result
                        }
                    ]
                })
        else:
            # Model finished, extract text response
            final_response = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "No response"
            )
            return final_response

if __name__ == "__main__":
    result = run_claude_agent("Search the database for all active users and tell me how many there are")
    print(f"Claude Response: {result}")
