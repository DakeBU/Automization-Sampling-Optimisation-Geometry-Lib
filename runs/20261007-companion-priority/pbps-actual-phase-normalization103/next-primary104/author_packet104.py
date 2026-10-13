import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path("E:/Samplinglib")
OUT = ROOT / "runs/20261007-companion-priority/pbps-actual-phase-normalization103/next-primary104"
BASE = "runs/20261007-companion-priority/"
P103 = BASE + "pbps-actual-weighted-sector102/next-primary103/"
PRIMARY = BASE + "phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html"
AUTHOR = "/root/source_final96"
inputs = {}


def binding(path):
    data = (ROOT / path).read_bytes()
    item = {"path": path, "raw_sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    inputs[path] = item
    return item


def read_json(path):
    binding(path)
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save(name, data):
    path = OUT / name
    assert not path.exists(), str(path)
    path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return binding(path.relative_to(ROOT).as_posix())


primary = binding(PRIMARY)
assert primary["raw_sha256"] == "d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760"
primary_bytes = (ROOT / PRIMARY).read_bytes()
inventory = read_json(P103 + "source-coverage-delta103.native.json")
regions = []
for old in inventory["regions"]:
    item = {k: old[k] for k in ("id", "line_start", "line_end", "byte_start", "byte_end_exclusive", "raw_sha256")}
    assert hashlib.sha256(primary_bytes[item["byte_start"]:item["byte_end_exclusive"]]).hexdigest() == item["raw_sha256"]
    if item["id"] in ("standing-curvature", "standing-eta"):
        disposition = "Original source assumptions retained without strengthening."
    elif item["id"] in ("target-position-energy", "phase-gibbs-law"):
        disposition = "Actual normalized initial phase measure, using NORM103; no normalization re-proof."
    elif item["id"] in ("simplex", "prescribed", "A7"):
        disposition = "Actual finite prescribed density and terminal endpoint; joint density measurability and simplex measure are required ingredients."
    elif item["id"] in ("A8", "unweighted-transform"):
        disposition = "Actual endpoint/time substitution and endpoint-pair flipped swap; same-witness alignment is internal."
    elif item["id"] == "average":
        disposition = "Only initial-law integration for a single fixed count is selected. Series assembly and full process identification remain red."
    elif item["id"] == "weight-matching-and-invariance":
        disposition = "Select 3210-3215 fixed-sector matching as a normalized endpoint-pair measure identity. Exclude 3216-3227 signed assembly, invariance and L2."
    elif item["id"] == "source-license":
        disposition = "ArXiv perpetual nonexclusive distribution license retained. Only source references and authored reconstruction; no full primary copy."
    else:
        disposition = "Unchanged inherited ingredient or excluded boundary; no new proof credit. In particular no jumpwise right-continuous reversal, energy proof, rate-product proof or L2 claim."
    item["disposition104"] = disposition
    regions.append(item)
assert len(regions) == 21
graph103 = binding(P103 + "source-proof-graph-delta103.native.json")
overlay103 = binding(P103 + "graph-normalization103/source-api-identity-normalization103.native.json")
topology103 = binding(BASE + "pbps-phase-normalization-preread103/independent-header-math103/source-topology-admission103.native.json")
compiled103 = binding(BASE + "pbps-actual-phase-normalization103/final-source103/compiled-source-coverage103.native.json")
handoff = ROOT / "docs/companion-papers-handoff.md"
context = {
    "path": handoff.relative_to(ROOT).as_posix(),
    "observed_raw_sha256": hashlib.sha256(handoff.read_bytes()).hexdigest(),
    "role": "Mutable scheduling context read before recommendation; not a mathematical input and not required to remain unchanged.",
    "observed_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "completion_caveat": "At assignment science103 was committed at 030f4f70feb3641cafca981ee81c48a2687db1ee and exact admission/integration was pending. This packet makes no delivery or aggregate-gate assertion."
}
conditions = [
    "0 < (alpha : Real), with alpha beta : NNReal",
    "alpha <= beta",
    "ContDiff Real 2 V",
    "For every x v : E, alpha*norm(v)^2 <= (fderiv Real (fderiv Real V) x v) v <= beta*norm(v)^2",
    "0 < eta, eta : Real",
    "(beta : Real)*eta <= 1"
]
reds = [
    "Identify the countable sum of endpoint sectors with the actual full finite-horizon process law and justify initial-law averaging of that sum.",
    "Countable Tonelli assembly, bounded signed decomposition and the displayed full bilinear operator identity.",
    "Invariant probability for the actual full process, L2 adjoint identity/hypocoercivity and any semigroup or restart/Markovness result.",
    "Finite/subprobability mass of each endpoint sector is not part of this target, even though actual finite-count law APIs may later prove it.",
    "Implementation/discretization error, oracle cost, Gaussian Cloud/midpoint composition and full-paper or whole-Goal completion."
]
first = save("primary-first104.native.json", {
    "kind": "primary-first bounded source reconstruction", "author": AUTHOR,
    "primary": primary, "source_license": regions[-1],
    "read_order": "Pinned primary Eq3.1 and Appendix A.1 reread before selecting the candidate and consulting actual93/97/102/103 interfaces. No104 header, implementation or decoder exists or was inspected. Prior103 reviewer involvement is acknowledged.",
    "source_reconstruction": "The paper integrates A7 against the normalized phase law, reverses endpoint and event tuple by A8, and says each fixed jump-count term is unchanged. Before summing counts, this identifies the joint initial/terminal phase sector with its momentum-flipped swap. The proposed endpoint-pair measure statement is an explicit measure-theoretic completion of that single-count assertion, not the printed full operator identity.",
    "selected_anchors": [{"lines": [1411, 1422], "role": "actual normalized phase law"}, {"lines": [3148, 3169], "role": "strict simplex, prescribed path, actual density"}, {"lines": [3171, 3198], "role": "initial integration and endpoint/time map"}, {"lines": [3200, 3215], "role": "weight matching and single-count substitution"}],
    "original_six_conditions": conditions, "all21_source_slices_rehashed": True,
    "context": context, "graph_self_validation": False, "proof_credit": False
})

module_dir = "AutoSamplingTheory/ExampleCases/ProximalBPS/"
producers = {}
for tag, filename, theorem, role in [
    ("MEASDENS93", "ActualFiniteCountPath.lean", "actual_finite_count_path_law", "Joint actual density measurability; do not assume this is publicly exported by102."),
    ("ACTUAL97", "ActualEndpointTimeReversal.lean", "actual_endpoint_time_reversal_laws", "Same witness supplies TIME97 coordinates, joint actual endpoint/Theta measurability and endpoint inverse A(RA,rho t)=Rz."),
    ("SECTOR102-UNNORM", "ActualWeightedSector.lean", "actual_weighted_sector_lintegral", "All measurable ENNReal tests under actual unnormalized W; own rho coordinate witness."),
    ("NORM", "ActualPhaseNormalization.lean", "actual_phase_gibbs_normalization", "Positive finite actual phase partition and normalized density equals tilted position law times stdGaussian.")
]:
    producers[tag] = {"artifact": binding(module_dir + filename), "declaration": theorem, "role": role}
sector_text = (ROOT / (module_dir + "ActualWeightedSector.lean")).read_text(encoding="utf-8")
literal20 = sector_text[sector_text.index("    let c :"):sector_text.index("    let R :")]
assert len(re.findall(r"^    let ", literal20, flags=re.M)) == 20
recommendation = save("recommendation104.native.json", {
    "kind": "one prospective substantive endpoint-pair measure edge", "author": AUTHOR,
    "selection": "Actual normalized fixed-count endpoint-pair reversal",
    "proposed_name": "actual_normalized_endpoint_sector_reversal",
    "ambient": "For every finite-dimensional real inner-product space E with its Borel measurable structure, V:E->Real, alpha beta:NNReal, eta:Real, under the original six conditions.",
    "conditions": conditions,
    "literal_definition_contract": {"source": producers["SECTOR102-UNNORM"]["artifact"], "first20_names": ["c", "Phi", "S", "rate", "Lambda", "Rec", "Hist", "Delta", "Prefix", "zAt", "K", "qReal", "q", "liveTime", "d", "weight", "Path", "Psi", "Gamma", "rho"], "exact_existing_definition_text_LF": literal20, "status": "Existing definitions quoted for exact interface binding only; not a new header or implementation."},
    "remaining_definitions": [
        "H=E×E, in position then momentum order. R(x,p)=(x,-p).",
        "Vy(y,x)=V(x)+norm(x-y)^2/(2*eta). piY(y)=volume.tilted(x -> -Vy(y,x)).",
        "nu(y)=piY(y).prod(stdGaussian E), exactly the actual source phase law, not a supplied arbitrary measure.",
        "m(n,T)=Measure.comap(Subtype.val)(volume on Fin n -> Real), on Prefix n T. This is unnormalized ordered-simplex volume; no factorial multiplier.",
        "X(n,T)=H×Prefix n T, phase first. A(y,r,n,T)(z,t)=Gamma y r z n T t evaluated at <T,le_rfl>.",
        "sigma(y,r,n,T)=((nu(y)).prod(m(n,T))).withDensity(q -> rho y r q.1 n T q.2).",
        "B(y,r,n,T)(q)=(q.1,A(y,r,n,T)(q)) in H×H; L(y,r,n,T)=Measure.map B sigma.",
        "J:H×H->H×H, J(z0,zT)=(R(zT),R(z0))."
    ],
    "single_public_conclusion": "For every n:Nat, T:NNReal, y r:E, MeasurePreserving J (L(y,r,n,T)) (L(y,r,n,T)). Equivalently, the globally measurable flipped swap pushes the actual normalized endpoint-pair sector measure to itself.",
    "quantifier_note": "n,T,y,r all universal. No public event-time-reversal witness, observable, normalizer, density, finiteness, measurability or integrability provider is a binder. Internal rho-time witnesses are identified by coordinates.",
    "normalization_constant": "Internally U=Vy+norm(p)^2/2, w=exp(-U), ell=volume.prod volume, Zphase=lintegral ofReal(w) ell, C=(sqrt(2*pi))^finrank(E), Zphase=ofReal(Zx*C), cNorm=Zphase^-1. sigma=(ell.prod m).withDensity(q -> cNorm*ofReal(w(q.1))*rho(q)). All constants are actual; no new parameter.",
    "actual_consumer": "AVG100 can apply this measure equality to endpoint tests F(z0)G(zT), then assemble actual count sectors. The target supplies actual normalized initial-law integration and endpoint transport, which102 alone does not export.",
    "why_substantive": "One actual measure interface joins normalized Gibbs law, true prescribed density, event-simplex measure and terminal path endpoint. It requires density/product adapters, measurable pushforward, common-witness alignment and endpoint commutation; it is not a one-line specialization F=f*g(A).",
    "seven_step_route": [
        "Extract actual93 joint rho measurability and actual97 joint A/Theta measurability. Derive measurability of strict Delta and SigmaFinite(m) via map_comap_subtype_coe, volume.restrict and SigmaFinite.of_map.",
        "Use actual103 to identify the actual product phase law with ell.withDensity(cNorm*ofReal w), with finite positive Zphase. No repeat of normalization analysis.",
        "Use prod_withDensity_left and withDensity_mul, with actual measurable densities and SFinite(m), to rewrite sigma as (ell.prod m).withDensity(cNorm*W).",
        "Extract97 and102 reversal witnesses. TIME97 and the coordinate conjunct of102 identify them by extensionality on Prefix and Fin coordinates; then retain endpoint inverse and Theta measurability for that same witness.",
        "Multiply102's all-test equality by cNorm, use lintegral_withDensity and lintegral_map, and Measure.ext_of_lintegral to obtain MeasurePreserving Theta sigma sigma. This completes the existing normalized SECTOR100 internal node.",
        "Use97's actual endpoint inverse to prove B(Theta q)=J(B q), with B and J measurable; use R involution only as the literal coordinate fact.",
        "Push sigma forward by B and use map_map plus the commutation identity to obtain the single exported MeasurePreserving J L L conclusion."
    ],
    "edge_cases": {
        "n0": "Prefix 0 T is the unique empty tuple; no jump factors, final actual flow from z0. Include T=0.",
        "T0_positive_n": "Strict positive ordered times below zero give an empty Prefix. Sector measure is zero; no division by simplex mass.",
        "rank0": "Volume/Gaussian conventions inherited unchanged. C=1; positive-count rates vanish, with no positive-dimension premise.",
        "zero_normal_or_rate": "Existing total reflection definition and nonnegative density retained; no rate division or strict positive-rate premise.",
        "endpoints_and_jumps": "Use actual endpoint at finite T and strict interior event times. No pointwise right-continuous path reversal at jumps is asserted.",
        "infinite_integrals": "All measure/extensionality arguments allow infinite nonnegative integrals. No signed integrability or finite sector mass claim."
    },
    "source_completion_delta": "Endpoint-pair measure equality packages the fixed-count change of variables stated in A.1. All measurable nonnegative endpoint tests are covered; the paper phrases the step for bounded tests. This is explicit elaboration, not a full semigroup claim.",
    "remaining_reds": reds, "proof_credit": False, "header_created": False,
    "readiness": "Analytically dependency-ready on actual93/97/102/103 interfaces; scheduling/proof must wait for root's103 delivery/admission boundary."
})

slots = save("expected-semantic-slots104.native.json", {
    "kind": "source-only seven expected slots", "primary_first": first,
    "objects": "Actual normalized Gibbs initial phase law, actual finite prescribed density rho=q*terminal survival, actual Gamma endpoint, strict simplex comap volume, endpoint-pair pushforward L and flipped swap J.",
    "domains": "Finite-dimensional real Borel inner-product E including rank zero; H=E×E; n:Nat,T:NNReal; X=H×Prefix n T; L on H×H. No path-space topology is substituted.",
    "quantifiers": "Ambient parameters under six original conditions; forall n T y r, MeasurePreserving J L L. No externally supplied reversal witness or density.",
    "assumptions": conditions,
    "conclusion": "Exactly actual normalized fixed-count endpoint-pair reversal measure preservation. Normalized initial law does not assert normalized sector mass.",
    "scopes": "Fixed finite count and finite deterministic horizon only. No sum over counts, full process invariance, signed operator identity, all-time jump reversal, restart or cost.",
    "constant_dependencies": "eta and actual V,y,r retained. Position Gaussian penalty 1/(2eta), momentum 1/2, rate sqrt(eta), exact phase normalizer with C=(sqrt(2pi))^dim. No artificial normalizing factorial or hidden constants.",
    "source_hypothesis_vs_ingredient": "Measurability, simplex sigma-finiteness, normalizer positivity, actual density equality, witness matching and endpoint commutation are internal producer/adapter obligations, never new binders.",
    "proof_credit": False
})

mathlib_dir = ".lake/packages/mathlib/Mathlib/MeasureTheory/"
apis = [
    ("Measure/WithDensity.lean", "MeasureTheory.prod_withDensity_left", "Measurable initial density and SFinite second measure m; cannot omit the m side condition."),
    ("Measure/WithDensity.lean", "MeasureTheory.withDensity_mul", "Both density factors measurable; preserves actual multiplication order up to proved commutativity."),
    ("Measure/WithDensity.lean", "MeasureTheory.lintegral_withDensity_eq_lintegral_mul", "Actual density and observable measurability, no finite integral requirement."),
    ("Integral/Lebesgue/Map.lean", "MeasureTheory.lintegral_map", "Measurable test and map."),
    ("Integral/Lebesgue/Basic.lean", "MeasureTheory.Measure.ext_of_lintegral", "Equality on all measurable ENNReal tests; no finite mass assumption."),
    ("Integral/Lebesgue/Add.lean", "MeasureTheory.lintegral_const_mul", "Measurable integrand; no finiteness assumption."),
    ("Measure/Map.lean", "MeasureTheory.Measure.map_map", "Both maps measurable."),
    ("Measure/Restrict.lean", "map_comap_subtype_coe", "Global declaration outside MeasureTheory namespace; measurable strict-simplex set."),
    ("Measure/Typeclasses/SFinite.lean", "MeasureTheory.SigmaFinite.of_map", "AEMeasurable subtype inclusion and sigma-finite pushed-forward measure.")
]
retrieval = save("retrieval104.native.json", {
    "kind": "bounded local and fixed-Mathlib retrieval", "actual_producers": producers,
    "fixed_apis": [{"declaration": name, "artifact": binding(mathlib_dir + path), "contract": contract} for path, name, contract in apis],
    "toolchain": binding("lean-toolchain"), "manifest": binding("lake-manifest.json"),
    "external_catalog": binding("research-wiki/external-lean-libraries/README.md"),
    "search_scope": "PBPS and TechnicalLemmas searched for normalized sector/endpoint measure results; existing102 remains unnormalized. Existing103 reuses shared Gibbs/Gaussian analysis, so no new upstream port is needed. Fixed Mathlib already supplies all measure adapters.",
    "compatible_upstream": "External catalog is reference-only. No SLT/ATLAS/OpenAI declaration is imported, ported or credited; no external theorem is needed for this candidate.",
    "public_private_boundary": "The sigma-finite subtype recipe appears in actual97 implementation, but its private endpoint_data is not a new callable public parent. Derive the measurable strict-simplex adapter locally from literal Delta.",
    "namespace_warning": "prod_withDensity_left is in MeasureTheory, not MeasureTheory.Measure. map_map and Measure.ext_of_lintegral have Measure namespace components.",
    "no_proof_search": True
})

graph = save("source-proof-graph-delta104.native.json", {
    "kind": "prospective minimal source graph delta", "author": AUTHOR,
    "base_source_graph103": graph103, "effective_api_identity_overlay103": overlay103,
    "independent_base_topology_admission": topology103, "compiled_base_coverage": compiled103,
    "inherited_count": {"nodes": 51, "edges": 79},
    "stable_identity_policy": "Keep NORM, SECTOR102-UNNORM, SECTOR100, TIME97, THETA97, TERM97, MEASDENS93, AVG100 and all inherited identities. RHO97 remains only the existing display alias of TIME97. New ENDPOINT97 is a distinct public endpoint-inverse/measurability projection, not another time-coordinate node or the TERM97 terminal-flow formula.",
    "new_nodes": [
        {"id": "SECTOR-MEASURE104", "content": "Actual normalized sigma rewritten as cNorm*W density over ell.prod m; includes measurable-density and sigma-finite simplex adapters."},
        {"id": "ALIGN104", "content": "Identify actual97 and actual102 rho-time witnesses by their coordinate conjuncts; all y,r use the same witness."},
        {"id": "ENDPOINT97", "content": "Previously available public97 projection: joint actual A measurability and A(RA,rho t)=Rz, under the same witness as TIME97/THETA97."},
        {"id": "ENDPAIR104", "content": "Selected public actual normalized endpoint-pair measure preservation under flipped swap; includes B-Theta/J-B commutation and measurable pushforward."}
    ],
    "public_projection_bindings": {"ENDPOINT97": producers["ACTUAL97"], "TIME97": producers["ACTUAL97"], "THETA97": producers["ACTUAL97"]},
    "projection_note": "ENDPOINT97 is not inferred from measure preservation alone. All three facts are sibling projections of the full actual97 theorem, with its one existential witness.",
    "AND_dependency_groups": [
        {"sources": ["H99", "D99"], "target": "ENDPOINT97", "ingredients": ["public actual97 joint endpoint measurability and endpoint inverse projections; same witness as TIME97/THETA97"], "status": "existing producer projection, not104 proof credit"},
        {"sources": ["NORM", "MEASDENS93", "D99", "DEFWEIGHT101"], "target": "SECTOR-MEASURE104", "ingredients": ["actual continuous Gibbs density", "measurable Delta -> SigmaFinite m", "prod_withDensity_left", "withDensity_mul"]},
        {"sources": ["TIME97", "SECTOR102-UNNORM", "D99"], "target": "ALIGN104", "ingredients": ["coordinate conjuncts from both public producers", "Subtype.ext and coordinate extensionality"]},
        {"sources": ["NORM", "SECTOR102-UNNORM", "SECTOR-MEASURE104", "ALIGN104", "THETA97"], "target": "SECTOR100", "ingredients": ["all-test102", "constant extraction", "lintegral_withDensity", "lintegral_map", "Measure.ext_of_lintegral"]},
        {"sources": ["SECTOR100", "ENDPOINT97", "ALIGN104", "D99"], "target": "ENDPAIR104", "ingredients": ["joint endpoint measurability", "R coordinate measurability/involution", "actual endpoint inverse", "map_map"]},
        {"sources": ["ENDPAIR104", "A795"], "target": "AVG100", "status": "future only; countable/actual-process identification and signed conditions still red"}
    ],
    "producer_edges": [{"source_declaration": producers["ACTUAL97"]["declaration"], "source_artifact": producers["ACTUAL97"]["artifact"], "target": "ENDPOINT97", "logic": "public projection, not a separate graph-node identity or new proof"}],
    "existing_edge_policy": "Inherited NORM+SECTOR102-UNNORM -> SECTOR100 aggregate dependency is refined by the explicit density/measurability/witness adapters above; predecessors are not edited. No102 -> NORM edge is introduced.",
    "api_dependencies": retrieval, "topology_status": "creator-authored, awaiting independent topology validation",
    "self_topology_validation": False, "certified_Lean_edges_added": False, "proof_credit": False
})

coverage = save("source-coverage-delta104.native.json", {
    "kind": "bounded source-only coverage", "primary": primary,
    "inherited21_inventory": binding(P103 + "source-coverage-delta103.native.json"),
    "all21_slices_rechecked": True, "regions": regions,
    "selected_target": "ENDPAIR104", "internal_completed_if_proved": ["SECTOR-MEASURE104", "ALIGN104", "SECTOR100"],
    "existing_projection_not_new_proof": "ENDPOINT97",
    "changed_required_slice": "Eq3.1 actual normalized law + A7 actual single-count density + A8 actual endpoint/time substitution -> normalized endpoint-pair sector law. No countable or signed operator assembly.",
    "graph_delta": graph, "remaining_reds": reds,
    "implementation_coverage": "Not applicable. No104 header or implementation exists or is inspected.",
    "source_gap": "The printed bounded-test termwise change of variables is completed as an actual endpoint-pair measure identity; measurable densities, product conventions and same-witness contracts must be discharged explicitly.",
    "self_topology_validation": False, "proof_credit": False
})
run = save("preread-run104.native.json", {
    "author": AUTHOR, "kind": "closed source-only prerequisite packet",
    "primary_first": first, "recommendation": recommendation, "expected_slots": slots,
    "retrieval": retrieval, "graph": graph, "coverage": coverage,
    "current_delivery_context": context,
    "no_header": True, "no_proof": True, "no_claim_or_seal": True,
    "no_shared_mutation": True, "no_full_primary_copy": True,
    "graph_requires_independent_review": True
})
owned = []
for path in sorted(OUT.iterdir()):
    if path.is_file():
        data = path.read_bytes()
        assert b"\r" not in data
        assert data.endswith(b"\n") and not data.endswith(b"\n\n")
        assert all(line.rstrip() == line for line in data.splitlines())
        owned.append(binding(path.relative_to(ROOT).as_posix()))
owned_paths = {item["path"] for item in owned}
manifest = save("closed-RAW-manifest104.native.json", {
    "kind": "immutable exact-RAW source-only closure", "author": AUTHOR,
    "inputs": [item for path, item in sorted(inputs.items()) if path not in owned_paths],
    "owned_outputs": owned, "run": run,
    "mutable_context_policy": "Current handoff is recorded in the run as scheduling observation only; it is not required mathematical input or immutable closure evidence.",
    "closure_scope": "All listed owned files immutable after this close. No self-hash cycle; manifest identity is reported externally.",
    "proof_credit": False, "topology_self_validation": False
})
print(json.dumps({"recommendation": recommendation, "graph": graph, "coverage": coverage, "run": run, "manifest": manifest}, indent=2))
