import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("E:/Samplinglib")
BASE = "runs/20261007-companion-priority/"
RUN = BASE + "pbps-actual-normalized-endpoint104/"
PRE = BASE + "pbps-normalized-endpoint-preread104/"
OUT = ROOT / (RUN + "final-source104")
SOURCE = BASE + "pbps-actual-phase-normalization103/next-primary104/"
REVIEWER = "/root/source_final96"
EXPECTED_PACKET, EXPECTED_PUBLICATION = sys.argv[1:3]
inputs = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bind(path):
    path = path.replace("\\", "/")
    if path.startswith("E:/Samplinglib/"):
        path = path[len("E:/Samplinglib/"):]
    data = (ROOT / path).read_bytes()
    item = {"path": path, "raw_sha256": sha(data), "bytes": len(data)}
    inputs[path] = item
    return item


def read(path):
    bind(path)
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def put(name, obj):
    path = OUT / name
    assert not path.exists(), str(path)
    path.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return bind(path.relative_to(ROOT).as_posix())


primary_first = read(RUN + "final-source104/primary-first/primary-first-reconstruction104.native.json")
expected = read(RUN + "final-source104/primary-first/expected-semantic-slots104.native.json")
bind(RUN + "final-source104/primary-first/closed-primary-first-RAW104.native.json")
packet = read(RUN + "reviewer-packet104.json")
canonical = dict(packet)
canonical.pop("packet_sha256")
assert sha(json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()) == EXPECTED_PACKET == packet["packet_sha256"]
assert packet["publication_binding_sha256"] == EXPECTED_PUBLICATION
assert all(value is False for value in packet["anti_anchoring"].values())
module = packet["lean"]["file"]
production = bind(module)
assert production["raw_sha256"] == "c2a980f6397528f818120ca6163bf9b286f5c2ef5d4c730d9608267271b03074"
raw = (ROOT / module).read_bytes()
text = raw.decode("utf-8").replace("\r\n", "\n")
lines = raw.splitlines(keepends=True)
assert len(lines) == 230
header = bind(PRE + "Header104.lean")
assert header["raw_sha256"] == "4fc65e051233c07d0d2272b3371fad1c1164546b51a4c313c0ec0d314b805be4"
header_text = (ROOT / header["path"]).read_text(encoding="utf-8")
body = lambda s: s[s.index("    {E : Type*}"):s.index("      MeasurePreserving J L L") + len("      MeasurePreserving J L L")]
assert body(text) == body(header_text)
assert len(re.findall(r"^    let ", text.split("theorem actual_normalized_endpoint_sector_reversal")[0], re.M)) == 25
assert len(re.findall(r"^      let ", text.split("theorem actual_normalized_endpoint_sector_reversal")[0], re.M)) == 5

lesson_path = "website/content/declaration_lessons/pbps-actual-normalized-endpoint-sector.json"
pub_path = "website/content/publications/pbps-actual-normalized-endpoint-sector.json"
lesson = read(lesson_path)
unit = lesson["units"][0]
publication = read(pub_path)["items"][0]
assert unit["statement"] == publication["statement"] == packet["source"]["original_text"]
assert sha(packet["source"]["original_text"].encode()) == packet["source"]["text_sha256"]
assert sha(packet["lean"]["statement"].encode()) == packet["lean"]["statement_sha256"]
assert packet["candidate_publication_context"]["current_lean_module"] == text

