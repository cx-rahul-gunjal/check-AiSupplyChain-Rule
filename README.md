"""
README documentation for AI-BOM-POC Application
"""

# AI-BOM-POC: Comprehensive AI Application

A production-ready Python application demonstrating advanced AI capabilities using FastMCP, multiple AI frameworks, and distributed agent systems.

## Overview

AI-BOM-POC is a comprehensive proof-of-concept application that integrates:

- **FastMCP Server**: Model Context Protocol server with tools, resources, and external service integrations
- **MCP Clients**: Multiple clients using `stdio_client` for service communication
- **LangChain Agents**: Multi-agent system with sequential and parallel execution
- **CrewAI**: Role-based agent crews with structured task execution
- **PydanticAI**: Type-safe agents with Pydantic models for structured outputs
- **AI Models**: Multiple production models (GPT-4, Claude 3, Llama 2) with model selection and registry

## Project Structure

```
/Users/usamayaseen/ch/EVO/AI-BOM-POC2/
├── mcp_server.py           # FastMCP server implementation
├── mcp_clients.py          # MCP client implementations
├── langchain_agents.py     # LangChain agent system
├── crewai_agents.py        # CrewAI crew implementation
├── pydantic_agents.py      # PydanticAI type-safe agents
├── models.py               # AI models implementation (GPT-4, Claude, Llama)
├── config.py               # Configuration management
├── main.py                 # Main orchestration module
└── README.md              # This file
```

## Components

### 1. MCP Server (`mcp_server.py`)

FastMCP-based server providing:

**Tools:**
- `analyze_text`: Text analysis and statistics
- `calculate_sum`, `calculate_average`, `calculate_statistics`: Math operations
- `fetch_weather_data`: Weather API integration
- `search_web`: Web search functionality
- `process_data`: Data processing with multiple operations
- `filter_data`: Data filtering operations
- `transform_data`: Data transformation
- `call_external_api`: Generic external API calls

**Resources:**
- `config://system`: System configuration
- `data://sample/{dataset_name}`: Sample datasets (users, products, metrics)
- `docs://api/{endpoint}`: API documentation
- `stats://server`: Server statistics

**Prompts:**
- `analysis_prompt`: Generate analysis prompts
- `research_prompt`: Generate research prompts
- `coding_prompt`: Generate coding task prompts

### 2. MCP Clients (`mcp_clients.py`)

Multiple specialized MCP client implementations:

- **WeatherMCPClient**: Weather data retrieval
- **DataProcessingMCPClient**: Data processing and analysis
- **SearchMCPClient**: Web search functionality
- **CalculationMCPClient**: Mathematical calculations
- **ResourceMCPClient**: Resource access
- **APICallMCPClient**: External API calls
- **UnifiedMCPClient**: Orchestrated multi-service access

### 3. LangChain Agents (`langchain_agents.py`)

Tool-based agent system featuring:

- **ToolRegistry**: Dynamic tool registration and management
- **ResearchAgent**: Information gathering and analysis
- **AnalysisAgent**: Sentiment and text analysis
- **SummarizationAgent**: Text summarization
- **MultiAgentSystem**: Sequential and parallel agent execution

### 4. CrewAI Agents (`crewai_agents.py`)

Role-based agent coordination system:

- **Agent Roles**: Leader, Analyst, Specialist, Executor, Validator
- **Task System**: Priority-based task management with dependencies
- **Crew Management**: Multi-agent orchestration
- **Execution Modes**: Sequential and parallel task execution

### 5. PydanticAI Agents (`pydantic_agents.py`)

Type-safe agent system with Pydantic models:

**Result Models:**
- `TextAnalysisResult`: Text analysis output
- `DataProcessingResult`: Data processing output
- `PredictionResult`: ML predictions
- `ClassificationResult`: Text classification
- `ExtractionResult`: Information extraction
- `AgentResponse`: Standard agent response

**Agents:**
- `TextAnalysisAgent`: Type-safe text analysis
- `DataProcessor`: Structured data processing
- `PredictionAgent`: ML predictions with confidence
- `ClassificationAgent`: Multi-class text classification
- `ExtractionAgent`: Entity and relationship extraction

**System:**
- `TypeSafeMultiAgentSystem`: Manages multiple typed agents
- Pipeline execution with data flow
- Parallel execution with asyncio

