"""
NEURA-1 Core Engine

Connects NEURA intelligence with:
- External AI inference
- Memory system
- Knowledge base
- Tools system
- Tool Router
- Code Agent
"""

from datetime import datetime

from core.config import Config
from core.model_loader import ModelLoader
from core.memory import MemorySystem
from core.knowledge import KnowledgeBase
from core.tools import ToolsSystem
from core.tool_router import ToolRouter
from core.code_agent import CodeAgent



class NEURAEngine:
    """
    Main AI engine for NEURA-1.
    """


    def __init__(self):

        self.config = Config()

        self.name = "NEURA-1"
        self.version = "0.6.0"


        # Model

        self.model_loader = ModelLoader()

        self.model = None
        self.inference = None



        # Memory

        self.memory = MemorySystem()



        # Knowledge

        self.knowledge = KnowledgeBase()



        # Tools

        self.tools = ToolsSystem()



        # Code Agent

        self.code_agent = CodeAgent()



        # Tool Router

        self.router = ToolRouter(
            self.tools,
            self.code_agent
        )



        self.created = datetime.utcnow()



        self.knowledge.add_knowledge(
            "NEURA-1",
            "NEURA-1 is an Arabic-first AI system with tools, memory and reasoning."
        )




    def load_model(self):

        self.model = self.model_loader.load()

        self.inference = self.model_loader.inference


        return {

            "status":
                "model connected",

            "model":
                self.model_loader.model_name

        }




    def process_message(
        self,
        message,
        user_id="guest",
        history=None
    ):


        # Save memory

        self.memory.save_memory(
            user_id,
            message
        )



        # Check tools first

        tool_result = self.router.execute(
            message
        )



        if tool_result.get("tool") != "model":

            return {

                "response":
                    tool_result,

                "user_id":
                    user_id,

                "timestamp":
                    datetime.utcnow().isoformat()

            }



        # Knowledge search

        knowledge_results = self.knowledge.search(
            message
        )


        context = ""


        if knowledge_results:

            context = "\n".join(
                item["content"]
                for item in knowledge_results
            )



        prompt = message



        if context:

            prompt = f"""
Knowledge:

{context}


User:

{message}
"""



        # Load AI model

        if self.inference is None:

            self.load_model()



        response = self.inference.generate(
            prompt
        )



        return {

            "response":
                response,

            "user_id":
                user_id,

            "timestamp":
                datetime.utcnow().isoformat()

        }





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