repair_proposal = read(RUN + "exposition-index-repair104/proposal104.json")
repair_review = read(RUN + "exposition-index-repair104/independent-review/decision104.native.json")
assert repair_review["decision"] == "ACCEPT_AUTHORED_NOTATION_CLARIFICATION_ONLY"
assert repair_review["reviewer"] != REVIEWER
assert repair_review["proposal"] == bind(RUN + "exposition-index-repair104/proposal104.json")
old_lesson = read(RUN + "exposition-index-repair104/0.before.exactraw.snapshot.json")
old_packet = read(RUN + "exposition-index-repair104/1.before.exactraw.snapshot.json")
expected_lesson = json.loads(json.dumps(old_lesson))
expected_lesson["units"][0]["steps"][0]["text"] = repair_proposal["new"]
assert expected_lesson == lesson
assert unit["steps"][0]["text"] == repair_review["exact_new"]
assert old_packet["lean"] == packet["lean"]
assert old_packet["blind_reconstruction"] == packet["blind_reconstruction"]
assert old_packet["source"] == packet["source"]
bind(RUN + "final-source104/initial-exposition-finding104.native.json")
bind(RUN + "exposition-index-repair104/independent-review/run104.native.json")
bind(RUN + "exposition-index-repair104/independent-review/closed-RAW104.native.json")
bind(RUN + "exposition-index-repair104/applied104.json")

decoder_path = "runs/semantic-roundtrip/anonymous104/decoder-native/"
decoder_run = read(decoder_path + "decoder-run.json")
for key in ("source_text_visible", "source_identity_visible", "prior_audit_visible", "repair_proposals_visible"):
    assert decoder_run[key] is False
decoder = read(decoder_path + "reconstruction.json")
decoder_text = (ROOT / (decoder_path + "reconstruction.txt")).read_text(encoding="utf-8")
bind(decoder_path + "reconstruction.txt")
assert decoder_text == packet["blind_reconstruction"]["text"]
for item in decoder_run["input_artifacts"] + decoder_run["reconstruction_artifacts"]:
    assert bind(item["path"])["raw_sha256"] == item["sha256_raw"]

topology = read(PRE + "independent-header-math104/source-topology-admission104.native.json")
topology_data = read(PRE + "independent-header-math104/topology-binding-check104.native.json")
graph = topology_data["effective_graph"]
assert len(graph["nodes"]) == 55 and len(graph["edges"]) == 96
source_graph = bind(SOURCE + "source-proof-graph-delta104.native.json")
assert source_graph == topology["graph"]
source_coverage = read(SOURCE + "source-coverage-delta104.native.json")
primary = bind(source_coverage["primary"]["path"])
assert primary == source_coverage["primary"]
primary_raw = (ROOT / primary["path"]).read_bytes()
regions = []
for old in source_coverage["regions"]:
    assert sha(primary_raw[old["byte_start"]:old["byte_end_exclusive"]]) == old["raw_sha256"]
    region = dict(old)
    region["fresh_RAW_verified"] = True
    if old["id"] in ("standing-curvature", "standing-eta"):
        region["compiled104_disposition"] = "Original six public binders and private Prop retained at21-28/105-112; all four producer calls receive them."
    elif old["id"] in ("target-position-energy", "phase-gibbs-law"):
        region["compiled104_disposition"] = "Actual piY.prod gamma in85-86/94; internal hphase consumes103 at187-190; exact sigma density conversion191-200."
    elif old["id"] in ("simplex", "prescribed", "A7"):
        region["compiled104_disposition"] = "Literal actual definitions31-82; joint density143-150; strict-simplex measurability/sigma-finiteness151-172. Only one fixed n density, not full A7 sum."
    elif old["id"] in ("A8", "unweighted-transform"):
        region["compiled104_disposition"] = "Actual97/102 coordinate witness alignment116-127, endpoint measurability/intertwining128-142, normalized parameter-sector201-216 and endpoint pushforward217-226."
    elif old["id"] == "average":
        region["compiled104_disposition"] = "Initial normalized Gibbs law is integrated in sigma. Countable assembly and its identification with the actual full process remain excluded."
    elif old["id"] == "weight-matching-and-invariance":
        region["compiled104_disposition"] = "3210-3215 fixed-sector completion realized by hsector201-216 and endpoint pushforward217-226. 3216-3227 signed/full process/L2 excluded."
    elif old["id"] == "source-license":
        region["compiled104_disposition"] = "License reference retained; no new full-source copy."
    else:
        region["compiled104_disposition"] = "Unchanged inherited source ingredient or explicitly excluded later claim; transitive actual97/102 inputs reused, not re-proved or credited here."
    regions.append(region)
