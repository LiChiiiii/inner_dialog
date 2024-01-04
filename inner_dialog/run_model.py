from inner_dialog.chatgpt import t2cb_ask_chatgpt
from inner_dialog.palm import t2cb_ask_palm
from inner_dialog.gemini import t2cb_ask_gemini, article2hiercc_gemini
from inner_dialog.hier_info_struct import hier_info_struct
from inner_dialog.inner_dialog import t2cb_ask_inner_dialog
from inner_dialog.model import Model
from inner_dialog.utils import article2hiercc_chatgpt, article2hiercc_palm


import json


def cache_result(
    question: str, model: Model, pred_dict: dict, force_write_cache: bool = False
) -> None:
    """Cache prediction dict if it has a cache miss."""
    if model == Model.INNER_DIALOG:
        file = "data/inner_dialog_cache.json"
    elif model == Model.GEMINI:
        file = "data/gemini_cache.json"
    elif model == Model.PALM:
        file = "data/palm_cache.json"
    elif model == Model.CHATGPT:
        file = "data/chatgpt_cache.json"
    else:
        raise NotImplementedError(f"Unknown model: {model}")

    ans = dict()
    with open(file) as f:
        ans = json.load(f)
    if question not in ans or force_write_cache:
        ans[question] = pred_dict
        with open(file, mode="w") as f:
            json.dump(ans, f, indent=2)


def run_model(question: str, model: Model, use_cache: bool, force_write_cache: bool = False) -> dict:
    """Get prediction dictionary given a question.

    Args:
        question (str): Input question.

        model (Model): Which model to run.

        use_cache (bool): Whether to use cache.

    Returns
        dict: prediction dictionary.
    """
    if use_cache:
        if model == Model.INNER_DIALOG:
            file = "data/inner_dialog_cache.json"
        elif model == Model.GEMINI:
            file = "data/gemini_cache.json"
        elif model == Model.PALM:
            file = "data/palm_cache.json"
        elif model == Model.CHATGPT:
            file = "data/chatgpt_cache.json"
        elif model == Model.EXTRACT:
            file = "data/extract_cache.json"
        else:
            raise NotImplementedError(f"Unknown model: {model}")
        with open(file) as f:
            ans = json.load(f)
        pred_dict = ans[question]
    else:
        if model == Model.INNER_DIALOG:
            article = t2cb_ask_inner_dialog(question=question)
            print(article)  # debug
            pred_dict = article2hiercc_gemini(article=article, question=question)
            print(pred_dict)  # debug
        elif model == Model.GEMINI:
            article = t2cb_ask_gemini(question=question)
            print(article)  # debug
            pred_dict = article2hiercc_gemini(article=article, question=question)
            print(pred_dict)  # debug
        elif model == Model.PALM:
            article = t2cb_ask_palm(question=question)
            print(article)  # debug
            pred_dict = article2hiercc_palm(article=article)
            print(pred_dict)  # debug
        elif model == Model.CHATGPT:
            article = t2cb_ask_chatgpt(question=question)
            print(article)  # debug
            pred_dict = article2hiercc_chatgpt(article=article)
            print(pred_dict)  # debug
        else:
            raise NotImplementedError(f"Unknown model: {model}")
        cache_result(
            question=question,
            model=model,
            pred_dict=pred_dict,
            force_write_cache=force_write_cache,
        )

    return pred_dict


def test_single_question() -> None:
    use_cache = False  # debug
    model = Model.INNER_DIALOG

    # load dataset and get q and a.
    with open("data/t2cb.json") as f:
        t2cb = json.load(f)
        # # Travel to foreign country.
        # question = t2cb[6]["question"]
        # ref_dict = t2cb[6]["final hierarchical concept"]

        # # Starting a business.
        # question = t2cb[0]["question"]
        # ref_dict = t2cb[0]["final hierarchical concept"]

        # Having a baby
        question = t2cb[2]["question"]
        ref_dict = {question: t2cb[2]["final hierarchical concept"]}

    # get prediction from system.
    pred_dict = run_model(
        question=question,
        model=model,
        use_cache=use_cache,
    )

    # # Exp1: Information coverage.
    # info_cov(ref_dict=ref_dict, pred_dict=pred_dict)

    # Exp2: Hierarchical relation.
    hier_info_struct(ref_dict=ref_dict, pred_dict=pred_dict)