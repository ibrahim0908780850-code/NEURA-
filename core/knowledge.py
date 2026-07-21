"""
NEURA-1 Knowledge Base

Stores, retrieves and manages information
to enhance AI responses.
"""

from datetime import datetime


class KnowledgeBase:
    """
    Knowledge storage system for NEURA-1.
    """

    def __init__(self):
        self.documents = []

    def add_knowledge(self, title, content, source="internal"):
        """
        Add information to knowledge base.
        """

        document = {
            "title": title,
            "content": content,
            "source": source,
            "created_at": datetime.utcnow().isoformat()
        }

        self.documents.append(document)

        return document

    def search(self, query):
        """
        Search knowledge by title or content.
        """

        results = []

        query = query.lower()

        for document in self.documents:

            title = document["title"].lower()
            content = document["content"].lower()

            if query in title or query in content:
                results.append(document)

        return results

    def get_all(self):
        """
        Return all knowledge documents.
        """

        return self.documents

    def clear(self):
        """
        Clear knowledge base.
        """

        self.documents = []


if __name__ == "__main__":

    knowledge = KnowledgeBase()

    knowledge.add_knowledge(
        "NEURA-1",
        "NEURA-1 is an Arabic-first cloud AI system.",
        "Neural AI"
    )

    result = knowledge.search(
        "Arabic"
    )

    print(result)