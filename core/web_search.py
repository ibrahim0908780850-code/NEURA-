"""
NEURA-1 Web Search Tool

Allows NEURA-1 to search the internet.
"""

import os
import requests

from core.search_cleaner import SearchCleaner


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
                "success": False,
                "error": "Web search unavailable"
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


            results = []


            for item in data.get(
                "results",
                []
            ):

                results.append({

                    "title":
                        item.get(
                            "title",
                            ""
                        ),

                    "url":
                        item.get(
                            "url",
                            ""
                        ),

                    "content":
                        SearchCleaner.clean(
                            item.get(
                                "content",
                                ""
                            )
                        )

                })


            return {

                "success": True,

                "answer":
                    data.get(
                        "answer",
                        ""
                    ),

                "results":
                    results

            }


        except requests.exceptions.Timeout:

            return {

                "success": False,

                "error":
                    "Search request timeout"

            }


        except requests.exceptions.RequestException as e:

            return {

                "success": False,

                "error":
                    str(e)

            }


        except Exception as e:

            return {

                "success": False,

                "error":
                    f"Unexpected error: {str(e)}"

            }



if __name__ == "__main__":

    web = WebSearch()


    result = web.search(
        "آخر أخبار الذكاء الاصطناعي"
    )


    print(result)