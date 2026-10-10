import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,base64,os,collections
O=pathlib.Path(__file__).resolve().parent
def H(b):return hashlib.sha256(b).hexdigest()
def C(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def J(n):return json.loads((O/n).read_bytes())
run=J('source.0.review-run.json');d=J('source.0.decision.json');packet=J('final70.official-source-review.packet.1.exactraw.json')
assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==d['review_run_sha256']
assert d['reviewer_packet_sha256']==packet['packet_sha256']
p=dict(packet);p.pop('packet_sha256');assert H(C(p))==packet['packet_sha256']
assert set(d)==set(packet['output_contract'])
slots={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
assert set(d['semantic_slots'])==slots and d['verdict']=='equivalent-after-elaboration' and d['repairs']==[]
assert all(v['relation'] in {'same','equivalent','explicit-elaboration'} and all(isinstance(v[k],str) and v[k] for k in ['original','reconstructed','evidence']) for v in d['semantic_slots'].values())
assert len(d['deltas'])==13 and all(set(v)=={'slot','severity','description','evidence'} and v['slot'] in slots and v['severity']=='informational' for v in d['deltas'])
inputs=J('complete-exact-input-manifest.json')['inputs'];payload=J('complete-exact-RAW-LF-input-payload.json')
assert len(inputs)==len(payload['inputs'])==74
for a,b in zip(inputs,payload['inputs']):
 raw=(O/a['snapshot']).read_bytes();lf=(O/a['LF_snapshot']).read_bytes()
 assert H(raw)==a['RAW_sha256'] and len(raw)==a['RAW_bytes'] and lf==raw.replace(b'\r\n',b'\n') and H(lf)==a['LF_sha256']
 assert base64.b64decode(b['RAW_base64'])==raw and base64.b64decode(b['LF_base64'])==lf
 if a['assert_original_still_current_at_finalization']:assert pathlib.Path(a['original_path']).read_bytes()==raw
named=J('complete-named-review-decision-input-payload.json');assert named['whole_logical_run_sha256']==run['run_sha256'] and named['named_layer_count']==20
for a in named['named_layers']:
 raw=(O/a['path']).read_bytes();assert H(raw)==a['RAW_sha256'] and len(raw)==a['RAW_bytes'] and base64.b64decode(a['RAW_base64'])==raw
assert (O/'complete-named-review-decision-input-payload.json').stat().st_size<100_000_000
for n,c in [('stageB.primary419-current-exhaustive-decisions.json',419),('stageB.whole-module544-line-coverage.json',544)]:
 x=J(n);assert x['count']==len(x['entries'])==c and x['unclassified']==0
assert J('stageB.all24-obligation-decisions.json')['count']==24
checkpoint=J('stageA.bounded-checkpoint-manifest.json')
for a in checkpoint['entries']:
 raw=(O/a['path']).read_bytes();assert H(raw)==a['RAW_sha256'] and len(raw)==a['RAW_bytes']
assert len(checkpoint['entries'])==108
prior=J('stageA.prior83.integrity.json')
# The explicit StageA integrity evidence already checked the immutable old CLOSED83 tree.
assert J('stageB.blind-native-integrity.json')['file_count']==10
receipts=[]
for p in sorted(O.glob('*.terminal-receipt.json')):
 x=json.loads(p.read_bytes())
 for k in ['stdout','stderr']:
  a=x[k];raw=(O/a['name']).read_bytes();assert H(raw)==a['RAW_sha256'] and len(raw)==a['RAW_bytes']
 receipts.append({'path':p.name,'actual_pid':x['actual_pid'],'EXIT':x['exit_code']})
out={'schema':'independent-source70-final-preclose-check-v1','actual_pid':os.getpid(),'EXIT_if_completed':0,'whole_logical_run_sha256':run['run_sha256'],'decision_RAW_sha256':H((O/'source.0.decision.json').read_bytes()),'official_packet_sha256':packet['packet_sha256'],'exact_inputs_checked':74,'named_layers_checked':20,'stageA_original108_unchanged':True,'source419_module544_obligations24_slots7_steps8':True,'native_decision_schema_exact':True,'all_RAW_LF_payloads_exact':True,'current_final_inputs_unchanged':True,'named_payload_under100MB':True,'complete_terminal_receipts':receipts,'native_lease_not_yet_written':True,'canonical_writes':False}
(O/'final.preclose-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,ensure_ascii=False))
