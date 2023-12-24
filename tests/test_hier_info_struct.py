import json
from inner_dialog import hier_info_struct


def test_get_all_path() -> None:
    mind_map = {
        "l0": {
            "l1-0": {
                "l2-0": None,
                "l2-1": None,
                "l2-2": None,
                "l2-3": None,
            },
            "l1-1": {
                "l2-0": {
                    "l3-0": None,
                }
            },
        }
    }
    ans = {
        "l0" + " " + "l1-0" + " " + "l2-0",
        "l0" + " " + "l1-0" + " " + "l2-1",
        "l0" + " " + "l1-0" + " " + "l2-2",
        "l0" + " " + "l1-0" + " " + "l2-3",
        "l0" + " " + "l1-1" + " " + "l2-0" + " " + "l3-0",
    }

    paths = hier_info_struct.get_all_path(mind_map=mind_map)
    for path in paths:
        assert path in paths

    # def test_with_real_data():
    #     with open("data/extract_cache.json") as f:
    #         q = "things to consider before starting a podcast"
    #         data = json.load(f)[q]
    #         mind_map2 = {q: data}

    #     paths = hier_info_struct.get_all_path(mind_map=mind_map2)
    #     for path in paths:
    #         print(path)
    # test_with_real_data()


def test_path_matching():
    ref_paths = ["a b c"]
    pred_paths = [
        "a1 b1 c1",
        "a1 b1 d1",
    ]
    hier_info_struct.path_matching(ref_paths=ref_paths, pred_paths=pred_paths)

    # def test_real_data():
    #     # Expected match list:
    #     # (gold123456, pred1x235)
    #     # (gold123457, pred1x235)
    #     # (gold1289, pred1x289)
    #     # (gold_money, pred) > (gold_sthelse, pred) since at least pred talks about money too.
    #     gold123456 = "it is not easy to make money as a podcaster earn money by landing sponsorship using cost per mille pricing model mid-roll ads longer ads in the middle of the show"
    #     gold123457 = "it is not easy to make money as a podcaster earn money by landing sponsorship using cost per mille pricing model mid-roll ads charge more: $20 per 1000 listener"
    #     gold1289 = "it is not easy to make money as a podcaster ask your subscribers to pay patreon"
    #     gold_money = "it is not easy to make money as a podcaster most people start with a negative cash flow people invest in their equipment and studio setup before starting"
    #     gold_sthelse = "what equipment is needed for a podcast? a microphone for beginer, use dynamic mic dynamic mic is less sensitive to ambient noise"

    #     pred1x235 = "how to start a pod cast learn how to monitize your podcast sponsorship ads mid-roll"
    #     pred1x289 = "how to start a pod cast learn how to monitize your podcast pay membership paytreon"

    #     ref_paths = [
    #         gold123456,
    #         gold123457,
    #         gold1289,
    #         gold_money,
    #         gold_sthelse,
    #     ]

    #     pred_paths = [
    #         pred1x235,
    #         pred1x289,
    #     ]
    #     hier_info_struct.path_matching(ref_paths=ref_paths, pred_paths=pred_paths)

    # test_real_data()


def test_hier_info_struct():
    q = "things to consider before traveling to a foreign country"
    placeholder = "yoyo"
    with open("data/chatgpt_cache.json") as f:
        data = json.load(f)[q]
        pred_dict = {placeholder: data}
    with open("data/extract_cache.json") as f:
        data = json.load(f)[q]
        ref_dict = {placeholder: data}

    hier_info_struct.hier_info_struct(ref_dict=ref_dict, pred_dict=pred_dict)


if __name__ == "__main__":
    test_hier_info_struct()
