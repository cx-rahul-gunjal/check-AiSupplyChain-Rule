"""
OpenAI Swarm agent implementation.
Lightweight multi-agent coordination framework.
"""

from swarm import Swarm, Agent
import json

client = Swarm()

# Define tool functions
def get_user_info(user_id: str) -> str:
    """Get user information."""
    return json.dumps({"user_id": user_id, "name": "John Doe", "email": "john@example.com"})

def process_order(order_id: str) -> str:
    """Process an order."""
    return f"Order {order_id} has been processed"

def escalate_to_specialist() -> str:
    """Escalate to a specialist."""
    return "Escalating to specialist..."

# Create agents
support_agent = Agent(
    name="Support Agent",
    model="gpt-4",
    instructions="You are a helpful customer support agent. Help users with their questions.",
    functions=[get_user_info, process_order, escalate_to_specialist]
)

specialist_agent = Agent(
    name="Specialist Agent",
    model="gpt-4",
    instructions="You are a specialist support agent. Handle complex technical issues.",
    functions=[get_user_info]
)

def run_swarm_agent(user_message: str):
    """Run the swarm agent system."""
    messages = [
        {"role": "user", "content": user_message}
    ]
    
    agent = support_agent
    
    while True:
        response = client.run(
            agent=agent,
            messages=messages
        )
        
        messages.append({"role": "assistant", "content": response.messages[-1]["content"]})
        
        if response.agent == agent:
            break
        
        agent = response.agent
    
    return response.messages[-1]["content"]

if __name__ == "__main__":
    result = run_swarm_agent("Can you help me with my order?")
    print(f"Swarm Response: {result}")
