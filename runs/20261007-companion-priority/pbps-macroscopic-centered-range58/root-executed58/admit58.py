from pathlib import Path
import json,hashlib,copy,sys
sys.path.insert(0,str(Path('tools').resolve()))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-macroscopic-centered-range58');s=r/'source-complete-review58'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));H=lambda b:hashlib.sha256(b).hexdigest();canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
n=j(s/'run.json');l=j(r/'source.complete.review.lease.json');v=j(s/'validator.json');c=j(s/'complete.json');im=j(s/'input.manifest.json');q=j(s/'source.2.complete.review.json')
assert H(canon({k:x for k,x in n.items() if k!='run_sha256'}))==n['run_sha256']==l['run_sha256']==q['review_run_sha256']=='16fc1812f0c671bf1848c1e2815089ab062fc8e88464c866f8958cae33d98715'
assert H(canon(n['source_review_payload']))==n['source_review_payload_sha256']==l['source_review_payload_sha256'];assert l['status']=='CLOSED' and l['compiler_lease']=='NOT_STARTED_CLOSED';assert c['validator_actual_exit_code']==c['seal_actual_exit_code']==0 and c['mathematical_blockers']==c['publication_blockers']==0 and c['current_publication_accepted']
rows=v['raw_lf_readbacks'];assert len(rows)==v['actual_raw_lf_readback_count']==351
for row in rows:
 b=Path(row['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==row['raw_bytes'] and H(b)==row['raw_sha256'] and len(lf)==row['lf_bytes'] and H(lf)==row['lf_sha256'],row['path']
mappings=[dict(original=x['actual_input'],exactraw_snapshot=x['exactraw_snapshot']) for x in im['inputs'] if '/semantic-roundtrip/audits/' in x['actual_input']['path'] or '/frontier-cells/' in x['actual_input']['path']]

s0=r/'source0-verdict-addendum58';n0=j(s0/'run.json');l0=j(s0/'lease.json');c0=j(s0/'complete.json');v0=j(s0/'validator.json');im0=j(s0/'input.manifest.json');q0=j(s0/'source.0.verdict-addendum.review.json')
assert H(canon({k:x for k,x in n0.items() if k!='run_sha256'}))==n0['run_sha256']==l0['run_sha256']==q0['review_run_sha256']=='c267d9cc30dd66179af65a5adc5ceff01b077fe1314b8fea98496d19a58f19c0'
assert H(canon(n0['source_review_payload']))==n0['source_review_payload_sha256']==l0['source_review_payload_sha256'];assert l0['status']=='CLOSED' and l0['compiler']=='NOT_STARTED_CLOSED';assert c0['validator_actual_exit_code']==c0['seal_actual_exit_code']==0 and c0['seven_slots_unchanged']
assert q0['semantic_slots']==j(r/'source-review58/source.0.review.json')['semantic_slots'] and q0['verdict']=='equivalent-after-elaboration'
assert len(v0['raw_lf_readbacks'])==v0['actual_raw_lf_readback_count']==118
for row in v0['raw_lf_readbacks']:
 b=Path(row['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==row['raw_bytes'] and H(b)==row['raw_sha256'] and len(lf)==row['lf_bytes'] and H(lf)==row['lf_sha256'],row['path']
mappings += [dict(original=x['actual_input'],exactraw_snapshot=x['exactraw_snapshot']) for x in im0['inputs'] if '/semantic-roundtrip/audits/' in x['actual_input']['path'] or '/frontier-cells/' in x['actual_input']['path']]
plan=j(r/'publication-plan.json');claim=j(r/'claim.json');accepted=[];adoptions=[]
assert not (r/'proved-local.json').exists()
assert j(r/'root.math58.adoption.json')['status']
for i,aid in enumerate(plan['audit_ids']):
 p=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');a=j(p);qp=s0/'source.0.verdict-addendum.review.json' if i==0 else r/'source-review58/source.1.review.json' if i==1 else s/'source.2.complete.review.json';q=j(qp)
 assert a['state']=='blind-reconstructed' and q['verdict'] in ['exact','equivalent-after-elaboration'] and not q['repairs'] and not q['mathematical_blockers'] and not q['publication_blockers'] and len(q['semantic_slots'])==7
 assert rt.semantic_reviewer_packet(a)['packet_sha256']==q['reviewer_packet_sha256']
 pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']==plan['slugs'][i]);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256']==q['publication_binding_sha256']
 assert q['independent_from_formalizer'] and q['independent_from_decoder'];ds=[]
 for d in q['deltas']:
  assert not d['blocking'];ds.append(dict(slot=d.get('slot','domains'),severity='informational',description=d['description'],evidence='Independent source classification '+d['classification']+'; native nonblocking result '+qp.as_posix()+' preserved.'))
 b=copy.deepcopy(a);b.update(state='accepted',semantic_slots=q['semantic_slots'],deltas=ds,verdict=q['verdict'],repairs=q['repairs']);b['source_review']=dict(state='accepted',reviewer=q['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=q['review_evidence'],review_run_sha256=q['review_run_sha256'],reviewer_packet_sha256=q['reviewer_packet_sha256'],run_artifact=qp.as_posix());accepted.append((p,b));adoptions.append(dict(native=qp.as_posix(),native_deltas=q['deltas'],canonical_deltas=ds))
registry=rt.load_registry();updates={a['id']:a for p,a in accepted};registry['audits']=[updates.get(a['id'],a) for a in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
w(r/'root.complete-source58.adoption.json',dict(status='ALL_THREE_SCOPED_SOURCE_RESULTS_ACCEPTED_NOT_EXACT_COMMIT_VERIFIED',whole_run_sha256=n['run_sha256'],named_source_payload_sha256=n['source_review_payload_sha256'],actual_current_source_raw_LF_checks=351,actual_source0_addendum_raw_LF_checks=118,source0_addendum_whole_run_sha256=n0['run_sha256'],source0_addendum_named_payload_sha256=n0['source_review_payload_sha256'],historical_mutable_input_mappings=mappings,canonical_delta_adapters=adoptions,earlier_negative_results_unchanged=True,remaining_boundary=plan['remaining_boundary']))
for i,(p,a) in enumerate(accepted):(r/('source-admission-before.'+str(i)+'.raw.snapshot.audit.json')).write_bytes(p.read_bytes());w(p,a)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
cells=[j('research-wiki/frontier-cells/'+x+'.json') for x in plan['active_cells']];assert all(x['conceptual_mirror_audit']['status']=='none-found' for x in cells)
boundary=plan['remaining_boundary']+' Complete independent precommit mathematics, anonymous source/identity-blind decoder and independent anti-anchored source review accepted. Exact-science commit verification and shared integration remain pending.'
e=dict(result_kind='integration-node',theorem_delta=claim['proposal']['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposal']['proposed_files'],focused_checks=[dict(command='lake build Tests.ProximalBPSMacroscopicRange',result='Root tests.2 PASS3908; independent whole-math58 focused PASS3908. All three declaration axioms only propext/Classical.choice/Quot.sound.'),dict(command='Independent complete mathematics, anonymous decoder, own-primary-first source fidelity',result='80 independent math inputs; three anonymous reconstructions; original source0/source1 accepted unchanged and fresh current source2 all7slots/all3claims/4formulae zero blockers,351 raw/LF readbacks. Original metadata negatives retained.')],truth_boundary=boundary,conceptual_mirror_audit=cells[0]['conceptual_mirror_audit'],useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+x+'.json' for x in plan['slugs']],integration_notes='Genuine arbitrary-measure AE pullback onto comap L2; actual PBPS P range/mean and full centered image; same actual55 M/T and actual57 T yield sharp allmacro contraction/squared defect. No root/inverse/weakH1/dynamics/cost/composition closure. Existing sole PhaseKernel stabilization lane; no new owner.')
for k in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[k]=[dict(declaration=plan['mathematical_declarations'][i],declaration_level=x['declaration_level'],report=x[k]) for i,x in enumerate(cells)]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['owner'],evidence=e)
for i,(cid,x) in enumerate(zip(plan['active_cells'],cells)):
 cp=Path('research-wiki/frontier-cells')/(cid+'.json');assert x['status']=='claimed';(r/('source-admission-before.'+str(i)+'.raw.snapshot.cell.json')).write_bytes(cp.read_bytes());x['status']='proved_locally';x['evidence'].update(proof_review=(r/'whole-math58/receipt.json').as_posix(),source_review=[a['native'] for a in adoptions],execution_boundary=boundary);w(cp,x)
w(r/'proved-local.json',e)
print('58 real reviewed publication gate passed; PROVED_LOCAL; native current source351 readbacks; exact-science verification pending.')
