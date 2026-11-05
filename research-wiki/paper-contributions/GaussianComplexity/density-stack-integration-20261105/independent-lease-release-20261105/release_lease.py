"""Release one owned Gaussian integration lease through the normal independent API."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,traceback
R=Path.cwd();sys.path.insert(0,str(R))
from tools import astis_advance as a
E=Path(__file__).resolve().parent;D=E.parent
candidate='3cb317e9fcec0cce55f5e42bbf63844dfd59730c'
source_commit='399983c34739fa1930dea35254597547cfe17ad1'
actor='/root/density_fresh_source_module_review'
ident='ASTIS-SA-20261105-GaussianComplexityMixtureDensities'
declarations=['AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities.actual_mixture_densities']
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(*args):return subprocess.check_output(['git',*args])
def blob(c,p):return git('show',f'{c}:{p}')
def info(p):return {'path':str(p.relative_to(R)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def write(name,data):
 p=E/name;p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return info(p)
def paired(label):
 p=next((D/'actual-checks').glob('*'+label+'*.receipt.json'));r=json.loads(p.read_bytes());l=p.with_suffix('').with_suffix('.log')
 assert r['exit_code']==0 and r['head_before']==r['head_after']==source_commit and sha(l.read_bytes())==r['log_sha256']
 assert l.read_bytes()==Path(r['log']).read_bytes() and p.read_bytes()==Path(r['log']).with_suffix('.receipt.json').read_bytes()
 return {'receipt':info(p),'log':info(l),'command':r['command'],'HEAD_before':r['head_before'],'HEAD_after':r['head_after'],'exit_code':r['exit_code']}
phase='preflight'
try:
 assert git('rev-parse','HEAD').decode().strip()==candidate
 manifest_path=D/'final-local-acceptance-manifest.json';manifest=json.loads(manifest_path.read_bytes());assert len(manifest['files'])==142 and sha(manifest_path.read_bytes())=='622708e124f3975845bbc5851798dd3612b037abf289103948fb3ef4174b823b'
 for x in manifest['files']:
  p=D/x['path'];assert sha(p.read_bytes())==x['sha256'] and len(p.read_bytes())==x['bytes'] and p.read_bytes()==blob(candidate,str(p.relative_to(R))),x['path']
 metadata=json.loads((D/'local-reader-frontier-metadata-delta.json').read_bytes());frontier_set={x['path'] for x in metadata['changes']}
 diffs=[x.split('\t',1) for x in git('diff','--name-status',source_commit,candidate).decode().splitlines()]
 assert {p for s,p in diffs if s=='M'}==frontier_set|{'.gitattributes'}
 assert all(s=='M' or (s=='A' and p.startswith(str(D.relative_to(R))+'/')) for s,p in diffs)
 for x in metadata['changes']:
  p=x['path'];b=json.loads(blob(source_commit,p));n=json.loads(blob(candidate,p));assert sha(blob(source_commit,p))==x['before_sha256'] and sha(blob(candidate,p))==x['after_sha256']
  assert b['status']==n['status']=='independently_verified';del n['evidence']['serialized_integration_20261105'];n['graph_contribution']['visual_review']=b['graph_contribution']['visual_review'];assert n==b
 review_path=D/'independent-integration-reader-review.json';assert sha(review_path.read_bytes())=='7f2c053d3997bd46c303c7999e533200843593229bf37e9720f8d77a4a8afca7'
 protected=json.loads((D/'shared-integration-delta.json').read_bytes())['protected_Gaussian_source_prose_and_audit_files'];assert len(protected)==39
 for x in protected:
  p=x['path'];assert sha((R/p).read_bytes())==x['sha256'] and (R/p).read_bytes()==blob(source_commit,p)==blob(candidate,p)
 dig=hashlib.sha256();paths=[R/'AutoSamplingTheory.lean',*sorted((R/'AutoSamplingTheory').rglob('*.lean')),R/'Tests.lean',*sorted((R/'Tests').rglob('*.lean')),R/'lakefile.lean',R/'lean-toolchain',R/'lake-manifest.json']
 for p in paths:
  if p.exists():dig.update(p.relative_to(R).as_posix().encode());dig.update(b'\0');dig.update(p.read_bytes());dig.update(b'\0')
 assert dig.hexdigest()=='c10081f873bcbff1ea4e4a282e8ad13626cddc7150571349679c4720132ed56d'
 gates={name:paired(label) for name,label in [('full_Lean','095725215617Z'),('final_publication','123447167181Z'),('final_contributor','123447167189Z'),('final_frontier','123447167178Z'),('harness','123324337389Z'),('current_browser','102150669593Z'),('source_index_clicks','102733799006Z')]}
 assert gates['harness']['log']['sha256']=='605ccd1db934aa6d696e0cb449dc1259dc812e73d4d48e0647388704dc8ada9b'
 harness=(R/gates['harness']['log']['path']).read_text();assert 'Ran 487 tests' in harness and 'OK (skipped=6)' in harness
 ledger=R/'runs/substantive_advances.jsonl';before=ledger.read_bytes();assert before==blob(candidate,'runs/substantive_advances.jsonl') and before.endswith(b'\n')
 discovery=R/'runs/substantive_discoveries.jsonl';discovery_before=discovery.read_bytes();assert discovery_before==blob(candidate,'runs/substantive_discoveries.jsonl')
 parse=lambda data:[json.loads(x) for x in data.splitlines() if x.strip()]
 states=a._replay_advances(parse(before));assert len(states)==271 and states[ident]['state']=='STABILIZING' and states[ident]['publication_declarations']==declarations
 assert [k for k,v in states.items() if v['state']=='STABILIZING']==[ident]
 others={k:v for k,v in states.items() if k!=ident};assert len(others)==270
 frontier_paths=git('ls-tree','-r','--name-only',candidate,'research-wiki/frontier-cells').decode().splitlines()
 frontiers={p:sha((R/p).read_bytes()) for p in frontier_paths}
 for p,h in frontiers.items():assert (R/p).read_bytes()==blob(candidate,p)
 # Complete original ledger and discovery bytes are retained before any API mutation.
 before_path=E/'before-substantive_advances.exactraw.jsonl';before_path.write_bytes(before)
 discovery_path=E/'before-substantive_discoveries.exactraw.jsonl';discovery_path.write_bytes(discovery_before)
 assert before_path.read_bytes()==before and discovery_path.read_bytes()==discovery_before
 source_dir=R/'research-wiki/paper-contributions/GaussianComplexity/mixture-densities-semantic-evidence/independent-source-module-reader-review-20261105'
 source_audit=R/'research-wiki/semantic-roundtrip/audits/huanjian-mixture-densities.json'
 before_check={'schema_version':1,'status':'pass','candidate_commit':candidate,'checked_source_commit':source_commit,'verifier_id':actor,'source_digest':dig.hexdigest(),'manifest':info(manifest_path),'all142_manifest_files_equal_candidate_Git_blobs':True,'closed_diff_is_three_owned_frontier_evidence_visual_fields_log_attribute_and_evidence_only':True,'protected39_code_prose_audit_files_unchanged':True,'original_review':info(review_path),'actual_gates':gates,'ledger_snapshot':info(before_path),'discovery_snapshot':info(discovery_path),'advance_count':len(states),'all_other270_states_canonical_sha256':sha(canon(others)),'frontier_file_digests':frontiers,'all_frontiers_canonical_sha256':sha(canon(frontiers)),'target_before':states[ident],'STABILIZING_before':[ident],'preexisting_process_notes':{'tracked_diff_paths':git('diff','--name-only').decode().splitlines(),'meaning':'Coordinator README/checkpoint process notes are outside the immutable candidate proof/reader review and remain untouched by this script.'}}
 before_info=write('before-checklist.json',before_check)
 print(json.dumps({'phase':'before-snapshot-saved','before_checklist':before_info,'complete_original_ledger':info(before_path),'complete_original_discovery':info(discovery_path),'candidate_commit':candidate}),flush=True)
 reason='Release only this local integration lease because remote GitHub authentication is unavailable. Local mathematics/source/reader acceptance remains valid. Return STABILIZING to VERIFIED, never MERGED or BLOCKED; remote PR/CI/deploy, postmerge purification/Exposition Seal and the overall Goal remain incomplete.'
 evidence={
  'verifier_id':actor,'verified_commit':candidate,'publication_declarations':declarations,
  'gate':{'candidate_preflight':before_info,'current_source_digest':dig.hexdigest(),'source_bound_actual_checks':gates,'reuse_rationale':'Immutable candidate changes only evidence attributes, owned frontier evidence/visual notes and saved evidence relative to the actually checked399 source. All Lean/test/toolchain/manifest bytes are unchanged. Normal transition API additionally runs its reviewed publication/round-trip gate at the actual candidate.'},
  'source_audit':{'canonical_fragment':info(source_audit),'result':info(source_dir/'source-review-result.json'),'run':info(source_dir/'source-review-run.json'),'verdict':'equivalent-after-elaboration','local_integration_reader_review':info(review_path),'no_mathematical_or_source_reissue':True},
  'fake_closure_scan':info(source_dir/'fake-closure-scan.json'),
  'whole_module_review':info(source_dir/'whole-module-review.json'),
  'failure_class':'ENV_BLOCKED','failure_subtype':'GITHUB_AUTHENTICATION','historical_auth_evidence':info(D/'publication-auth-blocker.json'),
  'release_reason':reason,'mathematical_failure':False,'local_reader_accepted':True,
  'released_integration_owner':states[ident]['latest_evidence'].get('integration_owner'),
  'verified_source_owner_preserved':states[ident]['owner_id'],
  'release_scope':'This SAU only; original prefix/all other270 states/discoveries/all frontiers preserved. No publication on behalf of coordinator, no foreign-owner action.',
  'truth_boundary':reason+' Actual TV-affinity upper bound/Eq25, products/amplification, both main bounds and oracle/precision/query/cost/hidden-basis adapters remain outside.',
  'release_evidence_directory':str(E.relative_to(R))}
 phase='normal_API'
 a.transition_advance(ident,'VERIFIED',worker_id=actor,modes=['independent-immutable-candidate-check','normal-api-local-lease-release','remote-auth-environment-boundary'],evidence=evidence)
 phase='postcheck'
 after=ledger.read_bytes();assert after.startswith(before);append=after[len(before):];assert append.endswith(b'\n') and len(append.splitlines())==1
 append_path=E/'release-transition.append-event.jsonl';append_path.write_bytes(append)
 after_path=E/'after-substantive_advances.exactraw.jsonl';after_path.write_bytes(after)
 event=json.loads(append);assert event['advance_id']==ident and event['from_state']=='STABILIZING' and event['to_state']=='VERIFIED' and event['worker_id']==actor and event['evidence']['verified_commit']==candidate
 post=a._replay_advances(parse(after));assert len(post)==271 and post[ident]['state']=='VERIFIED'
 other_after={k:v for k,v in post.items() if k!=ident};assert other_after==others
 assert post[ident]['owner_id']==states[ident]['owner_id']
 stabilizing=[k for k,v in post.items() if v['state']=='STABILIZING'];assert stabilizing==[]
 assert discovery.read_bytes()==discovery_before
 for p,h in frontiers.items():assert sha((R/p).read_bytes())==h
 for x in manifest['files']:assert sha((D/x['path']).read_bytes())==x['sha256']
 assert sha(review_path.read_bytes())=='7f2c053d3997bd46c303c7999e533200843593229bf37e9720f8d77a4a8afca7'
 assert git('rev-parse','HEAD').decode().strip()==candidate
 result={'schema_version':1,'status':'released-to-VERIFIED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verifier_id':actor,'worker_id':actor,'candidate_commit':candidate,'source_digest':dig.hexdigest(),'advance_id':ident,'state_before':'STABILIZING','state_after':'VERIFIED','failure_class':'ENV_BLOCKED','failure_subtype':'GITHUB_AUTHENTICATION','reason':reason,'before_checklist':before_info,'raw_before_ledger':info(before_path),'raw_after_ledger':info(after_path),'exact_single_append_event':info(append_path),'original_raw_prefix_fully_preserved':True,'only_target_advance_changed':True,'all_other270_states_canonical_sha256':sha(canon(other_after)),'all_other270_states_unchanged':True,'discovery_snapshot':info(discovery_path),'all_discovery_raw_bytes_unchanged':True,'all_frontier_files_unchanged':True,'frontier_file_count':len(frontiers),'all_frontiers_canonical_sha256':sha(canon(frontiers)),'STABILIZING_after':stabilizing,'source_owner_preserved':post[ident]['owner_id'],'original_review_unchanged':True,'all142_candidate_manifest_inputs_unchanged_after_release':True,'no_commit_branch_merge_remote_publication_source_or_foreign_mutation':True,'remote_and_purification_Goal_boundaries_preserved':True}
 post_info=write('after-checklist.json',result)
 print(json.dumps({'status':result['status'],'advance_id':ident,'verified_commit':candidate,'actor':actor,'raw_append':info(append_path),'old_prefix_preserved':True,'other270_states_and_discoveries_and_all_frontiers_unchanged':True,'STABILIZING_after':stabilizing,'after_checklist':post_info},ensure_ascii=False,indent=2),flush=True)
except Exception as e:
 error={'status':'error-no-manual-ledger-edit','phase':phase,'candidate_commit':candidate,'actor':actor,'exception_type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'normal_API_refusal_or_check_failure_retained':True}
 write('release-error.json',error)
 print(json.dumps(error,ensure_ascii=False,indent=2),flush=True)
 raise
