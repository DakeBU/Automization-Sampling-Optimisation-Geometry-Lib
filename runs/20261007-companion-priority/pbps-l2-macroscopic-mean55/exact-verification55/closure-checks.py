from common import *
prior=load(O/'native-input-checks.json');mappings={}
for row in prior['exact_historical_mappings']:
 e=row['expected'];mappings[(str(path(e['path'])),e['raw_sha256'],e['lf_sha256'])]=row['actual']['path']
checks=[];unresolved=[]
def walk(d,context):
 if isinstance(d,dict):
  if all(k in d for k in ['path','raw_sha256','lf_sha256']):
   if equal(d):checks.append(dict(context=context,expected=d,actual=pin(d['path'])));
   else:
    m=mappings.get((str(path(d['path'])),d['raw_sha256'],d['lf_sha256']))
    if m and equal(d,m):checks.append(dict(context=context,expected=d,actual=pin(m),original_to_snapshot=True))
    else:unresolved.append(dict(context=context,expected=d,current=pin(d['path'])))
  for k,v in d.items():walk(v,context+'/'+k)
 elif isinstance(d,list):
  for i,v in enumerate(d):walk(v,context+'/'+str(i))
files=['whole-math55/lease.json','reviewer.source.lease.json','source.review.lease.json','independent-review55/reviewer.source.repair.lease.json','source-metadata-repair55/source.repair.review.lease.json','root.whole-math55.adoption.json']
for p in files:walk(load(B/p),p)
selfs=[selfcheck(B/'source.review.lease.json','lease_run_sha256')]
whole=load(B/'whole-math55/checks.json')
for e in whole['preproof_complete_native_runs']:
 p=e['input']['path'];assert equal(e['input']);selfs.append(selfcheck(p))
assert not unresolved,unresolved
dump('closure-checks.json',dict(status='PASS',native_closure_actual_pins=checks,full_named_self_recipes=selfs,unresolved=unresolved))
dump('own-negatives.json',dict(status='PRESERVED_OWN_CHECKER_DIAGNOSIS_ONLY',compiler_invocations=1,proof_or_source_issue=False,negatives=[dict(stage='preflight0',error='Overbroad guard matched a numbered fragment within allowed55; narrowed to actual future packet directory components.',snapshot=pin(O/'common.0.guard-negative.raw.snapshot.py')),dict(stage='preflight1',error='Git raw incorrectly compared to current LF; actual Git production bytes equal current raw14107/248CRLF. Corrected comparison to Git LF vs current LF; both hashes retained, no fabricated digest.'),dict(stage='gates0',error='Own assumption item key lean caused KeyError; actual publication schema uses bindings. Read actual schema and preserved failed script.',snapshot=pin(O/'gates.0.schema-negative.raw.snapshot.py'))],no_repeat_Lean_build=True))
print(json.dumps(dict(status='PASS',native_closure_pins=len(checks),additional_full_self_recipes=len(selfs))))
