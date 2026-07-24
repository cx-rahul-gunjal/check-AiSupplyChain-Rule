"""
A simple agent implementation using Microsoft's AutoGen framework.
This demonstrates agent patterns with code execution and conversation.
"""

from autogen import AssistantAgent, UserProxyAgent

# Create a user proxy agent (simulates user interaction)
user_proxy = UserProxyAgent(
    name="User",
    system_message="A helpful human user.",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

# Create an assistant agent
assistant = AssistantAgent(
    name="Assistant",
    system_message="""You are a helpful AI assistant that can write and execute Python code.
When the user asks a question, you can write Python code to solve it.
You can also provide explanations and analysis.""",
    llm_config={
        "config_list": [{"model": "gpt-4", "api_key": "YOUR_API_KEY"}]
    }
)

def run_autogen_agent(task: str):
    """Run the AutoGen agent with a given task."""
    user_proxy.initiate_chat(
        assistant,
        message=task
    )

if __name__ == "__main__":
    # Test the agent
    test_task = "Write a Python function to calculate the Fibonacci sequence up to 10 numbers"
    run_autogen_agent(test_task)
