# Spam classifier

A Python rewrite of the spam classification task in assignment 6 of Andrew Ng's
[Machine Learning course on Coursera](https://www.coursera.org/learn/machine-learning/).

## Dataset

As in the original assignment, I use the [SpamAssassin data set](http://spamassassin.apache.org/old/publiccorpus/).

I've included a small sample for illustration purposes, but in order to run the
classifier, at least one "spam" and "ham" dataset should be downloaded and
extracted to `data/raw/spam` and `data/raw/ham` respectively.

From there, use `tools/extract_email_text` to extract just the email text e.g.

```
`python tools/extract_email_text.py < data/raw/spam > data/text/spam`
```

Then evaluate with

```
make test
```

## Limitations

I wrote this to consolidate my own learning, and there's plenty more to do!
For example:

* lists are used throughout rather than generators/tuples, for simplicity
* regexes for emails, money etc are not robust (apart from the excellent
[URL regex from John Gruber](https://daringfireball.net/2010/07/improved_regex_for_matching_urls)
* unit test coverage is patchy
* the stemmer was chosen pretty much at random
* I haven't yet played around with the different SVM parameters


## Evaluation

Despite these limitations, it works surprisingly well; using the `20021010_spam` and `20030228_easy_ham_2` datasets gives:

```
              precision    recall  f1-score   support

           0       0.99      0.98      0.98       286
           1       0.95      0.96      0.95        95
```

## What's next?

I plan to use this as a basis for the
[Kaggle insincere questions classification problem](https://www.kaggle.com/c/quora-insincere-questions-classification). Future improvements will probably be made there not here.

