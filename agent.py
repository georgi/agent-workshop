from typing import List, Dict, Any, Optional
import json
from conversation import Conversation
from tools import Tool


class Agent:
    """An agent that has an objective and uses tools to achieve it"""

    def __init__(
        self,
        objective: str,
        tools: Optional[List[Tool]] = None,
        model: str = "gpt-3.5-turbo",
        system_message: Optional[str] = None,
    ):
        """Initialize the agent with an objective and tools"""
        self.objective = objective
        self.tools = tools or []
        self.model = model
        self.conversation = Conversation()

        # Add system message
        default_system = f"You are a helpful AI assistant with the objective: {objective}. Think step by step to achieve the objective."
        self.conversation.add_message("system", system_message or default_system)

    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent"""
        self.tools.append(tool)

    def send_message(self, content: str) -> Dict[str, Any]:
        """Send a user message and get a response"""
        self.conversation.add_message("user", content)
        return self._get_response()

    def _get_response(self) -> Dict[str, Any]:
        """Get a response from the OpenAI API and handle tool calls"""
        tools_dict = [tool.to_dict() for tool in self.tools] if self.tools else None

        response = self.conversation.send(model=self.model, tools=tools_dict)

        # Handle tool calls if present
        tool_calls = getattr(response, "tool_calls", None)
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments
                tool_call_id = tool_call.id

                # Find the matching tool
                matching_tools = [
                    tool for tool in self.tools if tool.name == function_name
                ]
                if matching_tools:
                    tool = matching_tools[0]
                    try:
                        result = tool.execute(function_args)
                        self.conversation.add_tool_result(tool_call_id, result)
                    except Exception as e:
                        self.conversation.add_tool_result(
                            tool_call_id, f"Error: {str(e)}"
                        )
                else:
                    self.conversation.add_tool_result(
                        tool_call_id, f"Error: Tool '{function_name}' not found"
                    )

            # Get a new response after tool execution
            return self._get_response()

        return response

    def run(self, initial_input: str, max_turns: int = 10) -> List[Dict[str, Any]]:
        """Run the agent with an initial input for a maximum number of turns"""
        response = self.send_message(initial_input)
        turns = 1

        while turns < max_turns:
            # Check if we need to continue
            if "continue" in response.content.lower():
                response = self.send_message("Continue")
                turns += 1
            else:
                break

        return self.conversation.messages
