# Independent source graph challenge, phase 3 v1

Identity: pre-proof topology/binder/definition challenger, distinct from source graph author and prover. This report uses my frozen phase-1 original-source notebook/inventory, exact sealed P/T signatures, and the separate author's frozen phase-1 graph/coverage. It does not use implementation imports, Lean proofs, API searches, old reviews, or the metadata author's explanation.

Reviewed graph: `.astis/semantic-neutral-20261114/weighted_mgf_source_graph_c4e8/phase1.source-graph.json`, SHA256 `9b44b4b4e8df137231aea575a6c148da01097002ce1afdea9961f42aa7de82fa`; coverage SHA256 `8b1f8a57df7b250b0d97d5907aed6772156aedbfdccbd15e62a5b4644ac34d82`; freeze-manifest SHA256 `5359a0d25a7307a0ed7c99cb98f6094e6903e38c747343c71385efacbbfd2702`.

Decision for **phase-1 graph as a complete P/T pre-proof gate: HOLD**. The exact P/T statements remain admitted. The HOLD is restricted to the source graph's missing exact-P root closure, several overbroad/insufficient dependencies and coverage mappings. These are not mathematical refutations and require no new public binders. The graph author has been sent the precise corrections and will retain the frozen original while producing a versioned successor.

## Every hyperedge

| Edge | Independent challenge / decision |
| --- | --- |
| E01 angle-basis-Gaussian → basis cap | The inequality only uses the deterministic basis formula, q>=0 and |cos|<=1. Consuming the Gaussian law or B is unnecessary. Split the source node or name the exact basis projection and parameter source. The conclusion itself is source-correct, including q=0. |
| E02 truncation + angle-basis-Gaussian → truncated Y | Correct literal Ex107 formula. A Gaussian law is unnecessary to define the matrix; it is used for the added independence claim. Label definition/context versus independent-sequence fact so source ordering is not mistaken for a necessary proof edge. |
| E03 truncated Y + Gaussian → radial mean | Source-correct at Ex108/p12.3–4. Radial symmetry, common law and E R_i=r supply actual mean and 0<=a<=1. Their internal expansion remains a proof obligation, not a caller premise or already compiled discharge. |
| E04 truncated Y + radial mean → centered Z definition | Overstates necessity. Z=Y-EY is defined using the actual integral whether or not the radial formula has been calculated. Split actual mean definition from radial computation; keep the latter as one route to the sharp mean norm cap. Do not force the radial computation into a false AND prerequisite of literal centering. |
| E05 basis cap + radial mean + truncated Y → raw caps | Correct source route for Ex111, consuming precisely 0<=a<=1 and the inclusive cutoff. Make d>0 and nonnegative cutoff/scale consequences of G.parameters explicit. This is the route where the radial mean calculation is useful; an alternate valid sharp expectation cap would be an authored OR-route, not the Gaussian author's printed proof. |
| E06 raw caps + centered definition → centered cap | Accepted: source Ex112 uses triangle inequality with both component bounds. R_* must stay 2r(L+1)/d, not a silently inflated bound. |
| E07 centered cap → weighted cap | Accepted: p13.3 uses the two-sided norm bound and absolute cosine bound. This handles negative cosines. Replacing it by signed multiplication of a one-sided Loewner cap would be invalid. |
| E08 fourth moment + square + C.5 → sum second moment | Correct source direction for Ex115–117, but consume only C.5's basis-norm and sum-basis projections. Add the derivation of G.square from literal Y and the two rank-one square identities stated in p14.2. Those identities are not covered by G.gaussian-fourth's current claim, despite p14.2 mapping there. This is deferred variance context, not a prerequisite for the actual-variance P/T MGF. |
| E09 centered Z + radial mean → centered variance | The Ex118 identity needs actual mean definition, integrability/expectation algebra, and self-adjointness (for mean-square PSD). Radial coefficient computation is not necessary. Record these actual ingredients explicitly, leaving radial mean on the sharp-cap route. |
| E10 centered variance → weighted variance | Accepted for E[(cZ)²]=c²E[Z²]<=E[Z²]. The node's added claim “same total variance bound” also requires G.total-variance. Either add the corresponding deferred edge or separate the local square identity from the total-variance claim. G.total-variance itself needs sum-second-moment + centered-variance, not an orphan assertion if presented as proved topology. |
| E11 functional calculus → transfer rule | Accepted source direction, original Eq2.1–2.2. The interval condition is required; generic P needs (-infinity,1], not [-1,1]. |
| E12 scalar f + monotonicity gap + transfer → spectral bound | Accepted mathematical direction. Add explicit source-hypothesis ports for self-adjoint X, hcap and s>0. They are source premises, not conclusions of the generic L67 theorem. The removable value f(0)=s²/2 and all negative eigenvalues must survive. |
| E13 spectral bound + matrix exp + functional calculus → quadratic envelope | Accepted with the recorded exact remainder identity and congruence. These are distinct ingredients; there is no entrywise exponential or ordinary multiplication-order argument. |
| E14 quadratic envelope + regularity → expectation bound | Needs explicit expectation-order mathematics, e.g. original Tropp Eq2.13 (p9 §2.7), plus probability normalization and actual EX=0. Expectation Loewner preservation is a mathematical ingredient, not merely the phrase “sufficient regularity.” Finite X and X² expectations are concrete source-standing regularity; exp(sX) integrability is internally discharged for s>0. |
| E15 expectation bound + I+A<=exp A → exp close | Accepted, correct direction. Establish actual E(X²) self-adjointness internally. This is Eq2.3 applied to one self-adjoint matrix, not operator monotonicity of exp or replacement by a variance cover. |
| E16 centered Z + weighted cap + Gaussian regularity/centering/normalization gaps → signed specialization | Legitimate pre-proof obligations, but exact source-domain and self-adjointness/positive-scale ancestry need explicit edges/ports. G.parameters is currently orphaned. Exact T is epsilon=+1 with signed cosine; epsilon=-1 is optional future two-sided-tail infrastructure. It must not become another required T target or an unnecessary AND. The normalized conclusion must map to the exact T signature. |
| E17 total context → C.6 boundary | Not a sufficient mathematical hyperedge as written: weighted cap, truncation-event probability, bias, threshold/union and constant simplification are omitted and bundled into one “not discharged” phrase. Since C.6 is out of target, convert this to an explicitly deferred non-entailment consumer record; otherwise introduce the actual missing source-gap nodes/routes before allowing C.6 as an output. |

