import json
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from inner_dialog.utils import article2hiercc_chatgpt, chatgpt_summary
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def mult_round_chatgpt(question: str, round: int = 3) -> str:
    """Directly give ChatGPT the question. Nothing more.

    Args:
        question (str): The question to ask.

        round (int): How many round to ask ChatGPT.

    Returns:
        str: ChatGPT's response.
    """
    ans = ""
    chat = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")
    messages = [
        SystemMessage(content="You are a good summarizer."),
        HumanMessage(content=f"{question}"),
    ]
    for _ in range(round):
        msg = chat(messages)
        ans += chatgpt_summary(msg.content) + "\n---------------\n"
        messages.extend(
            [
                msg,
                HumanMessage(content="Anything else?"),
            ]
        )
    return ans


def vanilla_chatgpt(question: str) -> str:
    """Directly give ChatGPT the question. Nothing more.

    Args:
        question (str): The question to ask.

    Returns:
        str: ChatGPT's response.
    """
    chat = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")
    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="You are a helpful assistent."),
            HumanMessage(content=f"{question}"),
        ]
    )
    chatgpt_baseline = LLMChain(llm=chat, prompt=chat_prompt_template)
    return chatgpt_baseline.run(question=question)


def t2cb_ask_chatgpt(question: str) -> str:
    """Ask T2CB question to ChatGPT.

    Args:
        question (str): Things to consider before ...

    Returns
        str: ChatGPT's response.
    """
    # response = vanilla_chatgpt(question)
    response = mult_round_chatgpt(question, round=3)
    return response


if __name__ == "__main__":
    question = "things to consider before traveling to a foreign country."
    article = t2cb_ask_chatgpt(question)
    print(article)
    hierr = article2hiercc_chatgpt(article)
    hierr_str = json.dumps(hierr, indent=2)
    print(hierr_str)
