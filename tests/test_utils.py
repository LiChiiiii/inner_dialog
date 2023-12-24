from inner_dialog import utils
import json


def test_article2hiercc():
    article = """
   Before traveling to a foreign country, there are several important things to consider to ensure a smooth and enjoyable trip. Here are some key points:

Passport and Visa Requirements: Check if you need a passport, and make sure it is valid for at least six months beyond your planned departure date. Additionally, research visa requirements for your destination and apply well in advance if necessary.

Health and Safety: Research the health and safety situation in your destination. Check if any vaccinations are required or recommended and obtain necessary medications or prescriptions. Understand the local laws, customs, and cultural norms to ensure you respect and adhere to them. 
    """
    hiercc_dict = utils.article2hiercc(article=article)
    print(hiercc_dict)


def test_flatten_hier_json():
    jsonstr = """
    {
      "concept1": {
        "concept2": {
          "concept5": {
            "concept6": null,
            "concept7": null,
            "concept8": null,
            "concept9": null
          }
        },
        "concept3": null
      },
      "concept4": null
    }
    """
    data = json.loads(jsonstr)
    concepts = utils.flatten_hier_json(data)
    assert set(concepts) == {
      "concept1",
      "concept2",
      "concept3",
      "concept4",
      "concept5",
      "concept6",
      "concept7",
      "concept8",
      "concept9",
    }


if __name__ == "__main__":
    # test_article2hiercc()
    test_flatten_hier_json()
