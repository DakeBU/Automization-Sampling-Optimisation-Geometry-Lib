# Phase 3: authored reader and source mapping, final-v1

Reviewer: `mgf_fresh_source_5b7e`.
Timing: after the independent source-only and whole-module reviews were frozen; before any decoder reconstruction, canonical seven-slot packet, earlier semantic/native verdict, or generated candidate reader was viewed.

## Decision

**Needs revision in the authored source mapping before this exact v1 is accepted as the final reader/source-map artifact.**

The mathematical statement, assumptions and six explanatory steps match the frozen P/T code and the original source at this bounded local layer. The complete code folds and their exact locators are correct. The requested revision concerns inaccurate or incomplete semantic source labels in the Gaussian part; it does not require changing production Lean or revising the source theorem.

Current input bytes are preserved in `originals/` without edits:

| Input | SHA-256 |
| --- | --- |
| Lesson final-v1 | `3b87747bc5af5829b1741cb2de9a344549afac04a78432878590b38945396536` |
| Publication final-v1 | `45f975c80d7eeff14d66ad45b7c19d3abafd9118633b3a2cca4afbd0dc8e3993` |
| Exact fold locators final-v1 | `5605d8092eb2e698892d16bcf4a5d623ec1aa36bce56e830afa9928f691537f7` |

The mathematical P/T commit remains `4869db55d340cee39f0ba4d49fb0a7a4309ba2d6`, with the phase-2 hashes unchanged.

## Required source-mapping correction

In `units[0].steps[3].source_attribution`, the exact spans are mechanically correct, but several roles describe content outside the spanned original element:

| JSON position (zero-based) | Current role | Content actually in that exact source span | Required treatment |
| --- | --- | --- | --- |
| `steps[3].source_attribution[0]`, Ex107 | `Original row construction` | Definition of the truncated **matrix** Y_i in terms of gamma_i and t_i. It does not define gamma_i or its law. | Rename to the truncated matrix formula; add the actual row/feature and row-law anchors. |
| `steps[3].source_attribution[3]`, Ex110 | `Original matrix construction` | The summed expected-matrix identities `sum EY_i=aI` and `sum cos(n theta_i)EY_i=0`. | Name these identities accurately, or omit this contextual entry if it is not needed for the step. |
| `steps[3].source_attribution[4]`, Ex111 | `Actual centering and matrix sequence` | Operator-norm bounds for Y_i and E Y_i. It does not contain `Z_i=Y_i-EY_i`. | Rename to the Y/mean norm bounds and add the actual centering paragraph. |

The lesson's public `sources` entry with URL `#A3.Ex107` also scopes a single Y_i formula as `Literal original probability law, rowwise inclusive cutoff and actual mean construction.` Ex107 supports the cutoff matrix formula, but does not itself contain the Gaussian product law or the actual Z centering definition. That scope should be narrowed and complemented with the actual original-source locations.

The following missing anchors support definitions explicitly used in the assumptions and private step 4. Their exact independently computed char/UTF8/line/hash locators are provided in `suggested-source-anchor-additions.json`:

- `A3.Ex85`: literal t_i and gamma_i definitions.
- `A3.SS2.p1.2`: independent N(0,I_r) row statement and B row construction. Together with the original independent g vectors, this is the source context for the actual experiment.
- `S4.E11` (or the explicit recall in C.2): exact theta_i midpoint grid.
- `A3.SS2.p10.1`: definitions of L and R_i, which are not inside Ex107-112.
- `A3.SS2.p13.1`: actual Z_i=Y_i-EY_i definition immediately before Ex111.
- `A3.SS2.p13.3`: original signed cosine norm-bound use immediately after Ex112; useful to make step 5's original use site exact.
- `A3.SS2.p12.4`: the individual expectation formula immediately before Ex110; useful if the source mean construction is explicitly labelled in the map.

These are source-mapping additions, not new mathematical dependency edges or proof-credit units. No need to expand the claimed completed scope to all those source results.

## Mathematical content check

All six authored steps were read with their full formulas, explanatory prose, exact code and source attribution. No mathematical correction was found:

