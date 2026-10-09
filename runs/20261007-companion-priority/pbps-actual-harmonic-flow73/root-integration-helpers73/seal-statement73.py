from pathlib import Path
import hashlib, json, os

pre = Path('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73')
load = lambda p: json.loads(Path(p).read_bytes())
def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=hashlib.sha256(b).hexdigest(), LF_sha256=hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest())
source = load(pre / 'root.header-source73.adoption.json')
math = load(pre / 'root.header-math73.adoption.json')
header = pin(pre / 'header73.proposed.lean')
assert header['RAW_sha256'] == source['exact_header']['RAW_sha256'] == math['exact_header']['RAW_sha256'] == 'a8a7f0f891906e4635d8b77046ee59ddcc3b3cbaeb37f22e6eff00d26b88a27d'
assert source['anti_anchored'] and source['coverage']['EXCESS'] == 0 and math['no_mathematical_header_repair']
out = dict(schema_version=1, status='SEALED_BEFORE_PROOF_SEARCH_NOT_A_PROOF', actual_root_PID=os.getpid(), source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d', proposed_files=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'], declarations=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws'], exact_headers=[header], source_anchor='PBPS Algorithm1 harmonic arcs, Section3 exact dynamics and AppendixA.1 ODE/weighted-energy formulas; deterministic construction prerequisite for Proposition3.1', source_graph=source['source_graph'], source_expectations=pin(pre / 'independent-header-source73/StageA.source-expectations73.before-header.frozen.json'), binder_audit=source['decision'], math_audit=pin(pre / 'independent-header-math73/header.decision.json'), source_adoption=pin(pre / 'root.header-source73.adoption.json'), math_adoption=pin(pre / 'root.header-math73.adoption.json'), library_retrieval=pin('runs/20261007-companion-priority/pbps-half-turn-construction-preread73/api.retrieval.json'), exact_contract=pin('runs/20261007-companion-priority/pbps-half-turn-construction-preread73/selected-contract.json'), mathematical_delta='Actual centered harmonic flow from the six original analytic callers: joint continuous/Borel, zero/group/both inverse, both exact ODEs, nonnegative conserved weighted SUM energy, exact pi endpoint.', required_internal_source_gaps=7, additional_analytic_public_premises=[], additional_regularity=[], rank_zero_allowed=True, alphaeta_one_allowed=True, zero_energy_allowed=True, no_dependency_on_72_corrector_algebra=True, source_graph_not_Lean_implication=True, signature_policy='Exact complete private literal and six public callers fixed; proof-only imports may extend imports. Mathematical/binder changes require independent review.', failure_policy='After repeated same-shape failures diagnose statement/API/route; never add caller proof ingredients.', truth_boundary='No theorem proof or compiler theorem credit. Bounce/rate, stochastic construction, nonexplosion, Markov/invariance/reversal, actual endpoint H/kernel/B27/B28, main/error/cap/expected-query cost/actual-input composition, reader acceptance, whole-paper/Goal/Exposition/PURIFIED/main/live remain open.', claimed=False, proved=False)
p = pre / 'root.statement-seal73.json'
assert not p.exists()
p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('PASS Statement Seal73 fixed before proof search; exact nine conclusions; seven internal bridges remain; no SAU/proof credit.')
