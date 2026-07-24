"""
A simple agent implementation using CrewAI framework.
This demonstrates agent patterns with role-based agents and task execution.
"""

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Initialize tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Create agents with specific roles
researcher = Agent(
    role="Senior Researcher",
    goal="Discover and analyze information about given topics",
    backstory="""You are an expert researcher with years of experience 
    in finding and analyzing information. You have a keen eye for detail 
    and can quickly synthesize information from multiple sources.""",
    tools=[search_tool, scrape_tool],
    verbose=True
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze the research findings and provide insights",
    backstory="""You are a data analyst with expertise in interpreting 
    information and providing actionable insights.""",
    tools=[],
    verbose=True
)

# Define tasks
research_task = Task(
    description="Research the latest trends in artificial intelligence",
    agent=researcher,
    expected_output="A detailed report on AI trends"
)

analysis_task = Task(
    description="Analyze the research findings and provide key insights",
    agent=analyst,
    expected_output="Key insights and analysis of AI trends"
)

# Create a crew (team of agents)
crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task],
    verbose=True
)

def run_crew_agent(topic: str):
    """Run the crew with a given topic."""
    try:
        result = crew.kickoff()
        return result
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the crew
    result = run_crew_agent("Artificial Intelligence trends")
    print(f"Crew Result: {result}")
