"""
NEURA-1 Web Search Tool v0.9

Allows NEURA-1 to search the internet
using Tavily Search API.
"""


import os
import requests


from core.search_cleaner import SearchCleaner




class WebSearch:


    def __init__(self):


        self.name = "NEURA Web Search"

        self.version = "0.9.0"


        self.api_key = os.getenv(
            "TAVILY_API_KEY"
        )


        self.url = (
            "https://api.tavily.com/search"
        )



    # =========================
    # Search
    # =========================


    def search(
        self,
        query,
        limit=5,
        depth="advanced"
    ):


        if not self.api_key:


            return {

                "success": False,

                "tool":
                self.name,

                "error":
                "TAVILY_API_KEY missing"

            }




        payload = {


            "api_key":
            self.api_key,


            "query":
            query,


            "search_depth":
            depth,


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


                content = item.get(
                    "content",
                    ""
                )


                try:


                    content = SearchCleaner.clean(
                        content
                    )


                except Exception:


                    pass




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
                    content


                })





            return {


                "success":
                True,


                "tool":
                self.name,


                "query":
                query,


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


                "success":
                False,


                "error":
                "Search timeout"

            }





        except requests.exceptions.HTTPError as e:


            return {


                "success":
                False,


                "error":
                f"HTTP error: {str(e)}"

            }





        except Exception as e:


            return {


                "success":
                False,


                "error":
                str(e)

            }





    # =========================
    # Status
    # =========================


    def get_status(self):


        return {


            "tool":
            self.name,


            "version":
            self.version,


            "connected":
            bool(
                self.api_key
            )

        }





# =========================
# Test
# =========================


if __name__ == "__main__":


    web = WebSearch()


    print(
        web.get_status()
    )


    print(

        web.search(
            "آخر أخبار الذكاء الاصطناعي"
        )

    )