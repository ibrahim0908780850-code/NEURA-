"""
NEURA-1 Code Repair Engine

Generates corrected code using NEURA reasoning.
"""


class CodeRepair:


    def __init__(self, engine):

        self.engine = engine



    def repair(
        self,
        code,
        errors
    ):

        prompt = f"""

You are NEURA Code Repair Agent.

Fix the following code.

CODE:
{code}


ERRORS:
{errors}


Return:
1. Corrected code
2. Explanation of changes

"""


        response = self.engine.generate(
            prompt
        )


        return {

            "original":
                code,

            "errors":
                errors,

            "repair":
                response

        }