from split import EmailTokenizer


class TestEmailTokenizer:

    tokenizer = EmailTokenizer()

    def test_run_none(self):
        assert self.tokenizer.run(None) is None

    def test_run_blank(self):
        assert list(self.tokenizer.run('')) == []

    def test_run_valid(self):
        body = (
            '> Anyone knows how much it costs to host a web portal ?'
            '>'
            'Well, it depends on how many visitors youre expecting. This can be '
            'anywhere from less than number bucks a month to a couple of '
            'dollarnumber. You should checkout httpaddr or perhaps Amazon ecnumb '
            'if youre running something big.. '
            'To unsubscribe yourself from this mailing list, send an email to:'
            'emailaddr'
        )
        expected = (
            'anyon know how much it cost to host a web portal well it depend on how '
            'mani visitor your expect this can be anywher from less than number buck '
            'a month to a coupl of dollarnumb you should checkout httpaddr or perhap '
            'amazon ecnumb if your run someth big to unsubscrib yourself from this '
            'mail list send an email to emailaddr'
        )
        tokenized = self.tokenizer.run(body)
        assert ' '.join(list(tokenized)) == expected
