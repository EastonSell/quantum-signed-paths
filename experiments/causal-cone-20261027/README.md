# Query-local signed-path experiment

Local follow-on to quantum-signed-paths `8b717e8`. **Not published.**
Established backward-lightcone pruning, not an OpenAI counting-algorithm implementation.

## Result
- All **48/48 query cases** agreed exactly across five methods: ordered path-pair counting, grouped signed paths, exact dense Q(sqrt(2)) statevector, cone-grouped, cone-dense.
- **240/240 method-case pairs** completed. Each was run twice (480 solver invocations): once untraced for time, once traced for allocation peak. No failures or timeouts; `results/failures.json` is retained.
- **2,550/2,550 exhaustive cone/dense comparisons**, plus inherited tests, passed (16 unit-test methods total).
- On all 12 spectator/local-prefix cases, retained Hadamards fell from 8 to 2, so grouped enumeration used **4 rather than 256 paths (64x fewer)**. Dense receives the same pruning, so this is not exclusive to path methods.
- All 24 full-output controls retain h=8: **no path-count reduction**. Connected/local cases retain 2,4,5,7 or 8 Hadamards.
- Cone-grouped was faster than cone-dense on 33/48 timed cases, slower on 15/48. This is a single small run, **not a statistical speed claim**; the independent rerun reverses some timing rankings.

| Family / query (12 each) | Pair ms | Grouped ms | Dense ms | Cone-grouped ms | Cone-dense ms |
|---|---:|---:|---:|---:|---:|
| Spectator / one bit | 1.5497 | 0.2870 | 0.6364 | 0.0414 | 0.0788 |
| Spectator / full | 0.5216 | 0.3863 | 0.6360 | 0.2930 | 0.6715 |
| Connected / one bit | 1.5203 | 0.5103 | 0.7687 | 0.5413 | 0.8391 |
| Connected / full | 0.6226 | 0.5153 | 0.8329 | 0.5682 | 0.5953 |

Times are medians within each group, not paired speedup estimates. Tiny inputs and timing noise preclude generalization. The grouped full-output spectator timing happens to exceed cone-grouped despite zero pruning, illustrating noise/overhead variability.

For spectator/local cases, median traced allocation peaks were pair 2864 B,
grouped 1152 B, dense 7128 B, cone-grouped 1232 B and cone-dense 2288 B.
These are warm-run Python traced allocations, **not RSS, peak total process
memory, or complete retained object footprint**. No blanket memory win claimed.
Raw per-case resource proxies, times, peaks and inputs are in `results/benchmark.jsonl`.

## Structural result
[Proof](THEORY.md): prefix probability depends only on this conservative cone.
The signed-count gap is divisible by `2^(h-h_cone)` and equals that factor times
the reduced gap. Existing CNF bounds become `12 G_cone+3` variables and
`29 G_cone+8` clauses, with classical input/prefix checks. The external counting
corollary remains **conditional** and unimplemented. This is an application of
known unitary lightcone cancellation, not a new complexity breakthrough.

A target-only Toffoli shortcut is unsafe because of phase kickback; full gate
support is retained. No arbitrary gates, noisy states or quantum hardware tested.
No comparison against optimized native simulators, tensor networks, cuQuantum,
or decision diagrams; this is deliberately a standard-library reference study.

## Reproduce
Python 3.10+ on POSIX (runner uses SIGALRM), no packages required:
```
sha256sum -c protocol.sha256
python -m unittest discover -s tests -v
python benchmark.py
```
The last command overwrites generated benchmark/summary/failure files; run a copy
for comparisons. `PROTOCOL.md` was SHA-256 frozen before implementation/results,
locally, not externally preregistered. Original failures from test-first work are
preserved in `results/*red.txt`. [Clarifications](AMENDMENTS.md).
