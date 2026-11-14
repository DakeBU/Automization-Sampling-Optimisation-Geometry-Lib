# Raw-source reading freeze — ri_src_5ab9

Phase: `RAW_SOURCE_READING_FROZEN`; no Lean comparison or fidelity verdict has begun.
Reviewer role: independent source reviewer, distinct from the root formalizer,
source-topology extractor, topology challenger, and future blind decoder.
This file records source meaning and review obligations, not a mathematical proof,
source-topology judgment, proof approval, or publication/status grant.

The pinned source is `.astis/huanjian-resume-20261103/2610.20492v1.html`,
951991 UTF-8 bytes, SHA-256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
The assignment's adjacent `html951991B` was interpreted as filename `.html`
followed by its byte count after the literal concatenated filename did not exist.

## Frozen scope and anchors

The visible section C.2 is represented by raw HTML IDs `A3.SS2`, not `C2`.
The selected source material is:

- Lemma 4.4 standing input paragraph, `S4.Thmtheorem4.p1.1`.
- The exact midpoint angle grid, `S4.E11` and its C.2 recall `A3.SS2.p4.m2`.
- C.2 first paragraph `A3.SS2.p1`, particularly definitions `A3.Ex85` and
  the independence sentence in `A3.SS2.p1.2`.
- The cutoff definitions only, `A3.SS2.p10.m1` and `A3.SS2.p10.m2`.
- The first sentence `A3.SS2.p12.1` and actual matrix formula `A3.Ex107`.

Exact raw UTF-8 byte, Unicode-character and LF-line/column locators, extract
hashes, and source-derived readable transcriptions are in `source_locators.json`.
All byte/character intervals are zero-based and half-open. Lines are one-based,
columns zero-based. Raw extracts preserve the original bytes, with no newline
normalization. Readable transcriptions are convenience views; raw extracts and
the pinned original decide any ambiguity.

The narrow intended public subclaim concerns full joint independence of the
actual coordinate rows of the independent Gaussian columns on their canonical
product experiment. The real private consumer is measurability and full joint
independence of the actual truncated matrices displayed in C.2. These two roles
must remain distinct in later review.

## Seven source-meaning slots

1. **Objects.** There are `r=q+1` independent Gaussian column vectors
   `g_1,...,g_r` in real `d`-space. For each `i=1,...,d`, the row vector is
   exactly `gamma_i=((g_1)_i,...,(g_r)_i)^T`, an element of real `r`-space.
   It is an actual regrouping of those columns, not a newly sampled vector or
   merely an object with a matching marginal law. The source's C.2 sentence says
   these rows are independent `N(0,I_r)` vectors. The deterministic vector is
   `t_i=(1,sqrt(2) cos(theta_i),...,sqrt(2) cos(q theta_i))^T`, also of length `r`.

2. **Domains.** The intended source typing is natural `q,d`, with `q>=0` and
   strict `2q+1<d`. The Lemma 4.4 text literally says `q>=0`; integer typing is
   supplied by query/polynomial degrees and vector indexing, rather than an
   extra regularity assumption. In this scope `d>=2` and `r>=1`; `q=0` remains
   included. Source row indices are one-based `1<=i<=d`; column indices are
   `1<=a<=r`; the coordinates of `t_i` are frequencies `j=0,...,q`, with
   coordinate zero equal to `1`. Any zero-based finite-index encoding must
   retain the source shift in the angle grid.

3. **Quantifiers.** For each such source parameter choice, the Gaussian columns
   are jointly independent with their stated laws, and the whole finite family
   of rows is jointly independent. The row assertion is stronger than pairwise
   independence and stronger than a list of marginal laws. Its intended
   meaning is independence of the sigma-fields/random vectors, equivalently
   factorization for every family of Borel test sets, not only selected events
   or coordinate pairs. The analogous whole-family meaning applies to the
   displayed truncated matrices.

4. **Assumptions.** The source provides independent standard `d`-Gaussian
   columns, the natural parameter scope, and the fixed deterministic grid.
   The source provides neither row independence as an additional input nor
   measurability/independence of the matrices as an additional input: the latter
   are consumer obligations. No event, tail bound, moment bound, concentration
   conclusion, or theorem-shaped gate may be substituted as a premise for
   this subclaim. The condition on `tau_{d,q}` belongs to Lemma 4.4's later main
   conclusion; it is not used to restrict this row/matrix independence claim.

