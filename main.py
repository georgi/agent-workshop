from agent import Agent
from tools import Calculator


def main():
    # Create an agent with an objective
    agent = Agent(objective="Help the user solve math problems", model="gpt-4o-mini")

    # Add tools to the agent
    calculator_tool = Calculator()
    agent.add_tool(calculator_tool)

    # Run the agent
    print("Starting agent with calculator tool...")
    result = agent.run("I need to calculate 25 * 13 and then divide by 5.2")

    # Print the final answer
    print("\nFinal Answer:")
    print(result[-1]["content"])


if __name__ == "__main__":
    main()
