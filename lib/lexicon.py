from argparse import ArgumentParser
from errno import EEXIST
from os import listdir, makedirs
from os.path import dirname, exists, isfile, join
from tqdm import tqdm
from clean import EmailCleaner
from split import EmailTokenizer


class LexiconBuilder():
    lexicon = {}

    def add(self, word):
        if word not in self.lexicon:
            self.lexicon[word] = 0
        self.lexicon[word] += 1

    def add_all(self, iterable):
        for word in iterable:
            self.add(word)

    def get(self, wordcount=100):
        if not wordcount:
            return list(self.lexicon.keys())
        return [k for k, v in self.lexicon.items() if v >= wordcount]


def build_lexicon(spam_dir, ham_dir, size):
    def list_files(directory):
        return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]

    cleaner = EmailCleaner()
    lexicon = LexiconBuilder()
    tokenizer = EmailTokenizer()
    all_files = list_files(spam_dir) + list_files(ham_dir)
    file_count = len(all_files)
    pbar = tqdm(total=file_count)
    for file in all_files:
        with open(file, encoding='ISO-8859-1') as fp:
            cleaned = cleaner.replace(fp.read())
            tokens = tokenizer.run(cleaned)
            lexicon.add_all(tokens)
        pbar.update(1)

    return lexicon.get(size)


def main():
    """
    Build a lexicon of words found in spam and non-spam emails.
    """
    parser = ArgumentParser(description='Build a lexicon from spam and non-spam emails.')
    parser.add_argument('spam_dir', metavar='S', help='directory containing spam messages')
    parser.add_argument('ham_dir', metavar='H', help='directory containing non-spam messages')
    parser.add_argument('--count', dest='size', default=100, help='minimum word count to include')
    parser.add_argument('--output', default='data/lexicon.txt', help='output file')
    args = parser.parse_args()
    lexicon = build_lexicon(args.spam_dir, args.ham_dir, args.size)

    if not exists(dirname(args.output)):
        try:
            makedirs(dirname(args.output))
        except OSError as exc:      # Guard against race condition
            if exc.errno != EEXIST:
                raise

    with open(args.output, 'w') as fp:
        for word in lexicon:
            fp.write('{}\n'.format(word))


if __name__ == "__main__":
    main()
