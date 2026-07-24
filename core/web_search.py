"""
NEURA-1 Web Search Tool

Allows NEURA-1 to search the internet.
"""

import os
import re
import requests


class WebSearch:

    def __init__(self):

        self.api_key = os.getenv(
            "TAVILY_API_KEY"
        )

        self.url = (
            "https://api.tavily.com/search"
        )


    def clean_content(self, text):

        if not text:
            return ""

        patterns = [
            r"Shutterstock.*",
            r"FILE PHOTO.*",
            r"purchase_order.*",
            r"client:.*",
            r"job:.*",
            r"other:.*",
            r"إعلان",
        ]

        for pattern in patterns:

            text = re.sub(
                pattern,
                "",
                text,
                flags=re.IGNORECASE | re.DOTALL
            )


        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()



    def search(
        self,
        query,
        limit=5
    ):

        if not self.api_key:

            return {
                "error":
                "Web search unavailable"
            }


        payload = {

            "api_key":
                self.api_key,

            "query":
                query,

            "search_depth":
                "advanced",

            "max_results":
                limit,

            "include_answer":
                True,

            "include_raw_content":
                False

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
                        self.clean_content(
                            item.get(
                                "content",
                                ""
                            )
                        )

                })


            return {

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
                "error":
                "Search timeout"
            }


        except requests.exceptions.RequestException as e:

            return {
                "error":
                str(e)
            }



if __name__ == "__main__":

    web = WebSearch()

    print(
        web.search(
            "آخر أخبار الذكاء الاصطناعي"
        )
    )