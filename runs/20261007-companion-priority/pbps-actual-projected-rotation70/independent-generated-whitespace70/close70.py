import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,datetime,base64
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (O/'lease.final.json').exists()
inp=json.loads((O/'input-manifest.json').read_bytes())
for q in inp['inputs']:
 b=pathlib.Path(q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
for q in inp['other137_original_packet_inputs_checked_in_place_not_duplicated']:
 b=pathlib.Path(q['path']).read_bytes();assert sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
assert json.loads((O/'finalize.terminal-receipt.json').read_bytes())['exit_code']==0
run=json.loads((O/'review.run.json').read_bytes());h=run.pop('run_sha256');assert sha(canon(run))==h
payload=json.loads((O/'complete-named-review-decision-input-payload.json').read_bytes())
for q in payload['named_RAW_layers']:
 b=base64.b64decode(q['raw_base64'],validate=True);assert b==(O/q['name']).read_bytes() and len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256']
entries=[]
for p in sorted(O.iterdir()):
 if not p.is_file():continue
 assert p.name not in ['lease.final.json','owned-manifest.json'];b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');entries.append({'path':p.name,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'mtime_ns_at_close':p.stat().st_mtime_ns})
m={'schema':'independent-generated-whitespace70-owned-manifest-v1','count':len(entries),'LF_recipe':'Only CRLF bytes become LF; no trim.','entries':entries,'entries_canonical_sha256':sha(canon(entries)),'exclusions':['self owned-manifest.json and last lease.final.json only']};write('owned-manifest.json',m)
mb=(O/'owned-manifest.json').read_bytes();pb=(O/'complete-named-review-decision-input-payload.json').read_bytes();db=(O/'overlay.decision.json').read_bytes();a=json.loads((O/'audit-overlay.terminal-receipt.json').read_bytes())
l={'schema':'independent-generated-whitespace70-CLOSED-LAST-v1','status':'CLOSED_LAST','owned_count':len(entries)+2,'bound_layer_count':len(entries)+1,'manifest_RAW_sha256':sha(mb),'manifest_entries_canonical_sha256':m['entries_canonical_sha256'],'whole_logical_run_sha256':h,'decision_RAW_sha256':sha(db),'complete_named_payload':{'path':'complete-named-review-decision-input-payload.json','RAW_bytes':len(pb),'RAW_sha256':sha(pb)},'actual_audit_PID':a['actual_pid'],'actual_audit_EXIT':a['exit_code'],'actual_close_python_PID':os.getpid(),'close_EXIT_authority':'Actual foreground terminal return following last write; not predicted in lease.','finite_input_count':inp['count'],'other_original_current_inputs_checked':137,'original_CLOSED213_unchanged':True,'last_owned_write':'lease.final.json','no_further_owned_writes':True,'no_self_hash_policy':'Lease hash observed by external read-only postclose.','no_canonical_Git_ledger_source_math_VERIFIED_writes_or_credit':True,'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};write('lease.final.json',l)
print(json.dumps({'actual_close_PID':os.getpid(),'status':'CLOSED_LAST','owned_count':l['owned_count'],'finite_inputs':inp['count'],'whole_logical_run_sha256':h,'decision_RAW_sha256':sha(db),'manifest_RAW_sha256':sha(mb),'named_payload':l['complete_named_payload'],'lease_RAW_sha256':sha((O/'lease.final.json').read_bytes())}))
