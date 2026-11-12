# Product coupling: independent paired review

The [blind input](packets/anonymous-input.json), [blind result](decoder.json),
[source-review input](packets/reviewer-input.json), and
[independent verdict](source-review.json) bind the accepted `sogb-041`
statement, Lean target, formula proof, provisional levels, and rubric. The
[coordinator map](packets/coordinator-map.json) is not decoder or agent input.

The [first verdict](preflight-v1/source-review.json) is preserved with its
own frozen inputs. It required confining the rectangle formula to the
probability setting and identifying Mathlib's inferred `SFinite ν` premise.
The final round uses new independent actors on the repaired explanation and
shorter display lines; the mathematical premises, target and rubric did not
change. Lean 4.33.0 independently compiled both the trusted reference and an
explicit proof using the two Mathlib identities without the ASTIS answer
available in its import environment.

This is an original public-development question in the existing coupling
family, not a numbered exercise, new registry declaration, or hidden
test. Formal alignment certifies the product-coupling conclusion only;
the normalization explanation and absence of an optimality claim remain
prose assessment. Difficulty, isolated native runtime acceptance and model
performance are separate.
