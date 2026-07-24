"""
Reflexion agent implementation.
Agent framework with self-reflection and memory for continuous improvement.
"""

from typing import Any, Dict, List
import json

class Memory:
    """Agent memory for storing experiences and reflections."""
    
    def __init__(self):
        self.trajectory = []
        self.reflections = []
        self.learned_patterns = {}
    
    def add_experience(self, action: str, result: Any, success: bool):
        """Add experience to memory."""
        experience = {
            "action": action,
            "result": result,
            "success": success
        }
        self.trajectory.append(experience)
    
    def add_reflection(self, reflection: str):
        """Add reflection on past experiences."""
        self.reflections.append(reflection)
    
    def store_pattern(self, pattern_name: str, pattern_data: Dict):
        """Store learned patterns."""
        self.learned_patterns[pattern_name] = pattern_data

class ReflexionAgent:
    """Agent that reflects on its actions and learns from them."""
    
    def __init__(self, name: str, model: str = "gpt-4"):
        self.name = name
        self.model = model
        self.memory = Memory()
    
    def take_action(self, action: str) -> Dict[str, Any]:
        """Take an action and store it."""
        # Simulate action execution
        success = len(action) > 0
        result = f"Executed: {action}"
        
        # Store in memory
        self.memory.add_experience(action, result, success)
        
        return {"action": action, "result": result, "success": success}
    
    def reflect(self) -> str:
        """Reflect on recent actions and experiences."""
        # Analyze trajectory
        recent_actions = self.memory.trajectory[-5:] if self.memory.trajectory else []
        
        reflection = f"Reflecting on {len(recent_actions)} recent actions. "
        
        successful_count = sum(1 for exp in recent_actions if exp["success"])
        reflection += f"Success rate: {successful_count}/{len(recent_actions) if recent_actions else 1}. "
        
        # Generate reflection
        if successful_count < len(recent_actions) / 2:
            reflection += "Need to adjust strategy for future attempts."
        else:
            reflection += "Current approach is working well."
        
        self.memory.add_reflection(reflection)
        return reflection
    
    def learn_pattern(self, pattern_name: str, actions: List[str]) -> bool:
        """Learn a pattern from successful action sequences."""
        pattern_data = {
            "sequence": actions,
            "learned_at": len(self.memory.trajectory),
            "success_count": 0
        }
        
        self.memory.store_pattern(pattern_name, pattern_data)
        return True
    
    def apply_learned_pattern(self, pattern_name: str) -> bool:
        """Apply a previously learned pattern."""
        if pattern_name in self.memory.learned_patterns:
            pattern = self.memory.learned_patterns[pattern_name]
            pattern["success_count"] += 1
            return True
        return False
    
    def get_memory_state(self) -> Dict:
        """Get current memory state for introspection."""
        return {
            "total_experiences": len(self.memory.trajectory),
            "successful_experiences": sum(1 for exp in self.memory.trajectory if exp["success"]),
            "total_reflections": len(self.memory.reflections),
            "learned_patterns": len(self.memory.learned_patterns)
        }

def run_reflexion_agent(task_sequence: List[str]):
    """Run a Reflexion agent through a task sequence."""
    agent = ReflexionAgent(name="ReflexionAgent", model="gpt-4")
    
    # Execute tasks
    for task in task_sequence:
        print(f"Executing task: {task}")
        result = agent.take_action(task)
        print(f"Result: {result}")
    
    # Reflect on performance
    print("\n--- Reflection Phase ---")
    reflection = agent.reflect()
    print(f"Agent reflection: {reflection}")
    
    # Learn patterns
    print("\n--- Learning Phase ---")
    agent.learn_pattern("successful_sequence", task_sequence)
    print(f"Pattern learned: successful_sequence")
    
    # Get memory state
    print("\n--- Memory State ---")
    memory_state = agent.get_memory_state()
    print(f"Memory: {json.dumps(memory_state, indent=2)}")
    
    return {
        "final_reflection": reflection,
        "memory_state": memory_state
    }

if __name__ == "__main__":
    tasks = [
        "Query the database",
        "Filter results by date",
        "Send summary email",
        "Log completion"
    ]
    
    result = run_reflexion_agent(tasks)
    print(f"\n=== Final Result ===")
    print(json.dumps(result, indent=2))
