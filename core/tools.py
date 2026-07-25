"""
NEURA-1 Tools System v0.7

Manages external capabilities and actions
for NEURA-1 AI assistant.
"""


import ast
import operator
import os
import platform
import json

from datetime import datetime, timezone


from core.web_search import WebSearch
from core.code_agent import CodeAgent




class ToolsSystem:



    def __init__(
        self,
        engine=None
    ):


        self.version = "0.7.0"

        self.engine = engine


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


            "directory_list":
                self.directory_list,


            "memory_search":
                self.memory_search,


            "knowledge_search":
                self.knowledge_search,


            "translate":
                self.translate,


            "json_parser":
                self.json_parser,


            "env_info":
                self.env_info,


            "web_search":
                self.run_web_search,


            "code_agent":
                self.code_fix,


            "code_analyze":
                self.code_analyze,


            "code_fix":
                self.code_fix,


            "code_explain":
                self.code_explain

        }




    # =====================
    # Tools Manager
    # =====================


    def available_tools(
        self
    ):


        return list(
            self.tools.keys()
        )




    def run_tool(
        self,
        tool_name,
        data
    ):


        tool = self.tools.get(
            tool_name
        )


        if not tool:

            return {

                "error":
                "Tool not found"

            }


        try:

            return tool(data)


        except Exception as e:


            return {

                "error":
                str(e)

            }





    # =====================
    # Web Search
    # =====================


    def run_web_search(
        self,
        query
    ):


        return self.web.search(
            query
        )




    # =====================
    # Code Agent
    # =====================


    def code_analyze(
        self,
        code
    ):


        return self.code.analyze(
            code
        )




    def code_fix(
        self,
        code
    ):


        return self.code.fix(
            code,
            self.engine
        )




    def code_explain(
        self,
        code
    ):


        return self.code.explain(
            code
        )




    # =====================
    # Calculator
    # =====================


    def calculator(
        self,
        expression
    ):


        try:


            replacements = {


                "ضرب":
                "*",


                "قسمة":
                "/",


                "جمع":
                "+",


                "طرح":
                "-"

            }



            for k,v in replacements.items():

                expression = expression.replace(
                    k,
                    v
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



            def calculate(node):


                if isinstance(
                    node,
                    ast.Constant
                ):

                    if isinstance(
                        node.value,
                        (int,float)
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
                            calculate(node.left),
                            calculate(node.right)
                        )



                raise ValueError(
                    "Invalid calculation"
                )



            return {


                "tool":
                "calculator",


                "expression":
                expression,


                "result":
                calculate(
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
    # Text
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


            "has_arabic":
            any(
                "\u0600" <= c <= "\u06FF"
                for c in text
            )

        }




    # =====================
    # System
    # =====================


    def system_info(
        self,
        _
    ):


        return {


            "name":
            "NEURA-1",


            "version":
            self.version,


            "model":
            os.getenv(
                "MODEL_NAME",
                "Qwen/Qwen3.5-9B"
            ),


            "platform":
            platform.platform(),


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
            datetime.now(
                timezone.utc
            ).isoformat(),


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


        if not os.path.exists(path):

            return {

                "exists":
                False

            }


        return {


            "path":
            path,


            "exists":
            True,


            "size":
            os.path.getsize(path)

        }




    def directory_list(
        self,
        path="."
    ):


        try:


            return {


                "path":
                path,


                "files":
                os.listdir(path)

            }


        except Exception as e:


            return {

                "error":
                str(e)

            }





    # =====================
    # Memory / Knowledge
    # =====================


    def memory_search(
        self,
        query
    ):


        return {


            "tool":
            "memory_search",


            "query":
            query

        }




    def knowledge_search(
        self,
        query
    ):


        return {


            "tool":
            "knowledge_search",


            "query":
            query

        }





    # =====================
    # JSON
    # =====================


    def json_parser(
        self,
        data
    ):


        try:


            return json.loads(
                data
            )


        except Exception as e:


            return {

                "error":
                str(e)

            }




    # =====================
    # ENV
    # =====================


    def env_info(
        self,
        _
    ):


        return {


            "HF_TOKEN":
            bool(
                os.getenv("HF_TOKEN")
            ),


            "MODEL":
            os.getenv(
                "MODEL_NAME",
                "Qwen/Qwen3.5-9B"
            )

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
            "AI translation pending"

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