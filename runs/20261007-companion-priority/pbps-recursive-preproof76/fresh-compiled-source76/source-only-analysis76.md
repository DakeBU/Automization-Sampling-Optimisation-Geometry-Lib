# Independent source-only freeze 76

Status: OPEN source-only review. Candidate Lean, header76, previous source/math
verdicts, other reviewer transcripts, publication/frontier records and adoption
decisions have not been read. This is neither whole-source admission nor a
VERIFIED result. The semantic-roundtrip skill is being applied. The only
mathematical source is the pinned primary PBPS HTML; Davis (1984) is bibliographic
context because its theorem text has not been inspected.

## Source boundary

The principal anchor is Appendix A.1, `A1.SS1.p2`, RAW lines 2889–2912,
especially the combined equation region `A1.EGx2`, lines 2893–2907, containing
(A.1) and (A.2). The complete surrounding mathematical regions are preserved as
RAW bytes, including all of A.1, §3.2/Algorithm 1/Proposition 3.1, §2, (1.1),
and the reused display (4.5). `raw-manifest76.json` gives byte intervals, lengths,
and RAW plus CRLF-to-LF-only SHA256 values. The complete primary file has no
CRLF, so these two source digests coincide. `*.mathtext.txt` are reading aids;
RAW is authoritative.

Standing paper assumptions in (1.1): the target is on R^d; V is C²; there are
0 < α ≤ β with αI ≤ Hess V(x) ≤ βI for every x. §2.2 places η in (0,1/β].
For the selected deterministic finite-recursion argument, only η > 0 and the
β-Lipschitz property of g = ∇V are used analytically; α and normalization of μ
are not needed. A result for an arbitrary Lipschitz vector field g is a genuine
deterministic generalization of this ingredient, to be labelled as such. It
must not be described as the whole paper proposition.

## Objects, definitions, initialization and finite domain

Fix y and r = x-tilde in R^d. The same r remains fixed at every recursion step.
For z = (x,p) in R^d × R^d define

    c = y - η g(r),       h(x) = g(x) - g(r),
    λ(x,p) = sqrt(η) max(<p,h(x)>,0),
    R_h p = p - 2 <p,h> h / ||h||²  if h ≠ 0;   R_0 p = p,
    S(x,p) = (x,R_{h(x)}p),
    Φ_u(x,p) = (c+(x-c) cos u+sqrt(η) p sin u,
                -(x-c) sin u/sqrt(η)+p cos u).

Φ is defined for every real u. Waiting times and hazard integrals use u ≥ 0.
R_0 = I is an explicit source convention, not an invented fallback. S is an
involution, is Borel, and may fail to be continuous at h(x)=0. At h(x)=0 the
rate is zero. No global continuity of the bounce map may be imposed.

Start with z_0 = (x_0,p_0), T_0 = 0. The paper takes independent Exp(1) clocks
E_j, j ≥ 1. For a deterministic finite ingredient use indexed thresholds e_j
and, at an active state z_n, set

    A_z(u) = ∫_0^u λ(Φ_s(z)) ds,
    s_{n+1} = inf {u ≥ 0 : A_{z_n}(u) ≥ e_{n+1}}.

The infimum is an extended nonnegative waiting time, with inf(empty)=∞. For
finite s_{n+1} set

    T_{n+1} = T_n + s_{n+1},
    z_{n+1} = S(Φ_{s_{n+1}}(z_n)).

If the hit set is empty, the source sets both S_{n+1} and T_{n+1} to ∞ and
stops; it does not evaluate Φ_∞ or manufacture a post-bounce state. Later
indices may be represented as terminated, but have no mathematical ζ_{T_n}.
For 0 ≤ t < s_{n+1} the deterministic arc is Φ_t(z_n). A finite-step result
quantifies over finite n (or a finite prefix N), and over precisely the active
indices for which the recurrence has reached a finite time. Existence of the
next finite waiting time for every state is not asserted: constant-zero rates
already refute it.

Algorithm 1 draws r conditionally and draws p_0 independently; Proposition 3.1
then explicitly quantifies over every *fixed* y,r and every initial phase-space
point. These sampling laws are not extra premises for the selected pathwise
finite recursion. Resampling r at every bounce would change the source model.

## Exact finite proof ingredients (Ex4–Ex8)

For fixed c and η > 0 set

    H(x,p) = 1/2 (||x-c||²/η + ||p||²),       E = H(z_0).

The displayed flow is a rotation of ((x-c)/sqrt(η),p), so H(Φ_u z)=H(z).
Orthogonality of R_h, including R_0=I, gives H(Sz)=H(z). Induction through
the actual finite recurrence therefore gives H(z_n)=E and H(Φ_u z_n)=E,
without placing energy preservation into a public theorem premise.

Nonnegativity of the two summands then gives Ex5:

    ||p|| ≤ sqrt(2E),       ||x-c|| ≤ sqrt(2ηE).