### 6. Configuration (`config.py`)

Comprehensive configuration management:

- **Environment Support**: Development, Staging, Production
- **Model Configurations**: OpenAI, Anthropic, Azure, Local models
- **MCP Server Configs**: Service configurations
- **API Configurations**: External service integrations
- **Feature Flags**: Enable/disable components
- **Logger Configuration**: Structured logging setup

### 7. Main Application (`main.py`)

Application orchestration demonstrating:

- Integration of all components
- Demonstration workflows for each framework
- Parallel execution across frameworks
- Integrated multi-step workflows
- Comprehensive result reporting

## Features

### 6. AI Models (`models.py`)

Comprehensive model system with 4 production-ready models:

**Model Registry with 4 Advanced Models:**

1. **GPT-4 (OpenAI)**
   - Advanced reasoning and complex problem-solving
   - Code generation and analysis
   - Context window: 128K tokens
   - Capabilities: Text generation, summarization, Q&A, code generation, reasoning, entity extraction
   - Cost: $0.03 per 1K tokens
   - Best for: Complex reasoning, advanced analysis

2. **Claude 3 Opus (Anthropic)**
   - Constitutional AI with safety focus
   - Strong reasoning abilities
   - Context window: 200K tokens
   - Capabilities: Text generation, summarization, Q&A, code generation, reasoning, entity extraction
   - Cost: $0.015 per 1K tokens
   - Best for: Safety-critical tasks, long-form analysis

3. **Llama 2 70B (Meta)**
   - Open-source and self-hostable
   - Cost-effective implementation
   - Context window: 4K tokens
   - Capabilities: Text generation, summarization, Q&A, code generation, entity extraction
   - Cost: $0.002 per 1K tokens
   - Best for: On-premise deployment, cost-sensitive applications

4. **Text2Vec Embedding (DMetaSoul)**
   - Specialized embedding model
   - Semantic search optimization
   - Output dimension: 768
   - Capabilities: Embeddings, classification
   - Cost: $0.0001 per 1K tokens
   - Best for: Semantic search, similarity computation

**Key Features:**
- **ModelRegistry**: Centralized model management
- **ModelSelector**: Intelligent model selection based on capabilities or requirements
- **Model Capabilities**: Defined capability system for matching tasks to models
- **Performance Tracking**: Execution count and token usage monitoring
- **Cost Analysis**: Per-model cost tracking

### MCP Integration
- Stdio-based client-server communication
- Tool invocation and resource access
- Prompt generation capabilities
- External service integration

### Agent Systems
- **LangChain**: Tool-based agents with memory
- **CrewAI**: Role-based agents with task dependencies
- **PydanticAI**: Type-safe agents with structured outputs

### AI Models
- **Model Registry**: Centralized management of multiple production models
- **Model Selector**: Intelligent selection based on task requirements
- **Capability Matching**: Match models to specific capabilities
- **Cost Tracking**: Monitor usage and costs per model

### Execution Patterns
- Sequential execution with dependencies
- Parallel execution with asyncio
- Pipeline workflows with data flow
- Integrated multi-framework workflows
- Model-aware agent selection

### Configuration
- Environment-based settings
- Feature flags for component toggling
- Model and API configuration management
- Validation and logging

## Usage

### Running the Application

```bash
# Run the main orchestration
python main.py

# Run individual components
python mcp_server.py
python mcp_clients.py
python langchain_agents.py
python crewai_agents.py
python pydantic_agents.py
python config.py
```

### Environment Variables

Configure behavior via environment variables:

```bash
# Environment type
export ENV=development  # or staging, production

# Debug mode
export DEBUG=true

# Log level
export LOG_LEVEL=INFO

# API Keys
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-...
export WEATHER_API_KEY=...

# Feature flags
export ENABLE_LANGCHAIN_AGENTS=true
export ENABLE_CREWAI_AGENTS=true
export ENABLE_PYDANTIC_AGENTS=true
export ENABLE_MCP_CLIENT=true
export ENABLE_PARALLEL_EXECUTION=true
```

### Example Usage

#### Using AI Models