1. **One-spectrum bounds:** A is explicitly self-adjoint in the prose, A<=I and s>0 imply `||exp(sA)||<=exp(s)`. The separate I+H<=exp(H) comparison is correctly restricted to self-adjoint H. No arbitrary-pair exponential monotonicity is asserted.
2. **True expectations and regularity:** continuity plus the cap supplies exponential integrability. X squared is the ordinary matrix square; its integrable PSD expectation, multiplied by g>=0, is the actual matrix C. No scalar proxy replaces it.
3. **Expectation MGF:** the deterministic quadratic majorant is an actual cited ASTIS dependency. Probability normalization and zero mean yield I+C, and two PSD differences are added to obtain the displayed full matrix inequality. The argument matches Tropp pp.25-26 and P88-119.
4. **Original private Gaussian application:** the law is the unconditional product of independent d-dimensional Gaussian columns. Row extraction, the inclusive cutoff, actual mean, positive rho and the norm triangle bound agree with T. The mean/radius/structure facts are genuine existing dependencies, rather than public assumptions of the Gaussian theorem.
5. **Signed cosine:** the proof uses absolute cosine in the norm, so negative w_i is correctly supported; it does not multiply a Loewner inequality by a negative weight. Hermitian structure and normalized norm bound give X_i<=I.
6. **Internal hypotheses and normalized conclusion:** measurability, mean zero, integrability and the bounded square are derived on the original measure. The result holds for every s>0 and i with the actual E(X_i squared). The reader clearly defines X_i=rho^-1 w_i Z_i, so the normalization is not silently omitted.

The assumptions preserve the source's real finite nonempty specialization, a.s. one-sided cap, genuine probability law, integrable X and matrix square, all positive s, q=0, literal closed cutoff, exact r^2 matrix carrier and deterministic signed cosine. The private theorem retains only hq as a caller premise. The publication statement and formula agree with P46-58, and the private statement in the fourth fold agrees with T21-53.

The title and statement correctly say real individual-matrix MGF. Boundary text explicitly excludes a sum-MGF, negative-global-cosine application, two-sided tail, complete matrix Bernstein, Fact C.6, Lemma 4.4, both main lower bounds, site delivery and purification. Tropp remains independently matching background rather than a fictitious citation supplied by the Gaussian authors.

## Exact code and source locators

`locator-checks.json` records 26 independently recomputed checks, all passing after applying each field's actual convention:

- Six `step.lean` strings equal the specified immutable Git byte slices.
- All six decoded-character, UTF8-byte, inclusive-LF-line and start/end line-column locators, file hashes and slice hashes match.
- The fold locator document exactly agrees with each lesson step's own locator.
- Concatenating the first three folds reproduces the complete 121-line P blob; concatenating the final three reproduces the complete 159-line T blob, with no omission or duplication.
- Public statement P46-58 and private statement T21-53 both match their exact character, byte and hash locators.
- Every supplied Gaussian source span contains the named original id and has the right source file hash, char/byte correspondence, slice hash and containing LF line range. These HTML element spans need not include the final line's newline byte; their line fields are containing-line ranges, whereas the Lean folds explicitly retain complete newline bytes.
- Tropp source PDF hashes match the original pinned source, and the claimed printed pages were independently read in phase 1. The referenced derived page-text hashes also match their files. PDF page locators correctly make no PDF byte-span claim.

Six folds and 280 covered lines are audit-coverage facts, not mathematical progress counts.

## Self-contained prose and optional cleanup

The mathematical proof can be followed from the complete statement, assumptions, formulas and named mathematical parents without reading the agent run. A few process references should be removed or rewritten for a cleaner final reader:

- Lesson `assumptions[2]` and publication `assumptions[2]` say that a `preproof target/binder/topology admission accepted` the standing-regularity expansion. Source justification is Tropp section 2.2, not an earlier agent admission. The reader can simply say these are the explicit measurability/integrability conditions used to make the indicated expectations genuine. I did not inspect or rely on the referred earlier admission.
- Publication `bindings[0].assumption_deltas[1].reason` likewise refers to the earlier review. Its actual mathematical explanation should lead; the earlier process claim is not source evidence.
- `canonical R13` in `dependency_notes` is an internal alias. The explicit full ASTIS dependency is already recorded, so using its mathematical name would be clearer for a reader without run context.

These prose items do not invalidate the mathematical formula; they are editorial recommendations in addition to the required source-map correction above.

## Runtime boundary

No generated page or browser was inspected in this phase. I read the relevant shared renderer source only to distinguish stored fields from actual rendering: the progressive renderer uses literal step Lean strings and does not consume the additional per-step own-source/download metadata. I did not run it, build the site, validate downloads or infer actual reader acceptance from metadata existence.

The metadata accurately records its runtime limitation. A later isolated candidate-overlay check must independently verify the actual displayed source actions, fold defaults, source/download routing, readability and delivered bytes. This review does not approve a shared renderer change or production-site integration.

No original final-v1 file, production source, shared site, ledger or frontier was modified. A versioned successor is required to close the source-mapping finding. Decoder and canonical seven-slot comparison remain pending.
