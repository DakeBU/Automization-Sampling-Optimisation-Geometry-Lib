# Ex72 exact seal: independent binder and meaning-definition audit v1

Recorded 2026-11-07 05:41 UTC by `/root/ex72_topology_challenge`.

Disposition: **no public-interface blocker found in the supplied exact seal;
internal semantic discharges remain pending; sourcegraph/root-closure review
not yet performed**. This is a preproof interface audit, not a source-fidelity,
Lean-truth, proof, or finalgraph verdict.

## Exact evidence binding

- Raw paper SHA-256:
  `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
- Prior independent rawfreeze:
  `raw-ex72-tv-amplification-expectations-v1.md`, SHA-256
  `ad55bb2757180544ac3fd785bc6a6eed9ecbaf0eb55a99f380b261d076562743`.
  Both its original staging path and canonical copy were hashed and match.
  Neither was edited.
- Exact seal:
  `research-wiki/paper-contributions/GaussianComplexity/tv-amplification-statement-seal.json`,
  SHA-256 `bfcbf23020eaabee326e4d60b6775a25988151c135f9e34dafc5c7df420f5e04`.
- Exact signature SHA-256:
  `cf35f0b97b3d8bd4bf1625e294476e2da56d6d8f8e451f9e4b57abd689905fbd`.
  Independently hashing the JSON `lean_signature` string matched.
- The five `exact_definition_context` file hashes matched their supplied
  values, and their supplied exact body strings were present byte-for-byte.
  That check reported hashes and body-presence Booleans, not file proofs.

The seal references an elaboration receipt. This reviewer has not opened or
independently validated that receipt, and does not infer a proof from reported
signature-only elaboration.

The source expectations were frozen before this seal was read. No proposed
sourcegraph, earlier review content, extractor private rationale, or target
proof implementation has been read. Additional background definition lookups
were limited to matrix block indexing, finite-index equivalences, Haar
normalization, and measure bind. Bounded excerpts included definition-internal
inverse-law arithmetic and, by a range overshoot, the adjacent one-line
Mathlib `bind_zero_left` proof. Those background lines were not used to infer
the author's source topology. No Ex72 implementation or proof-search API was
opened or constructed.

## Seven-slot comparison against the rawfreeze

1. **Objects.** The seal fixes full orthogonal Haar `μ`, the two sign laws
   `νpos = 2 • μ.restrict {det = 1}` and
   `νneg = 2 • μ.restrict {det = -1}`, independent same-sign product priors
   pushed through `blockPrecision κ`, the actual Gaussian constructor
   `γ A = multivariateGaussian 0 A⁻¹`, and `Mpos = Dpos.bind γ`,
   `Mneg = Dneg.bind γ`. The conclusion concerns those fixed laws' event
   discrepancy supremum. No abstract density pair or affinity scalar replaces
   them. Source-law identification still needs the internal discharges below.

2. **Domains.** Public parameters are natural `d,n` and real `κ`, with exactly
   `3 ≤ n`, `n ≤ d`, `4 ≤ κ`, preserving inclusive endpoints. No
   positive-residual premise is added. The local matrix measurable structure
   `borel _` is typing context for the finite-dimensional source model.

3. **Quantifiers.** All laws are fixed by local lets. The block index is
   `Fin (d / n)`; `k` is not free. Since `3 ≤ n` gives `n > 0`, natural
   division represents the source floor. No algorithm, transcript, `T`,
   `ε`, free common-sign variable, density witness, support event, or bound
   is quantified as an extra input.

4. **Assumptions.** The public signature has only the three source inequalities
   and pure carriers. No project-owned proposition alias or structure hides
   more premises. No probability, boundedness, nonemptiness, kernel
   measurability, density, normalization, L1, Ex71, Eq. (25), or B.7 conclusion
   is a public binder. The author's `EXCESS: []` field was not treated as
   substitute evidence for inspecting the signature.

5. **Conclusion.** The scalar side is exactly
   `1 - exp (-(real (d / n) / 8) * exp (-(10 * real n) / sqrt κ)) ≤ δ`.
   Natural division precedes the real cast. This is the selected final Ex72
   inequality with outer subtraction from one, coefficient `k/8`, exponent
   `10n/√κ`, and the nested exponential. There is no real-division replacement,
   changed constant, or specialization `n = 2T+1`.

6. **Scopes and senses.** The discrepancy set is literally
   `{z | ∃ B, MeasurableSet B ∧ z = |Mpos.real B - Mneg.real B|}`.
   Its intended TV is the source event supremum, whose density identity is
   **half** L1, not full variation. Because `Measure.real = ENNReal.toReal`
   and real `sSup` is totalized, finite probability laws and a nonempty bounded
   discrepancy set are essential internal facts. Syntax does not prove them.

7. **Constants.** No hidden asymptotic constant, parameter-dependent witness,
   oracle budget, accuracy threshold, expected-cost convention, or
   eigenbasis-family parameter appears. Dependencies are exactly the source
   dimensions, floor block count, and condition-number expression.

## Meaning-definition expansion

### Precision and block indexing

The supplied `singleBlockPrecision` body is the literal source affine matrix
with `(κ+1)/2`, `(κ-1)/4`, and `O + O.transpose`.

The block body uses a block diagonal, residual identity of size `d % n`,
zero off-diagonal blocks, and coordinate reindexing. A meaning-only lookup
confirms that `Matrix.blockDiagonal M` is indexed by `(i,j)` and uses
`M j i i'` for equal block indices, zero otherwise. The supplied coordinates
swap `(i,j)` to `(j,i)`. The finite-product equivalence sends that pair to
`i + n*j`, giving contiguous size-n blocks in the source order, followed by
the residual via the finite-sum equivalence. `Nat.div_add_mod` supplies the
total dimension.

