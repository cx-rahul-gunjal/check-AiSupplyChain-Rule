"""
AgentGPT pattern implementation.
Open-source agent architecture with goal-driven behavior.
"""

from typing import Any, Dict, List, Optional
import json
from enum import Enum

class AgentGoalType(Enum):
    """Types of goals an agent can have."""
    TASK_COMPLETION = "task_completion"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    AUTOMATION = "automation"

class AgentGPTAgent:
    """Agent implementation following AgentGPT architecture."""
    
    def __init__(self, agent_id: str, name: str, goal: str, role: str):
        self.agent_id = agent_id
        self.name = name
        self.goal = goal
        self.role = role
        self.tasks: List[Dict] = []
        self.completed_tasks: List[Dict] = []
        self.memory: Dict[str, Any] = {}
    
    def add_task(self, task_description: str, priority: int = 1) -> str:
        """Add a task to the agent's task queue."""
        task = {
            "id": f"task_{len(self.tasks) + 1}",
            "description": task_description,
            "priority": priority,
            "status": "pending",
            "result": None
        }
        self.tasks.append(task)
        return task["id"]
    
    def get_next_task(self) -> Optional[Dict]:
        """Get the next task to execute (highest priority)."""
        if not self.tasks:
            return None
        
        # Sort by priority
        self.tasks.sort(key=lambda x: x["priority"], reverse=True)
        return self.tasks[0] if self.tasks else None
    
    def execute_task(self, task_id: str) -> bool:
        """Execute a task."""
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        
        if not task:
            return False
        
        # Simulate task execution
        task["status"] = "completed"
        task["result"] = f"Result of: {task['description']}"
        
        # Move to completed
        self.tasks.remove(task)
        self.completed_tasks.append(task)
        
        # Store in memory
        self.memory[f"completed_{task_id}"] = task["result"]
        
        return True
    
    def think(self) -> str:
        """Agent thinking/reasoning about the goal."""
        thought = f"Analyzing goal: {self.goal}\n"
        thought += f"Role: {self.role}\n"
        thought += f"Pending tasks: {len(self.tasks)}\n"
        thought += f"Completed tasks: {len(self.completed_tasks)}"
        return thought
    
    def act(self, action_description: str) -> Dict[str, Any]:
        """Perform an action towards the goal."""
        return {
            "agent_id": self.agent_id,
            "action": action_description,
            "timestamp": "now",
            "status": "executed"
        }
    
    def run_cycle(self) -> bool:
        """Run one cycle of think-act-observe."""
        # Think
        thought = self.think()
        print(f"Thought: {thought}\n")
        
        # Get next task
        next_task = self.get_next_task()
        
        if not next_task:
            return False
        
        # Act
        action_result = self.act(next_task["description"])
        print(f"Action: {json.dumps(action_result, indent=2)}\n")
        
        # Execute
        self.execute_task(next_task["id"])
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "goal": self.goal,
            "role": self.role,
            "pending_tasks": len(self.tasks),
            "completed_tasks": len(self.completed_tasks),
            "progress": f"{len(self.completed_tasks)}/{len(self.completed_tasks) + len(self.tasks)}" if (len(self.completed_tasks) + len(self.tasks)) > 0 else "0/0"
        }

class AgentGPTOrchestrator:
    """Orchestrator for managing multiple AgentGPT agents."""
    
    def __init__(self):
        self.agents: Dict[str, AgentGPTAgent] = {}
    
    def create_agent(self, agent_id: str, name: str, goal: str, role: str) -> AgentGPTAgent:
        """Create a new agent."""
        agent = AgentGPTAgent(agent_id, name, goal, role)
        self.agents[agent_id] = agent
        return agent
    
    def delegate_task(self, agent_id: str, task_description: str):
        """Delegate a task to an agent."""
        if agent_id in self.agents:
            self.agents[agent_id].add_task(task_description)
    
    def run_all_agents(self):
        """Run all agents."""
        print("=== Agent Orchestrator Running ===\n")
        
        for agent_id, agent in self.agents.items():
            print(f"--- Running {agent.name} ---")
            
            while agent.run_cycle():
                pass
            
            print(f"\nStatus: {json.dumps(agent.get_status(), indent=2)}\n")
    
    def get_overall_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return {
            "total_agents": len(self.agents),
            "agents": [agent.get_status() for agent in self.agents.values()]
        }

def run_agentgpt_simulation():
    """Run an AgentGPT simulation."""
    # Create orchestrator
    orchestrator = AgentGPTOrchestrator()
    
    # Create agents with specific goals
    research_agent = orchestrator.create_agent(
        agent_id="agent_1",
        name="Research Agent",
        goal="Find information about AI trends",
        role="Researcher"
    )
    
    analysis_agent = orchestrator.create_agent(
        agent_id="agent_2",
        name="Analysis Agent",
        goal="Analyze collected information",
        role="Analyst"
    )
    
    # Delegate tasks
    orchestrator.delegate_task("agent_1", "Search for AI trends 2024")
    orchestrator.delegate_task("agent_1", "Compile sources")
    orchestrator.delegate_task("agent_2", "Analyze trends")
    orchestrator.delegate_task("agent_2", "Generate report")
    
    # Run agents
    orchestrator.run_all_agents()
    
    # Get final status
    print("\n=== Overall Status ===")
    status = orchestrator.get_overall_status()
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    run_agentgpt_simulation()
