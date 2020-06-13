#!/usr/bin/env python3

import unittest

import tests.generated_syntax.syntax0 as syntax0
import tests.generated_syntax.syntax1 as syntax1
import tests.generated_syntax.syntax2 as syntax2
import tests.generated_syntax.syntax3 as syntax3
import tests.generated_syntax.syntax4 as syntax4
import tests.generated_syntax.syntax5 as syntax5
import tests.generated_syntax.syntax6 as syntax6
import tests.generated_syntax.syntax7 as syntax7
import tests.generated_syntax.syntax8 as syntax8
import tests.generated_syntax.syntax9 as syntax9
import tests.generated_syntax.syntax10 as syntax10
import tests.generated_syntax.syntax11 as syntax11
import tests.generated_syntax.syntax12 as syntax12
import tests.generated_syntax.syntax13 as syntax13
import tests.generated_syntax.syntax14 as syntax14
import tests.generated_syntax.syntax15 as syntax15

# itertools.product([True,False], repeat=4) ->
# True,  True,  True,  True
# True,  True,  True,  False
# True,  True,  False, True
# True,  True,  False, False
# True,  False, True,  True
# True,  False, True,  False
# True,  False, False, True
# True,  False, False, False
# False, True,  True,  True
# False, True,  True,  False
# False, True,  False, True
# False, True,  False, False
# False, False, True,  True
# False, False, True,  False
# False, False, False, True
# False, False, False, False
# Order: attached_values, raise_on_overfull, executable, debug_mode

