"""
NEURA-1 Web Search Tool

Allows NEURA-1 to search the internet.
"""

import os
import requests


class WebSearch:

    def __init__(self):

        self.api_key = os.getenv(
            "TAVILY_API_KEY"
        )

        self.url = (
            "https://api.tavily.com/search"
        )


    def search(
        self,
        query,
        limit=5
    ):

        if not self.api_key:

            return {
                "error": "TAVILY_API_KEY missing"
            }


        payload = {

            "api_key": self.api_key,

            "query": query,

            "search_depth": "advanced",

            "max_results": limit,

            "include_answer": True,

            "include_raw_content": False

        }


        try:

            response = requests.post(
                self.url,
                json=payload,
                timeout=30
            )


            response.raise_for_status()

            data = response.json()


            return {

                "answer":
                    data.get(
                        "answer",
                        ""
                    ),

                "results": [

                    {
                        "title":
                            item.get("title"),

                        "url":
                            item.get("url"),

                        "content":
                            item.get("content")

                    }

                    for item in data.get(
                        "results",
                        []
                    )

                ]

            }


        except Exception as e:

            return {
                "error": str(e)
            }


if __name__ == "__main__":

    web = WebSearch()

    print(
        web.search(
            "ما هو الذكاء الاصطناعي"
        )
    )