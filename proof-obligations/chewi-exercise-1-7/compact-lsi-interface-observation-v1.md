# Existing cutoff interface: actual elaboration observation

Coordinator observation, 2026-11-06; not a new lemma, Statement Seal,
independent source verdict or exercise admission. The independent preflight is
in `compact-lsi-extension-preflight-v1.json`; this is later, separate compiler
corroboration of an existing interface, not an amendment of that report.

At head `4f4122bce36ab38f2bb524d9fee60ad41a2f6660`, with pinned
`leanprover/lean4:v4.33.0`, the following trusted local introspection exited0:

```bash
lake env lean .astis/sog-bench/inspect_lsi_type_20261106.lean
```

Its complete probe is reproducible without any proof hole:

```lean
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianLogSobolev

open Lean Elab Command

run_cmd do
  let env ← getEnv
  for (name, info) in env.constants do
    if name.toString.endsWith ".cutoff_integral_limits" then
      logInfo m!"{name}: {info.type}"

#check AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianLogSobolev.gaussian_logSobolev_of_contDiff
#check MeasureTheory.memLp_two_iff_integrable_sq_norm
```

The elaborated existing private three-limit theorem has precisely:

- `{E : Type u}` with `NormedAddCommGroup E`, `InnerProductSpace ℝ E`,
  `CompleteSpace E`, `MeasurableSpace E`, `BorelSpace E`;
- arbitrary `(μ : Measure E)` and `(f : E → ℝ)`;
- `ContDiff ℝ 2 f`, `MemLp f 2 μ`, `MemLp (gradient f) 2 μ`, and
  `Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) μ`;
- the actual mass, `q log q` and genuine squared-gradient integral limits for
  `radialSmoothCutoff (n+1) * f`.

**No finite dimension, finite measure, probability, positivity, centering or
Gaussian assumption appears in this elaborated private interface.** The public
Gaussian consumer keeps finite dimension and its `C2` test class. Extraction
must preserve the former generic scope and the latter existing public statement.
Its private mangled identity is inspection-only, never a public proof dependency.

The pinned `memLp_two_iff_integrable_sq_norm` requires
`AEStronglyMeasurable f μ` and equates `MemLp f 2 μ` with integrability of
`fun x => norm (f x)^2`. Thus the square-root producer's Fréchet energy must
still be transported through the Riesz norm identity and genuine gradient
measurability, not asserted to be the same typed input by naming convention.

Raw SHA256 of the inspected unchanged Gaussian module:
`b8c610e7709e6bda0bc5b3e1c60798c9878b25e291a733bad29d7d908226046c`.
Raw SHA256 of the exact temporary probe above:
`4a0db8156cd2ad1119a475527dcdacbc171df22463ab78ee413a3ed0fd74d54c`.
No generated model Lean ran, no production file changed and no proof or Registry
credit follows. Exact proposed public names/signatures, source binding migration,
implementation, focused consumers and publication remain the next packet.

## Proposed types checked separately, still no proofs

The complete [two-proposition probe](compact-lsi-signatures-v1.lean.txt) has raw
SHA256 `5173d97fdf667e72d1b26d851ea7a60f97bbe276dc54a36d2341bcf608f8538d`.
The exact bytes were compiled from the temporary
`.astis/sog-bench/compact_lsi_signatures_20261106.lean`, with the same pinned
`lake env lean` command, and exited0. It contains **only `#check` propositions**,
not declared theorems, axioms, proof holes or proofs. It is retained as plain
text for reproducible interface preparation, not as a production Lean module.

The first proposed type preserves the existing generic three-limit scope. The
second checks the precise compact-`C^infinity` LSI premise and the global smooth
analytic domain described in the plan. Its imports do not include the Gaussian
LSI module, so they do not introduce the proposed reverse dependency cycle.

The initial second-type probe exited1 at the `infinity` notation because
`open scoped ContDiff` was missing. Adding that notation scope, without changing
any mathematical binder or conclusion, yielded the successful check above.
This was a parser/API preparation failure, not a false mathematical route.
These observations do not supply a Statement Seal, independent source acceptance,
implemented extraction, LSI extension, PI or exercise completion.
