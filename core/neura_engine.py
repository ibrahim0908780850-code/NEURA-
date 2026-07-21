"""
NEURA-1 Core Engine

Connects NEURA intelligence with:
- Qwen model
- Inference system
- Memory system
- Knowledge base
"""

from datetime import datetime

from core.model_loader import ModelLoader
from core.inference import InferenceEngine
from core.memory import MemorySystem
from core.knowledge import KnowledgeBase


class NEURAEngine:
    """
    Main AI engine for NEURA-1.
    """

    def __init__(self):
        self.name = "NEURA-1"
        self.version = "0.4.0"

        self.model_loader = ModelLoader()

        self.model = None
        self.inference = None

        self.memory = MemorySystem()
        self.knowledge = KnowledgeBase()

        self.created = datetime.utcnow()

        # Initial NEURA knowledge
        self.knowledge.add_knowledge(
            "NEURA-1",
            "NEURA-1 is an Arabic-first cloud AI system built by Neural AI Organization."
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

    def process_message(self, message, user_id="guest"):
        """
        Process user message using memory,
        knowledge and AI inference.
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
                "user_id": user_id,
                "status": "waiting"
            }

        response = self.inference.generate(
            prompt
        )

        return {
            "response": response,
            "memory": self.memory.get_memories(user_id),
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
            "model_loaded": self.model is not None,
            "inference_ready": self.inference is not None,
            "memory_ready": self.memory is not None,
            "knowledge_ready": self.knowledge is not None
        }