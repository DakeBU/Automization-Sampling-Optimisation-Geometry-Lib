# Prose round 9: two local L2 boundary exercises

- `sogb-033`: the antipodal two-point sphere has finite angular cost but
  no internal continuous path. Both Dirac transport problems have a
  feasible coupling; they differ by the cost evaluated at that pair.
- `sogb-034`: the second adjacent binary hybrid pair has ideal first
  history. Averaging its conditional error under the implemented history
  can fail for that pair even though the mistaken endpoint sum still
  bounds the endpoint in the example.

[Frozen input](packets/prose-input.json) and [independent source review](source-review.json). Both examples are original
public-dev prose, not independent held-out items. They reuse their
existing sphere and adaptive-hybrid families. No equivalent Lean
reconstruction is claimed.

The supporting Lean checks are reproducible with
`lake build Tests.SphereFeatureLawGradient Tests.KernelHybridTelescope`.
This checks existing library support and does not compile these prose
answers or count as independent editorial acceptance.
