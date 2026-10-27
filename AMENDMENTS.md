# Post-evaluation changes (no revised hypotheses or test-set selection)

Original 12,468-row successful evaluation retained verbatim under
`results/original-v1/`. Protocol remains unchanged and its hash still validates.

1. Review identified that the dense state-vector oracle was outside row-level
   exception containment. An oracle exception could have aborted the run before
   recording all affected prefixes. It did not occur in the original run.
   The harness now captures oracle errors and records every affected row with
   its full unreduced denominator. Evaluation rerun uses identical frozen inputs.
2. Additional edge test showed that multiple conflicting untouched prefix bits
   inserted repeated empty clauses. Counts were correct, but raw clause count
   could scale with n even at G=0. Encode now inserts at most one empty clause,
   restoring the claimed O(G+1) raw clause bound. Failing regression retained in
   `results/edge-red.txt`. This changes no model counts.
3. Added exact truth-table uniqueness checks for AND/XOR gadgets, an exhaustive
   assignment check of the DPLL counter on tiny CNFs, and empty-register coverage.
   These are post-hoc robustness tests, not additions to the frozen experiment.

The initial TDD missing-API errors are retained in `results/tdd-red.txt`; the
initial seven-test green record is `results/tdd-green.txt`. Final suite has 11 tests.
4. Independent review corrected the explicit clause-count constant in the proof:
   actual C=4a+7+14G+r+d <=29G+8, not the initially stated smaller bound.
   This does not change O(G+1) or the implementation.

Rerun evidence: all 12,468 inputs, counts, probabilities, and denominators are
identical. Some clause-count metadata decreased due to empty-clause deduplication;
`results/rerun-equivalence.json` records the precise number and both hashes.
An initial assertion of full-row identity failed on exactly that metadata, so
full byte identity is NOT claimed.
