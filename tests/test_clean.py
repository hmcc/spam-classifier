from clean import EmailCleaner


class TestEmailCleaner:

    cleaner = EmailCleaner()

    def test_replace_one_none(self):
        assert self.cleaner.replace_one(None, None, None) is None

    def test_replace_one_blank(self):
        assert self.cleaner.replace_one('', '', '') == ''

    def test_replace_email_addrs_valid(self):
        body = (
            'To unsubscribe yourself from this mailing list, send an email to: '
            'hello@google.com or mailto:hello@google.com.'
        )
        expected = (
            'To unsubscribe yourself from this mailing list, send an email to: '
            'emailaddr or emailaddr.'
        )
        cleaned = self.cleaner.replace(body)
        assert cleaned == expected

    def test_replace_money_valid(self):
        body = 'Please pay £1000 or $1,000.00 or €1.000,00.'
        expected = 'Please pay currencynumber or currencynumber or currencynumber.'
        cleaned = self.cleaner.replace(body)
        assert cleaned == expected

    def test_replace_urls_valid(self):
        body = (
            'Replace HTTP and HTTPS (https://www.google.com and http://www.google.com) '
            'and protocol-less URLs like www.google.com.'
        )
        expected = (
            'Replace HTTP and HTTPS (httpaddr and httpaddr) '
            'and protocol-less URLs like httpaddr.'
        )
        cleaned = self.cleaner.replace(body)
        assert cleaned == expected

    def test_strip_tags_easy(self):
        assert self.cleaner.strip_tags('<title>hello</title>') == 'hello'

    def test_strip_tags_table(self):
        body = (
            '<table>'
            '<tr><th>Name</th><th>Score</th></tr>'
            '<tr><td>Alice</td><td>80</td></tr>'
            '<tr><td>Bob</td><td>63</td></tr>'
            '<tr><td>Charlie</td><td>91</td></tr>'
            '</table>'
        )
        cleaned = self.cleaner.strip_tags(body)
        assert cleaned == 'Name Score Alice 80 Bob 63 Charlie 91'

    def test_strip_tags_twice(self):
        body = '<title>hello</title>'
        assert self.cleaner.strip_tags(self.cleaner.strip_tags(body)) == 'hello'
