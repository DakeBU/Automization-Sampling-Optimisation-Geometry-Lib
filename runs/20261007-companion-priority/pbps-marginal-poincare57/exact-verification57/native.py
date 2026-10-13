from common import *
sys.path.insert(0,str(R))
from tools import astis_publication as pub,astis_advance as advance
M=B/'whole-math57';S=B/'source-review57'
assert git('rev-parse','HEAD')==BASE
strict('inputs.native.json')
adoption=load(B/'root.source57.adoption.json');maps=adoption['historical_review_input_snapshot_mapping'];assert len(maps)==2
dec=load(B/'decoded.0.json');temporal=dec['initial_OPEN_lease_mapping']
pin_checks=[];used_maps=[];input_paths={}
def original_match(e,o):
 return path(e['path'])==path(o['path']) and all(e.get(k,o.get(k))==o.get(k,e.get(k)) for k in ['bytes','raw_sha256','lf_sha256','lf_bytes'])
def checkpin(e,where):
 p=path(e['path']);used=None
 if not equal(e):
  matched=[m for m in maps if original_match(e,m['original'])]
  if matched:
   assert len(matched)==1;used=matched[0];p=path(used['exactraw_snapshot']['path']);assert equal(used['exactraw_snapshot']) and equal(e,p)
  elif original_match(e,temporal['original']):
   used=temporal;p=path(used['actual_preserved']['path']);assert equal(used['actual_preserved']) and equal(e,p)
  else:raise AssertionError(('UNMAPPED_RAW_INPUT',where,e))
 if used:used_maps.append(dict(where=where,original=e,actual=pin(p),mapping=used))
 assert equal(e,p)
 input_paths[p.as_posix()]=pin(p);pin_checks.append(dict(where=where,original=e,actual=pin(p),mapped=used is not None))
def walk(x,where):
 if isinstance(x,dict):
  if all(k in x for k in ['path','raw_sha256','lf_sha256']):checkpin(x,where)
  for k,v in x.items():walk(v,where+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,where+'/'+str(i))
selves=[]
for p,k in [(M/'receipt.json','receipt_sha256'),(M/'run.json','run_sha256'),(M/'lease.json','lease_sha256'),(S/'reviewer.source.run.json','run_sha256'),(S/'source.review.json','content_self_sha256'),(S/'input-verification.json','content_self_sha256'),(S/'input.manifest.json','content_self_sha256'),(S/'manifest.json','content_self_sha256'),(S/'output.readbacks.json','content_self_sha256'),(S/'publication.binding.payload.json','content_self_sha256'),(B/'source.review.lease.json','content_self_sha256')]:
 selves.append(selfcheck(p,k));walk(load(p),p.relative_to(R).as_posix());input_paths[p.as_posix()]=pin(p)
mathrun=load(M/'run.json');assert logical(mathrun['review_binding_payload'])==mathrun['review_binding_payload_sha256']
mathinputs=load(M/'input.manifest.json');assert mathinputs['distinct_count']==611
for e in mathinputs['inputs']:checkpin(e,'math57_distinct_inputs')
mathlease=load(M/'lease.json');assert mathlease['status']=='CLOSED' and mathlease['actual_compiler_exit_code']==0
receipt=load(M/'receipt.json');assert len(receipt['fake_closure_scan'])==10
for scan in receipt['fake_closure_scan']:
 checkpin(scan['input'],'math57_fake_scan');assert not scan['authored_fake_closure_hits']
