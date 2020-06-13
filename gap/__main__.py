#!/usr/bin/env python3

import sys

from . import generator
from . import cli

def help_message():
    message = (
        "Usage: gap [OPTIONS] INPUT\n"
    )
    sys.stdout.write(message)

def version_message():
    message = (
        "gap 1.0.0\n"
    )
    sys.stdout.write(message)

def usage_message():
    message = (
        "Usage: gap [OPTIONS] INPUT\n"
    )
    sys.stderr.write(message)

def format_message(input_format):
    message = (
        f'gap: Invalid input format "{input_format}"\n'
        "Use one of: toml\n"
    )
    sys.stderr.write(message)

def file_message(filename):
    message = (
        f'gap: Cannot access file "{filename}"\n'
    )
    sys.stderr.write(message)

def main():
    config, positionals = cli.main(sys.argv[1:])

    # Check for --help
    if "help" in config.keys():
        help_message()
        sys.exit(0)
    elif "version" in config.keys():
        version_message()
        sys.exit(0)

    # Check for too few arguments
    if len(positionals) == 0:
        usage_message()
        sys.exit(1)
    else:
        filename = positionals[0]

    # Check for valid format, then import corresponding parser
    if "format" in config.keys():
        input_format = config["format"]
        if input_format == "toml":
            from . import toml_parser as parser
        else:
            format_message(input_format)
            sys.exit(0)
    else:
        from . import toml_parser as parser

    # Set verbosity level
    verbose = False
    if "verbose" in config.keys():
        verbose = True
    if "quiet" in config.keys():
        verbose = False
    if "output" in config.keys():
        output_filename = config["output"]
    else:
        output_filename = None

    # Set generator options
    attached_values = generator.DEFAULT_ATTACHED_VALUES
    if "attached-values" in config.keys():
        attached_values = True
    elif "no-attached-values" in config.keys():
        attached_values = False

    debug_mode = generator.DEFAULT_ATTACHED_VALUES
    if "debug-mode" in config.keys():
        debug_mode = True
    elif "no-debug-mode" in config.keys():
        debug_mode = False

    executable = generator.DEFAULT_ATTACHED_VALUES
    if "executable" in config.keys():
        executable = True
    elif "no-executable" in config.keys():
        executable = False

    raise_on_overfull = generator.DEFAULT_ATTACHED_VALUES
    if "raise-on-overfull" in config.keys():
        raise_on_overfull = True
    elif "no-raise-on-overfull" in config.keys():
        raise_on_overfull = False

    # Parse input file and generate output
    data = parser.data_from_file(filename)
    options = generator.Options._from_dict(data, expand_alternatives=True)
    options.attached_values(attached_values)
    options.debug_mode(debug_mode)
    options.executable(executable)
    options.raise_on_overfull(raise_on_overfull)
    syntax = options.build_syntax()

    # Write/print and return
    if output_filename is not None:
        try:
            with open(output_filename, 'w') as f:
                f.write(syntax)
        except OSError:
            file_message(output_filename)
    else:
        sys.stdout.write(syntax)
    sys.exit(0)

if __name__ == "__main__":
    main()

