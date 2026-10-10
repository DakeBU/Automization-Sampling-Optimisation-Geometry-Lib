from pathlib import Path
import copy,hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-centered-root64';load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert load(r/'independent-source64/lease.final.json')['state']=='CLOSED_LAST'
slug='real-l2-positive-square-order';aid='ASTIS-RT-20261009-RealL2PositiveSquareOrder'
pp=root/'website/content/publications'/f'{slug}.json';lp=root/'website/content/declaration_lessons'/f'{slug}.json';ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json'
out=r/'auxiliary-metadata-overlay64';out.mkdir(exist_ok=False);maps=[]
for p in [pp,lp,ap]:
 sp=out/(p.parent.name+'-'+p.name+'.before.exactraw.snapshot');sp.write_bytes(p.read_bytes());maps.append(dict(original=pin(p),explicit_exact_raw_snapshot=pin(sp)))
code=[root/p for p in load(r/'claim.json')['proposed_files']];before=[pin(p) for p in code];old_packet=rt.decoder_packet(load(ap))
p=load(pp);lesson=load(lp);audit=load(ap);item=p['items'][0];unit=lesson['units'][0]
old_anchor='Appendix D1 positive-square-root monotonicity; ASTIS real-L2 corollary for printed B15'
new_anchor='Appendix D.1 bounded selfadjoint spectral calculus and unique nonnegative square root; ASTIS auxiliary real-L2 square-order corollary via Mathlib CFC monotonicity, consumed by B.15'
url='https://arxiv.org/html/2609.06905v1#A4.SS1'
assert item['source']['anchor']==unit['sources'][0]['label']==audit['source']['anchor']==old_anchor
item['source'].update(anchor=new_anchor,url=url,wording_status='faithful paraphrase',attribution='Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang provide Appendix D.1 spectral-calculus and unique nonnegative-root background. The displayed arbitrary-real-L2 square-order statement is an ASTIS auxiliary corollary using Mathlib CFC monotonicity and canonical complexification, not a separately printed D.1 theorem.')
unit['sources'][0].update(label=new_anchor,url=url)
unused=['ContinuousLinearMap.isUnit_of_forall_le_norm_inner_map','ContinuousLinearMap.opNorm_le_bound']
assert all(x in unit['mathlib_dependencies'] for x in unused)
unit['mathlib_dependencies']=[x for x in unit['mathlib_dependencies'] if x not in unused]
audit['source'].update(anchor=new_anchor,url=url,original_text=audit['source']['original_text'].replace('Source anchor: '+old_anchor,'Source anchor: '+new_anchor))
audit['source']['text_sha256']=hashlib.sha256(audit['source']['original_text'].encode()).hexdigest()
assert audit['state']=='blind-reconstructed'
write(pp,p);write(lp,lesson)
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();current=next(x for x in pub.load() if x['id']==slug)
audit['publication_binding_sha256']=pub.binding_digest(current,current['bindings'][0],data);audit['publication_context']=pub.review_context(current,current['bindings'][0],data)
assert rt.decoder_packet(audit)==old_packet;write(ap,audit)
assert before==[pin(p) for p in code]
packet=rt.semantic_reviewer_packet(audit);write(out/'fresh-reviewer-packet.json',packet)
write(out/'overlay.json',dict(status='AUXILIARY_ATTRIBUTION_AND_UNUSED_DEPENDENCIES_CORRECTED_INDEPENDENT_REVIEW_PENDING',actual_preparer_pid=os.getpid(),finite_historical_maps=maps,unused_dependencies_removed=unused,old_anchor=old_anchor,new_anchor=new_anchor,exact_D1_url=url,old_candidate_packet=pin(r/'source.0.reviewer-packet.json'),new_candidate_packet=pin(out/'fresh-reviewer-packet.json'),current=[pin(pp),pin(lp),pin(ap)],Lean_unchanged=before,source_statement_mathematical_repair=False,source_assumptions_changed=False,blind_decoder_packet_unchanged=True,formulae_and_12_proof_regions_unchanged=True,full_ExpositionSeal=False))
pub.check_advance(load(r/'publication-plan.json')['mathematical_declarations'],reviewed=False)
print('Corrected auxiliary D1 attribution and removed two unused dependencies; same statement/code/decoder/12 excerpts; independent overlay admission pending.')
