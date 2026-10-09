from pathlib import Path
import hashlib,json,os,datetime
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-sharp-energy-preproof68/independent-header-source68');R=Path('E:/Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,o):(O/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
assert not (O/'lease.final.json').exists();r=json.loads((O/'review-run.json').read_text());assert sha(canon({k:v for k,v in r.items() if k!='run_sha256'}))==r['run_sha256'];assert json.loads((O/'foreground-readback.terminal.json').read_text())['actual_exit']==0
for n in ['source-inputs.manifest.json','header-inputs.manifest.json']:
 for e in json.loads((O/n).read_text())['entries']:assert sha((R/e['path']).read_bytes())==e['raw_sha256']
files=sorted([p for p in O.rglob('*') if p.is_file()],key=lambda p:p.relative_to(O).as_posix());entries=[]
for p in files:
 b=p.read_bytes();entries.append({'name':p.relative_to(O).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))})
count=len(entries)+2
write('owned-manifest.json',{'schema':1,'all_owned_files_except_this_manifest_and_final_lease':True,'entries':entries,'total_owned_files_including_this_and_final_lease':count,'negative_observers_preserved':True,'postclose_writes_permitted':False})
rb=json.loads((O/'foreground-readback.terminal.json').read_text());v=(O/'complete-RAW-verdict.json').read_bytes();rv=(O/'review-run.json').read_bytes()
lease={'schema':1,'status':'CLOSED_LAST','actor':'/root/independent_header_source68','owned_path':O.relative_to(R).as_posix(),'owned_file_count':count,'owned_manifest_RAW_sha256':sha((O/'owned-manifest.json').read_bytes()),'whole_logical_run_sha256':r['run_sha256'],'COMPLETE_RAW_VERDICT':{'name':'complete-RAW-verdict.json','RAW_bytes':len(v),'RAW_sha256':sha(v)},'COMPLETE_RAW_REVIEW':{'name':'review-run.json','RAW_bytes':len(rv),'RAW_sha256':sha(rv)},'actual_finalizer_pid':36256,'actual_finalizer_exit':0,'actual_readback_pid':rb['actual_pid'],'actual_readback_exit':rb['actual_exit'],'actual_lease_writer_pid':os.getpid(),'lease_writer_exit_authoritative_in_caller_tool_output':True,'last_owned_write':True,'postclose_writes_permitted':False,'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preproof_source_header_only':True,'compiled_truth_or_final_source_admission':False,'canonical_writes':False,'current67_finalsource_verdict_read':False}
write('lease.final.json',lease)
assert len([p for p in O.rglob('*') if p.is_file()])==count
print('SOURCE68_CLOSED_LAST_EXIT_0',os.getpid(),count,r['run_sha256'],sha(v),sha(rv),sha((O/'owned-manifest.json').read_bytes()),sha((O/'lease.final.json').read_bytes()))
