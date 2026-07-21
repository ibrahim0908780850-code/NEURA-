"""
NEURA-1 Core Engine

Connects NEURA intelligence with:
- Qwen model
- Inference system
- Memory system
- Knowledge base
- Tools system
"""

from datetime import datetime

from core.config import Config
from core.model_loader import ModelLoader
from core.inference import InferenceEngine
from core.memory import MemorySystem
from core.knowledge import KnowledgeBase
from core.tools import ToolsSystem


class NEURAEngine:
    """
    Main AI engine for NEURA-1.
    """

    def __init__(self):

        self.config = Config()

        self.name = "NEURA-1"
        self.version = "0.5.0"

        self.model_loader = ModelLoader()

        self.model = None
        self.inference = None

        self.memory = MemorySystem()
        self.knowledge = KnowledgeBase()
        self.tools = ToolsSystem()

        self.created = datetime.utcnow()


        self.knowledge.add_knowledge(
            "NEURA-1",
            "NEURA-1 is an Arabic-first cloud AI system built by Neural AI."
        )


    def load_model(self):
        """
        Load Qwen model and initialize inference.
        """

        self.model = self.model_loader.load()

        self.inference = InferenceEngine(
            model=self.model,
            tokenizer=self.model_loader.tokenizer
        )

        return {
            "status": "model loaded",
            "model": self.model_loader.model_name
        }


    def process_message(
        self,
        message,
        user_id="guest",
        history=None
    ):
        """
        Process user message.
        """

        self.memory.save_memory(
            user_id,
            message
        )


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


        if self.inference is None:

            return {
                "response": "NEURA-1 model is not loaded yet.",
                "status": "waiting"
            }


        response = self.inference.generate(
            prompt,
            history=history
        )


        return {
            "response": response,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }


    def get_status(self):
        """
        Return system status.
        """

        return {
            "name": self.name,
            "version": self.version,
            "model": self.model_loader.model_name,
            "model_loaded": self.model is not None,
            "inference_ready": self.inference is not None,
            "memory_ready": True,
            "knowledge_ready": True,
            "tools_ready": True
        }