VERSION=1.0.3

PY_COMPILE_BIN=python -m py_compile

#BUILD_BIN=python -m build
BUILD_BIN=pyproject-build

#UNITTEST_FILE_BIN=python -m unittest
#UNITTEST_DIR_BIN=python -m unittest discover --top-level-directory .
UNITTEST_FILE_BIN=unittest --color
UNITTEST_DIR_BIN=unittest --color --working-directory .

#MYPY_BIN=python -m mypy
MYPY_BIN=MYPY_CACHE_DIR=gap/__mypycache__ mypy

#PIPX_BIN=python -m pipx
PIPX_BIN=pipx

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
	$(PY_COMPILE_BIN) gap/*.py
	$(UNITTEST_DIR_BIN) tests
	$(PY_COMPILE_BIN) tests/generated_syntax/*.py
	$(UNITTEST_FILE_BIN) tests/generated_syntax_tests.py
	$(MYPY_BIN) -p gap

.PHONY: unittest
# more verbose than `make test`, skips `py_compile` and `mypy`
unittest: $(TEST_FILES)
	$(UNITTEST_DIR_BIN) tests --verbose
	$(UNITTEST_FILE_BIN) tests/generated_syntax_tests.py --verbose

PY_FILES=gap/cli.py gap/generator.py gap/__main__.py gap/toml_parser.py

build/gap-$(VERSION)-py3-none-any.whl: build

.PHONY:
build: $(PY_FILES)
	mkdir -p build
	$(BUILD_BIN) --wheel --no-isolation --outdir build/

.PHONY: reinstall
reinstall: uninstall install

.PHONY: install
install: build/gap-$(VERSION)-py3-none-any.whl
	$(PIPX_BIN) install build/gap-$(VERSION)-py3-none-any.whl

.PHONY: uninstall
uninstall:
	$(PIPX_BIN) uninstall gap

.PHONY: rc
rc:
	docker run --interactive --tty --rm --name pytest --mount type=bind,src=$(pwd),dst=/code python:3.11-rc sh

