# Raw source interpretation — frozen before target exposure

This is an independent reading of the pinned original HTML. It records the
source's mathematical content and proof ingredients, not a Lean result or a
fidelity verdict. ROOT remains the sole mathematical prover. No target name,
type, implementation, decoder reconstruction, prior verdict, canonical audit,
registry, ledger, or parent graph was supplied or inspected in this phase.

## Source and standing range

The original is *On Complexity of Gaussian Sampling*, arXiv 2610.20492v1,
SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
The relevant main-text item is **Lemma 4.4**, not a theorem labelled 4.4.
Its grid is introduced at `S4.SS1.p1` under `d >= 2`, `kappa >= 2`:

    theta_i = (i - 1/2) pi / d,       1 <= i <= d,
    lambda_i = (kappa + 1)/2 + (kappa - 1) cos(theta_i)/2.

The dimension and query indices are discrete: the source treats `d` as an
ambient vector dimension and `q` as a query budget, and indexes degrees
`0,...,q`. Lemma 4.4 explicitly states `q >= 0` and `2q+1 < d`. Its finite
indexing presupposes integer query budgets; it does not spell out a separate
`q is an integer` sentence in the displayed statement.

`S4.SS2.SSS0.Px1.p2` defines the block Krylov space as the span of
`Lambda^j g_a`, `1 <= a <= q+1`, `0 <= j <= q`.
`S4.SS2.SSS0.Px2.p1` defines `n=2q+1` and
`D_n = diag(cos(n theta_1),...,cos(n theta_d))`.

Lemma 4.4 states the existence of an absolute positive constant `C`, with

    tau_(d,q) = C [(q+1) sqrt(log d / d)
                  + (q+1)(q+1+log d) log d / d].

For independent `g_1,...,g_(q+1) ~ N(0,I_d)`, if `tau_(d,q) <= 1/2`, the
source concludes with probability at least `0.99` that
`|u^T D_n u| <= 2 tau_(d,q) ||u||^2` simultaneously for every `u` in the
Krylov space. The sentence after the lemma says the estimate is independent of
`kappa` because the spectral affine change of variable is nonconstant. These
are source context, not a claim that this bounded moment phase proves the
lemma or its probability bound.

## Experiment and literal definitions

`A3.SS2.p1` sets `r=q+1`, `n=2q+1`. The original random inputs are the
independent `d`-dimensional Gaussian **columns** `g_a`. For each physical row
`i` it forms

    t_i = (1, sqrt(2) cos(theta_i), ..., sqrt(2) cos(q theta_i))^T,
    gamma_i = ((g_1)_i,...,(g_r)_i)^T.

The source explicitly states that `gamma_1,...,gamma_d` are independent
`N(0,I_r)` vectors. The matrix `B` is `d` by `r^2`, with row `i` equal to
`d^(-1/2) (gamma_i tensor t_i)^T`. This fixes the tensor coordinate order:
the Gaussian-column coordinate is the first factor and cosine-feature degree
is the second. A later translation must preserve the physical-row experiment
or explicitly justify an equal-law representation.

At `A3.SS2.p10`:

    L = 2r + 3 log(1000d),       R_i = ||gamma_i||^2.

At `A3.SS2.p12`:

    Y_i = d^(-1) (gamma_i gamma_i^T tensor t_i t_i^T) 1_{R_i <= L}.

This truncation is **closed**. Its complement in the bias calculation is the
strict event `R_i > L`. The matrices are independently truncated row by row;
they are not conditioned on the simultaneous event for all rows. Their law is
not replaced by a conditional Gaussian law. These distinctions are literal
source semantics.

The source defines

    a = r^(-1) E[R_i 1_{R_i <= L}],
    Z_i = Y_i - E[Y_i].

Radial symmetry gives a single scalar `a` for every row. The source states
`0 <= a <= 1`, `1-a <= (L+3)/(1000rd)`,
`E Y_i = (a/d)(I_r tensor t_i t_i^T)`,
`sum_i E Y_i = a I_(r^2)`, and
`sum_i cos(n theta_i) E Y_i = 0`.

## Feature identities and their use

Fact C.5 (`A3.Thmtheorem5`) states:

    range(B) = K_q,
    E[B^T B] = I_(r^2),        E[B^T D_n B] = 0,
    ||t_i||^2 <= 2r,
    sum_i t_i t_i^T = d I_r,
    sum_i cos(n theta_i) t_i t_i^T = 0.

Its proof (`A3.SS2.p3`–`p8`) provides the actual source support, not an
arbitrary assumed tight-frame property. It uses the Chebyshev polynomial
change of basis; the grid identity `sum_i cos(k theta_i)=0` for integers
`0<|k|<2d`; product-to-sum for feature orthogonality; and triple
product-to-sum for weighted cancellation. The weighted frequency range is
`1 <= n-j-k <= n +/- j +/- k <= n+j+k <= 4q+1 < 2d`.
The final norm bound comes from
`1 + 2 sum_(j=1)^q cos^2(j theta_i) <= 1+2q <= 2r`.

Only the norm and unweighted tight-frame sum are used in the uncentered
squared-moment estimate itself. Weighted cancellation supplies the exact zero
mean of the truncated cosine-weighted total in `p12`; it is not needed to
show that multiplying centered summands by cosine cannot enlarge the second
moment matrix in `p14`.

