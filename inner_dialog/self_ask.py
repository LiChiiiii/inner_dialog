import json
from inner_dialog.utils import article2hiercc


def t2cb_ask_selfask(question: str) -> str:
    """Ask T2CB question to reflexion.

    Args:
        question (str): Things to consider before ...

    Returns
        str: Reflexion's response.
    """
    return "article"


if __name__ == "__main__":
    question = "things to consider before traveling to a foreign country."
    article = t2cb_ask_selfask(question)
    print(article)
    hierr = article2hiercc(article)
    hierr_str = json.dumps(hierr, indent=2)
    print(hierr_str)
