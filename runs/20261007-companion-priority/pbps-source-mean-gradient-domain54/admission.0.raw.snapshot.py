from pathlib import Path
import json,hashlib,sys,copy
sys.path.insert(0,str(Path('tools').resolve()))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
run=Path('runs/20261007-companion-priority/pbps-source-mean-gradient-domain54')
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def check(row):
 p=Path(row['path']);b=p.read_bytes();assert sha(b)==row['raw_sha256'],p
 if row.get('lf_sha256'):assert sha(b.replace(b'\r\n',b'\n'))==row['lf_sha256'],p
 if row.get('bytes') is not None:assert len(b)==row['bytes'],p
def closed(p):
 d=j(p)
 for k in ['status','state','read','write','compiler','read_lease','write_lease','compiler_lease','Python','Python_lease','python','python_lease']:
  if k in d:assert d[k] in ['CLOSED','NOT_STARTED_CLOSED'],(p,k)
plan=j(run/'publication-plan.json');claim=j(run/'claim.json');assert not (run/'proved-local.json').exists()
mp=run/'whole-proof-review54'
for p in [mp/'lease.json',mp/'compiler.lease.json',run/'anonymous-decoder/lease.json',run/'source.review.lease.json',run/'reviewer.source.lease.json']:closed(p)
assert sha((mp/'run.json').read_bytes())=='e1f8d734266a608a90d4db7c59bc6789cd18af34a882c9df0fc23e81a34bedb7'
mr=j(mp/'run.json');projection=copy.deepcopy(mr);expected=projection.pop('run_sha256');assert sha(canon(projection))==expected
for row in mr['actual_outputs']:check(row)
ml=j(mp/'lease.json')
check(ml['run']);check(ml['receipt']);assert ml['status']==ml['read']==ml['write']==ml['Python']==ml['compiler']=='CLOSED'
check(ml['actual_compiler_CLOSED_lease'])
assert sha(canon(mr['run_binding_payload']))==mr['review_run_binding_sha256']==ml['review_payload_sha256']
for row in mr['actual_inputs']:check(row)
math=j(mp/'receipt.json');assert math['status']=='ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER' and not math['blockers']
assert math['actual_focused_compiler']['exit_code']==0 and math['actual_focused_compiler']['jobs']==3898
assert all(not row['fake_closure_hits'] for row in math['fake_closure_scan'])
assert all(set(row['axioms'])=={'propext','Classical.choice','Quot.sound'} for row in math['axiom_closures'])
for row in j(run/'math-freeze.json')['inputs']:check(row)
for row in j(run/'source.review.lease.json')['input_artifacts']:check(row)
r=j(run/'source.0.review.json');assert r['verdict']=='equivalent-after-elaboration' and not r['repairs']
assert all(d['classification']=='explicit-elaboration' for d in r['deltas'])
EXPECTED_SOURCE_RAW='6eb6ce1f1c77c1e282621a35d7c4045a805cf5ea06c6e850ffda5d56f4bc4a4a'
assert sha((run/'source.0.review.json').read_bytes())==EXPECTED_SOURCE_RAW
sr=j(run/'reviewer.source.run.json');projection=copy.deepcopy(sr);expected=projection.pop('run_sha256');assert sha(canon(projection))==expected=='910f925fa51c34aa1af68ab29633c170f74a7e3b6634a2cc453f25211aec6b00'
assert sha((run/'reviewer.source.run.json').read_bytes())=='91070b3e00dfc2838898586c6e868d1bd574b0871b36ac7d7e8bc5cbf0c2d408'
h=r['review_run_sha256'];assert sha(canon(sr['reviewer_run_binding_payload']))==sr['reviewer_run_binding_sha256']==h=='c31132907ed4ec78df5d49212de76d3dbc559139b5d8ee2bd2497e5200b195da'
check(sr['inputs'])
for row in sr['output_artifacts_before_run_and_leases']:check(row)
si=j(run/'reviewer.source.input-bindings.json');assert si['original566_manifest_preserved'] and len(si['original566_current_pins'])==566
for row in si['original566_current_pins']:check(row)
for label,n,expected_raw in [('own','reviewer.source.lease.json','8bdb83b9f55be32799c1b121fa83e7910cb9564f6d4e1d9fa5fad7e60ec0f99b'),('provided','source.review.lease.json','b842b69b4afed81142f45a9205b6576b2aa13a9a30aadc44974b27bff628272e')]:
 d=j(run/n);assert sha((run/n).read_bytes())==expected_raw
 check(d['native_run_artifact'])
 for row in d['native_output_artifacts']:check(row)
 core=copy.deepcopy(d);core.pop('native_output_artifacts');core.pop('native_run_artifact')
 assert core==sr['expected_final_lease_closure_cores'][label],label
 assert sha(canon(core))==sr['expected_closure_core_logical_sha256'][label],label
