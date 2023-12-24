import inner_dialog.info_cov as infocov

def test_sentense_transformer_wrapper() -> None:
  print("(pred, ref, score)")

  ref = "qq starting a business assess and minimize financial risks"
  pred = "qq Business Planning Financial resources"
  score = infocov.sentense_transformer_wrapper(pred, ref)
  print(f"({pred}, {ref}, {score})")

  pred = "qq Business Essentials Risk assessment Contingency plans"
  score = infocov.sentense_transformer_wrapper(pred, ref)
  print(f"({pred}, {ref}, {score})")

if __name__ == "__main__":
  test_sentense_transformer_wrapper()