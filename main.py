from argparse import ArgumentParser
from errno import EEXIST
from os import makedirs
from os.path import dirname, exists
from lib.features import build_lexicon, extract_features
from lib.preprocess import tokenize


def save_lexicon(lexicon, lexicon_output):
    if lexicon_output:
        if not exists(dirname(lexicon_output)):
            try:
                makedirs(dirname(lexicon_output))
            except OSError as exc:      # Guard against race condition
                if exc.errno != EEXIST:
                    raise

        with open(lexicon_output, 'w') as fp:
            for word in lexicon:
                fp.write('{}\n'.format(word))


def main():
    """
    Build a lexicon of words found in spam and non-spam emails.
    """
    parser = ArgumentParser(description='Classify spam and non-spam emails.')
    parser.add_argument('spam_dir', metavar='S', help='directory containing spam messages')
    parser.add_argument('ham_dir', metavar='H', help='directory containing non-spam messages')
    parser.add_argument('--count', dest='size', default=100, help='minimum word count to include in lexicon')
    parser.add_argument(
        '--lexicon-only', action='store_true', dest='lexicon_only', default=False, help='stop after building lexicon'
    )
    parser.add_argument('--lexicon-output', dest='lexicon_output', default=None, help='save lexicon to a file')
    parser.add_argument(
        '--lexicon-size', dest='lexicon_size', default=100, help='minimum word count to include in lexicon'
    )
    args = parser.parse_args()

    processed_emails = tokenize(args.spam_dir, args.ham_dir)
    lexicon = build_lexicon(processed_emails, args.size)
    save_lexicon(lexicon, args.lexicon_output)
    if args.lexicon_only:
        return

    features = extract_features(processed_emails, lexicon)


if __name__ == "__main__":
    main()
