from evaluate import load

threshold = 0.9


def test_bertscore_similar():
    bertscore = load("bertscore")
    preds = [
        "determine min living cost",
        "define target customer",
    ]
    refs = [
        "determine minimum living cost",
        "define target audience",
    ]
    results = bertscore.compute(
        predictions=preds,
        references=refs,
        lang="en",
        model_type="distilbert-base-uncased",
    )
    print(results)

    for score in results["precision"]:
        assert score > threshold
    for score in results["recall"]:
        assert score > threshold
    for score in results["f1"]:
        assert score > threshold


if __name__ == "__main__":
    test_bertscore_similar()
