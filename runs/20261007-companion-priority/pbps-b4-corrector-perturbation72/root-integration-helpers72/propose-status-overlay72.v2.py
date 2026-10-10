from pathlib import Path
import copy,hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');o=r/'reader-status-overlay72.v2';o.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
plan=load(r/'publication-plan.json');rows=[];bindings=[]
before='Independent review, integration, Exposition Seal, PURIFIED, main/live and whole-Goal completion remain pending.'
after='The perturbation identity alone establishes no Exposition Seal, PURIFIED, main/live, whole-paper or Goal completion; independent review and serialized integration are separate admissions.'
for i,(slug,aid,cid) in enumerate(zip(plan['slugs'],plan['audit_ids'],plan['active_cells'])):
 paths=[Path('website/content/publications')/(slug+'.json'),Path('website/content/declaration_lessons')/(slug+'.json'),Path('research-wiki/frontier-cells')/(cid+'.json')]
 olditem=load(paths[0])['items'][0];oldcontext=pub.review_context(olditem,olditem['bindings'][0],pub.inputs());oldbinding=pub.binding_digest(olditem,olditem['bindings'][0],pub.inputs())
 for j,p in enumerate(paths):
  x=load(p);y=copy.deepcopy(x)
  fields=[(y['items'][0]['bindings'][0],'boundary'),(y['items'][0]['purification'],'scope'),(y['items'][0]['bindings'][0]['assumption_deltas'][1],'lean')] if j==0 else [(y['units'][0],'boundary'),(y['units'][0]['sources'][0],'scope')] if j==1 else [(y['purification'],'scope')]
  for d,k in fields:assert d[k].endswith(before);d[k]=d[k][:-len(before)]+after
  b=p.read_bytes();(o/f'{i}.{j}.before.exactraw.json').write_bytes(b);new(o/f'{i}.{j}.proposed.json',y)
  rows.append(dict(path=p.as_posix(),before_RAW_sha256=sha(b),proposed_RAW_sha256=sha((o/f'{i}.{j}.proposed.json').read_bytes()),before=(o/f'{i}.{j}.before.exactraw.json').as_posix(),proposed=(o/f'{i}.{j}.proposed.json').as_posix(),only_exact_boundary_status_suffix_changed=True))
 data=copy.copy(pub.inputs());data['lessons']=copy.copy(data['lessons'])
 item=load(o/f'{i}.0.proposed.json')['items'][0];lesson=load(o/f'{i}.1.proposed.json')['units'][0];data['lessons'][lesson['declaration']]=lesson
 newbinding=pub.binding_digest(item,item['bindings'][0],data);newcontext=pub.review_context(item,item['bindings'][0],data)
 beforecontext=copy.deepcopy(oldcontext);aftercontext=copy.deepcopy(newcontext)
 for context in [beforecontext,aftercontext]:
  context['lesson']['sources'][0]['scope']='STATUS_SUFFIX_PROPOSAL'
  context['candidate_assumptions'][1]['lean']='STATUS_SUFFIX_PROPOSAL'
 assert beforecontext==aftercontext and newbinding!=oldbinding
 ap=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');audit=load(ap);assert audit['state']=='blind-reconstructed' and audit['publication_binding_sha256']==oldbinding
 (o/f'audit.{i}.before.exactraw.json').write_bytes(ap.read_bytes());proposed=copy.deepcopy(audit);proposed['publication_binding_sha256']=newbinding;proposed['publication_context']=newcontext
 oldpacket=rt.semantic_reviewer_packet(audit);assert oldpacket==load(r/f'source-review.packet.{i}.json')
 packet=rt.semantic_reviewer_packet(proposed);allowed={'publication_binding_sha256','packet_sha256','candidate_publication_context'}
 assert {k:v for k,v in packet.items() if k not in allowed}=={k:v for k,v in oldpacket.items() if k not in allowed}
 new(o/f'audit.{i}.proposed.json',proposed);new(o/f'source-review.packet.{i+2}.proposed.json',packet)
 bindings.append(dict(audit_path=ap.as_posix(),old_binding=oldbinding,proposed_binding=newbinding,old_packet_sha256=oldpacket['packet_sha256'],proposed_packet_sha256=packet['packet_sha256'],proposed_packet=(o/f'source-review.packet.{i+2}.proposed.json').as_posix(),mathematical_statement_formula_proof_identical=True,review_context_changed_only=['lesson.sources.0.scope','candidate_assumptions.1.lean'],packet_changed_fields=sorted(allowed)))
new(o/'proposal.json',dict(status='PROPOSAL_ONLY_NOT_APPLIED_REQUIRES_INDEPENDENT_REVIEW',supersedes_underapplied_v1_proposal='reader-status-overlay72/proposal.json',actual_root_PID=os.getpid(),before=before,after=after,rows=rows,bindings=bindings,status_fields=12,files=6,Lean_changed=False,statement_formula_proof_changed=False,new_decoder_needed=False,canonical_writes=False))
print('PASS proposal72v2:12 status fields in6 exact files; explicit two status-context paths/unit and two derived digests. No canonical/Lean/math/decoder changes.')
