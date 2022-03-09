from os.path import isfile

from gensim.test.utils import common_texts
from gensim.models.word2vec import Text8Corpus
from gensim.models import Word2Vec
from gensim.models.keyedvectors import Word2VecKeyedVectors
import gensim.downloader as api


class WordModel:
    def __init__(self):
        print("New word model")

    def loadWv(self, wv = None):
        if(wv):
            self.wv = wv
        elif isfile("../resources/wv.model"):
            print("Loading model from file")
            self.wv = Word2VecKeyedVectors.load("../resources/wv.model")
        else:
            self.wv = api.load("glove-wiki-gigaword-100")
            self.wv.save("../resources/wv.model")

    def loadManual(self, retrain = False):
        self.modelLoc = "../resources/word2vec.model"

        if (not retrain and isfile(self.modelLoc)):
            print("Loading model from file")
            self.model = Word2Vec.load(self.modelLoc)
        else:
            sentences = Text8Corpus('../resources/enwik8')
            self.model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)
            self.model.save(self.modelLoc)

    def checkSim(self, word1, word2):
        if (word1 in self.wv.vocab) and (word2 in self.wv.vocab):
            return self.wv.similarity(word1, word2)
        else:
            return -1

    def getSimWords(self, word):
        vector = self.model.wv[word]
        sims = self.model.wv.most_similar(word, topn=10)
        return sims

    def check(self):
        print("check")

    def predictWithContext(self, context):
        return self.model.predict_output_word(context, topn=10)

    def analogy(self, fro1, to1, fro2):
        wv = self.wv
        return wv.most_similar(positive=[to1, fro2], negative=[fro1])
