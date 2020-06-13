#!/usr/bin/env python3

from typing import Dict

import toml

def data_from_file(filename: str) -> Dict:
    try:
        with open(filename, 'r') as f:
            data = toml.load(f)
    except OSError:
        message = 'file "{0}" cannot be found'.format(filename)
        raise FileNotFoundError(message) from None
    except toml.TomlDecodeError:
        message = 'file "{0}" is invalid TOML'.format(filename)
        raise ValueError(message) from None
    return data

if __name__=="__main__":
    pass

