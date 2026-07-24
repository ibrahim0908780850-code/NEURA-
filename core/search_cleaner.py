import re


class SearchCleaner:

    @staticmethod
    def clean(text):

        if not text:
            return ""

        remove_patterns = [
            r"Shutterstock.*",
            r"FILE PHOTO.*",
            r"purchase_order.*",
            r"client:.*",
            r"job:.*",
            r"other:.*",
            r"إعلان",
        ]

        for pattern in remove_patterns:
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