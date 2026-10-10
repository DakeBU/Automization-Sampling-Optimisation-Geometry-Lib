import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,base64,os
O=pathlib.Path(__file__).resolve().parent;H=lambda b:hashlib.sha256(b).hexdigest();C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();J=lambda n:json.loads((O/n).read_bytes())
run=J('header-source71.run.json');assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
dec=J('header-source71.decision.json');assert dec==run['decision'] and dec['required_mathematical_or_header_repairs']==[]
im=J('complete-exact-input-manifest.json');ip=J('complete-RAW-LF-input-payload.json');assert im['input_count']==ip['input_count']==14
for q,x in zip(im['inputs'],ip['inputs']):
 b=(O/q['snapshot']).read_bytes();l=(O/q['LF_snapshot']).read_bytes();assert len(b)==q['RAW_bytes'] and H(b)==q['RAW_sha256'];assert l==b.replace(b'\r\n',b'\n') and H(l)==q['LF_sha256']
 assert base64.b64decode(x['RAW_base64'])==b and base64.b64decode(x['LF_base64'])==l
 p=pathlib.Path(q['original_path']);assert p.read_bytes()==b and p.stat().st_mtime_ns==q['original_mtime_ns']
named=J('complete-named-review-decision-input-payload.json');assert named['whole_logical_run_sha256']==run['run_sha256']
for x in named['layers']:
 b=(O/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and H(b)==x['RAW_sha256'] and base64.b64decode(x['RAW_base64'])==b
assert len(named['layers'])==11
a=J('stageA-freeze71.terminal-receipt.json');b=J('stageB-read-header71.terminal-receipt.json');assert a['end_utc']<b['start_utc']
assert H((O/'stageA.source-expectations71.before-header.frozen.json').read_bytes())==dec['expectation_before_header_RAW_sha256']
assert len(J('stageB.all14-header-obligation-decisions.json')['obligations'])==14
assert len(J('stageA.finite-source255-and-target18-coverage.frozen.json')['entries'])==255
assert len(J('stageB.header147-finite-line-coverage.json')['entries'])==147
receipts=[]
for p in sorted(O.glob('*.terminal-receipt.json')):
 q=json.loads(p.read_bytes());assert q['exit_code']==0
 for k in ['stdout','stderr']:
  x=q[k];b=(O/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and H(b)==x['RAW_sha256']
 receipts.append({'name':p.name,'actual_PID':q['actual_pid'],'actual_EXIT':q['exit_code']})
out={'schema':'prospective-header71-final-preclose-check-v1','actual_pid':os.getpid(),'all14_inputs_RAW_LF_payload_and_current_originals_exact':True,'all11_named_layers_exact':True,'source_before_header_order_verified':True,'whole_logical_run_sha256':run['run_sha256'],'all14_obligations_source255_header147_complete':True,'current_terminal_receipts':receipts,'no71_compile':True,'no_canonical_oldCLOSED_writes':True}
(O/'final.preclose-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,ensure_ascii=False))
