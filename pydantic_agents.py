"""
PydanticAI implementation for type-safe AI agents.
Demonstrates agents using Pydantic models for structured outputs.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod


# ====================
# Pydantic Models for Structured Outputs
# ====================

class TextAnalysisResult:
    """Model for text analysis results."""
    
    def __init__(
        self,
        text: str,
        word_count: int,
        character_count: int,
        sentiment: str,
        key_phrases: List[str]
    ):
        self.text = text
        self.word_count = word_count
        self.character_count = character_count
        self.sentiment = sentiment
        self.key_phrases = key_phrases
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "sentiment": self.sentiment,
            "key_phrases": self.key_phrases
        }


class DataProcessingResult:
    """Model for data processing results."""
    
    def __init__(
        self,
        input_count: int,
        output_count: int,
        processing_time: float,
        success: bool,
        data: Any
    ):
        self.input_count = input_count
        self.output_count = output_count
        self.processing_time = processing_time
        self.success = success
        self.data = data
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_count": self.input_count,
            "output_count": self.output_count,
            "processing_time": self.processing_time,
            "success": self.success,
            "data": self.data
        }


class PredictionResult:
    """Model for prediction results."""
    
    def __init__(
        self,
        prediction: Any,
        confidence: float,
        model_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.prediction = prediction
        self.confidence = confidence
        self.model_name = model_name
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prediction": self.prediction,
            "confidence": self.confidence,
            "model_name": self.model_name,
            "metadata": self.metadata
        }


class ClassificationResult:
    """Model for classification results."""
    
    def __init__(
        self,
        text: str,
        category: str,
        confidence: float,
        alternatives: Optional[List[Dict[str, float]]] = None
    ):
        self.text = text
        self.category = category
        self.confidence = confidence
        self.alternatives = alternatives or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "category": self.category,
            "confidence": self.confidence,
            "alternatives": self.alternatives
        }


class ExtractionResult:
    """Model for information extraction results."""
    
    def __init__(
        self,
        source_text: str,
        entities: Dict[str, List[str]],
        relationships: List[Dict[str, str]],
        confidence: float
    ):
        self.source_text = source_text
        self.entities = entities
        self.relationships = relationships
        self.confidence = confidence
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_text": self.source_text,
            "entities": self.entities,
            "relationships": self.relationships,
            "confidence": self.confidence
        }


class AgentResponse:
    """Model for agent responses."""
    
    def __init__(
        self,
        agent_name: str,
        task: str,
        result: Any,
        success: bool,
        execution_time: float,
        timestamp: Optional[str] = None
    ):
        self.agent_name = agent_name
        self.task = task
        self.result = result
        self.success = success
        self.execution_time = execution_time
        self.timestamp = timestamp or datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "task": self.task,
            "result": self.result,
            "success": self.success,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp
        }


# ====================
# Type Variable for Generic Agents
# ====================

T = TypeVar('T')


# ====================
# Base PydanticAI Agent
# ====================

class PydanticAIAgent(ABC, Generic[T]):
    """Base class for type-safe PydanticAI agents."""
    
    def __init__(
        self,
        name: str,
        model: str = "gpt-4",
        output_type: Optional[Type[T]] = None
    ):
        self.name = name
        self.model = model
        self.output_type = output_type
        self.execution_count = 0
        self.execution_history: List[Dict[str, Any]] = []
    
    async def process(self, input_data: Any) -> AgentResponse:
        """Process input and return typed response."""
        try:
            start_time = datetime.now()
            
            result = await self._execute(input_data)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            response = AgentResponse(
                agent_name=self.name,
                task=str(input_data)[:50],
                result=result.to_dict() if hasattr(result, 'to_dict') else result,
                success=True,
                execution_time=execution_time
            )
            
            self.execution_count += 1
            self.execution_history.append(response.to_dict())
            
            return response
        
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            response = AgentResponse(
                agent_name=self.name,
                task=str(input_data)[:50],
                result={"error": str(e)},
                success=False,
                execution_time=execution_time
            )
            
            self.execution_history.append(response.to_dict())
            return response
    
    @abstractmethod
    async def _execute(self, input_data: Any) -> T:
        """Execute the agent's logic."""
        pass
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get agent execution statistics."""
        successful = sum(1 for item in self.execution_history if item.get("success"))
        
        return {
            "agent_name": self.name,
            "model": self.model,
            "total_executions": self.execution_count,
            "successful_executions": successful,
            "failed_executions": self.execution_count - successful,
            "success_rate": successful / self.execution_count if self.execution_count > 0 else 0,
            "average_execution_time": sum(
                item.get("execution_time", 0) 
                for item in self.execution_history
            ) / len(self.execution_history) if self.execution_history else 0
        }


# ====================
# Specific PydanticAI Agent Implementations
# ====================

class TextAnalysisAgent(PydanticAIAgent[TextAnalysisResult]):
    """PydanticAI agent for text analysis."""
    
    def __init__(self, name: str = "TextAnalyzer"):
        super().__init__(name, output_type=TextAnalysisResult)
    
    async def _execute(self, text: str) -> TextAnalysisResult:
        """Analyze text and return structured result."""
        await asyncio.sleep(0.1)
        
        words = text.split()
        
        # Sentiment detection
        positive_words = ["good", "great", "excellent", "amazing"]
        negative_words = ["bad", "terrible", "awful", "horrible"]
        
        pos_count = sum(1 for word in words if word.lower() in positive_words)
        neg_count = sum(1 for word in words if word.lower() in negative_words)
        
        sentiment = "positive" if pos_count > neg_count else ("negative" if neg_count > pos_count else "neutral")
        
        # Extract key phrases (simulated)
        key_phrases = [word for word in set(words) if len(word) > 5][:5]
        
        return TextAnalysisResult(
            text=text,
            word_count=len(words),
            character_count=len(text),
            sentiment=sentiment,
            key_phrases=key_phrases
        )


class DataProcessor(PydanticAIAgent[DataProcessingResult]):
    """PydanticAI agent for data processing."""
    
    def __init__(self, name: str = "DataProcessor"):
        super().__init__(name, output_type=DataProcessingResult)
    
    async def _execute(self, data: List[Dict[str, Any]]) -> DataProcessingResult:
        """Process data and return structured result."""
        await asyncio.sleep(0.1)
        
        start_time = datetime.now()
        
        # Process data
        processed = [
            {**item, "processed": True, "timestamp": datetime.now().isoformat()}
            for item in data
        ]
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return DataProcessingResult(
            input_count=len(data),
            output_count=len(processed),
            processing_time=processing_time,
            success=True,
            data=processed
        )


class PredictionAgent(PydanticAIAgent[PredictionResult]):
    """PydanticAI agent for making predictions."""
    
    def __init__(self, name: str = "Predictor", model_name: str = "neural-net-v1"):
        super().__init__(name, output_type=PredictionResult)
        self.model_name = model_name
    
    async def _execute(self, features: Dict[str, float]) -> PredictionResult:
        """Make prediction based on features."""
        await asyncio.sleep(0.1)
        
        # Simulated prediction
        prediction = sum(features.values()) / len(features) if features else 0
        confidence = 0.85 + (len(features) * 0.01)  # Increase confidence with more features
        
        return PredictionResult(
            prediction=prediction,
            confidence=min(confidence, 0.99),
            model_name=self.model_name,
            metadata={"feature_count": len(features)}
        )


class ClassificationAgent(PydanticAIAgent[ClassificationResult]):
    """PydanticAI agent for classification tasks."""
    
    def __init__(self, name: str = "Classifier", categories: Optional[List[str]] = None):
        super().__init__(name, output_type=ClassificationResult)
        self.categories = categories or ["A", "B", "C", "D"]
    
    async def _execute(self, text: str) -> ClassificationResult:
        """Classify text into categories."""
        await asyncio.sleep(0.1)
        
        # Simple classification based on text length and content
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["bad", "negative", "terrible"]):
            category = "negative"
            confidence = 0.9
        elif any(word in text_lower for word in ["good", "positive", "great"]):
            category = "positive"
            confidence = 0.9
        else:
            category = "neutral"
            confidence = 0.7
        
        alternatives = [
            {cat: round(0.1 / (len(self.categories) - 1), 3)}
            for cat in self.categories if cat != category
        ]
        
        return ClassificationResult(
            text=text,
            category=category,
            confidence=confidence,
            alternatives=alternatives
        )


class ExtractionAgent(PydanticAIAgent[ExtractionResult]):
    """PydanticAI agent for information extraction."""
    
    def __init__(self, name: str = "Extractor"):
        super().__init__(name, output_type=ExtractionResult)
    
    async def _execute(self, text: str) -> ExtractionResult:
        """Extract information from text."""
        await asyncio.sleep(0.1)
        
        # Simulated entity extraction
        words = text.split()
        
        entities = {
            "nouns": [w for w in words if len(w) > 3],
            "numbers": [w for w in words if w.isdigit()],
            "organizations": [w for w in words if w.isupper() and len(w) > 2]
        }
        
        # Simulated relationship extraction
        relationships = [
            {"subject": "Agent", "predicate": "extracts", "object": "information"}
        ]
        
        return ExtractionResult(
            source_text=text,
            entities=entities,
            relationships=relationships,
            confidence=0.8
        )


# ====================
# Multi-Agent System with Type Safety
# ====================

class TypeSafeMultiAgentSystem:
    """Multi-agent system with type safety."""
    
    def __init__(self):
        self.agents: Dict[str, PydanticAIAgent] = {}
        self.execution_log: List[Dict[str, Any]] = []
    
    def register_agent(self, agent: PydanticAIAgent):
        """Register an agent."""
        self.agents[agent.name] = agent
        print(f"✓ Registered agent: {agent.name}")
    
    async def execute_agent(
        self,
        agent_name: str,
        input_data: Any
    ) -> AgentResponse:
        """Execute a specific agent."""
        if agent_name not in self.agents:
            return AgentResponse(
                agent_name=agent_name,
                task="unknown",
                result={"error": f"Agent {agent_name} not found"},
                success=False,
                execution_time=0
            )
        
        agent = self.agents[agent_name]
        response = await agent.process(input_data)
        
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "success": response.success
        })
        
        return response
    
    async def execute_pipeline(
        self,
        pipeline_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute agents in a pipeline."""
        results = {}
        
        for step_name, step_config in pipeline_config.items():
            agent_name = step_config.get("agent")
            input_data = step_config.get("input")
            
            response = await self.execute_agent(agent_name, input_data)
            results[step_name] = response.to_dict()
        
        return {
            "pipeline": "completed",
            "steps": results,
            "total_agents_used": len(set(s.get("agent") for s in pipeline_config.values()))
        }
    
    async def execute_agents_parallel(
        self,
        tasks: Dict[str, tuple]
    ) -> Dict[str, Any]:
        """Execute multiple agents in parallel."""
        execution_tasks = [
            self.execute_agent(agent_name, input_data)
            for agent_name, input_data in tasks.values()
        ]
        
        responses = await asyncio.gather(*execution_tasks)
        
        return {
            "execution_type": "parallel",
            "total_agents": len(tasks),
            "results": {
                name: response.to_dict()
                for name, response in zip(tasks.keys(), responses)
            }
        }
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system-wide statistics."""
        stats = {}
        
        for agent_name, agent in self.agents.items():
            stats[agent_name] = agent.get_statistics()
        
        return {
            "agents": stats,
            "total_agents": len(self.agents),
            "total_executions": len(self.execution_log),
            "successful_executions": sum(
                1 for log in self.execution_log if log.get("success")
            )
        }


# ====================
# Demo Functions
# ====================

async def demo_single_agent():
    """Demonstrate single agent with type safety."""
    print("\n=== Single PydanticAI Agent Demo ===\n")
    
    agent = TextAnalysisAgent("TextAnalyzer-1")
    
    text = "This is an excellent product! I absolutely love it. The quality is amazing and the service is great!"
    response = await agent.process(text)
    
    print(f"Response:\n{json.dumps(response.to_dict(), indent=2)}")
    print(f"\nAgent Statistics:\n{json.dumps(agent.get_statistics(), indent=2)}")


async def demo_multi_agent_pipeline():
    """Demonstrate multi-agent pipeline."""
    print("\n=== Multi-Agent Pipeline Demo ===\n")
    
    system = TypeSafeMultiAgentSystem()
    
    # Register agents
    system.register_agent(TextAnalysisAgent())
    system.register_agent(ClassificationAgent())
    system.register_agent(ExtractionAgent())
    
    # Define pipeline
    pipeline_config = {
        "step_1_analyze": {
            "agent": "TextAnalyzer",
            "input": "This is a wonderful product with great features!"
        },
        "step_2_classify": {
            "agent": "Classifier",
            "input": "This is an excellent product!"
        },
        "step_3_extract": {
            "agent": "Extractor",
            "input": "Apple Inc. announced new products today."
        }
    }
    
    results = await system.execute_pipeline(pipeline_config)
    print(f"Pipeline Results:\n{json.dumps(results, indent=2)}")


async def demo_parallel_execution():
    """Demonstrate parallel agent execution."""
    print("\n=== Parallel Execution Demo ===\n")
    
    system = TypeSafeMultiAgentSystem()
    
    # Register agents
    system.register_agent(TextAnalysisAgent())
    system.register_agent(DataProcessor())
    system.register_agent(PredictionAgent())
    system.register_agent(ClassificationAgent())
    
    # Define parallel tasks
    tasks = {
        "text_analysis": ("TextAnalyzer", "Great product with excellent quality!"),
        "data_processing": ("DataProcessor", [{"value": 10}, {"value": 20}, {"value": 30}]),
        "prediction": ("Predictor", {"feature_1": 0.5, "feature_2": 0.7}),
        "classification": ("Classifier", "This product is amazing!")
    }
    
    results = await system.execute_agents_parallel(tasks)
    print(f"Parallel Execution Results:\n{json.dumps(results, indent=2, default=str)}")
    
    # Print system statistics
    stats = system.get_system_statistics()
    print(f"\nSystem Statistics:\n{json.dumps(stats, indent=2)}")


async def main():
    """Run all PydanticAI demos."""
    await demo_single_agent()
    await demo_multi_agent_pipeline()
    await demo_parallel_execution()


if __name__ == "__main__":
    asyncio.run(main())
