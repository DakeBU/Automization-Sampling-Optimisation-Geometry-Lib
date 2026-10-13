from pathlib import Path
import json,hashlib,copy,sys,os
sys.path.insert(0,str(Path('tools').resolve()));import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-macro-root63');n=r/'independent-source63';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def w(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
s=load(n/'run.json');l=load(n/'lease.json');receipt=load(n/'native.receipt.json');q=load(n/'review.payload.json');term=load(n/'terminal.readback.json')
assert l['status']=='CLOSED_LAST' and (n/'lease.json').read_bytes()==(n/'proposed-lease.closed.json').read_bytes()
assert sha(can({k:v for k,v in s.items() if k!='run_sha256'}))==s['run_sha256']==l['whole_run_sha256']==receipt['whole_run_sha256']=='32b39c9148d59120ba67a632e836ea203a7d8c8477703c27a9c774886857b2e5'
assert sha((n/'review.payload.json').read_bytes())==s['complete_review_payload_RAW_sha256']==l['named_complete_payload_RAW_sha256']==receipt['named_complete_payload_RAW_sha256']=='ab7dea212533a86af87d609044db50c7ef14366cce652963aa262c2936fa2a01'
assert s['full_semantic_review']==q and term['observed_finalizer_exit_code']==term['actual_reader_exit_code']==0 and term['all_bindings_passed']
assert term['native_receipt_RAW_sha256']==sha((n/'native.receipt.json').read_bytes())
for maps in [s['artifacts_before_finalization'],load(n/'output.manifest.json')['owned_outputs'],l['complete_owned_outputs']]:
 for path,digest in maps.items():assert sha((n/path).read_bytes())==digest,path
