
PYTHON_PATH=""

install:
	$(PYTHON_PATH)pip install --user --upgrade .

install_test:
	$(PYTHON_PATH)pip install --user --upgrade ".[test]"

test:
	$(PYTHON_PATH)pytest -s --cov cache_decorator --cov-report html

build:
	$(PYTHON_PATH)python setup.py sdist

publish:
	$(PYTHON_PATH)twine upload "./dist/$$(ls ./dist | grep .tar.gz | sort | tail -n 1)"

pytest:
	rm -rfd test_cache
	pytest -s
	rm -rfd test_cache