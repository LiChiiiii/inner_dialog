from inner_dialog.auth import auth


def test_auth():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imdlbl9taW5kbWFwIn0._o0YEp70nondUuckGagYUtlYMc5qXWR7LBh8abDQxEg"
    api_id = "37"
    is_verified, msg = auth(token=token, api_id=api_id)

    print(f"is_verified: {is_verified}")
    print(f"msg: {msg}")


if __name__ == "__main__":
    test_auth()
