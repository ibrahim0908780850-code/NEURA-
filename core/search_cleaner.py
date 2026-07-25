"""
NEURA-1 Search Cleaner v0.9

Cleans and prepares web search results
before sending them to NEURA-1.
"""


import re
import html




class SearchCleaner:


    @staticmethod
    def clean(text):


        if not text:

            return ""



        # Decode HTML entities

        text = html.unescape(
            text
        )



        # Remove HTML tags

        text = re.sub(

            r"<[^>]+>",

            "",

            text

        )




        # Remove unwanted patterns

        remove_patterns = [


            r"Shutterstock.*",


            r"FILE PHOTO.*",


            r"Getty Images.*",


            r"purchase_order.*",


            r"client:.*",


            r"job:.*",


            r"other:.*",


            r"cookie.*",


            r"privacy policy.*",


            r"إعلان",


            r"اقرأ المزيد",


            r"اشترك الآن"

        ]



        for pattern in remove_patterns:


            text = re.sub(

                pattern,

                "",

                text,

                flags=re.IGNORECASE | re.DOTALL

            )




        # Remove URLs

        text = re.sub(

            r"https?://\S+",

            "",

            text

        )




        # Remove emails

        text = re.sub(

            r"\S+@\S+",

            "",

            text

        )




        # Normalize spaces

        text = re.sub(

            r"\s+",

            " ",

            text

        )




        # Remove repeated punctuation

        text = re.sub(

            r"([.!؟])\1+",

            r"\1",

            text

        )




        return text.strip()




# =====================
# Test
# =====================


if __name__ == "__main__":


    sample = """

    <div>

    إعلان

    أحدث أخبار الذكاء الاصطناعي...

    https://example.com

    </div>

    """



    print(

        SearchCleaner.clean(
            sample
        )

    )