The identity-block size `d % n` agrees with `d - (d/n)*n`. That conversion
and the empty-residual equivalence must be proved/applied at the actual-law
bridge. The body structurally includes both residual cases and embeds no TV
property in the prior.

### Haar, conditioning, Gaussian constructor, and bind

The full-Haar body invokes `Measure.haarMeasure` with the whole compact
orthogonal group as normalizing compact set. Its constructor normalizes a
Haar-content measure by its value on that set. This has the right source
construction. The proof must obtain its actual probability/invariance facts,
measurability and mass `1/2` of each determinant event, and probability of
the doubled restrictions at these exact definitions. “Existing audited”
in the seal is provenance language, not evidence replacing those applications;
no earlier reviewer conclusion was consumed.

The supplied `multivariateGaussian` maps the standard Gaussian by
`x ↦ μ + toEuclideanCLM (CFC.sqrt S) x`. Its interpretation at `S=A⁻¹`
as the source `N(0,A⁻¹)` requires actual symmetric positive-definite precision
and the covariance-square-root characterization. Total inverse and functional
calculus behavior outside the source domain cannot serve as source semantics.

The background definition of `Measure.bind` is `join (map f m)`. The proof
must validate the measurable/a.e. measurable maps required to identify the
prior pushforward and Gaussian bind with the intended averaging. A default
of a totalized constructor/map cannot supply that meaning. None of these
conditions may become a new public hypothesis.

### Real probabilities and event supremum

The exact `Measure.real` body is `(μ s).toReal`. Derive actual probability
(or equivalent finite normalization) for both M-laws before using these
values as probabilities; `∞.toReal = 0` is no semantic shortcut.

The empty measurable event supplies discrepancy zero. Actual probabilities
lie in `[0,1]`, so discrepancies lie in `[0,1]`. These internal proofs
establish nonemptiness and boundedness and permit ordinary real-supremum
reasoning. The seal expression is a suitable source target once these facts
are internally established; this audit does not mark those facts proved.

## Mandatory internal discharges and coverage

The following are obligations, not certified producer facts:

- Full Haar, sign-conditioned and product/pushforward probabilities;
  measurability at the exact definitions.
- Precision symmetry/positive definiteness, source support/domain validity,
  and Gaussian-kernel measurability at the actual prior.
- Actual averaged probability, density witnesses, common Lebesgue domination,
  RN/a.e. representative independence, L1/integrability and mass one.
- Actual Eq. (6) product law, Ex70 density factorization, block-coordinate
  reference-measure compatibility, actual Ex71, Tonelli, and both residual cases.
- Event-sup TV equals half L1, then `1 - ∫ min`, for the actual M-laws.
- Nonnegative-density `min ≤ sqrt`, integral comparison, and correct
  subtraction direction.
- Actual Ex69 and Eq. (25), with B.7's `(1/2) exp(-5n/√κ)` source ancestry;
  exact squaring, nonnegative-root/range, natural-power and exponential steps.
- Actual finite real probabilities and nonempty bounded discrepancy set,
  without any `sSup` or `toReal` bad-domain shortcut.

The single selected final inequality is an appropriate public statement
boundary. It does not erase earlier Ex72 proof components from source coverage.

The seal's short `source.anchors` array is not a complete proof inventory:
it omits, for example, `S2.Ex2` and `A2.E25`, although explanatory fields
name their meanings. This is not a requested mathematical-signature change.
The sourcegraph must explicitly inventory and connect those anchors and
their substantive proof regions.

## Pending sourcegraph challenge

No graph artifact has been supplied for this audit. Its later exact bytes
must be challenged against the independent rawfreeze without private rationale
or earlier verdicts. A B.7 import must not silently truncate the author's proof.

Either the graph covers the complete raw B.7 → B.6 / Poisson → A.1 / external
Poisson-formula ancestry and unnamed estimates, or it records an explicit
canonical source-component boundary with exact source revision/anchors,
component identity and statement semantics, actual-law/TV/domain correspondence,
consumer use, conditional discharge, and honest referenced coverage extent.

A code theorem name alone is not a source-component identity. A paragraph absent
from both the local inventory and explicitly referenced coverage cannot be
called covered. Opaque imported coverage remains an explicit unreviewed
boundary; an interface for a different law/TV normalization or one retaining
undischarged conditions cannot close this root.

Oracle/transcript indistinguishability, the main precision/accuracy application,
deterministic query cap, expected-cost adapter, and fixed-spectrum eigenbasis
route remain separate downstream boundaries.

## Background definition bindings

The following hashes bind bounded meaning lookups, not target proof evidence.
Paths are under the pinned `.lake/packages/mathlib/Mathlib/`:

- `Data/Matrix/Block.lean`:
  `c15b7cd49955438bd2334788946fe742b9a827dd1fc485e2e70ef42885d5ea9e`.
- `Logic/Equiv/Fin/Basic.lean`:
  `c3470797814c2d81c32c21bfeb6e7ce503e28231a7d38aad665931f3f377bc12`.
- `MeasureTheory/Measure/Haar/Basic.lean`:
  `ede9dfecb46e2512332b7af9307fc8276df0440ed5ad86053bc4664683dbfe4b`.
- `MeasureTheory/Measure/GiryMonad.lean`:
  `46aafd3d73deb6b50925501da46d66f9466f52b0f9c40cd2637b47160ab0857c`.

No target implementation, implementation dependency graph, proposed sourcegraph,
or earlier review conclusion decided the author's topology.
