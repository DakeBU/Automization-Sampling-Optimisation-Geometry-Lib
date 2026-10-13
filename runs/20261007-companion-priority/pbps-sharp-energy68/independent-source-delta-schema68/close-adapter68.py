from pathlib import Path
import json,hashlib,os,sys,datetime
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-sharp-energy68/independent-source-delta-schema68'
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();read=lambda n:json.loads((O/n).read_text(encoding='utf8'))
def write(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(n):
 b=(O/n).read_bytes();return {'path':n,'RAW_bytes':len(b),'RAW_sha256':sha(b)}
assert not (O/'lease.final.json').exists();r=read('review-run.json');assert sha(canon({k:v for k,v in r.items() if k!='run_sha256'}))==r['run_sha256'];d=read('complete-RAW-decision.json');assert d['review_run_sha256']==r['run_sha256'] and d['decision']=='APPROVED_EXACT_FINITE_SCHEMA_ADAPTER';t=read('review-adapter68.terminal.json');assert t['actual_exit_code']==0 and t['actual_child_pid']==d['actual_author_pid'];assert sha((O/'review-adapter68.stdout.RAW.txt').read_bytes())==t['stdout_raw_sha256'];assert sha((O/'review-adapter68.stderr.RAW.txt').read_bytes())==t['stderr_raw_sha256']
for e in read('complete-RAW-input-payload.json')['entries']:
 b=(O/e['raw_snapshot']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'];assert (R/e['source_path']).read_bytes()==b
rows=[]
for p in sorted(O.rglob('*')):
 if p.is_file():
  b=p.read_bytes();rows.append({'path':p.relative_to(O).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))})
write('owned-manifest.json',{'schema':1,'rows':rows,'listed_owned_files':len(rows),'total_owned_files_including_manifest_and_final_lease':len(rows)+2,'exclusions_exactly':['owned-manifest.json','lease.final.json'],'actual_manifest_pid':os.getpid()})
l={'schema':'independent-source-delta-schema68-CLOSED_LAST-v1','status':'CLOSED_LAST','actual_closing_pid':os.getpid(),'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'whole_logical_run_sha256':r['run_sha256'],'logical_rule':'Delete ONLY top-level run_sha256 from whole review-run.json then canonical sorted compact UTF8 SHA256','complete_named_RAW_review':pin('review-run.json'),'complete_named_RAW_decision':pin('complete-RAW-decision.json'),'complete_named_RAW_input_payload':pin('complete-RAW-input-payload.json'),'owned_manifest':pin('owned-manifest.json'),'total_owned_file_count_including_manifest_and_final_lease':len(rows)+2,'terminal_receipt':t,'proposal_RAW_sha256':d['proposal_RAW_sha256'],'decision':'APPROVED_EXACT_FINITE_SCHEMA_ADAPTER','native_CLOSED363_modified':False,'canonical_writes':False,'compiler_started':False,'full_Exposition_Seal':False,'PURIFIED':False,'full_paper_or_Goal_complete':False,'closing_terminal_authority':'Foreground tool authoritative exit after final write; post-close read-only validation.','last_owned_write':'lease.final.json'}
write('lease.final.json',l)
print('ADAPTER_CLOSED_LAST',len(rows)+2,'PID',os.getpid());print('LOGICAL_RUN',r['run_sha256']);print('LEASE_RAW',sha((O/'lease.final.json').read_bytes()));print('DECISION_RAW',l['complete_named_RAW_decision']['RAW_sha256']);print('INPUT_RAW',l['complete_named_RAW_input_payload']['RAW_sha256']);print('MANIFEST_RAW',l['owned_manifest']['RAW_sha256'])
