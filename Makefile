install: requirements.txt
	pip3 install -r $<
	
install-test: requirements-test.txt install
	pip3 install -r $<
	python3 -m nltk.downloader punkt

lexicon: install
	python3 lexicon.py data/text/spam/ data/text/ham/

test: install-test
	python3 -m pytest tests