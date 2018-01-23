.DEFAULT_GOAL := develop

PYTHON_VERSION=3

.PHONY: deps
deps:
	ve/bin/pip install .

.PHONY: clean-ve
clean-ve:
	rm -rf ve

.PHONY: clean
clean: clean-ve
	rm -rf src/cryptowatch.egg-info
	find . -name '*.pyc' -delete

.PHONY: ve
ve:
	# We need to assert that the Python version requested actually exists.
	# If it doesn't virtualenv will happily ignore our request.
	which python${PYTHON_VERSION}
	[ -d ve ] || virtualenv "--python=`which python${PYTHON_VERSION}`" ve

.PHONY: test
test:
	ve/bin/nose2 -s tests

.PHONY: develop
develop: ve
	ve/bin/python setup.py develop

.PHONY: lint
lint:
	flake8 --ignore=E501 src/
	pydocstyle src/
