from pathlib import Path
import copy,hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');dest=r/'reader-status-overlay71';dest.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
before='Independent review, integration, full Exposition and PURIFIED remain pending.'
after='B21 alone establishes no full Exposition, PURIFIED, main/live, whole-paper or Goal completion.'
paths=[Path('website/content/publications/pbps-actual-corrector-change.json'),Path('website/content/declaration_lessons/pbps-actual-corrector-change.json'),Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json')]
old_item=load(paths[0])['items'][0];old_binding=pub.binding_digest(old_item,old_item['bindings'][0],pub.inputs());old_context=pub.review_context(old_item,old_item['bindings'][0],pub.inputs())
rows=[]
for i,p in enumerate(paths):
 b=p.read_bytes();x=load(p);y=copy.deepcopy(x)
 if i==0:
  fields=[y['items'][0]['bindings'][0],y['items'][0]['purification']];keys=['boundary','scope']
 elif i==1:fields=[y['units'][0]];keys=['boundary']
 else:fields=[y['purification']];keys=['scope']
 for d,k in zip(fields,keys):assert d[k].endswith(before);d[k]=d[k][:-len(before)]+after
 proposed=(json.dumps(y,ensure_ascii=False,indent=2)+'\n').encode();(dest/f'{i}.before.exactraw.json').write_bytes(b);(dest/f'{i}.proposed.json').write_bytes(proposed)
 rows.append(dict(path=p.as_posix(),before_RAW_sha256=sha(b),proposed_RAW_sha256=sha(proposed),changed_fields=['items.0.bindings.0.boundary','items.0.purification.scope'] if i==0 else ['units.0.boundary'] if i==1 else ['purification.scope']))
newdata=copy.copy(pub.inputs());newdata['lessons']=copy.copy(newdata['lessons']);item=load(dest/'0.proposed.json')['items'][0];lesson=load(dest/'1.proposed.json')['units'][0];newdata['lessons'][lesson['declaration']]=lesson
newbinding=pub.binding_digest(item,item['bindings'][0],newdata);newcontext=pub.review_context(item,item['bindings'][0],newdata)
assert newcontext==old_context and newbinding!=old_binding
q=dict(status='EXACT_READER_STATUS_SENTENCE_PROPOSAL_ONLY_NOT_APPLIED',actual_root_PID=os.getpid(),before=before,after=after,rows=rows,old_publication_binding_sha256=old_binding,proposed_publication_binding_sha256=newbinding,review_context_identical=True,canonical_writes=False,Lean_changed=False,statement_formula_proof_changed=False,new_premises=[],source_verdict=False,independent_overlay_review_required=True)
(dest/'proposal.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS exact4 status fields/3 proposed files only; mathematical review_context identical; canonical unchanged; independent overlay review pending.')
