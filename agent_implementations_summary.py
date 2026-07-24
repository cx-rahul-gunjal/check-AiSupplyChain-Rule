"""
Summary and index of all agent implementations for testing.
This file catalogs all available agent implementations.

AGENTS IMPLEMENTATION TABLE
==========================

| Agent Name | Library | Initialization Command | File |
|------------|---------|------------------------|------|
| LangChain | langchain | `agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)` | simple_agent.py |
| AutoGen | autogen | `assistant = AssistantAgent(name="Assistant", llm_config={...})` | autogen_agent.py |
| CrewAI | crewai | `researcher = Agent(role="...", goal="...", backstory="...", tools=[...])` | crewai_agent.py |
| OpenAI Assistants | openai | `assistant = client.beta.assistants.create(name="...", model="gpt-4", tools=tools)` | openai_assistants_agent.py |
| OpenAI Swarm | swarm | `support_agent = Agent(name="...", model="gpt-4", instructions="...", functions=[...])` | swarm_agent.py |
| Anthropic Claude | anthropic | `client = anthropic.Anthropic(api_key="...")` with tool use | anthropic_claude_agent.py |
| PydanticAI | pydantic_ai | `agent = Agent(model="gpt-4", system_prompt="...")` | pydantic_ai_agent.py |
| Semantic Kernel | semantic_kernel | `kernel = sk.Kernel()` + `kernel.add_service(OpenAIChatCompletion(...))` | semantic_kernel_agent.py |
| Haystack | haystack | `pipeline = Pipeline()` + component registration | haystack_agent.py |
| LlamaIndex | llama_index | `agent = ReActAgent.from_llm_and_tools(llm=llm, tools=[...], verbose=True)` | llamaindex_agents.py |
| Langroid | langroid | `agent = Agent(name="...", llm=llm, tools=[...], system_message="...")` | langroid_agent.py |
| HuggingFace Agents | transformers | `agent = Agent(tools=[...], model="...")` | huggingface_agents.py |
| smolagents | smolagents | `agent = CodeAgent(tools=[...], model="gpt-4")` | smolagents_agent.py |
| CAMEL | camel | `user_agent = ChatAgent(system_message=..., model_config=ChatGPTConfig(...))` | camel_agent.py |
| Marvin | marvin | `agent = Agent(name="...", description="...", tools=[...], model="gpt-4")` | marvin_agent.py |
| Reflexion | custom | `agent = ReflexionAgent(name="...", model="gpt-4")` | reflexion_agent.py |
| ToolFormer | custom | `agent = ToolFormerAgent(name="...", model="gpt-4")` | toolformer_agent.py |
| PyMongo Agent | pymongo | `agent = MongoDBAgent(name="...", db_url="mongodb://...", db_name="...")` | pymongo_agent.py |
| AgentGPT | custom | `agent = AgentGPTAgent(agent_id="...", name="...", goal="...", role="...")` | agentgpt_agent.py |

"""

