"""
NEURA-1 Tool Router v0.8

Automatically selects the correct tool
based on user request.
"""

import re



class ToolRouter:


    def __init__(
        self,
        tools,
        code_agent=None,
        engine=None
    ):

        self.tools = tools

        self.code_agent = code_agent

        self.engine = engine





    def extract_code(
        self,
        text
    ):

        """
        Extract code blocks from user message.
        """


        if "```" in text:


            parts = text.split("```")


            if len(parts) >= 2:


                code = parts[1]


                # إزالة اسم اللغة من بداية البلوك

                if code.startswith("python"):

                    code = code.replace(
                        "python",
                        "",
                        1
                    )


                return code.strip()



        return text






    def choose_tool(
        self,
        message
    ):


        text = message.lower()





        # Calculator

        if re.search(

            r"\d+\s*(\+|\-|\*|\/|ضرب|قسمة|جمع|طرح)\s*\d+",

            text

        ):

            return "calculator"






        # Web Search

        search_words = [

            "ابحث",
            "بحث عن",
            "اخبار",
            "أخبار",
            "آخر الأخبار",
            "latest",
            "search",
            "news"

        ]



        if any(

            word.lower() in text

            for word in search_words

        ):

            return "web_search"






        # Code Agent

        code_words = [

            "كود",
            "برمجة",
            "python",
            "javascript",
            "java",
            "خطأ",
            "error",
            "fix",
            "debug",
            "صلح",
            "اصلح",
            "عدل",
            "تصحيح"

        ]



        if any(

            word.lower() in text

            for word in code_words

        ):

            return "code_agent"






        # Time

        if (

            "وقت" in text

            or "الساعة" in text

            or "time" in text

        ):

            return "current_time"






        return "model"







    def execute(
        self,
        message
    ):


        tool = self.choose_tool(
            message
        )





        # AI Model

        if tool == "model":


            return {


                "tool":

                "model",


                "action":

                "send_to_ai"

            }







        # Code Agent

        if tool == "code_agent":



            if self.code_agent:



                code = self.extract_code(
                    message
                )



                result = self.code_agent.fix(

                    code,

                    self.engine

                )



                return {


                    "tool":

                    "code_agent",


                    "result":

                    result

                }





            return {


                "error":

                "Code agent not connected"

            }







        # Other Tools

        if (

            self.tools

            and tool in self.tools.tools

        ):


            return self.tools.run_tool(

                tool,

                message

            )






        return {


            "error":

            f"Tool '{tool}' unavailable"

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


    print(
        router.choose_tool(
            """
اصلح هذا الكود:

```python
def hello():
print("Hi")