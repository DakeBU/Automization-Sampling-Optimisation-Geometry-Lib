# Independent whole-code-only report: shared PSD integral and uncentered R9

**Code-reading result: no blocking mathematical, binder, definition, or
application mismatch found in the supplied shared producer and actual
uncentered R9 consumer.** This is based on the complete owned ASTIS sources and
the precise upstream ranges recorded here. It is not compilation acceptance,
a kernel/axiom audit, final source fidelity, publication admission, or Goal
credit. No compiler result was read or produced. The centered and weighted
variance target T is not implemented in this packet and receives no credit.

## Exact input boundary

The initial manifest raw digest is
`a732bbf0514472df4ddbc24daf24bc8a2aa6059ff3f8eca46cb98d0f767d203b`.
The explicitly requested provider supplements have manifest raw digests
`735abd1fc9f4400007091c2be2aa2b3eabbd320781f7812ffc66fcfcfe0b05a7`
and `43321f990f6c3c7a29fb6e609fc981ecc034351624479dbc6422877fc752f60d`.
All 29 supplied full-file snapshots were copied and their complete byte
counts/digests checked. Hashing/copying is not claimed as semantic reading.

I read all **950 lines of all 9 ASTIS modules**, including their imports,
scopes, comments, complete statements, and all owned proof/tactic code. Mathlib
reading was by the exact ranges listed in `actual-read-ranges.json`, plus
explicitly recorded single-line locator results. It was not a full reading of
every Mathlib snapshot or its transitive import closure. No original library
file outside the supplied snapshots, implementation predecessor, compiler
receipt, other reviewer's verdict, source graph, canonical audit, lesson,
repair, or exposition was opened.

The capture records old HEAD `441d54ee96a6182374d2df3bf4d2fb096d5b7e14`
with uncommitted new mathematical bytes. This report binds those exact
snapshots, not a claim that HEAD contains or compiled the new mathematics.
Earlier raw, R9 type, and shared-background type freezes remain unmodified.
The formalizer's disclosed API-pristine status remains false.

The actual code statement strings for the two new mathematical declarations
exactly reproduce their prior frozen signature hashes:

- shared: `283e07e3c85b9a5cce5c3c40f574f23f593dfcca5e35be4d3e2800f378208b19`;
- R9 uncentered: `d5ac54443c79ea7b35b09ddcd6b5e3c40bef081bbe4f196cae5ab3ead35aa2ea`.

`exact-type-continuity-check.json` records this direct extraction from the
whole code, independently of the manifest's intended classification.

## Shared producer: full cone geometry and genuine integral

Snapshot 00, lines 18–23 has the already reviewed authored generic statement:
finite real square matrices on arbitrary finite n, arbitrary measurable
sample carrier and probability law, integrable actual f, and a.e. full PSD of
f. The conclusion is full PSD of the actual Bochner integral. These are natural
contracts at the arbitrary-function background boundary; they are not added
to R9. This is **ASTIS-authored reusable background**, not a general theorem
printed in the primary paper, an independently discovered source theorem, or
a source repair.

The complete body (lines 25–42) proves the PSD cone is closed as the
intersection of the closed Hermitian locus and the closed nonnegative
quadratic-form loci for all vectors. The actual conversion uses
`Matrix.posSemidef_iff_dotProduct_mulVec`, whose supplied definition includes
Hermitian symmetry as well as every quadratic form. It does not silently
discard Hermitian symmetry. Each quadratic form is a finite continuous
coordinate polynomial. Nonnegative scalar multiplication and addition supply
convexity; the unused normalization equality in the convexity binder is
legitimate because this set is a cone.

The final `Convex.integral_mem` application has the required closed set,
convexity, a.e. membership and actual integrability. The inspected Mathlib
contract requires a complete real normed space and a probability law, all
provided by the matrix carrier/standard instances and declared law. It has no
`[Nonempty n]` premise. Its own nonempty-set selection comes from a.e.
membership under a probability law, not selection of a matrix coordinate.
There is no positive dimension premise or local default/conditional proof.

Both the source module and the actual consumer explicitly open
`Matrix.Norms.L2Operator`. The fully read CStarAlgebra/Matrix source transports
the l2 operator norm from Euclidean continuous linear maps, preserves the
existing matrix topology/uniformity, and supplies the scoped normed structures.
This supports the closure argument and finite-dimensional Bochner semantics.
The scalar real star-ordered instance is actually imported and supplied.
The generic empty-index case is respected by the complete source: no index is
chosen and the inspected finite-PSD/Jensen contracts introduce no nonempty
matrix-index restriction. I have not run an empty-index elaboration or seen
one pass.

No proof is based on a nonintegrable integral's default value. `hf` is used in
the final expectation-membership application. The new R9 application proves
its own integrability before providing hf.

## Actual R9 experiment and hypotheses