AGENT_IMPLEMENTATIONS = {
    "LangChain": {
        "file": "simple_agent.py",
        "library": "langchain",
        "pattern": "ZERO_SHOT_REACT_DESCRIPTION",
        "components": ["Tool", "initialize_agent", "AgentType", "AgentExecutor"],
        "description": "LangChain agent with tools and reasoning loop"
    },
    "AutoGen": {
        "file": "autogen_agent.py",
        "library": "autogen",
        "pattern": "Multi-Agent Conversation",
        "components": ["AssistantAgent", "UserProxyAgent"],
        "description": "Microsoft AutoGen with multi-agent coordination"
    },
    "CrewAI": {
        "file": "crewai_agent.py",
        "library": "crewai",
        "pattern": "Role-Based Agent Team",
        "components": ["Agent", "Task", "Crew"],
        "description": "CrewAI with role-based agents and team coordination"
    },
    "OpenAI Assistants": {
        "file": "openai_assistants_agent.py",
        "library": "openai",
        "pattern": "Assistant API with Tool Calling",
        "components": ["OpenAI", "Assistants", "Thread", "MessageAPI"],
        "description": "Native OpenAI Assistant API with function calling"
    },
    "OpenAI Swarm": {
        "file": "swarm_agent.py",
        "library": "swarm",
        "pattern": "Lightweight Multi-Agent",
        "components": ["Swarm", "Agent"],
        "description": "OpenAI Swarm lightweight coordination framework"
    },
    "Anthropic Claude": {
        "file": "anthropic_claude_agent.py",
        "library": "anthropic",
        "pattern": "Tool Use with Claude",
        "components": ["Anthropic", "Messages API", "Tool Use"],
        "description": "Claude SDK with tool use and agentic behavior"
    },
    "PydanticAI": {
        "file": "pydantic_ai_agent.py",
        "library": "pydantic_ai",
        "pattern": "Type-Safe Agent Framework",
        "components": ["Agent", "RunContext", "Tool Decorators"],
        "description": "Modern Pydantic-based AI framework with type safety"
    },
    "Semantic Kernel": {
        "file": "semantic_kernel_agent.py",
        "library": "semantic_kernel",
        "pattern": "Orchestration Framework",
        "components": ["Kernel", "KernelPlugin", "Functions"],
        "description": "Microsoft Semantic Kernel for AI orchestration"
    },
    "Haystack": {
        "file": "haystack_agent.py",
        "library": "haystack",
        "pattern": "Component-Based Pipeline",
        "components": ["Pipeline", "Component", "Retrievers"],
        "description": "Deepset Haystack production framework with pipelines"
    },
    "LlamaIndex": {
        "file": "llamaindex_agents.py",
        "library": "llama_index",
        "pattern": "ReAct Agent with Tools",
        "components": ["ReActAgent", "FunctionTool"],
        "description": "LlamaIndex agents with reasoning and action loop"
    },
    "Langroid": {
        "file": "langroid_agent.py",
        "library": "langroid",
        "pattern": "Agent Task Framework",
        "components": ["Agent", "Tool", "Task"],
        "description": "Langroid multi-agent conversation framework"
    },
    "HuggingFace Agents": {
        "file": "huggingface_agents.py",
        "library": "transformers",
        "pattern": "HF Agent Framework",
        "components": ["Tool", "Agent"],
        "description": "Native HuggingFace agent framework"
    },
    "smolagents": {
        "file": "smolagents_agent.py",
        "library": "smolagents",
        "pattern": "Lightweight Code Agents",
        "components": ["tool", "CodeAgent", "ToolCallingAgent"],
        "description": "HuggingFace lightweight agent framework"
    },
    "CAMEL": {
        "file": "camel_agent.py",
        "library": "camel",
        "pattern": "Multi-Agent Conversation",
        "components": ["ChatAgent", "BaseMessage"],
        "description": "CAMEL framework for building agent societies"
    },
    "Marvin": {
        "file": "marvin_agent.py",
        "library": "marvin",
        "pattern": "Tool-Based Agent Coordination",
        "components": ["Agent", "Tool"],
        "description": "Marvin multi-agent coordination framework"
    },
    "Reflexion": {
        "file": "reflexion_agent.py",
        "library": "custom",
        "pattern": "Self-Reflecting Agent",
        "components": ["Memory", "ReflexionAgent"],
        "description": "Agent with self-reflection and learning capabilities"
    },
    "ToolFormer": {
        "file": "toolformer_agent.py",
        "library": "custom",
        "pattern": "Tool Learning and Optimization",
        "components": ["Tool", "ToolFormerAgent"],
        "description": "Agent that learns optimal tool usage patterns"
    },
    "PyMongo Agent": {
        "file": "pymongo_agent.py",
        "library": "pymongo",
        "pattern": "Database-Integrated Agent",
        "components": ["MongoDBAgent", "MongoClient"],
        "description": "Agent integrated with MongoDB for state persistence"
    },
    "AgentGPT": {
        "file": "agentgpt_agent.py",
        "library": "custom",
        "pattern": "Goal-Driven Agent Architecture",
        "components": ["AgentGPTAgent", "AgentGPTOrchestrator"],
        "description": "Goal-driven agent architecture with task management"
    }
}

def print_agent_summary():
    """Print summary of all implemented agents."""
    print("=" * 80)
    print("AGENT IMPLEMENTATION SUMMARY")
    print("=" * 80)
    print(f"\nTotal Agents Implemented: {len(AGENT_IMPLEMENTATIONS)}\n")
    
    for agent_name, details in AGENT_IMPLEMENTATIONS.items():
        print(f"\n{'─' * 80}")
        print(f"Agent: {agent_name}")
        print(f"File: {details['file']}")
        print(f"Library: {details['library']}")
        print(f"Pattern: {details['pattern']}")
        print(f"Description: {details['description']}")
        print(f"Components: {', '.join(details['components'])}")

def get_agent_by_library(library_name: str):
    """Get agents that use a specific library."""
    agents = [
        name for name, details in AGENT_IMPLEMENTATIONS.items()
        if details['library'].lower() == library_name.lower()
    ]
    return agents

def get_agents_by_pattern(pattern_name: str):
    """Get agents that use a specific pattern."""
    agents = [
        name for name, details in AGENT_IMPLEMENTATIONS.items()
        if pattern_name.lower() in details['pattern'].lower()
    ]
    return agents

if __name__ == "__main__":
    # Print summary
    print_agent_summary()
    
    # Example queries
    print(f"\n\n{'=' * 80}")
    print("EXAMPLE QUERIES")
    print("=" * 80)
    
    print("\nAgents using OpenAI library:")
    print(get_agent_by_library("openai"))
    
    print("\nAgents using Multi-Agent patterns:")
    print(get_agents_by_pattern("Multi-Agent"))
    
    print("\nAgents using Tool-Based patterns:")
    print(get_agents_by_pattern("Tool"))
