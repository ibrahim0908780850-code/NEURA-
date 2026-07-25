"""
NEURA-1 Central Core v0.9

Main controller layer.

Integrates:
- NEURA Engine
- Conversation Manager
- Personality
- Tools
"""


from core.neura_engine import NEURAEngine
from core.conversation import ConversationManager
from core.personality import NEURAPersonality
from core.tools import ToolsSystem



class NEURACore:


    def __init__(self):


        self.engine = NEURAEngine()


        self.conversation = ConversationManager()


        self.personality = NEURAPersonality()


        self.tools = ToolsSystem(
            engine=self.engine
        )




    # =================================
    # Tool Detection
    # =================================


    def detect_tool(
        self,
        message
    ):


        text = message.lower()



        if (
            "احسب" in text
            or "calculate" in text
        ):

            return "calculator"



        return None





    # =================================
    # Chat
    # =================================


    def chat(
        self,
        user_id,
        message
    ):


        try:



            # Save user message

            self.conversation.add_message(

                user_id,

                "user",

                message

            )



            history = self.conversation.get_history(

                user_id

            )



            tool_result = None



            tool = self.detect_tool(

                message

            )



            if tool == "calculator":


                expression = (

                    message

                    .replace(
                        "احسب",
                        ""
                    )

                    .replace(
                        "calculate",
                        ""
                    )

                    .strip()

                )



                tool_result = self.tools.run_tool(

                    "calculator",

                    expression

                )





            # Generate response

            response = self.engine.process_message(

                message,

                user_id,

                history

            )





            if isinstance(
                response,
                dict
            ):


                assistant_text = response.get(

                    "response",

                    str(response)

                )


            else:


                assistant_text = str(response)





            # Save assistant message

            self.conversation.add_message(

                user_id,

                "assistant",

                assistant_text

            )





            return {


                "personality":

                    self.personality.get_profile(),



                "response":

                    response,



                "tool_result":

                    tool_result,



                "conversation":

                    self.conversation.get_history(

                        user_id

                    ),



                "tools":

                    self.tools.available_tools()


            }





        except Exception as e:


            return {


                "error":

                    str(e),


                "user_id":

                    user_id


            }





if __name__ == "__main__":


    neura = NEURACore()


    result = neura.chat(

        "demo-user",

        "مرحبا نيرا"

    )


    print(result)