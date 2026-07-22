"""
NEURA-1 Code Agent

Analyzes, explains and assists
with programming code.
"""

import ast
import re


class CodeAgent:


    def analyze(self, code):

        errors = []

        try:

            ast.parse(code)


        except SyntaxError as e:

            errors.append({

                "type": "SyntaxError",

                "message": e.msg,

                "line": e.lineno,

                "offset": e.offset

            })


        except Exception as e:

            errors.append({

                "type": type(e).__name__,

                "message": str(e)

            })


        return {

            "valid":
                len(errors) == 0,

            "errors":
                errors

        }



    def detect_language(self, code):

        if "import " in code or "def " in code:
            return "Python"

        if "function " in code or "console.log" in code:
            return "JavaScript"

        if "#include" in code:
            return "C/C++"

        return "Unknown"



    def explain(self, code):

        return {

            "language":
                self.detect_language(code),

            "length":
                len(code),

            "explanation":
                "NEURA will analyze this code using the reasoning model."

        }



    def suggest_fix(self, code):

        analysis = self.analyze(code)


        suggestions = []


        for error in analysis["errors"]:

            if error["type"] == "SyntaxError":

                suggestions.append(
                    "Check brackets, quotes, indentation and missing symbols."
                )


        return {

            "errors":
                analysis["errors"],

            "suggestions":
                suggestions

        }



    def fix(self, code):

        analysis = self.analyze(code)


        if analysis["valid"]:

            return {

                "status":
                    "Code is valid",

                "code":
                    code

            }


        return {

            "status":
                "Needs AI repair",

            "analysis":
                analysis,

            "instruction":
                """
Send code and errors to NEURA reasoning engine
to generate corrected version.
"""

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