# Quantum signed-paths audit

An exact, reproducible H/Toffoli circuit-to-counting audit. **Not a fast simulator,
not a quantum efficacy claim, and not a novel path-counting construction.**

## Verifiable result
* Proved restricted-basis proposition: prefix probability `(N_even-N_odd)/2^h`
  from two parsimonious width<=3 CNFs; all final bits matched. [Proof](THEORY.md).
* Disproved prefix-only matching shortcut: it gives probability 2 instead of 1.
* **12,468/12,468 exact comparisons passed**, including 10,200 exhaustive cases
  and 2,268 seeded-random prefix cases. Full rows and full denominators retained.
* Independent dense state-vector arithmetic uses exact rational coefficients in
  Q(sqrt(2)), not floating-point tolerance and not the path/CNF implementation.
* Finite 4,096-shot reproducible sampling demonstration; no statistical efficacy
  inference. External theorem gives only a **conditional** asymptotic corollary.

## Run (Python 3.10+, no third-party packages)
```sh
python -m unittest discover -s tests -v
python evaluate.py
```
Evaluation overwrites generated result files; preserve a copy to compare reruns.
Inputs: basis bits and tuples `('H',wire)` / `('T',control,control,target)`;
wire 0 is the most-significant/first prefix bit. `quantum.encode(...).dimacs()`
exports ordinary CNF. All counters here are exponential reference algorithms.

```python
from quantum import probability, encode
print(probability((0,0), [('H',1)], (0,)))  # 1
print(encode((0,0), [('H',1)], (0,), 0).dimacs())
```

[Protocol](PROTOCOL.md) was SHA-256 frozen before implementation/evaluation.
[Provenance](SOURCES.md) pins upstream theorem commit, distinguishes formal
scope from manuscript improvements, and notes comparator `sorry` is NOT proof.
No Lean build was run here. [Results](results/summary.json),
[sampling](results/sampling.json), [counterexample](results/counterexample.json).

No dependency downloads, credentials, network access, or quantum hardware are
needed to reproduce this project. Publication is handled separately after review.

## Reviewed causal-cone follow-on (2026-10-27)

[Experiment and reproduction instructions](experiments/causal-cone-20261027/README.md)
apply established backward-lightcone pruning to query-local probabilities.
All 48 queries agree across five methods (240 method-case pairs); 16 tests,
2,550 exhaustive comparisons and 300 independent random cases pass. Spectator
local-prefix cases enumerate 4 rather than 256 paths; full-output controls
show no pruning. These small single-run timings do not establish a universal
speedup or implement the external counting theorem.

The experiment directory is the exact reviewed local artifact, including its
manifest, frozen protocol, original failures and independent review. Statements
inside that snapshot saying “Not published” or “no push” describe its original
local preparation; this integration publishes it after review. Protocol freezing
was local and is not externally timestamped preregistration. Original root
protocol, code and evidence are retained unchanged; run the follow-on from its
own directory to use its appended `cone` implementation.

## Reviewed bounded-randomness sampler (2026-10-27)

[Implementation, proof and exact evidence](experiments/bounded-randomness-20261027/README.md)
implement integer prefix-tree inverse-CDF sampling: exactly h independent fair
bits and n faithful exact prefix-probability queries for a basis-input H/Toffoli
circuit with h Hadamards and n wires. The default oracle remains exponential;
this is neither a faster simulator nor an implementation or validation of the
external counting theorem.

All 720 cases and 3,548 ranks match the exact dense baseline, with 10,338 logical
prefix calls and zero failures. All 13 current and 11 inherited tests pass.
Independent re-review accepted iterator/oracle-validation fixes; original code,
failures, protocol and pre-correction documentation remain preserved.

The linked directory preserves the exact 37-file staged snapshot with its
36-entry manifest. Its “not published” and “authorization pending” statements
record preparation history. The user subsequently explicitly approved public
publication of this bounded-randomness sampler, separately from identity-padding
research. No held identity-padding files or commit are included. Protocol hashing
was local, not independently timestamped preregistration.
