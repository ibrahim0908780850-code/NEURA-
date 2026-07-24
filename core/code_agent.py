"""
NEURA-1 Code Agent

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


            except Exception as e:

                errors.append({

                    "type": type(e).__name__,
                    "message": str(e)

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



    def detect_issues(self, code, language):

        issues = []


        if language == "Python":

            if "print " in code:

                issues.append({

                    "type":
                        "StyleWarning",

                    "message":
                        "Python 3 uses print() instead of print statement."

                })


            if "\t" in code:

                issues.append({

                    "type":
                        "IndentationWarning",

                    "message":
                        "Mixed tabs and spaces detected."

                })


        return issues



    def explain(self, code):

        analysis = self.analyze(code)


        return {

            "language":
                analysis["language"],

            "characters":
                len(code),

            "lines":
                len(code.splitlines()),

            "valid":
                analysis["valid"],

            "errors":
                analysis["errors"],

            "explanation":
                "NEURA Code Agent analyzed syntax, structure and possible issues."

        }



    def suggest_fix(self, code):

        analysis = self.analyze(code)

        suggestions = []


        for error in analysis["errors"]:

            if error["type"] == "SyntaxError":

                suggestions.append(
                    "Fix syntax near the reported line."
                )


            elif error["type"] == "IndentationWarning":

                suggestions.append(
                    "Use consistent indentation."
                )


        return {

            "analysis":
                analysis,

            "suggestions":
                suggestions

        }



    def fix(self, code, engine=None):

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


        if engine:

            return self.repair(
                code,
                engine
            )


        return {

            "status":
                "Needs AI repair",

            "analysis":
                analysis

        }



    def repair(self, code, engine):

        analysis = self.analyze(code)


        if engine.inference is None:

            engine.load_model()



        prompt = f"""

You are NEURA Code Repair Agent.

Repair the following code.

Language:
{analysis['language']}

Errors:
{analysis['errors']}

Code:

{code}


Return:

1. Fixed code
2. Explanation
"""


        response = engine.inference.generate(
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