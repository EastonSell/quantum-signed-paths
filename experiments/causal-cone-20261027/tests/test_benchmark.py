import unittest
import importlib.util
from fractions import Fraction
class BenchmarkTests(unittest.TestCase):
    def test_grouped_and_design(self):
        self.assertIsNotNone(importlib.util.find_spec('benchmark'), 'missing benchmark module')
        import benchmark as b
        self.assertEqual(b.grouped((0,),[('H',0)],(0,)),Fraction(1,2))
        self.assertEqual(b.grouped((0,),[('H',0),('H',0)],(1,)),0)
        self.assertEqual(len(list(b.cases())),48)
        for family,seed,x,gates,prefix in b.cases():
            self.assertEqual(b.grouped(x,gates,prefix),b.dense(x,gates,prefix))
