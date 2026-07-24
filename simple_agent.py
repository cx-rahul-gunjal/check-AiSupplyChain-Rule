"""
A simple agent implementation using LangChain for testing agent detection.
This agent demonstrates basic agent patterns with tools and reasoning.
"""

from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper, WikipediaAPIWrapper

# Initialize the LLM
llm = OpenAI(temperature=0)

# Define tools the agent can use
search = SerpAPIWrapper()
wikipedia = WikipediaAPIWrapper()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for searching the internet for current information"
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Useful for looking up information on Wikipedia"
    ),
    Tool(
        name="Calculator",
        func=lambda x: str(eval(x)),
        description="Useful for math calculations"
    )
]

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_agent_query(query: str):
    """Run the agent with a given query."""
    try:
        result = agent.run(query)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the agent
    test_query = "What is the capital of France and how far is it from London?"
    result = run_agent_query(test_query)
    print(f"Query: {test_query}")
    print(f"Result: {result}")
