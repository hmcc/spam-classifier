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


def build(processed_emails, size=100):
    lexicon = LexiconBuilder()
    pbar = tqdm(processed_emails)
    pbar.set_description('Building lexicon')
    for processed_email in tqdm(processed_emails):
        lexicon.add_all(processed_email.tokens)

    return lexicon.get(size)
