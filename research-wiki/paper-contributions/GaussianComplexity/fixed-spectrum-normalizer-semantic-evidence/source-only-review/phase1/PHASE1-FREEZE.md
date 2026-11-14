# Phase 1 raw-first freeze

Frozen UTC: 2026-11-08T05:58:37.946136+00:00. Extractor: `/root/norm_source_graph_391602`.

Status: **source-only extraction; independent topology/coverage review pending**. No Lean/proof/source-fidelity acceptance or completion is claimed. The exact candidate statement and implementation remain unseen. Phase 2 comparison has not begun.

The pinned original is `On Complexity of Gaussian Sampling`, arXiv:2610.20492v1, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. The private archive is an exact byte copy; it has 951991 bytes, no CRLF line endings, and 4269 LF bytes. Public raw excerpts retain exact byte slices and offsets. Inspection text is derived and is not source evidence.

The source contract is the literal Eq.11 family for integer d≥2 and κ≥2: θ_i=(i−1/2)π/d, λ_i=(κ+1)/2+(κ−1)cosθ_i/2, Λ=diag(λ_i), A=OΛOᵀ, with every O∈O(d). Section2 supplies the unshifted quadratic and centered target N(0,A⁻¹).

C.4 is `A3.SS4`; its normalizer display is `A3.Ex160`. It states Z_A=(2π)^(d/2)(detA)^(−1/2)=(2π)^(d/2)(detΛ)^(−1/2), followed by independence of O and known value whenever the fixed spectrum is public. The selected source does **not** explicitly define Z_A by an integral or name its base measure. The actual unweighted Lebesgue integral ∫exp(−xᵀAx/2)dx, finite positive mass, diagonal determinant product, and positive real half-power conventions are explicit source-implicit consequences/bridges in this extraction, never fabricated source definitions.

Full C.4 coverage keeps admissibility, C∞/Hessian/strong-convexity/smoothness, zero value/coercivity/unique minimizer, Gaussian mass/value, determinant invariance, O-independence, and public-spectrum known value distinct. The Gaussian integration and determinant algebra are compressed in the paper and remain SOURCE_GAP nodes. Derived integrability, positivity and determinant identities are edges, not extra public premises.

Theorem4.1 and the whole Section4.4 are exhaustively inventoried for scope separation. Their δ/d/κ/ε ranges, Krylov dimensions, statistics, concentration thresholds, TV/query lower bounds and limitations do not become normalizer assumptions or conclusions. No precision/evaluation-cost or sampling-algorithm claim follows from “known”. The construction citation [22] is provenance only, not a cited Gaussian-integral theorem.

The inventory has 204 entries: 67 NODE dispositions and 137 explicit exclusions; the graph has 40 nodes, including 12 SOURCE_GAP nodes, and 17 use-site hyperedges. This count is a mechanical inventory, not self-approval of substantive coverage. The author supplies one compressed Gaussian-integration route; no alternative author proof has been invented. Optional product representation and collateral calculus remain separate branches rather than false AND premises.

Artifacts: `source-contract.json` contains all seven semantic slots; `source-proof-graph.json` contains use-site edges and conditional discharge; `coverage-inventory.json` contains every selected paragraph/display/theorem/formula/citation/reference disposition; `input-provenance.json` records input hashes, byte spans and exposures. `manifest.json` hashes every artifact and the exact archive; `manifest.sha256` seals the manifest.

**STOP: phase1 is frozen. Await the parent's phase2 input; do not read any candidate or implementation before this freeze is delivered.**
