from pathlib import Path
import json,hashlib,datetime,sys
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-rough-mean-gradient56';O=R/'source-review56'
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
opening=json.loads((O/'initial-source-lease.raw.snapshot.json').read_bytes());assert (R/'source.review.lease.json').read_bytes()==(O/'initial-source-lease.raw.snapshot.json').read_bytes()
for p in opening['input_artifacts']:
 actual=pin(ROOT/p['path']);assert all(actual[k]==p[k] for k in ['bytes','raw_sha256','lf_sha256'])
manifest=json.loads((O/'manifest.json').read_bytes());complete=json.loads((O/'complete.json').read_bytes())
for j in [manifest,complete]:assert sha(canon({k:v for k,v in j.items() if k!='content_self_sha256'}))==j['content_self_sha256']
for p in manifest['outputs']:
 a=pin(ROOT/p['path']);assert a==p
outputs=manifest['outputs']+[pin(O/'manifest.json'),pin(O/'complete.json')]
assert len(sys.argv)==2 and sys.argv[1]
closing=dict(opening);closing.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'NOT_STARTED_CLOSED','compiler_started':False,'closed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_open_snapshot':pin(O/'initial-source-lease.raw.snapshot.json'),'original_open_byte_identity_preserved':True,'exact_input_count':432,'all432_input_pins_actual_rechecked':True,'output_artifacts':outputs,'all_output_readbacks_verified':True,'result':pin(O/'result0.json'),'reviewer_native_run':pin(O/'reviewer.source.run.json'),'separate_operational_repair_review':pin(O/'decoder-locator-review56/review.json'),'separate_operational_repair_closed_lease':pin(O/'decoder-locator-review56/lease.json'),'process_resource_evidence':{'previous_verification_exit0':'2d754f','previous_locator_review_exit0':'299d8d','previous_source_author_exit0':'4b614d','seal_process_exit0':'ACTUAL_SEAL_EXIT0_SUPPLIED_BY_ENCLOSING_TOOL_BEFORE_THIS_FINALIZER','current_finalizer':'Synchronous Python. All operations have completed and handles closed before final lease readback returns; enclosing tool must observe actual EXIT0. No session, detached tool or background helper launched.','final_lease_is_last_write':True,'compiler':'NOT_STARTED_CLOSED'},'negative_chronology_preserved':True,'strict_final_proof_body_blindness':False,'strict_decoder_source_identity_blindness':False,'mathematical_or_aggregate_gate_admission':False,'hash_contract':{'complete_self_field':'content_self_sha256','recipe':'Canonical UTF8 JSON ensure_ascii=False sorted keys compact comma/colon; COMPLETE final native lease excluding only content_self_sha256. No named-payload subset.','raw_lf':'Exact physical bytes / CRLF->LF bytes, printed externally after actual final readback; no circular embedded self raw hash.'}})
closing['process_resource_evidence']['seal_process_exit0']={'actual_chunk_id':sys.argv[1],'exit_code':0,'session_id':None}
closing['content_self_sha256']=sha(canon(closing));p=R/'source.review.lease.json';p.write_bytes((json.dumps(closing,ensure_ascii=False,indent=2)+'\n').encode());read=json.loads(p.read_bytes());assert read==closing;assert sha(canon({k:v for k,v in read.items() if k!='content_self_sha256'}))==read['content_self_sha256']
print(json.dumps({'status':'CLOSED','final_lease':pin(p),'complete_self_sha256':read['content_self_sha256'],'input_count':432,'output_count':len(outputs),'compiler':'NOT_STARTED_CLOSED'}))
