# Independent type/definition audit, following the raw-source freeze

## Phase boundary and result

The only new input read in this phase is the exact selective packet whose raw
SHA-256 is `b9b93126880486157e88e9a59abcd2b89d81b4cf34d46fa9dc51f88d2b6e0170`.
The comparison baseline is my earlier raw-source interpretation, sealed by
`a543a126cd969c21bff3cd5b26cfe46a26ea4fd5bbe4f7b9ac618331d3d8bf11`.
The raw files have not been revised.

**Type/definition result:** no blocking mismatch found for this bounded
uncentered-moment and actual-centered-variance slice. The exact signatures and
expanded definition meanings preserve the objects, range, cutoff, matrix
square, PSD order, expectations, and two variance norm conclusions identified
in the independent raw reading. This is a type-only result, not proof
acceptance, compilation evidence, a decoder round trip, final anti-review,
source-complete assimilation, or Goal credit.

The packet includes producer-authored binder/output audits and definition-kind
annotations. They were visible input, not independent evidence. The
classifications below are my own comparison of the exact signatures and
literal definitions against the raw baseline. I have not read other reviewers'
opinions or the full statement-seal metadata. I have not opened any referenced
receipt or library file; hashes/paths of such files appearing in the packet do
not constitute my having inspected those original files.

## Exact targets read

The producer is
`AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments`,
with signature SHA-256
`d5ac54443c79ea7b35b09ddcd6b5e3c40bef081bbe4f196cae5ab3ead35aa2ea`.

The consumer is
`AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance.actual_source_centered_variance_bounds`,
with signature SHA-256
`95e81a02e5302de9a42e3b60038ffad6195315ac2eca99a4e6abb39978609f7e`.

The planned paths in the packet identify future code; no implementation body
was an input. Both signature string hashes, the literal-print string hash, and
all eight supplied literal-source excerpt string hashes recompute correctly.
This verifies the supplied strings' integrity, not a build or independent
verification of the receipt/library file hashes.

## Every binder and the source range

Both signatures have exactly the same explicit logical inputs:

| Input | Independent classification | Source justification |
|---|---|---|
| Implicit `d : Nat` | TYPING, with dimension positivity supplied by the range | The source dimension is a finite discrete dimension. |
| Implicit `q : Nat` | TYPING plus the source nonnegative-query convention encoded in the carrier | The source has `q>=0` and finite indices/degrees through q. No positive-query restriction is introduced. |
| `hq : 2*q+1<d` | SOURCE for Lemma 4.4; STANDING when this is inherited by its C.2 calculation | This is the exact source range, not a proof certificate. Its arithmetic consequences, including `d>=2` and a nonzero denominator, belong inside the proof. |

There are no input moment, frame, Gaussian-law, integrability, positivity,
variance, mean, measurability, transport, symmetry, or matrix-norm certificates.
There are no project-owned proposition aliases/structures in the input needing
a further hidden-binder expansion. All remaining local names are literal
`let` definitions, not universally quantified arbitrary witnesses or assumptions.
The standard finite-dimensional, probability, normed-space, and completeness
instances printed in the packet are synthesized standard structure, not user
supplied hypotheses.

`q=0` is included: `r=q+1` still gives one Gaussian column and one constant
feature. The only explicit range hypothesis remains `1<d` at that endpoint.
No `q>0`, `r^2<=d`, `tau<=1/2`, large-d threshold, or external endpoint
certificate is present or needed as a new source binder for this bounded
statement. The full Lemma 4.4 condition `tau<=1/2` belongs to its later
uniform/concentration conclusion, not to the p14 moment comparison.

There is no `kappa` binder. This does not discard a necessary hypothesis of
the bounded feature/row calculation: the original grid and features are
independent of `kappa`, and the source itself notes that independence. A claim
about the spectral Krylov equivalence or the original affine eigenvalue
construction would have additional scope, but neither target asserts that
claim.

