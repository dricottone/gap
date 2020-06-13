#!/usr/bin/env python3

import toml

import generator

GAP_TOML = """

[format]
number = 1
alternatives = ['f']

[output]
number = 1
alternatives = ['o']

[help]
number = 0
alternatives = ['h', 'x']

[version]
number = 0
alternatives = ['V']

[verbose]
number = 0
alternatives = ['v']

[quiet]
number = 0
alternatives = ['q']

[attached-values]
number = 0

[no-attached-values]
number = 0

[debug-mode]
number = 0

[no-debug-mode]
number = 0

[executable]
number = 0

[no-executable]
number = 0

[raise-on-overfull]
number = 0

[no-raise-on-overfull]
number = 0

"""

if __name__ == "__main__":
    data = toml.loads(GAP_TOML)
    syntax = generator.Options._from_dict(data, expand_alternatives=True).build_syntax()
    print(syntax)

