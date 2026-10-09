from pathlib import Path
import json,hashlib,sys,datetime,argparse
ROOT=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def read(n):return json.loads((ROOT/n).read_bytes())
def encode(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def validate():
 run=read('review-run.json');payload=dict(run);payload.pop('run_sha256');assert digest(payload)==run['run_sha256'],'whole logical run hash mismatch'
 assert run['source_graph']['candidate_visible'] is False
 assert sha((ROOT/'source-proof-graph.json').read_bytes())=='f4e62204a025c69b97a7baaeee685f084877ca03d76db6a336e9f50b5865e7e8'
 for x in read('primary-first-stage-seal.json')['all_pre_candidate_files']:assert sha((ROOT/x['relative_path']).read_bytes())==x['raw_sha256'],x['relative_path']
 checks=read('candidate-input-binding-and-span-checks.json');raw=(ROOT/checks['complete_named_raw_payload']['path']).read_bytes();assert sha(raw)==checks['complete_named_raw_payload']['raw_sha256']
 for x in checks['records']:
  a=(ROOT/x['raw_snapshot']).read_bytes();lf=(ROOT/x['lf_snapshot']).read_bytes();assert sha(a)==x['raw_sha256'];assert sha(lf)==x['lf_sha256'];assert lf==a.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert a==raw[x['complete_payload_byte_start']:x['complete_payload_byte_end_exclusive']]
 for x in checks['packets']:
  for key in ['packet_canonical_hash_match','publication_binding_match','current_candidate_context_match','module_matches_packet','source_text_hash_match','statement_hash_match','reconstruction_hash_match','reviewer_independent']:assert x[key],key
 for x in checks['all12_literal_spans']:
  for key in ['source_raw_hash_match','literal_code_equals_raw_region','literal_code_hash_match','inside_actual_proof_body']:assert x[key],key
  assert sha((ROOT/x['raw_excerpt_artifact']).read_bytes())==x['declared_excerpt_sha256']
 assert len(checks['all12_literal_spans'])==12
 for i in range(2):
  native=read(f'decision.{i}.json');assert native.pop('review_run_sha256')==run['run_sha256'];assert native==run['native_decisions'][i]==read(f'candidate-verdict.{i}.frozen.json');assert set(native['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'};assert all(s['relation']!='not-audited' and s['evidence'] for s in native['semantic_slots'].values());assert native['verdict']=='equivalent-after-elaboration';assert native['source_admission']['decision']=='SCOPED_ACCEPT';assert native['full_Exposition_Seal'] is False
 assert all(x['pass'] for x in read('negative-controls64.json')['controls'])
 cc=checks['focused_compiler_evidence'];assert cc['receipt_exit_code']==0 and cc['terminal_closed'] and cc['current_three_inputs_match'] and cc['stdout_hash_match'] and cc['stderr_hash_match']
 return {'status':'PASS','logical_run_sha256':run['run_sha256'],'complete_named_raw_payload_sha256':checks['complete_named_raw_payload']['raw_sha256'],'raw_lf_input_pairs':len(checks['records']),'source_math_items_classified':len(run['source_to_candidate_coverage']['items']),'literal_proof_body_spans':12,'native_decisions':2,'candidate_verdicts_immutable':True,'negative_controls_pass':True,'source_graph_independent_and_unchanged':True}
def close_owned():
 result=validate()
 for n in ['foreground-finalizer.receipt.json','foreground-readback.receipt.json']:
  rec=read(n);assert rec['exit_code']==0 and rec['terminal_closed'] and rec['actual_foreground_pid']>0
  for key in ['stdout','stderr']:
   out=rec[key];assert sha((ROOT/out['relative_path']).read_bytes())==out['raw_sha256']
 assert not (ROOT/'lease.final.json').exists()
 lease={'schema':'astis-independent-owned-lease-v1','owner':'/root/independent_source64','state':'CLOSED_LAST','closed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned_root':str(ROOT),'opening_lease':'lease.json','logical_run_sha256':result['logical_run_sha256'],'complete_named_raw_payload':'review64-complete-inputs.named.raw.payload','complete_named_raw_payload_sha256':result['complete_named_raw_payload_sha256'],'owned_manifest':'full-owned-manifest.json','terminal_receipts':['foreground-finalizer.receipt.json','foreground-readback.receipt.json'],'last_owned_write':'lease.final.json','postclose_policy':'READ_ONLY; no further owned writes, including audit receipts','source_status':'two immutable scoped independent mathematical acceptances; no full B16/PURIFIED/Exposition/whole-paper claim'}
 lease_bytes=encode(lease);entries=[]
 for p in sorted(ROOT.rglob('*')):
  if p.is_file():entries.append({'relative_path':p.relative_to(ROOT).as_posix(),'raw_bytes':p.stat().st_size,'raw_sha256':sha(p.read_bytes())})
 entries.append({'relative_path':'lease.final.json','raw_bytes':len(lease_bytes),'raw_sha256':sha(lease_bytes)})
 manifest={'schema':'source64-full-owned-manifest-v1','created_at_utc':lease['closed_at_utc'],'owned_root':str(ROOT),'files':sorted(entries,key=lambda x:x['relative_path']),'includes_all_negative_artifacts':True,'includes_source_stage_immutable_files':True,'includes_all_input_RAW_LF_snapshots':True,'includes_actual_foreground_terminal_receipts':True,'self_file':'full-owned-manifest.json','self_hash_binding':'The exact RAW SHA256 of this manifest is returned by the foreground close and read-only postclose terminal receipts; a manifest cannot contain its own RAW hash without a circular definition. Every other owned file, including the planned CLOSED_LAST lease, is enumerated exactly.','write_order':'Full manifest written first; lease.final.json written last. Postclose is read-only.'}
 (ROOT/'full-owned-manifest.json').write_bytes(encode(manifest));(ROOT/'lease.final.json').write_bytes(lease_bytes)
 result.update({'lease_state':'CLOSED_LAST','owned_manifest_raw_sha256':sha((ROOT/'full-owned-manifest.json').read_bytes()),'final_lease_raw_sha256':sha(lease_bytes),'manifest_entries':len(entries),'owned_files_including_manifest':len(entries)+1,'postclose_policy':'READ_ONLY'})
 return result
def postclose():
 result=validate();manifest=read('full-owned-manifest.json');lease=read('lease.final.json');assert lease['state']=='CLOSED_LAST';listed={x['relative_path'] for x in manifest['files']};actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()};assert actual==listed|{'full-owned-manifest.json'}
 for x in manifest['files']:
  p=ROOT/x['relative_path'];assert p.stat().st_size==x['raw_bytes'];assert sha(p.read_bytes())==x['raw_sha256'],x['relative_path']
 last=(ROOT/'lease.final.json').stat().st_mtime_ns;assert all(p.stat().st_mtime_ns<=last for p in ROOT.rglob('*') if p.is_file())
 result.update({'phase':'READ_ONLY_POSTCLOSE','lease_state':'CLOSED_LAST','owned_manifest_raw_sha256':sha((ROOT/'full-owned-manifest.json').read_bytes()),'final_lease_raw_sha256':sha((ROOT/'lease.final.json').read_bytes()),'manifest_entries':len(manifest['files']),'no_postclose_writes':True})
 return result
if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='close':out=close_owned()
 elif mode=='postclose':out=postclose()
 else:
  out=validate();out['phase']=mode
  if mode=='finalizer':(ROOT/'validation-summary.json').write_bytes(encode(out))
 print(json.dumps(out,ensure_ascii=False,indent=2))
