from agent import Agent
from tools import Calculator, WebsiteFetcher


def main():
    # Create an agent with an objective
    agent = Agent(
        objective="Help the user solve math problems and fetch website content",
        model="gpt-4o-mini",
    )

    # Add tools to the agent
    calculator_tool = Calculator()
    website_fetcher_tool = WebsiteFetcher()
    agent.add_tool(calculator_tool)
    agent.add_tool(website_fetcher_tool)

    # Run the agent
    print("Starting agent with calculator and website fetcher tools...")
    initial_prompt = """
    You have two tools available:
    1. A calculator for math operations
    2. A website fetcher to get content from URLs
    
    Please show me how to use both tools. First calculate 25 * 13 and then divide by 5.2.
    Then fetch the content from https://example.com.
    """
    result = agent.run(initial_prompt)

    # Print the final answer
    print("\nFinal Answer:")
    print(result[-1]["content"])


if __name__ == "__main__":
    main()