## Complete expansion of the literal objects

1. `D = EuclideanSpace Real (Fin d)` and
   `E = EuclideanSpace Real (Fin (q+1))` are the usual l2 Euclidean spaces.
   The packet expands `EuclideanSpace` as `PiLp 2`; `WithLp.toLp 2` wraps the
   coordinate vector in that l2 normed space without changing its coordinates.

2. `Omega = Fin(q+1) -> D` is the original array of Gaussian columns. The
   finite product measure
   `mu = Measure.pi (fun _ => stdGaussian D)` is the joint law of `q+1`
   independent standard d-dimensional columns. The packet expands
   `stdGaussian D` as the pushforward of independent `gaussianReal 0 1`
   coordinates through a standard orthonormal basis. The finite-product
   construction is also supplied. These definitions provide the intended
   original sampling representation; proving measurable row projections,
   the resulting standard row law, and any integral transport remains internal.

3. `r` is the real coercion of the natural `q+1`. `L` is exactly
   `2*r + 3*log(1000*d)`. No arbitrary radial threshold replaces the source
   threshold.

4. `theta i = (i.val+1-1/2)*pi/d` uses zero-based `Fin d` indices. Under the
   correspondence `source index = i.val+1`, this is exactly
   `(source index-1/2)*pi/d`. It is neither the endpoint grid nor a grid shifted
   by a whole unit. `t i 0=1`; all positive degree indices `k` have
   `sqrt 2 * cos(k.val * theta i)`. This gives precisely degrees `0,...,q`,
   with the special constant normalization required by Fact C.5.

5. `row i omega = toLp 2 (fun b => omega b i)` collects physical coordinate
   `i` across the Gaussian columns. It is exactly the source `gamma_i`,
   represented on the original column-product space; it is not a separately
   sampled row array on a replacement probability space. The law equivalence
   needed for Gaussian moments is a proof obligation, not an extra binder.

6. Put `m = Fin(q+1) x Fin(q+1)`. Matrices are real functions `m -> m -> R`.
   `vecMulVec u u` has entry `u_b*u_c`. `kronecker A B` has entry at
   `((b,k),(c,l))` equal to `A_b,c * B_k,l`. Therefore the untruncated Y entry
   is

       d^(-1) row_i(omega)_b row_i(omega)_c t_i(k) t_i(l).

   The first member of each pair is the Gaussian-column coordinate and the
   second is the feature coordinate, exactly matching `gamma tensor t` in the
   raw source. Matrix size is `r^2` by `r^2`.

7. `Y i omega` uses that matrix when `norm(row i omega)^2 <= L`, and is zero
   outside. It is the source's **closed** cutoff; the else branch is literal
   indicator semantics, not a fallback for failure of a theorem. Each row is
   truncated by its own norm. There is no conditioning on the all-row event,
   no changed Gaussian measure, and no pre-centered matrix in this definition.

8. In the consumer, `mean i` is the Bochner integral of this exact `Y i` under
   this exact `mu`. `Z i omega = Y i omega - mean i`. No arbitrary matrix,
   formal mean symbol, or supplied identity is substituted for the actual
   expectation.

9. `w i = cos((2*q+1)*theta i)` is deterministic in the physical row and
   equals the raw source `cos(n theta_i)`, including `n=1` when `q=0`.
   The real bound named `C` in these signatures is exactly
   `2*r*(r+2)/d = v_*` from p14. It is not the unspecified absolute constant
   also named `C` in the main-text definition of `tau_(d,q)`.

Each object is literal. No characterized/choice object or quotient
representative has been introduced. The finite zero-based renaming is an
index representation change, not a source repair.

## Matrix product, positivity, norm, and integration meanings

The actual `Mul` print supplied in the packet resolves to ordinary finite
matrix multiplication. The literal excerpt expands it to

    (A*B)(alpha,beta) = sum_eta A(alpha,eta) B(eta,beta).

