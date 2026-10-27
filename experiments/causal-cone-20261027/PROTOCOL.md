# Frozen causal-cone experiment (2026-10-27)
Base: EastonSell/quantum-signed-paths main 8b717e811b202f52e2743fcc0d2ef16ad2e28def, verified via GitHub branch API.
User authorized autonomous bounded improvement; no publication, installations or paid compute.

Hypothesis H1: exact backward support-cone pruning preserves every tested prefix probability, reduces enumerated path count on disconnected spectator families, but does not uniformly beat cone-reduced dense statevectors. Established optimization, not a new algorithm or unconditional complexity advance.

Algorithm: initialize support to prefix wires; scan gates in reverse; retain any gate whose support intersects current support and union its wires. Remap sorted surviving wires, including prefix wires; restrict basis input. Do not use target-only Toffoli pruning (quantum controls can experience phase kickback).

Frozen benchmark: n=3,5,8; seed=0,1,2,3; two families = 24 circuits. Spectators: H0,T(0,1,2),H0 then exactly six H gates on rng.randrange(1,n). Connected: eight H gates on rng.randrange(n), each followed by T on rng.sample(range(n),3). Input chosen with random.Random(20261027+seed+100*n), once per family; prefix=(0,) and full all-zero prefix =48 queries. Methods: existing ordered path-pair counter; grouped signed paths; exact Q(sqrt2) dense; cone-grouped; cone-dense. Each method's probability must agree exactly. All 240 attempts retained, including failures. 30-second per-call deadline; record errors/timeouts, never drop denominators. No timing significance claim (one measured run). Measure elapsed time and tracemalloc peak separately: timed pass untraced, memory pass traced. Peak is Python allocation peak, not RSS; dense/grouped/path work proxies reported separately, not interchangeable operation counts. Include preprocessing in cone timings/memory.

Correctness: inherited full unit suite; exhaustive n=3, input 000 and 101, all gate words length 0..3 from H0,H1,H2,T012, all 15 prefixes = 2550 comparisons against independent dense. Adversarial phase kickback and empty/invalid prefix tests. Freeze this document hash before implementation/results. Every failure preserved. No tuning based on results; amendments dated separately.

Plan: (1) write failing cone tests, observe missing behavior; implement cone; run full suite. (2) Implement frozen runner and proof, execute all methods with limits. (3) Independent review code/proof and rerun; fix only correctness/reporting issues, retaining first evidence. End with a local reviewed artifact; no push.

Prior art: NVIDIA CircuitToEinsum explicitly documents unitary reverse lightcone cancellation for marginal probabilities: https://docs.nvidia.com/cuda/cuquantum/26.06.0/python/generated/cuquantum.tensornet.CircuitToEinsum.html . This study compares simple Python references, not cuQuantum or state-of-art simulators. OpenAI counting theorem is neither implemented nor validated by this experiment.
