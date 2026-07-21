"""
NEURA-1 Tools System

Provides external capabilities and actions
for the NEURA-1 assistant.
"""


class ToolsSystem:
    """
    Manages tools available to NEURA-1.
    """

    def __init__(self):
        self.tools = {
            "calculator": self.calculator,
            "text_info": self.text_info
        }

    def available_tools(self):
        """
        Return available tools.
        """

        return list(self.tools.keys())

    def run_tool(self, tool_name, data):
        """
        Execute a selected tool.
        """

        if tool_name not in self.tools:
            return {
                "error": "Tool not found"
            }

        return self.tools[tool_name](data)

    def calculator(self, expression):
        """
        Basic calculator tool.
        """

        try:
            result = eval(expression)

            return {
                "result": result
            }

        except Exception:
            return {
                "error": "Invalid expression"
            }

    def text_info(self, text):
        """
        Basic text analysis tool.
        """

        return {
            "length": len(text),
            "words": len(text.split())
        }


if __name__ == "__main__":

    tools = ToolsSystem()

    print(
        tools.available_tools()
    )

    print(
        tools.run_tool(
            "calculator",
            "5+5"
        )
    )