Thus every `Y*Y` and `Z*Z` in the targets is a matrix square, as required by
Ex114/Ex118. It is not a Hadamard square or squared-entry array. Scalar
multiplication `w i • Z i omega` multiplies every matrix entry by the same
deterministic real scalar before ordinary multiplication.

The output `Matrix.PosSemidef M` expands to both:

    M.conjTranspose = M,
    for every finitely supported x,
      sum_alpha,beta star(x_alpha) M_alpha,beta x_beta >= 0.

The coefficients are real, so conjugate transpose is transpose. The finite
paired index set makes the Finsupp condition the full finite-dimensional
quadratic-form condition for all vectors. The producer asserts Hermitian
symmetry as well as nonnegative quadratic form; it does not weaken PSD to only
a quadratic inequality for a possibly nonsymmetric matrix. Its difference
`C • 1 - sum_i integral(Y_i*Y_i)` is exactly the Loewner upper bound by
`C I_(r^2)`. Matrix `1` here is the identity matrix under the ordinary matrix
ring structure.

The supplied actual normed-ring/normed-space instances are the L2-operator
instances. The literal norm construction is induced from continuous linear
maps between `EuclideanSpace`s, and the supplied norm equality identifies the
matrix norm with that continuous-linear-map operator norm. Consequently the
consumer's displayed `norm` means the Euclidean l2 operator norm appearing in
the source variance parameter, rather than the sup norm of entries or a
Frobenius norm. This conclusion uses the supplied actual instance prints plus
definition excerpts, not the fact that matrices happen to be functions.
No implementation scope or elaborated proof module has been independently
checked in this phase; future code must retain the packet's actual scope.

`Integrable f mu` expands to an a.e. strongly measurable representative and
finite integral of the extended norm. The supplied Bochner integral definition
returns zero when integrability/completeness fails. The fixed matrix carrier
has supplied standard completeness, and the explicit squared-variable
integrability outputs ensure that each displayed second moment is a genuine
integral in the accepted theorem. Integrability of Y itself is still required
internally to justify that `mean` agrees with the ordinary source expectation
and to justify centering algebra. Merely pointing at the syntactically defined
integral is insufficient. This is an internal applicability obligation for
the explicitly fixed truncated Gaussian variables, not a missing source
assumption or a reason to add a binder.

## Exact output audit against the frozen source

There are three random squared-variable families, all under the same `mu`:

| Output | Meaning and source relation |
|---|---|
| Producer: each `Y_i*Y_i` integrable | Establishes the ordinary actual uncentered second moments in p14; a source-implicit analytic obligation made explicit as a conclusion. |
| Producer: `C I - sum_i integral(Y_i*Y_i)` PSD | Exactly the Ex115–Ex117 uncentered Loewner bound with the complete PSD meaning. |
| Consumer: each `Z_i*Z_i` integrable | Establishes the actual centered second moments for Ex118 and the variance statement. |
| Consumer: each `(w_i Z_i)*(w_i Z_i)` integrable | Establishes the cosine-weighted centered second moments for Ex120. |
| Consumer: norm of `sum_i integral(Z_i*Z_i)` at most C | The actual centered variance-parameter bound, with genuine l2 operator norm. |
| Consumer: norm of `sum_i integral((w_i Z_i)*(w_i Z_i))` at most C | The actual weighted centered variance-parameter bound in p14. |

The two consumer estimates are norm conclusions, not only a statement of
quadratic-form domination. The source calls these sums' norm bounds variance
parameter bounds; neither target mistakes the sum for the expectation of the
square of a sum, nor requires cross-term cancellation as a hypothesis. Every
`i` quantifier and sum ranges over the physical rows `Fin d`, while the paired
matrix coordinates range over Gaussian-column/feature pairs.

The producer alone does not assert the centered variance conclusions; the
consumer does not treat them as arbitrary provided data. The stated intended
use of the producer by the consumer is coherent. An actual theorem dependency
edge can only be confirmed after a proof exists; the packet's intended edge is
not already compiled evidence.

