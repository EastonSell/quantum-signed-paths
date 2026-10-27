# Reproduction and scope

Python standard library only, tested with Python 3.12.14. No installation needed.
Frozen test suite uses explicit finite enumeration and Python Random seed
20261027. Record your Python version when comparing seeded output across runtimes.
The exact algebraic comparisons are independent of random sampling variability.

`evaluate.py` records full model counts and unreduced `2^h` denominators in
JSONL, including zero-mass prefixes. Any exception yields a failed row and a
nonzero process exit after all rows. Oracle exceptions are propagated to each
prefix row. A process kill/hardware failure cannot be guaranteed recoverable.

Enumeration uses 680 exhaustive circuit-input pairs (85 gate strings times
8 inputs), 15 prefixes each, and 100 generated random circuit-input pairs with
all 2^(n+1)-1 prefixes. Thus 780 circuit-input pairs and 12,468 prefix comparisons.
Each prefix checks both CNF counts and an independent exact state-vector value.
The 4,096-shot sampler uses the separate path-probability implementation, not
CNF counting; the reduction supplies an interchangeable exact probability oracle.

Limits: exponential memory/time in dense state-vector and path algorithms;
recursive DPLL can exceed Python's recursion limit on large CNFs. Tests do not
establish useful performance at scale. This is not a backend for the upstream
subexponential theorem, nor an independently checked Lean development.
