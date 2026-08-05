"""
NEURA-1 Core Engine v0.9.3

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
        self.version = "0.9.3"


        # ======================
        # AI MODEL
        # ======================

        self.model_loader = ModelLoader()

        self.model = None
        self.inference = None



        # ======================
        # CORE SYSTEMS
        # ======================

        self.memory = MemorySystem()

        self.knowledge = KnowledgeBase()



        # ======================
        # AGENTS
        # ======================

        self.code_agent = CodeAgent()



        # ======================
        # TOOLS
        # ======================

        self.tools = ToolsSystem(
            engine=self
        )



        # ======================
        # ROUTER
        # ======================

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
- Tool calling
- Web search
- Code analysis
- Code repair
- AI assistance
"""
        )



    # ======================
    # MODEL LOADING
    # ======================


    def load_model(self):

        if self.inference:

            return {
                "status": "already_loaded",
                "model":
                self.model_loader.model_name
            }


        try:

            self.model = self.model_loader.load()

            self.inference = (
                self.model_loader.inference
            )


            return {
                "status": "loaded",
                "model":
                self.model_loader.model_name
            }


        except Exception as e:

            return {
                "status": "failed",
                "error": str(e)
            }




    # ======================
    # RESPONSE CLEANER
    # ======================


    def clean_response(self, response):

        if not response:
            return "لم يتم إنشاء رد."


        if isinstance(response, dict):

            # OpenAI format

            if "choices" in response:

                try:

                    content = (
                        response["choices"][0]
                        ["message"]
                        .get("content", "")
                    )

                    if content:

                        return content.strip()


                except Exception:

                    pass



            if "response" in response:

                return response["response"]



            return str(response)



        if isinstance(response, str):

            text = response.strip()


            # Remove hidden reasoning

            if "Thinking Process:" in text:

                text = text.split(
                    "Thinking Process:"
                )[0]


            if "reasoning" in text.lower():

                return (
                    "أعتذر، حدثت مشكلة "
                    "في معالجة الإجابة."
                )


            return text



        return str(response)





    # ======================
    # AI GENERATION
    # ======================


    def generate(
        self,
        prompt,
        history=None
    ):


        if not self.inference:

            result = self.load_model()


            if result["status"] == "failed":

                return result



        try:


            result = self.inference.generate(
                prompt,
                history=history,
                max_tokens=512
            )


            return self.clean_response(
                result
            )



        except Exception as e:


            return {
                "error": str(e)
            }





    # ======================
    # MESSAGE PROCESSING
    # ======================


    def process_message(
        self,
        message,
        user_id="guest",
        history=None
    ):


        timestamp = datetime.now(
            timezone.utc
        ).isoformat()



        # MEMORY

        try:

            self.memory.save_memory(
                user_id,
                message
            )

        except Exception:

            pass





        # TOOLS

        try:

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


        except Exception:

            pass





        # KNOWLEDGE

        context = ""


        try:

            results = self.knowledge.search(
                message
            )


            if results:

                context = "\n".join(

                    item["content"]

                    for item in results

                )


        except Exception:

            pass





        history_text = (

            history

            or

            "No previous conversation"

        )





        prompt = f"""

You are NEURA-1.

You are an advanced Arabic AI assistant.


Rules:

- Answer mainly in Arabic.
- Be accurate.
- Explain clearly.
- Do not reveal internal reasoning.
- Return only the final answer.



Conversation:

{history_text}



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





    # ======================
    # CODE REPAIR
    # ======================


    def code_repair(
        self,
        code
    ):


        return self.code_agent.fix(
            code,
            self
        )





    # ======================
    # STATUS
    # ======================


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


            "memory_ready":
            True,


            "knowledge_ready":
            True,


            "tools":
            self.tools.available_tools(),


            "router_ready":
            True,


            "code_agent_ready":
            True,


            "created":
            self.created.isoformat()

        }





    # ======================
    # HEALTH
    # ======================


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