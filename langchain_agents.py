"""
LangChain Agents implementation for AI-BOM-POC.
Demonstrates agents using LLMs with tools and various model providers.
"""

import asyncio
from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
import json
from datetime import datetime


# ====================
# Tool Definitions for LangChain
# ====================

class Tool:
    """Base tool class for LangChain agents."""
    
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func
    
    async def execute(self, *args, **kwargs) -> Any:
        """Execute the tool."""
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(*args, **kwargs)
        else:
            return self.func(*args, **kwargs)


class ToolRegistry:
    """Registry for managing tools available to agents."""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, name: str, description: str):
        """Decorator to register a tool."""
        def decorator(func: Callable):
            self.tools[name] = Tool(name, description, func)
            return func
        return decorator
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools."""
        return [
            {"name": name, "description": tool.description}
            for name, tool in self.tools.items()
        ]


# ====================
# Tool Registry Instance
# ====================

tool_registry = ToolRegistry()


# ====================
# Available Tools
# ====================

@tool_registry.register("search_information", "Search for information on a topic")
async def search_information(query: str) -> Dict[str, Any]:
    """Search for information."""
    await asyncio.sleep(0.1)
    return {
        "query": query,
        "results": [
            {"title": f"Result 1 for {query}", "url": "https://example.com/1"},
            {"title": f"Result 2 for {query}", "url": "https://example.com/2"}
        ]
    }


@tool_registry.register("analyze_sentiment", "Analyze sentiment of text")
async def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Analyze sentiment of text."""
    positive_words = ["good", "great", "excellent", "amazing", "wonderful"]
    negative_words = ["bad", "terrible", "awful", "horrible", "poor"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "text": text,
        "sentiment": sentiment,
        "confidence": 0.8,
        "positive_indicators": positive_count,
        "negative_indicators": negative_count
    }


@tool_registry.register("summarize_text", "Summarize a text passage")
async def summarize_text(text: str, max_length: int = 100) -> Dict[str, Any]:
    """Summarize text."""
    words = text.split()
    summary_words = words[:min(len(words), max(5, len(words) // 3))]
    
    return {
        "original_length": len(text),
        "summary": " ".join(summary_words) + "...",
        "reduction_percentage": round((1 - len(" ".join(summary_words)) / len(text)) * 100, 2)
    }


@tool_registry.register("extract_entities", "Extract named entities from text")
async def extract_entities(text: str) -> Dict[str, Any]:
    """Extract entities from text."""
    # Simple entity extraction
    entities = {
        "locations": [],
        "organizations": [],
        "people": [],
        "dates": []
    }
    
    # Simulated entity detection
    keywords = {
        "locations": ["New York", "London", "Tokyo", "Paris", "Berlin"],
        "organizations": ["Google", "Microsoft", "Amazon", "Apple", "Facebook"],
        "people": ["John", "Alice", "Bob", "Charlie", "Diana"],
        "dates": ["2024", "January", "February", "Q1", "Q2"]
    }
    
    for entity_type, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword.lower() in text.lower():
                entities[entity_type].append(keyword)
    
    return {
        "text": text,
        "entities": entities,
        "total_entities": sum(len(v) for v in entities.values())
    }


@tool_registry.register("calculate_complexity", "Calculate text complexity")
async def calculate_complexity(text: str) -> Dict[str, Any]:
    """Calculate text complexity metrics."""
    words = text.split()
    sentences = text.split(".")
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "average_word_length": round(avg_word_length, 2),
        "complexity_score": round(avg_word_length * len(sentences) / 10, 2)
    }


# ====================
# Agent Base Class
# ====================

class LangChainAgent(ABC):
    """Base class for LangChain agents."""
    
    def __init__(self, name: str, model: str, tools: Optional[List[str]] = None):
        self.name = name
        self.model = model
        self.tools = tools or []
        self.memory: List[Dict[str, Any]] = []
    
    def add_memory(self, role: str, content: str):
        """Add to agent memory."""
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content
        })
    
    def get_memory_context(self) -> str:
        """Get memory context for the agent."""
        context = ""
        for item in self.memory[-5:]:  # Last 5 items
            context += f"{item['role']}: {item['content']}\n"
        return context
    
    @abstractmethod
    async def process(self, input_text: str) -> Dict[str, Any]:
        """Process input and return response."""
        pass
    
    async def use_tool(self, tool_name: str, **kwargs) -> Any:
        """Use a tool."""
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not available"}
        
        tool = tool_registry.get_tool(tool_name)
        if not tool:
            return {"error": f"Tool {tool_name} not found"}
        
        return await tool.execute(**kwargs)


# ====================
# Specific Agent Implementations
# ====================

class ResearchAgent(LangChainAgent):
    """Agent for research and information gathering."""
    
    def __init__(self, model: str = "gpt-4"):
        super().__init__(
            name="ResearchAgent",
            model=model,
            tools=["search_information", "summarize_text", "extract_entities"]
        )
    
    async def process(self, input_text: str) -> Dict[str, Any]:
        """Process research request."""
        self.add_memory("user", input_text)
        
        # Step 1: Search
        search_result = await self.use_tool("search_information", query=input_text)
        self.add_memory("agent", f"Searched for: {input_text}")
        
        # Step 2: Extract entities
        entities = await self.use_tool("extract_entities", text=input_text)
        self.add_memory("agent", f"Extracted entities: {entities['total_entities']}")
        
        # Step 3: Summarize
        summary = await self.use_tool("summarize_text", text=input_text)
        self.add_memory("agent", f"Created summary of {summary['reduction_percentage']}% reduction")
        
        return {
            "agent": self.name,
            "model": self.model,
            "input": input_text,
            "search_results": search_result,
            "entities": entities,
            "summary": summary,
            "memory_items": len(self.memory)
        }


