"""
NEURA-1 Code Agent v0.8

Analyzes, explains, fixes and repairs code
using NEURA reasoning engine.
"""

import ast


class CodeAgent:


    def __init__(self):

        self.name = "NEURA Code Agent"



    def analyze(self, code):

        errors = []

        language = self.detect_language(code)


        if language == "Python":

            try:

                ast.parse(code)


            except SyntaxError as e:

                errors.append({

                    "type": "SyntaxError",
                    "message": e.msg,
                    "line": e.lineno,
                    "offset": e.offset

                })


        errors.extend(
            self.detect_issues(
                code,
                language
            )
        )


        return {

            "agent": self.name,

            "language": language,

            "valid": len(errors) == 0,

            "errors": errors

        }




    def detect_language(self, code):

        indicators = {

            "Python": [
                "import ",
                "def ",
                "class ",
                "print("
            ],


            "JavaScript": [
                "function ",
                "console.log",
                "const ",
                "let "
            ],


            "HTML": [
                "<html",
                "<div"
            ],


            "SQL": [
                "SELECT ",
                "INSERT "
            ]

        }


        for language, keys in indicators.items():

            for key in keys:

                if key in code:

                    return language


        return "Unknown"





    def detect_issues(
        self,
        code,
        language
    ):

        issues = []


        if language == "Python":


            if "print " in code:

                issues.append({

                    "type":
                    "StyleWarning",

                    "message":
                    "Use print() in Python 3"

                })


            if "\t" in code:

                issues.append({

                    "type":
                    "IndentationWarning",

                    "message":
                    "Tabs detected"

                })


        return issues






    def explain(self, code):

        analysis = self.analyze(code)


        return {

            "analysis":
            analysis,


            "lines":
            len(code.splitlines()),


            "characters":
            len(code)

        }







    def fix(
        self,
        code,
        engine=None
    ):


        analysis = self.analyze(code)



        # الكود صحيح

        if analysis["valid"]:

            return {

                "status":
                "Code is valid",

                "code":
                code,

                "analysis":
                analysis

            }




        # إرسال إلى Qwen

        if engine:


            return self.repair(
                code,
                analysis,
                engine
            )




        return {

            "status":
            "Needs AI repair",

            "analysis":
            analysis

        }








    def repair(
        self,
        code,
        analysis,
        engine
    ):


        prompt = f"""

You are NEURA Code Repair Agent.

Fix this programming code.

Language:
{analysis['language']}


Detected errors:

{analysis['errors']}


Code:

{code}


Return JSON:

{{
"fixed_code":"",
"explanation":""
}}

"""


        response = engine.generate(
            prompt
        )


        return {

            "status":
            "repaired",

            "result":
            response,

            "analysis":
            analysis

        }







if __name__ == "__main__":


    agent = CodeAgent()


    broken_code = """

def hello():
print("Hi")

"""


    print(
        agent.fix(
            broken_code
        )
    )