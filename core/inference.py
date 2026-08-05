"""
NEURA-1 Inference Engine v0.9.3

Uses Hugging Face Inference Providers API.

Features:
- Chat Completion
- Arabic-first system prompt
- History support
- Response cleaning
- Error handling
"""


import os

from huggingface_hub import InferenceClient




class InferenceEngine:



    def __init__(
        self,
        model=None,
        tokenizer=None
    ):


        self.model_name = (

            model

            or os.getenv(
                "MODEL_NAME",
                "Qwen/Qwen3.5-9B"
            )

        )



        self.client = InferenceClient(

            api_key=os.getenv(
                "HF_TOKEN"
            )

        )



        self.system_prompt = """

You are NEURA-1.

Arabic-first advanced AI assistant.

Rules:

- Answer mainly in Arabic.
- Never reveal internal reasoning.
- Return only the final answer.
- Help with programming and debugging.
- Explain technical concepts clearly.
- Be accurate and concise.

"""




    # =========================
    # CLEAN RESPONSE
    # =========================


    def clean_response(
        self,
        text
    ):


        if not text:

            return (
                "أعتذر، لم أتمكن "
                "من إنشاء إجابة."
            )



        text = str(text).strip()



        # Remove reasoning leakage

        if "Thinking Process:" in text:

            text = text.split(
                "Thinking Process:"
            )[0].strip()



        if "reasoning" in text.lower():

            return (
                "أعتذر، حدث خطأ "
                "في معالجة الإجابة."
            )



        return text






    # =========================
    # GENERATE
    # =========================


    def generate(
        self,
        user_message,
        history=None,
        max_tokens=512
    ):



        token = os.getenv(
            "HF_TOKEN"
        )



        if not token:


            return {

                "error":
                "HF_TOKEN missing"

            }




        messages = [

            {

                "role":
                "system",

                "content":
                self.system_prompt

            }

        ]




        # Conversation history


        if history:


            for item in history:


                if (

                    "role" in item

                    and

                    "content" in item

                ):


                    messages.append({

                        "role":
                        item["role"],

                        "content":
                        item["content"]

                    })





        messages.append({

            "role":
            "user",

            "content":
            user_message

        })





        try:


            response = (

                self.client

                .chat

                .completions

                .create(

                    model=
                    self.model_name,


                    messages=
                    messages,


                    max_tokens=
                    max_tokens,


                    temperature=
                    0.5,


                    top_p=
                    0.9

                )

            )





            # OpenAI compatible response


            content = (

                response

                .choices[0]

                .message

                .content

            )



            return self.clean_response(
                content
            )





        except Exception as e:


            return {

                "error":
                str(e),

                "model":
                self.model_name

            }





    # =========================
    # STATUS
    # =========================


    def status(self):


        return {


            "provider":
            "HuggingFace Inference API",


            "model":
            self.model_name,


            "ready":
            bool(
                os.getenv("HF_TOKEN")
            )

        }





# =========================
# TEST
# =========================


if __name__ == "__main__":


    ai = InferenceEngine()



    print(

        ai.generate(
            "مرحبا نيرا"
        )

    )