from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from re import sub


class EmailTokenizer:
    stemmer = SnowballStemmer("english")

    def run(self, text):
        tokens = self.tokenize(text)
        if tokens:
            tokens = (sub('[^A-Za-z0-9]+', '', word) for word in tokens)
            tokens = (word for word in tokens if word)
        return self.stem(tokens)

    def stem(self, tokens):
        if tokens:
            return (self.stemmer.stem(t) for t in tokens)
        return tokens

    def tokenize(self, text):
        if text:
            return word_tokenize(text)
        return text