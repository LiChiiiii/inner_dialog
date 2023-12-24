"""Usage: excute this file and > output"""

from sentence_transformers import SentenceTransformer, util
from evaluate import load
from tqdm import tqdm
from inner_dialog.utils import flatten_hier_json

threshold: int = 0.6


def bertscore_wrapper(lhs: str, rhs: str) -> float:
    # NOTE:
    # - use precision or recall or f1? or simpler consine similarity
    # - implement batch similarity
    bertscore = load("bertscore")
    results = bertscore.compute(
        predictions=[lhs],
        references=[rhs],
        lang="en",
        model_type="distilbert-base-uncased",
    )
    return results["precision"][0]


def sentense_transformer_wrapper(lhs: str, rhs: str) -> float:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    emb1 = model.encode(lhs, convert_to_tensor=True)
    emb2 = model.encode(rhs, convert_to_tensor=False)
    sim = util.pytorch_cos_sim(emb1, emb2).numpy()[0][0]
    return sim


def similarity(lhs: str, rhs: str) -> float:
    # NOTE: Sentense transformer is better.
    # return bertscore_wrapper(lhs, rhs)
    return sentense_transformer_wrapper(lhs, rhs)


def find_max_sim(concept: str, labels: list[str]) -> tuple[str, float]:
    """
    Output the most similar label.
    If no label is above the similarity threshold, return none.
    """
    max_score = 0
    max_idx = -1
    for i, label in enumerate(labels):
        score = similarity(concept, label)
        if score > max_score:
            max_score = score
            max_idx = i
    return labels[max_idx], max_score


def find_losses(hits: list[tuple[str, str]], labels: list[str]) -> list[str]:
    """Return labels that is not hit."""
    hits_set = {hit[1] for hit in hits}
    losses = [label for label in labels if label not in hits_set]
    return losses


def output_f1(tp: float, fp: float, fn: float) -> None:
    # Calculate result.
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * tp / (2 * tp + fp + fn)

    print("\n\n-------------- Summary --------------")
    print(f"precision: {precision}")
    print(f"recall: {recall}")
    print(f"f1: {f1}")


def batch_rescue(
    misses: tuple[str, str, float]
) -> tuple[tuple[str, str, float], tuple[str, str, float]]:
    """Classify concept relation between pred and ref.

    Args:
        misses (tuple[str, str, float]): A list of missed concept.

    Returns:
        tuple[str, str, float]: A list of recued concept.

        tuple[str, str, float]: A new list of missed concept.
    """
    # TODO: Prompt chatgpt to detect relation
    return [], misses


def info_cov(ref_dict: dict, pred_dict: dict) -> None:
    """Information coverage experiment.

    Calculate using concept f1 and print the result on screen.

    Args:
      ref_dict (dict): Dictionary of golden hierarchical concept.

      pred_dict (dict): Dictionary of predicted hierarchical concept.
    """
    pred_list = flatten_hier_json(pred_dict)
    ref_list = flatten_hier_json(ref_dict)

    hits = list()
    misses = list()
    for pred in tqdm(pred_list):
        result, score = find_max_sim(pred, ref_list)
        if score >= threshold:
            hits.append((pred, result, score))
        else:
            misses.append((pred, result, score))

    rescued, misses = batch_rescue(misses)
    hits.extend(rescued)

    losses = find_losses(hits, ref_list)

    # Print the result.
    print("\n\n-------------- hits --------------")
    for hit in hits:
        print(hit)
    print("\n\n-------------- misses --------------")
    for miss in misses:
        print(f'"{miss}"')
    print("\n\n-------------- loss --------------")
    for loss in losses:
        print(f'"{loss}"')

    output_f1(tp=len(hits), fp=len(misses), fn=len(losses))