```python
from models import ModelRegistry, ModelSelector, ModelCapability

# Create registry
registry = ModelRegistry()

# Get a specific model
gpt4 = registry.get_model("gpt4")
response = await gpt4.generate("Explain quantum computing")

# Get model info
print(gpt4.get_info())

# Select model by capability
selector = ModelSelector(registry)
code_model = selector.select_for_capability(ModelCapability.CODE_GENERATION)

# Get models by task
model = selector.select_for_task("reasoning")

# Get recommendation based on requirements
recommended = selector.recommend_model({
    "requires_reasoning": True,
    "requires_code": True
})
```

#### Single Agent Execution

```python
from pydantic_agents import TextAnalysisAgent

agent = TextAnalysisAgent()
response = await agent.process("This is great text!")
print(response.to_dict())
```

#### Multi-Agent System

```python
from langchain_agents import MultiAgentSystem

system = MultiAgentSystem()
result = await system.process_sequential("Input text")
print(result)
```

#### Crew Execution

```python
from crewai_agents import Crew, LeaderAgent, Task, AgentRole

crew = Crew("Team")
crew.add_agent(LeaderAgent())
crew.add_task(Task("Task 1", "Description", AgentRole.LEADER))
results = await crew.execute_all_tasks()
```

#### MCP Client Integration

```python
from mcp_clients import UnifiedMCPClient

client = UnifiedMCPClient()
results = await client.execute_workflow({
    "search_query": "AI trends",
    "text_to_analyze": "Sample text"
})
```

## Key Design Patterns

### 1. Tool Registry Pattern
Dynamic tool registration allowing flexible tool management without hardcoding.

### 2. Role-Based Execution
CrewAI agents assigned specific roles with role-appropriate task execution.

### 3. Type Safety with Pydantic
Structured outputs using Pydantic models ensuring type safety and validation.

### 4. Composition over Inheritance
Using composition to build complex systems from simple, reusable components.

### 5. Async/Await Pattern
Full async support enabling concurrent execution and efficient resource usage.

## Dependencies

The application uses:

- **FastMCP**: MCP server implementation
- **asyncio**: Asynchronous execution
- **httpx**: Async HTTP client
- **Pydantic**: Data validation (simulated)
- **dataclasses**: Data structure definition

All dependencies are imported within modules to avoid hard requirements.

## Architecture

### Layered Architecture

```
┌─────────────────────────────────┐
│   Application Layer (main.py)   │
├─────────────────────────────────┤
│   Agent Frameworks Layer        │
│  ├─ LangChain                   │
│  ├─ CrewAI                      │
│  └─ PydanticAI                  │
├─────────────────────────────────┤
│   MCP Layer                     │
│  ├─ MCP Server                  │
│  └─ MCP Clients                 │
├─────────────────────────────────┤
│   Configuration & Utilities     │
│  ├─ Config Management           │
│  └─ Logging                     │
└─────────────────────────────────┘
```

## Execution Flow

1. **Initialization**: Load configuration and create agent systems
2. **Demonstrations**: Run individual framework demonstrations
3. **Integration**: Execute integrated workflows combining frameworks
4. **Reporting**: Generate comprehensive results and save to file

## Output

Application generates `application_results.json` containing:

- Timestamp of execution
- Configuration summary
- Results from each demonstration
- Execution statistics

## Error Handling

- Graceful degradation when features are disabled
- Comprehensive error logging
- Exception handling in async operations
- Fallback mechanisms for API failures

## Performance Considerations

- Async/await for concurrent operations
- Parallel execution when enabled
- Resource cleanup with context managers
- Configurable timeouts for external calls

## Extensibility

The application is designed for easy extension:

1. **Add New Tools**: Register in tool registry
2. **Add New Agents**: Extend base agent classes
3. **Add New Models**: Extend configuration classes
4. **Add New Frameworks**: Follow component patterns

## Testing

Each module includes demonstration functions:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

Run individual modules to test specific components.

## Future Enhancements

- Database integration for state persistence
- Advanced monitoring and metrics
- Real-time streaming responses
- Distributed execution across services
- Machine learning model integration
- Enhanced caching mechanisms
- API rate limiting and backoff

## License

This is a proof-of-concept application for demonstrating AI integration patterns.

## Notes

- No package manager files included as per requirements
- All imports are inline to support optional dependencies
- Simulated external API calls for demonstration
- Configuration supports multiple environments
- Comprehensive logging throughout

## Support

For issues or questions about the application:
1. Check the configuration settings
2. Review the console output and log files
3. Examine individual component demonstrations
4. Check async/await patterns for concurrency issues
