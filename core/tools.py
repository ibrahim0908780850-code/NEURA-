"""
NEURA-1 Tools System

Provides external capabilities and actions
for the NEURA-1 assistant.
"""

import ast
import operator
from datetime import datetime


class ToolsSystem:
    """
    Manages tools available to NEURA-1.
    """

    def __init__(self):

        self.tools = {
            "calculator": self.calculator,
            "text_info": self.text_info,
            "system_info": self.system_info
        }


    def available_tools(self):
        """
        Return available tools.
        """

        return list(
            self.tools.keys()
        )


    def run_tool(self, tool_name, data):
        """
        Execute selected tool.
        """

        if tool_name not in self.tools:
            return {
                "error": "Tool not found"
            }

        return self.tools[tool_name](data)


    def calculator(self, expression):
        """
        Safe basic calculator.
        """

        try:

            allowed = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv
            }

            tree = ast.parse(
                expression,
                mode="eval"
            )


            def evaluate(node):

                if isinstance(
                    node,
                    ast.Constant
                ):
                    return node.value

                if isinstance(
                    node,
                    ast.BinOp
                ):

                    return allowed[
                        type(node.op)
                    ](
                        evaluate(node.left),
                        evaluate(node.right)
                    )

                raise ValueError(
                    "Unsupported operation"
                )


            return {
                "result": evaluate(
                    tree.body
                )
            }


        except Exception:

            return {
                "error": "Invalid expression"
            }


    def text_info(self, text):
        """
        Analyze text.
        """

        return {
            "characters": len(text),
            "words": len(text.split())
        }


    def system_info(self, _):
        """
        Return NEURA system information.
        """

        return {
            "system": "NEURA-1",
            "time": datetime.utcnow().isoformat(),
            "status": "online"
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