VERSION=1.0.4
SRC=$(shell find . -type f -name '*.py')

clean:
	rm -rf **/__pycache__ **/__mypycache__ **/*.pyc build *.egg-info

gap/cli.py: gap/bootstrap.py
	./gap/bootstrap.py > gap/cli.py

tests/__init__.py:
	touch tests/__init__.py

tests/generated_syntax/__init__.py: tests/generated_syntax
	mkdir -p tests/generated_syntax
	touch tests/__init__.py

test: tests/__init__.py tests/generated_syntax/__init__.py
	python -m py_compile gap/*.py
	python -m unittest discover --top-level-directory . tests
	python -m py_compile tests/generated_syntax/*.py
	python -m unittest tests/generated_syntax_tests.py
	mypy -p gap

unittest:
	python -m unittest discover --top-level-directory . tests --verbose
	python -m unittest tests/generated_syntax_tests.py --verbose

PYBUILD_FILES=pyproject.toml LICENSE.md README.md

dist/gap-$(VERSION)-py3-none-any.whl: $(SRC) gap/cli.py $(PYBUILD_FILES)
	mkdir -p dist
	pyproject-build --wheel --no-isolation

build: dist/gap-$(VERSION)-py3-none-any.whl

install: dist/gap-$(VERSION)-py3-none-any.whl
	pipx install dist/gap-$(VERSION)-py3-none-any.whl

uninstall:
	pipx uninstall gap

.PHONY: clean build test unittest install uninstall