Cauchy–Schwarz, positivity of sqrt(η), the Lipschitz estimate
||h(x)|| ≤ β||x-r||, and ||x-r|| ≤ ||x-c||+||c-r|| give Ex6's bound

    0 ≤ λ(x,p) ≤ B,
    B = sqrt(η) β sqrt(2E) (sqrt(2ηE)+||c-r||).

This holds on every active finite state and every deterministic arc from it.
Integrating it on [0,u], u ≥ 0, gives Ex7: 0 ≤ A_z(u) ≤ B u.
The rate along an arc is continuous; its finite integral is therefore finite
and continuous, nondecreasing in u, and starts at zero. If e ≥ 0 and the
first-hit waiting time s is finite, closedness of the hit set gives A_z(s) ≥ e.
These are derived proof ingredients, not acceptable replacement hypotheses for
the concrete source hazard.

For B > 0, Ex8 follows as e ≤ A_z(s) ≤ Bs, hence s ≥ e/B. Summing finite
increments also gives T_n ≥ (sum_{j=1}^n e_j)/B on an active finite prefix.
The deterministic finite sum inequality is only the finite part of Ex9; it
does not supply its almost-sure divergence conclusion.

For B = 0 the rate on the energy shell is zero. If e > 0, the hit set is empty
and the recursion terminates; this is the source's no-jumps branch for positive
exponential clocks. Division by B must not be used here.

## Zero thresholds: permitted deterministic completion and its limit

The paper chooses Exp(1) thresholds; they are strictly positive almost surely.
It does not claim a process for every deterministic clock sequence containing
zeros. Extending the *indexed* finite recurrence to e_j ≥ 0 is mathematically
natural: e=0 gives s=0 because A_z(0)=0. The zero branch must preserve this
first-hit semantics. Replacing zero by ∞ would be off-source semantics for the
extended inverse-hazard definition.

However, zero waiting times may identify distinct indexed states with the
same timestamp. Source-compatible example: d=1, V(x)=x²/2, α=β=η=1,
y=r=0, z_0=(1,1), e_1=0. Then s_1=T_1=0 while z_1=(1,-1) ≠ z_0.
If e_2=0, z_2=(1,1) again at time zero. Thus one cannot interpret every
z_n as a single-valued trajectory value ζ_{T_n} for arbitrary zero thresholds
while also maintaining the original ζ_0. Timestamps are nondecreasing, not
necessarily strictly increasing. A deterministic zero-threshold result must
remain an indexed finite recursion; an actual process construction requires
the positive-clock event (or a separately justified zero-time convention).

If B=0 and e=0 then A_z≡0 and s=0, so the literal inverse-hazard recursion
does not stop. Under the source-derived cap and η>0, β-Lipschitz g, the relevant
bounces are inert: B=0 forces either E=0 (so p=0) or β=0 (so h=0). Even then
the indexed clock can repeat zero-time steps; the original 'there are no jumps'
wording must not be repurposed as 'every nonnegative threshold gives ∞'.
The all-zero threshold sequence also shows why deterministic finite control
alone does not establish nonaccumulation.

## Measurability: required meaning, not an extra source premise

On finite-dimensional Euclidean Borel spaces, g is continuous by Lipschitzness;
Φ and λ are continuous in their finite arguments. The reflected state map is
Borel by splitting the closed set {h=0} and its complement. For fixed source
parameters, A_z(u) is jointly continuous on finite bounded time regions. The
inverse hazard is extended-Borel because, for a ≥ 0,

    {s(z,e) ≤ a} = {e ≤ A_z(a)}.

At e=0 this identity includes s=0; at an empty hit set it excludes every
finite a. The finite domain {s<∞} is Borel. Induction gives measurable finite
states, waits and accumulated times on the reached finite domain; using an
explicit terminated option is a standard representation. These bridges are
mathematically required if a candidate claims Borel finite-input recursion,
but A.1's first three paragraphs do not supply their full proof. They are
recorded as SOURCE_GAP/proof obligations to be discharged by concrete local
dependencies, never as new theorem assumptions. This source-only stage does
not certify joint law, global path-space measurability, Markov kernels, or
Markov/invariance statements.

## What remains OPEN

The independent Exp(1) law, iid composition, strong-law divergence of their
sum, almost-sure nonaccumulation, global path assembly and uniqueness,
memorylessness/time-homogeneous Markov property, Davis's hypotheses/theorem,
stationarity, reversal, operator/semigroup statements, half-turn kernel,
bounce/query costs and whole-paper actual-input composition are all OPEN here.
They must remain dependency obligations, not assumptions silently added to the
finite theorem. The retained A.1 source text discusses these later claims, so
their exclusion is explicit in `source-coverage76.json`.

This source-derived graph is independently reconstructed from RAW, but it has
not been certified by a second topology reviewer. Candidate comparison and
packet/run binding are still pending. No Lean/compiler result has been used
as source evidence.
