from nnsplit import NNSplit

class SentenceSplitConfig:
    model_name = "en"    

sentence_split = SentenceSplitConfig()

def get_sentence_split_configured():
    return NNSplit.load(sentence_split.model_name)
