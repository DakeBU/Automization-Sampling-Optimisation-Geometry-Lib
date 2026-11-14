# Independent type-only judgment — ri_src_5ab9, phase 2

Disposition: **no type-level source-meaning blocker for the two assigned narrow
targets**. This is an independent comparison of the exact supplied types with
my previously frozen raw-source reading. It is not an implementation review,
compiler judgment, completed semantic round trip, source-VERIFIED transition,
proof approval, or permission to proceed under repository process gates.

## Bound inputs

The preexisting source freeze is `../source_reading_freeze.md`, SHA-256
`ebada7079da3a5f4315c69e5f14185f787e2c0fc93c4ad29feb6054f2199fec0`.
The sole new file is the 20581-byte selective type/definition packet, SHA-256
`c9f8312610515f2ebc067612c981889103e7d8a93a00aa5f75ec8c74feb1ab68`.
Its exact byte snapshot is retained in this phase directory.

The packet identifies statement seal
`88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e`
and minimal-definition context
`bb8e77b15c4905a3b5d4aa37e482314e44a5d97886088c72b91f36050bcf9860`.
These are packet fields matching the supplied binding identifiers; the original
seal/context artifacts were not opened or independently reconstituted.

The embedded signature string digests were recomputed and match:

- Producer: `2898f07e581afb8c38fa6dda16193a411dee6b9729a198b0a1437a98c726405a`.
- Private consumer: `026e3d3282b502cb069c022ac844e86ed4613cf62a8be2a9948edf3f25f02cf8`.

The embedded literal-print string and all supplied literal definition-excerpt
hashes also match their contents. This is a text-integrity check only.

## Binder and definition audit

Both statements quantify implicitly over `d q : Nat`. Their only logical
premise is `hq : 2 * q + 1 < d`. This is the exact frozen source range, includes
`q=0`, and supplies no caller certificate for any desired conclusion.
The type/definition classification is:

| Input | Class | Meaning |
| --- | --- | --- |
| `d q : Nat` | TYPING | Finite physical dimension and nonnegative integer degree/query count. |
| `hq : 2*q+1<d` | STANDING | The source's strict parameter range. |
| `D,E,Omega,mu,row` local lets | Definitional expressions, not logical premises | Concrete canonical carriers, experiment and actual rows. |
| `r,L,theta,t,Y` consumer local lets | Definitional expressions, not logical premises | Literal source constants, deterministic features and actual truncated maps. |

There is no `EXCESS` logical binder, no repaired-source `RULED` binder, and no
additional mathematical typeclass premise supplied by a caller. The packet's
word `DEFINITION` for local lets is understood as a description of definitional
abbreviations, not as a sixth classification of logical hypotheses under the
repository's five-bin binder audit.

Neither signature requires row independence, a row-law certificate, matrix
measurability, matrix independence, a probability/cutoff event, a Gram identity,
a norm/moment/tail estimate, `tau`, or `kappa` as input. Definitions remain
literal on the complete public carrier; there is no existential witness,
arbitrary representative, or existence-dependent fallback.

## Seven source-meaning comparisons

1. **Objects.** `D=EuclideanSpace R (Fin d)` is the real physical column space;
   `E=EuclideanSpace R (Fin (q+1))` is the real row space. A sample
   `omega : Fin (q+1) -> D` is the tuple of actual columns. The row definition
   `WithLp.toLp 2 (fun a => omega a i)` keeps precisely the coordinates of those
   columns at physical position `i`. It neither samples replacement rows nor
   asserts an unspecified equal-in-law coupling. The `WithLp` wrapper supplies
   the Euclidean row norm while retaining these coordinates.

2. **Domains.** Both statements have the same natural `d,q`, same strict
   `hq`, same finite column/sample/row carriers, and same canonical measure.
   They do not quantify over arbitrary ambient experiments. The matrix
   codomain is explicitly a function of two finite paired indices into `R`,
   definitionally a square `Matrix` of dimension `(q+1)^2`. Its supplied
   measurable structure is the ordinary finite product of real entry spaces,
   rather than an opaque locally chosen matrix measurable space.

