"""
NEURA-1 Code Agent v0.8

Analyzes, explains, fixes and repairs code
using NEURA reasoning engine.
"""

import ast
import json


class CodeAgent:

    def __init__(self):

        self.name = "NEURA Code Agent"


    # ====================================
    # Analyze Code
    # ====================================

    def analyze(
        self,
        code
    ):

        errors = []

        language = self.detect_language(
            code
        )


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



    # ====================================
    # Detect Programming Language
    # ====================================

    def detect_language(
        self,
        code
    ):

        indicators = {

            "Python": [

                "import ",

                "from ",

                "def ",

                "class ",

                "print("

            ],


            "JavaScript": [

                "function ",

                "console.log",

                "const ",

                "let ",

                "=>"

            ],


            "HTML": [

                "<html",

                "<body",

                "<div"

            ],


            "SQL": [

                "SELECT ",

                "INSERT ",

                "UPDATE ",

                "DELETE "

            ]

        }


        for language, keys in indicators.items():

            for key in keys:

                if key in code:

                    return language


        return "Unknown"



    # ====================================
    # Detect Common Problems
    # ====================================

    def detect_issues(
        self,
        code,
        language
    ):

        issues = []


        if language == "Python":


            if "print " in code:

                issues.append({

                    "type": "StyleWarning",

                    "message":
                    "Use print() in Python 3"

                })


            if "\t" in code:

                issues.append({

                    "type":
                    "IndentationWarning",

                    "message":
                    "Tabs detected, use spaces"

                })


            if "if " in code and "=" in code:

                issues.append({

                    "type":
                    "PossibleBug",

                    "message":
                    "Check assignment vs comparison"

                })


        return issues



    # ====================================
    # Explain Code
    # ====================================

    def explain(
        self,
        code
    ):

        analysis = self.analyze(
            code
        )


        return {

            "analysis":
            analysis,

            "lines":
            len(code.splitlines()),

            "characters":
            len(code)

        }



    # ====================================
    # Fix Code
    # ====================================

    def fix(
        self,
        code,
        engine=None
    ):

        analysis = self.analyze(
            code
        )


        if analysis["valid"]:

            return {

                "status":
                "Code is valid",

                "code":
                code,

                "analysis":
                analysis

            }



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



    # ====================================
    # AI Repair
    # ====================================

    def repair(
        self,
        code,
        analysis,
        engine
    ):

        prompt = f"""

You are NEURA Code Repair Agent.

Fix this code.

Language:
{analysis['language']}

Errors:
{analysis['errors']}

Code:

{code}


Return only JSON:

{{
"fixed_code":"",
"explanation":""
}}

"""


        try:

            response = engine.generate(
                prompt
            )


            if isinstance(response, str):

                try:

                    response = json.loads(
                        response
                    )

                except Exception:

                    response = {

                        "fixed_code":
                        response,

                        "explanation":
                        "AI returned text response"

                    }



            return {

                "status":
                "repaired",

                "result":
                response,

                "analysis":
                analysis

            }


        except Exception as e:


            return {

                "status":
                "failed",

                "error":
                str(e),

                "original_code":
                code,

                "analysis":
                analysis

            }



# ====================================
# Test
# ====================================

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