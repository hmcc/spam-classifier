from lib.features import extract_features_for_one


class TestFeaturesModule:

    lexicon = [
        'beautiful',    # 0
        'brown',        # 1
        'cat',          # 2
        'dog',          # 3
        'elephant',     # 4
        'flew',         # 5
        'greedy',       # 6
        'hopped',       # 7
        'jumped',       # 8
        'lazy',         # 9
        'monkey',       # 10
        'orange',       # 11
        'over',         # 12
        'pig',          # 13
        'pink',         # 14
        'quick',        # 15
        'ran',          # 16
        'skipped',      # 17
        'slow',         # 18
        'the'           # 19
    ]

    words = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']

    def test_extract_features_for_one(self):
        # expected_features is the same length as as the lexicon
        # with items set to 1 if they appear in the word list
        # "beautiful" is not, "brown" is, "cat" is not, "dog" is...
        expected_features = [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
        assert extract_features_for_one(self.words, self.lexicon) == expected_features
