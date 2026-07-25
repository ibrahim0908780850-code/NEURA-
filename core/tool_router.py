"""
NEURA-1 Tool Router v0.8.1

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

    def extract_code(self, text):
        """
        Extract code block from message.
        """

        if "```" not in text:
            return text

        parts = text.split("```")

        if len(parts) < 2:
            return text

        code = parts[1].strip()

        lines = code.splitlines()

        if lines:

            language = lines[0].strip().lower()

            if language in (
                "python",
                "javascript",
                "js",
                "java",
                "cpp",
                "c",
                "c#",
                "go",
                "rust",
                "php",
                "html",
                "css",
                "sql",
            ):
                code = "\n".join(lines[1:])

        return code.strip()

    def choose_tool(self, message):

        text = message.lower()

        # Any code block
        if "```" in message:
            return "code_agent"

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

        if any(word.lower() in text for word in search_words):
            return "web_search"

        # Code Agent
        code_words = [
            "كود",
            "برمجة",
            "python",
            "javascript",
            "typescript",
            "java",
            "c++",
            "c#",
            "go",
            "rust",
            "php",
            "html",
            "css",
            "sql",
            "خطأ",
            "error",
            "exception",
            "traceback",
            "bug",
            "fix",
            "debug",
            "اصلح",
            "صلح",
            "عدل",
            "تصحيح"
        ]

        if any(word.lower() in text for word in code_words):
            return "code_agent"

        # Time
        if (
            "وقت" in text
            or "الساعة" in text
            or "time" in text
        ):
            return "current_time"

        return "model"

    def execute(self, message):

        tool = self.choose_tool(message)

        # AI Model
        if tool == "model":
            return {
                "tool": "model",
                "action": "send_to_ai"
            }

        # Code Agent
        if tool == "code_agent":

            if not self.code_agent:
                return {
                    "tool": "code_agent",
                    "status": "unavailable",
                    "error": "Code agent not connected"
                }

            code = self.extract_code(message)

            try:

                result = self.code_agent.fix(code)

                return {
                    "tool": "code_agent",
                    "status": "success",
                    "result": result
                }

            except Exception as e:

                return {
                    "tool": "code_agent",
                    "status": "failed",
                    "error": str(e)
                }

        # External Tools
        if (
            self.tools
            and hasattr(self.tools, "tools")
            and tool in self.tools.tools
        ):
            return self.tools.run_tool(
                tool,
                message
            )

        return {
            "tool": tool,
            "status": "unavailable",
            "error": f"Tool '{tool}' unavailable"
        }


if __name__ == "__main__":

    router = ToolRouter(None)

    print(router.choose_tool("احسب 5*5"))

    print(router.choose_tool("ابحث عن الذكاء الاصطناعي"))

    print(router.choose_tool("اصلح هذا الكود"))

    print(
        router.extract_code(
            """
```python
def hello():
    print("Hi")