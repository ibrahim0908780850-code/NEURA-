"""
NEURA-1 Core Engine v0.9

Main intelligence layer.

Integrates:
- AI Model
- Memory
- Knowledge
- Tools
- Router
- Code Agent
- Conversation Context
"""


from datetime import datetime, timezone


from core.config import Config
from core.model_loader import ModelLoader
from core.memory import MemorySystem
from core.knowledge import KnowledgeBase
from core.tools import ToolsSystem
from core.tool_router import ToolRouter
from core.code_agent import CodeAgent



class NEURAEngine:


    def __init__(self):

        self.config = Config()

        self.name = "NEURA-1"

        self.version = "0.9.0"



        # AI MODEL

        self.model_loader = ModelLoader()

        self.model = None

        self.inference = None



        # CORE SYSTEMS

        self.memory = MemorySystem()

        self.knowledge = KnowledgeBase()

        self.tools = ToolsSystem()



        # AGENTS

        self.code_agent = CodeAgent()



        # ROUTER

        self.router = ToolRouter(

            tools=self.tools,

            code_agent=self.code_agent,

            engine=self

        )



        self.created = datetime.now(
            timezone.utc
        )



        self.knowledge.add_knowledge(

            "NEURA-1",

            """
NEURA-1 is an Arabic-first AI system.

Capabilities:

- Arabic conversation
- Memory
- Knowledge retrieval
- Tool usage
- Code analysis
- Code repair
- AI reasoning
"""

        )





    # ==============================
    # MODEL
    # ==============================


    def load_model(self):


        if self.inference:


            return {

                "status":
                "already_loaded"

            }



        try:


            self.model = (
                self.model_loader.load()
            )


            self.inference = (
                self.model_loader.inference
            )


            return {

                "status":
                "loaded",

                "model":
                self.model_loader.model_name

            }



        except Exception as e:


            return {

                "status":
                "failed",

                "error":
                str(e)

            }





    # ==============================
    # GENERATION
    # ==============================


    def generate(
        self,
        prompt,
        history=None
    ):


        if not self.inference:


            status = self.load_model()


            if status["status"] == "failed":

                return status



        return self.inference.generate(

            prompt,

            history=history

        )





    # ==============================
    # MESSAGE PROCESSING
    # ==============================


    def process_message(

        self,

        message,

        user_id="guest",

        history=None

    ):



        timestamp = datetime.now(
            timezone.utc
        ).isoformat()



        try:

            self.memory.save_memory(

                user_id,

                message

            )

        except:

            pass




        tool_result = self.router.execute(

            message

        )



        if tool_result.get("tool") != "model":


            return {

                "response":
                tool_result,

                "timestamp":
                timestamp

            }





        context = ""



        try:


            results = self.knowledge.search(

                message

            )


            if results:


                context = "\n".join(

                    x["content"]

                    for x in results

                )



        except:

            pass





        prompt = f"""

You are NEURA-1.

Answer in Arabic.

Conversation:

{history}


Knowledge:

{context}


User:

{message}


Assistant:

"""



        response = self.generate(

            prompt,

            history

        )



        return {


            "response":
            response,


            "user_id":
            user_id,


            "timestamp":
            timestamp

        }







    # ==============================
    # CODE REPAIR
    # ==============================


    def code_repair(

        self,

        code

    ):


        if not self.inference:


            self.load_model()



        return self.code_agent.fix(

            code,

            self

        )







    # ==============================
    # STATUS
    # ==============================


    def get_status(self):


        return {


            "name":
            self.name,


            "version":
            self.version,


            "model":
            self.model_loader.model_name,


            "loaded":
            self.model is not None,


            "inference":
            self.inference is not None,


            "memory":
            True,


            "knowledge":
            True,


            "tools":
            self.tools.available_tools(),


            "router":
            True,


            "code_agent":
            True

        }







    def health(self):


        return {


            "status":
            "healthy",


            "name":
            self.name,


            "version":
            self.version,


            "time":
            datetime.now(
                timezone.utc
            ).isoformat()

        }