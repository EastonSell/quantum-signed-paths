# Private fixed-randomness sampler audit
**Not published; independent re-review accepted. Not a faster simulator.** Separate from the held identity-padding update; no existing project files modified.

Implements the original audit's previously theory-only fixed-h-bit exact sampler. For a basis-input H/Toffoli circuit, a uniform rank in `[0,2^h)` is partitioned using integer prefix masses. Exactly h fair bits and n probability-oracle queries suffice. [Proof and resource caveats](THEORY.md).

Frozen exact evaluation: **720/720 cases, 3,548/3,548 ranks**, zero mismatches with an independently structured dense-state-vector inverse-CDF baseline. Exactly **10,338** logical prefix calls. All output histograms checked exactly, including zero-mass outputs. Exhaustive: 680 cases/3,200 ranks; seeded: 40 cases/348 ranks. Full denominators and rank outputs are in `results/evaluation/rows.jsonl`. No sampling-error statistic substitutes for exact checking.

**13/13 current tests; 11/11 unchanged inherited tests pass.** The original pre-review suite had 8 tests. Missing-feature TDD run retained (1 assertion failure, 7 missing-function errors). No evaluation failures. The dense baseline already has the whole distribution; this is correctness validation, not a fair performance contest or a speedup result. No parameter tuning, installs, costs, remote writes, or publication.

Reproduce with Python standard library, from this directory:
```
sha256sum -c protocol.sha256
python -m unittest -v
python evaluate.py --output results/fresh-run
```
Output directories must not already exist. The frozen protocol is local, not externally timestamped. `base_quantum.py` is unchanged parent code. The independent baseline avoids path/CNF methods but shares the inherited validator. The default prefix oracle is exponential, and exact fair-bit sampling assumes a genuine independent fair-bit source. The root project's conditional upstream theorem remains unverified.

## Review corrections
Independent review caught consumed gate iterators and uncontrolled float-oracle errors. Fixed with finite-iterable materialization and explicit exact-rational validation; correctness requires a faithful oracle. **13/13 tests now pass**, including all 3,548 bit-source strings from the unchanged grid. Full post-fix evaluation matches original rows. Original evidence/source preserved; added tests are post-hoc. [Amendment log](AMENDMENTS.md). Independent re-review accepted; see [status provenance](REVIEW-STATUS.md).
