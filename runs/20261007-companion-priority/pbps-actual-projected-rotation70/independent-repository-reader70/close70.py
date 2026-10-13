import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,datetime,base64
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (O/'lease.final.json').exists()
inputs=json.loads((O/'input-manifest70.json').read_bytes())
for q in inputs['inputs']:
 b=pathlib.Path(q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
run=json.loads((O/'review.run.json').read_bytes());r=dict(run);old=r.pop('run_sha256');assert sha(canon(r))==old
payload=json.loads((O/'complete-named-review-decision-input-payload.json').read_bytes());assert payload['finite_input_manifest_RAW_sha256']==sha((O/'input-manifest70.json').read_bytes())
for q in payload['named_RAW_layers']:
 b=base64.b64decode(q['raw_base64'],validate=True);assert b==(O/q['name']).read_bytes() and len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256']
assert json.loads((O/'finalize-named70.terminal-receipt.json').read_bytes())['exit_code']==0
entries=[]
for p in sorted(O.rglob('*')):
 if not p.is_file():continue
 assert p.name not in ['lease.final.json','owned-manifest.json']
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');entries.append({'path':str(p.relative_to(O)).replace('\\','/'),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'LF_recipe':'CRLF to LF only','mtime_ns_at_close':p.stat().st_mtime_ns})
manifest={'schema':'independent-repository-reader70-owned-manifest-v1','count':len(entries),'exclusions':['Only owned-manifest.json self and last lease.final.json; last lease binds this manifest.'],'entries':entries,'entries_canonical_sha256':sha(canon(entries))};write('owned-manifest.json',manifest)
mb=(O/'owned-manifest.json').read_bytes();pb=(O/'complete-named-review-decision-input-payload.json').read_bytes();db=(O/'repository-reader70.decision.json').read_bytes();pc=json.loads((O/'preclose70.terminal-receipt.json').read_bytes())
lease={'schema':'independent-repository-reader70-CLOSED-LAST-native-lease-v1','status':'CLOSED_LAST','owned_directory':str(O).replace('\\','/'),'owned_count':len(entries)+2,'bound_layer_count':len(entries)+1,'manifest':{'path':'owned-manifest.json','RAW_bytes':len(mb),'RAW_sha256':sha(mb),'entries_canonical_sha256':manifest['entries_canonical_sha256']},'whole_logical_run_sha256':old,'decision_RAW_sha256':sha(db),'complete_named_payload':{'path':'complete-named-review-decision-input-payload.json','RAW_bytes':len(pb),'RAW_sha256':sha(pb)},'finite_input_count':inputs['count'],'final_packet_current_input_count':140,'final_preclose_actual_PID':pc['actual_pid'],'final_preclose_actual_EXIT':pc['exit_code'],'actual_close_python_PID':os.getpid(),'actual_close_parent_PID':os.getppid(),'close_EXIT_authority':'Actual foreground tool return after this last owned write; no predicted EXIT is asserted inside lease.','last_owned_write':'lease.final.json','no_further_owned_writes':True,'RAW_authoritative_LF_recipe':'Only CRLF byte pairs become LF; no trim or other normalization.','no_self_hash_policy':'Lease self RAW hash is observed externally by read-only postclose.','old_CLOSED_and_canonical_Git_ledger_Goal_untouched':True,'scope':'Accept scoped aggregate and scoped local reader only; no new science/source/VERIFIED/fullpaper credit.','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
write('lease.final.json',lease)
print(json.dumps({'actual_close_PID':os.getpid(),'status':'CLOSED_LAST','owned_count':lease['owned_count'],'finite_inputs':inputs['count'],'whole_logical_run_sha256':old,'decision_RAW_sha256':sha(db),'manifest_RAW_sha256':sha(mb),'entries_canonical_sha256':manifest['entries_canonical_sha256'],'named_payload_RAW_bytes':len(pb),'named_payload_RAW_sha256':sha(pb),'lease_RAW_sha256':sha((O/'lease.final.json').read_bytes())},ensure_ascii=False))
