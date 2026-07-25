"""
NEURA-1 Code Agent v0.9

Advanced coding assistant.

Features:
- Code analysis
- Bug detection
- Explanation
- AI repair
- Multi-language detection
"""

import ast
import json
import re


class CodeAgent:


    def __init__(self):

        self.name = "NEURA Code Agent"

        self.version = "0.9.0"



    # ====================================
    # Analyze
    # ====================================

    def analyze(
        self,
        code
    ):

        errors = []

        suggestions = []

        language = self.detect_language(
            code
        )


        # Python syntax check

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


        issues = self.detect_issues(
            code,
            language
        )


        errors.extend(
            issues
        )


        suggestions.extend(
            self.generate_suggestions(
                code,
                language
            )
        )


        return {


            "agent":
            self.name,


            "version":
            self.version,


            "language":
            language,


            "valid":
            len(errors) == 0,


            "errors":
            errors,


            "suggestions":
            suggestions

        }



    # ====================================
    # Detect Language
    # ====================================

    def detect_language(
        self,
        code
    ):


        indicators = {


            "Python":

            [
                "import ",
                "from ",
                "def ",
                "class ",
                "print("
            ],



            "JavaScript":

            [
                "function ",
                "console.log",
                "const ",
                "let ",
                "=>"
            ],



            "HTML":

            [
                "<html",
                "<body",
                "<div"
            ],



            "SQL":

            [
                "SELECT ",
                "INSERT ",
                "UPDATE ",
                "DELETE "
            ]

        }



        for language, patterns in indicators.items():

            for pattern in patterns:

                if pattern.lower() in code.lower():

                    return language



        return "Unknown"



    # ====================================
    # Detect Problems
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

                    "type":
                    "StyleWarning",

                    "message":
                    "Use print() instead of print statement"

                })



            if "\t" in code:

                issues.append({

                    "type":
                    "IndentationWarning",

                    "message":
                    "Tabs detected, replace with spaces"

                })



            if re.search(
                r"\bif .*=",
                code
            ):

                issues.append({

                    "type":
                    "PossibleBug",

                    "message":
                    "Possible assignment instead of comparison"

                })



        if language == "JavaScript":


            if "var " in code:

                issues.append({

                    "type":
                    "StyleWarning",

                    "message":
                    "Use let or const instead of var"

                })



        return issues



    # ====================================
    # Suggestions
    # ====================================

    def generate_suggestions(
        self,
        code,
        language
    ):


        suggestions = []


        if language == "Python":

            suggestions.append(
                "Follow PEP8 formatting"
            )


        if language == "JavaScript":

            suggestions.append(
                "Use modern ES6 syntax"
            )


        return suggestions



    # ====================================
    # Explain
    # ====================================

    def explain(
        self,
        code
    ):


        return {

            "analysis":
            self.analyze(code),


            "lines":
            len(code.splitlines()),


            "characters":
            len(code)

        }



    # ====================================
    # Fix
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
                "valid",

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
            "needs_repair",

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

You are NEURA-1 Code Repair Agent.

Repair the code.

Language:
{analysis['language']}


Errors:
{analysis['errors']}


Code:

{code}


Return ONLY JSON:

{{
"fixed_code":"",
"explanation":"",
"changes":[]
}}

"""


        try:


            response = engine.generate(
                prompt
            )


            if isinstance(response, str):


                cleaned = (
                    response
                    .replace("```json","")
                    .replace("```","")
                    .strip()
                )


                try:

                    response = json.loads(
                        cleaned
                    )


                except Exception:


                    response = {

                        "fixed_code":
                        response,


                        "explanation":
                        "AI returned non JSON output"

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


    result = agent.fix(
        broken_code
    )


    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )