"""
NEURA-1 Tools System

Provides external capabilities and actions
for the NEURA-1 assistant.
"""

import ast
import operator
import os
import platform
import datetime
import os.path


class ToolsSystem:

    def __init__(self):

        self.tools = {

            "calculator": self.calculator,

            "text_info": self.text_info,

            "system_info": self.system_info,

            "current_time": self.current_time,

            "file_info": self.file_info,

            "memory_search": self.memory_search,

            "knowledge_search": self.knowledge_search,

            "translate": self.translate

        }



    def available_tools(self):

        return list(
            self.tools.keys()
        )



    def run_tool(self, tool_name, data):

        if tool_name not in self.tools:

            return {
                "error": "Tool not found"
            }


        return self.tools[tool_name](data)



    # =====================
    # Calculator
    # =====================

    def calculator(self, expression):

        try:

            allowed = {

                ast.Add: operator.add,

                ast.Sub: operator.sub,

                ast.Mult: operator.mul,

                ast.Div: operator.truediv,

                ast.Pow: operator.pow

            }


            tree = ast.parse(
                expression,
                mode="eval"
            )


            def evaluate(node):

                if isinstance(node, ast.Constant):

                    return node.value


                if isinstance(node, ast.BinOp):

                    operation = allowed.get(
                        type(node.op)
                    )

                    if operation:

                        return operation(
                            evaluate(node.left),
                            evaluate(node.right)
                        )


                raise ValueError()


            return {
                "result": evaluate(tree.body)
            }


        except:

            return {
                "error": "Invalid calculation"
            }



    # =====================
    # Text Analysis
    # =====================

    def text_info(self, text):

        return {

            "characters": len(text),

            "words": len(text.split()),

            "language":

                "Arabic"

                if any(
                    "\u0600" <= c <= "\u06FF"
                    for c in text
                )

                else "English"

        }



    # =====================
    # System Information
    # =====================

    def system_info(self, _):

        return {

            "system": "NEURA-1",

            "version": "0.5.0",

            "model": os.getenv(
                "MODEL_NAME",
                "Qwen/Qwen3.5-9B"
            ),

            "platform":
                platform.system(),

            "status":
                "online"

        }



    # =====================
    # Time
    # =====================

    def current_time(self, _):

        return {

            "time":
                datetime.datetime.utcnow()
                .isoformat(),

            "timezone":
                "UTC"

        }



    # =====================
    # File Tool
    # =====================

    def file_info(self, path):

        try:

            return {

                "exists":
                    os.path.exists(path),

                "size":
                    os.path.getsize(path)

                if os.path.exists(path)

                else 0

            }


        except Exception as e:

            return {
                "error": str(e)
            }



    # =====================
    # Memory Tool
    # =====================

    def memory_search(self, query):

        return {

            "tool":
                "memory_search",

            "query":
                query,

            "status":
                "connect memory database"

        }



    # =====================
    # Knowledge Base Tool
    # =====================

    def knowledge_search(self, query):

        return {

            "tool":
                "knowledge_search",

            "query":
                query,

            "status":
                "connect knowledge base"

        }



    # =====================
    # Translation Tool
    # =====================

    def translate(self, text):

        return {

            "input":
                text,

            "status":
                "translation API not connected yet"

        }



if __name__ == "__main__":


    tools = ToolsSystem()


    print(
        tools.available_tools()
    )


    print(
        tools.run_tool(
            "calculator",
            "10*5"
        )
    )


    print(
        tools.run_tool(
            "system_info",
            ""
        )
    )