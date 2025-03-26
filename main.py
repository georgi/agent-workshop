#!/usr/bin/env python3
import os
import readline
import atexit
from agent import Agent
from tools import Calculator, WebsiteFetcher, SerpApiSearch

# Set up readline with history file
HISTFILE = os.path.expanduser("~/.agent_chat_history")
HISTFILE_SIZE = 1000

# Make sure the history file exists
if not os.path.exists(HISTFILE):
    with open(HISTFILE, "w") as f:
        pass

# Load history if it exists
try:
    readline.read_history_file(HISTFILE)
    readline.set_history_length(HISTFILE_SIZE)
except FileNotFoundError:
    pass

# Save history on exit
atexit.register(readline.write_history_file, HISTFILE)


def initialize_agent():
    """Initialize the agent with tools"""
    print("Initializing agent...")

    # Create an agent with an objective
    agent = Agent(
        objective="Help the user solve problems using available tools",
        model="gpt-4o-mini",  # You can change this to use a different model
    )

    # Add tools to the agent
    agent.add_tool(Calculator())
    agent.add_tool(WebsiteFetcher())

    # Add the SerpAPI search tool if the API key is available
    try:
        agent.add_tool(SerpApiSearch())
        print("✓ Search tool initialized")
    except Exception as e:
        print(f"✗ Search tool not available: {e}")

    return agent


def display_response(response):
    """Display the agent's response in a readable format"""
    print("\n" + "=" * 80)
    print(response.content)
    print("=" * 80 + "\n")


def main():
    """Run the chat interface"""
    print("=" * 80)
    print("📢 Agent Chat Interface")
    print("=" * 80)
    print("Type 'exit', 'quit', or press Ctrl+D to exit.")
    print("Enter your message to interact with the agent.")
    print("=" * 80)

    agent = initialize_agent()

    while True:
        try:
            # Get user input with readline (with history support)
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            # Send the message to the agent
            print("\nAgent is thinking...")
            response = agent.send_message(user_input)

            # Display the response
            display_response(response)

        except EOFError:
            # Handle Ctrl+D
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C
            print("\nOperation interrupted. Type 'exit' to quit.")
            continue
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
