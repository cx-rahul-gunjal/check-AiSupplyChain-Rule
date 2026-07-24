"""
CAMEL agent implementation.
Multi-agent conversation framework for building agent societies.
"""

from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig
from camel.messages import BaseMessage
from camel.typing import RoleType

# Define system prompts for different roles
user_sys_prompt = """You are a helpful user assistant. 
Your role is to communicate with the AI assistant to accomplish tasks."""

assistant_sys_prompt = """You are a helpful AI assistant.
You have access to various tools and can help users accomplish their goals.
Always provide clear and concise responses."""

def run_camel_agents(user_message: str):
    """Run the CAMEL multi-agent system."""
    try:
        # Create user agent
        user_agent = ChatAgent(
            system_message=user_sys_prompt,
            model_config=ChatGPTConfig(
                api_key="YOUR_API_KEY",
                model="gpt-4"
            )
        )
        
        # Create assistant agent
        assistant_agent = ChatAgent(
            system_message=assistant_sys_prompt,
            model_config=ChatGPTConfig(
                api_key="YOUR_API_KEY",
                model="gpt-4"
            )
        )
        
        # Start conversation
        user_msg = BaseMessage.make_user_message(
            role_name="User",
            content=user_message
        )
        
        # Assistant responds
        assistant_response = assistant_agent.step(user_msg)
        
        # User can reply
        user_reply = user_agent.step(assistant_response)
        
        return user_reply.content
    except Exception as e:
        return f"Error: {str(e)}"

def run_camel_role_playing(task_description: str):
    """Run role-playing agents in CAMEL framework."""
    try:
        # Define roles for a conversation
        ceo_sys_prompt = "You are a CEO of a tech startup discussing growth strategy."
        cto_sys_prompt = "You are a CTO discussing technical implementation details."
        
        # Create role-specific agents
        ceo_agent = ChatAgent(
            system_message=ceo_sys_prompt,
            model_config=ChatGPTConfig(
                api_key="YOUR_API_KEY",
                model="gpt-4"
            )
        )
        
        cto_agent = ChatAgent(
            system_message=cto_sys_prompt,
            model_config=ChatGPTConfig(
                api_key="YOUR_API_KEY",
                model="gpt-4"
            )
        )
        
        # Start role-play conversation
        initial_message = BaseMessage.make_user_message(
            role_name="CEO",
            content=task_description
        )
        
        response = cto_agent.step(initial_message)
        
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    result = run_camel_agents("How can we improve our customer service?")
    print(f"CAMEL Response: {result}")
    
    result2 = run_camel_role_playing("How should we scale our infrastructure?")
    print(f"CAMEL Role-Play Response: {result2}")
