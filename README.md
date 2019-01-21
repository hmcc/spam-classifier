# Spam classifier

## Tools

### `extract_email_text`

Extract just the message body text from a raw email message using the builtin
Python [`email`](https://docs.python.org/3.4/library/email.html) package.

Tested with the
[SpamAssassin data set](http://spamassassin.apache.org/old/publiccorpus/).

Usage: `python tools/extract_email_text.py < <name of input file>`