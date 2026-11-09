# Scoped cutoff publication handoff

This is an isolated publication candidate for the Lean modules already checked
at `d1082b0a2`. It does not register a Frontier Cell, change the mathematical
Registry, admit a Bench task or publish a page.

The [candidate](cutoff-publication-candidate-v3.json) separates the generic
three-limit prerequisite from the finite-dimensional compact-test extension.
It uses the same lesson renderer and publication binding as the live site.
The Gaussian successor points to the shared provider; the existing Gaussian
public theorem and proof are unchanged. The mathematical source of that
background is the use of Gaussian LSI in [SPHMC (4.6)](https://arxiv.org/html/2609.06906v1#S4.E6),
not a claim that the combined transport estimate is proved here.

The first extension candidate is preserved in commit `22f4daeac`. Its
independent source reviewer found a domain ambiguity: in the arbitrary-measure
formulation, compact smooth tests need not have integrable terms, whereas the
source uses a probability measure. For example, a measure assigning infinity
to every nonempty measurable set is not locally finite. The formal premise
uses Mathlib's totalized Bochner integrals on such measures; the particular
cutoff products in the proof do have integrable terms. Version 2 makes both
facts explicit. Its new independent reviewer also found that one shared
summary could be read as dropping the three analytic inputs from the cutoff
prerequisite, and that the density argument was not attributed clearly.
Version 3 repeats all three integrability conditions explicitly and identifies
the detailed cutoff construction as original ASTIS exposition. Neither
revision changes a Lean statement or an anonymous decoder packet.

`lake env lean Tests/Shared/LogSobolevCutoffDomain.lean` checks a concrete
instance: for the smooth compact cutoff at radius one and the Borel measure
`⊤ • dirac 0`, the squared function is not integrable although its totalized
Bochner integral is zero. This is an API-boundary regression, not a new
publication declaration or a counterexample on the stated integrable domain.

## Replay and integration boundaries

`python proof-obligations/chewi-exercise-1-7/check_exercise_publication_packets.py --batch cutoff`
rehydrates the exact packet-backed records from the evidence folder, checks the
decoder and reviewer pins, compares all bindings to current Lean and lesson
content, and smoke-tests the actual progressive lesson renderer. It also checks
the two preserved blocking extension reviews and the superseded cutoff review,
which never count as acceptance for version 3. The three current isolated
records (cutoff limits, compact extension, Gaussian successor) each passed
independent seven-slot source review as `equivalent-after-elaboration` with
no blocking delta. They are scoped to the authored mathematical statements.
This is not the canonical publication gate or a deployed browser check.

At stabilization, create the two correctly scoped new Frontier Cells and place
the reviewed records, lesson units and publication edges in the canonical
indices. Keep the prior Gaussian audit as historical evidence and bind the
existing Gaussian item to the exact reviewed successor. The private cutoff
implementation should be covered by its whole-module source review, not by
new public wrappers or additional mathematical credit. Run the complete diff,
registry, compiler, site and live-reader gates before calling the batch shipped.
The compact PI and actual-law KL results are separate bindings. Their local
mathematical reviews do not replace their own packet-bound publication reviews.
