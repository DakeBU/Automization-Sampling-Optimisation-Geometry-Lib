# AutoSamplingTheory.TechnicalLemmas.Probability.RandomScanHeatBath

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/RandomScanHeatBath.lean`.
- Layer: shared KERN/MEAS finite-state operational integration.
- Truth source: [canonical Frontier Cell](../../frontier-cells/ASTIS-SHARED-random-scan-heat-bath.json).
- Consumer tests: `Tests/RandomScanHeatBath.lean`.
- Source correspondence: `ASTIS-RT-20260908-RandomScanLaw` in the
  [semantic registry](../../semantic-roundtrip/registry.json).
- [Local proof dependency slice](../../../runs/20260908-samplewiki-resume/random-scan-frontier.svg).

## Mathematical statement and calculation route

Let `mu` be any probability distribution on `Fin (n+1) -> Bool`, and let `x`
have positive singleton mass. In one step, choose a site uniformly and use the
existing coordinate heat-bath kernel. Write `F_i(x)` for configurations that
agree with `x` outside site `i`. The actual random-scan kernel satisfies

\[
 P(x,\{y\})=\frac{1}{n+1}\sum_i
 \begin{cases}
 \mu(\{y\})/\mu(F_i(x)),&y_j=x_j\text{ for every }j\ne i,\\
 0,&\text{otherwise}.
 \end{cases}
\]

This is one integration result: the definition and Markov instance support
this operational law and are not counted as additional substantive leaves.
The law sums over *all* selected sites. In particular, self-transition can
receive contributions from more than one site.

## Why this step is valid

Evaluate the existing finite mixture using its public evaluation theorem.
For each selected site, singleton inclusion gives
`0 < mu{x} <= mu(F_i(x)) <= 1`. Hence the already verified positive-fiber
conditional-law theorem applies without an added fiber-positivity premise.
Evaluate normalized restriction on `{y}`. The numerator is `mu{y}` when the
retained coordinates match and zero otherwise. Mathlib's `succAbove` enumerates
exactly the nonselected sites; its equivalence to the displayed coordinate test
is proved pointwise. Convert the nonzero reciprocal uniform weight from
nonnegative reals to extended nonnegative reals, then factor it from the sum.

## Hidden assumptions and Lean choices

- The target is a probability measure, so every denominator is finite.
  It may vanish at forbidden ambient configurations; full-cube positivity is
  neither assumed nor needed.
- Source-admissible starts are positive atoms. No pointwise normalized-fiber
  identity is claimed at an unsupported start. The underlying kernel remains
  Markov there through the chosen regular conditional versions.
- `Fin (n+1)` makes the uniformly selected site set nonempty. It is an indexing
  representation of a finite nonempty vertex set, not a restriction to a
  particular graph or a claim about the zero-site algorithm.
- Boolean coordinates provide the measurable singleton, nonempty and Standard
  Borel instances needed by the generic shared theorem. These are the finite
  source specialization, not extra regularity of a continuous target.
- This is one update, not a deterministic sweep or a continuous-time rate.
  The interface is noncomputable and does not supply an executable conditional
  sampler or a cost bound.

## Lean proof architecture and reuse

`randomScan` reuses `KernelMixture.finiteMixture` with uniform, state-independent
weights and `CoordinateHeatBath.heatBath`. The Markov instance is the existing
normalized-mixture instance. The theorem `randomScan_apply_singleton` uses
`finiteMixture_apply`, `heatBath_eq_cond`, Mathlib's `cond_apply'`, finite-measure
sum evaluation, `measure_mono`, `Fin.succAbove_ne`, `Fin.exists_succAbove_eq`
and `ENNReal.coe_inv`. Its public module has two imports.

Existing target invariance and finite powers are exercised as downstream test
consumers. They are not new public wrappers and are not proof parents of the
singleton law. The focused tests include the two-bit uniform row
`[1/2, 1/4, 1/4, 0]`, a target with forbidden ambient states, the one-site
boundary, and a nonzero target whose null-fiber normalized formula differs from
the actual Markov kernel.

The later [actual-kernel reversibility packet](AutoSamplingTheory.TechnicalLemmas.Probability.RandomScanHeatBathReversibility.md)
consumes this transition law in its positive-atom branches. That theorem's
proof/source status is separate; it does not extend this pointwise law to null
starts or certify the entire printed source algorithm.

## Source and status boundaries

The primary operational target is Discrete Sampling, arXiv:2307.13826v4,
section 1.1 (PDF p.4) and section 1.3 (PDF p.5): positive support, uniform site
choice, selected-coordinate conditioning and the explanatory retention prose.
ASTIS exposition is a mathematical paraphrase, not a quotation. The printed
step-2 copy-index discrepancy remains separately visible in the source map and
its exact-proposal review. See the
[support and repair audit](../../../runs/20260908-samplewiki-resume/source-support-and-repair-audit.md).

The independent source comparison accepted this narrow target as
`equivalent-after-elaboration`, not the entire printed numbered algorithm.
Its evidence also distinguishes the source's positive-support symbol from the
ambient cube used in the blind reconstruction. The exact one-site probability
formula is ASTIS's expansion of the conditional-update rule, not a formula
quoted from the monograph.

Compilation, independent proof review, source-semantic acceptance, Registry
integration and remote publication are separate gates; consult their canonical
records rather than interpreting this prose as a status flag. No concrete Gibbs
density normalization, supported-state subtype kernel, reversibility,
irreducibility, aperiodicity, mixing, complexity or continuous-time invariance
is claimed by this packet.