assert len(regions) == 21

wm = read(RUN + "independent-whole-math104/whole-math-decision104.native.json")
assert bind(RUN + "independent-whole-math104/whole-math-decision104.native.json")["raw_sha256"] == "7225d78b58d011e2e0272242d5023f020bab2dd15a51d86fb1ec55515cc27ed9"
kernel = read(wm["fresh_kernel"]["path"])
assert kernel["production"] == production and kernel["exit_code"] == 0 and kernel["terminal_closed"]
assert bind(kernel["input"]["path"]) == kernel["input"]
kernel_bytes = (ROOT / kernel["input"]["path"]).read_bytes()
assert kernel_bytes.startswith(raw)
assert not re.search(r"^import .*ActualNormalizedEndpointSector", kernel_bytes.decode("utf-8"), re.M)
for k in ("stdout", "stderr"):
    assert bind(kernel[k]["path"]) == kernel[k]
bind(wm["seal"]["path"])
bind(wm["root_terminal_production"]["path"])


def span(start, end):
    data = b"".join(lines[start - 1:end])
    return {"path": module, "line_start": start, "line_end": end,
            "raw_sha256": sha(data), "bytes": len(data),
            "LF_text_sha256": sha(data.replace(b"\r\n", b"\n"))}


parents = [
    ("ActualEndpointTimeReversal.lean", "actual_endpoint_time_reversal_laws", [116, 118], "TIME97,THETA97,ENDPOINT97 same witness; actual A/Theta measurability and endpoint inverse."),
    ("ActualWeightedSector.lean", "actual_weighted_sector_lintegral", [119, 121], "SECTOR102-UNNORM coordinate witness and all measurable ENNReal tests, consumed again216."),
    ("ActualFiniteCountPath.lean", "actual_finite_count_path_law", [143, 150], "MEASDENS93 actual rho joint measurability projection."),
    ("ActualPhaseNormalization.lean", "actual_phase_gibbs_normalization", [187, 190], "NORM actual normalized phase-density equality; positivity/finite partition remain internally proved by103.")
]
parent_rows = []
for filename, name, bounds, role in parents:
    path = "AutoSamplingTheory/ExampleCases/ProximalBPS/" + filename
    parent_rows.append({"declaration": "AutoSamplingTheory.ExampleCases.ProximalBPS." + filename[:-5] + "." + name,
                        "artifact": bind(path), "invocation": span(*bounds), "role": role,
                        "source_hypotheses": "Exactly hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta; no provider binder."})
assert set(unit["astis_dependencies"]) == {p["declaration"] for p in parent_rows}
retrieval = read(SOURCE + "retrieval104.native.json")
for api in retrieval["fixed_apis"]:
    assert bind(api["artifact"]["path"]) == api["artifact"]

