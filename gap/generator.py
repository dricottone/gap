#!/usr/bin/env python3

from pprint import pformat
from typing import Dict,List

DEFAULT_ARG_NUM =           1     # assumed number of arguments for an option
DEFAULT_ATTACHED_VALUES =   True  # if True, parser splits attached values (i.e. --verbosity=1)
DEFAULT_DEBUG_MODE =        False # if True, parser generates with logging calls
DEFAULT_EXECUTABLE =        False # if True, parser generates with executable main procedure
DEFAULT_RAISE_ON_OVERFULL = True  # if True, parser complains about flags with attached values (i.e. --quiet=true)

def update_no_collide(
    d1: Dict,
    d2: Dict,
) -> Dict:
    """Update d1 with the keys and values in d2, and raise KeyError instead of
    overwriting a key.
    """
    for key, val in d2.items():
        if key in d1.keys():
            message = "cannot overwrite key '{0}'".format(key)
            raise KeyError(message) from None
        d1[key] = val
    return d1

def indent(
    number: int,
    lines: List[str],
) -> List[str]:
    if number > 0:
        buffer = []
        for line in lines:
            buffer.append(("\t" * number) + line)
        return buffer
    else:
        return lines

class Options(object):
    def __init__(
        self,
        options: Dict[str, 'Option'] = {},
    ) -> None:
        self.options = options
        self._attached_values = DEFAULT_ATTACHED_VALUES
        self._debug_mode = DEFAULT_DEBUG_MODE
        self._executable = DEFAULT_EXECUTABLE

    def __len__(self):
        return len(self.options)

    def __str__(self):
        return pformat(self._as_dict())

    def __eq__(self, other):
        if not isinstance(other, Options):
            return NotImplemented
        elif len(self) != len(other):
            return False
        for key in self.options.keys():
            if key not in other.options.keys():
                return False
            elif self.options[key] != other.options[key]:
                return False
        return True

    def _as_dict(self):
        return {name: opt._as_dict() for name, opt in self.options.items()}

    @classmethod
    def _from_dict(
        cls,
        data: Dict[str,Dict],
        *,
        expand_alternatives: bool = False,
    ) -> 'Options':
        options = cls(
            {name: Option._from_dict(name,option_data)
                for name, option_data in data.items()}
        )
        if expand_alternatives:
            options.expand_alternatives()
        return options

    @classmethod
    def _from_list_object(
        cls,
        data: List['Option'],
        *,
        expand_alternatives: bool = False,
    ) -> 'Options':
        options = cls(
            {option.name: option for option in data}
        )
        if expand_alternatives:
            options.expand_alternatives()
        return options

    def expand_alternatives(self) -> None:
        orig_options = [key for key in self.options.keys()]
        for name in orig_options:
            new_options: Dict[str, 'Option'] = {}
            for alt in self.options[name]._alternatives:
                new_options[alt] = self.options[name].make_alternate(alt)
            self.options = update_no_collide(self.options, new_options)

    def attached_values(
        self,
        on: bool,
    ) -> None:
        self._attached_values = on
        for name in self.options.keys():
            self.options[name]._attached_values = on

    def raise_on_overfull(
        self,
        on: bool,
    ) -> None:
        for name in self.options.keys():
            self.options[name]._raise_on_overfull = on

    def executable(
        self,
        on: bool,
    ) -> None:
        self._executable = on

    def debug_mode(
        self,
        on: bool,
    ) -> None:
        self._debug_mode = on

    def build_syntax(self):
        # Accessible Variables
        # ====================
        # option          parsed option name
        # pattern         pattern for option names ('(?:a|b|c)?=.*')
        # attached_value  if a value came attached to an argument ('--a=b'),
        #                   then it is stored here
        # config          dictionary of options -> values, where value is...
        #                   Optional[bool] if flag option,
        #                   Optional[str] if singleton option,
        #                   Optional[List[str]] if multi-value option, or
        #                   Optional[List[str]] if range of values option
        # positional      list of positional arguments
        # consuming       name of option that the next argument *must* be
        #                   stored into
        # needing         number of arguments that *must* be stored into the
        #                   consuming option
        # wanting         number of arguments that will be stored into the
        #                   consuming option, unless '--' is received

        # build regex and body of parser syntax by looping over options
        flag_single, flag_double = [], []
        body = []
        for option in self.options.values():
            if len(option.name) == 1:
                flag_single.append(option.name)
            else:
                flag_double.append(option.name)
            body.extend(indent(3, option.build_syntax()))
        body[0] = body[0].replace("elif", "if", 1)
        pattern = r"(?:"
        pattern += r"-(?:" + '|'.join(flag_single) + r")"
        pattern += r"|"
        pattern += r"--(?:" + '|'.join(flag_double) + r")"
        pattern += r")"
        if self._attached_values:
            pattern += r"(?:=.*)?"
        pattern += r"$"

        # (mostly) static head/tail
        head = [
            """#!/usr/bin/env python3\n""",
            """import re\n""",
            """def main(arguments):""",
            """\tconfig=dict()""",
            """\tpositional=[]""",
            """\tpattern=re.compile(r"{0}")""".format(pattern),
            """\tconsuming,needing,wanting=None,0,0""",
        ]
        if self._attached_values: head.extend([
            """\tattached_value=None""",
        ])
        if self._debug_mode: head.extend([
            """\tdef log(*values): pass\n""",
            """\tif "--debug-gap-behavior" in arguments:""",
            """\t\tdef log(*values): print(*values)""",
        ])
        head.extend([
            """\twhile len(arguments) and arguments[0]!="--":""",
        ])
        if self._debug_mode: head.extend([
            """\t\tif arguments[0]=="--debug-gap-behavior":""",
            """\t\t\targuments.pop(0)""",
            """\t\t\tcontinue""",
            """\t\tlog(f'processing {arguments[0]}...')""",
        ])
        head.extend([
            """\t\tif consuming is not None:""",
        ])
        if self._debug_mode: head.extend([
            """\t\t\tlog(f'option {consuming} is consuming')""",
        ])
        head.extend([
            """\t\t\tif config[consuming] is None:""",
            """\t\t\t\tconfig[consuming]=arguments.pop(0)""",
        ])
        if self._debug_mode: head.extend([
            """\t\t\t\tlog(f'option {consuming} = {config[consuming]}')""",
        ])
        head.extend([
            """\t\t\telse:""",
            """\t\t\t\tconfig[consuming].append(arguments.pop(0))""",
        ])
        if self._debug_mode: head.extend([
            """\t\t\t\tlog(f'option {consuming} = {config[consuming]}')""",
        ])
        head.extend([
            """\t\t\tneeding-=1""",
            """\t\t\twanting-=1""",
            """\t\t\tif wanting==0:""",
        ])
        if self._debug_mode: head.extend([
            """\t\t\t\tlog(f'option {consuming} is no longer consuming')""",
        ])
        head.extend([
            """\t\t\t\tconsuming,needing,wanting=None,0,0""",
            """\t\telif pattern.match(arguments[0]):""",
        ])
        if self._debug_mode: head.extend([
            """\t\t\tlog(f'{arguments[0]} matched an option')""",
        ])
        head.extend([
            """\t\t\toption = arguments.pop(0).lstrip('-')""",
        ])
        if self._attached_values: head.extend([
            """\t\t\tif '=' in option:""",
        ])
        if self._attached_values and self._debug_mode: head.extend([
            """\t\t\t\tlog(f'{option} has an attached value')""",
        ])
        if self._attached_values: head.extend([
            """\t\t\t\toption,attached_value=option.split('=',1)""",
        ])
        if self._debug_mode: head.extend([
            """\t\t\tlog(f'{option} is an option')""",
        ])

        tail = [
            """\t\telse:""",
            """\t\t\tpositional.append(arguments.pop(0))""",
            """\tif needing>0:""",
            """\t\tmessage=(""",
            """\t\t\tf'unexpected end while parsing "{consuming}"'""",
            """\t\t\tf' (expected {needing} values)'""",
            """\t\t)""",
            """\t\traise ValueError(message) from None""",
            """\tfor argument in arguments[1:]:""",
        ]
        if self._debug_mode: tail.extend([
            """\t\tif argument=="--debug-gap-behavior":""",
            """\t\t\tcontinue""",
        ])
        tail.extend([
            """\t\tpositional.append(argument)""",
            """\treturn config,positional\n""",
        ])
        if self._executable: tail.extend([
            """if __name__=="__main__":""",
            """\timport sys""",
            """\tcfg,pos = main(sys.argv[1:])""",
            """\tcfg = {k:v for k,v in cfg.items() if v is not None}""",
            """\tif len(cfg):""",
            """\t\tprint("Options:")""",
            """\t\tfor k,v in cfg.items():""",
            """\t\t\tprint(f"{k:20} = {v}")""",
            """\tif len(pos):""",
            """\t\tprint("Positional arguments:", ", ".join(pos))\n""",
        ])

        # combine and return
        whole = head + body + tail
        return '\n'.join(whole)