The exact Gaussian fourth-moment identity Ex113, rank-one/tensor square
identity Ex114, centering identity Ex118, and scalar weighted comparison Ex120
need not all appear as separately named theorem conclusions. For this bounded
task, they may be internal proof steps leading to the exact advertised output.
Their omission as public conclusions does not weaken the specific endpoint
moment/variance statement. Their absence from an eventual proof would instead
be a proof-route/application question.

## Internal obligations, not additional binders

The following are still necessary evidence for a future proof/application and
are **not proved or searched for here**:

- Measurability of the original coordinate row maps, polynomial matrices,
  closed radial cutoff, and their combinations; the correct row law/transport
  from the actual column-product measure to standard r-dimensional Gaussian
  integrals.
- Sufficient finite Gaussian moments or direct bounds to establish all needed
  integrability, in particular Y itself, its matrix square, the mean/centering
  cross terms, Z's matrix square, and the weighted square. Finite-sum/integral
  interchanges must be justified for these actual functions.
- The Gaussian fourth-moment computation for the actual rows, ordinary
  rank-one/tensor multiplication, and indicator domination as stated by
  Ex113/114. These are proof ingredients, not assumptions to import as facts
  about an arbitrary random matrix.
- The exact cosine-grid norm and tight-frame sum from Fact C.5, valid on the
  given range including q=0. Weighted feature cancellation pertains to the
  source's separate mean-of-weighted-Y statement; the p14 centered weighted
  comparison uses the bounded scalar square, without a new cancellation
  hypothesis.
- Symmetry/PSD for Y, centered symmetric Z and their squares, expectations,
  and finite sums; expectation monotonicity and the full PSD difference.
- The identity `E[Z_i^2]=E[Y_i^2]-(E Y_i)^2` for the actual mean, with
  noncommuting products handled by the expectation identities rather than an
  unjustified commutativity assumption.
- Positivity plus upper PSD domination of the centered and weighted sums,
  `0<=w_i^2<=1`, and the finite-dimensional Hermitian spectral/operator-norm
  bridge converting `0<=S<=C I` to `norm S<=C`. An upper PSD comparison alone
  for an arbitrary possibly indefinite S would not establish the stated norm
  bound. Here the positivity must be proved internally from the actual
  squared symmetric matrices; no positivity certificate is an input.

No item above warrants a new public binder. The target fixes enough concrete
data for these obligations to be internal. No genuine target/source problem,
source-invalidity verdict, source repair, or formalization-artifact repair is
identified by the type/definition comparison. Proof feasibility and correct
library application remain unreviewed.

## Seven semantic slots and exclusions

| Slot | Type-only assessment |
|---|---|
| Objects | Same original columns, physical rows, actual Y, actual mean and Z; exact matrix/tensor carriers. |
| Domains | Natural d,q; paired r-by-r feature/Gaussian coordinates; real Euclidean l2 spaces; original finite product Gaussian law. |
| Quantifiers | All d,q in the exact range; each physical row's integrability; whole finite sums' PSD/norm conclusions. No arbitrary proof certificates. |
| Assumptions | Sole explicit proposition is the source range; q>=0 encoded by Nat; d>=2 internal consequence; no EXCESS input. |
| Conclusion | Exact uncentered PSD bound plus actual centered and weighted variance norms, with the three required integrability families. |
| Scopes/senses | Ordinary matrix products, closed rowwise truncation, full Hermitian PSD, actual Bochner expectations under identical mu, actual l2 operator norm. |
| Constant dependence | Explicit `2(q+1)(q+3)/d` variance coefficient, independent of kappa; no confusion with the main lemma's existential absolute constant. |

Matrix Bernstein, tail concentration of summed matrices, final uniform Krylov
bound, implementation code, API choice, proof checking, final semantic
round-trip verdict, publication admission, and Goal completion remain excluded.
