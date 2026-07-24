"""
Langroid agent implementation.
Multi-agent conversation and orchestration framework.
"""

from langroid.agent.agent import Agent
from langroid.agent.tools.tool import Tool
from langroid.agent.task import Task
from langroid.language_models.openai_gpt import OpenAIGPT

# Define tools
class DataTools:
    @staticmethod
    def query_database(query: str) -> str:
        """Query the database."""
        return f"Database results for '{query}': 10 records found"
    
    @staticmethod
    def fetch_user(user_id: str) -> str:
        """Fetch user information."""
        return f"User {user_id}: John Doe (john@example.com)"
    
    @staticmethod
    def update_record(record_id: str, data: str) -> str:
        """Update a record."""
        return f"Record {record_id} updated with: {data}"

# Create tools
database_tool = Tool(
    name="query_database",
    func=DataTools.query_database,
    description="Query the database for information"
)

user_tool = Tool(
    name="fetch_user",
    func=DataTools.fetch_user,
    description="Fetch user information by ID"
)

update_tool = Tool(
    name="update_record",
    func=DataTools.update_record,
    description="Update a record in the database"
)

def run_langroid_agent(user_message: str):
    """Run the Langroid agent system."""
    # Initialize LLM
    llm = OpenAIGPT(
        model="gpt-4",
        api_key="YOUR_API_KEY"
    )
    
    # Create agent
    agent = Agent(
        name="DataAgent",
        llm=llm,
        tools=[database_tool, user_tool, update_tool],
        system_message="You are a helpful data agent with access to database tools."
    )
    
    # Create task
    task = Task(
        agent=agent,
        name="DataTask",
        description="Handle user queries about data"
    )
    
    # Run task
    try:
        result = task.run(user_message)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    result = run_langroid_agent("Can you get me information about user 123?")
    print(f"Langroid Response: {result}")
