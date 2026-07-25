"""
NEURA-1 Core Engine v0.8

Main intelligence layer.
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

        # ======================
        # AI Model
        # ======================

        self.model_loader = ModelLoader()
        self.model = None
        self.inference = None

        # ======================
        # Core Systems
        # ======================

        self.memory = MemorySystem()
        self.knowledge = KnowledgeBase()
        self.tools = ToolsSystem()

        # ======================
        # Agents
        # ======================

        self.code_agent = CodeAgent()

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
NEURA-1 is an Arabic-first AI assistant.

Features:
- Memory
- Knowledge Base
- Web Search
- Tool Calling
- Code Analysis
- Code Repair
"""
        )

    # ====================================
    # Model Loading
    # ====================================

    def load_model(self):

        if self.inference is not None:

            return {
                "status": "already_loaded",
                "model": self.model_loader.model_name
            }

        try:

            self.model = self.model_loader.load()

            self.inference = (
                self.model_loader.inference
            )

            return {
                "status": "loaded",
                "model": self.model_loader.model_name
            }

        except Exception as e:

            return {
                "status": "failed",
                "error": str(e)
            }

    # ====================================
    # AI Generate
    # ====================================

    def generate(
        self,
        prompt
    ):

        if self.inference is None:

            result = self.load_model()

            if result["status"] == "failed":

                return result

        return self.inference.generate(prompt)

    # ====================================
    # Message Processing
    # ====================================

    def process_message(
        self,
        message,
        user_id="guest",
        history=None
    ):

        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

        # حفظ الرسالة في الذاكرة
        try:
            self.memory.save_memory(
                user_id,
                message
            )
        except Exception:
            pass

        # تشغيل الـ Router
        tool_result = self.router.execute(
            message
        )

        # إذا كانت الأداة ليست النموذج
        if tool_result.get("tool") != "model":

            return {
                "response": tool_result,
                "user_id": user_id,
                "timestamp": timestamp
            }

        # ======================
        # Knowledge Retrieval
        # ======================

        context = ""

        try:

            knowledge = self.knowledge.search(
                message
            )

            if knowledge:

                context = "\n".join(
                    item["content"]
                    for item in knowledge
                )

        except Exception:
            pass

        # ======================
        # Build Prompt
        # ======================

        prompt = ""

        if history:

            prompt += f"""
Conversation History

{history}

"""

        if context:

            prompt += f"""
Knowledge

{context}

"""

        prompt += f"""
User

{message}

Assistant
"""

        # ======================
        # AI Generation
        # ======================

        response = self.generate(
            prompt
        )

        return {

            "response": response,

            "user_id": user_id,

            "timestamp": timestamp

        }
    # ====================================
    # Code Repair
    # ====================================

    def code_repair(
        self,
        code
    ):

        if self.inference is None:
            self.load_model()

        return self.code_agent.fix(
            code,
            self
        )

    # ====================================
    # Engine Status
    # ====================================

    def get_status(self):

        return {

            "name": self.name,

            "version": self.version,

            "model": self.model_loader.model_name,

            "model_loaded":
                self.model is not None,

            "inference_ready":
                self.inference is not None,

            "memory_ready":
                self.memory is not None,

            "knowledge_ready":
                self.knowledge is not None,

            "tools":
                self.tools.available_tools(),

            "router_ready":
                self.router is not None,

            "code_agent_ready":
                self.code_agent is not None,

            "created":
                self.created.isoformat()

        }

    # ====================================
    # Reload Model
    # ====================================

    def reload_model(self):

        self.model = None
        self.inference = None

        return self.load_model()

    # ====================================
    # Health Check
    # ====================================

    def health(self):

        return {

            "status": "healthy",

            "engine": self.name,

            "version": self.version,

            "utc_time":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }