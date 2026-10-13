# AutoSamplingTheory.TechnicalLemmas.Probability.RandomScanHeatBathReversibility

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/RandomScanHeatBathReversibility.lean`.
- Layer: shared KERN/MEAS finite conditional-update consumer.
- Canonical packet: [Frontier Cell](../../frontier-cells/ASTIS-SHARED-random-scan-reversibility.json).
- Tests: `Tests/RandomScanHeatBathReversibility.lean`.
- Source window: [precise source audit](../../../runs/20260908-samplewiki-resume/reversibility-source-audit.md).

## Statement and calculation route

For any probability target `mu` on `Fin(n+1) -> Bool`, the **existing** uniform
random-scan kernel is reversible in Mathlib's set-integral sense. No full-support
or positive-start premise is imposed on this weighted balance assertion.

Let `F_i(x)` be the retained-coordinate fiber. For positive target atoms `x,y`,
the already proved transition law expresses their flux as

\[
 \mu(\{x\})P(x,\{y\})=
 \frac1{n+1}\sum_i
 \mathbf 1_{\{y_{-i}=x_{-i}\}}
 \frac{\mu(\{x\})\mu(\{y\})}{\mu(F_i(x))}.
\]

The matching condition is symmetric. Where it holds, `F_i(x)=F_i(y)`, so the
summand is symmetric in `x,y`. Where it fails, both summands are zero. The
countable singleton-balance bridge then reaches the actual set-lintegral
contract; the proof does not stop at a scalar formula without a consumer.

## Null atoms, representatives and assumptions

If `mu{x}=0` and `mu{y}>0`, use the already proved transition law **from y**, whose
conditional numerator at `x` is zero. The reverse flux is zero, matching the
zero-weighted forward flux. If both atoms vanish, both weighted fluxes vanish.
Thus the old positive-start formula is never applied at an unsupported input.
The selected Markov conditional versions may still be totalized at null fibers;
this theorem does not identify those individual transition laws.

Finite Boolean state space supplies countability and singleton measurability.
The target is a probability measure, the site set is nonempty, and the clock is
one uniformly selected site per update. No graph, activity, temperature,
connectivity, laziness or positive spectral gap is assumed.

## Lean architecture and source correspondence

The only new source-facing theorem is `randomScan_isReversible`. A private flux
calculation consumes `randomScan_apply_singleton` and native coordinate equality;
the generic `KernelReversibility.isReversible_of_singleton_balance` supplies
the reusable point-to-set integration step. There is no new random-scan kernel,
no second conditional law, and no new invariance/powers wrapper.

Levin–Peres second edition, §3.3.2, printed pp.42–43 / PDF pp.58–59,
equations (3.6)–(3.7), and Exercise 3.2, printed p.45 / PDF p.61, provide the
direct finite-state background. The present consumer is the Boolean
specialization, not the entire arbitrary finite-alphabet exercise. The MCMC
primary source §2.1.1, printed p.48 / PDF p.54, explains conditional-move
detailed balance and why deterministic composition is a different contract.
The exact source/Lean roundtrip is independent of proof compilation.

## Consumers and strict boundaries

Existing Mathlib `IsReversible.invariant` and ASTIS finite powers can consume
the actual kernel once its existing Markov instance is supplied. These tests
check real interface use without counting those old consequences as new leaves.
The current result is a prerequisite for finite reversible Dirichlet/spectral
analysis, not that analysis itself.

A disconnected positive support can make this reversible chain nonergodic.
In particular, the existing two-point diagonal target must not inherit the
hard-core model's irreducibility argument. No mixing bound, executable sampler,
sampling complexity, deterministic-scan reversibility or continuous-time result
is asserted. The cell and independent source audit own status; this card does
not declare Registry integration or chapter completion.
