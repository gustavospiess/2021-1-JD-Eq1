.PHONY: build test publish depend publish-test

build:
	rm dist/*
	python setup.py sdist bdist_wheel

publish:
	python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

publish-test:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test:
	python -m pytest

retest:
	while true; do \
		find src/ | entr -d -c python -m pytest; \
	done; \

depend:
	python -m pip install -r requirements_dev.txt
