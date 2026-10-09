from pathlib import Path
import copy, hashlib, json, os, subprocess, sys

root = Path.cwd()
base = Path('runs/20261007-companion-priority')
pre = base / 'pbps-harmonic-flow-preproof73'
prior = base / 'pbps-b4-corrector-perturbation72'
r = base / 'pbps-actual-harmonic-flow73'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
def write(p, x):
    p = Path(p)
    assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

seal = load(pre / 'root.statement-seal73.json')
assert seal['status'] == 'SEALED_BEFORE_PROOF_SEARCH_NOT_A_PROOF'
for z in seal['exact_headers']:
    assert sha(Path(z['path']).read_bytes()) == z['RAW_sha256']
assert load(prior / 'root.exact-verification72.adoption.json')['native_verified']
assert load(prior / 'root.repository72.adoption.json')['accepted_scoped_aggregate']
assert load(prior / 'integration72/github-push-record/summary.json')['status'] == 'SUCCESS'
for name in ['root.source-first73.adoption.json', 'root.sourcegraph73.extraction-adoption.json', 'root.header-math73.adoption.json', 'root.header-source73.adoption.json']:
    assert (pre / name).is_file(), name
files, names = seal['proposed_files'], seal['declarations']
assert len(files) == len(names) == 1 and all(not Path(p).exists() for p in files)
cid = 'ASTIS-SW-PBPS-actual-harmonic-flow'
aid = 'ASTIS-SA-20261010-PBPSActualHarmonicFlow'
owner = 'companion_root_20261005'
gradient = 'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one'
delta, source, boundary = seal['mathematical_delta'], seal['source_anchor'], seal['truth_boundary']
r.mkdir(exist_ok=False)
for label, args in [('harness-reconcile', ['tools/astis.py', 'harness-reconcile', '--json']), ('capsule', ['tools/astis_advance.py', 'capsule'])]:
    with (r / (label + '.stdout.json')).open('wb') as out, (r / (label + '.stderr.log')).open('wb') as err:
        cmd = [sys.executable, '-X', 'utf8', *args]
        child = subprocess.Popen(cmd, stdout=out, stderr=err)
        code = child.wait()
    write(r / (label + '.receipt.json'), dict(command=cmd, actual_PID=child.pid, exit_code=code, terminal_closed=True))
    assert code == 0, (label, code)
