"""
CrewAI implementation for multi-agent collaboration.
Demonstrates structured crews with different roles and responsibilities.
"""

import asyncio
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import json


# ====================
# Role Definitions
# ====================

class AgentRole(Enum):
    """Available agent roles in the crew."""
    LEADER = "Leader"
    ANALYST = "Analyst"
    SPECIALIST = "Specialist"
    EXECUTOR = "Executor"
    VALIDATOR = "Validator"


# ====================
# Task System
# ====================

class Task:
    """Represents a task to be executed by agents."""
    
    def __init__(
        self,
        name: str,
        description: str,
        required_role: AgentRole,
        priority: int = 1,
        dependencies: Optional[List[str]] = None
    ):
        self.name = name
        self.description = description
        self.required_role = required_role
        self.priority = priority
        self.dependencies = dependencies or []
        self.status = "pending"
        self.result = None
        self.created_at = datetime.now()
    
    def mark_completed(self, result: Any):
        """Mark task as completed with a result."""
        self.status = "completed"
        self.result = result
    
    def mark_failed(self, error: str):
        """Mark task as failed."""
        self.status = "failed"
        self.result = {"error": error}


# ====================
# Crew Agent
# ====================

class CrewAgent(ABC):
    """Base class for agents in a crew."""
    
    def __init__(
        self,
        name: str,
        role: AgentRole,
        model: str = "gpt-4",
        expertise: Optional[List[str]] = None
    ):
        self.name = name
        self.role = role
        self.model = model
        self.expertise = expertise or []
        self.executed_tasks: List[str] = []
        self.performance_score = 1.0
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task."""
        try:
            if task.required_role != self.role:
                return {
                    "success": False,
                    "error": f"Role mismatch: {self.role.value} cannot execute {task.required_role.value} task"
                }
            
            result = await self._perform_task(task)
            task.mark_completed(result)
            self.executed_tasks.append(task.name)
            
            return {"success": True, "result": result}
        except Exception as e:
            task.mark_failed(str(e))
            return {"success": False, "error": str(e)}
    
    @abstractmethod
    async def _perform_task(self, task: Task) -> Any:
        """Perform the actual task logic."""
        pass
    
    def get_summary(self) -> Dict[str, Any]:
        """Get agent summary."""
        return {
            "name": self.name,
            "role": self.role.value,
            "model": self.model,
            "expertise": self.expertise,
            "tasks_completed": len(self.executed_tasks),
            "performance_score": self.performance_score
        }


# ====================
# Specific Agent Types
# ====================

class LeaderAgent(CrewAgent):
    """Leader agent that coordinates the crew."""
    
    def __init__(self, name: str = "Captain"):
        super().__init__(
            name=name,
            role=AgentRole.LEADER,
            expertise=["coordination", "planning", "decision-making"]
        )
    
    async def _perform_task(self, task: Task) -> Any:
        """Lead and coordinate tasks."""
        await asyncio.sleep(0.1)
        return {
            "action": "coordinate",
            "task": task.name,
            "strategy": "Break task into subtasks and delegate",
            "assigned_to": "team"
        }


class AnalystAgent(CrewAgent):
    """Analyst agent for data analysis and insights."""
    
    def __init__(self, name: str = "Analyst"):
        super().__init__(
            name=name,
            role=AgentRole.ANALYST,
            expertise=["data-analysis", "insights", "reporting"]
        )
    
    async def _perform_task(self, task: Task) -> Any:
        """Analyze and provide insights."""
        await asyncio.sleep(0.1)
        return {
            "analysis": f"Analysis of {task.name}",
            "insights": [
                "Key insight 1",
                "Key insight 2",
                "Key insight 3"
            ],
            "confidence": 0.85
        }


class SpecialistAgent(CrewAgent):
    """Specialist agent with domain expertise."""
    
    def __init__(self, name: str = "Specialist", specialty: str = "General"):
        super().__init__(
            name=name,
            role=AgentRole.SPECIALIST,
            expertise=[specialty, "domain-knowledge", "technical-skills"]
        )
        self.specialty = specialty
    
    async def _perform_task(self, task: Task) -> Any:
        """Execute specialized tasks."""
        await asyncio.sleep(0.1)
        return {
            "specialty": self.specialty,
            "execution": f"Specialized execution of {task.name}",
            "technical_details": {
                "approach": "Domain-specific methodology",
                "complexity": "medium",
                "estimated_time": "2 hours"
            }
        }


class ExecutorAgent(CrewAgent):
    """Executor agent that performs actionable tasks."""
    
    def __init__(self, name: str = "Executor"):
        super().__init__(
            name=name,
            role=AgentRole.EXECUTOR,
            expertise=["execution", "automation", "implementation"]
        )
    
    async def _perform_task(self, task: Task) -> Any:
        """Execute and implement tasks."""
        await asyncio.sleep(0.1)
        return {
            "execution_status": "completed",
            "task": task.name,
            "actions_taken": [
                f"Action 1: {task.name}",
                f"Action 2: Verification",
                f"Action 3: Completion"
            ],
            "artifacts": ["result_1", "result_2"]
        }


class ValidatorAgent(CrewAgent):
    """Validator agent that validates results and quality."""
    
    def __init__(self, name: str = "Validator"):
        super().__init__(
            name=name,
            role=AgentRole.VALIDATOR,
            expertise=["validation", "quality-assurance", "verification"]
        )
    
    async def _perform_task(self, task: Task) -> Any:
        """Validate and verify task results."""
        await asyncio.sleep(0.1)
        return {
            "validation_status": "passed",
            "task": task.name,
            "checks": {
                "completeness": True,
                "accuracy": True,
                "compliance": True
            },
            "quality_score": 0.95,
            "recommendations": []
        }


# ====================
# Crew Management
# ====================

class Crew:
    """Manages a crew of agents working together."""
    
    def __init__(self, name: str = "Default Crew"):
        self.name = name
        self.agents: Dict[AgentRole, List[CrewAgent]] = {}
        self.tasks: List[Task] = []
        self.execution_log: List[Dict[str, Any]] = []
        self.completed_tasks: List[Task] = []
    
    def add_agent(self, agent: CrewAgent):
        """Add an agent to the crew."""
        role = agent.role
        if role not in self.agents:
            self.agents[role] = []
        self.agents[role].append(agent)
        print(f"✓ Added {agent.name} ({role.value}) to crew")
    
    def add_task(self, task: Task):
        """Add a task to the crew."""
        self.tasks.append(task)
        print(f"✓ Added task: {task.name}")
    
    def get_agent_for_task(self, task: Task) -> Optional[CrewAgent]:
        """Get an agent that can execute the task."""
        if task.required_role not in self.agents:
            return None
        
        agents = self.agents[task.required_role]
        return agents[0] if agents else None
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a single task."""
        agent = self.get_agent_for_task(task)
        
        if not agent:
            return {
                "success": False,
                "error": f"No agent available for role {task.required_role.value}"
            }
        
        result = await agent.execute_task(task)
        
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "task": task.name,
            "agent": agent.name,
            "success": result["success"]
        })
        
        if result["success"]:
            self.completed_tasks.append(task)
        
        return result
    
    async def execute_all_tasks(self) -> Dict[str, Any]:
        """Execute all tasks in the crew."""
        results = {}
        
        # Sort tasks by priority
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority, reverse=True)
        
        for task in sorted_tasks:
            result = await self.execute_task(task)
            results[task.name] = result
        
        return {
            "crew": self.name,
            "total_tasks": len(self.tasks),
            "completed_tasks": len(self.completed_tasks),
            "success_rate": len(self.completed_tasks) / len(self.tasks) if self.tasks else 0,
            "results": results
        }
    
    async def execute_tasks_parallel(self) -> Dict[str, Any]:
        """Execute all tasks in parallel."""
        tasks_to_execute = [task for task in self.tasks if task.status == "pending"]
        
        # Create tasks for all agents
        execution_tasks = [
            self.execute_task(task) for task in tasks_to_execute
        ]
        
        results = await asyncio.gather(*execution_tasks, return_exceptions=True)
        
        return {
            "crew": self.name,
            "execution_type": "parallel",
            "total_tasks": len(tasks_to_execute),
            "completed_tasks": len(self.completed_tasks),
            "execution_log_items": len(self.execution_log)
        }
    
    def get_crew_status(self) -> Dict[str, Any]:
        """Get status of the crew."""
        return {
            "crew_name": self.name,
            "agents": {
                role.value: [agent.get_summary() for agent in agents]
                for role, agents in self.agents.items()
            },
            "total_agents": sum(len(agents) for agents in self.agents.values()),
            "total_tasks": len(self.tasks),
            "completed_tasks": len(self.completed_tasks),
            "execution_log_items": len(self.execution_log)
        }


