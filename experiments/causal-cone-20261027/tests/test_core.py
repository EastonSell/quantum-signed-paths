import unittest
from fractions import Fraction
import quantum as q

class Tests(unittest.TestCase):
    def test_identity_and_h(self):
        self.assertEqual(q.pair_counts((0,), [], (0,)), (1,0,1))
        self.assertEqual(q.probability((0,), [('H',0)], (0,)), Fraction(1,2))
    def test_interference(self):
        self.assertEqual(q.probability((0,), [('H',0),('H',0)], (1,)),0)
    def test_cnf(self):
        for parity in (0,1):
            cnf=q.encode((0,), [('H',0),('H',0)], (1,),parity)
            counts=q.pair_counts((0,), [('H',0),('H',0)],(1,))
            self.assertEqual(cnf.count(),counts[parity])
            self.assertTrue(all(len(c)<=3 for c in cnf.clauses))
    def test_unmeasured(self):
        self.assertEqual(q.probability((0,0), [('H',1)], (0,)),1)
    def test_invalid(self):
        with self.assertRaises(ValueError): q.probability((0,0), [('T',0,0,1)], ())
    def test_sampler(self):
        import random
        self.assertEqual(q.sample((1,), [], random.Random(1)),(1,))
    def test_state_vector(self):
        self.assertEqual(q.state_probabilities((0,), [('H',0),('H',0)]),[Fraction(1),Fraction(0)])

if __name__=='__main__': unittest.main()

class EdgeTests(unittest.TestCase):
    def test_many_untouched_conflicts_one_clause(self):
        c=q.encode((0,)*100, [], (1,)*100,0)
        self.assertEqual(c.clauses.count(()),1)
        self.assertEqual(c.count(),0)
        self.assertLess(c.n,10)
    def test_gadget_unique_extensions(self):
        from itertools import product
        for op,truth in [('conjunction',lambda a,b:a&b),('xor',lambda a,b:a^b)]:
            for a,b in product((0,1),repeat=2):
                c=q.CNF(); av=c.const(a); bv=c.const(b); z=getattr(c,op)(av,bv)
                self.assertEqual(c.count(),1)
                c.pin(z,truth(a,b)); self.assertEqual(c.count(),1)
                c.pin(z,1-truth(a,b)); self.assertEqual(c.count(),0)
    def test_empty_register(self):
        self.assertEqual(q.probability((),[],()),1)
        self.assertEqual(q.state_probabilities((),[]),[1])
    def test_cnf_count_against_full_assignment_enumeration(self):
        from itertools import product
        for parity in (0,1):
            c=q.encode((0,), [('H',0)], (),parity)
            count=sum(all(any(bits[abs(lit)-1]==(lit>0) for lit in clause) for clause in c.clauses) for bits in product((0,1),repeat=c.n))
            self.assertEqual(c.count(),count)