assert r['independent_from_formalizer'] and r['independent_from_decoder']
pb=j(run/'reviewer.source.publication-binding.checkpoint.json');assert sha(canon(pb['full_payload']))==pb['native_full_binding_digest']==r['publication_binding_sha256']=='d3a360b37b967ace97266b63ea9fab2aaea2fd1ce4a68e6255be1065ea42b8d3'
slots={'D54-authored-space':'domains','D54-closed-core':'scopes','D54-selected-scope':'conclusion'}
canonical_deltas=[dict(slot=slots[d['id']],severity='informational',description=d['source']+'; '+d['lean'],evidence='Native independent source54 '+d['id']+': '+d['classification']+'; '+d['necessity'],native_delta=d) for d in r['deltas']]
p=Path('research-wiki/semantic-roundtrip/audits')/(plan['audit_ids'][0]+'.json');a=j(p)
assert a['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(a)['packet_sha256']==r['reviewer_packet_sha256']
accepted=copy.deepcopy(a);accepted.update(state='accepted',semantic_slots=r['semantic_slots'],deltas=canonical_deltas,verdict=r['verdict'],repairs=r['repairs'])
accepted['source_review']=dict(state='accepted',reviewer=r['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=r['review_evidence'],review_run_sha256=h,reviewer_packet_sha256=r['reviewer_packet_sha256'],run_artifact=(run/'source.0.review.json').as_posix())
registry=rt.load_registry();registry['audits']=[accepted if x['id']==accepted['id'] else x for x in registry['audits']]
errors=rt.validate_registry(registry);assert not errors,errors
snap=run/'source-admission-before.0.raw.snapshot.audit.json';assert not snap.exists();snap.write_bytes(p.read_bytes());w(p,accepted)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
cells=[j('research-wiki/frontier-cells/'+x+'.json') for x in plan['active_cells']];mirror=cells[0]['conceptual_mirror_audit'];assert mirror['status']=='none-found'
boundary=plan['remaining_boundary']+' Independent complete mathematics and own-primary-first source0 accepted; exact-commit independent verification/shared integration remain pending. Anonymous source-text-blind reconstruction disclosed inherited general identities; strict identity blindness is not claimed. Source reviewer separately discloses incidental math-summary exposure after its own semantic assessment.'
e=dict(result_kind='integration-node',theorem_delta=claim['proposal']['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposal']['proposed_files'],focused_checks=[dict(command='lake build Tests.ProximalBPSSourceMeanGradientDomain',result='Actual3898PASS tests.4; SAME mu/J/nu/S actual canonical closed-gradient pair, real PUP mean consumer and noncentered rank0 canonical1/0; standard3 only. Original failures retained; direct proof-dependent toLp rewrite route retired in favor of actual MemLp.toLp_congr.'),dict(command='Independent whole mathematics / fresh anonymous decoder / own-primary-first source0',result='552 strict frozen mathematical originals plus566 full review inputs; independent3898PASS actualPID37192, complete actual50/53/51/weighted-C1 bodies, literal law/whole C1/L2/uniform genuine core/closed-gradient proof, actual PUP and rank0 canonical consumers; source0 equivalent-after-elaboration with three recorded informational scope/space/closed-core elaborations within advertised compact branch. Operative T54 correction retained.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+x+'.json' for x in plan['slugs']],integration_notes='The actual literal source mean canonical L2 function/gradient pair belongs to one uniform genuine gradient core closure on SAME nu. Full rough all-L2 B13/weak-H1 identification/Gamma/main/cost/composition remain separate. Original PhaseKernel sole stabilization lane unchanged. Five source-attributed formula steps in existing companion metadata; operative topology correction and failed routes retained.')
for k in ['statement_seal','source_proof_coverage','proof_digestion','purification']:
 e[k]=[dict(declaration=plan['mathematical_declarations'][i],declaration_level=c['declaration_level'],report=c[k]) for i,c in enumerate(cells)]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['owner'],evidence=e)
for cid,c in zip(plan['active_cells'],cells):
 assert c['status']=='claimed';cp=Path('research-wiki/frontier-cells')/(cid+'.json')
 (run/'source-admission-before.0.raw.snapshot.cell.json').write_bytes(cp.read_bytes())
 c['status']='proved_locally';c['evidence'].update(proof_review=(mp/'receipt.json').as_posix(),source_review=[(run/'source.0.review.json').as_posix()],execution_boundary=boundary);w(cp,c)
w(run/'proved-local.json',e)
print('54 PROVED_LOCAL with independent whole mathematics and source0 accepted; exact-commit verification next.')
