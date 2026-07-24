# AI Agents Implementation Table

Complete reference of all agent implementations with their initialization commands and libraries.

## Summary

- **Total Agents**: 19
- **Libraries Used**: 15+ frameworks
- **Coverage**: Multi-agent systems, ReAct patterns, tool use, agentic patterns

---

## Excel Copy-Paste Format

```
Agent Name	Library	Initialization Command	File
LangChain	langchain	agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)	simple_agent.py
AutoGen	autogen	assistant = AssistantAgent(name="Assistant", llm_config={...})	autogen_agent.py
CrewAI	crewai	researcher = Agent(role="...", goal="...", backstory="...", tools=[...])	crewai_agent.py
OpenAI Assistants	openai	assistant = client.beta.assistants.create(name="...", model="gpt-4", tools=tools)	openai_assistants_agent.py
OpenAI Swarm	swarm	support_agent = Agent(name="...", model="gpt-4", instructions="...", functions=[...])	swarm_agent.py
Anthropic Claude	anthropic	client = anthropic.Anthropic(api_key="...")	anthropic_claude_agent.py
PydanticAI	pydantic_ai	agent = Agent(model="gpt-4", system_prompt="...")	pydantic_ai_agent.py
Semantic Kernel	semantic_kernel	kernel = sk.Kernel() + kernel.add_service(OpenAIChatCompletion(...))	semantic_kernel_agent.py
Haystack	haystack	pipeline = Pipeline() + component registration	haystack_agent.py
LlamaIndex	llama_index	agent = ReActAgent.from_llm_and_tools(llm=llm, tools=[...], verbose=True)	llamaindex_agents.py
Langroid	langroid	agent = Agent(name="...", llm=llm, tools=[...], system_message="...")	langroid_agent.py
HuggingFace Agents	transformers	agent = Agent(tools=[...], model="...")	huggingface_agents.py
smolagents	smolagents	agent = CodeAgent(tools=[...], model="gpt-4")	smolagents_agent.py
CAMEL	camel	user_agent = ChatAgent(system_message=..., model_config=ChatGPTConfig(...))	camel_agent.py
Marvin	marvin	agent = Agent(name="...", description="...", tools=[...], model="gpt-4")	marvin_agent.py
Reflexion	custom	agent = ReflexionAgent(name="...", model="gpt-4")	reflexion_agent.py
ToolFormer	custom	agent = ToolFormerAgent(name="...", model="gpt-4")	toolformer_agent.py
PyMongo Agent	pymongo	agent = MongoDBAgent(name="...", db_url="mongodb://...", db_name="...")	pymongo_agent.py
AgentGPT	custom	agent = AgentGPTAgent(agent_id="...", name="...", goal="...", role="...")	agentgpt_agent.py
```

**How to use:**
1. Copy the table above (including the header)
2. Open Excel
3. Paste directly into a cell
4. Excel will automatically split the columns by tabs

---

## Agents Comparison Table

| # | Agent Name | Library | Initialization Command | Key Features | File |
|---|------------|---------|------------------------|--------------|------|
| 1 | LangChain | langchain | `agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)` | Tool-based reasoning, ReAct pattern | simple_agent.py |
| 2 | AutoGen | autogen | `assistant = AssistantAgent(name="Assistant", llm_config={...})` | Multi-agent conversation, code execution | autogen_agent.py |
| 3 | CrewAI | crewai | `researcher = Agent(role="...", goal="...", backstory="...", tools=[...])` | Role-based teams, task orchestration | crewai_agent.py |
| 4 | OpenAI Assistants | openai | `assistant = client.beta.assistants.create(name="...", model="gpt-4", tools=tools)` | Native API, function calling | openai_assistants_agent.py |
| 5 | OpenAI Swarm | swarm | `support_agent = Agent(name="...", model="gpt-4", instructions="...", functions=[...])` | Lightweight coordination, agent transfer | swarm_agent.py |
| 6 | Anthropic Claude | anthropic | `client = anthropic.Anthropic(api_key="...")` with tool use | Tool use, agentic patterns | anthropic_claude_agent.py |
| 7 | PydanticAI | pydantic_ai | `agent = Agent(model="gpt-4", system_prompt="...")` with `@agent.tool` | Type-safe, decorators, modern | pydantic_ai_agent.py |
| 8 | Semantic Kernel | semantic_kernel | `kernel = sk.Kernel()` + `kernel.add_service(OpenAIChatCompletion(...))` | Orchestration, plugin system | semantic_kernel_agent.py |
| 9 | Haystack | haystack | `pipeline = Pipeline()` + component registration | Component-based, production-grade | haystack_agent.py |
| 10 | LlamaIndex | llama_index | `agent = ReActAgent.from_llm_and_tools(llm=llm, tools=[...], verbose=True)` | Retrieval-augmented, ReAct pattern | llamaindex_agents.py |
| 11 | Langroid | langroid | `agent = Agent(name="...", llm=llm, tools=[...], system_message="...")` | Task-based, multi-agent conversation | langroid_agent.py |
| 12 | HuggingFace Agents | transformers | `agent = Agent(tools=[...], model="...")` | Native HF framework, transformers | huggingface_agents.py |
| 13 | smolagents | smolagents | `agent = CodeAgent(tools=[...], model="gpt-4")` | Lightweight, code-based agents | smolagents_agent.py |
| 14 | CAMEL | camel | `user_agent = ChatAgent(system_message=..., model_config=ChatGPTConfig(...))` | Multi-agent conversation, role-based | camel_agent.py |
| 15 | Marvin | marvin | `agent = Agent(name="...", description="...", tools=[...], model="gpt-4")` | Tool coordination, orchestration | marvin_agent.py |
| 16 | Reflexion | custom | `agent = ReflexionAgent(name="...", model="gpt-4")` | Self-reflection, learning, memory | reflexion_agent.py |
| 17 | ToolFormer | custom | `agent = ToolFormerAgent(name="...", model="gpt-4")` | Tool optimization, learning patterns | toolformer_agent.py |
| 18 | PyMongo Agent | pymongo | `agent = MongoDBAgent(name="...", db_url="mongodb://...", db_name="...")` | Database persistence, MongoDB integration | pymongo_agent.py |
| 19 | AgentGPT | custom | `agent = AgentGPTAgent(agent_id="...", name="...", goal="...", role="...")` | Goal-driven, task orchestration | agentgpt_agent.py |

