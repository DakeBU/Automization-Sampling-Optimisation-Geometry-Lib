# Independent midpoint/Lobatto conceptual review

**Verdict: ACCEPT_CONCEPTUAL_ONLY. Issue list: empty. No validation API has been called.**

Exact candidate: `midpoint-lobatto-conceptual-candidate.json`, SHA-256 `b928bd44a996aa9086d214aff8e1746bef3149f7e62f104e7a16092be61a03e7`, Discovery `ASTIS-DISC-20261109-MidpointLobattoCosineCancellation`. The reviewer is `/root/cosine_topology_challenge`, distinct from the root creator.

This review accepts a source/implementation-backed mathematical relation, with the candidate's stated failure boundaries. It does not certify a formal transport, source V, compilation, foreign original-source fidelity/completion, a proof-ledger transition or Goal/queue/model credit. All earlier grid/C7 reviews remain untouched.

## Read order and exact inputs

The pinned Gaussian raw paragraphs `A3.SS3.p3` and `A3.SS3.p6` were freshly read before the candidate. The former states the all-integer midpoint alias identity and both proof cases; the latter uses zero low-frequency constant mode, product-to-sum and the two shifted frequencies before its separate tail resummation. The source pin is the same 951991-byte HTML, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

The candidate was then opened and its four exact local input hashes/sizes independently matched. The two current midpoint files were read as implementation-side context; the named Lobatto C/sine_C/C_index/C_difference/C_sum/D/D_formula records, nearby cardinal construction and the public nonnegative_momentum_weights context were inspected directly. The exact publication metadata was read only for existing attribution/boundaries. No original SPHMC paper, foreign source audit/queue, compiler, provider, model or external source was invoked.

This is not zero-cue: the assignment already names the proposed relation and failure tests, and this actor retains its earlier C7/grid raw-source cognition. Implementation bodies read here are authorized conceptual evidence, not a new proof/source-V review.

## Formulas, hypotheses and mechanism

Use N for the Lobatto degree to avoid confusing it with the Gaussian consumer frequency n. With N=J−1≥1, the implementation's literal formula is

\[
C_N(t)=2\sum_{j=0}^N\cos(jt)-1-\cos(Nt)
=\cos0+2\sum_{j=1}^{N-1}\cos(jt)+\cos(Nt).
\]

Thus C_N(kπ/N) is the endpoint-weighted sampled-cosine functional with weights 1 at j=0,N and 2 in the interior. These sampling weights are not the eventual ordinary-Lebesgue momentum integrals b_j.

The midpoint functional instead has d equally weighted half-shifted angles θᵢ=(i+1/2)π/d, i=0,…,d−1, d≥2. Its exact public statement retains every k:ℤ, integer divisibility by 2d, negative integer quotient/zpow and the signed alias d(−1)^a at k=2ad. No κ or positive-frequency restriction belongs to this alias theorem. Its reciprocal-grid consumer separately uses κ≥2 and 1≤n<d.

The Lobatto `C_index` statement has degree N>0 and k:ℕ with k≤2N. It evaluates C_N(kπ/N) to 2N for k=0 or k=2N, and zero otherwise. This inspected helper is not an all-integer periodic-extension theorem. `C_difference` handles i,j≤N by a guarded sign split and evenness; `C_sum` handles i+j≤2N and isolates coincident endpoints. These formulas do not identify N with d or erase the two distinct index domains.

The sine-product mechanisms agree at the level claimed. Lobatto proves sin(t/2)C_N(t)=cos(t/2)sin(Nt), treating t=0,2π separately before division. The midpoint nonalias proof uses a sine-times-finite-cosine-sum identity, integer sine cancellation and a nonzero denominator; the multiple case evaluates the literal half-shifted grid. Both use finite harmonic cancellation with separately handled alias/endpoint cases. They have different functionals and different surviving aliases.

For the Lobatto pair kernel,

\[
D_N(a,b)=2\sum_{j=0}^N\cos(ja)\cos(jb)-1-\cos(Na)\cos(Nb),
\qquad 2D_N(a,b)=C_N(a-b)+C_N(a+b).
\]

