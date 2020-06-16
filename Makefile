
unittest = unittest --color
#unittest = python -m unittest
unittest_discover = unittest --color --working-directory .
#unittest_discover = python -m unittest discover tests --top-level-directory . --start-directory
python = python3

clean:
	rm -rf **/__pycache__ **/*.pyc

bootstrap:
	./gap/bootstrap.py > gap/cli.py

test:
	mkdir -p tests/generated_syntax
	touch tests/__init__.py tests/generated_syntax/__init__.py
	$(python) -m py_compile gap/*.py
	$(unittest_discover) tests
	$(python) -m py_compile tests/generated_syntax/*.py
	$(unittest) tests/generated_syntax_tests.py

build:
	mkdir -p build
	mkdir -p dist
	$(python) setup.py sdist bdist_wheel

unittest:
	$(unittest_discover) tests --verbose
	$(unittest) tests/generated_syntax_tests.py --verbose

install:
	pipx install --spec . gap

uninstall:
	pipx uninstall gap