class Test_GeneratedSyntax(unittest.TestCase):
    def read(self, filename):
        try:
            with open(filename, 'r') as f:
                return f.readlines()
        except OSError:
            self.skipTest("cannot read file '{0}'".format(filename))

    def test_attached_values(self):
        # The below tests shoudl parse apart "-b=1" and set beta to "1".
        args = ["-b=1"]
        cfg, pos = syntax0.main(args)
        self.assertEqual(pos, [])
        self.assertEqual(cfg, {"beta": "1"})

        args = ["-b=1"]
        cfg, pos = syntax1.main(args)
        self.assertEqual(pos, [])
        self.assertEqual(cfg, {"beta": "1"})

        args = ["-b=1"]
        cfg, pos = syntax2.main(args)
        self.assertEqual(pos, [])
        self.assertEqual(cfg, {"beta": "1"})

        args = ["-b=1"]
        cfg, pos = syntax3.main(args)
        self.assertEqual(pos, [])
        self.assertEqual(cfg, {"beta": "1"})

        args = ["-b=1"]
        cfg, pos = syntax4.main(args)
        self.assertEqual(pos, [])
        self.assertEqual(cfg, {"beta": "1"})

        args = ["-b=1"]
        cfg, pos = syntax5.main(args)
        self.assertEqual(pos, [])
        self.assertEqual(cfg, {"beta": "1"})

        args = ["-b=1"]
        cfg, pos = syntax6.main(args)
        self.assertEqual(pos, [])
        self.assertEqual(cfg, {"beta": "1"})

        args = ["-b=1"]
        cfg, pos = syntax7.main(args)
        self.assertEqual(pos, [])
        self.assertEqual(cfg, {"beta": "1"})

        # The below tests should set "-b=1" into positionals.
        args = ["-b=1"]
        cfg, pos = syntax8.main(args)
        self.assertEqual(pos, ["-b=1"])
        self.assertEqual(cfg, {})

        args = ["-b=1"]
        cfg, pos = syntax9.main(args)
        self.assertEqual(pos, ["-b=1"])
        self.assertEqual(cfg, {})

        args = ["-b=1"]
        cfg, pos = syntax10.main(args)
        self.assertEqual(pos, ["-b=1"])
        self.assertEqual(cfg, {})

        args = ["-b=1"]
        cfg, pos = syntax11.main(args)
        self.assertEqual(pos, ["-b=1"])
        self.assertEqual(cfg, {})

        args = ["-b=1"]
        cfg, pos = syntax12.main(args)
        self.assertEqual(pos, ["-b=1"])
        self.assertEqual(cfg, {})

        args = ["-b=1"]
        cfg, pos = syntax13.main(args)
        self.assertEqual(pos, ["-b=1"])
        self.assertEqual(cfg, {})

        args = ["-b=1"]
        cfg, pos = syntax14.main(args)
        self.assertEqual(pos, ["-b=1"])
        self.assertEqual(cfg, {})

        args = ["-b=1"]
        cfg, pos = syntax15.main(args)
        self.assertEqual(pos, ["-b=1"])
        self.assertEqual(cfg, {})

    def test_attached_values_raise_on_overfull(self):
        # The below tests should raise on finding the "=1".
        args = ["-a=1"]
        with self.assertRaises(ValueError):
            cfg, pos = syntax0.main(args)

        args = ["-a=1"]
        with self.assertRaises(ValueError):
            cfg, pos = syntax1.main(args)

        args = ["-a=1"]
        with self.assertRaises(ValueError):
            cfg, pos = syntax2.main(args)

        args = ["-a=1"]
        with self.assertRaises(ValueError):
            cfg, pos = syntax3.main(args)

        # The below tests should set alpha to True and ignore the "=1".
        args = ["-a=1"]
        cfg, pos = syntax4.main(args)
        self.assertEqual(cfg, {"alpha": True})
        self.assertEqual(pos, [])

        args = ["-a=1"]
        cfg, pos = syntax5.main(args)
        self.assertEqual(cfg, {"alpha": True})
        self.assertEqual(pos, [])

        args = ["-a=1"]
        cfg, pos = syntax6.main(args)
        self.assertEqual(cfg, {"alpha": True})
        self.assertEqual(pos, [])

        args = ["-a=1"]
        cfg, pos = syntax7.main(args)
        self.assertEqual(cfg, {"alpha": True})
        self.assertEqual(pos, [])

        # The below tests should set "-a=1" into positionals.
        # raise_on_overfull only matters for options that take 0 values but
        #   have an attached value. Therefore, this option is only effective
        #   if attached_values is also True.
        args = ["-a=1"]
        cfg, pos = syntax8.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["-a=1"])

        args = ["-a=1"]
        cfg, pos = syntax9.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["-a=1"])

        args = ["-a=1"]
        cfg, pos = syntax10.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["-a=1"])

        args = ["-a=1"]
        cfg, pos = syntax11.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["-a=1"])

        args = ["-a=1"]
        cfg, pos = syntax12.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["-a=1"])

        args = ["-a=1"]
        cfg, pos = syntax13.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["-a=1"])

        args = ["-a=1"]
        cfg, pos = syntax14.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["-a=1"])

        args = ["-a=1"]
        cfg, pos = syntax15.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["-a=1"])

    def test_executable(self):
        for fn in enumerate([
            "tests/generated_syntax/syntax0.py",
            "tests/generated_syntax/syntax1.py",
            "tests/generated_syntax/syntax2.py",
            "tests/generated_syntax/syntax3.py",
            "tests/generated_syntax/syntax4.py",
            "tests/generated_syntax/syntax5.py",
            "tests/generated_syntax/syntax6.py",
            "tests/generated_syntax/syntax7.py",
            "tests/generated_syntax/syntax8.py",
            "tests/generated_syntax/syntax9.py",
            "tests/generated_syntax/syntax10.py",
            "tests/generated_syntax/syntax11.py",
            "tests/generated_syntax/syntax12.py",
            "tests/generated_syntax/syntax13.py",
            "tests/generated_syntax/syntax14.py",
            "tests/generated_syntax/syntax15.py",
        ]):
            with self.subTest(fn=fn):
                number, filename = fn
                lines = self.read(filename)
                # These files should have a line 'if __name__=="__main__":'
                if number in (0,1,4,5,8,9,12,13,):
                    self.assertIn('if __name__=="__main__":\n', lines)

    def test_debugmode_catch_option(self):
        # The below tests should pull "--debug-gap-behavior" from the arguments
        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax0.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, [])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax2.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, [])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax4.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, [])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax6.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, [])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax8.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, [])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax10.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, [])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax12.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, [])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax14.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, [])

        # The below tests should set "--debug-gap-behavior" into positionals
        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax1.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["--debug-gap-behavior"])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax3.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["--debug-gap-behavior"])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax5.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["--debug-gap-behavior"])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax7.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["--debug-gap-behavior"])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax9.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["--debug-gap-behavior"])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax11.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["--debug-gap-behavior"])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax13.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["--debug-gap-behavior"])

        args = ["--", "--debug-gap-behavior"]
        cfg, pos = syntax15.main(args)
        self.assertEqual(cfg, {})
        self.assertEqual(pos, ["--debug-gap-behavior"])

if __name__ == "__main__":
    unittest.main()

