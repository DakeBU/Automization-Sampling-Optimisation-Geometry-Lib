# Lower Bounds across libraries

The standalone `lower-bounds/index.html` is a thematic reader, independent of
the Log-Concave Sampling chapter spine. It is not a new book, proof registry,
Frontier Cell, SAU or scheduling Goal. Canonical source statements, full
formula proofs and folded Lean stay in their existing readers.

- **Optimisation §4** supplies the first-order oracle and hard-instance lens.
  The linked §3 quadratic sharpness example is a checked component for a
  specified method, not a substitute for a §4 oracle-complexity theorem.
- **Midpoint, arXiv:2610.06308v1 §§5–6** gives method-specific deterministic
  and randomized obstructions. Keep stationary bias, finite initialization
  and query accounting separate. Do not promote a bound for the named
  algorithms to a lower bound on every first-order sampler.
- **Gaussian Complexity, arXiv:2610.20492v1 §§2–4** compares two different
  information restrictions: determinant-sign indistinguishability and the
  fixed-spectrum hidden eigenbasis. Selected Lean results come from existing
  reviewed publication bindings, not paper titles or a hard-coded badge.

The reader reuses `concept:lower` and `transport:oracle-reduction` in the
Functor Hypergraph and the same declaration identities in the Lean graph. A
method comparison is a navigation aid. A genuine hardness transfer must
preserve instance and oracle classes, adaptivity/randomness, output
guarantee, budget semantics and simulation overhead. It needs its own typed
theorem before it can become a formal edge.

## Coordination snapshot (2026-11-09)

Audited official main `d9bcd423` and Huanjian Zhou's affinity branch
`5a257960`. [PR #380](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/380)
and the later main receipt retain literal evaluated Eq. 24, Proposition B.7
single-block TV separation and normalized actual mixture densities.
[PR #385](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/385)
has the normalized density TV–affinity theorem and actual Eq. 25 with
independent and root checks, but was open at this snapshot. Its selected
reader link appears automatically once the accepted binding is on the
built checkout. Do not copy that proof, edit its integration records or
claim its pending route.

The next Gaussian Complexity boundaries include the actual product law and
amplification, transcript/query-cap and expected-cost adapters, the
hidden-eigenbasis route and both main lower bounds. These are not
Gaussian Cloud §6. Leave them with the existing Gaussian Complexity lane;
recheck live branch/Cell/SAU ownership before scheduling any proposed
shared lemma. The four-paper order and all proof state remain unchanged.

When proof work resumes, compare the optimisation information argument to
the sampling consumer at the level of admissible queries, the observable
transcript and the output map. Look for an existing Lean interface first.
Extract a shared lemma only for a named, dependency-ready consumer; keep
paper-specific separation, initialization and cost conversions in their
own lanes. Midpoint's method-specific obstruction needs no Gaussian
Complexity query theorem unless an actual proof dependency is established.

## Maintenance

Edit [the reader projection](../website/scripts/lower_bounds.py), not
generated HTML. Add a selected reading by canonical publication item ID;
the projection checks its current reviewed binding and existing graph node.
Prefer source or chapter links when a full Lean certificate is still open.

```bash
python -m unittest tools.tests.test_lower_bounds tools.tests.test_samplewiki_navigation
python website/scripts/build_site.py
python website/scripts/check_site.py
```