Snapshot 01, lines 19–43 retains d,q natural and sole explicit proposition
`2*q+1<d`, including q=0. It defines the actual original independent-column
product Gaussian law, row projection, real r=q+1, exact L, exact half-grid
theta, constant-normalized cosine features, and the **closed** rowwise cutoff
Y. Tensor indices remain Gaussian-column first and feature second. No
integrability/transport/frame/moment/PSD certificate is a public input.

The repeated local definitions in lines 47–84 are the proof's actual objects,
not replacement data. The body contains no arbitrary expected matrix or
arbitrary PSD function substituted for Y. Its auxiliary `nu=stdGaussian E` is
used only after proving the marginal law of the original row map.

The result is precisely actual Y-square integrability and the uncentered
Loewner bound. It is not an operator-norm variance conclusion and does not
assert centering, the weighted centered bound, concentration, or the main
Krylov theorem.

## Row transport and R4 applicability

Snapshot 03 is fully read. It first identifies each coordinate of a standard
d-dimensional column with `gaussianReal 0 1`, using the supplied
`map_pi_eq_stdGaussian` and the product-coordinate evaluation law. It then
collects these coordinates across the independent columns with
`measurePreserving_pi`, and wraps the result in Euclidean r-space. This proves
the actual physical row map is measure preserving from the original column
product mu to `stdGaussian E`. It does not assert a new ambient experiment or
joint-row independence. Joint-row independence is unnecessary for this linear
sum-of-expectations calculation.

R9 lines 87–102 instantiate the R4 radial matrix moment at the same q and hq,
with E, nu, R, G and weighted matrix matching literally. Integrability is
pulled back by `MeasurePreserving.integrable_comp_of_integrable`.
The expectation transport deliberately uses general `integral_map` with a.e.
measurability of the row map and a.e. strong measurability of weighted under
the pushforward law. The inspected contract **does not require injectivity**.
No measurable-embedding or inverse-row assumption is smuggled in. The equality
orientation correctly converts the row integral back to the known nu moment.

Snapshot 04's complete R4 proof supplies both its integrability and exact
`E[||x||^2 x x^T]=(r+2)I` identity internally:

- Fernique's finite-moment theorem supplies MemLp id at exponent 4; the exact
  inspected `MemLp.integrable_norm_pow` contract requires the natural exponent
  be nonzero, which the concrete value 4 satisfies.
- Each weighted entry is continuous and bounded in absolute value by
  `||x||^4`. Finite product integrability and the continuous linear equivalence
  from rows to operator-norm matrices transfer this to the actual matrix
  function. Integral evaluation is justified by actual entry integrability.
- An explicit coordinate reflection preserves standard Gaussian measure and
  radius and negates off-diagonal entries. The transport also uses the general
  map-integral formula with the supplied measurability.
- The canonical coordinate product law yields the diagonal sum. The scalar
  second moment is one; the scalar fourth moment is three from snapshot 06;
  distinct coordinate squares are independent via `iIndepFun_pi`, with the
  concrete polynomial measurability supplied. Their mixed integral is one and
  the coincident term is three. Integrability is established in both cases
  before the finite-sum integral exchange.

Snapshot 06 is fully read: its scalar fourth moment uses the Gaussian mgf on
the full real exponential-integrability domain, the derivative/moment
identity, and four explicit derivatives of `exp(v*t^2/2)`. The supplied
MGFAnalytic and IntegrableExpMul contracts confirm the required interior-zero
condition and finite powers. The four derivative expressions and the value at
zero agree with `3*v^2`; R4 specializes to variance one. No fourth-moment
conclusion is assumed as a public R9 binder. The inherited d/hq context of R4
is mathematically unnecessary for the isolated radial identity but is already
available at the unchanged source range; this is not a new input to R9.

## Actual square, closed indicator, integrability and PSD residual

R9 lines 110–142 use **ordinary matrix multiplication**, prove both rank-one
squares, and apply ordinary Kronecker multiplication. They identify each
actual `Y_i*Y_i` exactly with `1_good_i W_i`, where

    W_i = (S_i/d^2) [ (||gamma_i||^2 gamma_i gamma_i^T) tensor (t_i t_i^T) ],
    S_i = sum_k t_i(k)^2,
    good_i = {omega | ||row_i omega||^2 <= L}.

The coefficient is S_i/d^2, with no lost factor of d, r, sqrt(2), or norm.
The indicator is that row's own closed cutoff; there is no conditioning on
all rows and no switched measure. The else branch produces zero by the same
literal cutoff. This matches source Ex114, including indicator idempotence.

W_i is a fixed continuous linear map of the transported integrable weighted
Gaussian matrix (lines 81–104), not an arbitrarily assumed majorant. The good
set's measurability is derived from the actual measurable row and norm square.
The inspected indicator-integrability contract therefore supplies actual
Y-square integrability in lines 143–145. No nonintegrable/default-zero moment
shortcut is taken.

