#!/usr/bin/env python3
import os
import readline
import atexit
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table
from agent import Agent
from tools import Calculator, WebsiteFetcher, SerpApiSearch

# Set up console
console = Console()

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
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Initializing agent...[/bold blue]"),
        transient=True,
    ) as progress:
        task = progress.add_task("", total=None)

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
            progress.update(
                task, description="[bold green]✓ Search tool initialized[/bold green]"
            )
            time.sleep(0.5)  # Brief pause for visual effect
        except Exception as e:
            progress.update(
                task,
                description=f"[bold red]✗ Search tool not available: {e}[/bold red]",
            )
            time.sleep(0.5)  # Brief pause for visual effect

    return agent


def display_response(response):
    """Display the agent's response in a readable format"""
    text = Text(response.content)
    panel = Panel(
        text,
        title="[bold cyan]AGENT RESPONSE[/bold cyan]",
        border_style="cyan",
        expand=False,
        padding=(1, 2),
    )
    console.print(panel)


def display_tool_usage(response):
    """Display information about tools used in the response"""
    if hasattr(response, "tool_calls") and response.tool_calls:
        table = Table(title="[bold magenta]Tools Used[/bold magenta]", box=None)
        table.add_column("Tool", style="cyan")
        table.add_column("Usage", style="green")

        for tool_call in response.tool_calls:
            table.add_row(
                tool_call.name,
                (
                    tool_call.args[:50] + "..."
                    if len(tool_call.args) > 50
                    else tool_call.args
                ),
            )

        console.print(table)


def display_ascii_header():
    """Display a futuristic ASCII art header"""
    header = """
    [bold blue]
    ╔═══════════════════════════════════════════════════════════════╗
    ║  █▀▀ █░█ ▀█▀ █░█ █▀█ █ █▀ ▀█▀ █ █▀▀   ▄▀█ █▀▀ █▀▀ █▄░█ ▀█▀  ║
    ║  █▀░ █▄█ ░█░ █▄█ █▀▄ █ ▄█ ░█░ █ █▄▄   █▀█ █▄█ ██▄ █░▀█ ░█░  ║
    ╚═══════════════════════════════════════════════════════════════╝
    [/bold blue]
    """
    console.print(header)


def main():
    """Run the chat interface"""
    console.clear()
    display_ascii_header()

    console.print("[bold green]Initializing AI Agent System...[/bold green]")
    agent = initialize_agent()

    console.print("\n[bold cyan]System ready! Enter your commands below.[/bold cyan]")
    console.print("[dim]Type 'exit', 'quit', or press Ctrl+D to exit.[/dim]")

    while True:
        try:
            # Get user input with custom prompt
            user_input = Prompt.ask("\n[bold green]YOU[/bold green]")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                console.print(
                    "[bold yellow]Shutting down system. Goodbye![/bold yellow]"
                )
                break

            # Show thinking animation
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold yellow]Agent processing...[/bold yellow]"),
                transient=True,
            ) as progress:
                task = progress.add_task("", total=None)
                response = agent.send_message(user_input)

            # Display the response
            display_response(response)

            # Display tool usage information if available
            display_tool_usage(response)

        except EOFError:
            # Handle Ctrl+D
            console.print(
                "\n[bold yellow]System shutdown initiated. Goodbye![/bold yellow]"
            )
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C
            console.print(
                "\n[bold red]Operation interrupted.[/bold red] [dim]Type 'exit' to quit.[/dim]"
            )
            continue
        except Exception as e:
            import traceback

            console.print_exception()
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")


if __name__ == "__main__":
    main()
