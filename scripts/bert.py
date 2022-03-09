from transformers import pipeline, AutoModelForMaskedLM, AutoTokenizer


class BertModel:
    def __init__(self, unmasker = None):
        if(unmasker):
            self.model = unmasker
        else:
            pretrained = AutoModelForMaskedLM.from_pretrained("distilroberta-base")
            tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")
            self.model = pipeline("fill-mask", model=pretrained, tokenizer=tokenizer)

    def predictMask(self, sentence, top_k = 20):
        return self.model(sentence, top_k = top_k)

if __name__ == "__main__":
    m = BertModel()