"""
NEURA-1 Core Engine v0.8

Main intelligence layer.

Connects:
- AI Model
- Memory
- Knowledge
- Tools
- Router
- Code Agent
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

        self.version = "0.8.0"



        # =====================
        # AI Model
        # =====================

        self.model_loader = ModelLoader()

        self.model = None

        self.inference = None




        # =====================
        # Core Systems
        # =====================

        self.memory = MemorySystem()

        self.knowledge = KnowledgeBase()

        self.tools = ToolsSystem()



        # =====================
        # Agents
        # =====================

        self.code_agent = CodeAgent()



        # Router

        self.router = ToolRouter(
            self.tools,
            self.code_agent,
            self
        )




        self.created = datetime.now(
            timezone.utc
        )



        self.knowledge.add_knowledge(
            "NEURA-1",
            """
NEURA-1 is an Arabic-first AI system.
Supports memory, tools, web search,
knowledge retrieval and coding assistance.
"""
        )





    # =====================
    # Model Loading
    # =====================


    def load_model(self):


        if self.inference:


            return {

                "status":
                "already loaded"

            }




        self.model = (
            self.model_loader.load()
        )


        self.inference = (
            self.model_loader.inference
        )



        return {


            "status":
            "model connected",


            "model":
            self.model_loader.model_name

        }





    # =====================
    # Message Processing
    # =====================


    def process_message(
        self,
        message,
        user_id="guest",
        history=None
    ):


        timestamp = datetime.now(
            timezone.utc
        ).isoformat()



        self.memory.save_memory(
            user_id,
            message
        )




        # Tool Router

        tool_result = self.router.execute(
            message
        )



        if tool_result.get(
            "tool"
        ) != "model":


            return {

                "response":
                tool_result,

                "user_id":
                user_id,

                "timestamp":
                timestamp

            }





        # Knowledge

        knowledge_results = (
            self.knowledge.search(
                message
            )
        )



        context = ""



        if knowledge_results:


            context = "\n".join(

                item["content"]

                for item in knowledge_results

            )





        prompt = message




        if history:


            prompt = f"""

Conversation history:

{history}


User:

{message}

"""




        if context:


            prompt += f"""

Knowledge:

{context}

"""





        if not self.inference:


            self.load_model()





        try:


            response = (
                self.inference.generate(
                    prompt
                )
            )



        except Exception as e:


            response = {


                "error":
                str(e),


                "fallback":
                "NEURA model unavailable"

            }





        return {


            "response":
            response,


            "user_id":
            user_id,


            "timestamp":
            timestamp

        }





    # =====================
    # Code Repair
    # =====================


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





    # =====================
    # Generate for Agents
    # =====================


    def generate(
        self,
        prompt
    ):


        if not self.inference:

            self.load_model()



        return self.inference.generate(
            prompt
        )






    # =====================
    # Status
    # =====================


    def get_status(self):


        return {


            "name":
            self.name,


            "version":
            self.version,


            "model":
            self.model_loader.model_name,


            "model_loaded":
            self.model is not None,


            "inference_ready":
            self.inference is not None,


            "tools":
            self.tools.available_tools(),


            "memory_ready":
            True,


            "knowledge_ready":
            True,


            "code_agent_ready":
            True,


            "router_ready":
            True

        }