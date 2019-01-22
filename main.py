from argparse import ArgumentParser
from errno import EEXIST
from os import makedirs
from os.path import dirname, exists

from lib.ml import build_lexicon, extract_features, train_and_test
from lib.preprocess import tokenize


def save_lexicon(lexicon, lexicon_output=None):
    """
    Save the lexicon, if configured to do so.
    @param lexicon A list of words in the lexicon
    @param lexicon_output Full path to the file to save
    @return True if saved, False otherwise
    """
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
        return True

    return False


def build_parser():
    """
    Set up the command line arguments for the program.
    @return: ArgumentParser
    """
    parser = ArgumentParser(description='Classify spam and non-spam emails.')
    parser.add_argument('spam_dir', metavar='S', help='directory containing spam messages')
    parser.add_argument('ham_dir', metavar='H', help='directory containing non-spam messages')
    parser.add_argument('--c', dest='C', default=1.0, help='penalty to use with SVM')
    parser.add_argument('--kernel', default='linear', help='SVM kernel type e.g. linear, gaussian')
    parser.add_argument('--lexicon-word-count', dest='lexicon_word_count', default=100,
                        help='minimum word count to include in lexicon')
    parser.add_argument(
        '--lexicon-only', action='store_true', dest='lexicon_only', default=False, help='stop after building lexicon'
    )
    parser.add_argument('--lexicon-output', dest='lexicon_output', default=None, help='save lexicon to a file')
    parser.add_argument(
        '--lexicon-size', dest='lexicon_size', default=100, help='minimum word count to include in lexicon'
    )
    parser.add_argument('--test-size', dest='test_size', default=0.2, help='fraction of data to use as test set')
    return parser


def main():
    """
    Classify emails as spam and non-spam.
    """
    parser = build_parser()
    args = parser.parse_args()

    processed_emails = tokenize(args.spam_dir, args.ham_dir)
    lexicon = build_lexicon(processed_emails, args.lexicon_word_count)
    save_lexicon(lexicon, args.lexicon_output)
    if args.lexicon_only:
        return

    X = extract_features(processed_emails, lexicon)
    y = [1 if processed_email.spam else 0 for processed_email in processed_emails]

    train_and_test(X, y, args.test_size, args.kernel, args.C)


if __name__ == "__main__":
    main()
