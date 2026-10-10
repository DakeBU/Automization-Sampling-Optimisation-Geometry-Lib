from pathlib import Path
import copy,hashlib,json,os,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub, astis_semantic_roundtrip as rt, astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');o=r/'independent-clean-source75';ov=r/'independent-clean-source75-admission-overlay'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z,path=None):
 p=Path(path or z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p;return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;write(p,x)
expected_overlay_lease,expected_overlay_payload=sys.argv[1:]
lp=o/'CLOSED_LAST.json';assert sha(lp.read_bytes())=='2de491f96fcce996feb3a98cb4b5da2d1753c6a457188e7c715b314768bf4dd6'
l=load(lp);assert l['status']=='CLOSED_LAST' and l['actor']=='/root/independent_clean_source75' and l['actual_EXIT']==0 and l['actual_PID']==42004
rows=l['complete_owned_prior_manifest'];assert len(rows)==l['complete_owned_prior_file_count']==51
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'source.0.run.json');h=sha(can({k:v for k,v in run.items() if k!='review_run_sha256'}));assert h==run['review_run_sha256']==l['review_run_sha256']=='db373b9bcc61a10d1ea3a42d51f16e8d5f3e34b4b8d6031e02f71b7e435887c5'
payload=load(o/'whole-logical-payload75.json');assert sha(can({k:v for k,v in payload.items() if k!='whole_logical_payload_sha256'}))==payload['whole_logical_payload_sha256']==l['whole_logical_payload_sha256']
assert len(payload['complete_named_RAW_payloads'])==5
for z in payload['complete_named_RAW_payloads']:assert check(z)==z['RAW_utf8'].encode()
assert run['independent_from_formalizer'] and run['independent_from_decoder'] and not run['VERIFIED_transition_performed']
inputs=load(o/'source.0.input-manifest.json');assert inputs['source_only_before_implementation'] and inputs['no_canonical_or_Git_mutation']
for z in inputs['clean_finite_inputs']:assert check(z)==Path(z['snapshot']).read_bytes()
assert run['mechanical_verification_full']['terminal']['actual_EXIT']==0
coverage=load(o/'source-proof-coverage75.json');assert coverage['node_count']==32 and coverage['edge_count']==67 and coverage['item_count']==137 and coverage['NODE']==77 and coverage['EXCLUDED']==60 and coverage['internal_bridge_count']==13
assert coverage['source_graph_preserved'] and coverage['source_classifications_preserved'] and not coverage['whole_paper_coverage']
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'read_only_verify75.py')],stdout=s,stderr=e);code=p.wait()
assert code==0
# The separately closed exact administrative overlay is checked below before any canonical write.
overlay_lease=ov/'CLOSED_LAST.json';assert sha(overlay_lease.read_bytes())==expected_overlay_lease
overlay=load(ov/'admission-overlay75.json')
assert overlay['accepted'] and overlay['source_review_run_sha256']==h
assert overlay['generation1_CLOSED_RAW_sha256']==sha(lp.read_bytes())
assert overlay['publication_binding_sha256']==run['clean_official_packet_full']['publication_binding_sha256']
# Exact overlay closure schema is finalized only after the independent writer closes.
ol=load(overlay_lease);assert ol['status']=='CLOSED_LAST'
orows=ol['complete_owned_prior_manifest']
assert {p.resolve() for p in ov.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in orows}|{overlay_lease.resolve()}
for z in orows:check(z);assert Path(z['path']).stat().st_mtime_ns<=overlay_lease.stat().st_mtime_ns
op=ov/'whole-logical-payload75.json';assert sha(op.read_bytes())==expected_overlay_payload
with (out/'overlay-readonly.stdout.log').open('wb') as s,(out/'overlay-readonly.stderr.log').open('wb') as e:
 q=subprocess.Popen([sys.executable,'-B','-X','utf8',str(ov/'read_only_verify75.py')],stdout=s,stderr=e);qc=q.wait()