class Option(object):
    def __init__(
        self,
        name: str,
        *,
        alternatives: List[str] = [],
        canon_name: str = "",
        minimum: int = DEFAULT_ARG_NUM,
        maximum: int = DEFAULT_ARG_NUM,
    ) -> None:
        # core attributes
        self.name = name
        self.canon_name = name
        if canon_name != "":
            self.canon_name = canon_name
        self.min = minimum
        self.max = maximum

        # check min and max
        if self.min > self.max:
            message = (
                "expected maximum greater than minimum (got {0} and {1})"
            ).format(self.min, self.max)
            raise ValueError(message) from None

        # hidden attributes
        self._alternatives = alternatives
        self._raise_on_overfull = DEFAULT_RAISE_ON_OVERFULL
        self._attached_values = DEFAULT_ATTACHED_VALUES

    def __eq__(self, other):
        if not isinstance(other, Option):
            print("  -> ???")
            return NotImplemented
        elif self.canon_name != other.canon_name:
            print("  -> 'canon_name' differs in one")
            return False
        elif self.min != other.min:
            print("  -> 'min' differs in one")
            return False
        elif self.max != other.max:
            print("  -> 'max' differs in one")
            return False
        return True

    def _as_dict(self):
        return {
            "name": self.name,
            "canon_name": self.canon_name,
            "minimum": self.min,
            "maximum": self.max,
        }

    @classmethod
    def _from_dict(cls, name, data):
        option = cls(
            name,
            alternatives=data.get("alternatives", []),
            canon_name=name,
            minimum=data.get("minimum", DEFAULT_ARG_NUM),
            maximum=data.get("maximum", DEFAULT_ARG_NUM),
        )
        if "number" in data.keys():
            option.max = data["number"]
            option.min = data["number"]
        return option

    def make_alternate(
        self,
        name: str,
    ) -> 'Option':
        return Option(
            name,
            canon_name=self.canon_name,
            minimum=self.min,
            maximum=self.max,
        )

    def build_syntax(self) -> List[str]:
        buffer = ['elif option=="{0}":'.format(self.name)]
        if self.min == self.max == 0:
            buffer.extend(indent(1, self._build_syntax_flag()))
        elif self.min == self.max == 1:
            buffer.extend(indent(1, self._build_syntax_singleton()))
        elif self.min == 0 and self.max == 1:
            buffer.extend(indent(1, self._build_syntax_optional_singleton()))
        elif self.min <= self.max:
            buffer.extend(indent(1, self._build_syntax_multivalue()))
        else:
            message = (
                "cannot parse option '{0}' with {1} to {2} values"
            ).format(self.name, self.min, self.max)
            raise ValueError(message) from None
        return buffer

    def _build_syntax_flag(self) -> List[str]:
        #Generate syntax to consume a flag (Optional[bool])
        cnn = self.canon_name
        if self._raise_on_overfull and self._attached_values:
            return [
                """if attached_value is not None:""",
                """\tmessage=(""",
                """\t\t'unexpected value while parsing "{0}"'""".format(cnn),
                """\t\t' (expected 0 values)'""",
                """\t)""",
                """\traise ValueError(message) from None""",
                """config["{0}"]=True""".format(cnn),
            ]
        else:
            return [
                    """config["{0}"]=True""".format(self.canon_name),
            ]

    def _build_syntax_singleton(self) -> List[str]:
        #Generate syntax to consume an option (Optional[str])
        cnn = self.canon_name
        if self._attached_values:
            return [
                """if attached_value is not None:""",
                """\tconfig["{0}"]=attached_value""".format(cnn),
                """\tattached_value=None""",
                """\tconsuming,needing,wanting=None,0,0""",
                """else:""",
                """\tconfig["{0}"]=None""".format(cnn),
                """\tconsuming,needing,wanting="{0}",1,1""".format(cnn),
            ]
        else:
            return [
                """config["{0}"]=None""".format(cnn),
                """consuming,needing,wanting="{0}",1,1""".format(cnn),
            ]

    def _build_syntax_optional_singleton(self) -> List[str]:
        #Generate syntax to consume a 0 or 1 value option (Optional[List[str]])
        cnn = self.canon_name
        if self._attached_values:
            return [
                """if attached_value is not None:""",
                """\tconfig["{0}"]=[attached_value]""".format(cnn),
                """\tconsuming,needing,wanting=None,0,0""",
                """\tattached_value=None""",
                """else:""",
                """\tconfig["{0}"]=[]""".format(cnn),
                """\tconsuming,needing,wanting="{0}",1,1""".format(cnn),
            ]
        else:
            return [
                """config["{0}"]=[]""".format(cnn),
                """consuming,needing,wanting="{0}",1,1""".format(cnn),
            ]


    def _build_syntax_multivalue(self) -> List[str]:
        #Generate syntax to consume a multi-value option (Optional[List[str]])
        cnn = self.canon_name
        etc = (cnn, self.min-1, self.max-1, )
        if self._attached_values:
            return [
                """if attached_value is not None:""",
                """\tconfig["{0}"]=[attached_value]""".format(cnn),
                """\tconsuming,needing,wanting="{0}",{1},{2}""".format(*etc),
                """\tattached_value=None""",
                """else:""",
                """\tconfig["{0}"]=[]""".format(cnn),
                """\tconsuming,needing,wanting="{0}",{1},{2}""".format(*etc),
            ]
        else:
            return [
                    """config["{0}"]=[]""".format(cnn),
                    """consuming,needing,wanting="{0}",{1},{2}""".format(*etc),
            ]

