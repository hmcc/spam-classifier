from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from tqdm import tqdm


class LexiconBuilder():
    lexicon = {}

    def add(self, word):
        if word not in self.lexicon:
            self.lexicon[word] = 0
        self.lexicon[word] += 1

    def add_all(self, iterable):
        for word in iterable:
            self.add(word)

    def get(self, wordcount):
        if not wordcount:
            return list(self.lexicon.keys())
        return [k for k, v in self.lexicon.items() if v >= wordcount]


class SVMClassifier():

    def train(self, X, y, kernel, C):
        self.model = SVC(kernel=kernel)
        self.model.fit(X, y)
        return self

    def predict(self, X):
        if not hasattr(self, 'model'):
            raise('First call train()')
        return self.model.predict(X)


def build_lexicon(processed_emails, size=100):
    lexicon = LexiconBuilder()
    pbar = tqdm(processed_emails)
    pbar.set_description('Building lexicon')
    for processed_email in tqdm(processed_emails):
        lexicon.add_all(processed_email.tokens)

    return lexicon.get(size)


def extract_features_for_one(words, lexicon):
    indices = [lexicon.index(word) for word in words if word in lexicon]
    features = [0] * len(lexicon)
    for i in indices:
        features[i] = 1
    return features


def extract_features(processed_emails, lexicon):
    features = []
    pbar = tqdm(processed_emails)
    pbar.set_description('Extracting features')
    for processed_email in tqdm(processed_emails):
        features.append(extract_features_for_one(processed_email.tokens, lexicon))
    return features


def train_and_test(X, y, test_size, kernel, C, quiet=False):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    if not quiet:
        print('Training SVM...')
    classifier = SVMClassifier().train(X_train, y_train, kernel, C)
    y_pred = classifier.predict(X_test)
    if not quiet:
        print('Done.')
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
