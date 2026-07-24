"""
Semantic Kernel agent implementation.
Microsoft's orchestration framework for AI agents.
"""

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.core_plugins import TextPlugin

# Initialize kernel
kernel = sk.Kernel()

# Add OpenAI chat completion
kernel.add_service(
    OpenAIChatCompletion(
        model_id="gpt-4",
        api_key="YOUR_API_KEY"
    )
)

# Create a plugin with semantic functions
@sk.kernel_function(
    description="Get weather information for a location"
)
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

@sk.kernel_function(
    description="Get real-time stock prices"
)
def get_stock_price(symbol: str) -> str:
    """Get stock price."""
    return f"Stock price for {symbol}: $150.50"

@sk.kernel_function(
    description="Perform text analysis"
)
def analyze_text(text: str) -> str:
    """Analyze text."""
    return f"Analysis of text: {len(text)} characters, sentiment: positive"

# Register plugin
plugin = sk.KernelPlugin(
    name="utilities",
    functions=[get_weather, get_stock_price, analyze_text]
)
kernel.add_plugin(plugin)

# Add text plugin
kernel.add_plugin(TextPlugin())

async def run_semantic_kernel_agent(user_message: str):
    """Run the Semantic Kernel agent."""
    try:
        # Create a chat prompt
        chat_function = kernel.add_function(
            plugin_name="chat",
            function_name="chat",
            prompt="You are a helpful AI assistant. {{$input}}"
        )
        
        # Run the agent
        result = await kernel.invoke_async(
            chat_function,
            input=user_message
        )
        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(
        run_semantic_kernel_agent("What's the weather in New York and the stock price of AAPL?")
    )
    print(f"Semantic Kernel Response: {result}")
