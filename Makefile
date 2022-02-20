PY_COMPILE_BIN=python -m py_compile

#BUILD_BIN=python -m build
BUILD_BIN=pyproject-build

#UNITTEST_BIN=python -m unittest
UNITTEST_BIN=unittest --color

#MYPY_BIN=python -m mypy
MYPY_BIN=MYPY_CACHE_DIR=gap/__mypycache__ mypy

#PIPX_BIN=python -m pipx
PIPX_BIN=pipx

.PHONY: clean bootstrap test build unittest reinstall install uninstall

clean:
	rm -rf **/__pycache__ **/__mypycache__ **/*.pyc build *.egg-info

bootstrap:
	./gap/bootstrap.py > gap/cli.py

test:
	mkdir -p tests/generated_syntax
	touch tests/__init__.py tests/generated_syntax/__init__.py
	$(PY_COMPILE_BIN) gap/*.py
	$(UNITTEST_BIN) --working-directory . tests
	$(PY_COMPILE_BIN) tests/generated_syntax/*.py
	$(UNITTEST_BIN) tests/generated_syntax_tests.py
	$(MYPY_BIN) -p gap

# more verbose than `make test`, skips `py_compile` and `mypy`
unittest:
	mkdir -p tests/generated_syntax
	touch tests/__init__.py tests/generated_syntax/__init__.py
	$(UNITTEST_BIN) --working-directory . tests --verbose
	$(UNITTEST_BIN) tests/generated_syntax_tests.py --verbose

build:
	mkdir -p build
	$(BUILD_BIN) --wheel --no-isolation --outdir build/

reinstall: uninstall install

install:
	$(PIPX_BIN) install build/gap-1.0.2-py3-none-any.whl

uninstall:
	$(PIPX_BIN) uninstall gap