---

## Library Breakdown

### Official Framework Libraries
- **OpenAI**: OpenAI Assistants, Swarm
- **Anthropic**: Claude SDK
- **Microsoft**: AutoGen, Semantic Kernel
- **Deepset**: Haystack
- **HuggingFace**: transformers (Agents), smolagents

### Multi-Agent & Orchestration Frameworks
- **CrewAI**: Role-based agent teams
- **Langroid**: Task-based multi-agent framework
- **CAMEL**: Agent society framework
- **Marvin**: Multi-agent coordination

### Agent Building Libraries
- **LangChain**: ReAct agent framework
- **LlamaIndex**: Retrieval-augmented agents
- **PydanticAI**: Type-safe agent framework

### Specialized/Custom Implementations
- **Reflexion**: Self-reflecting agents with memory
- **ToolFormer**: Tool optimization agent
- **AgentGPT**: Goal-driven agent architecture
- **PyMongo**: Database-backed agents

---

## Initialization Pattern Categories

### 1. Factory Pattern
```python
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)  # LangChain
agent = ReActAgent.from_llm_and_tools(llm=llm, tools=[...])  # LlamaIndex
agent = CodeAgent(tools=[...], model="gpt-4")  # smolagents
```

### 2. Class Constructor
```python
agent = Agent(role="...", goal="...", tools=[...])  # CrewAI
agent = Agent(name="...", model="gpt-4", instructions="...", functions=[...])  # Swarm
agent = Agent(model="gpt-4", system_prompt="...")  # PydanticAI
```

### 3. Builder/Kernel Pattern
```python
kernel = sk.Kernel()
kernel.add_service(OpenAIChatCompletion(...))  # Semantic Kernel
```

### 4. Pipeline/Component Pattern
```python
pipeline = Pipeline()
pipeline.add_component(...)  # Haystack
```

### 5. Client-Based
```python
assistant = client.beta.assistants.create(...)  # OpenAI Assistants
client = anthropic.Anthropic(api_key="...")  # Claude
```

---

## Tool Definition Methods

| Pattern | Libraries | Example |
|---------|-----------|---------|
| Tool Class/List | LangChain, LlamaIndex, Swarm | `tools=[Tool(name="...", func=..., description="...")]` |
| Function Tool | LlamaIndex | `FunctionTool.from_defaults(fn=func, description="...")` |
| Decorator-Based | PydanticAI, smolagents | `@agent.tool` or `@tool` |
| Custom Class | HuggingFace, Marvin | `class WeatherTool(Tool):` |
| Dictionary Format | OpenAI, Anthropic | `{"type": "function", "function": {...}}` |

---

## Use Case Recommendations

### For Research & Rapid Development
- **PydanticAI**: Modern, type-safe, Python-first
- **LangChain**: Mature, extensive integrations
- **CrewAI**: Great for role-based team scenarios

### For Production Systems
- **Haystack**: Component-based, enterprise-ready
- **OpenAI Assistants**: Native API, officially supported
- **Semantic Kernel**: Microsoft ecosystem integration

### For Multi-Agent Systems
- **CAMEL**: Agent society simulations
- **CrewAI**: Team coordination
- **Langroid**: Multi-agent conversations

### For Advanced Patterns
- **Reflexion**: When self-improvement is needed
- **ToolFormer**: When tool optimization matters
- **PyMongo Agent**: When persistence is critical

### For Specific Use Cases
- **LlamaIndex**: RAG (Retrieval-Augmented Generation)
- **Swarm**: Lightweight agent handoff
- **smolagents**: Resource-constrained environments

---

## Quick Start Guide

### 1. Basic Tool-Based Agent (LangChain)
```python
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI

tools = [Tool(name="Search", func=search_func, description="...")]
agent = initialize_agent(tools, OpenAI(), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
result = agent.run("Your query here")
```

### 2. Role-Based Team Agent (CrewAI)
```python
from crewai import Agent, Task, Crew

researcher = Agent(role="Researcher", goal="...", tools=[...])
analyst = Agent(role="Analyst", goal="...", tools=[...])
crew = Crew(agents=[researcher, analyst], tasks=[...])
result = crew.kickoff()
```

### 3. ReAct Agent (LlamaIndex)
```python
from llama_index.core.agent import ReActAgent

agent = ReActAgent.from_llm_and_tools(
    llm=OpenAI(model="gpt-4"),
    tools=[tool1, tool2],
    verbose=True
)
response = agent.chat("Your question")
```

### 4. Type-Safe Agent (PydanticAI)
```python
from pydantic_ai import Agent

agent = Agent(model="gpt-4", system_prompt="You are helpful...")

@agent.tool
def get_data(ctx, query: str) -> str:
    return "data"

result = agent.run_sync("Your message")
```

---

**Last Updated**: January 10, 2026  
**Total Agent Implementations**: 19  
**Framework Coverage**: 15+ major AI frameworks
