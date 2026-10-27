# A query-local bound, not a new simulation algorithm

Let C consist of H and Toffoli gates on a computational-basis input x. For a
prefix p of length k, start with S={0,...,k-1}. Scan gates backwards. Discard a
gate if its entire support is disjoint from S; otherwise retain it and union
its support into S. Let Cc be retained gates on the final set S (sorted and
remapped), xc the restriction of x, Gc its gate count and hc its H count.
Then P_C(p)=P_Cc(p). In particular the original signed-count gap obeys

    N_even(C,p)-N_odd(C,p)
      = 2^(h-hc) [N_even(Cc,p)-N_odd(Cc,p)].

This is an exact divisibility relation for the GAP, not for the two counts
separately. It offers a check on implementation and sharper query-local bounds.

Proof: The output projector is |p><p| tensor identity, supported inside S.
In the Heisenberg expression <x|C† P C|x>, process gates in reverse order.
For a gate U disjoint from the current support, U† O U=O, so remove it.
Otherwise U† O U has support contained in the union of the old support and
the gate's wires. This inductive upper bound is exactly the algorithm. At the
end the operator is identity outside S, so the expectation in product input
x equals its expectation in xc. Reversing the retained gates reconstructs
Cc with the same prefix projector. Because prefix wires were included from
the start and are smaller than all other included wires, sorted remapping
leaves p unchanged. Apply the audited signed-pair probability identity to
both circuits and multiply by 2^h to obtain the gap relation. Empty prefix
has empty cone, no gates and probability one, as required.

Existing parsimonious encoding consequently needs at most 12Gc+3 variables
and 29Gc+8 clauses (untouched prefix wires checked classically). Conditional
on exactly the external fixed-width counting theorem described in the base
repository, the existing asymptotic corollary sharpens to
poly(n+G) * 2^{o(Gc)} for this query. This experiment does NOT implement or
validate that theorem. It proves only the elementary reduction above.

Grouped signed-path enumeration evaluates the same probability with 2^hc
paths, O(Gc*2^hc) gate visits and at most min(2^hc,2^|S|) signed-integer bins
(up to wire-key and h-bit integer costs). Dense statevector simulation of Cc
uses O(2^|S|) amplitude slots and O(Gc*2^|S|) arithmetic operations. Thus neither
algorithm uniformly dominates; large hc and small |S| favor the dense reference.
The code's conservative cone can be bigger than a minimal observable-specific
cone and can give no reduction. Both optimized methods include preprocessing
in measured costs. The pair reference has a quadratic path loop; comparing
only against it would misleadingly exaggerate the improvement.

Important failure of a more aggressive shortcut: a Toffoli whose target is
unmeasured cannot generally be discarded merely because it does not change
its controls' computational bits. Prepare control 0 in |+>, control 1 in |1>,
and target 2 in |->, apply T012 and then H0. Phase kickback flips control 0's
X eigenvalue. Removing T012 changes P(control 0=0) from 0 to 1. The unit test
retains the full cone, and the report treats this as a known quantum effect,
not a new counterexample in the literature.

Prior art: reverse lightcone cancellation is explicitly documented for marginal
probabilities by NVIDIA cuQuantum CircuitToEinsum (26.06.0 documentation),
https://docs.nvidia.com/cuda/cuquantum/26.06.0/python/generated/cuquantum.tensornet.CircuitToEinsum.html .
This implementation and bound are an auditable application of established
techniques. No priority, new unconditional complexity result, quantum advantage,
or state-of-the-art simulator performance claim is made.
