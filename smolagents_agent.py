"""
smolagents implementation.
Lightweight agent framework from HuggingFace.
"""

from smolagents import tool, Agent, CodeAgent, ToolCallingAgent
import json

# Define tools using decorator
@tool
def get_current_weather(location: str) -> str:
    """Get the current weather for a location."""
    return json.dumps({"location": location, "temperature": 72, "condition": "sunny"})

@tool
def calculate(operation: str, a: float, b: float) -> float:
    """Perform a calculation."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else None
    return None

@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base."""
    return f"Found 5 results for '{query}': Result 1, Result 2, Result 3..."

@tool
def send_email(recipient: str, subject: str, body: str) -> str:
    """Send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"

def run_smolagents_agent(user_task: str):
    """Run the smolagents agent."""
    try:
        # Create agent with tools
        agent = CodeAgent(
            tools=[get_current_weather, calculate, search_knowledge_base, send_email],
            model="gpt-4"
        )
        
        # Run agent
        result = agent.run(user_task)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    result = run_smolagents_agent("What's the weather in New York? Also calculate 100 + 50")
    print(f"smolagents Response: {result}")
