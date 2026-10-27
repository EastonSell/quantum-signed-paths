# Pre-evaluation protocol v1
Frozen before implementation/evaluation on 2026-10-27 UTC. This is a correctness audit,
not a speed benchmark and not an implementation of the reported SAT algorithm.

Proposition to resolve: basis-input H/Toffoli circuits admit exact prefix probabilities
via a difference of two parsimonious width-at-most-three CNF counts, with O(G)
variables after untouched fixed wires are removed. See proof in THEORY.md.

Reject shortcut: matching only measured/prefix final wires is sufficient. Counterexample
H on an unmeasured wire will be retained, including wrong output.

Evaluation: enumerate every circuit of length 0..3 on 3 wires over H(0), H(1),
H(2), T(0,1;2); every 3-bit basis input; every prefix of lengths 0..3.
Compare signed path counts, CNF DPLL exact counts, and separately implemented
state-vector evolution using exact rational coefficients in Q(sqrt(2)).
All comparisons exact (no tolerance); retain every row, exception and denominator.
Additional random circuits: seed 20261027, 100 circuits, n=1..5, G=0..8,
H probability .6 (all H when n<3), random basis input, all prefixes.
Sampling: exact prefix conditional sampler, seeded finite PRNG, 4096 shots on
three Hadamards over |000>; save histogram and total variation from uniform.
No statistical efficacy claim or pass/fail from histogram. Sampling algorithm has
ideal fair-bit semantics; a seeded PRNG is only a reproducible finite demonstration.
Accept only zero exact mismatches and all unit tests passing. Any failure requires
retaining original evidence and documenting correction; do not change the test set.
