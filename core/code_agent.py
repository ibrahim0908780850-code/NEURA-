"""
NEURA-1 Code Agent

Analyzes, explains and assists
with programming code.
"""

import ast


class CodeAgent:


    def analyze(self, code):

        errors = []

        language = self.detect_language(code)


        if language == "Python":

            try:

                ast.parse(code)


            except SyntaxError as e:

                errors.append({

                    "type":
                        "SyntaxError",

                    "message":
                        e.msg,

                    "line":
                        e.lineno,

                    "offset":
                        e.offset

                })


            except Exception as e:

                errors.append({

                    "type":
                        type(e).__name__,

                    "message":
                        str(e)

                })


        return {

            "language":
                language,

            "valid":
                len(errors) == 0,

            "errors":
                errors

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

            "C/C++": [
                "#include",
                "int main"
            ],

            "Java": [
                "public class",
                "System.out.println"
            ],

            "HTML": [
                "<html",
                "<div"
            ],

            "SQL": [
                "SELECT ",
                "INSERT INTO"
            ]

        }


        for language, keys in indicators.items():

            for key in keys:

                if key in code:

                    return language


        return "Unknown"



    def explain(self, code):

        analysis = self.analyze(code)


        return {

            "language":
                analysis["language"],

            "characters":
                len(code),

            "lines":
                len(
                    code.splitlines()
                ),

            "valid":
                analysis["valid"],

            "explanation":
                "NEURA Code Agent analyzed the code structure and syntax."

        }



    def suggest_fix(self, code):

        analysis = self.analyze(code)

        suggestions = []


        for error in analysis["errors"]:

            if error["type"] == "SyntaxError":

                suggestions.append(
                    "Review indentation, brackets, quotes and missing syntax."
                )


        if analysis["language"] == "Python":

            if "print " in code:

                suggestions.append(
                    "Use print() function in Python 3."
                )


        return {

            "analysis":
                analysis,

            "suggestions":
                suggestions

        }



    def fix(self, code):

        analysis = self.analyze(code)


        if analysis["valid"]:

            return {

                "status":
                    "Code is valid",

                "language":
                    analysis["language"],

                "code":
                    code

            }


        return {

            "status":
                "Needs AI repair",

            "analysis":
                analysis,

            "instruction":
                "Send code and errors to NEURA reasoning engine."

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