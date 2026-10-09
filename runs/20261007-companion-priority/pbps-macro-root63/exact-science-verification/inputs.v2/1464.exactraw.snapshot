from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,str(Path('tools').resolve()));import astis_semantic_roundtrip as rt,astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-macro-root63');slug='pbps-unique-positive-macroscopic-defect-root';aid='ASTIS-RT-20261009-PBPSUniquePositiveMacroscopicDefectRoot'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def w(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.resolve().as_posix(),raw_bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
assert load(r/'root.math63.adoption.json')['status']=='INDEPENDENT_PRECOMMIT_SCOPED_MATHEMATICS63_ACCEPTED_WITH_EXACT_EXCERPT_BLOCKER'
assert load(r/'root.decoder63.adoption.json')['status']=='ACTUAL_CLOSED_FRESH_ANONYMOUS_DECODER63_ADOPTED'
issue=load(r/'independent-math63/publication-step3.binding.issue-and-proposal.json');proposal=issue['minimal_proposed_repair']
main=Path(proposal['path']);raw=main.read_bytes();s=raw.decode();body=s.index(':= by\n',s.index('theorem actual_unique_positive_macroscopic_defect_root'))+len(':= by\n')
a=s.index('  let A :',body);b=s.index('  have hPB',a);code=s[a:b];assert code.endswith('\n')
row=dict(path=proposal['path'],source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode()))
assert row['start_line']==120 and row['end_line']==146 and all(row[k]==proposal[k] for k in row) and code==proposal['lean']
assert b''.join(raw.splitlines(keepends=True)[119:146])==code.encode()
draftp=r/'exposition.draft.json';manifestp=r/'exact-step-code63.manifest.json';lessonp=Path('website/content/declaration_lessons')/(slug+'.json');pubp=Path('website/content/publications')/(slug+'.json');auditp=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');cellp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-unique-macroscopic-defect-root.json')
draft=load(draftp);manifest=load(manifestp);lesson=load(lessonp);audit=load(auditp);assert audit['state']=='blind-reconstructed'
assert draft['units'][0]['steps'][2]['lean']==lesson['units'][0]['steps'][2]['lean'];assert sha(draft['units'][0]['steps'][2]['lean'].encode())==issue['advertised_digest']
out=r/'presentation-step3-repair63';out.mkdir(exist_ok=False);maps=[]
for i,p in enumerate([r/'math-freeze.json',draftp,manifestp,lessonp,pubp,auditp,r/'frozen-cell0.json',cellp]):
 target=out/(f'{i:02d}-'+p.parent.name+'-'+p.name+'.before.exactraw.snapshot');target.write_bytes(p.read_bytes());maps.append(dict(original=pin(p),exact_raw_snapshot=pin(target)))
for x in [draft['units'][0]['steps'][2],lesson['units'][0]['steps'][2]]:x['lean']=code;x['lean_source_region']=row
manifest['regions'][2]=row
replace(draftp,draft);replace(lessonp,lesson);replace(manifestp,manifest)
assert main.read_bytes()==raw
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']==slug);binding=item['bindings'][0]
audit['publication_binding_sha256']=pub.binding_digest(item,binding,data);audit['publication_context']=pub.review_context(item,binding,data);replace(auditp,audit)
assert rt.decoder_packet(audit)==load(r/'anonymous.0.decoder.json')
sourcepacket=rt.semantic_reviewer_packet(audit);w(r/'source.0.reviewer-packet.json',sourcepacket)
historical=[]
# Include the preceding DRAFT audit before native decoder adoption as a qualified
# source-read history, never as a replacement for a current semantic review.
oldaudit=r/'audit.0.before-decoder.raw.snapshot.json'
for q in load(r/'independent-math63/input.manifest.json')['qualified_raw_LF_pairs']:
 original=q['original'];p=Path(original['path']);now=pin(p)
 if now['raw_sha256']!=original['raw_sha256']:
  candidates=[x for x in maps if x['original']['path']==p.resolve().as_posix() and x['original']['raw_sha256']==original['raw_sha256']]
  if p.resolve()==auditp.resolve() and sha(oldaudit.read_bytes())==original['raw_sha256']:snapshot=pin(oldaudit)
  else:assert len(candidates)==1,(p,original['raw_sha256']);snapshot=candidates[0]['exact_raw_snapshot']
  assert snapshot['raw_sha256']==original['raw_sha256'] and snapshot['lf_sha256']==original['lf_sha256'] and snapshot['raw_bytes']==original['bytes'];historical.append(dict(original=original,exact_raw_snapshot=snapshot))
for step in draft['units'][0]['steps']:
 q=step['lean_source_region'];bb=Path(q['path']).read_bytes();exact=b''.join(bb.splitlines(keepends=True)[q['start_line']-1:q['end_line']]);assert exact==step['lean'].encode() and sha(exact)==q['exact_code_raw_sha256'] and sha(bb)==q['source_raw_sha256']
current_inputs=[pin(q['path']) for q in load(r/'math-freeze.json')['inputs']]
w(r/'math-freeze.presentation-supplement-v2.json',dict(schema_version=1,status='EXACT_EXCERPT_FIXED_INDEPENDENT_PRESENTATION_REVIEW_PENDING',original_immutable_math_freeze=pin(r/'math-freeze.json'),original_independent_math_run=pin(r/'independent-math63/run.json'),current30=current_inputs,qualified_original58_history=historical,original_source_statement_and_proof_unchanged=True,only_step3_excerpt_changed=True,current_source_packet=pin(r/'source.0.reviewer-packet.json'),canonical_publication_context_sha256=audit['publication_binding_sha256'],no_exposition_seal=True))
w(out/'root.presentation-repair63.json',dict(actual_writer_pid=os.getpid(),classification='exact-multiline-excerpt-binding-only',issue=issue,adopted_region=row,all_eight_literal_snippets_match=True,raw_snapshot_mappings=maps,qualified_original58_history=historical,independent_review_pending=True,statement_or_mathematical_proof_repair=False,Lean_source_unchanged=pin(main)))
pub.check_advance([load(r/'claim.json')['target_declarations'][0]],reviewed=False)
print('PASS only step3 exact excerpt repaired to120-146; all8 literal spans match; original mathfreeze/run unchanged; independent source/presentation review pending.')
