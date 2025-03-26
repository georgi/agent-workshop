from typing import Dict, Any, Callable, List, Optional
import json


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
