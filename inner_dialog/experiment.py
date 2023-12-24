import logging
from inner_dialog.model import Model
from inner_dialog.hier_info_struct import hier_info_struct
from inner_dialog.run_model import run_model
from inner_dialog.info_cov import info_cov
import json


use_cache = False  # debug
model = Model.INNER_DIALOG
placeholder = "qq"


def main():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - %(levelname)s - %(message)s",
    #     filename="inner_dialog.log",
    #     filemode="w",
    # )

    # load dataset and get q and a.
    with open("data/t2cb.json") as f:
        t2cb = json.load(f)

    total_path_coverage_score = 0
    for entry in t2cb:
        question = entry["question"]
        ref_dict = {placeholder: entry["final hierarchical concept"]}

        # get prediction from system.
        pred_content = run_model(
            question=question,
            model=model,
            use_cache=use_cache,
        )
        pred_dict = {placeholder: pred_content}

        # # # Exp1: Information coverage.
        # # info_cov(ref_dict=ref_dict, pred_dict=pred_dict)

        # Exp2: Hierarchical relation.
        path_coverage_score = hier_info_struct(ref_dict=ref_dict, pred_dict=pred_dict)
        total_path_coverage_score += path_coverage_score

    print(f"Average path coverage score: {total_path_coverage_score/len(t2cb)}")


if __name__ == "__main__":
    main()