step_judgments = [
    "The repaired explicit zero-based Fin n convention makes n-1-i exact. Coordinate equations from97/102 yield extensional equality before either is combined. For n=0 there is no coordinate to evaluate.",
    "Fixing y,r by the measurable parameter map yields measurable actual A,B,R,J,Theta. Parent97 supplies the second coordinate of B(Theta x)=J(B x), with the terminal flow included. No jumpwise path equality is asserted.",
    "The93 projection is genuinely joint actual density measurability; composition supplies exactly rho(z,t), including terminal survival. It is not assumed or replaced by another density.",
    "Finite coordinate inequalities produce measurable Delta. map_comap_subtype_coe identifies its image measure with restricted volume, then SigmaFinite.of_map supplies the required product-side instance. Empty/rank-zero cases require no exception.",
    "The actual phase energy and measurable weight are correct. hphase extracts the exact103 product-law identity. The formula uses ordinary positive-density notation; ofReal and ENNReal normalizer are explicit in adjacent Lean and complete statement.",
    "prod_withDensity_left uses proved simplex sigma-finiteness and actual measurable initial density. withDensity_mul combines the true rho, and associativity gives exactly cNorm*W. Phase remains first.",
    "hsector explicitly proves full normalized parameter-sector preservation, using all measurable ENNReal tests and two lintegral density rewrites. Constant multiplication applies without cancellation or finite-integral assumptions. This is the stable SECTOR100 ingredient.",
    "Two measurable pushforward compositions plus the actual endpoint intertwining transport hsector to exactly map J L=L; hJ supplies the measurability component. No full-process/countable claim follows here."
]
step_rows = []
for i, step in enumerate(unit["steps"]):
    region = step["lean_source_region"]
    s = span(region["start_line"], region["end_line"])
    raw_span = b"".join(lines[region["start_line"] - 1:region["end_line"]])
    displayed = step["lean"].encode("utf-8")
    assert displayed == raw_span.replace(b"\r\n", b"\n")
    assert sha(displayed) == region["exact_code_raw_sha256"]
    assert region["source_raw_sha256"] == production["raw_sha256"]
    slash_runs = [len(m.group()) for m in re.finditer(r"\\+", step["formula"])]
    assert all(n == 1 for n in slash_runs)
    step_rows.append({"step": i + 1, "title": step["title"], "source_span": s,
                      "display_code_RAW_sha256": sha(displayed), "formula": step["formula"],
                      "formula_UTF8_sha256": sha(step["formula"].encode()), "literal_backslash_run_lengths": slash_runs,
                      "text_UTF8_sha256": sha(step["text"].encode()), "judgment": "accepted",
                      "reason": step_judgments[i]})
assert len(step_rows) == 8

direct_map = {
    "H99": ([21, 28], "Six literal assumptions repeated105-112; passed to all four actual producers."),
    "D99": ([31, 98], "Actual algorithm, state/time conventions, normalized phase and endpoint-sector definitions."),
    "DEFWEIGHT101": ([173, 178], "Actual U,w,W reintroduced definitionally for normalization; no new density provider."),
    "TIME97": ([116, 127], "Public97 coordinate projection, compared with102 coordinate projection."),
    "ALIGN104": ([122, 127], "Subtype/coordinate extensionality aligns time witnesses; all parameters share it."),
    "ENDPOINT97": ([128, 142], "Existing97 joint A measurability and endpoint inverse projections; not a new endpoint theorem."),
    "THETA97": ([128, 137], "Direct use is joint Theta measurability. Volume-preservation projection is obtained but unused directly; its inherited formal role is already inside102."),
    "MEASDENS93": ([143, 150], "Direct93 joint actual rho measurability projection."),
    "SECTOR-MEASURE104": ([151, 200], "Strict-simplex sigma-finiteness, actual measurable weights, phase-law and density/product adapters."),
    "NORM": ([187, 190], "Exact actual103 product-law equality; upstream positive-finite normalization reused, not separately assumed."),
    "SECTOR102-UNNORM": ([119, 121], "Existing102 all-test identity used at216 after alignment; no old weighting proof repeated."),
    "SECTOR100": ([201, 216], "Explicit local hsector: MeasurePreserving Theta sigma sigma, including measurability and map equality."),
    "ENDPAIR104": ([217, 226], "Selected public endpoint-pair measure preservation through measurable pushforward.")
}
red_nodes = {"AVG100", "INV100", "L2A3", "RESTART", "A795"}
normalization_nodes = {"VY-DOM103", "PHASE-FACTOR103", "MeasureTheory.lintegral_prod_mul", "MeasureTheory.prod_withDensity"}
node_rows = []
for node in graph["nodes"]:
    if node in direct_map:
        bounds, explanation = direct_map[node]
        row = {"id": node, "disposition": "direct-current-definition-producer-or-proof-ingredient",
               "production_span": span(*bounds), "explanation": explanation}
    elif node in red_nodes:
        row = {"id": node, "disposition": "excluded-or-downstream-only", "production_span": None,
               "explanation": "No current proof or theorem credit. Fixed-count input does not assemble actual process sectors, signed averages, invariant law, L2 or restart. A795 remains existing bounded expansion for a later consumer."}
    elif node in normalization_nodes or node.startswith("AutoSamplingTheory.TechnicalLemmas."):
        row = {"id": node, "disposition": "unchanged-transitive103-ingredient",
               "consuming_span": span(187, 190), "explanation": "Reused through NORM103; no direct104 invocation, duplicate analytic proof or new assumption."}
    else:
        row = {"id": node, "disposition": "unchanged-transitive93-97-102-ingredient",
               "consuming_spans": [span(116, 121), span(143, 150), span(216, 216)],
               "explanation": "Inherited source-DAG identity retained. Actual97 endpoint/time and actual102 weighted substitution encapsulate earlier reversal, energy, rates, path and survival work. Actual93 is used only for joint rho measurability; no104 credit for re-proving these inherited nodes."}
    node_rows.append(row)
