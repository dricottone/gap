
unittest = unittest --color
unittest_discover = unittest --color --working-directory .
# If you don't have my unittest wrapper installed...
#unittest = python -m unittest
#unittest_discover = python -m unittest discover tests --top-level-directory . --start-directory

clean:
	rm -rf **/__pycache__ **/*.pyc

bootstrap:
	./gap/bootstrap.py > gap/cli.py

test:
	mkdir -p tests/generated_syntax
	touch tests/__init__.py tests/generated_syntax/__init__.py
	python -m py_compile gap/*.py
	$(unittest_discover) tests
	python -m py_compile tests/generated_syntax/*.py
	$(unittest) tests/generated_syntax_tests.py

unittest:
	$(unittest_discover) tests --verbose
	$(unittest) tests/generated_syntax_tests.py --verbose

install:
	pipx install --spec . gap

uninstall:
	pipx uninstall gap

