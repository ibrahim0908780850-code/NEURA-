"""
NEURA-1 Tool Router

Automatically selects the correct tool
based on user request.
"""


import re


class ToolRouter:


    def __init__(
        self,
        tools,
        code_agent=None
    ):

        self.tools = tools
        self.code_agent = code_agent



    def choose_tool(
        self,
        message
    ):

        text = message.lower()


        # =====================
        # Calculator
        # =====================

        if re.search(
            r"\d+\s*[\+\-\*\/]\s*\d+",
            text
        ):

            return "calculator"



        # =====================
        # Web Search
        # =====================

        search_words = [

            "ابحث",
            "بحث",
            "اخبار",
            "آخر",
            "latest",
            "search",
            "news"

        ]


        if any(
            word in text
            for word in search_words
        ):

            return "web_search"



        # =====================
        # Programming
        # =====================

        code_words = [

            "كود",
            "برمجة",
            "python",
            "javascript",
            "خطأ",
            "error",
            "fix",
            "debug"

        ]


        if any(
            word in text
            for word in code_words
        ):

            return "code_agent"



        # =====================
        # Time
        # =====================

        if (
            "وقت" in text
            or "time" in text
        ):

            return "current_time"



        # =====================
        # Default
        # =====================

        return "model"



    def execute(
        self,
        message
    ):

        tool = self.choose_tool(
            message
        )


        if tool == "model":

            return {

                "tool":
                    "model",

                "action":
                    "send_to_ai"

            }



        if tool == "code_agent":

            if self.code_agent:

                return self.code_agent.fix(
                    message
                )


            return {

                "error":
                    "Code agent not connected"

            }



        if tool in self.tools.tools:

            return self.tools.run_tool(
                tool,
                message
            )


        return {

            "error":
                "Unknown tool"

        }



if __name__ == "__main__":


    router = ToolRouter(
        None
    )


    print(
        router.choose_tool(
            "احسب 5*5"
        )
    )

    print(
        router.choose_tool(
            "ابحث عن الذكاء الاصطناعي"
        )
    )