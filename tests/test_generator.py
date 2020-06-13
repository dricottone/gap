#!/usr/bin/env python3

import itertools
import unittest

from gap import generator

class Test_Option(unittest.TestCase):
    def test_object(self):
        a = generator.Option("alpha", minimum=0, maximum=0, alternatives=['a'])
        b = generator.Option("beta", alternatives=['b'])
        y = generator.Option("gamma", minimum=0, alternatives=['y'])
        d = generator.Option("delta", minimum=1, maximum=4, alternatives=['d'])

        self.assertEqual(a.min, 0)
        self.assertEqual(a.max, 0)
        self.assertEqual(a._alternatives, ['a'])
        self.assertEqual(a.canon_name, "alpha")

        self.assertEqual(b.min, 1)
        self.assertEqual(b.max, 1)
        self.assertEqual(b._alternatives, ['b'])
        self.assertEqual(b.canon_name, "beta")

        self.assertEqual(y.min, 0)
        self.assertEqual(y.max, 1)
        self.assertEqual(y._alternatives, ['y'])
        self.assertEqual(y.canon_name, "gamma")

        self.assertEqual(d.min, 1)
        self.assertEqual(d.max, 4)
        self.assertEqual(d._alternatives, ['d'])
        self.assertEqual(d.canon_name, "delta")

    def test_bad_object(self):
        with self.assertRaises(ValueError):
            z = generator.Option("zeta", minimum=1, maximum=0, alternatives=['z'])

class Test_Options(unittest.TestCase):
    def test_object(self):
        a = generator.Option("alpha", minimum=0, maximum=0, alternatives=['a'])
        b = generator.Option("beta", alternatives=['b'])
        y = generator.Option("gamma", minimum=0, alternatives=['y'])
        d = generator.Option("delta", minimum=1, maximum=4, alternatives=['d'])

        options = generator.Options._from_list_object([a,b,y,d])

        self.assertEqual(options.options["alpha"].min, 0)
        self.assertEqual(options.options["alpha"].max, 0)
        self.assertEqual(options.options["alpha"]._alternatives, ['a'])
        self.assertEqual(options.options["alpha"].canon_name, "alpha")

        self.assertEqual(options.options["beta"].min, 1)
        self.assertEqual(options.options["beta"].max, 1)
        self.assertEqual(options.options["beta"]._alternatives, ['b'])
        self.assertEqual(options.options["beta"].canon_name, "beta")

        self.assertEqual(options.options["gamma"].min, 0)
        self.assertEqual(options.options["gamma"].max, 1)
        self.assertEqual(options.options["gamma"]._alternatives, ['y'])
        self.assertEqual(options.options["gamma"].canon_name, "gamma")

        self.assertEqual(options.options["delta"].min, 1)
        self.assertEqual(options.options["delta"].max, 4)
        self.assertEqual(options.options["delta"]._alternatives, ['d'])
        self.assertEqual(options.options["delta"].canon_name, "delta")

    def test_expand_alternatives(self):
        a = generator.Option("alpha", minimum=0, maximum=0, alternatives=['a'])
        b = generator.Option("beta", alternatives=['b'])
        y = generator.Option("gamma", minimum=0, alternatives=['y'])
        d = generator.Option("delta", minimum=1, maximum=4, alternatives=['d'])

        options = generator.Options._from_list_object(
            [a,b,y,d],
            expand_alternatives=True,
        )

        self.assertEqual(options.options["a"].min, 0)
        self.assertEqual(options.options["a"].max, 0)
        self.assertEqual(options.options["a"].canon_name, "alpha")

        self.assertEqual(options.options["b"].min, 1)
        self.assertEqual(options.options["b"].max, 1)
        self.assertEqual(options.options["b"].canon_name, "beta")

        self.assertEqual(options.options["y"].min, 0)
        self.assertEqual(options.options["y"].max, 1)
        self.assertEqual(options.options["y"].canon_name, "gamma")

        self.assertEqual(options.options["d"].min, 1)
        self.assertEqual(options.options["d"].max, 4)
        self.assertEqual(options.options["d"].canon_name, "delta")

    def test_bad_expand_alternatives(self):
        a1 = generator.Option("a1", minimum=0, maximum=0, alternatives=['a'])
        a2 = generator.Option("a2", minimum=1, maximum=1, alternatives=['a'])

        with self.assertRaises(KeyError):
            options = generator.Options._from_list_object(
                [a1,a2],
                expand_alternatives=True,
            )

class Test_GeneratedCode(unittest.TestCase):
    def try_write(self, filename, syntax):
        try:
            with open(filename, 'w') as f:
                f.write(syntax)
        except OSError:
            self.skipTest("cannot write to file '{0}'".format(filename))
    def make_options(self):
        a = generator.Option("alpha", minimum=0, maximum=0, alternatives=['a'])
        b = generator.Option("beta", alternatives=['b'])
        y = generator.Option("gamma", minimum=0, alternatives=['y'])
        d = generator.Option("delta", minimum=1, maximum=4, alternatives=['d'])
        options = generator.Options._from_list_object(
            [a,b,y,d],
            expand_alternatives=True,
        )
        return options

    def test_generate(self):
        b = [True,False]
        for permutation in enumerate(itertools.product(b, repeat=4)):
            with self.subTest(permutation=permutation):
                options = self.make_options()
                number, settings = permutation

                options.attached_values(settings[0])
                options.raise_on_overfull(settings[1])
                options.executable(settings[2])
                options.debug_mode(settings[3])

                syntax = options.build_syntax()
                filename = "tests/generated_syntax/syntax{0}.py".format(number)
                self.try_write(filename, syntax)

if __name__ == "__main__":
    unittest.main()