node_lookup = {row["id"]: row for row in node_rows}
edge_rows = []
for source, target in graph["edges"]:
    if target in red_nodes or source in red_nodes:
        status = "future-or-excluded; no104 theorem credit"
    elif target in {"ALIGN104", "SECTOR-MEASURE104", "SECTOR100", "ENDPAIR104"}:
        status = "current ingredient incidence realized; producer/same-witness roles as recorded"
    elif target == "ENDPOINT97":
        status = "existing public97 projection under H99/D99, not re-proved from binders alone"
    else:
        status = "unchanged inherited incidence reused transitively"
    edge_rows.append({"source": source, "target": target, "disposition": status,
                      "target_evidence": node_lookup[target].get("production_span", node_lookup[target].get("consuming_span")),
                      "not_a_new_Lean_edge_claim": target not in {"ALIGN104", "SECTOR-MEASURE104", "SECTOR100", "ENDPAIR104"}})

whole_ranges = [
    (1, 18, "Imports, attributed scope, namespace and options"),
    (19, 99, "Single private literal proposition, six assumptions and30 definitions"),
    (100, 115, "Proof options, public theorem with original binders, unfold/intro"),
    (116, 127, "Actual97/102 producers and coordinate witness alignment"),
    (128, 142, "Measurable actual endpoint diagram and intertwining"),
    (143, 150, "Actual93 joint density measurability"),
    (151, 172, "Strict-simplex measurability and sigma-finiteness"),
    (173, 190, "Actual phase weight and103 normalized phase-law equality"),
    (191, 200, "Actual normalized parameter-sector density rewrite"),
    (201, 216, "Explicit full sector preservation hsector"),
    (217, 226, "Measurable endpoint-pair pushforward"),
    (227, 230, "Axiom command and namespace closure")
]
assert [i for a, b, _ in whole_ranges for i in range(a, b + 1)] == list(range(1, 231))
coverage_artifact = put("compiled-source-coverage104.native.json", {
    "kind": "independently owned final compiled source coverage104",
    "reviewer": REVIEWER, "reviewer_packet_sha256": EXPECTED_PACKET,
    "publication_binding_sha256": EXPECTED_PUBLICATION,
    "production": production, "original_sealed_header": header,
    "source_primary": primary, "source_graph": source_graph,
    "independent_noncreator_topology": bind(PRE + "independent-header-math104/source-topology-admission104.native.json"),
    "topology_self_validation": False,
    "effective_counts": {"source_regions": 21, "nodes": 55, "edges": 96, "direct_public_parents": 4, "production_lines": 230, "exposition_regions": 8},
    "source_regions": regions, "node_dispositions": node_rows, "edge_dispositions": edge_rows,
    "all_production_regions": [dict(span(a, b), role=role) for a, b, role in whole_ranges],
    "whole_module": "All230 lines reviewed; exactly one private literal Prop and one public theorem. All local have/let arguments are internal to that proof. No arbitrary public provider or hidden private theorem call.",
    "actual_parent_discharge": parent_rows,
    "proof_ingredient_vs_source_binder": "Every measurability, sigma-finiteness, normalized-law, witness-alignment, weighted-substitution and endpoint-commutation ingredient is internally derived. Only the six original analytic source binders remain.",
    "explicit_internal_sector": {"identifier": "SECTOR100", "local_name": "hsector", "span": span(201, 216),
                                 "status": "proved internal full normalized parameter-sector preservation; not a second public process-invariance theorem"},
    "new_public_target": {"identifier": "ENDPAIR104", "span": span(217, 226)},
    "remaining_reds": ["AVG100 countable/signed assembly", "INV100 actual process invariance", "L2A3", "RESTART", "sector finite/subprobability mass", "error/cost/main/composition"],
    "fresh_kernel": bind(wm["fresh_kernel"]["path"]),
    "mathematical_review_use": "Fresh exact production/sealed-header kernel and axiom evidence reused only as Lean/math evidence, not as this source-fidelity verdict.",
    "no_source_graph_or_prior_review_edit": True
})
exposition_artifact = put("exposition104.native.json", {
    "verdict": "ACCEPT_BOUNDED_EIGHT_STEP_AUTHORED_EXPOSITION",
    "reviewer": REVIEWER, "reviewer_packet_sha256": EXPECTED_PACKET,
    "publication_binding_sha256": EXPECTED_PUBLICATION,
    "lesson": bind(lesson_path), "publication": bind(pub_path), "production": production,
    "steps": step_rows,
    "complete_statement": "Actual algorithm20 definitions, phase-law/simplex5 definitions and endpoint-sector5 definitions agree with private Prop and sealed header; all six conditions and zero cases are explicit.",
    "formula_conventions": "Commands have one literal backslash; JSON escaping was decoded before examination. Mathematical positive-density notation elides ofReal in several display formulas, with the exact coercions explicit in adjacent code and statement. Step1 alone now explicitly uses zero-based Fin n coordinates; surrounding simplex uses one-based names.",
    "source_and_display_bytes": "Each exact original source-byte interval and displayed LF UTF8 code hash is recorded separately. Only CRLF-to-LF normalization is allowed; actual equality was checked.",
    "repair": {"initial_finding": bind(RUN + "final-source104/initial-exposition-finding104.native.json"),
               "proposal": bind(RUN + "exposition-index-repair104/proposal104.json"),
               "independent_acceptance": bind(RUN + "exposition-index-repair104/independent-review/decision104.native.json"),
               "applied_exactly": True, "only_changed_field": "/units/0/steps/0/text",
               "source_theorem_repair": False, "Lean_or_decoder_change": False},
    "claim_boundary": "Normalized refers to actual initial phase law. Neither sigma nor L is asserted to have total mass one or finite mass. Internal Theta preservation is fixed-n only; endpoint-pair reversal is the exported result. No countable averaging or process-invariance credit.",
    "ownership": "The source reviewer independently checked the whole module and every exact-code explanation region after primary-first freeze and fresh anonymous reconstruction.",
    "generated_reader_checked": False, "actual_browser_acceptance": False, "full_Exposition_Seal": False,
    "purified": False, "whole_paper": False
})