class AnalysisAgent(LangChainAgent):
    """Agent for analyzing and processing text."""
    
    def __init__(self, model: str = "gpt-4"):
        super().__init__(
            name="AnalysisAgent",
            model=model,
            tools=["analyze_sentiment", "calculate_complexity", "extract_entities"]
        )
    
    async def process(self, input_text: str) -> Dict[str, Any]:
        """Process analysis request."""
        self.add_memory("user", input_text)
        
        # Analyze sentiment
        sentiment = await self.use_tool("analyze_sentiment", text=input_text)
        self.add_memory("agent", f"Sentiment: {sentiment['sentiment']}")
        
        # Calculate complexity
        complexity = await self.use_tool("calculate_complexity", text=input_text)
        self.add_memory("agent", f"Complexity score: {complexity['complexity_score']}")
        
        # Extract entities
        entities = await self.use_tool("extract_entities", text=input_text)
        self.add_memory("agent", f"Found {entities['total_entities']} entities")
        
        return {
            "agent": self.name,
            "model": self.model,
            "input": input_text,
            "sentiment": sentiment,
            "complexity": complexity,
            "entities": entities,
            "memory_items": len(self.memory)
        }


class SummarizationAgent(LangChainAgent):
    """Agent specialized in text summarization."""
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        super().__init__(
            name="SummarizationAgent",
            model=model,
            tools=["summarize_text", "extract_entities", "analyze_sentiment"]
        )
    
    async def process(self, input_text: str) -> Dict[str, Any]:
        """Process summarization request."""
        self.add_memory("user", input_text)
        
        # Summarize
        summary = await self.use_tool("summarize_text", text=input_text, max_length=50)
        self.add_memory("agent", "Summarized text")
        
        # Get sentiment of original
        sentiment = await self.use_tool("analyze_sentiment", text=input_text)
        self.add_memory("agent", f"Original sentiment: {sentiment['sentiment']}")
        
        # Get sentiment of summary
        summary_sentiment = await self.use_tool(
            "analyze_sentiment", 
            text=summary['summary']
        )
        self.add_memory("agent", f"Summary sentiment: {summary_sentiment['sentiment']}")
        
        return {
            "agent": self.name,
            "model": self.model,
            "original_text": input_text,
            "summary": summary['summary'],
            "original_sentiment": sentiment,
            "summary_sentiment": summary_sentiment,
            "reduction": summary['reduction_percentage']
        }


# ====================
# Multi-Agent System
# ====================

class MultiAgentSystem:
    """Manages multiple agents working together."""
    
    def __init__(self):
        self.agents: Dict[str, LangChainAgent] = {
            "researcher": ResearchAgent(),
            "analyst": AnalysisAgent(),
            "summarizer": SummarizationAgent()
        }
        self.execution_log: List[Dict[str, Any]] = []
    
    async def process_with_agent(
        self, 
        agent_name: str, 
        input_text: str
    ) -> Dict[str, Any]:
        """Process input with a specific agent."""
        if agent_name not in self.agents:
            return {"error": f"Agent {agent_name} not found"}
        
        agent = self.agents[agent_name]
        result = await agent.process(input_text)
        
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "success": True
        })
        
        return result
    
    async def process_sequential(self, input_text: str) -> Dict[str, Any]:
        """Process input through all agents sequentially."""
        results = {}
        
        for agent_name in ["researcher", "analyst", "summarizer"]:
            try:
                result = await self.process_with_agent(agent_name, input_text)
                results[agent_name] = result
            except Exception as e:
                results[agent_name] = {"error": str(e)}
        
        return {
            "input": input_text,
            "agents_results": results,
            "execution_count": len(self.execution_log)
        }
    
    async def process_parallel(self, input_text: str) -> Dict[str, Any]:
        """Process input through all agents in parallel."""
        tasks = [
            self.process_with_agent(agent_name, input_text)
            for agent_name in self.agents.keys()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "input": input_text,
            "parallel_results": {
                agent_name: result
                for agent_name, result in zip(self.agents.keys(), results)
            },
            "agents_count": len(self.agents)
        }


# ====================
# Demo Functions
# ====================

async def demo_single_agent():
    """Demonstrate single agent usage."""
    print("\n=== Single Agent Demo ===\n")
    
    analyst = AnalysisAgent()
    text = "I absolutely love this product! It's amazing and works wonderfully. Great quality!"
    
    result = await analyst.process(text)
    print(f"Analysis Result:\n{json.dumps(result, indent=2)}")


async def demo_multi_agent_sequential():
    """Demonstrate multi-agent sequential processing."""
    print("\n=== Multi-Agent Sequential Demo ===\n")
    
    system = MultiAgentSystem()
    text = "Artificial intelligence is revolutionizing technology. ML algorithms improve continuously with data."
    
    result = await system.process_sequential(text)
    print(f"Sequential Results:\n{json.dumps(result, indent=2, default=str)}")


async def demo_multi_agent_parallel():
    """Demonstrate multi-agent parallel processing."""
    print("\n=== Multi-Agent Parallel Demo ===\n")
    
    system = MultiAgentSystem()
    text = "The new quantum computer is a breakthrough in computational power."
    
    result = await system.process_parallel(text)
    print(f"Parallel Results:\n{json.dumps(result, indent=2, default=str)}")


async def main():
    """Run all LangChain agent demos."""
    await demo_single_agent()
    await demo_multi_agent_sequential()
    await demo_multi_agent_parallel()


if __name__ == "__main__":
    asyncio.run(main())
