from pathlib import Path
import base64,copy,hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=root/'runs/20261007-companion-priority/pbps-reflection-intertwining69';o=r/'independent-source69'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(root).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;write(p,x)
def check(b,z):
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256']
 assert sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256']
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='ae74df4c28b149a46c0e28a4a87905b2585921b555fbac6abdbe375326f2444c'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['postclose_writes_permitted']
assert lease['owner']=='/root/independent_primary69' and lease['owned_file_count']==211
assert sha((o/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']=='9637e0a49b7d78bdd9283042d3a7c8951d2d105a7a851fb24dd45140900178ea'
m=load(o/'owned-manifest.json');rows=m['regular_file_entries'];assert len(rows)==209
assert sha(can(rows))==m['closure_entries_canonical_sha256']==lease['finite_owned_closure_sha256']
files={p.relative_to(o).as_posix():p for p in o.rglob('*') if p.is_file()}
assert set(files)=={z['name'] for z in rows}|{'owned-manifest.json','lease.final.json'}
last=(o/'lease.final.json').stat().st_mtime_ns
for z in rows:check(files[z['name']].read_bytes(),z);assert files[z['name']].stat().st_mtime_ns<=last
for k in ['COMPLETE_NAMED_DECISION','COMPLETE_NAMED_REVIEW_DECISION_INPUT','COMPLETE_RAW_REVIEW','SEPARATE_COMPLETE_RAW_LF_INPUT','FINITE_REVIEW_COVERAGE']:check((o/lease[k]['name']).read_bytes(),lease[k])
run=load(o/'review-run.json');logical=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='f1e5024fe6afdaedae4ac5f9b2dfc48bc86e09da51b490212c392bbc9bf2ce90'
payload=load(o/'RAW-input-payload.json');assert len(payload['entries'])==payload['count']==62
finite=[]
for z in payload['entries']:
 b=base64.b64decode(z['RAW_base64'],validate=True);lf=base64.b64decode(z['LF_base64'],validate=True)
 check(b,z);assert lf==b.replace(b'\r\n',b'\n') and len(lf)==z['LF_bytes']
 assert (o/z['name']).read_bytes()==b
 current=Path(z['original_path']).read_bytes()
 if current!=b:
  assert z['name']=='current.lesson.RAW.json'
  assert b==(r/'reader-api-overlay69/lesson.before.exactraw.json').read_bytes()
  assert sha(current)=='6242d60d05c88045f0beffda0a62eff912d0794d2c0ca98bde3f8574e7e2d43a'
  finite.append(dict(original_path=z['original_path'],before_RAW_sha256=sha(b),after_RAW_sha256=sha(current),independently_approved_exact_two_fields='reader-api-overlay69/application.json',post_overlay_packet_bound=True))
assert len(finite)==1
coverage=load(o/'finite-current-source-review-coverage.json')
assert coverage['source_math']['count']==419 and coverage['source_math']['NODE']==161 and coverage['source_math']['EXCLUDED']==258 and not coverage['source_math']['unclassified']
assert coverage['whole_module']['count']==446 and not coverage['whole_module']['unclassified']
assert coverage['BODY']['steps']==6 and coverage['BODY']['all_exact_code_and_formula_matches']
assert coverage['semantic_slots']['count']==7 and coverage['semantic_deltas']['blocking']==0 and coverage['mathematical_repairs']==0
assert coverage['top_level_common_witnesses']==12 and coverage['public_analytic_conditions']==6 and coverage['other_private_providers']==0
decision=load(o/'source.0.decision.json');assert sha((o/'source.0.decision.json').read_bytes())=='9ba27b05b85a94e051d7fafd83b2716836bb7702994c65a8a11479d85fdca9ea'
assert decision['verdict']=='equivalent-after-elaboration' and decision['repairs']==[] and not decision['mathematical_repair_needed']
assert decision['independent_from_formalizer'] and decision['independent_from_decoder'] and decision['review_run_sha256']==logical
assert len(decision['deltas'])==12 and all(z['severity']=='informational' and set(z)=={'slot','severity','description','evidence'} for z in decision['deltas'])
assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS) and all(z['evidence'] and z['relation']!='not-audited' for z in decision['semantic_slots'].values())
assert decision['publication_supports_admitted']==['reflection-intertwining'] and decision['publication_obligations_not_admitted']==['remaining-paper']
ap=root/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualReflectionIntertwining.json';audit=load(ap);assert audit['state']=='blind-reconstructed'
packet=load(r/'source.0.reviewer-packet.json');assert packet==rt.semantic_reviewer_packet(audit)
assert packet['packet_sha256']==decision['reviewer_packet_sha256']=='98e9a39c9f7eafea5a7a6660c162631fed010e9533ef2ab6debbdcdcd6405fc6'
assert sha((r/'source.0.reviewer-packet.json').read_bytes())==decision['reviewer_packet_RAW_sha256']
pub.inputs.cache_clear();pub.load.cache_clear();item=next(x for x in pub.load() if x['id']=='pbps-actual-reflection-intertwining')
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==audit['publication_binding_sha256']==decision['publication_binding_sha256']=='571c2916738f1981c5074a9a5f4e1cdf3efce3f94fafd26670566c70c3b25152'
assert pub.review_context(item,item['bindings'][0],pub.inputs())==audit['publication_context']
accepted=copy.deepcopy(audit);accepted.update(state='accepted',semantic_slots=decision['semantic_slots'],deltas=decision['deltas'],verdict=decision['verdict'],repairs=[])
accepted['source_review']=dict(state='accepted',reviewer=decision['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=decision['review_evidence'],review_run_sha256=logical,reviewer_packet_sha256=decision['reviewer_packet_sha256'],run_artifact=(o/'source.0.decision.json').relative_to(root).as_posix())
assert rt.semantic_reviewer_packet(accepted)==packet
registry=rt.load_registry();registry['audits']=[accepted if x['id']==audit['id'] else x for x in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
assert load(r/'root.math69.adoption.json')['native_files']==112 and load(r/'root.decoder69.adoption.json')['native_owned_files']==17
adoption=dict(status='ACCEPTED_INDEPENDENT_SOURCE69_P11_ONLY',actual_root_PID=os.getpid(),native_owned_files=211,native_inputs=62,native_whole_logical_run_sha256=logical,native_named_RAW_sha256=lease['COMPLETE_NAMED_REVIEW_DECISION_INPUT']['RAW_sha256'],native_lease=pin(o/'lease.final.json'),finite_preoverlay_input_maps=finite,all_other61_inputs_current_RAW=True,source_items=419,source_NODE=161,source_EXCLUDED=258,whole_module_lines=446,BODY_steps=6,semantic_slots=7,informational_deltas=12,blocking_deltas=0,mathematical_repairs=[],native_decision=pin(o/'source.0.decision.json'),canonical_schema_adapter_required=False,reader_aggregate=False,VERIFIED=False,Goal_complete=False)
new(r/'root.source69.adoption.json',adoption)
(r/'audit.before-source-admission.exactraw.json').write_bytes(ap.read_bytes());write(ap,accepted)
pub.inputs.cache_clear();pub.load.cache_clear();plan=load(r/'publication-plan.json');claim=load(r/'claim.json');pub.check_advance(plan['mathematical_declarations'],reviewed=True)
mirror=load(r/'conceptual-mirror-audit69.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary=claim['truth_boundary']+' Independent math112/blind17/source211 accepted with419 source items,446 lines,six literal BODY spans and seven slots. Exact science commit and serialized aggregate/reader remain pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command=claim['focused_checks'][0],result='Root43856 EXIT0/3948; independent fresh Lean1612 EXIT0; exactly propext,Classical.choice,Quot.sound. Earlier v1 API timeout is retained without theorem credit.'),dict(command='Independent math,blind decoder,primary-first source/publication review',result='CLOSED112/17/211;419 source items,446lines,6literal BODY spans,7slots;12 informational nonblocking deltas;0 mathematical repairs.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+s+'.json' for s in plan['slugs']],integration_notes='Same actual full-micro intertwining only. Next actual U(P-Pperp) rotation and corrector B21; no sharp-energy68 proof dependency or extra caller. Sole existing stabilization lane. No full main/cost/composition/Exposition/PURIFIED/Goal claim.')
cells=[root/'research-wiki/frontier-cells'/(c+'.json') for c in plan['active_cells']]
for key in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[key]=[dict(declaration=decl,declaration_level=load(p)['declaration_level'],report=load(p)[key]) for p,decl in zip(cells,plan['mathematical_declarations'])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
for p in cells:
 cell=load(p);assert cell['status']=='claimed';(r/'cell.before-proved.exactraw.json').write_bytes(p.read_bytes());cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror;cell['evidence'].update(proof_review=(r/'independent-math69/named-mathematical-review.payload.json').relative_to(root).as_posix(),source_review=(o/'source.0.decision.json').relative_to(root).as_posix(),execution_boundary=boundary);write(p,cell)
new(r/'proved-local.json',e)
new(r/'source-admission-finite-current-maps69.json',dict(source_input_maps=finite,audit_before=pin(r/'audit.before-source-admission.exactraw.json'),audit_after=pin(ap),only_review_admission_fields_changed=True,official_reviewer_packet_unchanged=True))
print('PASS69 PROVED_LOCAL: CLOSED112 math,17 blind,211 source; exact original inputs/full kerP; one production declaration; SCI/aggregate/reader pending.')
