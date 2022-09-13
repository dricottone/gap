#!/usr/bin/env python3

from typing import MutableMapping, Any

try:
    #3.11+
    import tomllib

    def data_from_file(filename: str) -> MutableMapping[str, Any]:
        try:
            with open(filename, 'rb') as f:
                data = tomllib.load(f)
        except OSError:
            message = 'file "{0}" cannot be found'.format(filename)
            raise FileNotFoundError(message) from None
        except tomllib.TOMLDecodeError:
            message = 'file "{0}" is invalid TOML'.format(filename)
            raise ValueError(message) from None
        return data

except:
    import toml #type: ignore

    def data_from_file(filename: str) -> MutableMapping[str, Any]: #type: ignore
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

