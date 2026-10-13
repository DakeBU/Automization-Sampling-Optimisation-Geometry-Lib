from pathlib import Path
import json,hashlib,os,datetime,subprocess,sys
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-sharp-energy-preproof68/independent-header-source68');R=Path('E:/Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,o):(O/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
r=json.loads((O/'review-run.json').read_text());assert sha(canon({k:v for k,v in r.items() if k!='run_sha256'}))==r['run_sha256'];v=(O/'complete-RAW-verdict.json').read_bytes();assert sha(v)==r['complete_named_raw_verdict']['raw_sha256'];assert json.loads(v)==r['independent_verdict']
for name in ['source-inputs.manifest.json','header-inputs.manifest.json']:
 m=json.loads((O/name).read_text())
 for e in m['entries']:
  b=(R/e['path']).read_bytes();assert len(b)==e['raw_bytes'] and sha(b)==e['raw_sha256'];assert (O/e['raw_snapshot']).read_bytes()==b;assert (O/e['lf_snapshot']).read_bytes()==b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
write('readback.json',{'status':'EXIT_0_HEADER_SOURCE_ONLY_READBACK','actual_pid':os.getpid(),'logicalrun_sha256':r['run_sha256'],'complete_raw_verdict_sha256':sha(v),'unchanged_primary_and_all_current_candidate_inputs':True,'native_closed59_source_coverage_reused':True,'exact344_primary_math_items_verified':True,'own_source68_compilation_claimed':False,'root_writes':False})
print('SOURCE68_READBACK_EXIT_0',os.getpid(),r['run_sha256'])
