"""
NEURA-1 Knowledge Base

Stores and retrieves information
to enhance AI responses.
"""


class KnowledgeBase:
    """
    Basic knowledge storage system for NEURA-1.
    """

    def __init__(self):
        self.documents = []

    def add_knowledge(self, title, content):
        """
        Add information to knowledge base.
        """

        document = {
            "title": title,
            "content": content
        }

        self.documents.append(document)

        return document

    def search(self, query):
        """
        Simple knowledge search.
        """

        results = []

        for document in self.documents:
            if query.lower() in document["content"].lower():
                results.append(document)

        return results


if __name__ == "__main__":

    knowledge = KnowledgeBase()

    knowledge.add_knowledge(
        "NEURA",
        "NEURA-1 is an Arabic-first cloud AI system."
    )

    print(
        knowledge.search("Arabic")
    )