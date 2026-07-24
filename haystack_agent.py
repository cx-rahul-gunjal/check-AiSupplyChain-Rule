"""
Haystack agent implementation.
Deepset's production-grade framework for AI agents and pipelines.
"""

from haystack import Pipeline, component
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack.document_stores import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever

document_store = InMemoryDocumentStore()

# Define tool components
@component
class DataQueryComponent:
    @component.output_types(result=str)
    def run(self, query: str) -> dict:
        """Execute a data query."""
        return {"result": f"Query results for: {query}"}

@component
class CalculatorComponent:
    @component.output_types(answer=int)
    def run(self, expression: str) -> dict:
        """Perform a calculation."""
        try:
            result = eval(expression)
            return {"answer": result}
        except Exception as e:
            return {"answer": 0}

@component
class DataValidationComponent:
    @component.output_types(validated=str)
    def run(self, data: str) -> dict:
        """Validate data."""
        return {"validated": f"Data validated: {data}"}

def run_haystack_agent(user_query: str):
    """Run the Haystack agent pipeline."""
    # Create pipeline
    pipeline = Pipeline()
    
    # Add components
    query_component = DataQueryComponent()
    calculator = CalculatorComponent()
    validator = DataValidationComponent()
    
    prompt_builder = PromptBuilder(
        template="Answer this query: {{query}}"
    )
    
    generator = OpenAIGenerator(
        model="gpt-4",
        api_key="YOUR_API_KEY"
    )
    
    # Add to pipeline
    pipeline.add_component("query_component", query_component)
    pipeline.add_component("calculator", calculator)
    pipeline.add_component("validator", validator)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("generator", generator)
    
    # Connect components
    pipeline.connect("query_component.result", "validator.data")
    pipeline.connect("validator.validated", "prompt_builder.query")
    pipeline.connect("prompt_builder.prompt", "generator.prompt")
    
    # Run pipeline
    try:
        result = pipeline.run({
            "query_component": {"query": user_query},
            "calculator": {"expression": "10 + 5"}
        })
        return result
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    result = run_haystack_agent("Find all users with premium membership")
    print(f"Haystack Response: {result}")
