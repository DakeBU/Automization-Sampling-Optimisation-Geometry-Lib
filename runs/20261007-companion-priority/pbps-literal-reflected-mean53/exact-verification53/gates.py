import verify as v
import sys,os,json,subprocess,re
sys.path.insert(0,str(v.R));sys.path.insert(0,str(v.R/'tools'))
from tools import astis_publication as pub,astis_advance as advance,astis
print('actual_python_pid='+str(os.getpid()),flush=True)
pub.check_advance([v.TARGET],reviewed=True)
item=next(i for i in pub.load() if any(b['declaration']==v.TARGET for b in i['bindings']));binding=next(b for b in item['bindings'] if b['declaration']==v.TARGET)
digest=pub.binding_digest(item,binding)
assert digest==v.load(v.AUDIT)['publication_binding_sha256']==v.load(v.B/'source.0.review.json')['publication_binding_sha256']==v.load(v.B/'source.0.reviewer-packet.json')['publication_binding_sha256']
payload=pub.binding_payload(item,binding);packet=v.load(v.B/'source.0.reviewer-packet.json')
assert pub.review_context(item,binding)==packet['candidate_publication_context'] and v.logical(payload)==digest
v.dump('publication-binding.actual.json',dict(status='PASS',declaration=v.TARGET,digest=digest,actual_complete_payload=payload,recipe='canonical binding_payload; sorted compact UTF8 ensure_ascii=False SHA256; file/source/statement/formulae/assumptions/obligations/lesson/exact binding all included, not projected review_context',real_check_advance_reviewed=True,python_pid=os.getpid()))
scan=[]
for row in v.load(v.B/'whole-proof-review53/checks.json')['fake_closure_scan']:
 p=row['input']['path'];assert v.equal(row['input']);code=astis.strip_lean_comments_and_strings(v.path(p).read_text());hits=[dict(line=n,text=l) for n,l in enumerate(code.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits
 scan.append(dict(input=v.pin(p),forbidden_hits=hits))
state=advance.current_advances();s=state[v.ADV];assert s['state']=='PROVED_LOCAL' and s['owner_id']!='whole_math52';lane=[i for i,d in state.items() if d.get('state')=='STABILIZING'];assert lane==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
v.dump('gate.checks.json',dict(status='PASS',actual_python_pid=os.getpid(),check_advance_reviewed=True,publication_binding_sha256=digest,fake_closure_scan=scan,source_audit=v.AUDIT,source_verdict=v.load(v.AUDIT)['verdict'],state_before=s['state'],owner_id=s['owner_id'],sole_STABILIZING=lane,scope='Focused Lean/source/publication and complete consumed-body fake closure gate. Full shared repository aggregate required later in the original serialized lane.'))
print(json.dumps(dict(status='PASS',publication_binding_sha256=digest,fake_closure_sources=len(scan),state=s['state'],sole_STABILIZING=lane)),flush=True)
