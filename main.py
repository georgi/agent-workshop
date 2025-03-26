from agent import Agent
from tools import Calculator, WebsiteFetcher, SerpApiSearch


def main():
    # Create an agent with an objective
    agent = Agent(
        objective="Help the user solve math problems, fetch website content, and search the web",
        model="gpt-4o-mini",
    )

    # Add tools to the agent
    calculator_tool = Calculator()
    website_fetcher_tool = WebsiteFetcher()

    # Add the new SerpAPI search tool - requires API key as env var or parameter
    # Uncomment below to use with direct API key (not recommended for production)
    # serp_api_tool = SerpApiSearch(api_key="your_api_key_here")

    # Recommended: Use environment variable SERPAPI_API_KEY
    serp_api_tool = SerpApiSearch()

    agent.add_tool(calculator_tool)
    agent.add_tool(website_fetcher_tool)
    agent.add_tool(serp_api_tool)

    # Run the agent
    print("Starting agent with calculator, website fetcher, and Google search tools...")
    initial_prompt = """
    You have three tools available:
    1. A calculator for math operations
    2. A website fetcher to get content from URLs
    3. A Google search tool to search the web
    
    Please show me how to use all three tools. First calculate 25 * 13 and then divide by 5.2.
    Then fetch the content from https://example.com.
    Finally, search for "Python programming best practices".
    """
    result = agent.run(initial_prompt)

    # Print the final answer
    print("\nFinal Answer:")
    print(result[-1]["content"])


if __name__ == "__main__":
    main()
