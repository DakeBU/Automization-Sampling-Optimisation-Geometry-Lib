from pathlib import Path
import hashlib,json,datetime,os,subprocess
out=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-root-preproof64/independent-header64');pre=out.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((out/'primary-before-header-reread-receipt.json').read_bytes());proc=json.loads((out/'source-reread.process-receipt.json').read_bytes());assert proc['actual_exit_code']==0 and proc['terminal'];assert not r['exact_header0_or_header1_received_or_read']
seal={'schema':1,'event':'SOURCE_GRAPH_BEFORE_EXACT_HEADER_INPUT_PIN','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'source_graph_sha256':r['graph_sha256'],'source_coverage_sha256':r['coverage_sha256'],'source_raw_sha256':r['primary_source_raw_sha256'],'preread_receipt_sha256':sha(out/'primary-before-header-reread-receipt.json'),'actual_preread_process_receipt_sha256':sha(out/'source-reread.process-receipt.json'),'exact_headers_read':False,'original_source_binders':r['source_inputs']}
(out/'pre-header-source-seal.json').write_bytes((json.dumps(seal,indent=2)+'\n').encode())
files=[]
for name in ['header0.lean','header1.lean','root.named-types64.adoption.json']:
 p=pre/name;raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n');(out/(name+'.raw.snapshot.txt')).write_bytes(raw);(out/(name+'.lf.snapshot.txt')).write_bytes(lf)
 files.append({'path':str(p),'name':name,'raw_sha256':hashlib.sha256(raw).hexdigest(),'lf_sha256':hashlib.sha256(lf).hexdigest(),'bytes':len(raw),'first_exact_read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 print('EXACT INPUT '+name+'\n'+raw.decode('utf8'))
record={'schema':1,'event':'EXACT_HEADER_INPUTS_READ_AFTER_SOURCE_GRAPH_SEAL','actual_pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pre_header_source_seal_sha256':sha(out/'pre-header-source-seal.json'),'workspace_commit_observed':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r'E:/Samplinglib',text=True).strip(),'inspected_science_commit':'4d02622332d02d0bd6c977d3cee48fd535ebf203','files':files,'compile_run':False,'proof_search':False}
(out/'exact-header-input-pins.json').write_bytes((json.dumps(record,indent=2)+'\n').encode());print('INPUT PINS SHA256 '+sha(out/'exact-header-input-pins.json'))
