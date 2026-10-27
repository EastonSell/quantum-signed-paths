# Reporting clarifications after the frozen run
2026-10-27: The original protocol and raw results are retained unchanged.
- `attempts=240` and `successful_calls=240` in original summary mean method-case pairs. Each has an untraced timed invocation and a separately traced memory invocation: 480 solver invocations, all completed and internally equal.
- H1's nonuniform-performance clause means grouped-path versus dense simulation after BOTH get identical cone preprocessing, measured wall time. It is not a claim about all resources or asymptotic dominance.
- All benchmark circuits have h=8; this is a small controlled mechanism test, not a scaling study.
- Tracemalloc measures allocations made while tracing after the timing pass. Allocator/freelist reuse and prior warm-up can affect it. These numbers are not RSS or total retained data-structure footprint. Work proxies are separate and exact for path enumerations/state slots, upper bounds where explicitly labeled.
No algorithm, circuit, seed, endpoint, timeout or result was changed after inspection.
