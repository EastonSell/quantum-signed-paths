# Pinned provenance (accessed 2026-10-27)

Upstream repository: https://github.com/openai/math
Pinned HEAD: `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a` (git ls-remote).

* [Scope note](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/docs/378.md):
  reports a deterministic exact counting machine, fixed k>=2, canonical CNF,
  polynomial space, formal time `(L+1)^O_k(1) 2^O_k(n(log log n)^2/sqrt(log n))`.
* [Actual theorem/proof entry](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean):
  `OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.exact_count_and_sat`,
  with `compiled_exact_count_and_sat` and `exact_count_eth`. Inspected proof bodies
  in this entry file; did NOT rebuild Lean, traverse all imports, or independently
  kernel-check the theorem. Conditional use is explicit.
* [Comparator statement](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/ComparatorChallenges/SubexponentialSAT.lean):
  ends its theorem with `by sorry`. This comparator is a specification, NOT proof
  evidence. Do not confuse it with the actual proof entry above.
* [October 25 manuscript](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf):
  scope note attributes sharper exponent `n log log n / sqrt(log n)` and, for
  fixed density M<=Dn, `n/sqrt(log n)`. These manuscript statements are not the
  stated formalized exponent. Our corollary needs only the weaker subexponential
  form, not the sharper manuscript bound. No claim to independently validate PDF.

## Prior art and novelty restraint
* Wang, Cheng, Yuan, Ji, [FeynmanDD: Quantum Circuit Analysis with Classical
  Decision Diagrams](https://arxiv.org/html/2509.08276v1), especially section 6.1:
  path-pair marginals and sequential output sampling precede this project.
* [QCMC, CAV 2024](https://doi.org/10.1007/978-3-031-65633-0_25): quantum circuit
  analysis via weighted model counting is prior art. No comparative benchmark
  or claim of priority over this work is made.

This repository's value is an inspectable exact restricted-basis implementation,
explicit parsimonious encoding/proof and gate-count accounting, frozen evidence,
and provenance qualification. It is not presented as novel underlying theory.