actual={p.relative_to(n).as_posix() for p in n.rglob('*') if p.is_file()};assert len(actual)==122 and actual==set(l['complete_owned_outputs'])|{'lease.json','proposed-lease.closed.json'}
assert s['source_first_seal_receipt']['actual_foreground_preread_complete'] and s['source_first_seal_receipt']['all24_literal_regions_read']
assert not any(s['source_first_seal_receipt'][k] for k in ['candidate_seen','decoder_seen','prior_verdict_seen'])
primary=Path('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)==s['source_primary_RAW_sha256']
for row in s['source_primary_regions']:
 lo,hi=row['byte_range'];b=Path(row['raw_path']).read_bytes();assert primary[lo:hi]==b and sha(b)==row['raw_sha256'] and Path(row['lf_path']).read_bytes()==b.replace(b'\r\n',b'\n') and sha(Path(row['lf_path']).read_bytes())==row['lf_sha256']
for row in s['candidate_input_manifest']:
 b=Path(row['origin']).read_bytes();assert b==Path(row['raw_snapshot']).read_bytes() and sha(b)==row['raw_sha256'] and len(b)==row['bytes'];z=b.replace(b'\r\n',b'\n');assert Path(row['lf_snapshot']).read_bytes()==z and sha(z)==row['lf_sha256']
history={}
for row in load(r/'math-freeze.presentation-supplement-v2.json')['qualified_original58_history']:
 original=row['original'];snapshot=row['exact_raw_snapshot'];b=Path(snapshot['path']).read_bytes();assert sha(b)==original['raw_sha256']==snapshot['raw_sha256'];history[(str(Path(original['path']).resolve()),original['raw_sha256'])]=Path(snapshot['path'])
seen=set();resolutions=[]
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256'}<=x.keys():
   p=Path(x['path']);span='start_line' in x and 'end_line' in x;k=(str(p.resolve()),x.get('start_line'),x.get('end_line'),x['raw_sha256'],x.get('lf_sha256'))
   if k not in seen:
    effective=history.get((str(p.resolve()),x['raw_sha256']),p);whole=effective.read_bytes();b=b''.join(whole.splitlines(keepends=True)[x['start_line']-1:x['end_line']]) if span else whole;assert sha(b)==x['raw_sha256'],(p,'literal-span' if span else 'whole-file')
    if 'lf_sha256' in x:assert sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256'],p
    for key,length in [('bytes',len(b)),('raw_bytes',len(b)),('lf_bytes',len(b.replace(b'\r\n',b'\n')))]:
     if key in x:assert x[key]==length,p
    seen.add(k)
    if effective!=p:resolutions.append(dict(original=x,exact_snapshot=effective.as_posix()))
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for p in n.rglob('*.json'):walk(load(p))
assert load(r/'root.math63.adoption.json')['status']=='INDEPENDENT_PRECOMMIT_SCOPED_MATHEMATICS63_ACCEPTED_WITH_EXACT_EXCERPT_BLOCKER'
assert load(r/'root.decoder63.adoption.json')['status']=='ACTUAL_CLOSED_FRESH_ANONYMOUS_DECODER63_ADOPTED'
assert q['verdict']=='equivalent-after-elaboration' and set(q['semantic_slots'])==set(rt.SEMANTIC_SLOTS) and not q['repairs'] and not q['source_assumption_repair'] and q['binder_audit']['EXCESS_count']==0
assert q['independent_from_formalizer'] and q['independent_from_decoder'] and all(not x['blocking'] for x in q['deltas'])
assert len(q['source_proof_coverage']['regions'])==24 and q['presentation_review']['verdict']=='accepted-exact-multiline-excerpt-binding-only' and not q['presentation_review']['full_rendered_Exposition_Seal_granted']
for row in q['presentation_review']['eight_spans']:
 b=Path(row['path']).read_bytes();span=b''.join(b.splitlines(keepends=True)[row['start_line']-1:row['end_line']]);assert row['literal_match'] and sha(span)==row['raw_sha256']
assert len(q['presentation_review']['eight_spans'])==8 and q['binding_checks']['all_checks_passed']
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');aid=plan['audit_ids'][0];slug=plan['slugs'][0];ap=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');a=load(ap);assert a['state']=='blind-reconstructed'
assert rt.semantic_reviewer_packet(a)==load(r/'source.0.reviewer-packet.json') and rt.semantic_reviewer_packet(a)['packet_sha256']==q['reviewer_packet_sha256']
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']==slug);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256']==q['publication_binding_sha256']
adapter=copy.deepcopy(q);adapter['review_run_sha256']=s['run_sha256'];adapter['native_named_RAW_payload_sha256']=receipt['named_complete_payload_RAW_sha256'];adapter['native_payload_unchanged']=True;w(r/'source.0.review.root-adapter.json',adapter)
ds=[dict(slot=d['slot'],severity='informational',description=d['description'],evidence='Independent native '+d['classification']+' nonblocking classification in '+(n/'review.payload.json').as_posix()) for d in q['deltas']]
b=copy.deepcopy(a);b.update(state='accepted',semantic_slots=q['semantic_slots'],deltas=ds,verdict=q['verdict'],repairs=[]);b['source_review']=dict(state='accepted',reviewer=q['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=q['review_evidence'],review_run_sha256=s['run_sha256'],reviewer_packet_sha256=q['reviewer_packet_sha256'],run_artifact=(r/'source.0.review.root-adapter.json').as_posix())
registry=rt.load_registry();registry['audits']=[b if x['id']==aid else x for x in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
w(r/'root.source63.adoption.json',dict(status='INDEPENDENT_SCOPED_SOURCE_AND_ALL8_EXACT_FORMULA_PROOFS63_ACCEPTED',actual_adopter_pid=os.getpid(),native_run_sha256=s['run_sha256'],native_named_RAW_payload_sha256=receipt['named_complete_payload_RAW_sha256'],whole_run_hash_recipe=s['whole_run_hash_recipe'],payload_hash_recipe=s['named_full_payload_hash_recipe'],native_closed_outputs=122,qualified_pin_readbacks=len(seen),qualified_historical_resolutions=resolutions,mechanical_presentation_repair_independently_accepted=True,source_statement_repair=False,rendered_Exposition_Seal=False,remaining_boundary=plan['remaining_boundary'],VERIFIED=False))
(r/'audit.0.before-source-admission.raw.snapshot.json').write_bytes(ap.read_bytes());replace(ap,b)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
mirror=load(r/'conceptual-mirror-audit63.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']};boundary=plan['remaining_boundary']+' Independent mathematics, fresh source-blind decoder, source-first seven-slot review and mechanical excerpt repair/all8 literal spans accepted. Exact-science verification, serialized aggregate and rendered Exposition Seal remain separate.'
e=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command='lake build Tests.ProximalBPSMacroscopicDefectRoot',result='Root39868 and independent3376 EXIT0 PASS3920; exact sealed headers, standard3, zero private; genuine original-input macro root contractivity.'),dict(command='Independent source-first seven-slot and presentation repair review',result='24literal source regions; EXCESS0; all8 literal proof excerpts; whole native run and distinct RAW payload/122 CLOSED outputs verified.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+slug+'.json'],integration_notes='Canonical actual M onto closed HP, SAME U/T and transported scalar root. Typed B:HP-to-joint first Gram, all-macro energy/norm and ALL positive same-square uniqueness. Fulljoint P differs from macro identity. All8 exact step excerpts accepted after a presentation-only region correction. Sole existing PhaseKernel stabilization lane. No centered inverse/polar/H1/dynamics/main/cost/composition/full-paper claim.')
cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');cell=load(cp)
for k in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[k]=[dict(declaration=plan['mathematical_declarations'][0],declaration_level=cell['declaration_level'],report=cell[k])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
assert cell['status']=='claimed';(r/'cell.0.before-proved.raw.snapshot.json').write_bytes(cp.read_bytes());cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror;cell['evidence'].update(proof_review=(r/'independent-math63/native.receipt.json').as_posix(),source_review=(r/'source.0.review.root-adapter.json').as_posix(),execution_boundary=boundary);replace(cp,cell)
w(r/'proved-local.json',e)
print('PASS63 PROVED_LOCAL after independent math/blind decoder/source/presentation and reviewed publication admission. Exact commit VERIFIED and aggregate pending.')