5. **Conclusion.** Public intended subclaim: the actual rows `gamma_i` are
   jointly independent on their same canonical column experiment. Private
   intended consumer: each actual `Y_i` is measurable as a matrix-valued random
   variable and the entire family is jointly independent, where
   `Y_i=d^(-1) (gamma_i gamma_i^T tensor t_i t_i^T) 1_{R_i<=L}`,
   `R_i=||gamma_i||^2`, and `L=2r+3 log(1000d)`.
   The source explicitly asserts row standard-normal laws and explicitly calls
   these matrices independent; it does not explicitly state their
   measurability. No mean, bias, norm, variance, or concentration conclusion is
   part of this frozen intended conclusion.

6. **Scopes and senses.** All row vectors and matrices are functions of the
   same sample of columns. For the assigned narrow canonical realization, the
   experiment is the finite product of `r` copies of standard Gaussian measure
   on real `d`-space, with `g_a` the actual coordinate projections and `gamma_i`
   their actual evaluation/regrouping map. The source does not itself name this
   probability-space carrier: it is a source-compatible realization specified
   by the assignment, not a newly discovered literal source premise. No
   transfer to an arbitrary enlarged ambient probability space is reviewed
   here. The matrices take values in real square matrices of dimension `r^2`,
   with Kronecker coordinate order inherited from `gamma_i tensor t_i`.
   The deterministic map may vary with `i` through `t_i`; independence of
   `Y_i` is the claim, and identical distribution of `Y_i` is not asserted.
   The truncation is local to row `i`; it is not conditioning on a common
   event and not multiplication by a simultaneous all-row cutoff.

7. **Constants and endpoints.** The exact grid is
   `theta_i=(i-1/2) pi/d`, not `i pi/d`, a random angle, or an arbitrary grid.
   The frequency coefficient is exactly `sqrt(2)` for `j=1,...,q`, while the
   zero-frequency coordinate is exactly `1`. The normalization is exactly
   `d^(-1)`. The squared row norm, not its unsquared norm, is compared with
   `L=2(q+1)+3 log(1000d)`. The cutoff is closed: equality `R_i=L` keeps the
   displayed outer-product term; `R_i>L` gives the zero matrix. The same
   deterministic `L` is used for every row. Its dependencies are only `q,d`
   through `r=q+1` and the displayed logarithm. Standard Gaussian means
   covariance identity, with no extra scaling parameter. The constants
   `C`, `tau`, `kappa`, and probabilities in the larger main bound are outside
   this subclaim.

## Explicit source claims versus implicit bridges

**Literally supplied:** column independence and `N(0,I_d)` laws in the standing
lemma; `r=q+1`; exact actual-row and deterministic-vector formulas; full row
independence and `N(0,I_r)` laws; exact midpoint angle grid; exact definitions
of `L`, `R_i`, and `Y_i`; the words “independent truncated matrices.”

**Implicit/source-compatible obligations, not added public hypotheses:**

- Realization of the stated Gaussian experiment by actual coordinate
  projections of the canonical finite column product.
- Identification of each actual row map with the displayed source coordinates
  on that same experiment; coordinate regrouping must respect the full joint
  experiment, and cannot be justified from marginal row laws alone.
- Measurability of the column/row evaluations in the finite-dimensional Borel
  spaces and measurability of the actual matrix map, including its local closed
  cutoff. The source is using these as random vectors/matrices without writing
  separate measurability sentences.
- Passing the actual whole-family row independence to the actual row-local
  matrix functions. The deterministic `t_i` is allowed to vary with `i`.

These are recorded as bridge obligations only. This phase supplies no formal
proof or implementation-derived route for them, and makes no judgment that a
future sealed type or code has discharged them.

## Outside the review boundary

All mean/bias calculations, boundedness/norm estimates, moments/variance,
tail bounds, matrix Bernstein/concentration, the main uniform Krylov bound,
constants for that main result, and arbitrary ambient-space transfer remain
outside scope. The surrounding `B` construction, spectral `lambda_i/Lambda`
material sharing equation (11), and the rest of Lemma 4.4 are context, not
independent claims reviewed here. Reading their raw snippets creates no source
coverage or proof credit for them.

## Exposure barrier at freeze

Only the explicit assignment, the six required instruction/protocol files, the
pinned raw source and source-derived selections have been used. The exposure
manifest records incidental out-of-scope raw-source snippets and the repaired
transcription bug. No Lean signatures/types, implementation source, current
lessons, prior graphs, prior audits/verdicts, decoder reconstruction, publication
packet, or compiler receipts have been inspected. No shared ledger, control
plane, Git state, registry, graph, goal or status was mutated. All created files
are inside the assigned private review directory.

Stop after this freeze. The next authorized input is the separately supplied
exact sealed types, followed only later by current code and a fresh
anti-anchored source-review packet after independent blind decoding.