slots = {}
judgments = {
    "objects": ("equivalent", "The anonymous reconstruction identifies all30 literal objects, including q times terminal survival, actual Gamma(T), tilted position times stdGaussian, phase-first comap product, sigma, map B sigma and flipped J. Exact sealed private Prop body is unchanged."),
    "domains": ("explicit-elaboration", "Finite real Borel inner-product spaces represent the source Euclidean phase coordinate-free, including rank0. Arbitrary total Hist and Path functions are bookkeeping domains; actual K/Gamma are selected for the sector. No path-space regularity assumption is hidden."),
    "quantifiers": ("equivalent", "All six source assumptions and universal y,r,n,T are reconstructed. z and event tuple are integrated variables in sigma, not a claim that every fixed initial state has an invariant endpoint law. The introductory prose's initial phase names the actual density parameter; its final explicit measure conclusion fixes the quantifier scope."),
    "assumptions": ("equivalent", "Genuine Frechet C2/Hessian lower-and-upper bounds and original eta conditions are retained exactly. Joint measurability, simplex sigma-finiteness and normalized phase identity are producers/internal lemmas, never extra premises."),
    "conclusion": ("explicit-elaboration", "MeasurePreserving J L L is the exact measurable flipped-swap invariant endpoint-pair measure underlying the source single-count change of variables. It does not assert probability/finite sector mass or full process invariance. hsector is the explicit internal normalized parameter-sector ingredient."),
    "scopes": ("equivalent", "Fixed n and finite nonnegative T only, including n0/T0 and empty positive-count zero-horizon sectors. Zero rates/normals and rank0 require no exclusion. The source's later series, signed identity, invariant process and L2 statements remain red."),
    "constant_dependencies": ("equivalent", "Actual sqrt(eta) dynamics/rates, 2eta proximal penalty, unit Gaussian momentum and no factorial normalization are retained. Normalizer is the actual103 partition inverse; its equality is consumed without new constants, cancellation or extra finite-test assumptions.")
}
for name, (relation, evidence) in judgments.items():
    original = expected["semantic_slots"][name]
    if not isinstance(original, str):
        original = "; ".join(original)
    slots[name] = {"original": original, "reconstructed": "\n".join(decoder[name]),
                   "relation": relation, "evidence": evidence}
