import unittest
import quantum
from itertools import product

class ConeTests(unittest.TestCase):
    def test_implementation_exists(self):
        self.assertTrue(callable(getattr(quantum, 'cone', None)), 'missing cone implementation')
    def test_exhaustive(self):
        self.assertTrue(callable(getattr(quantum, 'cone', None)), 'missing cone implementation')
        alphabet=[('H',0),('H',1),('H',2),('T',0,1,2)]
        count=0
        for length in range(4):
            for gates in product(alphabet,repeat=length):
                for x in [(0,0,0),(1,0,1)]:
                    state=quantum.state_probabilities(x,gates)
                    for k in range(4):
                        for prefix in product((0,1),repeat=k):
                            xx,gg=quantum.cone(x,gates,prefix)
                            reduced=quantum.state_probabilities(xx,gg)
                            expected=sum(p for i,p in enumerate(state) if i>>(3-k)==sum(b<<(k-1-j) for j,b in enumerate(prefix)))
                            got=sum(p for i,p in enumerate(reduced) if i>>(len(xx)-k)==sum(b<<(k-1-j) for j,b in enumerate(prefix)))
                            self.assertEqual(expected,got,(x,gates,prefix)); count+=1
        self.assertEqual(count,2550)
    def test_spectators_empty_invalid(self):
        self.assertTrue(callable(getattr(quantum, 'cone', None)), 'missing cone implementation')
        self.assertEqual(quantum.cone((0,0),[('H',1)],(0,)),((0,),[]))
        self.assertEqual(quantum.cone((0,0),[('H',1)],()),((),[]))
        with self.assertRaises(ValueError): quantum.cone((0,),[],(0,1))
    def test_control_phase_kickback(self):
        self.assertTrue(callable(getattr(quantum, 'cone', None)), 'missing cone implementation')
        x=(0,1,1); gates=[('H',0),('H',2),('T',0,1,2),('H',0)]
        xx,gg=quantum.cone(x,gates,(0,))
        self.assertEqual(gg,gates)
        self.assertEqual(quantum.state_probabilities(xx,gg),quantum.state_probabilities(x,gates))
        self.assertEqual(sum(quantum.state_probabilities(x,gates)[:4]),0)
        self.assertEqual(sum(quantum.state_probabilities(x,[g for g in gates if g[0]!='T'])[:4]),1)