## Exact-root and OR semantics

The phase-1 graph targets A.single-mgf, a later-authored actual Gaussian specialization. It has no explicit generic-P construction root: T.L67-exp-close is not connected to the generic theorem root T.L67-statement/P. For this task P is itself the theorem to be constructed. It cannot be proved by the black-box L67 statement it is intended to formalize. The source expansion must close the generic P root; T may then consume the established P through its concrete adapter.

The graph correctly discloses that the stated-L67 and expanded-L67 views are the same Tropp proof at different granularity, not independent discoveries. Keep that disclosure. A black-box already-proved generic theorem is a legitimate reuse route for T; it is not a second independent proof of P. Do not flatten expansion and reuse into one conjunction, and do not count them as two source authors or two independent proofs.

## Coverage challenge from raw source

I compared all raw C.2 regions to the author's coverage records. No substantive C.2 paragraph or numbered display was absent from the inventory. My inventory additionally records the two theorem wrapper containers, whose statements are already individually covered by the author's statement paragraphs/displays; the author's six extra heading records are harmless explicit exclusions. These set differences are not mathematics or completion percentages.

Two substantive mapping repairs are needed:

1. `A3.SS2.p15.2` asserts that **the same tail bound holds for the weighted sum**. The coverage points it to G.sequence-properties, which only claims independent/centered/self-adjoint sequences at p15.1. Point it instead to an explicit deferred weighted-tail consumer or GAP.uncited-bernstein with that actual weighted claim.
2. `A3.SS2.p14.2` contains both the Gaussian fourth-moment calculation and the two rank-one-square identities used by Ex114. Its sole mapping to G.gaussian-fourth does not cover the latter identities. Expand G.square's claim/anchors or add a square-algebra node and dependency from Y.

The explicit exclusions Ex122–132 and the p16–19 paragraphs are appropriate for a P/T-only scope: they preserve the real later threshold, union, on-truncation equality, bias transfer, absolute-constant simplification and Krylov-space consumers without pretending they are closed. C.5 range/cosine orthogonality is likewise not needed by a single fixed-index MGF beyond the stated deterministic basis norm. The graph must keep its bounded scope after correction.

## Source gaps and provenance

The named gaps T.L67-scalar, Gaussian regularity, actual centering and cap normalization are legitimate obligations that must remain internal to proof construction; no gap is permission to add a target hypothesis. In particular exp(theta X) integrability from **one-sided** cap is valid for theta>0, not for every real theta as the P.regularity port currently says. Gaussian T has a separate two-sided bounded route and can support more parameters, but the generic assertion must retain its positive domain.

Gaussian C.2 invokes unnamed two-sided bounded matrix Bernstein. The Tropp paper is independently selected background and is not a citation supplied by the Gaussian paper. This attribution is correctly explicit. Source graph author and challenger are distinct; neither is the proving worker. No graph counts are used here as evidence of mathematical novelty, sufficiency, proof, or completion.

Final state of this v1 report: exact P/T signatures admitted; frozen phase-1 graph **HOLD for versioned topology/coverage correction only**. This report does not authorize proof-search start until ROOT has the corrected graph and a fresh explicit independent admission of that successor.
