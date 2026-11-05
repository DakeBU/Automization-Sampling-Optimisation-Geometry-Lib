# Staged model bridge: independent review requires changes

This is the next packet of the **same** Sampling-Optimisation-Geometry-Bench
Goal. It is not part of PR379/head731d98de or the accepted native08 verifier.
Do not merge or advertise the bridge as an accepted model runner yet.

## What exists

- `tools/sog_bench_lean_model.py`: optional finite Responses function-call loop
  over the existing fixed-target compiler workspace. No hosted service or host
  Lean execution fallback. Initial input is the two canonical nongold agent files.
- `tools/tests/test_sog_bench_lean_model.py`: eight trusted mocked contract tests;
  no provider calls, paid requests or submitted Lean execution.
- `benchmarks/samplingoptimisationgeometrybench/lean-runtime/MODEL.md`: proposed
  operator contract, not native/provider acceptance.
- [Immutable independent v1 review](independent-design-review.json): actual
  exact-source hashes, eight passing unit cases and five additional probes.
  Review report raw SHA256:
  `0bd2e563864bf7fa950b9a17d6ab3fcfa4c8dd1ca6bc641b968209b058ed9854`.

The reviewer requests changes. Keep this original prototype and report intact as
historical evidence if a successor is implemented; never relabel v1 as accepted.

## Required next repair

1. **M1 — canonical termination accounting.** A provider/HTTP/runtime failure
   before final currently becomes ordinary `no-final-submission` in the child
   completion and suite rollup. Stop text is insufficient. Add a separately
   reviewed canonical typed external-termination boundary, or an equivalent
   explicit accounting layer, retaining every selected target. Infrastructure
   must remain unscored and distinct from an actual model missing final. Never
   override a genuine reserved final or its result. Test the full suite rollup
   and partial/interrupted evidence, not just a single summary field.
2. **M2 — response/model identity.** Require meaningful returned model identity,
   define the requested-ID/version/alias policy, reject repeated response IDs,
   and preserve provider identity/usage before tool dispatch. Identity failure
   must remain non-admissible without replacing a genuine compiler final.
3. Clarify that the bridge does not directly append gold/challenge/configuration,
   but submitted Lean can print *readable public container data* into bounded
   compiler feedback. This is not enforced closed-book isolation. The container
   has no oracle mount; existing runtime trust assumptions remain unchanged.
4. Re-review the exact repaired source and run a new native integration fixture.
   Real provider acceptance additionally requires an authorized API/model and
   spending policy. The owner has been asked; no API key is currently configured
   and no paid run has been attempted. A technical token/call cap is not a dollar
   ceiling. Never record a scripted fixture as model performance.

Do not change the accepted engine while PR379 is in its current-head CI/merge
lane. Root is the sole writer; any successor engine/record-contract change is a
new bounded packet with its own native/review evidence. Preserve the protected
KernelReversibilityTransport drafts, old mathematical frontiers, cycles, source
reviews and all failed native evidence. Registry remains608; mathematical cores,
families, splits and all thirteen aligned targets are unchanged.
