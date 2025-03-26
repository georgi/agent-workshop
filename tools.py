from typing import Dict, Any, Callable, List, Optional
import json
import requests  # Added this import for HTTP requests


class Tool:
    """Base class for tools that agents can use"""

    def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
        """Initialize a tool with name, description, and parameters"""
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary format for OpenAI API"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def execute(self, arguments: str) -> str:
        """Execute the tool with the given arguments"""
        # Default implementation to be overridden by subclasses
        raise NotImplementedError("Tool subclasses must implement execute method")


class Calculator(Tool):
    """A simple calculator tool example"""

    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform simple arithmetic calculations",
            parameters={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The arithmetic operation to perform",
                    },
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"},
                },
                "required": ["operation", "a", "b"],
            },
        )

    def execute(self, arguments: str) -> str:
        """Execute the calculator with the given arguments"""
        args = json.loads(arguments)
        operation = args["operation"]
        a = args["a"]
        b = args["b"]

        if operation == "add":
            return str(a + b)
        elif operation == "subtract":
            return str(a - b)
        elif operation == "multiply":
            return str(a * b)
        elif operation == "divide":
            if b == 0:
                return "Error: Division by zero"
            return str(a / b)
        else:
            return f"Error: Unknown operation {operation}"


class WebsiteFetcher(Tool):
    """A tool to fetch the content of a website"""

    def __init__(self):
        super().__init__(
            name="fetch_website",
            description="Fetch the content of a website given a URL",
            parameters={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the website to fetch content from",
                    },
                },
                "required": ["url"],
            },
        )

    def execute(self, arguments: str) -> str:
        """Fetch content from the specified URL"""
        args = json.loads(arguments)
        url = args["url"]

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Return a summary and truncate if it's too large
            content_length = len(response.text)
            content_preview = response.text[:2000]  # Get first 2000 chars

            result = {
                "status_code": response.status_code,
                "content_length": content_length,
                "content_type": response.headers.get("Content-Type", "unknown"),
                "content_preview": content_preview,
            }

            if content_length > 2000:
                result["note"] = (
                    f"Content truncated (showing {2000}/{content_length} characters)"
                )

            return json.dumps(result, indent=2)

        except requests.RequestException as e:
            return f"Error fetching website: {str(e)}"