def test_expand_alternatives():
    a = Option("a", minimum=0, maximum=1, alternatives=["ab", "abc"])
    ab = Option("ab", canon_name="a", minimum=0, maximum=1)
    abc = Option("abc", canon_name="a", minimum=0, maximum=1)
    a._alternatives = ["ab", "abc"]

    x = Option("x", minimum=2)
    y = Option("y", minimum=3)
    z = Option("z", minimum=4)

    compacted = Options({"a": a, "x": x, "y": y, "z": z})
    expanded = Options({"a": a, "ab": ab, "abc": abc, "x": x, "y": y, "z": z})

    compacted.expand_alternatives()

    #print(compacted)
    #print(expanded)
    assert compacted == expanded

def test_expand_alternatives_bad():
    a = Option("a", minimum=0, maximum=1, alternatives=["ab", "abc"])
    ab = Option("ab", canon_name="a", minimum=0, maximum=1)

    x = Option("x", minimum=2)
    y = Option("y", minimum=3)
    z = Option("z", minimum=4)

    options = Options({"a": a, "ab": ab, "x": x, "y": y, "z": z})

    try:
        options.expand_alternatives()
        raise AssertionFailure
    except KeyError:
        pass

def test_build_syntax_no_attached_values():
    a = Option("alpha", minimum=0, maximum=0, alternatives=['a'])
    b = Option("beta", alternatives=['b'])
    g = Option("gamma", minimum=0, alternatives=['y'])
    d = Option("delta", minimum=1, maximum=4, alternatives=['d'])
    options = Options({"alpha": a, "beta": b, "gamma": g, "delta": d})
    options.expand_alternatives()
    options.attached_values(False)
    print(options.build_syntax())

def test_build_syntax_executable():
    a = Option("alpha", minimum=0, maximum=0, alternatives=['a'])
    b = Option("beta", alternatives=['b'])
    g = Option("gamma", minimum=0, alternatives=['y'])
    d = Option("delta", minimum=1, maximum=4, alternatives=['d'])
    options = Options({"alpha": a, "beta": b, "gamma": g, "delta": d})
    options.expand_alternatives()
    options.executable(True)
    print(options.build_syntax())

def test_build_syntax_executable_debug_mode():
    a = Option("alpha", minimum=0, maximum=0, alternatives=['a'])
    b = Option("beta", alternatives=['b'])
    g = Option("gamma", minimum=0, alternatives=['y'])
    d = Option("delta", minimum=1, maximum=4, alternatives=['d'])
    options = Options({"alpha": a, "beta": b, "gamma": g, "delta": d})
    options.expand_alternatives()
    options.executable(True)
    options.debug_mode(True)
    print(options.build_syntax())

#if __name__=="__main__":
    #test_expand_alternatives()
    #test_expand_alternatives_bad()
    #test_build_syntax()
    #test_build_syntax_no_attached_values()
    #test_build_syntax_executable()
    #test_build_syntax_executable_debug_mode()

