import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,base64,datetime
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (O/'lease.final.json').exists()
pc=json.loads((O/'preclose70.terminal-receipt.json').read_bytes());assert pc['exit_code']==0
layers=[]
for n in ['repository-reader70.full-review.RAW.md','repository-reader70.decision.json','bounded-synthesis70.json','input-manifest70.json','repository70.checks.json','reader70.checks.json','history70.checks.json','corroboration70.json','preclose70.terminal-receipt.json']:
 b=(O/n).read_bytes();layers.append({'name':n,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'raw_base64':base64.b64encode(b).decode()})
payload={'schema':'complete-named-small-review-decision-input-payload70-v1','recursion_policy':'Only this bounded native review/decision/finite-input/check layers are embedded; no prior native history or scientific payload is recursively duplicated.','finite_input_manifest_RAW_sha256':sha((O/'input-manifest70.json').read_bytes()),'named_RAW_layers':layers,'all_other_owned_helpers_failures_streams_and_snapshots':'Bound by the final owned-manifest.json and last CLOSED lease; no circular payload self hash.','LF_recipe':'Only CRLF->LF; RAW authoritative.'}
write('complete-named-review-decision-input-payload.json',payload)
def ref(n):
 b=(O/n).read_bytes();return {'path':n,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
run={'schema':'independent-repository-reader70-review-run-v1','reviewer':'/root/independent_primary69','scope':'SCI70 repository and scoped local reader only','checked_science_commit':'c46af8a55e89419109f654c4553cf527993cbeed','packet_RAW_sha256':'4b98a34d129fcd9c0d8aa5352eb25b5b198a480585a6f37edfba2726e8cf5740','conclusion':'accept_scoped_aggregate','accept_scoped_reader':True,'decision':ref('repository-reader70.decision.json'),'complete_RAW_review':ref('repository-reader70.full-review.RAW.md'),'input_manifest':ref('input-manifest70.json'),'complete_named_payload':ref('complete-named-review-decision-input-payload.json'),'preclose_actual_PID':pc['actual_pid'],'preclose_actual_EXIT':pc['exit_code'],'terminal_receipts':[ref(p.name) for p in sorted(O.glob('*.terminal-receipt.json'))],'logical_hash_recipe':'Delete ONLY top-level run_sha256; JSON UTF8 ensure_ascii=False sorted keys compact separators; preserve nested hashes and all other fields.','no_science_source_VERIFIED_fullpaper_credit':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
run['run_sha256']=sha(canonical(run));write('review.run.json',run)
print('actual_PID',os.getpid(),'PASS named payload bytes',(O/'complete-named-review-decision-input-payload.json').stat().st_size,'whole_logical_run',run['run_sha256'])
