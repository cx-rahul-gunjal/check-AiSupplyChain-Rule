"""
Marvin agent implementation.
Multi-agent coordination and conversation framework.
"""

from marvin.agent import Agent
from marvin.models import Message
from marvin.tools import Tool
from typing import Optional

# Define agent tools
class WeatherService:
    @staticmethod
    def get_weather(location: str) -> dict:
        """Get weather for a location."""
        return {"location": location, "temperature": 72, "condition": "sunny"}

class EmailService:
    @staticmethod
    def send_email(to: str, subject: str, body: str) -> bool:
        """Send an email."""
        return True

class DataService:
    @staticmethod
    def query_data(query: str) -> list:
        """Query data."""
        return [f"Result {i}" for i in range(5)]

# Create agent tools
weather_tool = Tool(
    name="get_weather",
    description="Get current weather information",
    func=WeatherService.get_weather
)

email_tool = Tool(
    name="send_email",
    description="Send an email message",
    func=EmailService.send_email
)

data_tool = Tool(
    name="query_data",
    description="Query data from the system",
    func=DataService.query_data
)

def run_marvin_agent(task: str, agent_type: str = "standard"):
    """Run a Marvin agent."""
    try:
        # Create agent with tools
        agent = Agent(
            name="MarvinAgent",
            description="A helpful agent powered by Marvin",
            tools=[weather_tool, email_tool, data_tool],
            model="gpt-4"
        )
        
        # Run the agent
        result = agent.run(task)
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def run_marvin_multi_agent(task: str):
    """Run multiple coordinated Marvin agents."""
    try:
        # Create coordinator agent
        coordinator = Agent(
            name="Coordinator",
            description="Coordinates multiple agents",
            model="gpt-4"
        )
        
        # Create specialist agents
        specialist_1 = Agent(
            name="DataSpecialist",
            description="Handles data queries",
            tools=[data_tool],
            model="gpt-4"
        )
        
        specialist_2 = Agent(
            name="CommunicationSpecialist",
            description="Handles communication",
            tools=[email_tool],
            model="gpt-4"
        )
        
        # Coordinator delegates to specialists
        result = coordinator.run(task)
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    result = run_marvin_agent("Get the weather in New York and send me a summary email")
    print(f"Marvin Agent Response: {result}")
    
    result2 = run_marvin_multi_agent("Query the database and send results via email")
    print(f"Marvin Multi-Agent Response: {result2}")
