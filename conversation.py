import os
import openai
from typing import List, Dict, Any, Optional


class Conversation:
    """Manages the conversation with the OpenAI API"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the conversation manager"""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly."
            )

        self.client = openai.OpenAI(api_key=self.api_key)
        self.messages = []

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history"""
        self.messages.append({"role": role, "content": content})

    def add_tool_result(self, tool_call_id: str, output: str) -> None:
        """Add a tool result to the conversation history"""
        self.messages.append(
            {"role": "tool", "tool_call_id": tool_call_id, "content": output}
        )

    def send(
        self, model: str = "gpt-3.5-turbo", tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Send the conversation to the OpenAI API and get a response"""
        response = self.client.chat.completions.create(
            model=model, messages=self.messages, tools=tools
        )

        # Add the assistant's response to our message history
        message = response.choices[0].message
        self.messages.append(dict(message))

        return message
