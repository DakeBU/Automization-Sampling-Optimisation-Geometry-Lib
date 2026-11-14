from pathlib import Path
import sys,subprocess,json,datetime,time,hashlib,base64,os,stat
P=Path("/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261111/kr_src_c47e12/phase5-normal-sourceV");ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');S=P.parent;PRIVATE=S/'private-phase5-preservation'
h=lambda b:hashlib.sha256(b).hexdigest()
child_code=r"""from pathlib import Path
import sys,json,hashlib,stat,datetime
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');S=ROOT/'.astis/semantic-neutral-20261111/kr_src_c47e12';P=S/'phase5-normal-sourceV';PRIVATE=S/'private-phase5-preservation';W=ROOT/'.astis/huanjian-gc-fixed-spectrum-krylov-range-20261110';E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(P))
import preservation_guard as g
h=lambda b:hashlib.sha256(b).hexdigest()
old=(PRIVATE/'old-ledger.raw').read_bytes();ledger=(ROOT/g.LEDGER).read_bytes();append=(P/'actual-normal-VERIFIED-append.exact.jsonl').read_bytes()
assert ledger==old+append and h(append)=='959a610cedf1d4f35528664abee862361c636ec1da3ec79f3a91565c29b3e9e9'
rows,state=g.replay(ledger);baseline=json.loads((PRIVATE/'full-baseline.private.json').read_text())
assert {k:v for k,v in state.items()if k!=g.ADV}==baseline['all_foreign_states']
assert [r for r in rows[:len(baseline['complete_existing_records'])]if r.get('to_state')=='VERIFIED']==baseline['all_existing_VERIFIED_objects']
assert state[g.ADV]['state']=='VERIFIED'and state[g.ADV]['owner_id']==g.OWNER and state[g.ADV]['last_actor']==g.ACTOR
events=[r for r in rows if r.get('advance_id')==g.ADV and r.get('to_state')=='VERIFIED']
assert len(events)==1 and events[0]==json.loads(append)
assert events[0]['evidence']['verifier_id']==g.ACTOR
assert events[0]['evidence']==json.loads((P/'normal-VERIFIED-evidence.full.json').read_text())
before=(PRIVATE/'old-own-frontier.raw').read_bytes();after=(ROOT/g.FRONT).read_bytes()
assert after==before.replace(b'"status": "proved_locally"',b'"status": "independently_verified"',1)
f=json.loads(after);b=json.loads(before);expected=dict(b);expected['status']='independently_verified';assert f==expected
assert (P/'normal-VERIFIED-attempted-once.PERMANENT.json').exists()
source_archive=json.loads((E/'fresh-source-c47e12-phases1-4-all-original-files.archive-manifest.json').read_text())
native_archive=json.loads((E/'fresh-native-5f09a3-all-original-files.archive-manifest.json').read_text())
preserved=[]
for label,manifest,origin in [('source-originals',source_archive,S),('native-originals',native_archive,W/'independent-native-reader-5f09a3')]:
 for rel,r in manifest['files'].items():
  path=origin/rel;data=path.read_bytes()
  assert len(data)==r['bytes']and h(data)==r['sha256']and oct(stat.S_IMODE(path.stat().st_mode))==r['original_mode'],rel
 # Enumerated original manifest paths only. Never glob S after private baseline exists.
 preserved.append({'category':label,'original_files':len(manifest['files']),'all_bytes_and_modes_exact':True,'original_archive_sha256':manifest['sha256']})
audit_receipts=0
for rp in sorted((P/'audit').glob('*.receipt.json')):
 r=json.loads(rp.read_text());assert r['exit_code']==0
 for k in ['stdout','stderr']:
  data=(rp.parent/r[k]['path']).read_bytes();assert len(data)==r[k]['bytes']and h(data)==r[k]['sha256']
 audit_receipts+=1
inputs=[]
for path in sorted((P/'original-inputs').iterdir()):
 if path.is_file():
  data=path.read_bytes();inputs.append({'retained_original_copy':str(path.relative_to(P)),'bytes':len(data),'sha256':h(data)})
for path in sorted((P/'metadata-git-readback').glob('*.receipt.json')):
 r=json.loads(path.read_text());assert r['exit_code']==0
 idx=path.name.split('.')[0]
 data=(path.parent/(idx+'.raw')).read_bytes();assert h(data)==r['stdout_sha256']
 inputs.append({'actual_readonly_Git_argv':r['argv'],'bytes':len(data),'sha256':h(data),'retained_copy':'metadata-git-readback/'+idx+'.raw'})
inventory={'retained_original_input_artifacts':inputs,'original_source_and_native_manifest_validation':preserved,'private_process_guard_inputs':'Full private W baseline/control lists and fresh foreign snapshots are intentionally not exported. Full values and raw Git list outputs remain solely in sibling private-phase5-preservation; portable counts/digests/scope attest exact full-value postguards.','all_private_foreign_baseline_data_excluded_from_portable':True,'normal_API_implementation_file':{'path':'tools/astis_advance.py','sha256':h((ROOT/'tools/astis_advance.py').read_bytes())},'normal_API_actual_execution_receipt':{'path':'audit/0011-exactly-one-normal-VERIFIED.receipt.json','sha256':h((P/'audit/0011-exactly-one-normal-VERIFIED.receipt.json').read_bytes())},'permanent_marker_sha256':h((P/'normal-VERIFIED-attempted-once.PERMANENT.json').read_bytes())}
(P/'complete-input-and-execution-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
out={'final_closure_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_actor':g.ACTOR,'normal_API_calls':1,'root_sourceV_API_calls':0,'state':'VERIFIED','owner_id_preserved':g.OWNER,'old_ledger_prefix_exact':True,'old_ledger_bytes':len(old),'all299_foreign_full_states_latest_evidence_exact':True,'all316_existing_VERIFIED_objects_complete_values_exact':True,'sole_new_append_sha256':h(append),'frontier_status':'independently_verified','only_frontier_status_changed':True,'full_reader_HOLD_and_boundary_values_exact':True,'original_source_native_preservation':preserved,'all_prior_raw_command_receipts_valid':audit_receipts,'normal_action_never_replayed':True,'private_foreign_baseline_exported':False,'no_reader_global_STAB_lease_remote_or_Goal_acceptance':True}
(P/'final-ledger-frontier-originals-readback.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
"""
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.monotonic();argv=['/opt/anaconda3/bin/python','-c',child_code]
r=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
receipt={'schema':'original-phase5-final-actual-execution-receipt-v1','actual_actor':'/root/krylov_fresh_source_c47e12','wrapper_argv':sys.argv,'wrapper_file_sha256':h(Path(__file__).read_bytes()),'child_argv':argv,'cwd':str(ROOT),'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t0,'exit_code':r.returncode,'stdout_raw_base64':base64.b64encode(r.stdout).decode('ascii'),'stderr_raw_base64':base64.b64encode(r.stderr).decode('ascii'),'stdout_sha256':h(r.stdout),'stderr_sha256':h(r.stderr),'actual_normal_API_execution_receipt_sha256':h((P/'audit/0011-exactly-one-normal-VERIFIED.receipt.json').read_bytes()),'actual_normal_API_command_argv':['/opt/anaconda3/bin/python',str(P/'execute_normal_once.py')],'actual_normal_API_program_sha256':h((P/'execute_normal_once.py').read_bytes()),'normal_VERIFIED_API_calls_by_this_actor':1,'root_sourceV_API_calls':0,'actual_new_VERIFIED_append_sha256':h((P/'actual-normal-VERIFIED-append.exact.jsonl').read_bytes()),'note':'Exact final subprocess byte streams are base64 encoded without normalization. This receipt is in the following detached complete portable manifest. Full foreign baselines/raw old ledger stay private outside this directory. Final hash reporting appears in original tool transcript.'}
rp=P/'original-final-execution-receipt.json';rp.write_text(json.dumps(receipt,indent=2)+'\n')
sys.stdout.buffer.write(r.stdout);sys.stdout.buffer.flush();sys.stderr.buffer.write(r.stderr);sys.stderr.buffer.flush()
if r.returncode:raise SystemExit(r.returncode)
# Only this own portable directory is inventoried; never S or the sibling private baseline.
rows=[]
for path in sorted(P.rglob('*')):
 if path.is_file()and path.name!='hash-manifest.json':
  assert not path.is_symlink(),str(path);os.chmod(path,0o444);data=path.read_bytes()
  rows.append({'path':str(path.relative_to(P)),'bytes':len(data),'sha256':h(data),'mode':'0444'})
m={'schema':'immutable-portable-phase5-normal-sourceV-manifest-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_actor':'/root/krylov_fresh_source_c47e12','advance_id':'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumKrylovRange','normal_VERIFIED_API_calls':1,'root_sourceV_API_calls':0,'state':'VERIFIED','frontier_status':'independently_verified','original_owner_id_preserved':'huanjian_gc_20261110_fixed_spectrum_krylov_range','mathematical_candidate':'972d8994a816bc63d2dd6fb2db1c2c638fa9a48f','metadata_checked_commit':'d4ff03bf3574da615cca39a812cd9b442dca47f0','actual_new_VERIFIED_append_sha256':h((P/'actual-normal-VERIFIED-append.exact.jsonl').read_bytes()),'reader_HOLD_and_global_exclusions_preserved':True,'full_private_foreign_baselines_included':False,'scope':'Every own portable phase5 file except this detached manifest. Original input archives/logs/receipts and full own PLOCAL/new V payloads retained. Full foreign baseline/raw old ledger/private Git lists remain solely in sibling private-phase5-preservation. No normalization of original EOFs or outputs. No post-V replay or global action.','files':rows,'file_mode':'0444','directory_mode':'0555'}
mp=P/'hash-manifest.json';mp.write_text(json.dumps(m,indent=2)+'\n');os.chmod(mp,0o444)
for d in sorted([x for x in P.rglob('*')if x.is_dir()],key=lambda x:len(x.parts),reverse=True):os.chmod(d,0o555)
os.chmod(P,0o555)
for path in [P]+list(P.rglob('*')):assert stat.S_IMODE(path.stat().st_mode)==(0o555 if path.is_dir()else 0o444)
for row in rows:
 data=(P/row['path']).read_bytes();assert len(data)==row['bytes']and h(data)==row['sha256']
for path in PRIVATE.rglob('*'):
 if path.is_file():os.chmod(path,0o600)
for d in sorted([x for x in PRIVATE.rglob('*')if x.is_dir()],key=lambda x:len(x.parts),reverse=True):os.chmod(d,0o700)
os.chmod(PRIVATE,0o700)
print(json.dumps({'portable_manifest_sha256':h(mp.read_bytes()),'original_final_execution_receipt_sha256':h(rp.read_bytes()),'actual_normal_API_execution_receipt_sha256':h((P/'audit/0011-exactly-one-normal-VERIFIED.receipt.json').read_bytes()),'actual_new_VERIFIED_append_sha256':h((P/'actual-normal-VERIFIED-append.exact.jsonl').read_bytes()),'portable_files':len(rows)+1,'portable_files_0444_directories_0555':True,'private_baseline_files_0600_directory_0700':True,'normal_VERIFIED_API_calls':1,'root_sourceV_API_calls':0,'frontier_status':'independently_verified','reader_HOLD_and_global_exclusions_preserved':True,'exit_code':0},indent=2))

