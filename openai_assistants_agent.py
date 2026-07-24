"""
OpenAI Assistants API agent implementation.
Uses native OpenAI assistant framework with function calling.
"""

import openai
from openai import OpenAI
import json

client = OpenAI(api_key="YOUR_API_KEY")

# Define tools/functions for the assistant
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def get_weather(location: str) -> str:
    """Simulate weather lookup."""
    return f"Weather in {location}: Sunny, 72°F"

def calculate(expression: str) -> str:
    """Perform calculation."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def run_assistant_agent(user_message: str):
    """Run the OpenAI assistant agent."""
    # Create assistant
    assistant = client.beta.assistants.create(
        name="Math and Weather Assistant",
        description="An assistant that can help with math and weather queries",
        model="gpt-4",
        tools=tools
    )
    
    # Create thread
    thread = client.beta.threads.create()
    
    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )
    
    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    
    # Process the run
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        
        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []
            
            for tool_call in tool_calls:
                if tool_call.function.name == "get_weather":
                    output = get_weather(json.loads(tool_call.function.arguments)["location"])
                elif tool_call.function.name == "calculate":
                    output = calculate(json.loads(tool_call.function.arguments)["expression"])
                
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": output
                })
            
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
    
    # Get messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text

if __name__ == "__main__":
    result = run_assistant_agent("What's the weather in New York and what's 15 * 4?")
    print(f"Assistant Response: {result}")
