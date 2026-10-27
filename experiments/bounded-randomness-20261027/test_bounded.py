import unittest
from fractions import Fraction
import bounded as b
import base_quantum as q

class Tests(unittest.TestCase):
    def test_feature_present(self):
        self.assertTrue(callable(getattr(b,'rank_sample',None)))
        self.assertTrue(callable(getattr(b,'bit_sample',None)))
    def test_empty(self):
        self.assertEqual(b.rank_sample((),[],0),((),0))
    def test_hh(self):
        for r in range(4):
            self.assertEqual(b.rank_sample((0,),[('H',0),('H',0)],r),((0,),1))
    def test_identity(self):
        self.assertEqual(b.rank_sample((1,0),[],0),((1,0),2))
    def test_bad_rank(self):
        for r in (-1,1,0.5,True):
            with self.assertRaises(ValueError): b.rank_sample((0,),[],r)
    def test_bad_oracle(self):
        for p in (Fraction(1,3),Fraction(2),Fraction(-1)):
            with self.assertRaises(ValueError): b.rank_sample((0,),[],0,lambda *a:p)
    def test_fair_bits(self):
        bits=iter([1,0]); calls=[]
        def bit():
            calls.append(1); return next(bits)
        self.assertEqual(b.bit_sample((0,0),[('H',0),('H',1)],bit),((1,0),2))
        self.assertEqual(len(calls),2)
    def test_bad_bit(self):
        with self.assertRaises(ValueError): b.bit_sample((0,),[('H',0)],lambda:2)

class ReviewRegressionTests(unittest.TestCase):
    def test_rank_gate_iterator(self):
        self.assertEqual(b.rank_sample((0,),iter([('H',0)]),1),((1,),1))
    def test_bit_gate_iterator(self):
        calls=[]
        def bit(): calls.append(1); return 1
        self.assertEqual(b.bit_sample((0,),iter([('H',0)]),bit),((1,),1))
        self.assertEqual(calls,[1])
    def test_reject_nonexact_oracles(self):
        for value in (0.5,True,'0',None,complex(0)):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    b.rank_sample((0,),[],0,lambda *args:value)
    def test_integer_oracle(self):
        self.assertEqual(b.rank_sample((0,),[],0,lambda *args:1),((0,),1))
    def test_all_bitstrings_frozen_cases(self):
        from evaluate import cases
        for _,x,gates in cases():
            h=sum(g[0]=='H' for g in gates)
            for rank in range(1<<h):
                source=iter((rank>>i)&1 for i in range(h-1,-1,-1))
                calls=[]
                def bit(): calls.append(1); return next(source)
                self.assertEqual(b.bit_sample(x,gates,bit),b.rank_sample(x,gates,rank))
                self.assertEqual(len(calls),h)