3. **Quantifiers.** The producer concludes `iIndepFun row mu` for the entire
   `Fin d` family. The supplied definition expansion passes through generated
   inverse-image sigma-algebras to factorization for every finite set of
   indices and every corresponding measurable event choice. It is full joint
   independence, not pairwise independence or a selection of coordinate tests.
   The constant-kernel/Dirac-on-Unit expansion does not introduce a source
   conditioning variable: its almost-everywhere clause is over the sole Unit
   point, and means the same ordinary measure factorization under `mu`.
   The consumer concludes a universal `forall i, Measurable (Y i)` and full
   `iIndepFun Y mu`. These are both outputs, not hypotheses.

4. **Assumptions.** `mu = Measure.pi (fun _ => stdGaussian D)` is the finite
   product of standard Gaussian column laws on that exact tuple space. It is
   not a claim of a standard Gaussian law on the bare function space's norm.
   The supplied standard definitions/instances match this meaning without
   adding column laws or independence as caller premises. No source main-bound
   condition is imported into the independence target.

5. **Conclusion.** The public producer proves exactly the added full-row
   independence component on the canonical experiment. It does not assert
   `N(0,I_r)` row laws or explicit row measurability as additional outputs.
   The source's complete first-paragraph sentence contains those Gaussian-law
   meanings too; this type alone therefore must not receive credit for the
   whole sentence. The independently existing canonical row-law result remains
   a separate dependency/boundary and has not been inspected here. The private
   consumer's conjunction has exactly the intended actual-matrix measurability
   and joint independence outputs. In particular, `iIndepFun` alone does not
   establish arbitrary-map measurability; the separate `Measurable` conjunct is
   material and is present.

6. **Scopes/senses.** Physical source row index is `i.val+1`; physical column
   index is `a.val+1`. In contrast, feature index `k.val` is the actual frequency
   `0,...,q`, so no frequency shift is made. Both statements use literally the
   same `Omega`, `mu`, and `row` expressions. The consumer's `Y i` depends on
   that actual row alone and deterministic `t i`. The cutoff is local to `i`;
   there is no shared all-row event and no conditioned law. The matrix
   functions may differ with `i`; neither type claims identical distribution
   of the matrices. No arbitrary ambient-space transfer is asserted.

7. **Constants/endpoints.** The consumer has
   `r=((q+1:Nat):R)`, `L=2*r+3*Real.log(1000*(d:R))`, and
   `theta i=(((i.val:R)+1-(1/2:R))*Real.pi)/(d:R)`.
   This is the exact one-based midpoint grid of the frozen source, with the
   half interpreted in `R`. The feature zero is exactly `1`; every other
   frequency is `sqrt(2)*cos(k.val*theta i)`. The norm is Euclidean row norm,
   squared before comparison. Equality at `norm^2=L` selects the retained
   branch. The retained normalization is `(d:R)^(-1)`, and the removed branch
   is the zero entry-array. Parameter range prevents the otherwise irrelevant
   zero-dimension denominator case. `q=0` retains the one-dimensional row and
   sole feature `1` without a special missing endpoint.

## Actual matrix identity

Using paired indices `(a,j)` and `(b,k)`, with the Gaussian coordinate first,
the supplied literal outer-product/Kronecker definitions interpret the retained
entry as

`(d:R)^(-1) * ((row i omega a)*(row i omega b)) * ((t i j)*(t i k))`.

The branch test is exactly `norm(row i omega)^2 <= L`. This is the source's
`d^(-1) (gamma_i gamma_i^T tensor t_i t_i^T) 1_{R_i<=L}` on the actual row, in
the source tensor order. The explicit real-entry function type retains the
ordinary matrix semantics and does not weaken the object to a trace, norm,
distributional proxy, conditional mean, or existential matrix.

## Exposure and remaining boundary

I received the parent's disclosures `formalizer_API_pristine=false`, retained
preseal Matrix-alias/let-instance formation failures, and that final-v4 Props
were formed only at seal rather than proved there. Those are process-history
disclosures, not independent mathematical evidence. They do not change this
type-only comparison, and I do not certify their timing or receipt contents.

The packet contains receipt paths and hashes alongside literal standard
definition prints. I saw those metadata fields but did not open any receipt,
log, implementation file, lesson, graph, previous source audit, decoder
artifact, or compiler evidence. Definition print/excerpt bodies in the packet
were permitted semantic input, not target implementation proof input.

There is no type-level blocker within the assigned scope. Remaining work is
to inspect only the separately supplied current code after this freeze, then
compare the source to a fresh anti-anchored packet after independent anonymous
decoding. This judgment does not discharge either later phase and does not
assert that either theorem is proved or compiled.
