"""
Main orchestration module for AI-BOM-POC application.
Demonstrates integration of all components: MCP, LangChain, CrewAI, and PydanticAI.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

# Import application modules
from config import get_config, LoggerConfig
from mcp_clients import UnifiedMCPClient
from langchain_agents import MultiAgentSystem as LangChainMultiAgentSystem
from crewai_agents import Crew, LeaderAgent, AnalystAgent, SpecialistAgent, ExecutorAgent, ValidatorAgent, Task, AgentRole
from pydantic_agents import TypeSafeMultiAgentSystem, TextAnalysisAgent, DataProcessor, PredictionAgent, ClassificationAgent, ExtractionAgent
from models import ModelRegistry, ModelSelector, ModelCapability


# ====================
# Logger Setup
# ====================

def setup_logging(log_level: str = "INFO", debug: bool = False):
    """Setup logging for the application."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    return logging.getLogger(__name__)


logger = setup_logging()


# ====================
# Application Coordinator
# ====================

class AIBOMPOCApplication:
    """Main application class coordinating all AI components."""
    
    def __init__(self):
        self.config = get_config()
        self.start_time = datetime.now()
        self.execution_results: Dict[str, Any] = {}
        self.model_registry = ModelRegistry()
        self.model_selector = ModelSelector(self.model_registry)
        
        logger.info("Initializing AI-BOM-POC Application")
        logger.info(f"Environment: {self.config.environment.value}")
        logger.info(f"Debug: {self.config.debug}")
        logger.info(f"Loaded {len(self.model_registry.models)} AI models")
    
    async def demonstrate_mcp_client(self) -> Dict[str, Any]:
        """Demonstrate MCP client functionality."""
        logger.info("\n=== MCP Client Demonstration ===")
        
        if not self.config.is_feature_enabled("mcp_client"):
            logger.warning("MCP Client feature is disabled")
            return {"status": "disabled"}
        
        try:
            client = UnifiedMCPClient()
            
            workflow_config = {
                "search_query": "artificial intelligence breakthroughs",
                "max_results": 3,
                "text_to_analyze": "AI and machine learning are revolutionizing technology.",
                "cities": ["London", "Tokyo"],
                "data_to_process": {"category": "AI", "year": 2024},
                "operation": "aggregate",
                "numbers_to_calculate": [10, 20, 30, 40, 50]
            }
            
            logger.info("Executing MCP workflow...")
            results = await client.execute_workflow(workflow_config)
            
            logger.info("✓ MCP workflow completed successfully")
            return results
        
        except Exception as e:
            logger.error(f"✗ MCP Client error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def demonstrate_langchain_agents(self) -> Dict[str, Any]:
        """Demonstrate LangChain agent functionality."""
        logger.info("\n=== LangChain Agents Demonstration ===")
        
        if not self.config.is_feature_enabled("langchain_agents"):
            logger.warning("LangChain Agents feature is disabled")
            return {"status": "disabled"}
        
        try:
            system = LangChainMultiAgentSystem()
            
            text_input = "Artificial intelligence is transforming industries globally. It's an amazing technology!"
            
            logger.info("Processing input through LangChain agents...")
            results = await system.process_sequential(text_input)
            
            logger.info("✓ LangChain processing completed")
            return results
        
        except Exception as e:
            logger.error(f"✗ LangChain Agents error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def demonstrate_crewai_agents(self) -> Dict[str, Any]:
        """Demonstrate CrewAI crew functionality."""
        logger.info("\n=== CrewAI Agents Demonstration ===")
        
        if not self.config.is_feature_enabled("crewai_agents"):
            logger.warning("CrewAI Agents feature is disabled")
            return {"status": "disabled"}
        
        try:
            crew = Crew("AI-POC Team")
            
            # Add diverse agents
            crew.add_agent(LeaderAgent("ProjectManager"))
            crew.add_agent(AnalystAgent("DataAnalyst"))
            crew.add_agent(SpecialistAgent("AISpecialist", "Artificial Intelligence"))
            crew.add_agent(ExecutorAgent("Developer"))
            crew.add_agent(ValidatorAgent("QAEngineer"))
            
            # Create task workflow
            tasks = [
                Task(
                    "Business Requirements Analysis",
                    "Analyze and document business requirements",
                    AgentRole.ANALYST,
                    priority=3
                ),
                Task(
                    "AI Solution Design",
                    "Design AI solution architecture",
                    AgentRole.SPECIALIST,
                    priority=2
                ),
                Task(
                    "Implementation",
                    "Implement the AI solution",
                    AgentRole.EXECUTOR,
                    priority=1
                ),
                Task(
                    "Quality Assurance",
                    "Validate solution quality and performance",
                    AgentRole.VALIDATOR,
                    priority=1
                )
            ]
            
            for task in tasks:
                crew.add_task(task)
            
            logger.info("Executing CrewAI workflow...")
            results = await crew.execute_all_tasks()
            
            logger.info("✓ CrewAI workflow completed")
            return results
        
        except Exception as e:
            logger.error(f"✗ CrewAI Agents error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def demonstrate_pydantic_agents(self) -> Dict[str, Any]:
        """Demonstrate PydanticAI agent functionality."""
        logger.info("\n=== PydanticAI Agents Demonstration ===")
        
        if not self.config.is_feature_enabled("pydantic_agents"):
            logger.warning("PydanticAI Agents feature is disabled")
            return {"status": "disabled"}
        
        try:
            system = TypeSafeMultiAgentSystem()
            
            # Register agents
            system.register_agent(TextAnalysisAgent())
            system.register_agent(ClassificationAgent())
            system.register_agent(DataProcessor())
            system.register_agent(PredictionAgent())
            system.register_agent(ExtractionAgent())
            
            logger.info("Executing PydanticAI pipeline...")
            
            pipeline_config = {
                "text_analysis": {
                    "agent": "TextAnalyzer",
                    "input": "This is an excellent product with amazing features!"
                },
                "classification": {
                    "agent": "Classifier",
                    "input": "This product is wonderful and great!"
                },
                "extraction": {
                    "agent": "Extractor",
                    "input": "Apple Inc. announced new AI features."
                }
            }
            
            results = await system.execute_pipeline(pipeline_config)
            
            logger.info("✓ PydanticAI pipeline completed")
            return results
        
        except Exception as e:
            logger.error(f"✗ PydanticAI Agents error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def demonstrate_parallel_execution(self) -> Dict[str, Any]:
        """Demonstrate parallel execution across frameworks."""
        logger.info("\n=== Parallel Execution Demonstration ===")
        
        if not self.config.is_feature_enabled("parallel_execution"):
            logger.warning("Parallel Execution feature is disabled")
            return {"status": "disabled"}
        
        try:
            # Create multiple systems
            pydantic_system = TypeSafeMultiAgentSystem()
            pydantic_system.register_agent(TextAnalysisAgent())
            pydantic_system.register_agent(ClassificationAgent())
            pydantic_system.register_agent(DataProcessor())
            
            langchain_system = LangChainMultiAgentSystem()
            
            logger.info("Executing parallel tasks across frameworks...")
            
            tasks = [
                pydantic_system.execute_agent("TextAnalyzer", "Great product!"),
                pydantic_system.execute_agent("Classifier", "Amazing quality!"),
                langchain_system.process_sequential("AI is transforming the world."),
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            logger.info("✓ Parallel execution completed")
            return {
                "execution_type": "parallel",
                "total_tasks": len(tasks),
                "completed": sum(1 for r in results if not isinstance(r, Exception)),
                "results": [
                    r.to_dict() if hasattr(r, 'to_dict') else r
                    for r in results
                ]
            }
        
        except Exception as e:
            logger.error(f"✗ Parallel Execution error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def demonstrate_integrated_workflow(self) -> Dict[str, Any]:
        """Demonstrate an integrated workflow using multiple frameworks."""
        logger.info("\n=== Integrated Workflow Demonstration ===")
        
        try:
            # Step 1: PydanticAI for structured analysis
            logger.info("Step 1: Analyzing data with PydanticAI...")
            pydantic_system = TypeSafeMultiAgentSystem()
            pydantic_system.register_agent(TextAnalysisAgent())
            
            analysis_response = await pydantic_system.execute_agent(
                "TextAnalyzer",
                "AI technology is advancing rapidly with breakthrough innovations!"
            )
            
            # Step 2: LangChain for multi-step processing
            logger.info("Step 2: Processing with LangChain agents...")
            langchain_system = LangChainMultiAgentSystem()
            
            langchain_result = await langchain_system.process_sequential(
                "AI technology is advancing rapidly with breakthrough innovations!"
            )
            
            # Step 3: CrewAI for orchestrated execution
            logger.info("Step 3: Orchestrating with CrewAI crew...")
            crew = Crew("Integrated Team")
            crew.add_agent(AnalystAgent("Analyst"))
            crew.add_agent(SpecialistAgent("Specialist", "AI"))
            
            task1 = Task("Analyze Requirements", "Analyze findings", AgentRole.ANALYST, 2)
            task2 = Task("AI Implementation Plan", "Create implementation plan", AgentRole.SPECIALIST, 1)
            
            crew.add_task(task1)
            crew.add_task(task2)
            
            crew_result = await crew.execute_all_tasks()
            
            logger.info("✓ Integrated workflow completed successfully")
            
            return {
                "workflow_status": "completed",
                "steps": {
                    "pydantic_analysis": analysis_response.to_dict() if hasattr(analysis_response, 'to_dict') else analysis_response,
                    "langchain_processing": langchain_result,
                    "crewai_orchestration": crew_result
                }
            }
        
        except Exception as e:
            logger.error(f"✗ Integrated Workflow error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def demonstrate_models(self) -> Dict[str, Any]:
        """Demonstrate AI models and selection."""
        logger.info("\n=== AI Models Demonstration ===")
        
        try:
            # Get model registry info
            model_summary = self.model_registry.get_model_summary()
            
            logger.info(f"Loaded {model_summary['total_models']} AI models")
            
            # Test model execution
            gpt4 = self.model_registry.get_model("gpt4")
            claude3 = self.model_registry.get_model("claude3")
            llama2 = self.model_registry.get_model("llama2")
            
            test_prompt = "Explain artificial intelligence in 2 sentences."
            
            logger.info("Testing model inference...")
            gpt4_result = await gpt4.generate(test_prompt) if gpt4 else None
            claude3_result = await claude3.generate(test_prompt) if claude3 else None
            llama2_result = await llama2.generate(test_prompt) if llama2 else None
            
            # Test model selection
            code_models = self.model_registry.get_models_by_capability(ModelCapability.CODE_GENERATION)
            reasoning_models = self.model_registry.get_models_by_capability(ModelCapability.REASONING)
            
            logger.info("✓ Model demonstration completed")
            
            return {
                "status": "success",
                "models_loaded": model_summary,
                "test_results": {
                    "gpt4_tested": gpt4 is not None,
                    "claude3_tested": claude3 is not None,
                    "llama2_tested": llama2 is not None
                },
                "capability_analysis": {
                    "code_generation_models": code_models,
                    "reasoning_models": reasoning_models
                }
            }
        
        except Exception as e:
            logger.error(f"✗ Models error: {e}")
            return {"status": "error", "error": str(e)}
    
    async def run_all_demonstrations(self) -> Dict[str, Any]:
        """Run all demonstrations."""
        logger.info("=" * 60)
        logger.info("Starting AI-BOM-POC Application")
        logger.info("=" * 60)
        
        # Run all demonstrations
        results = {
            "timestamp": datetime.now().isoformat(),
            "config": self.config.get_summary(),
            "demonstrations": {}
        }
        
        # Run individual demonstrations
        if self.config.is_feature_enabled("mcp_client"):
            results["demonstrations"]["mcp_client"] = await self.demonstrate_mcp_client()
        
        if self.config.is_feature_enabled("langchain_agents"):
            results["demonstrations"]["langchain_agents"] = await self.demonstrate_langchain_agents()
        
        if self.config.is_feature_enabled("crewai_agents"):
            results["demonstrations"]["crewai_agents"] = await self.demonstrate_crewai_agents()
        
        if self.config.is_feature_enabled("pydantic_agents"):
            results["demonstrations"]["pydantic_agents"] = await self.demonstrate_pydantic_agents()
        
        # Run model demonstration
        results["demonstrations"]["models"] = await self.demonstrate_models()
        
        # Run integrated demonstrations
        if self.config.is_feature_enabled("parallel_execution"):
            results["demonstrations"]["parallel_execution"] = await self.demonstrate_parallel_execution()
        
        results["demonstrations"]["integrated_workflow"] = await self.demonstrate_integrated_workflow()
        
        # Add execution summary
        execution_time = (datetime.now() - self.start_time).total_seconds()
        results["execution_summary"] = {
            "total_execution_time_seconds": execution_time,
            "demonstrations_run": len(results["demonstrations"]),
            "completed_at": datetime.now().isoformat()
        }
        
        logger.info("=" * 60)
        logger.info("AI-BOM-POC Application Completed")
        logger.info(f"Total execution time: {execution_time:.2f} seconds")
        logger.info("=" * 60)
        
        return results


# ====================
# Utility Functions
# ====================

async def main():
    """Main entry point for the application."""
    app = AIBOMPOCApplication()
    
    try:
        # Run all demonstrations
        results = await app.run_all_demonstrations()
        
        # Print results
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        print(json.dumps(results, indent=2, default=str))
        print("=" * 60)
        
        return results
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}


def print_application_info():
    """Print application information."""
    config = get_config()
    
    print("\n" + "=" * 60)
    print("AI-BOM-POC Application Information")
    print("=" * 60)
    print(f"Environment: {config.environment.value}")
    print(f"Debug Mode: {config.debug}")
    print(f"Log Level: {config.log_level}")
    print("\nAvailable Components:")
    print(f"  Models: {len(config.models)}")
    print(f"  MCP Servers: {len(config.mcp_servers)}")
    print(f"  External APIs: {len(config.apis)}")
    print("\nEnabled Features:")
    for feature, enabled in config.features.items():
        status = "✓" if enabled else "✗"
        print(f"  {status} {feature}")
    print("=" * 60 + "\n")


# ====================
# Entry Point
# ====================

if __name__ == "__main__":
    # Print application info
    print_application_info()
    
    # Run the application
    results = asyncio.run(main())
    
    # Save results to file
    with open("application_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info("Results saved to application_results.json")
