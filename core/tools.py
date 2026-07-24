"""
NEURA-1 Tools System v0.6.1

Manages external capabilities and actions
for the NEURA-1 assistant.
"""


import ast
import operator
import os
import platform
from datetime import datetime


from core.web_search import WebSearch
from core.code_agent import CodeAgent



class ToolsSystem:


    def __init__(self):

        self.web = WebSearch()

        self.code = CodeAgent()


        self.tools = {

            "calculator":
                self.calculator,

            "text_info":
                self.text_info,

            "system_info":
                self.system_info,

            "current_time":
                self.current_time,

            "file_info":
                self.file_info,

            "memory_search":
                self.memory_search,

            "knowledge_search":
                self.knowledge_search,

            "translate":
                self.translate,

            "web_search":
                self.run_web_search,

            "code_agent":
                self.code_fix,

            "code_analyze":
                self.code_analyze,

            "code_fix":
                self.code_fix

        }



    def available_tools(self):

        return list(
            self.tools.keys()
        )



    def run_tool(
        self,
        tool_name,
        data
    ):

        tool = self.tools.get(tool_name)


        if not tool:

            return {

                "error":
                    "Tool not found"

            }


        return tool(data)



    # =====================
    # Web Search
    # =====================


    def run_web_search(
        self,
        query
    ):

        return self.web.search(query)



    # =====================
    # Code Agent
    # =====================


    def code_analyze(
        self,
        code
    ):

        return self.code.analyze(code)



    def code_fix(
        self,
        code
    ):

        return self.code.fix(code)



    # =====================
    # Calculator
    # =====================


    def calculator(
        self,
        expression
    ):


        try:

            replacements = {

                "ضرب": "*",
                "قسمة": "/",
                "جمع": "+",
                "طرح": "-"

            }


            for key, value in replacements.items():

                expression = expression.replace(
                    key,
                    value
                )


            allowed = {

                ast.Add:
                    operator.add,

                ast.Sub:
                    operator.sub,

                ast.Mult:
                    operator.mul,

                ast.Div:
                    operator.truediv,

                ast.Pow:
                    operator.pow

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

                    if isinstance(
                        node.value,
                        (int, float)
                    ):

                        return node.value



                if isinstance(
                    node,
                    ast.BinOp
                ):

                    operation = allowed.get(
                        type(node.op)
                    )


                    if operation:

                        return operation(
                            evaluate(node.left),
                            evaluate(node.right)
                        )


                raise ValueError(
                    "Invalid expression"
                )



            return {

                "tool":
                    "calculator",

                "expression":
                    expression,

                "result":
                    evaluate(
                        tree.body
                    )

            }



        except Exception as e:


            return {

                "tool":
                    "calculator",

                "error":
                    str(e)

            }




    # =====================
    # Text Analysis
    # =====================


    def text_info(
        self,
        text
    ):


        return {

            "characters":
                len(text),

            "words":
                len(text.split()),

            "language":

                "Arabic"

                if any(
                    "\u0600" <= c <= "\u06FF"
                    for c in text
                )

                else "English"

        }



    # =====================
    # System Info
    # =====================


    def system_info(
        self,
        _
    ):


        return {

            "system":
                "NEURA-1",

            "version":
                "0.6.1",

            "model":
                os.getenv(
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


    def current_time(
        self,
        _
    ):


        return {

            "time":
                datetime.utcnow()
                .isoformat(),

            "timezone":
                "UTC"

        }



    # =====================
    # Files
    # =====================


    def file_info(
        self,
        path
    ):


        try:

            exists = os.path.exists(path)


            return {

                "path":
                    path,

                "exists":
                    exists,

                "size":
                    os.path.getsize(path)
                    if exists
                    else 0

            }


        except Exception as e:

            return {

                "error":
                    str(e)

            }




    # =====================
    # Memory
    # =====================


    def memory_search(
        self,
        query
    ):

        return {

            "tool":
                "memory_search",

            "query":
                query,

            "status":
                "connected"

        }



    # =====================
    # Knowledge
    # =====================


    def knowledge_search(
        self,
        query
    ):

        return {

            "tool":
                "knowledge_search",

            "query":
                query,

            "status":
                "connected"

        }




    # =====================
    # Translation
    # =====================


    def translate(
        self,
        text
    ):

        return {

            "input":
                text,

            "status":
                "translation engine pending"

        }




if __name__ == "__main__":


    tools = ToolsSystem()


    print(
        tools.available_tools()
    )


    print(
        tools.run_tool(
            "calculator",
            "25 ضرب 4"
        )
    )