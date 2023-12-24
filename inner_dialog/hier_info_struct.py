from inner_dialog.info_cov import sentense_transformer_wrapper


def get_all_path(mind_map: dict) -> list[str]:
    """Enumerate all the root-to-leaf path of given mind map.

    Concate all the arguments in the path into a argument
    chain.

    Args:
      mind_map (dict): The mind map represented as a nested dict.

    Returns:
      list[str]: A list of argument chains.
    """

    def recursive_preorder(
        path: list[str], submap: dict, key: str, paths: list[str]
    ) -> None:
        if submap == None:
            path_str = " ".join(path) + " " + key
            paths.append(path_str)
            return

        path.append(key)
        for key in submap:
            recursive_preorder(path, submap[key], key, paths)
        path.pop()

    key = next(iter(mind_map.keys()))
    paths = []
    path = []
    recursive_preorder(path, mind_map[key], key, paths)
    return paths


def path_matching(ref_paths: list[str], pred_paths: list[str]) -> float:
    """Find the most similar path for every ref path and return a path
    coverage score.

    Args:
      ref_paths (list[str]): All the path in ref mind map.

      pred_paths (list[str]): All the path in predicted mind map.

    Returns:
        float: Path coverage score.
    """
    total_score = 0
    print("(ref_path, most_similar_pred_path, score)")
    for ref_path in ref_paths:
        # max_score = max(
        #     [
        #         sentense_transformer_wrapper(ref_path, pred_path)
        #         for pred_path in pred_paths
        #     ]
        # )

        max_score = -1
        most_sim = ""
        for pred_path in pred_paths:
            score = sentense_transformer_wrapper(ref_path, pred_path)
            if score > max_score:
                most_sim = pred_path
                max_score = score
        print(f"({ref_path}, {most_sim}, {max_score})")
        total_score += max_score
    path_coverage_score = total_score / len(ref_paths)
    print(f"path coverage score: {path_coverage_score}")
    return path_coverage_score


def hier_info_struct(ref_dict: dict, pred_dict: dict) -> float:
    """Hierarchical relation experiment.

    Calculate using weighted concept f1 and print the result on screen.

    Args:
      ref_dict (dict): Dictionary of golden hierarchical concept.

      pred_dict (dict): Dictionary of predicted hierarchical concept.

    Returns:
        float: Path coverage score.
    """
    ref_paths = get_all_path(ref_dict)
    pred_paths = get_all_path(pred_dict)
    print(f"num of ref paths: {len(ref_paths)}")  # debug
    print(f"num of pred paths: {len(pred_paths)}")  # debug
    path_coverage_score = path_matching(ref_paths, pred_paths)
    return path_coverage_score
