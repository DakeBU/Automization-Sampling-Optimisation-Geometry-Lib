from pathlib import Path
import json,hashlib,copy,sys,runpy
sys.path.insert(0,str(Path('tools').resolve()))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-marginal-poincare57');s=r/'source-review57'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
count=0
def check(row):
 global count
 b=Path(row['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==row['bytes'] and sha(b)==row['raw_sha256'] and sha(lf)==row['lf_sha256'],row['path']
 if 'lf_bytes' in row:assert len(lf)==row['lf_bytes']
 count+=1
def selfcheck(d,k):
 o=copy.deepcopy(d);h=o.pop(k);assert sha(canon(o))==h,(k,h);return h
assert not (r/'proved-local.json').exists()
math=runpy.run_path('.astis/pbps-marginal-gradient51/adopt-math57.py')['require_math']()
q=j(s/'result0.json');nr=j(s/'reviewer.source.run.json');l=j(r/'source.review.lease.json');report=j(s/'source.review.json');manifest=j(s/'manifest.json');complete=j(s/'complete.json');iv=j(s/'input-verification.json');readbacks=j(s/'output.readbacks.json');im=j(s/'input.manifest.json')
assert sha((s/'result0.json').read_bytes())=='ec6237b62f7c52b0017a5c39367f9bff553c6fac4283cb9919413e95d0c17020'
assert sha((r/'source.review.lease.json').read_bytes())=='411cc533adc03cd89ff5e5bffdf55d08061c4ca73abb100689386bc77cba9912'
h=selfcheck(nr,'run_sha256');assert h==q['review_run_sha256']==l['reviewer_source_run_complete_minus_run_sha256']=='35e5f216e513a097ffb3dd8ff41ec3eaab380f5258e274ab9bc5fdbd0e4448f0'
for d in [l,report,manifest,complete,iv,readbacks,im]:selfcheck(d,'content_self_sha256')
assert l['status']==l['read_lease']==l['write_lease']==l['Python_lease']=='CLOSED' and l['compiler_lease']=='NOT_STARTED_CLOSED' and not l['compiler_started']
assert l['math_freeze602_current_unchanged'] and l['actual_foreground_sealing_process']['actual_exit_code']==0 and not l['foreground_lease_closer']['detached']
assert not l['strict_final_proof_body_blindness'] and not l['decoder_identity_blind'] and l['decoder_source_text_blind'] and not l['whole_math_verdict_read']
assert len(l['input_artifacts'])==l['input_actual_readback_count']==im['count']==len(im['pins'])==iv['native_input_count']==len(iv['native_inputs'])==614
assert len(l['actual_output_artifacts'])==l['output_actual_readback_count']==readbacks['count']==len(readbacks['artifacts'])==1252
assert manifest['count']==len(manifest['artifacts'])==1247 and readbacks['all_match'] and iv['all_match']
for row in l['input_artifacts']+l['actual_output_artifacts']+im['pins']+iv['native_inputs']+readbacks['artifacts']+manifest['artifacts']:check(row)
for key in ['original_OPEN_exact_snapshot','source_review_result','reviewer_source_run','input_manifest','output_readbacks','primary_first_contract','primary_first_closed_lease']:check(l[key])
for key in ['actual_foreground_sealing_process','foreground_lease_closer']:check(l[key]['script'])
assert len(iv['decoder_temporal_OPEN_input_checks'])==2
for row in iv['decoder_temporal_OPEN_input_checks']:
 check(row['current_CLOSED_path_pin']);check(row['preserved_exact_OPEN_snapshot'])
 assert all(row['historical_OPEN_input'][k]==row['preserved_exact_OPEN_snapshot'][k] for k in ['bytes','raw_sha256','lf_bytes','lf_sha256'])
admin_mappings=[]
for i,row in enumerate(iv['native_inputs']):
 snap=s/'inputs'/(f'{i:03d}.'+Path(row['path']).name+'.exactraw.snapshot')
 assert snap.read_bytes()==Path(row['path']).read_bytes(),(i,row['path'])
 if Path(row['path']).name in ['ASTIS-RT-20261008-GaussianMarginalPoincare.json','ASTIS-SHARED-gaussian-marginal-poincare.json']:
  b=snap.read_bytes();admin_mappings.append(dict(original=row,exactraw_snapshot=dict(path=snap.as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))))
assert len(admin_mappings)==2
for n in ['packet0.json','result0.json','run.json','lease.json','initial-lease.raw.snapshot.json']:assert (r/'anonymous-decoder'/n).read_bytes()==(Path('.astis/decoder-57')/n).read_bytes()
assert q['verdict']=='equivalent-after-elaboration' and not q['repairs'] and len(q['semantic_slots'])==7 and all(not x['blocking'] for x in q['deltas'])
assert q['independent_from_formalizer'] and q['independent_from_decoder'] and q['reviewer']=='/root/next_primary56'
plan=j(r/'publication-plan.json');claim=j(r/'claim.json');p=Path('research-wiki/semantic-roundtrip/audits')/(plan['audit_ids'][0]+'.json');a=j(p)
assert a['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(a)['packet_sha256']==q['reviewer_packet_sha256']==nr['reviewer_packet_sha256']
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']==plan['slugs'][0]);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256']==report['publication_binding_sha256']==nr['publication_binding_sha256']=='cd7704313084137b33ef2cff81e754a65cfe0cee0af14f8eddcacef27de8442e'
deltas=[dict(slot=x['slot'],severity='informational',description=x['description'],evidence='Independent source classification: '+x['classification']+'; explicitly nonblocking.') for x in q['deltas']]
accepted=copy.deepcopy(a);accepted.update(state='accepted',semantic_slots=q['semantic_slots'],deltas=deltas,verdict=q['verdict'],repairs=q['repairs'])
accepted['source_review']=dict(state='accepted',reviewer=q['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=q['review_evidence'],review_run_sha256=h,reviewer_packet_sha256=q['reviewer_packet_sha256'],run_artifact=(s/'result0.json').as_posix())
registry=rt.load_registry();registry['audits']=[accepted if x['id']==accepted['id'] else x for x in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
w(r/'root.source57.adoption.json',dict(status='INDEPENDENT_SOURCE57_NATIVE_ACCEPTED_NOT_VERIFIED',actual_pin_checks=count,native_complete_run_sha256=h,independent_result=l['source_review_result'],closed_lease=dict(path=(r/'source.review.lease.json').as_posix(),raw_sha256=sha((r/'source.review.lease.json').read_bytes())),canonical_nonblocking_delta_adapter=dict(recipe='Same artifact-backed API adapter native slot/classification/blocking/description -> canonical slot/severity/description/evidence.',native_result_unchanged=True,native_deltas=q['deltas'],canonical_deltas=deltas),historical_review_input_snapshot_mapping=admin_mappings,exposure=dict(strict_final_proof_body_blindness=False,decoder_identity_blind=False,decoder_source_text_blind=True,own_primary_blueprint_precedes_implementation=True),scope=plan['remaining_boundary']))
snapshot=r/'source-admission-before.0.raw.snapshot.audit.json';assert not snapshot.exists();snapshot.write_bytes(p.read_bytes());w(p,accepted)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
cells=[j('research-wiki/frontier-cells/'+x+'.json') for x in plan['active_cells']];mirror=cells[0]['conceptual_mirror_audit'];assert mirror['status']=='none-found'
boundary=plan['remaining_boundary']+' Complete independent mathematics, fresh source-text-blind decoder and own-primary-first source fidelity accepted; exact-science/shared aggregate pending. Final candidate-body exposure and identity nonblindness disclosed; all original negatives retained.'
e=dict(result_kind='integration-node',theorem_delta=claim['proposal']['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposal']['proposed_files'],focused_checks=[dict(command='lake build Tests.GaussianMarginalPoincare',result='Actual root production.0/test.4 PASS3904; independent one nonforced3904 PID54196/CLOSED. Main and SAME56 actual C3/C4 consumer standard3 only.'),dict(command='Independent complete mathematics / fresh anonymous decoder / own-primary-first source fidelity',result='602 original/611 distinct mathematics pins; six actual production parents and55/56 real consumer parents. Source614inputs1252outputreadbacks, seven semantic slots and zero repairs; exact1244 and six formula steps accepted.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+x+'.json' for x in plan['slugs']],integration_notes='Actual Gaussian marginal normalization/moments/sharp two-sided Hessians and genuine closure PI; SAME56 closure identity and actual55 stationary disintegration derive centering then sharp C3/C4. No private background copies/caller certificates. Full weakH1/macro/Gamma/dynamics/main/error/cost/composition remain OPEN; only originalPhaseKernel stabilization lane. Official bounded publication command timing debt and all source/compile/schema/temporal negatives preserved.')
for k in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[k]=[dict(declaration=plan['mathematical_declarations'][i],declaration_level=c['declaration_level'],report=c[k]) for i,c in enumerate(cells)]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['owner'],evidence=e)
for cid,c in zip(plan['active_cells'],cells):
 assert c['status']=='claimed';cp=Path('research-wiki/frontier-cells')/(cid+'.json');(r/'source-admission-before.0.raw.snapshot.cell.json').write_bytes(cp.read_bytes());c['status']='proved_locally';c['evidence'].update(proof_review=(r/'whole-math57/receipt.json').as_posix(),source_review=[(s/'result0.json').as_posix()],execution_boundary=boundary);w(cp,c)
w(r/'proved-local.json',e)
print('57 PROVED_LOCAL; independent math/source/decoder adopted. Actual source pin checks',count,'exact-science verification next.')
