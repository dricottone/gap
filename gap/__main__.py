#!/usr/bin/env python3

import sys

from . import generator
from . import cli

VERSION = (1,0,1,)

def _msg(content, quiet):
    if not quiet:
        for line in content:
            sys.stdout.write(line)
            sys.stdout.write("\n")

def _err(content, quiet):
    if not quiet:
        for line in content:
            sys.stdout.write(line)
            sys.stdout.write("\n")

def _help_message():
    message = (
        "gap - Generate argument parser syntax for Python programs",
        "Usage: gap [OPTIONS] <INPUT>",
        "Options:",
        "  -f <FMT>,                define <INPUT>'s format [Default: toml]",
        "    --format <FMT>",
        "  -h, --help               print this message",
        "  -o <FILE>,E>             write parser to <FILE>, instead of STDOUT",
        "    --output <FILE>",
        "  -q,--quiet               suppress error messages",
        "  -v,--verbose             print debugging messages",
        "  -V,--version             print executable version",
        "  --no-debug-mode,         include `--debug-gap-behavior' debugging",
        "    --debug-mode             flag in parser? [Default: No]",
        "  --no-attached-values,    include handling for values attached to",
        "    --attached-values        options (i.e. -a=b)? [Default: Yes]",
        "  --no-executable,         include standalone program in generated",
        "    --executable             parser? [Default: No]",
        "  --no-raise-on-overfull,  include check for too many values given",
        "    --raise-on-overfull      to an option? [Default: Yes]",
    )
    _msg(message, False)

def _version_message():
    message = (
        "gap {0}".format(".".join(str(v) for v in VERSION)),
    )
    _msg(message, False)

def _usage_message(quiet):
    message = (
        "Usage: gap [OPTIONS] INPUT",
    )
    _err(message, quiet)

def _format_message(input_format, quiet):
    message = (
        '{0}: Invalid input format "{1}"'.format(sys.argv[0], input_format),
        'Use one of: toml',
    )
    _err(message, quiet)

def _file_message(filename, quiet):
    message = (
        '{0}: Cannot access file "{1}"\n'.format(sys.argv[0], filename),
    )
    _err(message, quiet)

def _file_format_message(filename, input_format, quiet):
    _format = {"toml": "TOML"}[input_format]
    message = (
        '{0}: File "{1}" is not a valid {2} file\n'.format(
            sys.argv[0], filename, _format,
        ),
    )
    _err(message, quiet)

def main():
    config, positionals = cli.main(sys.argv[1:])

    # Check for --help
    if "help" in config.keys():
        _help_message()
        sys.exit(0)
    elif "version" in config.keys():
        _version_message()
        sys.exit(0)

    # Set verbosity level
    verbose = False
    quiet = False
    if "verbose" in config.keys():
        verbose = True
        quiet = False
    if "quiet" in config.keys():
        verbose = False
        quiet = True
    if "output" in config.keys():
        output_filename = config["output"]
    else:
        output_filename = None

    # Check for too few arguments
    if len(positionals) == 0:
        _usage_message(quiet)
        sys.exit(1)
    else:
        filename = positionals[0]

    # Check for valid format, then import corresponding parser
    if "format" in config.keys():
        input_format = config["format"]
        if input_format == "toml":
            from . import toml_parser as parser
        else:
            _format_message(input_format, quiet)
            sys.exit(0)
    else:
        from . import toml_parser as parser

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
    try:
        data = parser.data_from_file(filename)
    except OSError:
        _file_message(filename, quiet)
        sys.exit(1)
    except ValueError: #parser-dependent exceptions are converted to ValueError
        _file_format_message(filename, input_format, quiet)
        sys.exit(1)

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
            _file_message(output_filename, quiet)
            sys.exit(1)
    else:
        sys.stdout.write(syntax)
    sys.exit(0)

if __name__ == "__main__":
    main()

