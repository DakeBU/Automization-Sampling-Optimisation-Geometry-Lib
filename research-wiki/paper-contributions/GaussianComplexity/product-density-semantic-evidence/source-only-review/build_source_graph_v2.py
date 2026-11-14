"""Explicit source-closure repairs to frozen v1 after independent challenge.

Reads only this review packet. It never opens mathematical implementation Lean.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
v1_path = OUT / "source-proof-graph.freeze.json"
inventory_path = OUT / "raw-source-inventory.freeze.json"
g = json.loads(v1_path.read_text())
inventory = json.loads(inventory_path.read_text())
g["schema"] = "source-only-proof-graph-v2"
g["revision"] = "gc-actual-ex70-source-topology-v2"
g["supersedes_graph_sha256"] = sha256(v1_path.read_bytes()).hexdigest()
g["frozen_source_expectations_unchanged"] = True
g["source_topology_repair_provenance"] = "Distinct raw-source topology challenge identified omitted explicit context edges, floor/divmod guard discharge, and pre-product actual density identification bridges. v1 remains byte-identical. No implementation proof read."
g["status"] = "REVISED_EXTRACTOR_GRAPH_REQUIRES_DISTINCT_TOPOLOGY_REVIEW"
g["construction_inputs"].append("independent topology challenge; exact seal used only for definition/binder audit, never author-proof attribution")

nodes = [
    {"id": "bridge:floor-divmod-accounting", "kind": "SOURCE_GAP", "gap_type": "source-omitted-bookkeeping", "source_anchors": ["S3.SS1.p1.1"], "meaning": "For natural d,n with 3<=n<=d, let k=floor(d/n) and r=d-kn. Then k>=1, k*n<=d, d=k*n+(d%n), d%n=d-k*n=r.", "not_author_written": True, "not_public_binder": True},
    {"id": "bridge:residual-case-exhaustion", "kind": "SOURCE_GAP", "gap_type": "source-omitted-bookkeeping", "source_anchors": ["S3.SS1.p3.2", "A2.SS2.SSS3.p3.1", "A2.SS2.SSS3.p3.3"], "meaning": "From k*n<=d and r=d-k*n, exactly one of (k*n<d and r>0) or (k*n=d and r=0) holds. No k*n>d case remains.", "not_author_written": True, "not_public_binder": True},
    {"id": "bridge:conditioned-Haar-probability", "kind": "SOURCE_GAP", "gap_type": "source-implied-measure-identification", "source_anchors": ["S2.p2.1", "S3.SS1.p2.1"], "meaning": "For either source sign b, the actual conditioned law mu_n,b equals 2 times full Haar restricted to det O=b, since that component has mass 1/2. This is a probability measure.", "not_author_written": True, "not_public_binder": True},
    {"id": "bridge:actual-Gaussian-density", "kind": "SOURCE_GAP", "gap_type": "source-implied-library-density-identification", "source_anchors": ["S2.p1.1", "S2.SS0.SSS0.Px1.p1.2", "S3.E4", "A2.SS2.p2.1"], "meaning": "For actual O in O(n) and kappa>=4, Eq4 gives a real symmetric positive precision A_O. The normalized Euclidean Gaussian density sqrt(det A_O)/(2*pi)^(n/2) * exp(-x^T A_O x/2) is an everywhere nonnegative measurable unit-mass Lebesgue density of the actual N(0,A_O^{-1}). The real n/2 exponent and Euclidean reference volume are retained.", "conditions_discharged_by": ["source orthogonality", "literal Eq4", "source kappa>=4"], "not_author_written": True, "not_public_binder": True, "corroborating_source_only_not_required_ancestor": ["A2.SS2.SSS2.p4.2 invokes I<=A_O<=kappa I", "A2.Ex60 uses the same Gaussian determinant and (2*pi)^(-n/2) normalization factors; it is not cited by Ex70"]},
    {"id": "bridge:actual-mixture-density", "kind": "SOURCE_GAP", "gap_type": "source-implied-mixture-density-identification", "source_anchors": ["S3.SS1.p3.1", "A2.SS2.p2.1"], "meaning": "Averaging the actual canonical Gaussian density over the actual conditioned probability mu_n,b gives a specified representative p_b(x)=int p_O(x) dmu_n,b(O) of the actual mixture P_b, with nonnegativity, measurability, normalization and required integrability proved internally. Pointwise inner integrability is part of this chosen raw-average representative, not an added premise. Gaussian-kernel measurability and exchange of nonnegative integrals are background/library bridge obligations; the paper defines the measures/densities without writing this identification proof.", "not_author_written": True, "not_public_binder": True},
    {"id": "route:Ex70-positive-residual", "kind": "conditional-source-route", "guard": "k*n<d (equivalently r>0 under floor-divmod bookkeeping)", "statement_shape": "guard -> actual product density in positive residual coordinates", "source_anchors": ["A2.SS2.SSS3.p3.1", "A2.Ex70"], "meaning": "Author explicitly cites Eq6 and displays the residual-factor density; omitted library/coordinate bridges are separate dependencies."},
    {"id": "route:Ex70-zero-residual", "kind": "conditional-source-route", "guard": "k*n=d (equivalently r=0 under floor-divmod bookkeeping)", "statement_shape": "guard -> actual product density with unit/omitted residual", "source_anchors": ["S3.SS1.p3.2", "A2.SS2.SSS3.p3.3"], "meaning": "Source omission convention specializes actual product law and density to no residual; the all-dimensional explicit phi convention needs the recorded unit-factor bridge."},
    {"id": "route:Ex71-positive-residual", "kind": "conditional-consumer-route", "guard": "k*n<d", "statement_shape": "guard -> actual affinity equals a^k", "source_anchors": ["A2.SS2.SSS3.p3.2", "A2.Ex71"]},
    {"id": "route:Ex71-zero-residual", "kind": "conditional-consumer-route", "guard": "k*n=d", "statement_shape": "guard -> actual affinity equals a^k without residual factor", "source_anchors": ["A2.SS2.SSS3.p3.3"]}
]
g["nodes"].extend(nodes)

# Omitted bridge attributes from v1 become actual dependency incidences; the
# original route labels still distinguish author-written and expanded steps.
edges = []
for old in g["edges"]:
    edge = deepcopy(old)
    bridge_ids = []
    if edge.get("omitted_bridge"):
        bridge_ids.append(edge["omitted_bridge"])
    bridge_ids.extend(edge.get("omitted_bridges", []))
    edge["from"] = list(dict.fromkeys(edge["from"] + bridge_ids))
    if bridge_ids:
        edge["expanded_source_gap_dependencies"] = bridge_ids
    if edge["to"] == "source:A2.Ex70":
        if edge["route"] == "author-explicit-product-law-to-density":
            edge["to"] = "route:Ex70-positive-residual"
            edge["guard"] = "k*n<d"
        else:
            edge["to"] = "route:Ex70-zero-residual"
            edge["guard"] = "k*n=d"
        edge["from"].extend(["bridge:actual-mixture-density", "bridge:floor-divmod-accounting"])
        edge["edge_semantics"] = "conditional-route: guard is case-local, not an extra public binder or an unconditional claimed fact"
    elif edge["to"] == "source:A2.Ex71":
        if "positive-residual" in edge["route"]:
            edge["to"] = "route:Ex71-positive-residual"
            edge["guard"] = "k*n<d"
        else:
            edge["to"] = "route:Ex71-zero-residual"
            edge["guard"] = "k*n=d"
        edge["edge_semantics"] = "conditional consumer route; the guard is discharged in its selected case"
    edges.append(edge)

def add(from_, to, use, route, **extra):
    edge = {"from": from_, "to": to, "consumer_use_site": use, "route": route}
    edge.update(extra)
    edges.append(edge)

add(["source:S3.SS1.p1.1"], "bridge:floor-divmod-accounting",
    "S3.SS1.p1.1 block count; d-kn dimensions in S3.E5/S3.E6 and A2.SS2.SSS3.p3.1",
    "source-omitted-integer-bookkeeping", not_author_written=True, no_new_public_premise=True)
add(["bridge:floor-divmod-accounting", "source:S3.SS1.p3.2"], "bridge:residual-case-exhaustion",
    "A2.SS2.SSS3.p3.1 positive branch and p3.3 equality branch",
    "source-omitted-exhaustive-guard-discharge", not_author_written=True, no_new_public_premise=True)
add(["source:S2.p1.1", "source:S2.p2.1", "source:S3.E4", "source:S3.SS1.p1.1", "source:S2.target", "source:A2.SS2.p2.1"],
    "bridge:actual-Gaussian-density", "A2.SS2.p2.1 defines p_O as actual Gaussian density; canonical representative needed when interpreting the explicit Ex70 candidate",
    "source-implied-library-Gaussian-density", not_author_written=True,
    conditions_discharge="Orthogonality and kappa>=4 produce SPD and positive determinant internally; no SPD/density binder.")
add(["source:S2.p2.1", "source:S3.SS1.p1.1"], "bridge:conditioned-Haar-probability",
    "S3.SS1.p2.1 draws from mu_n,b; S3.SS1.p3.1 integrates the Gaussian law",
    "source-implied-conditioned-measure-identification", not_author_written=True,
    conditions_discharge="Source determinant components each have Haar mass 1/2; b is one of the two source signs.")
add(["bridge:actual-Gaussian-density", "bridge:conditioned-Haar-probability", "source:S3.SS1.p3.1", "source:A2.SS2.p2.1"],
    "bridge:actual-mixture-density", "A2.SS2.p2.1 actual p_b; used in Ex70's product at A2.SS2.SSS3.p3.1 / Ex70",
    "source-implied-library-mixture-density", not_author_written=True,
    conditions_discharge="Measurability/nonnegativity and integrability/normalization derive from the actual Gaussian family and probability prior, not new assumptions.")
add(["source:S2.p1.1", "bridge:floor-divmod-accounting"], "gap:coordinate-volume-identification",
    "A2.Ex70 uses block tuples and Ex71 integrates dx on R^d",
    "source-omitted-coordinate-volume-bookkeeping", not_author_written=True,
    conditions_discharge="Actual ordered coordinate dimension equality k*n+r=d; standard Euclidean/Lebesgue conventions.")
add(["bridge:actual-mixture-density", "source:S3.E6"], "gap:product-density-and-representative",
    "A2.SS2.SSS3.p3.1 / A2.Ex70 product of actual p_b and residual density",
    "source-omitted-library-product-density", not_author_written=True,
    conditions_discharge="Now actual-law density status is supplied by the predecessor bridge rather than assumed.")
add(["bridge:floor-divmod-accounting", "source:S3.SS1.p3.2"], "gap:zero-residual-bridge",
    "S3.SS1.p3.2 and A2.SS2.SSS3.p3.3 omit the factor at k*n=d",
    "source-omitted-zero-dimensional-bookkeeping", not_author_written=True,
    conditions_discharge="Inside equality branch r=0; zero-dimensional Euclidean volume and Gaussian are unit probability, giving phi=1.")
add(["bridge:residual-case-exhaustion", "route:Ex70-positive-residual", "route:Ex70-zero-residual"], "source:A2.Ex70",
    "A2.SS2.SSS3.p3.1 / Ex70 together with S3.SS1.p3.2 omission convention and A2.SS2.SSS3.p3.3",
    "exhaustive-two-case-closure", edge_semantics="AND of (G or H), (G implies T), (H implies T); does NOT assert G and H simultaneously",
    guards_discharged="G is k*n<d; H is k*n=d; floor accounting proves exactly one and rules out k*n>d.")
add(["bridge:residual-case-exhaustion", "route:Ex71-positive-residual", "route:Ex71-zero-residual"], "source:A2.Ex71",
    "A2.Ex71 positive branch and A2.SS2.SSS3.p3.3 no-residual branch",
    "exhaustive-two-case-consumer-closure", edge_semantics="AND of exhaustive guard disjunction and two conditional implications; no false AND of branch conditions")

g["edges"] = edges
g["branch_semantics"] = "Explicit exhaustive case closure: (kn<d OR kn=d), with each density/affinity route conditional on its own guard; floor/divmod bookkeeping discharges both branch dimensions. No kn>d case; no extra public premise."
g["definition_identification_chain"] = ["actual Eq4 Gaussian", "canonical Gaussian precision density", "actual conditioned Haar probability", "actual P_b mixture", "canonical Haar-average mixture-density representative", "actual Eq6 product law", "product density and coordinate-volume identification", "Ex70 actual averaged-target density"]
g["root_closure_policy"] = "Backward closure follows only from/to incidences (including explicit SOURCE_GAP dependencies). Consumer-only destinations and corroborating-source notes never create reverse edges."
node_ids = {n["id"] for n in g["nodes"]}
for edge in edges:
    assert edge["to"] in node_ids, edge
    assert set(edge["from"]) <= node_ids, edge
closure, todo = set(), [g["root"]]
while todo:
    cur = todo.pop()
    if cur in closure:
        continue
    closure.add(cur)
    for edge in edges:
        if edge["to"] == cur:
            todo.extend(edge["from"])
g["root_ancestor_boundary"] = sorted(closure - {g["root"]})
assert "source:S2.p1.1" in closure
assert "source:S3.SS1.p1.1" in closure
assert "bridge:floor-divmod-accounting" in closure
assert "bridge:residual-case-exhaustion" in closure
assert "bridge:actual-Gaussian-density" in closure
assert "bridge:actual-mixture-density" in closure
for prohibited in ["source:A2.Ex68", "source:A2.Ex69", "source:A2.E19", "source:A2.E25", "source:A2.Ex71", "source:A2.Ex72", "source:Tonelli"]:
    assert prohibited not in closure, prohibited

inventory["schema"] = "source-only-inventory-v2"
inventory["supersedes_inventory_sha256"] = sha256(inventory_path.read_bytes()).hexdigest()
inventory["source_items_unchanged"] = True
inventory["revision_note"] = "Every raw item retains its frozen disposition/text/line; source-implied/library/bookkeeping bridge incidences are now explicit in v2 graph, without pretending they are author-written proof paragraphs."
inventory["source_implied_bridge_coverage"] = [
    {"anchors": n.get("source_anchors", []), "node": n["id"], "kind": n.get("gap_type", n["kind"]), "disposition": "NODE", "provenance": "source-omitted; not author-written"}
    for n in nodes if n["kind"] == "SOURCE_GAP"
]
(OUT / "source-proof-graph.v2.json").write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
(OUT / "raw-source-inventory.v2.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"nodes": len(g["nodes"]), "edges": len(g["edges"]), "root_ancestors": len(g["root_ancestor_boundary"]), "all_node_references_resolve": True, "required_context_and_bridges_reach_root": True, "consumer_nodes_not_root_ancestors": True}, indent=2))
