from langchain.chat_models import ChatOpenAI
from langchain.chat_models import ChatGooglePalm
import google.generativeai
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import SystemMessage, HumanMessage
import json
import openai
import os, re
from dotenv import load_dotenv

def palm_summary(article: str) -> str:
    """PALM provide bullet list of summary given an article.

    Args:
        article (str): Input article to be summarized.

    Returns:
        str: The bullet list of keyphrases acting as the summary
        of the given article.
    """
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    chat = ChatGooglePalm(temperature=0.2)
    summarize_msg_temp = HumanMessagePromptTemplate.from_template(
        """
        {article}

        provide a summary of the above text. Your summary 
        should be informative and factual, covering the most 
        important aspects of the text. Use bullet list. be concise 
        of each bullet point, only list keyphrases.
        """
    )
    messages = [
        SystemMessage(content="You are a good summarizer."),
        summarize_msg_temp.format(article=article),
    ]
    summary_msg = chat(messages)
    return summary_msg.content

def chatgpt_summary(article: str) -> str:
    """ChatGPT provide bullet list of summary given an article.

    Args:
        article (str): Input article to be summarized.

    Returns:
        str: The bullet list of keyphrases acting as the summary
        of the given article.
    """
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")
    summarize_msg_temp = HumanMessagePromptTemplate.from_template(
        """
        {article}

        provide a summary of the above text. Your summary 
        should be informative and factual, covering the most 
        important aspects of the text. Use bullet list. be concise 
        of each bullet point, only list keyphrases.
        """
    )
    messages = [
        SystemMessage(content="You are a good summarizer."),
        summarize_msg_temp.format(article=article),
    ]
    summary_msg = chat(messages)
    return summary_msg.content


def article2hiercc_chatgpt(article: str) -> dict:
    """Summarize the article and produce hierarchical concept as dictionary.

    Use ChatGPT to perform bullet list summary and extract hierarchical
    concept.

    Args:
      article (str): An article from website or system output.
    Returns:
      dict: Hierarchical concept.
    """
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    chat = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k")

    summarize_msg_temp = HumanMessagePromptTemplate.from_template(
        """
        {article}

        provide a summary of the above text. Your summary 
        should be informative and factual, covering the most 
        important aspects of the text. Use bullet list.
        """
    )

    extract_hiercc_msg = HumanMessage(
        content="""
        Organize the above points into a JSON format  represents the hierarchical 
        organization of the points, with each topic and sub-topic listed as keys, 
        and their corresponding sub-topics as or examples (if any) as their values, 
        if it does not have sub-topic or examples, just put null (not None). 
        Here is an example JSON format:
        ```
        {{
          "hierachical concepts": {{
            "topic": {{
              "sub_topic": {{
                "sub_topic1": [example1, example2],
                "sub_topic2": why_we_should_follow_this_subtopic,
              }}
            }}
          }}
        }}
        ```
        """
    )

    messages = [
        SystemMessage(content="You are a good summarizer."),
        summarize_msg_temp.format(article=article),
    ]
    summary_msg = chat(messages)
    messages.extend(
        [
            summary_msg,
            extract_hiercc_msg,
        ]
    )
    hiercc_msg = chat(messages)
    hiercc_dict: dict = json.loads(hiercc_msg.content)
    return hiercc_dict



def article2hiercc_palm(article: str) -> dict:
    """Summarize the article and produce hierarchical concept as dictionary.

    Use PALM to extract hierarchical concept.

    Args:
      article (str): An article from website or system output.
    Returns:
      dict: Hierarchical concept.
    """
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    chat = ChatGooglePalm(temperature=0.2)


    extract_hiercc_msg = HumanMessagePromptTemplate.from_template(
        """
        {article}

        Organize the above text into a JSON format, with each topic and sub-topic listed as keys, 
        and their corresponding sub-topics as or examples (if any) as their values, 
        if there is no subtopic or there is no example after the subtopic, just put null (not None), and also put null after the example. 
        In addition, restrict the outermost key of the JSON format to each topics.
        Here is an example JSON format:
        ```json
        {{
            " ": {{
                " ": {{
                    " " : null,
                }}
            }}

        }}
        ```
        """
    )

    messages = [
        extract_hiercc_msg.format(article=article),
    ]
    hiercc_msg = chat(messages)
    print("hiercc_msg: ",hiercc_msg.content)
    # hiercc_json = hiercc_msg.content.strip('```json')
    hiercc_json = re.search(r'```json\n(.*?)\n```', hiercc_msg.content, re.DOTALL)
    print("hiercc_json: ",hiercc_json.group(1))
    hiercc_dict: dict = json.loads(hiercc_json.group(1))
    return hiercc_dict


def flatten_hier_json(data: dict) -> list[str]:
    concepts = list()
    for key, value in data.items():
        concepts.append(key)
        if isinstance(value, dict):
            concepts.extend(flatten_hier_json(data[key]))
    return concepts
