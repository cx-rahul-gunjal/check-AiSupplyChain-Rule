"""
PyMongo with Agent patterns implementation.
Database-integrated agents using MongoDB and PyMongo.
"""

from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Any, Dict, List, Optional
import json
from datetime import datetime

class MongoDBAgent:
    """Agent that uses MongoDB for storage and retrieval."""
    
    def __init__(self, name: str, db_url: str = "mongodb://localhost:27017/", db_name: str = "agent_db"):
        self.name = name
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.agents_collection: Collection = self.db["agents"]
        self.tasks_collection: Collection = self.db["tasks"]
        self.memories_collection: Collection = self.db["memories"]
    
    def store_agent_state(self, state: Dict[str, Any]) -> str:
        """Store agent state in MongoDB."""
        state["agent_name"] = self.name
        state["timestamp"] = datetime.utcnow()
        
        result = self.agents_collection.insert_one(state)
        return str(result.inserted_id)
    
    def retrieve_agent_state(self, state_id: Optional[str] = None) -> Optional[Dict]:
        """Retrieve agent state from MongoDB."""
        if state_id:
            from bson.objectid import ObjectId
            return self.agents_collection.find_one({"_id": ObjectId(state_id)})
        else:
            # Get the latest state
            return self.agents_collection.find_one(
                {"agent_name": self.name},
                sort=[("timestamp", -1)]
            )
    
    def log_task(self, task_description: str, result: Any, success: bool) -> str:
        """Log a task execution to MongoDB."""
        task_record = {
            "agent_name": self.name,
            "description": task_description,
            "result": str(result),
            "success": success,
            "timestamp": datetime.utcnow()
        }
        
        result = self.tasks_collection.insert_one(task_record)
        return str(result.inserted_id)
    
    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """Retrieve task history from MongoDB."""
        tasks = list(
            self.tasks_collection.find(
                {"agent_name": self.name}
            ).sort("timestamp", -1).limit(limit)
        )
        
        # Convert ObjectId to string for JSON serialization
        for task in tasks:
            task["_id"] = str(task["_id"])
            task["timestamp"] = str(task["timestamp"])
        
        return tasks
    
    def store_memory(self, memory_type: str, content: Dict) -> str:
        """Store memory in MongoDB."""
        memory_record = {
            "agent_name": self.name,
            "type": memory_type,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        
        result = self.memories_collection.insert_one(memory_record)
        return str(result.inserted_id)
    
    def retrieve_memories(self, memory_type: Optional[str] = None) -> List[Dict]:
        """Retrieve memories from MongoDB."""
        query = {"agent_name": self.name}
        if memory_type:
            query["type"] = memory_type
        
        memories = list(
            self.memories_collection.find(query).sort("timestamp", -1)
        )
        
        # Convert ObjectId to string
        for memory in memories:
            memory["_id"] = str(memory["_id"])
            memory["timestamp"] = str(memory["timestamp"])
        
        return memories
    
    def execute_task(self, task_description: str) -> Dict[str, Any]:
        """Execute a task and log it."""
        try:
            # Simulate task execution
            result = f"Completed: {task_description}"
            success = True
            
            # Log to MongoDB
            task_id = self.log_task(task_description, result, success)
            
            return {
                "task_id": task_id,
                "description": task_description,
                "result": result,
                "success": success
            }
        except Exception as e:
            # Log failure
            task_id = self.log_task(task_description, str(e), False)
            
            return {
                "task_id": task_id,
                "description": task_description,
                "error": str(e),
                "success": False
            }
    
    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get statistics about the agent from MongoDB."""
        total_tasks = self.tasks_collection.count_documents({"agent_name": self.name})
        successful_tasks = self.tasks_collection.count_documents({
            "agent_name": self.name,
            "success": True
        })
        
        return {
            "agent_name": self.name,
            "total_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "success_rate": successful_tasks / total_tasks if total_tasks > 0 else 0,
            "total_memories": self.memories_collection.count_documents({"agent_name": self.name})
        }
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()

def run_mongodb_agent(agent_name: str, tasks: List[str]):
    """Run a MongoDB-integrated agent."""
    try:
        # Create agent
        agent = MongoDBAgent(
            name=agent_name,
            db_url="mongodb://localhost:27017/",
            db_name="agent_db"
        )
        
        print(f"=== {agent_name} Agent ===")
        
        # Execute tasks
        for task in tasks:
            print(f"\nExecuting: {task}")
            result = agent.execute_task(task)
            print(f"Result: {result}")
        
        # Store memory
        agent.store_memory("session", {
            "tasks_executed": len(tasks),
            "status": "completed"
        })
        
        # Get statistics
        print("\n=== Agent Statistics ===")
        stats = agent.get_agent_statistics()
        print(json.dumps(stats, indent=2))
        
        # Get task history
        print("\n=== Recent Task History ===")
        history = agent.get_task_history(limit=5)
        for task in history:
            print(f"- {task['description']}: {task['success']}")
        
        agent.close()
        return stats
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    tasks = [
        "Query database",
        "Process results",
        "Generate report",
        "Send notification"
    ]
    
    result = run_mongodb_agent("DataAgent", tasks)
