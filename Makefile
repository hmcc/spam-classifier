install: requirements.txt
	pip3 install -r $<
	
install-test: requirements-test.txt install
	pip3 install -r $<
	python3 -m nltk.downloader punkt

lexicon: install
	python3 main.py data/text/spam/ data/text/ham/ --lexicon-only --lexicon-output data/lexicon.txt

test: install-test
	python3 -m pytest tests