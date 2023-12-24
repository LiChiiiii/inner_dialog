import openai
from inner_dialog.chatgpt import t2cb_ask_chatgpt
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def test_t2cb_ask_chatgpt():
    question = "things to consider before travelling to a foreign country"
    result = t2cb_ask_chatgpt(question=question)
    print(result)


def test_chatgpt_raw():
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {
                "role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020.",
            },
            {"role": "user", "content": "Where was it played?"},
        ],
    )
    ans = res["choices"][0]["message"]["content"]
    print(ans)


if __name__ == "__main__":
    test_t2cb_ask_chatgpt()
