from pathlib import Path
import json,hashlib,os,sys,datetime
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-sharp-energy68/independent-energy-alias-overlay68'
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();read=lambda n:json.loads((O/n).read_text(encoding='utf8'))
def write(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(n):
 b=(O/n).read_bytes();return {'path':n,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))}
assert not (O/'lease.final.json').exists();r=read('review-run.json');d=read('complete-RAW-decision.json');assert sha(canon({k:v for k,v in r.items() if k!='run_sha256'}))==r['run_sha256']==d['review_run_sha256'];rep=read('final-readback.json');assert rep['status'].endswith('_PASS')
term={}
for prefix in ['review-energy-alias68','final-readback68']:
 t=read(prefix+'.terminal.json');assert t['foreground'] and not t['detached'] and t['actual_exit_code']==0;assert sha((O/(prefix+'.stdout.RAW.txt')).read_bytes())==t['stdout_raw_sha256'];assert sha((O/(prefix+'.stderr.RAW.txt')).read_bytes())==t['stderr_raw_sha256'];term[prefix]=t
assert term['review-energy-alias68']['actual_child_pid']==d['actual_author_pid'];assert term['final-readback68']['actual_child_pid']==rep['actual_pid']
rows=[]
for p in sorted(O.rglob('*')):
 if p.is_file():
  b=p.read_bytes();rows.append({'path':p.relative_to(O).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))})
write('owned-manifest.json',{'schema':1,'rows':rows,'listed_owned_files':len(rows),'total_owned_files_including_manifest_and_final_lease':len(rows)+2,'exclusions_exactly':['owned-manifest.json','lease.final.json'],'actual_manifest_pid':os.getpid()})
for e in rows:
 b=(O/e['path']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256']
l={'schema':'independent-energy-alias-overlay68-CLOSED_LAST-v1','status':'CLOSED_LAST','actual_closing_pid':os.getpid(),'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'whole_logical_run_sha256':r['run_sha256'],'logical_rule':'Delete ONLY top-level run_sha256 from whole review-run.json, then canonical sorted compact UTF8 SHA256.','complete_named_RAW_review':pin('review-run.json'),'complete_named_RAW_decision':pin('complete-RAW-decision.json'),'complete_named_RAW_input_payload':pin('complete-RAW-input-payload.json'),'owned_manifest':pin('owned-manifest.json'),'rows_canonical_sha256':sha(canon(rows)),'total_owned_file_count_including_manifest_and_final_lease':len(rows)+2,'actual_terminal_receipts':term,'final_readback':pin('final-readback.json'),'proposal_RAW_sha256':d['proposal_RAW_sha256'],'new_reviewer_packet_sha256':d['reviewer_packet_sha256'],'new_reviewer_packet_RAW_sha256':d['reviewer_packet_RAW_sha256'],'new_binding_sha256':d['publication_binding_sha256'],'new_context_canonical_sha256':d['candidate_context_canonical_sha256'],'native_source_run_sha256':d['native_source_run_sha256'],'native_source_lease_RAW_sha256':d['native_source_lease_RAW_sha256'],'decision':'APPROVED_EXACT_ALIAS_PREFIX_AND_REFRESHED_PACKET_BINDING_CONTEXT','source_review_refresh_provenance':d['source_review_refresh_provenance'],'canonical_writes':False,'native_CLOSED363_and_CLOSED24_modified':False,'compiler_started':False,'proof_search':False,'source_mathematical_repair':False,'specified_aliases_only':True,'full_Exposition_Seal':False,'PURIFIED':False,'full_paper_or_Goal_complete':False,'closing_terminal_authority':'Foreground tool exit after last owned write; subsequent verifier read-only.','last_owned_write':'lease.final.json'}
write('lease.final.json',l)
print('ENERGY_ALIAS_CLOSED_LAST',len(rows)+2,'PID',os.getpid());print('LOGICAL_RUN',r['run_sha256']);print('LEASE_RAW',sha((O/'lease.final.json').read_bytes()));print('RAW_REVIEW',l['complete_named_RAW_review']['RAW_sha256']);print('RAW_DECISION',l['complete_named_RAW_decision']['RAW_sha256']);print('RAW_INPUT',l['complete_named_RAW_input_payload']['RAW_sha256']);print('MANIFEST_RAW',l['owned_manifest']['RAW_sha256'])
