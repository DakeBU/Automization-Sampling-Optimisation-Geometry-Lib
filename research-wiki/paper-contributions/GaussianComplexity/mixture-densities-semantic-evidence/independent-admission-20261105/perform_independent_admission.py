"""One real independent VERIFIED transition, with raw append and preservation checks."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys
R=Path.cwd()
sys.path.insert(0,str(R))
from tools import astis_advance as a
E=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(*args): return subprocess.check_output(['git',*args])
def blob(commit,path): return git('show',f'{commit}:{path}')
def info(path):
    p=R/path
    return {'path':str(p.relative_to(R)),'sha256':sha(p.read_bytes())}
pre_path=E/'admission-preflight.json'
pre=json.loads(pre_path.read_bytes())
verified=pre['verified_commit']
assert pre['status']=='pass' and verified=='8001430a5ce67810c37e35886d1771bf73cd4e20'
assert git('rev-parse','HEAD').decode().strip()==verified
for p,h in pre['protected_input_digests'].items(): assert sha((R/p).read_bytes())==h['sha256'],p
assert sha((R/pre['canonical_audit_fragment']['path']).read_bytes())==pre['canonical_audit_fragment']['sha256']
review_dir=R/'research-wiki/paper-contributions/GaussianComplexity/mixture-densities-semantic-evidence/independent-source-module-reader-review-20261105'
rm=json.loads((review_dir/'review-manifest.json').read_bytes())
assert sha((review_dir/'review-manifest.json').read_bytes())==pre['review_manifest_sha256']
for p,h in rm['artifacts'].items(): assert sha((R/p).read_bytes())==h['sha256'],p
for x in pre['gate_results']:
    for key in ['receipt','log']:
        p=R/x[key]['path']; assert sha(p.read_bytes())==x[key]['sha256'] and p.read_bytes()==blob(verified,x[key]['path'])
ledger_path=R/pre['old_advance_ledger']['path']; before=ledger_path.read_bytes()
discovery_path=R/pre['old_discovery_ledger']['path']; discovery_before=discovery_path.read_bytes()
assert len(before)==pre['old_advance_ledger']['bytes'] and sha(before)==pre['old_advance_ledger']['sha256'] and before==blob(verified,str(ledger_path.relative_to(R)))
assert sha(discovery_before)==pre['old_discovery_ledger']['sha256']
state_before=a._replay_advances([json.loads(x) for x in before.splitlines() if x.strip()])
ident='ASTIS-SA-20261105-GaussianComplexityMixtureDensities'
actor='/root/density_fresh_source_module_review'
others_before={k:v for k,v in state_before.items() if k!=ident}
assert len(others_before)==266 and sha(canon(others_before))==pre['old_advance_ledger']['all266_other_advance_states_canonical_sha256']
assert state_before[ident]==pre['target_advance_before'] and state_before[ident]['state']=='PROVED_LOCAL'
frontier_path=R/pre['frontier_baseline']['target_path']; frontier_before=frontier_path.read_bytes(); frontier=json.loads(frontier_before)
assert frontier['status']=='proved_locally'
for p,h in pre['frontier_baseline']['all_tracked_frontier_file_digests'].items(): assert sha((R/p).read_bytes())==h,p
source_result=json.loads((review_dir/'source-review-result.json').read_bytes())
assert source_result['reviewer']==pre['source_review_label_verbatim']
declarations=['AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities.actual_mixture_densities']
evidence={
    'verifier_id':actor,'verified_commit':verified,
    'source_review_label_verbatim':source_result['reviewer'],
    'publication_declarations':declarations,
    'gate':{
        'scope':'Immutable-descendant independent local SAU admission only; no root/site/UI acceptance.',
        'focused_Lean_build_reused':pre['focused_build_reuse'],
        'postreview_checks':pre['gate_results'],
        'normal_transition_publication_gate':'tools.astis_advance.transition_advance invokes check_advance(reviewed=True) before appending this VERIFIED event.',
        'immutable_descendant_preflight':info(str(pre_path.relative_to(R)))},
    'source_audit':{
        'verdict':'equivalent-after-elaboration','deltas':[],'repairs':[],'blockers':[],
        'canonical_audit_fragment':pre['canonical_audit_fragment'],
        'source_review_result':info(str((review_dir/'source-review-result.json').relative_to(R))),
        'source_review_run':info(str((review_dir/'source-review-run.json').relative_to(R))),
        'reviewer_packet_sha256':source_result['reviewer_packet_sha256'],
        'publication_binding_sha256':source_result['publication_binding_sha256'],
        'independent_actor':actor,'formalizer':pre['target_advance_before']['owner_id'],
        'decoder':'/root/decode_507824'},
    'fake_closure_scan':info(str((review_dir/'fake-closure-scan.json').relative_to(R))),
    'whole_module_review':info(str((review_dir/'whole-module-review.json').relative_to(R))),
    'authored_reader_content_review':info(str((review_dir/'authored-reader-review.json').relative_to(R))),
    'reader_acceptance_scope':'accepted-content-only; rendered/UI/interaction/navigation/Exposition Seal remain pending.',
    'truth_boundary':pre['truth_boundary'],
    'result_kind':'integration-node',
    'preserved_baselines':{
        'advance_ledger':pre['old_advance_ledger'],
        'discovery_ledger':pre['old_discovery_ledger'],
        'other_frontier_files_canonical_sha256':pre['frontier_baseline']['all_other_frontier_files_canonical_sha256']},
    'foreign_state_preservation':pre['foreign_state'],
    'admission_artifact':'research-wiki/paper-contributions/GaussianComplexity/mixture-densities-semantic-evidence/independent-verified-admission.json'}
print(json.dumps({'action':'calling normal transition_advance','advance_id':ident,'from_state':'PROVED_LOCAL','to_state':'VERIFIED','worker_id':actor,'verifier_id':actor,'verified_commit':verified,'publication_declarations':declarations},ensure_ascii=False),flush=True)
a.transition_advance(ident,'VERIFIED',worker_id=actor,modes=['independent-source-review','whole-module-review','authored-reader-content-only','immutable-descendant-admission'],evidence=evidence)
after=ledger_path.read_bytes()
assert after.startswith(before), 'Old raw ledger prefix changed'
append=after[len(before):]
assert append.endswith(b'\n') and len(append.splitlines())==1
append_path=E/'verified-transition.append-event.jsonl'; append_path.write_bytes(append)
event=json.loads(append)
assert event['event']=='transition' and event['advance_id']==ident and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
assert event['worker_id']==actor and event['evidence']['verifier_id']==actor and event['evidence']['verified_commit']==verified
assert event['evidence']['publication_declarations']==declarations
state_after=a._replay_advances([json.loads(x) for x in after.splitlines() if x.strip()])
others_after={k:v for k,v in state_after.items() if k!=ident}
assert others_after==others_before and len(others_after)==266
assert discovery_path.read_bytes()==discovery_before
assert state_after[ident]['state']=='VERIFIED' and state_after[ident]['owner_id']==state_before[ident]['owner_id']
frontier['status']='independently_verified'
frontier['evidence']['independent_verification']={
    'verifier_id':actor,'verified_commit':verified,'source_review_label_verbatim':source_result['reviewer'],
    'advance_id':ident,'transition_event':info(str(append_path.relative_to(R))),
    'admission_artifact':evidence['admission_artifact'],
    'focused_Lean_build_reused':pre['focused_build_reuse'],
    'gate_manifest':pre['gate_manifest'],
    'source_audit':evidence['source_audit'],
    'whole_module_review':evidence['whole_module_review'],
    'fake_closure_scan':evidence['fake_closure_scan'],
    'authored_reader_content_review':evidence['authored_reader_content_review'],
    'truth_boundary':pre['truth_boundary'],
    'reader_acceptance_scope':evidence['reader_acceptance_scope']}
frontier_path.write_text(json.dumps(frontier,ensure_ascii=False,indent=2)+'\n')
new_frontier=json.loads(frontier_path.read_bytes());old_frontier=json.loads(frontier_before)
assert set(k for k in new_frontier if new_frontier[k]!=old_frontier[k])=={'status','evidence'}
assert set(k for k in new_frontier['evidence'] if new_frontier['evidence'][k]!=old_frontier['evidence'][k])=={'independent_verification'}
assert new_frontier['learning_contract']==old_frontier['learning_contract']
other_frontiers_after={}
for p,h in pre['frontier_baseline']['all_tracked_frontier_file_digests'].items():
    if p==str(frontier_path.relative_to(R)): continue
    assert sha((R/p).read_bytes())==h,p
    other_frontiers_after[p]=h
assert sha(canon(other_frontiers_after))==pre['frontier_baseline']['all_other_frontier_files_canonical_sha256']
for p,h in pre['protected_input_digests'].items(): assert sha((R/p).read_bytes())==h['sha256'],p
assert sha((R/pre['canonical_audit_fragment']['path']).read_bytes())==pre['canonical_audit_fragment']['sha256']
assert git('rev-parse','HEAD').decode().strip()==verified
post={
    'schema_version':1,'status':'verified-admission-completed','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'advance_id':ident,'verifier_id':actor,'verified_commit':verified,
    'source_review_label_verbatim':source_result['reviewer'],
    'normal_API_called':'tools.astis_advance.transition_advance',
    'publication_declarations':declarations,
    'advance_state_before':'PROVED_LOCAL','advance_state_after':state_after[ident]['state'],
    'owner_id_preserved':state_after[ident]['owner_id'],
    'raw_append_event':info(str(append_path.relative_to(R))),
    'raw_ledger':{'path':str(ledger_path.relative_to(R)),'old_bytes':len(before),'old_sha256':sha(before),'new_bytes':len(after),'new_sha256':sha(after),'append_bytes':len(append),'append_sha256':sha(append),'old_exact_raw_prefix_unchanged':True,'exactly_one_event_appended':True},
    'all266_other_advances':{'count':len(others_after),'before_after_equal':True,'canonical_sha256':sha(canon(others_after))},
    'discoveries':{'path':str(discovery_path.relative_to(R)),'before_after_raw_bytes_equal':True,'sha256':sha(discovery_before)},
    'other_frontier_files':{'count':len(other_frontiers_after),'all_before_after_raw_digests_equal':True,'canonical_sha256':sha(canon(other_frontiers_after))},
    'own_frontier':{'path':str(frontier_path.relative_to(R)),'before_sha256':sha(frontier_before),'after_sha256':sha(frontier_path.read_bytes()),'status_before':'proved_locally','status_after':'independently_verified','only_changed_paths':['status','evidence.independent_verification'],'all_other_fields_and_reader_pending_seals_preserved':True},
    'all_protected_candidate_inputs_rechecked_unchanged':True,
    'truth_boundary':pre['truth_boundary'],'foreign_state':pre['foreign_state'],
    'no_STABILIZING_merge_commit_branch_or_foreign_mutation':True}
p=E/'admission-postcheck.json';p.write_text(json.dumps(post,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':post['status'],'advance_id':ident,'state':state_after[ident]['state'],'verifier_id':actor,'verified_commit':verified,'raw_append_event':post['raw_append_event'],'old_exact_raw_ledger_prefix_unchanged':True,'all266_other_advance_states_unchanged':True,'all_discovery_bytes_unchanged':True,'all_other_frontier_files_unchanged':True,'own_frontier':post['own_frontier'],'postcheck':info(str(p.relative_to(R)))},ensure_ascii=False,indent=2),flush=True)
