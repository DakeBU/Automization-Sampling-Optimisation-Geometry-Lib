# Ex72 actual averaged Gaussian-target TV: independent raw expectations v1

Status: `RAW_EXPECTATIONS_FROZEN`. Authored 2026-11-07 05:11 UTC by the distinct
raw-first topology challenger `/root/ex72_topology_challenge`.

This is source-only preproof preparation attached to the existing work. It is
not a new SAU, proof route, theorem-completion claim, Statement Seal approval,
sourcegraph approval, or final root-closure verdict. No exact seal or proposed
sourcegraph has yet been supplied to this reviewer. Those later artifacts must
be compared against these prior expectations; any correction to this freeze
must be a separately identified successor, retaining these bytes.

## Provenance and independence boundary

- Pinned source: *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1.
- Raw local source: `.astis/huanjian-resume-20261103/2610.20492v1.html`.
- Verified raw SHA-256:
  `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
- Primary target: `A2.Ex72`, within Appendix B.2.3, ending the proof of
  Lemma B.5 / Lemma 3.3 (`A2.E14`, `S3.E8`).
- Raw regions actually read: Section 2; Section 3.1 (`S3.E4`–`S3.E6` and its
  standing setup); Section 3.2; all of `A2.SS2` (B.2.1–B.2.3, including B.6,
  B.7, and every displayed/unnamed proof step); Appendix A.1; Appendix B.3;
  and the raw bibliography item `bib.bib24` used by A.1.
- Protocols read: root `AGENTS.md`, `docs/proof-digestion-protocol.md`,
  `docs/evidence-routed-memory-protocol.md`, and the repository source-dependency
  audit / semantic-roundtrip skill instructions. No nested applicable AGENTS
  file was present in the owned staging ancestry.
- Source was inspected directly from the pinned HTML. A read-only Python
  standard-library HTML parser replaced each `math` element by its `alttext`
  when displaying the raw regions, preserving source IDs. The initial optional
  BeautifulSoup import was unavailable; no dependency was installed and no
  mathematical conclusion was drawn from that environment failure.
- No implementation Lean, prior audit content, old or proposed sourcegraph,
  Statement Seal, reviewer verdict, or extractor private rationale was read.
  A broad instruction-file discovery returned some historical path names; no
  historical evidence contents were opened. No implementation-derived topology
  informed this document.
- This reviewer has written only this new owned staging directory. The root's
  later byte-exact canonical archival/path mapping is separate from this freeze.

## Seven semantic slots frozen before any seal/graph access

### 1. Objects

The conclusion concerns the **actual averaged target probability laws** from
the determinant-sign construction, not freely supplied densities or a scalar
surrogate bearing a TV-like name.

For an orthogonal matrix $O\in O(n)$, the precision matrix is exactly

\[
A_O=\frac{\kappa+1}{2}I_n-\frac{\kappa-1}{4}(O+O^\top).
\]

For $b\in\{-1,+1\}$, $\mu_{n,b}$ is Haar probability on $O(n)$
conditioned on determinant sign $b$. The single-block mixture is

\[
P_b=\mathbb E_{O\sim\mu_{n,b}}[N(0,A_O^{-1})].
\]

The $k$ matrices $O_1,\ldots,O_k$ are independent under the same fixed
sign $b$. Set

\[
A_{\boldsymbol O}
=\operatorname{diag}(A_{O_1},\ldots,A_{O_k},I_{d-kn}),
\quad
\mathcal D_b=\mathcal L(A_{\boldsymbol O}),
\quad
\pi_A=N(0,A^{-1}),
\]

\[
\bar\pi_b
=\mathbb E_{A\sim\mathcal D_b}[\pi_A]
=P_b^{\otimes k}\otimes N(0,I_{d-kn}).
\]

The final factor/identity block is omitted when $kn=d$. These are the
source objects in `S3.E4`–`S3.E6`, with target semantics from Section 2.

`A2.SS2.p2.1` fixes $p_O$ as a density of the actual
$N(0,A_O^{-1})$ and $p_b$ as a density of the actual $P_b$.
`A2.SS2.SSS3.p3.1` fixes $\bar p_b$ as a density of the actual
$\bar\pi_b$. The affinity is exactly

\[
a=\int_{\mathbb R^n}\sqrt{p_{+1}(x)p_{-1}(x)}\,dx.
\]

All measure/density identifications need actual semantic bridges. Choosing a
Radon–Nikodym or almost-everywhere representative may be legitimate only with
the audited equivalence and representative independence made explicit.

### 2. Domains

The source setup has integer dimensions $d,n$, with

\[
3\le n\le d,\qquad \kappa\in\mathbb R,\quad\kappa\ge4,
\qquad k=\lfloor d/n\rfloor.
\]

In particular $d\ge1$, $n>0$, $k\ge1$. Write the residual dimension as
$m=d-kn$, so $0\le m<n$. The actual sample space is the Euclidean Borel
space $\mathbb R^d$, with the block product coordinates
$(\mathbb R^n)^k\times\mathbb R^m$, and Lebesgue measure for the displayed
density integrals. Keep separate the two source cases:

1. $kn<d$: $m>0$, with the normalized standard Gaussian factor
   $\varphi_m$ on $\mathbb R^m$.
2. $kn=d$: no residual Gaussian factor; the source explicitly omits it.

A zero-dimensional representation may implement the second case only after an
audited equivalence to omission. Do not silently discard that case or add
$kn<d$ as a premise. A generic library statement with a wider valid domain
can be an ingredient, but cannot silently replace this source-facing domain.

### 3. Quantifiers and order

For every admissible $d,n,\kappa$, $k$ is **determined** by
$\lfloor d/n\rfloor$; the construction determines the two signs' priors and
the two averaged laws. The conclusion compares those two laws for the same
parameters. The sign $b$ indexes the construction; it is not an additional
random sign averaged out in the target conclusion. The blocks are independent
conditional on the common fixed sign, not independently assigned signs.

There is no algorithm, stopping time, transcript, query budget $T$, accuracy
$\varepsilon$, free choice of a density pair, or free block count quantified
in the Ex72 target. The later choice $n=2T+1$ belongs to application to the
main theorem, not to the separation theorem's premise list. Natural-number
division can represent the floor only with $n>0$ and the dimension arithmetic
linked explicitly to the source convention.

### 4. Assumptions and their classification

Source/standing assumptions are the source domain above, the Euclidean/Haar
setup, the literal precision construction, and the definitions of the actual
Gaussian mixtures. Pure carrier/Borel/finite-dimensional information is typing
context. No human-approved source repair is assumed in this freeze.

The following are **proof ingredients to derive internally**, not new public
premises: precision symmetry/positive definiteness/spectral bounds; existence
and measurability of the Gaussian and mixture laws; density witnesses or RN
identities; nonnegativity; probability normalization; integrability and L1
membership; product-law/product-density factorization; the Ex71 affinity
identity; the quantitative B.7 TV bound; the TV–affinity inequality; Eq. (25);
the TV overlap identity; or the pointwise/integral min–square-root comparison.

Reject a source-facing theorem whose binder expansion assumes any of those
conclusions, including a bundled `Prop`/structure/typeclass that hides them.
The existence of a separate producer theorem does not permit passing its
conclusion as an extra source hypothesis. A producer must appear as an applied
dependency inside the actual target proof. This applies equally to a proposed
"actual-law bridge" or "Gaussian target" interface.

### 5. Conclusion, with every coefficient and exponent

The exact Ex72 source chain is

\[
\begin{aligned}
\operatorname{TV}(\bar\pi_{+1},\bar\pi_{-1})
&=1-\int_{\mathbb R^d}
       \min\{\bar p_{+1}(x),\bar p_{-1}(x)\}\,dx\\
&\ge1-\int_{\mathbb R^d}
       \sqrt{\bar p_{+1}(x)\bar p_{-1}(x)}\,dx\\
&=1-a^k\\
&\ge1-\exp\!\left\{-\frac{k}{8}
                  e^{-10n/\sqrt\kappa}\right\}.
\end{aligned}
\]

The final bound is the statement of Lemma 3.3/B.5 (`S3.E8`, `A2.E14`).
If the eventual sealed declaration states only the final inequality, the
preceding equalities/inequality remain source-proof obligations rather than
disappearing from its topology. Do not change $k$ to $d/n$, replace the
floor using an auxiliary lower estimate, lose the outer subtraction from one,
halve/double TV, or change $1/8$, $10$, or the nesting of the exponential.

### 6. Scopes, senses, and conventions

Section 2 (`S2.Ex2`) defines

\[
\operatorname{TV}(P,Q)
=\sup_{B\text{ measurable}}|P(B)-Q(B)|
=\frac12\int|p-q|\,d\lambda
\]

for probability measures and any common dominating measure $\lambda$.
Use this exact normalization. An unnormalized total-variation norm, a density
L1 quantity without the factor $1/2$, an opaque real function, or an
affinity-defined surrogate is not automatically the source TV.

For the displayed Ex72 density integrals, $\lambda$ is Euclidean Lebesgue
measure, not the Gaussian law. The source's densities are nonnegative and have
mass one. Their identities may be proved a.e.; the final measure statement
and each integral must be invariant under admissible density representatives.
Any ENNReal/real or extended-integral conversion needs its finiteness and
measurability bridge. The bound is deterministic in $d,n,\kappa$ after
averaging the target over the matrix prior; it is not an algorithm's random
output TV, a high-probability event, a statement for every fixed matrix, or
the TV between the matrix priors themselves.

### 7. Constant dependencies

Every displayed number is fixed and universal. The bound depends only on the
source parameters through $k=\lfloor d/n\rfloor$ and
$e^{-10n/\sqrt\kappa}$. There is no hidden dimension/sign/algorithm constant
or unrecorded asymptotic qualification.

The relevant exact upstream quantitative chain is

\[
\begin{aligned}
\operatorname{TV}(P_{+1},P_{-1})
&\ge
\frac{\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^n}
 {2+\frac{4n\sqrt\kappa}{(\sqrt\kappa+1)^2}}\\
&\ge\frac12e^{-5n/\sqrt\kappa},
\end{aligned}
\]

\[
0\le a\le1,
\qquad
\operatorname{TV}(P_{+1},P_{-1})\le\sqrt{1-a^2},
\]

\[
a\le\sqrt{1-\frac14e^{-10n/\sqrt\kappa}}
\le\exp\!\left\{-\frac18e^{-10n/\sqrt\kappa}\right\}.
\]

Thus the $1/4$ and exponent $10$ come from squaring the B.7 lower bound,
and $1/8$ from the square-root/exponential step. All of those constants and
their positivity/range discharges must survive the later topology audit.

## Authored proof and root-closure expectations

This section predicts what a faithful **source** proof graph needs. It is not
an examination or approval of any graph artifact. Source edges must name their
consumer use sites; merely listing the right theorem names is insufficient.

### Immediate Ex72 spine

1. Start with the actual $\bar\pi_{\pm1}$ and their common-Lebesgue density
   witnesses. Establish that both are probability measures with mass-one,
   nonnegative integrable densities.
2. Apply the Section 2 normalized TV identity to those actual laws. The
   algebraic identity
   $2\min(u,v)=u+v-|u-v|$, together with normalization, yields
   $\operatorname{TV}=1-\int\min$. This is an indispensable bridge behind
   Ex72's first equality, even though the source leaves its expansion implicit.
3. Prove/apply $\min(u,v)\le\sqrt{uv}$ for $u,v\ge0$, and justify
   comparison of the integrals. Subtracting from one reverses the inequality
   as required. The affinity integral is finite, so this is a real inequality.
4. Consume the **actual** Ex71 identity at Ex72's third line, giving $1-a^k$.
   Its root closure must retain the Ex70 actual-law density factorization,
   Tonelli, normalization of the residual Gaussian when present, and both
   residual cases.
5. Consume Eq. (25) at Ex72's last line (`A2.SS2.SSS3.p3.4`). Use $a\ge0$
   and natural $k$ to raise the scalar bound to the $k$-th power, and use
   the exact exponential-power identity to obtain
   $a^k\le\exp\{-k e^{-10n/\sqrt\kappa}/8\}$. Do not assume the powered
   inequality as a public premise or introduce a different $k$.

Unlike an isolated Ex71 tensorization theorem, this root **does require** the
quantitative single-block separation: Eq. (25) is explicitly invoked by the
author, and B.7 is explicitly invoked to prove Eq. (25).

### Affinity and actual-law branch

| Raw region / item | Expected obligation and consumer |
| --- | --- |
| Section 2 targets; `S3.SS1.p1.1`, `S3.E4`–`S3.E6`, `S3.SS1.p2.1`–`p3.2` | Literal construction, fixed common sign, independent blocks, actual averaged target equality, floor block count, residual omission; consumed by all density/affinity identities. |
| `A2.SS2.p2.1` | Actual meanings of $p_O,p_b$; source domain $n\ge3,\kappa\ge4$; not arbitrary supplied functions. |
| `A2.SS2.SSS3.p1.1` | Independent-block mechanism and the quantitative-to-affinity amplification architecture; substantive proof paragraph. |
| `A2.Ex68`, `A2.SS2.SSS3.p2.2`, `A2.Ex69` | Exact definition of $a$, density masses one, $0\le a\le1$, and Cauchy–Schwarz derivation of $\operatorname{TV}(P_+,P_-)\le\sqrt{1-a^2}$; consumed by Eq. (25). |
| `A2.SS2.SSS3.p2.3`–`p2.4`, `A2.E25` | B.7 + Ex69, then $\log(1-t)\le-t$ for $0\le t<1$; range/nonnegative-root/squaring discharges must be visible. |
| `A2.SS2.SSS3.p3.1`, `A2.Ex70` | Actual $\bar p_b$ factors as $\prod_jp_b(x_j)\varphi_m(z)$ under Eq. (6); justify actual density equality and product-coordinate reference measure. |
| `A2.SS2.SSS3.p3.2`, `A2.Ex71` | Tonelli, nonnegative square-root factorization, repeated product integration, and $\int\varphi_m=1$, yielding $a^k$. |
| `A2.SS2.SSS3.p3.3` | Explicit $kn=d$ case with omitted Gaussian factor, plus the pointwise min–square-root comparison used by Ex72. Do not exclude the entire paragraph as tensorization commentary. |
| `S2.Ex2`, `A2.Ex72`, `A2.SS2.SSS3.p3.4` | Normalized actual TV / overlap identity, affinity comparison, Ex71 substitution, Eq. (25) powered bound; the final target root. |
| `S3.SS2.SSS0.Px3.p1.1`, `A2.Ex73`, `A2.E26` and relevant B.3 paragraphs | Source-supplied precision symmetry and spectral positivity give legitimate Gaussian targets and the domination used upstream. These may be proved earlier or locally; do not turn positive definiteness into an extra target assumption. The separate unique-minimizer conclusion is not needed for Ex72. |

### Quantitative B.7 branch now required in root closure

| Raw region / item | Expected obligation and consumer |
| --- | --- |
| `A2.SS2.SSS2.p1.1`–`p2.1`, Proposition B.7 / `A2.E19` | Exact two-stage lower bound, under $n\ge3,\kappa\ge4$; consumed by Eq. (25). The radial-test / spherical-integral mechanism is substantive, not optional commentary. |
| `A2.Ex56`–`A2.Ex57`, `A2.E20`, `A2.SS2.SSS2.p3.1`–`p3.4` | Define $h_\lambda=e^{-\lambda\|x\|^2}$, $\lambda\ge0$, and $H(\lambda)$. Haar component mass $1/2$ gives $H=\tfrac12(\mathbb E_{P_+}h_\lambda-\mathbb E_{P_-}h_\lambda)$; bounded-test TV gives $\operatorname{TV}\ge2\lvert H\rvert$. Preserve both factors of two. |
| `A2.Ex58`–`A2.Ex60`, `A2.SS2.SSS2.p4.1`–`p4.4` | Conjugation invariance and Gaussian covariance of densities permit radialization. Precision bounds give the displayed integrable Gaussian domination; $\lvert\det O\rvert=1$, Fubini, and Gaussian integration compute $H$. The denominator is at least $2+4\lambda$, discharging B.6's Borel/integrability premise at the application. |
| `A2.E21`, `A2.SS2.SSS2.p4.4`–`p4.5` | Apply B.6 to the reciprocal-power denominator, then identify $Oe_1$ as uniform on the sphere so Lemma A.1 applies to $U=O_{11}$. These are actual use sites. |
| `A2.SS2.SSS2.p5.4`–`p5.5`, `A2.E22`–`A2.E23` | Explain $H(0)=0$ by mass one; choose $r=(1-1/n)(\sqrt\kappa-1)/(\sqrt\kappa+1)$ and the exact displayed $\lambda=[4n\sqrt\kappa+(\sqrt\kappa-1)^2]/[8n(n-1)]$. Show $0<r<1$, $\lambda>0$, and both exact denominator factorizations before using Poisson identities. |
| `A2.Ex61`, `A2.E24`, `A2.SS2.SSS2.p5.6`–`p5.7` | Both Poisson identities are used to reduce the numerator integral. Substitute to obtain $H(\lambda)=(-1)^n n^{-1}[(\sqrt\kappa-1)/(\sqrt\kappa+1)]^n(1-1/n)^{n/2}/(1-r^2)$. The sign disappears only when taking $\lvert H\rvert$. |
| `A2.Ex62`–`A2.Ex64`, `A2.SS2.SSS2.p6.1`–`p6.4` | Convexity gives $(1-1/n)^{n/2}\ge1/2$. The exact $n(1-r^2)$ bound, E20 and E24 prove the rational first B.7 bound; these unnamed bookkeeping estimates cannot be silently omitted. |
| `A2.Ex65`–`A2.Ex67`, `A2.SS2.SSS2.p6.4`–`p6.6` | Log-ratio estimate $\le3/\sqrt\kappa$, hence numerator $\ge e^{-3n/\sqrt\kappa}$, and denominator $\le2e^{2n/\sqrt\kappa}$, yield $\tfrac12e^{-5n/\sqrt\kappa}$. Retain the $\kappa\ge4$ use and the $3+2=5$ exponent accounting. |

### B.6 / spherical-citation ancestors of B.7

B.6 (`A2.E15`) must remain the exact cancellation identity, for Borel $h$
with $\mathbb E|h(U)|<\infty$:

\[
\mathbb E[\det(O)\sqrt{\det A_O}\,h(U)]
=\frac{(-1)^{n-1}(\sqrt\kappa-1)^{n-1}}{2^n}
 \mathbb E[((\sqrt\kappa+1)U-(\sqrt\kappa-1))h(U)].
\]

Expected source ancestors and use sites are:

- `A2.SS2.SSS1.p1.1`: component-average difference and normalization-factor
  cancellation motivation; its relevant mathematical content must be covered.
- `A2.E16`, `A2.Ex52`, `A2.SS2.SSS1.p2.2`–`p2.4`, `A2.E17`:
  Gram factorization; lower norm bound throughout the interpolation interval;
  invertibility; determinant positive at zero and hence positive throughout by
  continuity; exact square-root/determinant identity. Merely using
  $\sqrt{\det(B^\top B)}=\det B$ without determinant-sign discharge fails.
- `A2.E18`, `A2.SS2.SSS1.p2.5`–`p2.6`: multiply by $O^\top$, use
  $\det O^\top=\det O$, and transpose to obtain the signed determinant form.
- `A2.Ex53`–`A2.Ex55`, `A2.SS2.SSS1.p3.1`–`p3.3`: principal-minor
  expansion, empty minor convention, row reflection preserving Haar and $U$,
  sign reversal for any minor containing an index $i\ge2$, integrability from
  $|\det O_{S,S}|\le1$, cancellation, and the two surviving minors.
- Lemma A.1 / `A1.E12`, `A1.SS1.p1.1`, `A1.SS1.p2.1`–`p2.2`,
  `A1.Ex31`: normalized surface measure; the Poisson representation formula
  applied at $re_1$ to both harmonic functions $1$ and $x\mapsto x_1$;
  the distance identity and division by $1-r^2>0$. The source has an awkward
  statement containing both “$n\ge2$” and “where $n\ge3$”; retain that raw
  fact, with no silent repair. The B.7/Ex72 use has $n\ge3$, so its use site
  satisfies both displayed dimension restrictions.
- The external citation `[5, Theorem 1.21]` at
  `A1.SS1.p2.1.1`, linked to `bib.bib24` (*Harmonic function theory*), is a
  real external source input, not an internal theorem proved by the paper.
  This freeze has read the citation as present in the pinned source, not
  independently certified that external text. A graph must preserve the
  citation/conditional analytic hypotheses rather than label it a locally
  compiled theorem without separate evidence.

At the B.7 use site the two required spherical identities are exactly

\[
\mathbb E[(1+r^2-2rU)^{-n/2}]=\frac1{1-r^2},
\qquad
\mathbb E[U(1+r^2-2rU)^{-n/2}]=\frac r{1-r^2},
\]

where \(U\) is the first coordinate under uniform sphere probability and
\(0<r<1\). They share that same expectation law and parameter.

The two Poisson identities and the determinant-cancellation result are genuine
AND ingredients of the author's selected B.7 route. A different formally proved
route may be recorded separately as an OR-route; it cannot rewrite the author's
source topology or flatten optional routes into a false AND.

## Hidden bridge challenges for the later exact-seal/graph review

The following must have an explicit producer/application, or a visible named
source-gap if absent. They must never be discharged by a theorem-shaped binder.

1. **Actual law and density:** measurability of the precision/inverse map and
   Gaussian kernel; mixture measures; identification of the Gaussian/mixture
   density with the actual $P_b$ and $\bar\pi_b$; the Eq. (6) average-law
   product identity. An arbitrary normalized product density is insufficient.
2. **RN/a.e. semantics:** common dominating measure, absolute continuity,
   nonnegative a.e. density witnesses, legitimate real-valued representatives,
   and representative independence of sqrt, min, absolute difference and all
   integrals. Avoid treating a raw RN derivative as pointwise continuous or
   everywhere finite without proof.
3. **L1 and normalization:** Gaussian density mass one, mixture mass one,
   product mass one, finite/integrable absolute difference, overlap and affinity.
   Fubini for signed $H$ requires domination; Tonelli for nonnegative
   affinity requires measurability. These are distinct uses, not interchangeable.
4. **Product coordinates:** the Euclidean block decomposition with residual
   dimension, its product Lebesgue reference measure, and compatibility of
   Gaussian measures/densities with that decomposition. Both residual cases
   must feed the same Ex71 conclusion and then the Ex72 root.
5. **Actual TV:** Section 2's measurable-event supremum must be identified with
   half L1 for the actual laws. Normalization must then justify
   $1-\int\min$. No factor-two change, definition-by-desired-bound, or scalar
   replacement for the probability-distance object is accepted by this freeze.
6. **Min and sqrt:** positivity hypotheses are proved for the chosen density
   representatives/a.e. classes, the pointwise inequality is justified, and
   integral monotonicity plus subtraction has the correct direction.
7. **Quantitative closure:** B.7 actually supplies the single-block TV lower
   bound; Ex69 actually supplies the matching upper bound; nonnegative roots,
   squaring and the $0\le t<1$ range in Eq. (25) are discharged; the natural
   power and exponential identities preserve $k/8$ and exponent $10$.

## Explicit exclusions and downstream boundaries

- Main determinant-sign oracle simulation, adaptive posterior/transcript
  indistinguishability, randomized-algorithm seed averaging, and query lower
  bound application (`A2.SS1`, the indistinguishability lemma, and the main
  theorem budget argument) are **not** ancestors of the target-mixture
  separation proof merely because they share the same family. Their eventual
  combination is downstream. Do not create a false AND from the two branches.
- Section 2's algorithm model, accuracy $\varepsilon$, and uniform sampler
  guarantee are not Ex72 assumptions. Precision/TV application and the later
  $n=2T+1$ choice remain downstream with their own domain checks.
- The source query budget is a deterministic cap for every admissible input
  and every seed. An expected-cost adapter is a separate mathematical boundary;
  Ex72 does not prove it or permit silently replacing the cap by an expectation.
- The fixed-spectrum hidden-eigenbasis construction and its lower bounds are
  a separate source route. Ex72 concerns the determinant-sign hard family and
  does not certify the eigenbasis route.
- Full B.8's unique minimizer/minimum-value conclusion is unnecessary for
  Ex72; the precision spectral bounds are relevant to actual Gaussian validity
  and the domination used in B.7. A future graph can exclude the minimizer
  claim with that precise reason without excluding the needed spectral input.
- Restatement headers, section introductions and terminal proof symbols may be
  explicitly excluded as non-substantive or mapped as statement aliases.
  Substantive prose, unnamed estimates, normalization, residual-case sentences
  and external citations may not disappear under such an exclusion.
- No novelty, Lean truth, axiom cleanliness, compilation, semantic-roundtrip
  acceptance, finalgraph acceptance, publication, or whole-paper completion is
  asserted here.

## Deferred review contract

Only after the root supplies the exact Statement Seal and independently authored
sourcegraph may this reviewer compare them with this freeze. The later review
must bind their exact paths/hashes, expand the seal's meaning-carrying project
definitions/binders, trace the complete actual Ex72 root backward through both
the Ex71/product-law branch and Eq. (25)/B.7 branch, and classify each omission
or mismatch. It must preserve the independence boundary against implementation
Lean, prior reviewer conclusions, and extractor private rationale. Until then,
the disposition is **raw expectations frozen; finalgraph verdict withheld**.