sys.path.insert(0, str(root / 'tools'))
import astis_advance as adv
ledger = Path('runs/substantive_advances.jsonl')
before = ledger.read_bytes()
write(r / 'ledger.before73.pin.json', dict(path=ledger.as_posix(), RAW_bytes=len(before), RAW_sha256=sha(before)))
proposal = adv.AdvanceProposal(advance_id=aid, task_id='ASTIS-SW-PBPS-2026', goal=delta, source_anchor=source, theorem_delta=delta, truth_boundary=boundary, created_by=owner, dag_inputs=(gradient,), proposed_files=tuple(files), focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow',), modes=('faithfulPaper',), priority=100, frontier_cell=cid, target_declarations=tuple(names))
adv.propose_advance(proposal)
adv.transition_advance(aid, 'CLAIMED', worker_id=owner, evidence=dict(statement_seal=(pre / 'root.statement-seal73.json').as_posix(), owned_files=files))
adv.transition_advance(aid, 'EXPLORING', worker_id=owner, evidence=dict(route='Actual c/Phi/H; internal gradient continuity; trigonometric group/derivative laws; weighted norm-square cancellation; exact pi endpoint.', truth_boundary=boundary))
after = ledger.read_bytes()
assert after[:len(before)] == before
(r / 'ledger.claim73.append.exactraw.jsonl').write_bytes(after[len(before):])
write(r / 'claim.json', proposal.as_event())

c = copy.deepcopy(load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-perturbation.json'))
consumers = ['PBPS Proposition3.1 fixed-reference PDMP construction/nonexplosion: deterministic harmonic segment before bounce/rate/clock recursion', 'Actual Algorithm1 pi-terminal position kernel, after separate measurable stochastic construction and invariance proof']
searched = ['Exact source-first finite retrieval: ' + seal['library_retrieval']['path'], 'Independent73 gradient producer audit and prospective header math API typing; fixed Mathlib trigonometric/derivative/Hilbert/Borel APIs.']
reason = 'Actual source input center depends on gradient V. Reuse the canonical gradient continuity producer; implement one deterministic arc theorem. No duplicate Flow structure, probability reference law, corrector-algebra dependency or invented second shared consumer.'
c.update(schema_version=3, cell_id=cid, title='Actual PBPS harmonic arcs, ODE, conserved weighted energy and half-turn', source_anchor=source, target_statement=Path(seal['exact_headers'][0]['path']).read_text(encoding='utf8'), status='claimed', parents=[gradient], consumers=consumers, blocked=dict(status=False, reason='Independent source/topology and exact header accepted; Statement Seal fixed; theorem proof not yet implemented.'), source_targets=names)
c['evidence'] = dict(substantive_advance=aid, statement_seal=(pre / 'root.statement-seal73.json').as_posix(), focused_checks=[], owned_files=files, truth_boundary=boundary)
c['shared_floor_audit'] = dict(searched=searched, classification='missing', decision='new_route_local', canonical_declaration=names[0], canonical_shared_cell='', reason=reason)
c['reuse_plan'] = dict(searched_existing=searched, reused_declarations=[gradient], new_shared_declarations=[], known_consumers=[], planned_consumers=consumers, no_duplicate_wrapper=True, decision_reason=reason)
c['statement_seal'] = dict(evidence=(pre / 'root.statement-seal73.json').as_posix(), source_revision=seal['source_revision'], statement_version=1, signature_digest=sha(json.dumps(seal['exact_headers'], sort_keys=True, separators=(',', ':')).encode()), binder_audit=seal['binder_audit'], definition_kind='Complete private literal of actual c/Phi/H and all nine conclusions; same six source-standing callers. No proof provider.')
c['source_proof_coverage'] = dict(source_graph=seal['source_graph']['path'], source_inventory=(pre / 'independent-header-source73/StageA.independent-source79-classification73.frozen.json').as_posix(), coverage_report=seal['binder_audit'], coverage_status='Independent prospective source topology/header only:13 regions51 blocks79 semantic items24NODE55EXCLUDED;23 nodes37 edges7 SOURCE_GAP;20 binders4SOURCE6STANDING10TYPING0EXCESS. Implementation coverage pending.')
c['source_detail_audit'] = dict(primary_edition=seal['source_revision'], primary_anchor=source, fidelity_boundary=boundary, detail_status='cites_external', gap='Seven internal omitted-source bridges remain proof obligations; no stochastic dynamics/kernel/nonexplosion/invariance credit.', source_preread=seal['source_expectations']['path'], consulted=[dict(source='PBPS fixed v1 Algorithm1/Section3/AppendixA.1; fixed Mathlib and canonical Gradient', anchor=source, hypothesis_adapter='Source C2 supplies gradient continuity internally; eta>0 supplies reciprocal cancellation. No extra analytic premise, dimension positivity or strict cap.', expanded_binder_audit=seal['binder_audit'])])
c['proof_digestion'] = dict(existing_substrate=[gradient], bookkeeping=['Keep the exact source center and literal weighted SUM energy.'], new_reusable=[], new_topology=delta)
c['purification'] = dict(status='pending', dead_code_audit='Pending implementation; one actual deterministic theorem.', duplicate_semantics_audit='Existing corrector algebra/reference-law kernels do not construct this flow.', canonicalization='One actual explicit harmonic arc; Mathlib Flow packaging optional and unnecessary.', compressed_spine_delta=delta, reader_default_view='Complete attributed statement plus stepwise formulas and exact adjacent folded Lean.', scope=boundary)
lc = c['learning_contract']
lc['failure_class'] = 'NONE'
lc['salvage'] = dict(required=False, status='not-applicable', reason='No proof attempt before claim; prospective source/math evidence and sealed header retained.', promoted_fragments=[], discarded_fragments=[])
lc['parallelism'].update(decision='serial', direction_fingerprints=['actual-harmonic/Phi/ODE/weighted-sum'], shared_verified_context_digest=load(pre / 'root.header-source73.adoption.json')['whole_logical_run_sha256'], expected_information_gain='Sole proving writer; distinct fresh mathematics, strict blind reconstruction and anti-anchored source verification after focused compile.')
lc['reader_backpressure'].update(purification_status='pending', exposition_seal_status='pending', exposition_evidence='', lean_expansion_nodes=names, source_expansion_nodes=['actual-center', 'joint-continuous-Borel', 'group-inverse', 'actual-ODE', 'weighted-energy', 'pi-endpoint', 'stochastic-construction-open'], assumptions_preserved=True, boundary_preserved=True)
c['graph_contribution'].update(lean_view='integration-node', overview_view='updated', functor_view='none-found', focus_targets=names, visual_review='Pending focused proof and independent review; no new graph layer.')
c['conceptual_mirror_audit'] = dict(status='pending', discovery_ids=[], reason='Audit before PROVED_LOCAL; deterministic trigonometric energy symmetry does not imply invariant probability dynamics.')
write(Path('research-wiki/frontier-cells') / (cid + '.json'), c)
write(r / 'preproof-admission.json', dict(status='CLAIMED_EXPLORING_NOT_PROVED', actual_root_PID=os.getpid(), checked_parent=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(), statement_seal=(pre / 'root.statement-seal73.json').as_posix(), theorem_delta=delta, truth_boundary=boundary, active_cells=[cid], production_declarations=names, Goal_complete=False))
print(aid, 'EXPLORING: actual deterministic flow only; no dependency on72 algebra; no proof credit.')
