# Makefile

SHELL := /bin/bash
.PHONY: build test publish depend publish-test

test:
	source bin/activate && python -m pytest

retest:
	while true; do \
		source bin/activate && find src/ | entr -d -c python -m pytest; \
	done; \

depend:
	source bin/activate && python -m pip install -r requirements_dev.txt

ipython:
	source bin/activate && ipython

freeze:
	source bin/activate && python -m pip freeze > requirements_dev.txt

publish:
	source bin/activate && python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

publish-test:
	source bin/activate && python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
