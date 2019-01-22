from argparse import ArgumentParser
from html.parser import HTMLParser
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from os import listdir
from os.path import basename, dirname, isfile, join
from re import compile, sub
from sys import stdin
from tqdm import tqdm


class HTMLTagStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True

    def handle_data(self, d):
        self.fed.append(d)

    def get_text(self):
        return ' '.join(self.fed)

    def reset(self):
        super().reset()
        self.fed = []


class EmailCleaner:
    tag_stripper = HTMLTagStripper()

    # With many thanks to John Gruber: https://daringfireball.net/2010/07/improved_regex_for_matching_urls
    url_regex = compile(r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))')

    replacements = {
        compile(r'(?<=[\s€$£₽¥])([0-9]+[\.,]?)*([0-9]+)\b'): 'number',
        compile(r'[€$£₽¥]'): 'currency',
        compile(r'[^\s]+@([^\s]+\.)+[^\s\.]+'): 'emailaddr',
        url_regex: 'httpaddr'
    }

    def replace_one(self, regex, replacement, text):
        return sub(regex, replacement, text) if text else text

    def replace(self, text):
        for regex, replacement in self.replacements.items():
            text = self.replace_one(regex, replacement, text)
        return text

    def strip_tags(self, text):
        if text:
            self.tag_stripper.reset()
            self.tag_stripper.feed(text)
            return self.tag_stripper.get_text()
        return text

    def run(self, text):
        text = text.lower()
        text = self.strip_tags(text)
        text = self.replace(text)
        return text


class EmailTokenizer:
    stemmer = SnowballStemmer("english")

    def run(self, text):
        tokens = self.tokenize(text)
        if tokens:
            tokens = [sub('[^A-Za-z0-9]+', '', word) for word in tokens]
            tokens = [word for word in tokens if word]
        return self.stem(tokens)

    def stem(self, tokens):
        if tokens:
            return [self.stemmer.stem(t) for t in tokens]
        return tokens

    def tokenize(self, text):
        if text:
            return word_tokenize(text)
        return text


class ProcessedEmail:
    def __init__(self, identifier, spam, tokens=tuple()):
        self.identifier = identifier
        self.spam = spam
        self.tokens = tokens


def tokenize(spam_dir, ham_dir):
    def list_files(directory):
        return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]

    cleaner = EmailCleaner()
    processed = []
    tokenizer = EmailTokenizer()
    all_files = list_files(spam_dir) + list_files(ham_dir)
    file_count = len(all_files)
    pbar = tqdm(total=file_count)
    pbar.set_description('Tokenizing emails')
    for file in all_files:
        identifier = basename(file)
        spam = dirname(file) in spam_dir
        with open(file, encoding='ISO-8859-1') as fp:
            cleaned = cleaner.replace(fp.read())
            tokens = tokenizer.run(cleaned)
            processed.append(ProcessedEmail(identifier, spam, tokens))
        pbar.update(1)

    return processed


def main():
    """
    Tokenize a single email message body, reading from stdin and printing the
    result to stdout.
    """
    body = stdin.read()
    parser = ArgumentParser(description='Classify spam and non-spam emails.')
    parser.add_argument(
        '--clean-only', action='store_true', dest='clean_only', default=False, help='stop after cleaning'
    )
    args = parser.parse_args()

    print(body)
    print('================================================================================')
    cleaned = EmailCleaner().run(body)
    if (args.clean_only):
        print(cleaned)
    else:
        tokenizer = EmailTokenizer()
        tokens = tokenizer.run(cleaned)
        print(list(tokens))


if __name__ == "__main__":
    main()
