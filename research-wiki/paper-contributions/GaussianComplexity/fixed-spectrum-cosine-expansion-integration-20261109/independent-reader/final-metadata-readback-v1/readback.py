import ast, copy, datetime, gzip, hashlib, json, subprocess, tarfile
from pathlib import Path
ROOT=Path.cwd()
P=Path('.astis/huanjian-gc-fixed-spectrum-cosine-expansion-integration-20261109')
O=P/'independent-reader/final-metadata-readback-v1'
B=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-expansion-integration-20261109')
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-expansion-semantic-evidence')
S=Path('.astis/semantic-neutral-20261109/src_cosine_5d8c2a')
R=S/'normal-release-runtime/release-preflight-bound-v2-01'
CP=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-expansion.json')
RM=Path('research-wiki/paper-contributions/GaussianComplexity/README.md')
LP=Path('runs/substantive_advances.jsonl')
CORE='7ad39273de26a0ed0315db46be231b5585e26409'
CAND='37645c774481c4cad19fc29bcaa76799da64db7d'
CARRIER='8af00592e92ea43bff573fb407aeed013415748c'
AID='ASTIS-SA-20261109-GaussianComplexityFixedSpectrumCosineExpansion'
OWNER='huanjian_gc_20261109_fixed_spectrum_cosine_expansion'
VERIFIER='/root/cosine_fresh_source_5d8c2a'
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda j:(json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
inputs={}
def read(p):
 p=Path(p); b=p.read_bytes();inputs[str(p)]={'sha256':sha(b),'bytes':len(b)};return b
def js(p):return json.loads(read(p))
def git(*args):return subprocess.check_output(['git',*args])
def blob(p):return git('show',CORE+':'+str(p))
def put(name,j):(O/name).write_bytes(enc(j))
assert git('rev-parse','HEAD').decode().strip()==CORE
changed=git('diff','--name-only',CORE).decode().splitlines()
assert set(changed)=={str(CP),str(RM),str(LP)},changed
before_raw=gzip.decompress(read(B/'final-metadata-before/frontier.raw.json.gz'))
before_readme=gzip.decompress(read(B/'final-metadata-before/README.raw.md.gz'))
assert before_raw==blob(CP) and before_readme==blob(RM)
assert sha(before_raw)=='76d456791e12fb52c17243fd5b4046642a57e93037867316a566912d73919640'
a_raw=read(CP); b=json.loads(before_raw);a=json.loads(a_raw)
assert sha(a_raw)=='2e6471ac0645a36bcc3b3f5cf406e177243f5dfb3e66c70d0b6e4957902b5b46'
def differences(x,y,p=''):
 if type(x)!=type(y):return [p]
 if isinstance(x,dict):
  return [q for k in sorted(x.keys()|y.keys()) for q in ([p+'/'+k] if k not in x or k not in y else differences(x[k],y[k],p+'/'+k))]
 return [] if x==y else [p]
paths=differences(b,a)
expected=sorted(['/evidence/execution_boundary','/evidence/graph_regeneration','/evidence/local_integration_acceptance','/evidence/root_build','/graph_contribution/visual_review','/source_detail_audit/fidelity_boundary','/source_detail_audit/gap','/statement_seal/status','/status'])
assert paths==expected,paths
restored=copy.deepcopy(a);edits=[]
for p in paths:
 ks=p.split('/')[1:];x=b;y=a;z=restored
 for k in ks[:-1]:x=x[k];y=y[k];z=z[k]
 k=ks[-1]
 if k not in x:
  assert p=='/evidence/local_integration_acceptance' and isinstance(y[k],dict)
  del z[k];edits.append({'path':p,'before_absent':True,'after':y[k]})
 else:
  assert isinstance(x[k],str) and isinstance(y[k],str)
  z[k]=x[k];edits.append({'path':p,'before':x[k],'after':y[k]})
assert enc(restored)==before_raw
assert a['owner_id']==b['owner_id']==OWNER
assert a['status']=='stabilized'
assert a['evidence']['source_phase_history']==b['evidence']['source_phase_history']
assert a['evidence']['canonical_integration']==b['evidence']['canonical_integration']
assert a['evidence']['independent_verification']==b['evidence']['independent_verification']
assert a['statement_seal']['status']=='EXACT_SEALED_C7_SOURCE_AND_LOCAL_INTEGRATION_ACCEPTED_REMOTE_PURIFICATION_PENDING'
readme=read(RM);assert readme.endswith(before_readme)
prefix=readme[:-len(before_readme)];assert CORE.encode() in prefix and b'37645' in prefix
checkpoint=js(B/'resume-checkpoint.json')
assert checkpoint['accepted_immutable_core']==CORE and checkpoint['checked_source_candidate']==CAND
assert checkpoint['normal_state_after_actual_release']=='VERIFIED'
assert checkpoint['fresh_build_at_metadata_successor'] is False and checkpoint['whole_Goal_complete'] is False
assert checkpoint['remote_and_postmerge_purification']=='pending'
oldv_raw=read(E/'actual-source-V/actual-append-observed.exact.jsonl');oldv=json.loads(oldv_raw)
assert sha(oldv_raw)=='09633595f7b49375b1ac22ea17661a439f3125ba0ca2811c3751bace07046ef8'
append=read(R/'actual-release-append.exact.jsonl');event=json.loads(append)
assert sha(append)=='8a1a05a7950dd536d97a9771ac04916a64716199c9141772af1f2545fa51a96e'
assert len(append.splitlines())==1
assert (event['advance_id'],event['event'],event['from_state'],event['to_state'],event['worker_id'])==(AID,'transition','STABILIZING','VERIFIED',VERIFIER)
assert len(oldv['evidence'])==13
assert {k:v for k,v in event['evidence'].items() if k!='post_integration'}==oldv['evidence']
assert set(event['evidence'])==set(oldv['evidence'])|{'post_integration'}
assert sha(enc(oldv['evidence']))=='0b630ef183c2c0af9840d658926272bc8333ada78dbea9abb3ab8eef3b3ca808'
assert event['evidence']==js(R/'actual-call-evidence.json')
post=event['evidence']['post_integration']
assert post['integration_core']==CORE and post['source_checked_commit_preserved']==CAND
assert post['source_V_first_carrying_commit']==CARRIER
for k in ['actual_core_checks','actual_same_core_browser48','independent_all48_pixel_review','independent_local_acceptance','park_eligibility']:
 ref=post[k];p=ref.get('path',ref.get('manifest'));assert sha(read(p))==ref['sha256']
release=js(R/'actual-release-receipt.json');observation=js(R/'API-observation.json');inv=js(R/'execution-invocation.json')
assert release['normal_API_calls']==1 and release['source_verifier']==VERIFIER
assert release['source_checked_commit']==CAND and release['integration_core']==CORE
assert release['actual_append_sha256']==sha(append)
assert inv['actual_exit_code']==0 and inv['no_retry'] is True
assert observation['API_call_attempts']==1 and observation['API_exception'] is None
assert observation['old_prefix_preserved'] is True
assert read(LP)==blob(LP)+append
assert read(R/'before-ledger.exact.jsonl')==blob(LP)
assert read(R/'after-observed-ledger.exact.jsonl')==read(LP)
assert sha(read(LP))=='14cc6872a000c5a2714f36908c963280056081fd02971c433f6229a472f50f16'
for n in ['actual-call-evidence.json','API-observation.json','actual-release-append.exact.jsonl','actual-release-receipt.json','preflight-receipt.json']:
 assert read(B/'actual-existing-V-release'/n)==read(R/n)
archive=B/'actual-existing-V-release/release-preparations-and-actual-runtime.lossless.tar.gz';read(archive)
tar_files=[]
with tarfile.open(archive) as t:
 for m in t.getmembers():
  if not m.isfile():continue
  parts=Path(m.name).parts;first=parts[0]
  roots={'actual-runtime':R,'normal-release-preparation':S/'normal-release-preparation','normal-release-preparation-bound-v2':S/'normal-release-preparation-bound-v2'}
  original=roots[first].joinpath(*parts[1:]) if first in roots else P/m.name
  raw=t.extractfile(m).read();assert raw==read(original),m.name
  tar_files.append({'member':m.name,'original':str(original),'sha256':sha(raw),'bytes':len(raw)})
bs=js(R/'before-snapshot.json');as_=js(R/'after-snapshot.json')
assert bs['foreign_states']==as_['foreign_states'] and len(bs['foreign_states'])==286
assert bs['frontier']==as_['frontier'] and len(bs['frontier'])==446
frontiers={str(p):sha(p.read_bytes()) for p in Path('research-wiki/frontier-cells').glob('*.json')}
assert set(frontiers)==set(bs['frontier'])
foreign={p:h for p,h in bs['frontier'].items() if p!=str(CP)}
assert len(foreign)==445 and all(frontiers[p]==h for p,h in foreign.items())
for p,h in bs['protected_models_and_discovery'].items():assert sha(read(p))==h and read(p)==blob(p)
AP=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-cosine-expansion.json')
assert sha(read(AP))==bs['audit_sha256']==as_['audit_sha256']=='0b8b3e19cece6446f117d682b5826dbac274f14a4e8bbd3be316a41cbc3ddb67'
assert read(AP)==blob(AP)
# Extract only the pure replay function and its literal threshold; no API/module import.
src=read(Path('tools/astis_advance.py')).decode();tree=ast.parse(src)
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_replay_advances')
threshold=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NO_PROGRESS_FREEZE_AT' for t in n.targets))
ns={'NO_PROGRESS_FREEZE_AT':threshold};exec(compile('from __future__ import annotations\n'+ast.get_source_segment(src,fn),'<extracted-pure-replay>','exec'),ns)
records=lambda raw:[json.loads(l) for l in raw.splitlines() if l.strip()]
pre=ns['_replay_advances'](records(blob(LP)));current=ns['_replay_advances'](records(read(LP)))
assert pre==bs['all_states'] and current==as_['all_states']
assert {k:v for k,v in current.items() if k!=AID}==bs['foreign_states']
assert pre[AID]['state']=='STABILIZING' and current[AID]['state']=='VERIFIED'
assert pre[AID]['owner_id']==current[AID]['owner_id']==OWNER
assert current[AID]['last_actor']==VERIFIER and not [k for k,v in current.items() if v['state']=='STABILIZING']
prior=P/'independent-reader/actual-shared-application-readback-v1'
application=js(prior/'actual-application-readback-review.json')
pins=js(prior/'actual-stage-A-and-eight-payload-readback.json')['source_Test_lesson_pub_seal_A1_and_core_protocol_pins_unchanged']
for p,h in application['shared_after_hashes'].items():assert sha(read(p))==h and read(p)==blob(p)
sourcefiles={p:sha(read(p)) for p in pins}
for p in pins:assert read(p)==blob(p)
# Already reviewed pixel/local records are checked by exact byte reference, not re-reviewed.
reference_paths=['original48-independent-review-v1/actual48-original-pixel-review.json','original48-independent-review-v1/original48-per-image-findings.json','local-acceptance-and-eligibility-v1/local-integration-acceptance-v1.json','local-acceptance-and-eligibility-v1/existing-V-normalpark-eligibility-v1.json']
for p in reference_paths:assert read(P/'independent-reader'/p)==read(B/'independent-reader'/p)
assert read(P/'root-original8-spot-review-v5.json')==read(B/'actual-browser-v5/root-original8-spot-review-v5.json')
assert sha(read(P/'root-original8-spot-review-v5.json'))=='d9d30f670578c1172985fa6b00b069155737a197f067dc3558c4a1ac42e896d9'
receipts=[]
L=Path('.astis/huanjian-resume-20261103')
receipt_paths=sorted(L.glob('20261109T125258*cosine-expansion-final*receipt.json'))+[L/'20261109T125217481286Z-cosine-expansion-final-local-metadata.receipt.json']
assert len(receipt_paths)==5
for p in receipt_paths:
 r=js(p);assert r['exit_code']==0 and r['head_before']==r['head_after']==CORE
 assert sha(read(r['log']))==r['log_sha256'];receipts.append({'path':str(p),'sha256':sha(read(p)),'exit_code':0,'head_before':CORE,'head_after':CORE,'log_sha256':r['log_sha256']})
summary=json.loads(read(L/'20261109T125217481286Z-cosine-expansion-final-local-metadata.log'))
assert summary['own_frontier_before_sha256']==sha(before_raw) and summary['own_frontier_after_sha256']==sha(a_raw)
assert summary['normal_API_calls_in_this_script']==0 and summary['foreign_raw_frontiers_preserved']==445
assert summary['selected_core']==CORE and summary['actual_release_append_sha256']==sha(append)
assert not summary['new_source_verdict_fresh_build_or_remote_acceptance']
read(P/'finalize_local_metadata.py')
put('exact-own-cell-projection.json',{'before_sha256':sha(before_raw),'after_sha256':sha(a_raw),'changed_json_paths':paths,'scalar_replacements':8,'new_evidence_objects':1,'edits':edits,'inverse_restores_exact_before_raw_bytes':True,'preserved_other_fields_and_historical_evidence':True})
put('actual-runtime-public-copy-readback.json',{'public_direct_copies':5,'all_equal_private_original_bytes':True,'archive_file_count':len(tar_files),'archive_files_all_equal_actual_originals':True,'members':tar_files})
report={'reviewer':'/root/geometry_integration_reader','verdict':'ACCEPT_EXACT_C7_FINAL_METADATA_READBACK','review_kind':'Bounded independent mechanical readback only','actual_observed_HEAD':CORE,'source_checked_candidate':CAND,'source_V_first_carrying_commit':CARRIER,'accepted_immutable_integration_core':CORE,'future_metadata_commit':None,'current_tracked_changes':changed,'original_source_V_append_sha256':sha(oldv_raw),'actual_existing_V_release_append_sha256':sha(append),'actual_existing_V_release_receipt_sha256':sha(read(R/'actual-release-receipt.json')),'actual_release_normal_API_calls':1,'original_source_verifier_preserved':VERIFIER,'original_source_evidence_fields':list(oldv['evidence']),'all13_original_evidence_values_preserved':True,'sole_evidence_addition':'post_integration','canonical_original13_hash':sha(enc(oldv['evidence'])),'canonical_hash_writer':"(json.dumps(evidence, ensure_ascii=False, indent=2) + '\\n').encode('utf-8'); insertion order; no sort_keys; default separators; one LF",'current_normal_state':'VERIFIED','STABILIZING_reservations':[],'proof_owner_preserved':OWNER,'raw_ledger_is_exact_core_ledger_plus_one_release_append':True,'raw_ledger_sha256':sha(read(LP)),'foreign_normal_states_preserved':286,'foreign_raw_frontier_inventory_and_hashes_preserved':445,'own_cell_before_sha256':sha(before_raw),'own_cell_after_sha256':sha(a_raw),'own_cell_changed_json_paths':paths,'own_cell_inverse_exact':True,'README_before_sha256':sha(before_readme),'README_after_sha256':sha(readme),'README_old_raw_suffix_exact':True,'README_added_prefix_bytes':len(prefix),'all8_shared_payload_bytes_source_Test_lesson_pub_seal_A1_protocol_pins_unchanged':True,'sourcefile_sha256':sourcefiles,'accepted_audit_unchanged_sha256':sha(read(AP)),'actual_final_overlay_receipts':receipts,'final_focused_overlay_checks':['frontier PASS','semantic PASS','contributor PASS','publication PASS'],'official_8gates_122tests_Chrome48_and_root8_authority':'Previously actually accepted immutable core7ad; exact acceptance/public references rechecked; not re-run or upgraded to a future metadata commit.','pixel_review_repeated':False,'new_mathematical_or_source_verdict':False,'reviewer_API_build_browser_OS_stage_commit_calls':0,'selected_C7_local_cycle_closed':True,'limits':['Actual source37645, first-V carrier8af, real-main mergee193 and accepted local core7ad remain separate; no predicted metadata carrier hash.','Original48 selected viewport/node acceptance only: mobile exact Lean/code continues below viewport; complete code supported by DOM/download/Git, not all-lines pixels. Global190/neighbour layout and entire typed semantic ledger not accepted in one screenshot.','Private Test/extra native/old DensityAffinity/ancillary subject-outline rows are DOM/UI only. Own-site HTTP only; external GitHub/public remote delivery/original owner release unconfirmed.','Full C8 alias/moment/Gaussian pipeline, both main bounds/TV/caps/expected-cost closure, postmerge purification/Exposition Seal and whole Goal remain open.','Historical source phase/application/failure/acceptance-at-creation records were preserved, not retroactively upgraded.','No full4.8GB scan, proof/module/source re-review, image rereview, fresh Lean/site/browser or API execution by this reviewer.']}
put('final-metadata-readback-review.json',report)
put('evidence-manifest.json',{'state':'ACTUAL_BOUNDED_FINAL_METADATA_READBACK','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_files':inputs,'raw_foreign_frontier_manifest':foreign,'full_scan_repeated':False,'core':CORE})
files={str(p.relative_to(O)):{'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(O.iterdir()) if p.is_file()}
put('freeze-manifest.json',{'state':'FROZEN_ACTUAL_C7_FINAL_METADATA_MECHANICAL_ACCEPTANCE','files':files})
print(json.dumps({'verdict':report['verdict'],'report_sha256':sha((O/'final-metadata-readback-review.json').read_bytes()),'freeze_sha256':sha((O/'freeze-manifest.json').read_bytes()),'own_projection_sha256':sha((O/'exact-own-cell-projection.json').read_bytes()),'release_receipt_sha256':report['actual_existing_V_release_receipt_sha256'],'archive_files':len(tar_files),'directory':str(O)},ensure_ascii=False))