sl=load(B/'source.review.lease.json');assert sl['status']=='CLOSED' and sl['compiler_lease']=='NOT_STARTED_CLOSED'
assert all(sl[k]=='CLOSED' for k in ['read_lease','write_lease','Python_lease'])
assert len(sl['input_artifacts'])==614 and len(sl['actual_output_artifacts'])==1252
outprev=load(S/'output.readbacks.json')['artifacts'];assert len(outprev)==1251
outlast=sl['actual_output_artifacts'];lastset={path(x['path']).as_posix() for x in outlast};prevset={path(x['path']).as_posix() for x in outprev}
assert lastset-prevset=={(S/'output.readbacks.json').as_posix()} and prevset-lastset==set()
sr=load(S/'reviewer.source.run.json');q=load(S/'result0.json');canonical=load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-GaussianMarginalPoincare.json')
assert sr['run_sha256']==q['review_run_sha256']==adoption['native_complete_run_sha256']==sl['reviewer_source_run_complete_minus_run_sha256']
assert q['verdict']=='equivalent-after-elaboration' and len(q['semantic_slots'])==7 and len(q['deltas'])==3 and not q['repairs']
assert all(d['blocking'] is False for d in q['deltas']) and q['independent_from_formalizer'] and q['independent_from_decoder']
assert canonical['state']=='accepted' and canonical['source_review']['review_run_sha256']==sr['run_sha256']
adapter=adoption['canonical_nonblocking_delta_adapter'];assert q['deltas']==adapter['native_deltas'] and canonical['deltas']==adapter['canonical_deltas']
assert canonical['semantic_slots']==q['semantic_slots'] and canonical['verdict']==q['verdict'] and canonical['repairs']==q['repairs']
assert sr['decoder_source_text_blind'] and not sr['decoder_identity_blind'] and not sr['strict_final_proof_body_blindness']
payload=load(S/'publication.binding.payload.json');assert logical(payload['payload'])==payload['named_payload_sha256']==sr['publication_binding_sha256']==canonical['publication_binding_sha256']
items=[(i,b) for i in pub.load() for b in i['bindings'] if b['declaration']==TARGET];assert len(items)==1
actual_payload=pub.binding_payload(*items[0]);assert actual_payload==payload['payload'] and pub.digest(actual_payload)==payload['named_payload_sha256']
dump('publication.payload.actual.json',dict(payload=actual_payload,named_payload_sha256=logical(actual_payload),recipe='Full actual astis_publication.binding_payload item/binding; no context projection substituted.'))
portable=dec['portable'];walk(dec,'decoder_root_adoption')
dr=load(dec['native_run']['path']);dl=load(dec['actual_CLOSED_lease']['path']);selves.append(selfcheck(dec['native_run']['path']));walk(dr,'decoder_native_run');walk(dl,'decoder_native_lease')
assert dr['run_sha256']==dec['native_complete_run_sha256'];assert dl['status']=='CLOSED'
assert dec['source_text_blind'] and not dec['strict_identity_blind']
iv=load(S/'input-verification.json')
for x in iv['decoder_temporal_OPEN_input_checks']:
 checkpin(x['historical_OPEN_input'],'decoder_historical_OPEN_exact_mapping');checkpin(x['preserved_exact_OPEN_snapshot'],'decoder_preserved_OPEN');checkpin(x['current_CLOSED_path_pin'],'decoder_actual_CLOSED')
assert len(iv['decoder_temporal_OPEN_input_checks'])==2
state=advance.current_advances();cur=state['ASTIS-SA-20261008-GaussianMarginalPoincare'];assert cur['state']=='PROVED_LOCAL' and cur['owner_id']!=ACTOR
lane=[k for k,v in state.items() if v['state']=='STABILIZING'];assert lane==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
cell=load('research-wiki/frontier-cells/ASTIS-SHARED-gaussian-marginal-poincare.json');assert cell['status']=='proved_locally'
assert cell['evidence']['source_review']==[str((S/'result0.json').relative_to(R).as_posix())]
adm=[]
for original,filename in [('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-GaussianMarginalPoincare.json','before-transition.audit.raw.snapshot.json'),('research-wiki/frontier-cells/ASTIS-SHARED-gaussian-marginal-poincare.json','before-transition.cell.raw.snapshot.json')]:
 assert path(original).read_bytes()==(O/filename).read_bytes();adm.append(dict(original=pin(original),exactraw_snapshot=pin(O/filename)));input_paths[(O/filename).as_posix()]=pin(O/filename)
dump('before-transition.mappings.json',dict(exact_verified_admin_before_mappings=adm,recipe='Exactly TWO current full raw/LF audit/cell snapshots; entire original row equality required. These are distinct from historical source admission mappings.'))
dump('native.checks.json',dict(status='PASS',checked_commit=BASE,pin_check_count=len(pin_checks),pin_checks=pin_checks,complete_object_self_checks=selves,source_native_schema='astis-independent-source-review-run-v1',source614_count=614,source_terminal_output_count=1252,source_predecessor_output_count=1251,terminal_difference_only_own_readback=True,historical_mapping_count=2,mapped_checks=used_maps,math602_originals_unchanged=True,math611_distinct_unchanged=True,math_full_body_reused=pin(M/'mathematical-reasons.json'),source_result=pin(S/'result0.json'),source_run=pin(S/'reviewer.source.run.json'),source_CLOSED_lease=pin(B/'source.review.lease.json'),source_binding_sha256=payload['named_payload_sha256'],canonical_nonblocking_deltas_exact=adapter,decoder_source_TEXT_blind=True,decoder_identity_blind=False,final_proof_body_blind=False,source_review_slot_count=7,source_repairs=0,sole_STABILIZING=lane,advance_current_state='PROVED_LOCAL',cell_source_review_normalization='Existing singleton list to exact same path STRING only with authorized VERIFIED mutation; administrative, not source verdict defect.'))
for p in [B/'root.source57.adoption.json',B/'root.whole-math57.adoption.json',B/'proved-local.json',B/'decoded.0.json',path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-GaussianMarginalPoincare.json'),path('research-wiki/frontier-cells/ASTIS-SHARED-gaussian-marginal-poincare.json')]:input_paths[p.as_posix()]=pin(p)
dump('input.manifest.native.json',dict(inputs=list(input_paths.values()),count=len(input_paths),recipe='Actual distinct raw/LF/bytes rows; complete expected original mappings recorded in native.checks.json.'))
print(json.dumps(dict(status='PASS',actual_pin_checks=len(pin_checks),native_self_checks=len(selves),distinct_native_inputs=len(input_paths),source614=614,terminal1252=1252,historical_two_maps=True,checked_commit=BASE)))
