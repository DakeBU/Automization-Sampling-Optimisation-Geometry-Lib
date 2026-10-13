import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path("E:/Samplinglib")
BASE = "runs/20261007-companion-priority/"
PRE = BASE + "pbps-normalized-endpoint-preread104/"
SRC = BASE + "pbps-actual-phase-normalization103/next-primary104/"
OUT = ROOT / (PRE + "independent-header-source104")
records = {}


def bind(path):
    data = (ROOT / path).read_bytes()
    result = {"path": path, "raw_sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    records[path] = result
    return result


def load(path):
    bind(path)
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def put(name, data):
    path = OUT / name
    assert not path.exists()
    path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return bind(path.relative_to(ROOT).as_posix())


expected = load(SRC + "expected-semantic-slots104.native.json")
recommendation = load(SRC + "recommendation104.native.json")
coverage = load(SRC + "source-coverage-delta104.native.json")
source_graph = bind(SRC + "source-proof-graph-delta104.native.json")
source_first = bind(SRC + "primary-first104.native.json")
source_closure = bind(SRC + "closed-RAW-manifest104.native.json")
retrieval = load(SRC + "retrieval104.native.json")
primary = bind(coverage["primary"]["path"])
assert primary == coverage["primary"]
raw = (ROOT / primary["path"]).read_bytes()
source_regions = []
for region in coverage["regions"]:
    span = raw[region["byte_start"]:region["byte_end_exclusive"]]
    assert hashlib.sha256(span).hexdigest() == region["raw_sha256"]
    source_regions.append(dict(region, original_slice_RAW_rechecked=True))
assert len(source_regions) == 21

header = bind(PRE + "Header104.lean")
assert header["raw_sha256"] == "4fc65e051233c07d0d2272b3371fad1c1164546b51a4c313c0ec0d314b805be4"
text = (ROOT / header["path"]).read_text(encoding="utf-8")
lines = text.splitlines()
receipt = load(PRE + "header104.receipt.json")
assert receipt["header_raw_sha256"] == header["raw_sha256"]
assert receipt["terminal_closed"] and receipt["exit_code"] == 0
bind(PRE + "header104.stdout.log")
bind(PRE + "header104.stderr.log")
parents = {}
for node, item in retrieval["actual_producers"].items():
    current = bind(item["artifact"]["path"])
    assert current == item["artifact"]
    parents[node] = dict(item, current_RAW_rechecked=True)
sector = (ROOT / parents["SECTOR102-UNNORM"]["artifact"]["path"]).read_text(encoding="utf-8")


def between(value, start, end):
    return value[value.index(start):value.index(end)]


literal_header = between(text, "    let c :", "    let R :")
literal_parent = between(sector, "    let c :", "    let R :")
assert literal_header == literal_parent == recommendation["literal_definition_contract"]["exact_existing_definition_text_LF"]
binders_header = between(text, "    {E : Type*}", " : Prop := by")
binders_parent = between(sector, "    {E : Type*}", " : Prop := by")
assert binders_header == binders_parent
definitions = [{"line": i, "name": re.match(r"\s+let ([^ :]+)", line).group(1)}
               for i, line in enumerate(lines, 1) if re.match(r"\s+let ", line)]
assert len(definitions) == 30
assert [d["name"] for d in definitions[20:]] == ["R", "Vy", "piY", "gamma", "m", "A", "B", "sigma", "L", "J"]
assert "    ∀ y r : E, ∀ n : ℕ, ∀ T : ℝ≥0," in text
assert "      MeasurePreserving J L L" in text
mechanical = put("header-definition-checks104.native.json", {
    "header": header, "header_lines": len(lines), "definitions": definitions,
    "literal_first20_equal_actual102_and_frozen104_recommendation": True,
    "first20_LF_text_sha256": hashlib.sha256(literal_header.encode("utf-8")).hexdigest(),
    "source_six_binders_and_ambient_contract_text_equal_actual102": True,
    "binder_LF_text_sha256": hashlib.sha256(binders_header.encode("utf-8")).hexdigest(),
    "outer_lets": 25, "inner_lets": 5,
    "literal_measure_contract": {
        "phase_order": "position then momentum, (piY y).prod gamma",
        "parameter_order": "phase then event tuple, ((piY y).prod gamma).prod (m n T)",
        "density": "Actual rho y r q.1 n T q.2; rho=q times terminal weight from the first20 exact definitions.",
        "event_measure": "comap Subtype.val of volume on Fin n -> Real; no normalization or factorial.",
        "endpoint": "A q = actual Gamma y r q.1 n T q.2 evaluated at <T,le_rfl>",
        "endpoint_pair": "B q=(q.1,A q); L=map B sigma",
        "flip": "J p=(R p.2,R p.1), R(x,p)=(x,-p)"
    },
    "type_only_receipt": bind(PRE + "header104.receipt.json"),
    "type_only_not_mathematical_proof": True
})

slot_texts = {
    "objects": ("equivalent", "Header22-73 preserves the actual20 algorithm definitions literally. Header74-89 uses actual tilted position law, standard Gaussian, simplex comap measure, terminal Gamma and endpoint-pair pushforward."),
    "domains": ("equivalent", "Header12-14 retains finite-dimensional real Borel inner-product E, including rank zero; Header80 universally includes n:Nat and T:NNReal. Endpoint-pair measure is on (E×E)×(E×E)."),
    "quantifiers": ("equivalent", "Header80 writes forall y r n T rather than recommendation forall n T y r. All four are universal and independent before dependent lets, so their order is immaterial. No observable or reversal witness is a premise."),
    "assumptions": ("equivalent", "Header15-19 is text-identical to actual102's six original analytic binders. Neither normalizer, minimizer, measurability, integrability, sigma-finiteness nor a producer law is supplied."),
    "conclusion": ("explicit-elaboration", "Header89 is precisely MeasurePreserving J L L for the literal normalized-initial fixed-count endpoint-pair measure. This packages the single-count source change of variables; it does not assert L is a probability measure."),
    "scopes": ("equivalent", "Only a fixed count and horizon sector is transported. There is no countable sum, full process kernel, signed operator identity, pointwise jump reversal, invariant law or cost conclusion."),
    "constant_dependencies": ("equivalent", "Header retains sqrt(eta) rate and actual harmonic coefficients; Vy has denominator2eta and gamma is unit covariance. Actual103 supplies the exact finite phase normalizer internally; it is not an extra binder. No n! or sector-mass normalization appears.")
}
slots = {}
for name, (relation, evidence) in slot_texts.items():
    slots[name] = {"source": expected[name], "header": evidence, "relation": relation, "evidence": evidence}

edge_cases = {
    "n0": "StrictMono on Fin1 containing zero is vacuous and Fin0 bounds are empty, so Prefix0T is the empty tuple. Empty product and terminal actual flow are retained.",
    "T0_n0": "Endpoint is time0; no positive-horizon premise. Pair becomes (z,z), with actual initial phase law; reversal uses momentum flip.",
    "T0_positive_n": "Strict first time >0 and all times <0 make the subtype empty. MeasurePreserving of the zero sector is meaningful without dividing by mass.",
    "rank0": "No nontrivial-space or positive-rank binder. Canonical volume, tilted Gibbs and standard Gaussian are the inherited zero-dimensional laws; no hidden normalizing constant is supplied.",
    "zero_normals_rates": "Total Lean reflection formula and max0 rate are preserved. The claim never divides by rate or requires strictly positive sector mass.",
    "endpoint_jumps": "All prescribed event times are strictly inside (0,T). Only the actual terminal endpoint enters B; no equality of reversed right-continuous paths at event times is asserted.",
    "infinite_integrals": "MeasurePreserving permits measures of infinite mass. Internal all-test ENNReal route does not require finite test integrals or a finite/subprobability sector conclusion."
}
ingredients = [
    {"source_node": "MEASDENS93", "producer": "actual_finite_count_path_law", "obligation": "Extract actual joint rho measurability. A withDensity expression being well-typed does not discharge this proof obligation."},
    {"source_node": "TIME97/THETA97/ENDPOINT97", "producer": "actual_endpoint_time_reversal_laws", "obligation": "Extract same-witness coordinates, actual joint endpoint/Theta measurability and A(RA,rho t)=Rz; derive B-Theta/J-B commutation."},
    {"source_node": "SECTOR102-UNNORM/ALIGN104", "producer": "actual_weighted_sector_lintegral", "obligation": "Use all measurable nonnegative tests and identify102's time witness with97's using coordinates, not a supplied compatibility hypothesis."},
    {"source_node": "NORM", "producer": "actual_phase_gibbs_normalization", "obligation": "Rewrite actual piY.prod gamma as normalized ell.withDensity, with exact positive finite Zphase. No103 analysis re-proof or102->NORM dependency."},
    {"source_node": "SECTOR-MEASURE104", "producer": "Local adapter plus fixed Mathlib", "obligation": "Derive measurable strict simplex and SigmaFinite(m); use prod_withDensity_left, withDensity_mul and actual measurable weights."},
    {"source_node": "SECTOR100/ENDPAIR104", "producer": "Local adapter plus fixed Mathlib", "obligation": "Normalize all-test substitution, pass to measure equality, then push forward by actual endpoint-pair map. These are pending proof ingredients, not source binders."}
]
coverage_result = put("header-source-coverage104.native.json", {
    "kind": "prospective header/source coverage; not compiled proof coverage",
    "primary": primary, "source_regions": source_regions,
    "frozen_source_graph": source_graph, "frozen_source_closure": source_closure,
    "header": header,
    "header_regions": [
        {"lines": [1, 10], "role": "Imports, namespace and type-only environment; no proof claim."},
        {"lines": [11, 21], "role": "Prop definition with ambient contract and exactly six original source assumptions."},
        {"lines": [22, 73], "role": "Twenty actual algorithm definitions, literally inherited."},
        {"lines": [74, 79], "role": "R, actual Vy, piY, gamma and strict-simplex measure."},
        {"lines": [80, 89], "role": "Universal y,r,n,T and actual endpoint, pair, sector and flipped-swap measure-preservation conclusion."},
        {"lines": [90, 93], "role": "Type-only check and namespace closure."}
    ],
    "proof_ingredients_not_header_binders": ingredients,
    "edge_cases": edge_cases,
    "selected_source_region": "Eq3.1 and A.1 fixed-count substitution through3215 only.",
    "excluded_source_region": "3216-3227 countable/signed operator assembly, process invariance and L2 remain separate; all other inherited source regions retain their frozen dispositions.",
    "graph_topology_validation": "Not performed: reviewer is creator of the source graph. Independent mathematical/topology admission is required.",
    "implementation_coverage": "No implementation exists or is reviewed; no prospective ingredient receives theorem credit."
})
decision = put("header-source-decision104.native.json", {
    "verdict": "ACCEPT_PROSPECTIVE_SOURCE_HEADER",
    "reviewer": "/root/source_final96",
    "header": header, "primary_first": source_first,
    "expected_slots": bind(SRC + "expected-semantic-slots104.native.json"),
    "semantic_slots": slots,
    "deltas": [
        {"slot": "quantifiers", "severity": "informational", "description": "Independent universal parameter order is permuted.", "source": "forall n T y r", "lean": "forall y r n T", "evidence": "No quantifier changes kind and no additional binder depends on the permuted parameters before their lets.", "blocking": False},
        {"slot": "conclusion", "severity": "informational", "description": "Explicit endpoint-pair measure completion of the source fixed-count substitution.", "source": "Each fixed n-jump term is unchanged under A8, before countable assembly.", "lean": "MeasurePreserving J (map B actualNormalizedSector) (map B actualNormalizedSector).", "evidence": "Actual source normalization and prescribed density are literal definitions. The measure packaging permits all nonnegative measurable tests without extra integrability or mass claims.", "blocking": False}
    ],
    "repairs": [], "blocking_findings": [],
    "mechanical_definition_checks": mechanical,
    "source_coverage": coverage_result,
    "actual_parent_bindings": parents,
    "independence": {
        "source_first_expectations_preexist_header": True,
        "frozen_expectations_read_before_header": True,
        "prior_source_graph_authorship_acknowledged": True,
        "prior103_source_review_involvement_acknowledged": True,
        "graph_self_topology_validation": False,
        "header_author": False,
        "proof_implementation_seen": False,
        "other_header_math_verdict_used_as_source_evidence": False,
        "decoder_seen": False
    },
    "truth_boundary": "Prospective source-header fidelity only. Type-only PASS is bound but is not a proof. No Statement Seal, claim, mathematical completion, VERIFIED state, merged validation or delivery admission is granted.",
    "remaining": recommendation["remaining_reds"],
    "no_shared_or_prior_evidence_mutations": True,
    "no_full_primary_copy": True
})
run = put("header-source-run104.native.json", {
    "reviewer": "/root/source_final96", "decision": decision,
    "header": header, "primary": primary,
    "all21_original_slices_rehashed": True,
    "source_definition_comparison": mechanical, "source_coverage": coverage_result,
    "type_only_evidence": bind(PRE + "header104.receipt.json"),
    "proof_credit": False, "source_graph_self_validation": False,
    "reading_sequence": "Frozen104 expected slots/source-only recommendation first; exact Header104 next; pinned primary formulas and original slices rechecked; actual producers checked only for definition identity and required internal ingredients.",
    "stage": "Prospective header source review; final compiled source/decoder/exposition review remains required."
})
owned = [bind(path.relative_to(ROOT).as_posix()) for path in sorted(OUT.iterdir()) if path.is_file()]
owned_paths = {item["path"] for item in owned}
for item in owned:
    data = (ROOT / item["path"]).read_bytes()
    assert b"\r" not in data
    assert data.endswith(b"\n") and not data.endswith(b"\n\n")
    assert all(line.rstrip() == line for line in data.splitlines())
manifest = put("closed-RAW-manifest104.native.json", {
    "kind": "immutable prospective header-source104 RAW closure",
    "inputs": [item for key, item in sorted(records.items()) if key not in owned_paths],
    "owned_outputs": owned, "decision": decision, "run": run,
    "self_hash_intentionally_omitted": True,
    "no_source_graph_modification_or_topology_self_validation": True,
    "no_proof_credit": True
})
print(json.dumps({"decision": decision, "coverage": coverage_result, "run": run, "manifest": manifest}, indent=2))
