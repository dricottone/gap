
# generated argument parser

A package that uses external configuration files to generate a static, standalone parser module.


## To-Do

Add parsers aside from `toml`, like `json` and `configparser`.

Allow import of third-party libraries, like `toml`, to fail-just remove that format from the valid list.


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


