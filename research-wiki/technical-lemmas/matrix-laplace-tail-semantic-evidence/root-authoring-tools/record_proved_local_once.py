"""One normal mathematical PROVED_LOCAL; no proving-owner VERIFIED call."""
from pathlib import Path
import hashlib,json,subprocess,sys,datetime
r=Path.cwd();sys.path.insert(0,str(r))
from tools import astis_advance as api
w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence'
A='ASTIS-SA-20261114-MatrixLaplaceTail';O='huanjian_20261114_matrix_laplace_tail'
P='AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail.max_eigenvalue_tail_le_iInf_trace_exp'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def ident(p):return {'file':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def git(*args):return subprocess.check_output(['git',*args],env={**__import__('os').environ,'GIT_OPTIONAL_LOCKS':'0'})
carrier=read(w/'metadata-candidate-commit.json')['commit']
assert git('rev-parse','HEAD').decode().strip()==carrier
assert not git('diff','--name-only',carrier).strip(),'Commit owned metadata before normal PL; inspect any actual foreign edit.'
marker=w/'normal-PL-attempted.once.json';assert not marker.exists(),'Inspect actual ledger/marker; do not replay.'
before=(r/'runs/substantive_advances.jsonl').read_bytes()
states=api._replay_advances(json.loads(v) for v in before.splitlines())
assert states[A]['state']=='EXPLORING' and states[A]['owner_id']==O
dbefore=(r/'runs/substantive_discoveries.jsonl').read_bytes()
discovery=api._replay_discoveries(json.loads(v) for v in dbefore.splitlines())
assert discovery['ASTIS-DISC-20261114-ScalarSelfadjointLaplaceTailMechanism']['status']=='validated'
baseline=read(w/'preservation-baseline.private.json')
for p,h in baseline['all_existing_frontier_sha256'].items():assert sha((r/p).read_bytes())==h,p
public=read(r/'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json')
private=read(e/'private-consumer-audit.source-reviewed.v4.json')
assert public['state']==private['state']=='source-reviewed'
assert public['publication_binding_sha256']==private['publication_binding_sha256']=='159708e68a0601d85a6081464aa654ea80b7b58cbf0fa41ac697a03fcd8e4346'
nf=e/'native-originals/laplace_native_61e4';native=read(nf/'native-mathematics-report.v1.json')
assert native['candidate_commit']=='1d1103af694b9663a72b0d610004ed85c7c6b527'
assert native['sorryAx_or_unauthorized_axiom'] is False
gates=read(w/'metadata-candidate-commit.json')['actual_gates']
for g in gates:
    v=read(r/g['receipt']);log=Path(v['log'])
    assert v['exit_code']==0 and v['head_before']==carrier and sha(log.read_bytes())==v['log_sha256']
assert {v['gate'] for v in gates}=={'publication','contributor','semantic','private-semantic','frontier','whitespace'}
cellpath=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL.json'
cell=read(cellpath)
payload={
 'result_kind':'reusable-interface',
 'theorem_delta':(w/'P.proposition.sealed.v1.txt').read_text(),
 'lean_files':['AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean','Tests/GaussianComplexityLaplaceTail.lean'],
 'lean_declarations':[P],'publication_declarations':[P],
 'focused_checks':{'ROOT_actual':cell['evidence']['focused_checks'],'independent_native':ident(nf/'native-mathematics-report.v1.json'),'actual_metadata_gates':gates},
 'truth_boundary':read(r/'website/content/publications/huanjian-matrix-laplace-tail.json')['items'][0]['bindings'][0]['boundary'],
 'conceptual_mirror_audit':cell['conceptual_mirror_audit'],
 'checked_metadata_commit':carrier,'actual_math_commit':native['candidate_commit'],
 'statement_seal':ident(r/'research-wiki/technical-lemmas/matrix-laplace-tail-statement-seal.json'),
 'binder_definition_audit':ident(e/'preproof-originals/binder-inventory-singleton.supplement.v1.json'),
 'preproof_source_admission':ident(e/'preproof-source-admission.json'),
 'source_topology_and_coverage':ident(e/'preproof-originals/source-graph.repaired.v2.1.json'),
 'source_lean_correspondence':ident(e/'source-lean-correspondence.authored-v2.json'),
 'source_blind_decoding':{'actor':'/root/decoder_6f91','originals':str((e/'decoder-originals/anon_6f91').relative_to(r)),'source_visible':False},
 'fresh_source_wholemodule_and_seven_slot':{'actor':'/root/laplace_fresh_source_8d2a','public_binding':public['publication_binding_sha256'],
 'public_verdict':public['verdict'],'private_verdict':private['verdict'],'raw_source_scope_deltas_preserved':True,
 'selected_originals':ident(e/'source-review/laplace_fresh_source_8d2a/selected-source-through-v4-context.originals117.v1.tar.gz')},
 'native_type_value_kernel':{'report':ident(nf/'native-mathematics-report.v1.json'),'selected_public238_originals':ident(nf/'selected-native-originals.public238.v2.tar.gz'),
 'original239_manifest_unchanged':True,'full_repo_inventory_excluded_local_only':True,'actual_parent_witnesses':ident(nf/'actual-canonical-parent-witnesses.v1.json'),
 'std3_only':True,'q0_q0_d2_and_four_cases_checked':True},
 'actual_source_bytes':read(e/'local-mathematics-checkpoint.v1.json')['inputs'],
 'actual_build_identity_qualification':'ROOT checked exact worktree source bytes while HEAD2da2, then froze actual mathematics1d110; independent native rebuilt that immutable11-module source closure. No retroactive Lean build at metadata/public-export identities.',
 'PROVED_LOCAL_reader_snapshot':{'current_authored_context':'v4; latest independent source seven-slot and metadata-only schema review accepted',
 'exact_site_identity':'v4 original103+candidate104 served files byte-identical to v3; independently checked; not a new browser-v4 run',
 'actual_isolated_browser_current_scope':'PENDING separate current-v3 runtime and independent visual acceptance at this local-proof snapshot',
 'production_main_site_purification':'held/not accepted'},
 'proof_digestion':{'existing_substrate':['Mathlib CFC/spectral theorem/trace and scalar nonnegative Markov','Existing genuine Gaussian Radius/Structure/Mean closure'],
 'bookkeeping':'AE direct-trace event comparison and reciprocal/infimum algebra; actual four signed weighted Gaussian sum regularity and finite trace-exponential expectation.',
 'new_reusable':[P],'new_topology':'No novelty claim; sufficient direct-trace route combines source elementary comparisons. Stronger GC.FINITE.MGF all-real/strict-trace/explicit-r²-cap full node remains open.'},
 'private_consumer_scope':'Literal original unconditional Gaussian law, inclusive own-row cutoff, actual means, paired Gaussian-first coordinates, all four signs/weights, all positive s and real a, q=0. Integrability/positivity derived internally; no separate public T node or sign-law/MGF symmetry.',
 'preservation_scope':'One normal target-only PL append; old prefixes, all foreign advance/discovery states and original474 frontiers protected; HEAD/index unchanged during the API window; full guard maps stay local.'
}
assert len(payload)==24
dump(e/'PROVED_LOCAL-evidence.full.json',payload)
dump(marker,{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'planned_normal_PL_calls':1,
 'payload_sha256':sha((e/'PROVED_LOCAL-evidence.full.json').read_bytes()),'executed_driver_sha256':sha(Path(__file__).read_bytes()),'checked_metadata_commit':carrier})
indexpath=Path(git('rev-parse','--git-path','index').decode().strip());indexpath=indexpath if indexpath.is_absolute() else r/indexpath
indexbefore=sha(indexpath.read_bytes())
api.transition_advance(A,'PROVED_LOCAL',worker_id=O,modes=['proof-design','compiler-diagnosis','source-review'],evidence=payload)
after=(r/'runs/substantive_advances.jsonl').read_bytes();assert after.startswith(before)
delta=[json.loads(v) for v in after[len(before):].splitlines()]
assert len(delta)==1 and delta[0]['advance_id']==A and delta[0]['to_state']=='PROVED_LOCAL'
new=api._replay_advances(json.loads(v) for v in after.splitlines())
assert {k:v for k,v in states.items() if k!=A}=={k:v for k,v in new.items() if k!=A}
assert (r/'runs/substantive_discoveries.jsonl').read_bytes()==dbefore
assert git('rev-parse','HEAD').decode().strip()==carrier and sha(indexpath.read_bytes())==indexbefore
assert git('diff','--name-only',carrier).decode().splitlines()==['runs/substantive_advances.jsonl']
for p,h in baseline['all_existing_frontier_sha256'].items():assert sha((r/p).read_bytes())==h,p
(e/'actual-PROVED_LOCAL-append.exact.jsonl').write_bytes(after[len(before):])
cell['status']='proved_locally';cell['evidence']['normal_PROVED_LOCAL']={'full_evidence':ident(e/'PROVED_LOCAL-evidence.full.json'),
 'actual_append':ident(e/'actual-PROVED_LOCAL-append.exact.jsonl'),'normal_calls':1,'checked_metadata_commit':carrier}
cell['phase_snapshot']='One actual normal PROVED_LOCAL; immutable mathematics/native and current source acceptance complete. Current-v3 browser/independent visual and proof VERIFIED still pending; no production/main/global integration/purification/full-paper claim.'
dump(cellpath,cell)
mem=read(e/'local-cycle-memory.json');mem['normal_state']='PROVED_LOCAL';mem['normal_PL_calls']=1;mem['ROOT_V_calls']=0;dump(e/'local-cycle-memory.json',mem)
print(json.dumps({'actual_state':new[A]['state'],'normal_PL_calls':1,'ROOT_V_calls':0,'original_PL_fields':len(payload),
 'all_foreign_states_and_old_frontiers_preserved':True,'actual_reader_acceptance':'pending'}))
