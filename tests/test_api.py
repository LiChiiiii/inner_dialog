import requests
import json


def test_api():
    question = "things to consider before choosing a career"
    model = "inner_dialog"
    api_url = "http://140.116.245.152:3211/gen_mindmap/"
    res = requests.get(
        api_url,
        params={
            "question": question,
            "model": model,
            "use_cache": True,
            "force_write_cache": False,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imdlbl9taW5kbWFwIn0._o0YEp70nondUuckGagYUtlYMc5qXWR7LBh8abDQxEg",
        },
        headers={"Content-type": "application/json"},
    )

    if res.status_code == 200:
        print(res.content)
        data_dict = json.loads(res.content)
        print(data_dict)
    else:
        print("request failed")


if __name__ == "__main__":
    test_api()
