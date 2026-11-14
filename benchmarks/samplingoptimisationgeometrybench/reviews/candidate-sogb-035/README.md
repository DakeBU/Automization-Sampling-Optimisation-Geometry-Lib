# Candidate audit: stopped work on binary paths

This is the independent mathematical/source audit of the exact two trusted
candidate proofs at `ffd1ee02652c961a0230182b2cda550dc0de005d` for the
already-public `sogb-035`. It does not alter the natural-language core,
its family, or any admitted task, calibration, or model score.

- [Anonymous compiled signatures](anonymous-input.json) → [independent
  blind reconstruction](decoder.json).
- [Frozen source-review packet](reviewer-input.json) → [distinct independent
  source review](source-review.json). The packet binds the candidate source,
  toolchain, original question, and exact blind report. The reviewer accepted
  both **mathematical candidates**, with no repair.
- [Target-design preflight](target-preflight.json) records a local prototype,
  not the final solver packet. Its proofless environment did not contain
  either answer declaration. A separate trusted assembly compiled both
  obligations without importing their completed modules. Comparing those
  environments matched all 21 selected model and target expressions.

The positive candidate gives a full-path density and the stated variance
bound for extended work; it proves a.e. convergence to an \(L^2\) density,
not a separately stated \(L^2\)-norm convergence result. The negative
candidate constructs the padded counterexample on the same path space.
These cover the mathematics of rubric items 1–3. Item 4—why neither
published sampler's TV or single-phase work bounds supply the added
likelihood/work assumptions—remains prose only. The omitted common
post-stop padding premise is unnecessary for the positive bound; the
negative witness does realize that padding.

The fixed candidate below retains **both** mathematical outcomes and keeps
the trusted reference and proof helpers separate from the solver definitions.
Editorial alignment of the exact challenge, native isolated acceptance, and
empirical difficulty are still pending. The roughly 218 MB local owner
export and the 57,138-byte prototype reference are sizing evidence only,
not an isolated verifier receipt.
The existing native exporter only accepts an admitted exact catalogue
packet. Do not relabel this prototype as admitted to force a run; a
pre-admission fixed-oracle check must preserve that public export guard.

### Reproduce the fixed candidate check

```sh
python tools/sog_bench_candidate_native.py freeze --output .astis/sogb-035-frozen
python tools/sog_bench_candidate_native.py check-local --output .astis/sogb-035-local
```

The generator checks the frozen reviewer input, exact prose core, owned Lean
sources and pinned toolchain/manifest. It extracts only the shared model and
the two full signatures for the solver; the reference proofs are not staged.
`check-local` elaborates only the owned generated challenge and reference on
the host. It checks the reference's axioms, compares 21 definition expressions
and the exact fixed theorem type in separate Lean environments, and checks
that neither completed answer is in the challenge.

The separate **Bench fixed candidate pre-admission** workflow prepares the
ordinary pinned Linux runtime and runs `verify --runtime … --output …` on a
fresh directory. The trusted preparation first builds the exact Mathlib
imports with Lake, including dependency traces that a direct Lean check
does not write; it does not make the runtime dependency mount writable.
It requires the complete reference to pass, and requires
the pinned Comparator to reject (1) a proof of only the positive conclusion,
(2) the same target name with its negative proposition replaced by `True`,
and (3) a proof hole. The receipt records each classification and expected
diagnostic. Resource failures are not proof rejections or model scores.
This candidate-only workflow accepts no external solution file and cannot
admit, score, or export the item through the public catalogue.
