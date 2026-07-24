"""
NEURA-1 Code Agent v0.7

Analyzes, explains, fixes and assists
with programming code.
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
                "INSERT"
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

                    "type": "StyleWarning",

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

        result = self.analyze(code)


        return {

            "analysis": result,

            "lines":
            len(code.splitlines()),

            "characters":
            len(code)

        }



    def suggest_fix(self, code):

        analysis = self.analyze(code)

        suggestions = []


        for error in analysis["errors"]:


            if error["type"] == "SyntaxError":

                suggestions.append(
                    "Check syntax near line "
                    + str(error.get("line"))
                )


            if error["type"] == "IndentationWarning":

                suggestions.append(
                    "Fix indentation"
                )


        return {

            "analysis": analysis,

            "suggestions": suggestions

        }



    def fix(self, code):

        analysis = self.analyze(code)


        if analysis["valid"]:

            return {

                "status":
                "Code is valid",

                "code":
                code,

                "analysis":
                analysis

            }


        return {

            "status":
            "Needs AI repair",

            "analysis":
            analysis,

            "instruction":
            "Send to NEURA reasoning engine"

        }



if __name__ == "__main__":


    agent = CodeAgent()


    test = """

def hello():
print("Hi")

"""


    print(
        agent.fix(test)
    )