# ====================
# Demo Functions
# ====================

async def demo_basic_crew():
    """Demonstrate basic crew functionality."""
    print("\n=== Basic Crew Demo ===\n")
    
    # Create crew
    crew = Crew("Alpha Team")
    
    # Add agents
    crew.add_agent(LeaderAgent("Commander"))
    crew.add_agent(AnalystAgent("DataAnalyst"))
    crew.add_agent(SpecialistAgent("MLSpecialist", "Machine Learning"))
    crew.add_agent(ExecutorAgent("Developer"))
    crew.add_agent(ValidatorAgent("QA"))
    
    # Create and add tasks
    crew.add_task(Task(
        "Analyze Requirements",
        "Analyze project requirements",
        AgentRole.ANALYST,
        priority=3
    ))
    crew.add_task(Task(
        "Design Solution",
        "Design technical solution",
        AgentRole.SPECIALIST,
        priority=2,
        dependencies=["Analyze Requirements"]
    ))
    crew.add_task(Task(
        "Implement Solution",
        "Implement the designed solution",
        AgentRole.EXECUTOR,
        priority=1,
        dependencies=["Design Solution"]
    ))
    crew.add_task(Task(
        "Validate Results",
        "Validate the implementation",
        AgentRole.VALIDATOR,
        priority=1,
        dependencies=["Implement Solution"]
    ))
    
    # Execute all tasks
    results = await crew.execute_all_tasks()
    print(f"Crew Execution Results:\n{json.dumps(results, indent=2)}")
    
    # Print crew status
    status = crew.get_crew_status()
    print(f"\nCrew Status:\n{json.dumps(status, indent=2)}")


