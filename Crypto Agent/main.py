from agents import Agent, Runner, function_tool
from connection import config
import requests
import rich

# 🔧 Tool: Get crypto price
@function_tool
def get_crypto_price(symbol: str) -> str:
    """
    Get current price of cryptocurrency (e.g. BTCUSDT, ETHUSDT).
    """
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        response = requests.get(url)
        response.raise_for_status()
        price = response.json()["price"]
        return f"The current price of {symbol.upper()} is **${price}**."
    except Exception as e:
        return f"Failed to fetch price for {symbol.upper()}. Error: {e}"

# 🤖 Agent definition
crypto_agent = Agent(
    name="Crypto Data Agent",
    instructions="You provide real-time crypto prices using the Binance API.",
    tools=[get_crypto_price]
)

# 🧪 Main runner
def handle_message():
    prompt = "Display the price of ETHUSDT"
    
    result = Runner.run_sync(
        crypto_agent,
        input=prompt,
        run_config=config
    )

    rich.print("\n [bold yellow]User Prompt:[/bold yellow]", prompt)
    rich.print("\n [bold green]Output:[/bold green]", result.final_output)

# 🚀 Run the program
if __name__ == "__main__":
    handle_message()
