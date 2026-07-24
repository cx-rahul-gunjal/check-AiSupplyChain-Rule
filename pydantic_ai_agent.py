"""
PydanticAI agent implementation.
Modern Pydantic-based AI framework with type safety.
"""

from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

# Define data models
class UserInfo(BaseModel):
    user_id: str
    name: str
    email: str

class OrderInfo(BaseModel):
    order_id: str
    status: str
    total: float

# Create agent
agent = Agent(
    model="gpt-4",
    system_prompt="You are a helpful customer service agent with access to user and order information."
)

# Define tools using decorators
@agent.tool
def get_user_info(ctx: RunContext, user_id: str) -> UserInfo:
    """Retrieve user information by user ID."""
    return UserInfo(
        user_id=user_id,
        name="John Doe",
        email="john@example.com"
    )

@agent.tool
def get_order_info(ctx: RunContext, order_id: str) -> OrderInfo:
    """Retrieve order information by order ID."""
    return OrderInfo(
        order_id=order_id,
        status="shipped",
        total=99.99
    )

@agent.tool
def update_order_status(ctx: RunContext, order_id: str, status: str) -> str:
    """Update the status of an order."""
    return f"Order {order_id} status updated to {status}"

def run_pydantic_ai_agent(user_message: str):
    """Run the PydanticAI agent."""
    try:
        result = agent.run_sync(user_message)
        return result.data
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    result = run_pydantic_ai_agent("Can you tell me about user 123 and their recent order?")
    print(f"PydanticAI Response: {result}")
