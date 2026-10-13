from pathlib import Path
import json,hashlib,os,sys,traceback
ROOT=Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72';OWN=RUN/'independent-source72'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def diff(a,b,path=''):
 if type(a)!=type(b):return [{'path':path,'before':a,'after':b}]
 if isinstance(a,dict):
  assert set(a)==set(b);return [r for k in a for r in diff(a[k],b[k],path+'/'+k)]
 if isinstance(a,list):
  assert len(a)==len(b);return [r for i,(x,y) in enumerate(zip(a,b)) for r in diff(x,y,path+'/'+str(i))]
 return [] if a==b else [{'path':path,'before':a,'after':b}]
def left(s,x,path=''):
 if isinstance(x,dict):return [r for k,v in x.items() for r in left(s,v,path+'/'+k)]
 if isinstance(x,list):return [r for i,v in enumerate(x) for r in left(s,v,path+'/'+str(i))]
 return [path] if isinstance(x,str) and s in x else []
def write(n,x): (OWN/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
code=0
try:
 path=RUN/'reader-status-overlay72.v3/proposal.json';p=json.loads(path.read_text(encoding='utf-8'))
 rows=[];remaining=[];inputpins=[]
 for r in p['rows']:
  a=(ROOT/r['before']).read_bytes();b=(ROOT/r['proposed']).read_bytes()
  assert sha(a)==r['before_RAW_sha256'] and sha(b)==r['proposed_RAW_sha256'];assert (ROOT/r['path']).read_bytes()==a
  ds=diff(json.loads(a),json.loads(b))
  for d in ds:assert d['after']==d['before'].replace(p['before'],p['after'])
  residual=left(p['before'],json.loads(b));remaining.extend({'file':r['path'],'pointer':z} for z in residual)
  rows.append({'path':r['path'],'before_RAW_sha256':sha(a),'approved_proposed_RAW_sha256':sha(b),'changes':ds,'remaining_old_status':residual})
  for f in [r['before'],r['proposed']]:
   bb=(ROOT/f).read_bytes();inputpins.append({'path':f,'raw_bytes':len(bb),'raw_sha256':sha(bb),'lf_sha256':sha(bb.replace(b'\r\n',b'\n'))})
 maps=[]
 for n,r in enumerate(p['bindings']):
  a=json.loads((RUN/f'source-review.packet.{n}.json').read_text(encoding='utf-8'));qpath=ROOT/r['proposed_packet'];b=json.loads(qpath.read_text(encoding='utf-8'))
  ds=diff(a,b);expected={'/publication_binding_sha256','/packet_sha256','/candidate_publication_context/lesson/sources/0/scope','/candidate_publication_context/candidate_assumptions/1/lean'}
  assert {d['path'] for d in ds}==expected
  for d in ds:
   if d['path'].startswith('/candidate_'):assert d['after']==d['before'].replace(p['before'],p['after'])
  logical=dict(b);logical.pop('packet_sha256');assert sha(canon(logical))==b['packet_sha256']==r['proposed_packet_sha256']
  assert a['lean']==b['lean'] and a['blind_reconstruction']==b['blind_reconstruction'] and a['source']==b['source']
  ap=RUN/f'reader-status-overlay72.v3/audit.{n}.proposed.json'; ab=RUN/f'reader-status-overlay72.v3/audit.{n}.before.exactraw.json'
  ad=diff(json.loads(ab.read_bytes()),json.loads(ap.read_bytes()))
  assert {x['path'] for x in ad}=={'/publication_binding_sha256','/publication_context/lesson/sources/0/scope','/publication_context/candidate_assumptions/1/lean'}
  for x in ad:
   if x['path']!='/publication_binding_sha256':assert x['after']==x['before'].replace(p['before'],p['after'])
  for f in [ap,ab]:
   bb=f.read_bytes();inputpins.append({'path':f.relative_to(ROOT).as_posix(),'raw_bytes':len(bb),'raw_sha256':sha(bb),'lf_sha256':sha(bb.replace(b'\r\n',b'\n'))})
  maps.append({'unit':n,'approved_packet_raw_sha256':sha(qpath.read_bytes()),'approved_packet_sha256':b['packet_sha256'],'approved_publication_binding_sha256':b['publication_binding_sha256'],'exact_diff_pointers':[d['path'] for d in ds],'mathematical_context_equal':True,'whole_review_context_equal':False})
  inputpins.append({'path':qpath.relative_to(ROOT).as_posix(),'raw_bytes':qpath.stat().st_size,'raw_sha256':sha(qpath.read_bytes()),'lf_sha256':sha(qpath.read_bytes().replace(b'\r\n',b'\n'))})
 count=sum(len(r['changes']) for r in rows)
 assert count==16 and not remaining
 print(json.dumps({'changed_fields':count,'remaining':remaining},indent=2))
 # The candidate cells also quote the old boundary in their assumptions ledger.
 # These are evaluated transparently below instead of assuming the root's count.
 decision={'schema':'source72-reader-status-overlay-v3-specific-decision-v1','proposal_RAW_sha256':sha(path.read_bytes()),'decision':'accept-exact-proposed-metadata-overlay' if count==16 and not remaining else 'needs-revision','sixteen_field_claim_checked':count,'rows':rows,'remaining_old_status_occurrences':remaining,'packet_mapping':maps,'review_context_change':'Exactly lesson.sources[0].scope and candidate_assumptions[1].lean; both are the same status-only suffix replacement. Context hash changes are acknowledged.','math_Lean_BODY_formulas_assumptions_decoder_unchanged':True,'independent_source_verdict_now':False,'canonical_writes':False,'actual_pid':os.getpid(),'superseded_versions':'Unapplied incomplete v1 and v2 status proposals retained; their observer diagnostics are historical negative evidence. v3 independently enumerates all residual paths and requires zero.'}
 write('reader-status-overlay72.v3.independent-decision.json',decision);write('reader-status-overlay72.v3.input-pins.json',{'proposal':{'path':path.relative_to(ROOT).as_posix(),'raw_sha256':sha(path.read_bytes())},'inputs':inputpins})
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'decision':decision['decision'],'decision_RAW_sha256':sha((OWN/'reader-status-overlay72.v3.independent-decision.json').read_bytes()),'packet_mapping':maps},indent=2))
except BaseException:code=1;traceback.print_exc()
finally:write('reader-status-overlay72.v3.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False})
sys.exit(code)