async def demo_parallel_execution():
    """Demonstrate parallel task execution."""
    print("\n=== Parallel Execution Demo ===\n")
    
    crew = Crew("Beta Team")
    
    # Add multiple agents of different roles
    crew.add_agent(LeaderAgent("Leader"))
    crew.add_agent(AnalystAgent("Analyst1"))
    crew.add_agent(AnalystAgent("Analyst2"))
    crew.add_agent(SpecialistAgent("DataScientist", "Data Science"))
    crew.add_agent(SpecialistAgent("Engineer", "Software Engineering"))
    
    # Add independent tasks
    for i in range(5):
        crew.add_task(Task(
            f"Analysis Task {i+1}",
            f"Independent analysis task {i+1}",
            AgentRole.ANALYST,
            priority=1
        ))
    
    # Execute in parallel
    results = await crew.execute_tasks_parallel()
    print(f"Parallel Execution Results:\n{json.dumps(results, indent=2)}")


async def demo_crew_workflow():
    """Demonstrate complex crew workflow."""
    print("\n=== Complex Crew Workflow Demo ===\n")
    
    crew = Crew("Gamma Team")
    
    # Build crew with specialized agents
    crew.add_agent(LeaderAgent("ProjectLead"))
    crew.add_agent(AnalystAgent("BusinessAnalyst"))
    crew.add_agent(SpecialistAgent("MLEngineer", "ML/AI"))
    crew.add_agent(SpecialistAgent("DataEngineer", "Data Engineering"))
    crew.add_agent(ExecutorAgent("DevOps"))
    crew.add_agent(ValidatorAgent("TestEngineer"))
    
    # Define workflow
    workflow_tasks = [
        Task("Requirements Gathering", "Gather and document requirements", AgentRole.ANALYST, 3),
        Task("Data Preparation", "Prepare and clean data", AgentRole.SPECIALIST, 2),
        Task("Model Development", "Develop ML models", AgentRole.SPECIALIST, 2),
        Task("Deployment", "Deploy solution to production", AgentRole.EXECUTOR, 1),
        Task("Testing & Validation", "Run tests and validation", AgentRole.VALIDATOR, 1)
    ]
    
    for task in workflow_tasks:
        crew.add_task(task)
    
    # Execute workflow
    results = await crew.execute_all_tasks()
    print(f"Workflow Results:\n{json.dumps(results, indent=2)}")


async def main():
    """Run all CrewAI demos."""
    await demo_basic_crew()
    await demo_parallel_execution()
    await demo_crew_workflow()


if __name__ == "__main__":
    asyncio.run(main())
