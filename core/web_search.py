"""
NEURA-1 Web Search Tool

Allows NEURA to search the internet.
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


    def search(self, query, limit=5):

        if not self.api_key:

            return {
                "error": "TAVILY_API_KEY missing"
            }


        payload = {

            "api_key": self.api_key,

            "query": query,

            "search_depth": "basic",

            "max_results": limit

        }


        try:

            response = requests.post(
                self.url,
                json=payload,
                timeout=30
            )


            data = response.json()


            results = []


            for item in data.get(
                "results",
                []
            ):

                results.append({

                    "title":
                        item.get("title"),

                    "url":
                        item.get("url"),

                    "content":
                        item.get("content")

                })


            return results


        except Exception as e:

            return {
                "error": str(e)
            }



if __name__ == "__main__":

    search = WebSearch()

    print(
        search.search(
            "latest AI news"
        )
    )