assert qc==0
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert adv.current_advances()[claim['advance_id']]['state']=='EXPLORING'
assert load(r/'root.math75.adoption.json')['native_files']==46
assert load(r/'root.decoder75.adoption.json')['status']=='CLOSED_BLIND_DECODER75_ADOPTED_ONLY'
assert load(r/'root.review-input-metadata75.adoption.json')['fresh_source_required']
ap=Path('research-wiki/semantic-roundtrip/audits')/(plan['audit_ids'][0]+'.json');cp=Path('research-wiki/frontier-cells')/(plan['active_cells'][0]+'.json');pp=Path('website/content/publications')/(plan['slugs'][0]+'.json')
audit,cell,publication=load(ap),load(cp),load(pp);packet=load(r/'source-review.clean.packet.json');d=load(o/'source.0.decision.json');admission=load(o/'source.0.admission-fields.json')
assert audit['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(audit)==packet==run['clean_official_packet_full']
assert d['accepted'] and d['verdict']=='equivalent-after-elaboration' and not d['blocking_deltas'] and not d['repairs'] and d['source_first']
assert d['review_run_sha256']==admission['review_run_sha256']==h and d['reviewer_packet_sha256']==admission['reviewer_packet_sha256']==packet['packet_sha256']
assert audit['publication_binding_sha256']==admission['publication_binding_sha256']==overlay['publication_binding_sha256']
accepted=copy.deepcopy(audit);accepted.update(admission['audit_fields']);accepted.update(overlay['audit_state_overlay'])
assert rt.semantic_reviewer_packet(accepted)==packet
cell['source_proof_coverage']=overlay['cell_source_proof_coverage'];publication['items'][0]['source_proof_coverage']=overlay['publication_source_proof_coverage']
registry=rt.load_registry();registry['audits']=[accepted if x['id']==accepted['id'] else x for x in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
for path,kind in [(ap,'audit'),(cp,'cell'),(pp,'publication')]:
 snapshot=r/(kind+'.before-source-admission75.exactraw.json');assert not snapshot.exists();snapshot.write_bytes(path.read_bytes())
write(ap,accepted);write(cp,cell);write(pp,publication);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
item=next(x for x in pub.load() if x['id']==plan['slugs'][0]);assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==accepted['publication_binding_sha256'] and pub.review_context(item,item['bindings'][0],pub.inputs())==accepted['publication_context']
mirror=load(r/'conceptual-mirror-audit75.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary='One actual PBPS integrated hazard and first-clock law: original six analytic callers/eight literal definitions/ten conclusions; focused compiled, independent fresh math, strict-blind decoder and fresh source-first anti-anchored review accepted. Exact SCI75, serialized aggregate and reader remain pending. Recursive actual PDMP/iid nonaccumulation/global path/Markov/invariance/kernel/hypocoercivity/main/errors/expected-query costs/actual-input composition, full Exposition/PURIFIED/main/live/paper/Goal remain open.'
math=load(r/'root.math75.adoption.json')['fresh_compiler'];focused=load(r/'mathematics-freeze75.json')['compiled'][0]
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command=claim['focused_checks'][0],result=f"Root{focused['focused_PID']} EXIT0/{focused['jobs']}jobs; independent directLean{math['actual_foreground_Lean_PID']} EXIT0/standard3; fresh source Lean43360 EXIT0. Exact header and compiled BODY unchanged; negative inference routes retained.")],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+plan['slugs'][0]+'.json'],integration_notes='Actual73 flow/74 bounce rate are real parents; closed finite-time first crossing, measurable actual Exp(1) law, exact survival including infinity and original-energy waiting majorant are substantive consumers for finite actual recursion76. Earlier exposed source review is supplemental only; exact neutral metadata overlay plus fresh source-first review are bound separately. No arbitrary law/cap/provider, AS finite wait premise or fake consumer.')
for key in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[key]=[dict(declaration=plan['mathematical_declarations'][0],declaration_level=cell['declaration_level'],report=cell[key])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror;cell['evidence'].update(proof_review=(r/'independent-math75/decision.json').as_posix(),source_review=(o/'source.0.decision.json').as_posix(),source_admission_overlay=(ov/'admission-overlay75.json').as_posix(),execution_boundary=boundary);write(cp,cell)
new(r/'proved-local.json',e)
new(r/'root.source75.adoption.json',dict(status='ACCEPTED_FRESH_INDEPENDENT_SOURCE75_FIRST_CLOCK_ONLY',actual_root_PID=os.getpid(),native_owned_files=len(rows)+1,native_whole_logical_run_sha256=h,native_whole_five_payload=pin(o/'whole-logical-payload75.json'),native_lease=pin(lp),administrative_overlay_lease=pin(overlay_lease),administrative_overlay_complete_payload=pin(op),native_readonly_PID=p.pid,native_readonly_EXIT=code,overlay_readonly_PID=q.pid,overlay_readonly_EXIT=qc,coverage_counts={k:coverage[k] for k in ['node_count','edge_count','item_count','NODE','EXCLUDED','internal_bridge_count']},no_mathematical_repair=True,earlier_exposed_source_not_adopted=True,official_clean_reviewer_packet_unchanged=True,publication_binding_unchanged=True,VERIFIED=False,Goal_complete=False))
print('PASS75 PROVED_LOCAL once after full math/strictblind/fresh anti-source; exactscience/aggregate/reader remain pending.')
