# Actual-law KL candidate: independent local review

Verdict: **ACCEPT the bounded local candidate; no required repairs.**
Reviewer: `agent-task:/root/actual_kl_candidate_review`.
Reviewed commit: `d54cd8871247d9cf278d9dd1c3568f63cfa6b095`.
Target: `AutoSamplingTheory.TechnicalLemmas.InformationTheory.AffinePerturbationKL.klDiv_affine_perturbation_second_order`.
This receipt is not a formal semantic round-trip, Source Seal, VERIFIED transition,
or publication approval.

| Exact Git input at the reviewed commit | Blob |
| --- | --- |
| `AutoSamplingTheory/TechnicalLemmas/InformationTheory/AffinePerturbationKL.lean` | `75b5c07b3e322ce1566cb5bdb684e85ecf1205bb` |
| `Tests/Shared/AffinePerturbationKL.lean` | `2ee02b93ff3faa9bad984b00e260c439226b88db` |
| `actual-kl-statement-v1.lean.txt` | `22815e7a475b78f21ba7fd6592e77e253048ac80` |
| `actual-kl-statement-v1.md` | `9ed29b0a3e1f70c8bfabe88df454b29398492445` |
| `actual-kl-candidate-v1.md` | `09b3b532021b835222a0587fbe263e199aa8d3ca` |
| `source-topology-review-v2.json` | `8064496bc3e965f68fb8eff23f8c18b1a48990b6` |
| `AutoSamplingTheory/TechnicalLemmas/InformationTheory/BoundedPerturbationLaw.lean` | `288674c5441f5d0b2605301039819ca9994d61e3` |
| `AutoSamplingTheory/TechnicalLemmas/InformationTheory/BoundedDensityPerturbation.lean` | `1435a4fff16d99bb6e9d0c9ce68fa1152952eb64` |
| `Tests/Shared/BoundedPerturbationLaw.lean` (also unchanged at the parent) | `212962a7cf811dcd6f3b4341d95622d245eb8a9b` |

The declaration header, excluding ` := by` and ending with LF, matches the
frozen signature byte for byte (SHA-256
`21bee5da0f009cb6bcd1c0585ba1a32ddb4739113aa45cf96179d9a467119bfa`).
Primary-source boundaries are taken from the
[independent source topology review v2](source-topology-review-v2.json):
Chewi, *Log-Concave Sampling*, August 20, 2026, Exercise 1.7 / (1.E.1),
printed p. 43 (PDF p. 55), and the explicit use in Corollary 2.1.2,
printed p. 50 (PDF p. 62), with its test class from Proposition 2.1.1
(PDF p. 61). The cached PDF hash agrees with the reviewed pin:
`8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`.

- **Actual probability and finite KL.** The measure is literally
  `μ.withDensity (fun x => ENNReal.ofReal (1 + e * f x))`, and the divergence
  is Mathlib's canonical `klDiv` in the order `(ν e) μ`. The law parent gives
  the a.e. density interval `[1/2, 3/2]` near zero (including zero), so `ofReal`
  does not clip there. Boundedness on a probability space makes `f` integrable;
  centering and unit mass give normalization. The parent identifies the a.e.
  Radon–Nikodym density and uses integrability of the compensated entropy and
  absolute continuity to prove the extended-real equality. The new proof
  obtains `< ⊤` from that equality by `ENNReal.ofReal_lt_top`, independently
  of `toReal`. Its later real rewrite uses nonnegativity of the integral.
- **Coefficient and filter.** The analytic parent proves the punctured quotient
  limit by differentiating the scalar compensated entropy and using dominated
  convergence with integrable envelope `f²`; it does not assume the expansion.
  Substituting the eventual real-KL identity gives precisely `(∫ f² dμ) / 2`.
  At zero, `withDensity_one` and `klDiv_self` prove `ν 0 = μ`, `KL = 0`,
  and hence a zero remainder. Off zero the proof divides by `e²`; at zero
  it separately proves the quotient limit on `pure 0`. `nhdsNE_sup_pure`
  joins those filters, and `isLittleO_of_tendsto` also checks the vanishing
  denominator condition. The result is little-o on `𝓝 0`, not merely on a
  punctured or right-sided neighborhood. The original reader proof's Taylor
  integral remainder and envelope are valid; its calculus route is clearly
  distinguished from Lean's differentiation and scalar bound.
- **Generality and regression.** Chewi's compact smooth centered tests are
  continuous and bounded, with strong measurability supplied by the Borel
  structure. The regression derives these facts from its test data rather
  than taking them as extra hypotheses. The generic bounded-centered theorem
  also applies to the broader bounded smooth class with compactly supported
  gradient used by Corollary 2.1.2; it never requires the observable itself
  to have compact support. The same regression derives the positive-sided KL
  quotient, without a transport premise or conclusion.
- **Canonical ownership.** The exact-tree search found no duplicate production
  theorem. The two named parents are strictly smaller: one proves law/KL
  identification, the other the compensated-integral limit. The old anonymous
  actual-KL composition in `Tests/Shared/BoundedPerturbationLaw.lean` proves
  only the punctured normalized quotient; it is not a public theorem or a
  single statement of the eventual probability and finite-KL conditions plus
  the full-neighborhood remainder. No duplicate producer or new edge into the
  compact LSI-to-PI proof is needed.

Independent checks: exact-blob review, byte comparison, scoped placeholder scan,
production reuse search, and `git diff --check` on the reviewed commit passed.
Coordinator-supplied Lean evidence (not rerun here): the focused
`lake build --quiet AutoSamplingTheory.TechnicalLemmas.InformationTheory.AffinePerturbationKL`
and `lake env lean Tests/Shared/AffinePerturbationKL.lean` passed;
`#print axioms` returned only `[propext, Classical.choice, Quot.sound]`.
The coordinator's direct-body check confirmed both parent occurrences.

Corollary 2.1.2 is an observed **source consumer** of (1.E.1), not a proved
Lean consumer or a certified transport edge. This candidate proves neither
T2-implies-PI nor the full exercise, any Fisher/energy or LSI step, or the
closed-form-domain and abstract semigroup extensions. Aggregate and publication
gates remain separate. No status, registry, Lean source, or tests were changed
by this review.
