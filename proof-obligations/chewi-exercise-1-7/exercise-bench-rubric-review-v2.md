# Exercise 1.7: independent Bench draft scoring re-review

**Disposition:** Accept both v2 drafts for bounded mathematical scoring
review. The substantive v1 scoring findings are addressed. There is no
remaining mathematical scoring blocker in these drafts. This does not
approve an executable profile, an export, a graph task, or Bench admission.

## Exact inputs

SHA-256 over raw bytes, without newline normalization:

| Input | SHA-256 |
| --- | --- |
| compact-pi-bench-draft-v2.md | 7b9d1fcf1bb85ece5327ac22581bfb50c3489df4260c23f734d275f255c31c63 |
| actual-kl-bench-draft-v2.md | 4869a923acf2e9acedaa2eb095bc448641e5e7a775c94da7c36cd0d0119515a1 |
| exercise-bench-rubric-review-v1.md | 939dc83cd5c31df0845e1185130d1a6fc7f2eafb667819d4bde8fab89002ccd9 |

The last input supplies the prior findings. No new inspection of source
pages, frozen Lean code, proof modules, or graph artifacts is claimed.

## Compact PI: accepted

Lines 46–57 specify exactly four separately reported 0/1 criteria:
integrability and centering, legitimate LSI test domain, entropy limit,
and energy limit and PI. All four are necessary for completeness.

- The first criterion expressly requires integrability of the original
  \(f\), its centered square, and the squared gradient norm. It permits
  a single argument to cover them and does not require proof by derivative
  support. It also requires a positive mass-one perturbation of the
  arbitrary test, not an assumed mean-zero input.
- The second criterion denies domain credit for applying the compact
  premise directly to a generally noncompact square root. It accepts a
  permitted extension only with its hypotheses checked. The grader key
  at lines 59–70 now gives the cutoff and the two-term gradient bound as
  well as mass and entropy convergence. Read \(\chi_R\) as a smooth
  cutoff: a merely Lipschitz cutoff is not an admissible test. The
  chain rule and the positive lower bound on \(p\) supply
  \(\nabla\sqrt p\in L^2(\mu)\); continuity of the mass normalization
  then completes the entropy passage. Spelling out these routine facts
  in an eventual standalone key would improve clarity.
- The entropy criterion accepts direct expansion of \(p\log p\) or
  compensation and requires a justified integral limit. The last
  criterion requires the genuine \(1/4\) energy factor, positive
  squared-parameter division, and the original \(C\), without a stronger
  premise. A positive-sided limit is allowed; actual-law KL and optimal
  constant equality are correctly not scored.

The prompt-only L4 remains defensible for the cutoff-domain adapter and
the distinct controlled limits. The proposed Lean L4 remains conditional
on what the pinned helper interfaces leave to the solver; the fixed
target certifies the conclusion, not use of the prose proof route.

## Actual-law KL: accepted

Lines 17–29 now define the extended-real divergence by absolute continuity
and the density-entropy integral, then name the ordinary real value
\(K_\varepsilon\) only after finiteness. This is equivalent to the RN log
integral convention for probability laws and does not assert local
normalization or integrability for the solver.

Lines 35–46 specify exactly four separately reported 0/1 criteria:
local law, finite canonical KL, quadratic coefficient, and full remainder.
All four are necessary for completeness. The first checks the measurable
representative, actual density, absolute continuity and mass one, with
no mandatory separate \(M=0\) case. The second requires the genuine
extended-real finiteness bridge, not a totalized real identity or repeated
Taylor evidence. The third requires cancellation and a controlled integral
coefficient, not just a scalar expansion. The fourth correctly requires
both sides and the zero endpoint; an implicit all-small-parameters
argument or a positive-side argument transferred explicitly to \(-f\)
counts. A bare compensated limit or an arbitrary quotient value at zero
does not get full credit.

The revised prompt-only L3 is accepted: one a.e. bound controls the local
law and one uniform remainder, with a genuine finite-KL identification.
The separate Lean L3 remains conditional on the stated producers leaving
the finite extended-real/real and full-neighborhood bridges to the solver.
Neither level is empirically calibrated.

## Profile and family boundary

Both drafts distinguish no-retrieval prompt-only prose, separately pinned
library-assisted prose, and an answer-excluded fixed-target Lean profile
with declared compiler/search tools and transitive context. Both segregate
answer-access/open-web experiments and reject restricted ATLAS material.
Their packaging boundary excludes rubric, reference and reviewer material;
only the mathematical prompt and definitions enter prompt-only prose.
For any future executable package, apply the PI draft's explicit rule
against answer copies to the KL assisted-prose profile too, and record the
exact toolchain, pinned retrieval/import closure and enforced permissions.
These are runtime packaging checks, not evidence of a defect in the
mathematical scoring or of an already enforced environment. Use fixed-target
verification for Lean, not the prose flags or the reference's exact calls.

The shared family chewi-lcs-2026-08-20-exercise-1-7 is preserved. If
released, both distinct results, their views and near-answer variants
belong to the same public-dev exposure group, never independent private
samples. The draft graph remarks remain descriptive, not evidence of
logical necessity or a replayed structural task. No draft, prior review
or canonical Bench file was modified by this re-review.