This exactly matches the product-to-sum **mechanism**, including the factor 2, of the midpoint weighted consumer's two integer frequencies m−n and m+n. On Lobatto nodes the endpoint factor is 1/(2N), and the interior factor is 2/(2N); the nearby cardinal formula reflects that distinction. The public momentum theorem has J≥2 and h>0, nodes h/2[1−cos(iπ/(J−1))], actual Lagrange polynomials and nonnegative integrals against ordinary Lebesgue measure on [0,h]. It supplies no direct alias transfer to the Gaussian side.

## Refutation attempts and failure boundaries

- **Direct transport fails.** At the first alias, S_d(2d)/d=−1 while C_N(2N)/(2N)=+1. The permitted concrete comparison d=N=2 gives midpoint values −2 versus Lobatto endpoint-weighted value 4 before normalization. The candidate correctly retains this counterexample rather than claiming equivalence.
- **Endpoint corrections matter.** For N=2 at k=2, the weighted Lobatto sum is 1−2+1=0, while equal weights give 1−1+1=1. Dropping either correction in the literal C formula also changes its zero-frequency mass. The candidate's endpoint warning is substantive.
- **Mass factors differ.** S_d(0)=d and C_N(0)=2N, including N=1 where there are no interior nodes. A shared cancellation pattern cannot erase the d versus 2N normalization or the d versus N+1 node counts.
- **Cancellation is not pointwise positivity.** For example C_2(3π/4)=1−√2<0. Nothing in the candidate claims C_N(t)≥0 for all t; its explicit refusal to infer Clenshaw-Curtis momentum-weight positivity from midpoint aliasing is correct. The positivity construction also needs polynomial/cardinal, ordinary-integral moment and affine-scaling ingredients beyond sampled cancellation.
- **Ranges and signs are preserved.** The inspected Lobatto bounded-natural helper is not promoted to all k:ℤ. The midpoint half shift is responsible for alternating signed aliases and cannot be dropped. The private midpoint difference m−n is formed in Int; no natural truncation is licensed.
- **No Gaussian or continuous-average shortcut.** The relation does not identify deterministic spectral sums with Gaussian expectations, finish C8 tails, or replace discrete grids by continuous circle averaging. Finite aliases and r^(2d) corrections remain. There is no Poisson surface/circle adapter or TV/oracle/cost/main-bound transfer.

These attempts refute stronger transport claims but do not refute the candidate's deliberately weaker, typed conceptual family.

## Source/conclusion/status maps

The midpoint source map is supported directly by pinned p3/p6 and the literal Eq11 grid. The local all-integer theorem and private reciprocal-grid series are genuine implementation candidates for the two stated roles; this run does not recertify their compilation or pending source V.

The Lobatto formulas are ASTIS internal implementation facts. They are not attributed verbatim to the SPHMC author. The local module's existing attribution and supplied publication metadata provide a repository-provenance association with the SPHMC coefficient route. In particular, that publication file binds the separate coefficient theorem and still lists positivity as an independent remaining obligation there; it is not a new publication/source-audit certificate for the named positivity implementation. The candidate's explicit implementation-side scope and refusal to upgrade that foreign lane are therefore essential and are preserved by this ACCEPT.

The proposed future abstract sampling-functional lemma is a possible abstraction only. `formal_refs=[]`, `formal_transport_certificate=false` and overview/functor-only placement correctly prevent a compiled Lean implication, certified functor or foreign status change. No such model integration is performed.

## Freeze and next action

`input-manifest.json` pins the exact candidate, four local files, raw source fragments, selected formula extracts and preserved earlier freezes. `validation-plan.json` is a **non-executed** plan for one normal Discovery validation with a strict complete-ledger replay, exact candidate/review pins, current RAW/creator-independence checks, preservation of every foreign state and raw byte prefix, and protected file hashes. An explicit later execution instruction is required; this review does not read/mutate the live ledger or invoke that API.
