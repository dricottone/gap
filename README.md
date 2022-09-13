
# generated argument parser

A package that uses external configuration files to generate a static,
standalone parser module.


## Usage

To install, try:

```
pipx install git+https://git.dominic-ricottone.com/~dricottone/gap
```


## To-Do

Python 3.11 introduces a `tomllib` module. **Release 1.0.2** will continue to
work perfectly for Python 3.6 or later. **Release 1.0.3** will continue to
function perfectly as well, but the test suite will fail with Python 3.10 or
earlier due to `mypy` not having type stubs for `tomllib`. **Release 1.0.4**
will drop `toml` as a dependency and therefore drop support for Python 3.10 or
earlier.


## Workflow

Given a configuration like:

```toml
# Quickly define '--help', '-h', and '-x'
[help]
number = 0
alternatives = ['h', 'x']

# Immediately raise an error if too few values given.
[range]
number = 2

# Take variable numbers of values, only raising an error at the minimum.
# Will greedily consume arguments up to the maximum.
[files]
minimum = 1
maximum = 9
```

You could include the following in your build process:

```shell
python -m gap my-project-cli.conf > cli.py
```

Your argument parser then is accessible in Python like:

```python
import sys, cli

options, positionals = cli.main(sys.argv[1:])

if "help" in options.keys():
	print_help_message()

# It's just a built-in dict, so use all the usual methods as you please.
for file in options.get("files", []):
	read_input(file)
else:
	for argument in positionals:
		read_input(file)
```


## Licensing

This software is distributed under the GPL license.

I claim absolutely no license over any code generated *by* this software.


