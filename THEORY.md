# Resolved proposition and limits

## Claim (proved here in ordinary mathematics, not machine-formalized here)
Let C be a circuit of G Hadamard/Toffoli gates on n wires, with computational-basis
input x, h Hadamards, and computational-basis output prefix p. There are two
width-at-most-three CNFs F0,F1, each with O(G+1) variables and clauses, such that

    Pr[C(x) begins with p] = (#F0 - #F1) / 2^h.

Constructing them takes polynomial time in n+G. Untouched wires are fixed by x;
check prefix consistency on them and remove them before allocating variables.
For G=0 the constant-size construction handles deterministic outcomes directly.

## Proof
A path is a string z of h branch bits, one new output bit for each H gate. All
other wire updates are deterministic. An H with input a and chosen output b
contributes (-1)^(ab)/sqrt(2); Toffoli updates t to t XOR (a AND b).
Let f(z) be the full final bit string and s(z) the XOR of all H input-output
products. By inserting computational-basis resolutions of identity, amplitude y is

    A(y)=2^(-h/2) sum_{z:f(z)=y} (-1)^s(z).

Squaring this real amplitude and summing over every completion of p gives

    2^(-h) sum_{z,z': f(z)=f(z'), f(z) starts with p} (-1)^(s(z) XOR s(z')).

Thus N0 and N1 count ordered path pairs of even and odd combined sign. The
normalizer is 2^h, NOT 2^(2h), despite 2h free path bits. Equality must be imposed
on ALL final wires, not merely the measured prefix. Untouched wires agree
by construction. Prefix consistency on untouched wires is checked classically.

Encode two deterministic Boolean path computations. Allocate the h branch
variables in each copy freely. Initial active wire bits and initial parity
are unit-pinned; unchanged wire values reuse variables (no n-by-G time grid).
For z=a AND b use clauses

    (-z OR a), (-z OR b), (z OR -a OR -b).

For z=a XOR b use

    (a OR b OR -z), (a OR -b OR z),
    (-a OR b OR z), (-a OR -b OR -z).

Enforce final equality with two binary clauses per active wire; pin the first
copy's constrained outputs and combined parity. These are full equivalences,
not implication-only SAT gadgets. Each pair of branch assignments has exactly
one assignment to every auxiliary variable, and it satisfies the CNF precisely
when it meets the required final conditions/parity. This proves parsimony and
the identity. An inconsistent untouched prefix adds the empty clause, correctly
representing zero satisfying assignments; empty clauses have width zero.

At most a<=3G wires are active. Let t=G-h. In this implementation each copy uses
a+1+3h+2t variables; the final combined parity adds one. Thus
V=2a+3+6h+4t <=12G+3. Clause count is C=4a+7+14G+r+d, where r<=a pins active prefix bits and
d is zero or one for an untouched-prefix conflict. Hence C<=29G+8, including
G=0 (which uses seven clauses without a conflict). Thus the raw encoding is
O(G+1) even when n is huge. Literal identifiers
have O(log(G+2)) bits. Deduplicate repeated literals/clauses for canonical
set-based upstream CNF encoding; this changes no satisfying assignments.

## Conditional corollary: gate-count subexponential simulation
Assume the pinned fixed-width exact-counting theorem in SOURCES.md is valid.
Apply it with k=3 and V=O(G+1), M=O(G+1); canonical encoding has polynomial bit
length in G (the upstream unary literal encoding uses O((G+1)^2) bits).
Two count calls, O(G)-bit subtraction, and the 2^h denominator yield exact
prefix probability in poly(n+G) * 2^{o(G)} time. This is an asymptotic upper bound,
not a practical speed claim; the Python DPLL code does NOT implement that theorem.

For weak simulation, at a positive-probability prefix p compute P(p0)/P(p),
select the next bit with that exact rational conditional, and repeat. The
chain rule proves the output distribution. Zero-probability prefixes are never
visited. There are O(n) count calls. Exact integer rejection sampling from ideal
fair bits has expected polynomial overhead; it is almost surely finite, not a
fixed worst-case random-bit cap. A PRNG is only a finite reproducibility device.
One can alternatively draw exactly h ideal bits once to select a rank among
2^h outcomes and descend cumulative integer prefix masses, obtaining a fixed
h-bit sampler (not the implementation supplied here).

## Disproved shortcut
Input |00>, H on wire 1, prefix 0 on wire 0. Correct probability is 1. Matching
only prefix bits pairs the two distinct final strings as well, producing 4/2=2.
The exact counterexample is retained in results/counterexample.json. This is a
failure of a specific proposed shortcut, not a new quantum-complexity separation.

## What is and is not settled
The finite identity/parsimonious reduction is proved above and independently
checked on the frozen small cases. The complexity corollary depends on the
external counting theorem; our project does not independently verify its Lean
proof graph. Existing path-integral, gap-counting, paired-marginal, model-counting,
and sequential-sampling ideas are prior art. We claim no novelty for those
constructions, no new unconditional complexity result, no quantum advantage,
and no real-device efficacy. Extending this implementation to arbitrary complex
gates, noisy states, continuous inputs, or arbitrary measurements is out of scope.