deltas = [
    {"slot": "domains", "severity": "informational", "description": "Coordinate-free finite real Hilbert Borel presentation includes rank zero.",
     "source": "Finite-dimensional Euclidean phase law.", "lean": "FiniteDimensional real inner-product E with Borel structure and canonical volume.",
     "evidence": "The actual producers preserve the source formulas and Gaussian/volume conventions; no positive-rank hypothesis is introduced.", "blocking": False},
    {"slot": "conclusion", "severity": "informational", "description": "Explicit measure-theoretic completion of one normalized endpoint-pair sector.",
     "source": "Each n-jump term is unchanged under A8 before countable assembly.",
     "lean": "Measurable flipped J and map J L=L; normalized parameter-sector preservation is proved internally.",
     "evidence": "Current201-226 proves the fixed-sector transport with nonnegative tests, without finite integral or sector-mass assumptions.", "blocking": False},
    {"slot": "scopes", "severity": "informational", "description": "Later averaging and process conclusions remain explicitly outside this bounded result.",
     "source": "A.1 proceeds from fixed sectors to countable/signed identity, invariance and L2.",
     "lean": "One actual normalized-initial fixed-count endpoint-pair measure only.",
     "evidence": "Publication supports only normalized-endpoint-sector; weighted-invariance remains an unresolved obligation. All source regions and red nodes are accounted for.", "blocking": False}
]
run_artifact = put("source-review-run104.native.json", {
    "kind": "independent primary-first anti-anchored source/exposition review104",
    "reviewer": REVIEWER, "reviewer_packet_sha256": EXPECTED_PACKET,
    "publication_binding_sha256": EXPECTED_PUBLICATION,
    "packet_RAW": bind(RUN + "reviewer-packet104.json"),
    "primary_first": bind(RUN + "final-source104/primary-first/primary-first-reconstruction104.native.json"),
    "expected_slots": bind(RUN + "final-source104/primary-first/expected-semantic-slots104.native.json"),
    "read_sequence": "Source-only104 expectations and exact primary were frozen before current implementation/prose/decoder; then fresh canonical packet and anonymous reconstruction, all230 production lines and eight authored steps were independently compared. Initial indexing ambiguity was preserved and separately reviewed; only its accepted exact text clarification changed. No prior final fidelity slots/deltas/verdict served as decision input.",
    "prior_context": "Reviewer created source104 graph and reviewed prospective header; this is acknowledged. Independent exact_verifier96 topology admission is reused, not self-validated.",
    "decoder_run": bind(decoder_path + "decoder-run.json"), "decoder_visibility_flags": {k: decoder_run[k] for k in ("source_text_visible", "source_identity_visible", "prior_audit_visible", "repair_proposals_visible")},
    "production": production, "sealed_header": header,
    "compiled_coverage": coverage_artifact, "exposition": exposition_artifact,
    "independent_whole_math": bind(RUN + "independent-whole-math104/whole-math-decision104.native.json"),
    "independently_owned_whole_module_review": True,
    "independently_owned_exposition_review": True,
    "fresh_kernel_reused_not_rerun": True,
    "no_shared_mutation_or_VERIFIED_transition": True
})
review_evidence = "Independent primary-first source, anonymous reconstruction, all230 production lines and eight exact explanation regions agree after the separately accepted step1 indexing clarification. Coverage21/55/96 and four actual parents closed; hsector is explicit. Exact compiled/kernel evidence is separately bound. No AVG/countable/process/sector-mass or full-reader credit."
source_review = {
    "state": "accepted", "reviewer": REVIEWER,
    "independent_from_formalizer": True, "independent_from_decoder": True,
    "reviewer_packet_sha256": EXPECTED_PACKET,
    "publication_binding_sha256": EXPECTED_PUBLICATION,
    "review_run_sha256": run_artifact["raw_sha256"],
    "run_artifact": run_artifact["path"], "evidence": review_evidence,
    "primary_read_before_current_implementation_exposition_decoder": True,
    "source_text_read": True, "source_identity_read": True,
    "prior_final_semantic_verdict_read": False,
    "prior_final_semantic_slots_read": False, "prior_final_deltas_or_repairs_used": False,
    "prior_prospective_header_involvement_acknowledged": True,
    "source_graph_creator": True, "source_graph_self_topology_validation": False,
    "independently_owned_whole_module_review": True,
    "independently_owned_exposition_review": True
}
decision = put("source-review104.native.json", {
    "semantic_slots": slots, "deltas": deltas,
    "verdict": "equivalent-after-elaboration",
    "repairs": [],
    "source_review": source_review,
    "reviewer": REVIEWER, "independent_from_formalizer": True, "independent_from_decoder": True,
    "review_evidence": review_evidence,
    "reviewer_packet_sha256": EXPECTED_PACKET,
    "publication_binding_sha256": EXPECTED_PUBLICATION,
    "review_run_sha256": run_artifact["raw_sha256"],
    "compiled_source_coverage": coverage_artifact, "bounded_exposition": exposition_artifact,
    "authored_notation_clarification": "Separate accepted exposition-only repair recorded in exposition104; repairs=[] because no source theorem, Lean statement or proof repair is required.",
    "no_full_paper_or_process_invariance_credit": True,
    "no_generated_or_browser_reader_acceptance": True
})
owned = []
for path in sorted(OUT.rglob("*")):
    if path.is_file():
        owned.append(bind(path.relative_to(ROOT).as_posix()))
owned_paths = {item["path"] for item in owned}
for item in owned:
    data = (ROOT / item["path"]).read_bytes()
    assert b"\r" not in data
    assert data.endswith(b"\n") and not data.endswith(b"\n\n")
    assert all(line.rstrip() == line for line in data.splitlines())
manifest = put("closed-RAW-final-source104.native.json", {
    "kind": "immutable final source104 exact RAW closure",
    "reviewer": REVIEWER, "reviewer_packet_sha256": EXPECTED_PACKET,
    "publication_binding_sha256": EXPECTED_PUBLICATION,
    "inputs": [item for path, item in sorted(inputs.items()) if path not in owned_paths],
    "owned_outputs": owned, "decision": decision, "run": run_artifact,
    "self_hash_intentionally_omitted": True,
    "no_full_primary_copy": True,
    "native_bytes_immutable_after_close": True
})
print(json.dumps({"decision": decision, "coverage": coverage_artifact, "exposition": exposition_artifact,
                  "run": run_artifact, "manifest": manifest}, indent=2))
