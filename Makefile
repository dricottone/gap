VERSION=1.0.3

#INSTALLER=pip
INSTALLER=pipx

# If using system build module
#BUILDER=python -m build
# If using module installed by pipx
BUILDER=pyproject-build

#UNITTEST_FILE_BIN=python -m unittest
#UNITTEST_DIR_BIN=python -m unittest discover --top-level-directory .
UNITTEST_FILE_BIN=unittest --color
UNITTEST_DIR_BIN=unittest --color --working-directory .

#MYPY_BIN=python -m mypy
MYPY_BIN=MYPY_CACHE_DIR=gap/__mypycache__ mypy

.PHONY: clean
clean:
	rm -rf **/__pycache__ **/__mypycache__ **/*.pyc build *.egg-info

gap/cli.py: gap/bootstrap.py
	./gap/bootstrap.py > gap/cli.py

tests/__init__.py:
	touch tests/__init__.py

tests/generated_syntax:
	mkdir -p tests/generated_syntax

tests/generated_syntax/__init__.py: tests/generated_syntax
	touch tests/__init__.py

TEST_FILES=tests/__init__.py tests/generated_syntax tests/generated_syntax/__init__.py

.PHONY: test
test: $(TEST_FILES)
	python -m py_compile gap/*.py
	$(UNITTEST_DIR_BIN) tests
	python -m py_compile tests/generated_syntax/*.py
	$(UNITTEST_FILE_BIN) tests/generated_syntax_tests.py
	$(MYPY_BIN) -p gap

.PHONY: unittest
# more verbose than `make test`, skips `py_compile` and `mypy`
unittest: $(TEST_FILES)
	$(UNITTEST_DIR_BIN) tests --verbose
	$(UNITTEST_FILE_BIN) tests/generated_syntax_tests.py --verbose

PY_FILES=gap/cli.py gap/generator.py gap/__main__.py gap/toml_parser.py
PYBUILD_FILES=pyproject.toml LICENSE.md README.md

dist:
	mkdir -p dist

dist/gap-$(VERSION)-py3-none-any.whl: dist $(PY_FILES) $(PYBUILD_FILES)
	$(BUILDER) --wheel --no-isolation --outdir build/

build: dist/gap-$(VERSION)-py3-none-any.whl

install: dist/gap-$(VERSION)-py3-none-any.whl
	$(INSTALLER) install dist/gap-$(VERSION)-py3-none-any.whl

uninstall:
	$(INSTALLER) uninstall gap

reinstall:
	make uninstall
	make install

.PHONY: clean build install uninstall reinstall