Lines 148–161 express W_i as a rank-one matrix on the paired vector
`v_(a,k)=gamma_a*t_k` with coefficient `(S_i/d^2)*||gamma||^2 >= 0`.
The rank-one PSD fact includes full symmetry. Lines 162–170 then prove the
pointwise **residual** `sum W_i - sum Y_i^2` is PSD: each row contributes zero
on good_i and W_i off good_i. They do not assume or try to prove that the final
`C I - sum Y_i^2` is pointwise PSD.

Both finite sums are first proved integrable. Lines 175–178 actually apply the
new shared producer to their integrable PSD residual. Thus the shared theorem
is a substantive used dependency, not an imported unused badge or an
assumption wrapper. Its generic hf/hpos premises are discharged internally.

## Tensor/scalar means and the exact frame coefficient

R9 lines 181–200 pass the actual expectation through the fixed scaled tensor
continuous linear map, using the inspected integrable CLM commutation
contract. The result is `(r+2)/d^2 * S_i * (I tensor feature_i)` in the same
tensor ordering. Both the finite-sum expectation and difference-integral
rewrites have already established integrability of their actual operands.

Snapshot 05's complete deterministic frame proof uses snapshot 07's exact
Gram and feature-norm facts to show `C I-B` PSD. It transports the Gram sum by
the fixed tensor map, proves each `I tensor feature_i` PSD, sums the
nonnegative coefficients `2r-S_i`, and uses d!=0 derived from hq in the final
coefficient identity. It does not assume the frame comparison.

Snapshots 07 and 08 are fully read. The cosine-frame proof uses exact midpoint
grid aliases, product-to-sum and the strict frequency bounds from hq. The
constant degree is treated separately, so q=0 is retained. The alias theorem
handles divisible frequencies, including negative integers, with the signed
alias and handles other frequencies by the nonzero sine denominator. The
Gram and weighted Gram branches use their actual finite frequencies; the
feature-norm branch retains the special constant normalization.

R9 lines 203–208 prove the exact ring equality between the old zero-based
`i.val+1/2` angle and the source-facing `i.val+1-1/2` angle. They rewrite the
actual frame theorem by this equality, not by an approximate or shifted-grid
assumption. Finally `C I-B` and the integrated `B-sum E[Y_i^2]` residual are
added and algebraically cancelled. The final bound is an expectation bound,
with the correct `C=2r(r+2)/d`.

## All owned modules and cleanup flags

| Snapshot | Full range | Semantic role / flags |
|---|---|---|
| 00 RealMatrixPositiveIntegral | 1–44 | New shared cone/integral producer; genuinely called by 01; no input conclusion wrapper. |
| 01 FixedSpectrumSourceMatrixVariance | 1–216 | New actual uncentered consumer; all advertised inputs literal; all local majorant/residual obligations proved internally. |
| 02 Tests/RealMatrixPositiveIntegral | 1–9 | Imports and two #check commands only; creates no theorem alias. Its comment references separate empty probes that were not input/read/tested here. |
| 03 FixedSpectrumSourceRowLaw | 1–54 | Actual row marginal transport, used by 01; no claimed joint independence. |
| 04 FixedSpectrumRadialFourthMoment | 1–190 | Integrable radial matrix moment, used by 01; analytic conditions internal. |
| 05 FixedSpectrumWeightedFrameBound | 1–90 | Exact deterministic coefficient comparison used by 01; no symbolic arbitrary frame. |
| 06 GaussianFourthMoment | 1–93 | Scalar fourth moment used by 04; explicit mgf derivative computation. |
| 07 FixedSpectrumCosineGram | 1–168 | Actual cosine Gram, weighted cancellation and feature-norm facts; its Gram/norm outputs used by 05. |
| 08 FixedSpectrumGridAlias | 1–86 | Exact finite-grid frequency sums used by 07; retains negative aliases. |

No axiom/sorry/admit/fake closure, added hypothesis certificate, dead new
theorem, duplicate new PSD-integral cone proof, or new wrapper-only declaration
was observed in this fully read ASTIS closure. The source type/proof local-let
repetition is local definitional setup, not a second mathematical node.
Some parent conjunction outputs exceed what this particular consumer needs;
that is ordinary reuse of their existing interfaces, not proof of their
downstream results. The generic convex proof does not use the sum-one scalar
equality because it proves the stronger cone closure.

This is a closure-local code cleanup assessment, not a repository-wide API or
duplicate search, compiler-generated declaration inventory, performance check,
or purification certificate. Imports alone were not taken as mathematical
dependencies. Actual theorem calls above were read in the code, but kernel
acceptance remains separate.

## Stop boundary

All requested code-only applicability inputs were supplied and the relevant
contracts read. No unresolved blocking code-semantic issue was identified.
Compilation/axiom results, anonymous reconstruction, both anti-anchored audit
packets, source coverage, authored exposition, publication/integration and the
centered/weighted actual target remain outside this phase. No credit is given
to the absent centered target, to p15 Bernstein/concentration, or to the whole
Lemma 4.4/Goal. This report is frozen before those later inputs.