## Tail, bias, and boundedness context

`p10` uses `E exp(R_i/3)=3^(r/2)` and Markov's inequality to state
`P(R_i>2r+3x) <= exp((r/2)log 3 - 2r/3 - x) <= exp(-x)` for `x>=0`.
It then gives probability at least `0.999` for the simultaneous closed
truncation event. `p11` integrates the same tail to obtain
`E[R_i 1_{R_i>L}] <= (L+3)/(1000d)`.

`p13` gives the deterministic norm bounds

    ||Y_i||op <= 2rL/d,
    ||E Y_i||op <= 2r/d,
    ||Z_i||op <= 2r(L+1)/d = R_*.

The same `R_*` applies to `cos(n theta_i) Z_i` since the cosine has absolute
value at most one. The tail/bias and centered-norm calculations are source
neighbors and future concentration inputs. The uncentered squared-moment
comparison below does not require the probability `0.999` as a hypothesis.

## Exact moment and variance boundary

`A3.Ex113` in `p14` is exactly the source Gaussian fourth-moment identity

    E[R_i gamma_i gamma_i^T] = (r+2) I_r.

The source explains that off-diagonal entries vanish by sign symmetry and
each diagonal is `3+(r-1)=r+2`.

`A3.Ex114` is the squared truncated matrix formula

    Y_i^2 = (R_i ||t_i||^2 / d^2)
            (gamma_i gamma_i^T tensor t_i t_i^T) 1_{R_i <= L}.

The single indicator is correct for the source's formula because the
indicator is squared when the matrix is squared. The preceding source text
uses `(gamma_i gamma_i^T)^2 = R_i gamma_i gamma_i^T` and
`(t_i t_i^T)^2 = ||t_i||^2 t_i t_i^T`.

The display `A3.EGx11` (rows `A3.Ex115`–`A3.Ex117`) then states

    sum_i E[Y_i^2]
      <=PSD (r+2)/d^2 sum_i ||t_i||^2 (I_r tensor t_i t_i^T)
      <=PSD 2r(r+2)/d^2 (I_r tensor sum_i t_i t_i^T)
       = 2r(r+2)/d I_(r^2).

This is an **uncentered matrix second moment**. The source route drops the
truncation indicator from a positive semidefinite integrand, then uses
Ex113, the feature norm bound, and the exact feature sum. It is not an
estimate of `(E Y_i)^2`, and it is not itself a tail probability.

`A3.Ex118` supplies the distinct centered comparison

    E[Z_i^2] = E[Y_i^2] - (E Y_i)^2 <=PSD E[Y_i^2].

The source consequently says the centered sequence has variance parameter
at most `v_* = 2r(r+2)/d` (`A3.Ex119`). The expected convention here is the
operator norm of the sum of centered second-moment matrices; `p14` itself
expresses the derivation by positive semidefinite comparisons and calls the
result a variance parameter. I did not read the later Bernstein paragraph to
import any additional convention.

Finally `A3.Ex120` states

    E[(cos(n theta_i) Z_i)^2]
       = cos^2(n theta_i) E[Z_i^2] <=PSD E[Z_i^2],

and the source says the weighted centered sequence has the same bound. This
comparison is for a deterministic row-dependent scalar cosine and uses the
positive semidefiniteness of `E[Z_i^2]`.

## Source hypotheses versus proof obligations

The source inputs are the discrete dimension/query range, the exact cosine
grid/features, and the original independent standard Gaussian column
experiment. The matrix construction and cutoff are definitions. The Gaussian
fourth-moment identity, feature sums and bounds, truncated mean formula,
integrability needed to take matrix expectations, positivity/order comparison,
and centering identity are proof ingredients. They should be discharged
internally for this experiment, not added as public assumptions to claim this
source calculation.

Necessary internal ports identified by this reading, with no library/API
search and no assertion that any port already exists:

1. Product standard-Gaussian coordinates / conversion from independent column
   samples to the physical-row marginal and joint laws; measurable row
   extraction and the closed radial event.
2. Gaussian coordinate moments, sign symmetry, and finite polynomial moments
   sufficient for Ex113 and the matrix-valued expectations in the calculation.
3. Rank-one square and tensor-product multiplication identities with the exact
   tensor order and finite index sizes in the source.
4. Symmetry/positive semidefiniteness of these rank-one tensors and their
   squares; indicator domination; expectation and finite-sum monotonicity.
5. The exact feature norm bound and tight-frame sum from the pinned grid.
   Weighted feature cancellation is a separate source identity for `p12`.
6. Entrywise integrability/linearity sufficient for the matrix centering
   identity, and positivity of the square of a symmetric expectation matrix.
7. Deterministic scalar-square extraction and `0<=cos^2<=1` for the weighted
   centered comparison; conversion from the PSD sum bound to the source's
   variance-parameter norm statement.

This list distinguishes omitted implementation obligations from absent source
assumptions. It does not assert a source error or an accepted repair.

## Cutoff

The bounded calculation stops at the end of `A3.SS2.p14`, after Ex120.
`A3.SS2.p15` and all subsequent matrix Bernstein/concentration work are
excluded. The main lemma, the strategy paragraphs, and Fact C.6's title were
visible as context; no proof of concentration or final uniform bound is
claimed. This raw freeze awards no theorem, integration, or Goal credit.
