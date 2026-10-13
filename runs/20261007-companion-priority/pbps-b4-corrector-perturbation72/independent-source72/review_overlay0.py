from pathlib import Path
import json,hashlib,os,sys,traceback
ROOT=Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72';OWN=RUN/'independent-source72'
def sha(b):return hashlib.sha256(b).hexdigest()
def diff(a,b,path=''):
 if type(a)!=type(b):return [{'path':path,'before':a,'after':b}]
 if isinstance(a,dict):
  assert set(a)==set(b)
  return [r for k in a for r in diff(a[k],b[k],path+'/'+k)]
 if isinstance(a,list):
  assert len(a)==len(b)
  return [r for i,(x,y) in enumerate(zip(a,b)) for r in diff(x,y,path+'/'+str(i))]
 return [] if a==b else [{'path':path,'before':a,'after':b}]
def paths_of(s,x,path=''):
 if isinstance(x,dict):return [r for k,v in x.items() for r in paths_of(s,v,path+'/'+k)]
 if isinstance(x,list):return [r for i,v in enumerate(x) for r in paths_of(s,v,path+'/'+str(i))]
 return [path] if isinstance(x,str) and s in x else []
def write(n,x): (OWN/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
code=0
try:
 path=RUN/'reader-status-overlay72/proposal.json';proposal=json.loads(path.read_text(encoding='utf-8'))
 rows=[];remaining=[]
 for row in proposal['rows']:
  before=(ROOT/row['before']).read_bytes();after=(ROOT/row['proposed']).read_bytes()
  assert sha(before)==row['before_RAW_sha256'] and sha(after)==row['proposed_RAW_sha256']
  assert (ROOT/row['path']).read_bytes()==before
  changes=diff(json.loads(before),json.loads(after))
  for c in changes:assert c['after']==c['before'].replace(proposal['before'],proposal['after'])
  left=paths_of(proposal['before'],json.loads(after))
  rows.append({'path':row['path'],'before_RAW_sha256':sha(before),'proposed_RAW_sha256':sha(after),'changes':changes,'remaining_same_suffix_paths':left})
  remaining.extend({'path':row['path'],'pointer':p} for p in left)
 packetmaps=[]
 for n,row in enumerate(proposal['bindings']):
  old=json.loads((RUN/f'source-review.packet.{n}.json').read_text(encoding='utf-8'));new=json.loads((ROOT/row['proposed_packet']).read_text(encoding='utf-8'))
  ds=diff(old,new);assert {d['path'] for d in ds}=={'/publication_binding_sha256','/packet_sha256'}
  assert old['candidate_publication_context']==new['candidate_publication_context']
  q=dict(new);q.pop('packet_sha256');assert sha(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==new['packet_sha256']
  packetmaps.append({'unit':n,'changes':ds,'context_identical':True,'proposed_packet_RAW_sha256':sha((ROOT/row['proposed_packet']).read_bytes())})
 assert len(remaining)==4 and sum(len(r['changes']) for r in rows)==8
 decision={'schema':'source72-reader-status-overlay-specific-decision-v1','proposal_RAW_sha256':sha(path.read_bytes()),'decision':'needs-revision-for-exhaustive-reader-status-update','eight_exact_replacements_individually_appropriate':True,'mathematical_repair':False,'canonical_writes':False,'remaining_exact_status_suffix_paths':remaining,'required_change':'Apply the same exact suffix substitution at these four additional pointers. Revised packet context will differ in lesson.sources[0].scope and candidate_assumptions[1].lean; new packet/context pins must record it honestly. No Lean/formula/BODY/assumption mathematics or decoder change is required.','rows':rows,'packet_mapping':packetmaps,'final_source_verdict':False,'actual_pid':os.getpid()}
 write('reader-status-overlay72.proposal0.independent-decision.json',decision)
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'decision_RAW_sha256':sha((OWN/'reader-status-overlay72.proposal0.independent-decision.json').read_bytes()),'eight_changes_checked':8,'remaining':remaining},indent=2))
except BaseException:code=1;traceback.print_exc()
finally:write('reader-status-overlay72.proposal0.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False})
sys.exit(code)
