from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def test_sentense_transformer_negative():
    sent1 = "i like apple"
    sent2 = "i hate apple"
    emb1 = model.encode(sent1, convert_to_tensor=True)
    emb2 = model.encode(sent2, convert_to_tensor=False)
    sim = util.pytorch_cos_sim(emb1, emb2).numpy()[0][0]
    assert sim < 0.9
    print((sent1, sent2, sim))

def test_sentense_transformer_different():
    sent1 = "i like apple"
    sent2 = "i like travel"
    emb1 = model.encode(sent1, convert_to_tensor=True)
    emb2 = model.encode(sent2, convert_to_tensor=False)
    sim = util.pytorch_cos_sim(emb1, emb2).numpy()[0][0]
    assert sim < 0.8
    print((sent1, sent2, sim))

if __name__ == "__main__":
    test_sentense_transformer_different()
    test_sentense_transformer_negative()
