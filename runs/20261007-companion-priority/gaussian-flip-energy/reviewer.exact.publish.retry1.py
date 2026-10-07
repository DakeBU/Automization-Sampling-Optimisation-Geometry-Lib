exec(open('runs/20261007-companion-priority/gaussian-flip-energy/reviewer.exact.check.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
import datetime
def put(path,x):
 assert not path.exists(),path
 path.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(path)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
x=j(R/'reviewer.exact.bindings.json');assert x['status']=='passed-scoped-exact-admission-ready'
for row in x['git_inputs']:pin(row)
for row in x['gates']['results']:assert row['returncode']==0;pin(row)
s=j(R/'source.0.review.overlay1.json');p=j(R/'source.0.reviewer-packet.overlay1.json');old=j(R/'source.0.review.json');overlay=j(R/'dependency-metadata-overlay1/overlay1.review.json')
assert sha(p['source']['original_text'].encode())==s['source_text_sha256']==p['source']['text_sha256']
assert sha(p['lean']['statement'].encode())==s['statement_sha256']==p['lean']['statement_sha256']
assert s['source_excess']==[]
old_drifts=[];assert len(old['input_artifacts'])==83
for i,row in enumerate(old['input_artifacts']):
 snap=R/f'source.review.input.{i:03d}.raw.snapshot';pin(row,snap)
 assert (R/f'source.review.input.{i:03d}.lf.snapshot').read_bytes()==snap.read_bytes().replace(b'\r\n',b'\n')
 if d(row['path'])['raw_sha256']!=row['raw_sha256']:
  assert row['path'] in {'website/content/declaration_lessons/gaussian-compact-full-flip-energy.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianFlipEnergy.json','research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-flip-energy.json'}
  old_drifts.append(dict(path=row['path'],before=pin(row,snap),current=d(row['path']),paths=dif(j(snap),j(row['path']))))
O=R/'dependency-metadata-overlay1'
lesson=Path('website/content/declaration_lessons/gaussian-compact-full-flip-energy.json')
assert lesson.read_bytes()==(O/'lesson.before.raw.snapshot.json').read_bytes().replace(b'Filter.tendsto_inv_atTop_zero',b'tendsto_inv_atTop_zero',1)
assert d(O/'overlay1.review.json')['raw_sha256']=='94cd5cf10744a7fe04590de176499b0f31e8cf49e8d4ccaf7107006e54a94407'
for n in ['anonymous-decoder/lease.json','source.overlay1.review.lease.json','whole-proof-review/lease.json','dependency-metadata-overlay1/reviewer.overlay1.lease.json']:
 lease=j(R/n);assert lease['status']=='CLOSED',(n,lease)
for row in s['supporting_input_artifacts']:pin(row)
plan=j(R/'publication-plan.json');local=j(R/'proved-local.json');decls=plan['mathematical_declarations'];A='ASTIS-SA-20261007-GaussianFlipEnergy'
assert decls==local['lean_declarations']==local['publication_declarations'];pub.check_advance(decls,reviewed=True)
states=advance.current_advances();assert states[A]['state']=='PROVED_LOCAL' and states[A]['owner_id']!=V
stabilizing=[a for a,z in states.items() if z['state']=='STABILIZING'];assert stabilizing==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
snaps=[]
for q in ['research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-flip-energy.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianFlipEnergy.json']:
 target=R/('reviewer.exact.before.'+Path(q).name+'.raw.snapshot');assert not target.exists();target.write_bytes(Path(q).read_bytes());snaps.append(d(target))
admission=put(R/'reviewer.exact.admission-reconciliation.json',dict(status='passed-scoped',checked_commit=C,current119_admin=x['source_admin_reconciliation'],original83_inputs=83,original83_current_drift=old_drifts,one_name_overlay=d(O/'overlay1.review.json'),all27_mathfreeze_42_wholemath_pins_unchanged=True,original_BLOCKED_preserved=d(R/'source.0.review.json'),verifier_diagnostics=[dict(script=d(R/'reviewer.exact.check.py'),log=d(R/'reviewer.exact.check.log'),issue='Verifier omitted explicit accepted-source metadata_only_overlay administrative field.'),dict(script=d(R/'reviewer.exact.check.retry1.py'),log=d(R/'reviewer.exact.check.retry1.log'),issue='Verifier omitted declared cell execution/source/overlay evidence fields; all actual differences were enumerated before corrected check.'),dict(script=d(R/'reviewer.exact.check.retry2.py'),log=d(R/'reviewer.exact.check.retry2.log'),status='PASS')],mathematical_changes=False))
counts={}
for name,key,pattern in [('publication','publication',r'Publication PASS: (\d+)'),('semantic','semantic_audits',r'valid: (\d+) audits'),('frontier','frontier_cells',r'passed: (\d+) registered')]:
 counts[key]=int(re.search(pattern,(R/f'reviewer.exact.{name}.log').read_text())[1])
m=re.search(r'affected declarations=(\d+); changed cells=(\d+)',(R/'reviewer.exact.contributor.log').read_text());counts['contributor_declarations']=int(m[1]);counts['contributor_cells']=int(m[2])
gate=dict(status='PASS',checked_commit=C,focused_jobs=3163,aggregate_jobs=x['aggregate_jobs'],metadata_counts=counts,contributor_base=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),commands=x['gates'],root_scope='Previous integrated36 root/Tests/Registry480; new37 direct/focused exercised. No37 shared import or repository ProofSeal credit.')
se=dict(status='accepted',audit_id=plan['audit_ids'][0],reviewed=True,source_receipt=x['source_review'],packet=x['source_packet'],review_run_sha256=s['review_run_sha256'],publication_binding_sha256=s['publication_binding_sha256'],decoder_run_sha256=s['decoder_run_sha256'],decoder_packet_sha256=s['decoder_packet_sha256'],independent_actor=s['reviewer'],seven_slots=list(s['semantic_slots']),current_source_inputs=119,original_source_inputs=83,one_name_repair_overlay=d(O/'overlay1.review.json'),admin_reconciliation=admission)
receipt=dict(schema_version=4,verification_status='passed-scoped',verified_commit=C,checked_working_head=C,verifier_id=V,role='independent_verifier',advance_id=A,proving_owner=states[A]['owner_id'],lean_declarations=decls,publication_declarations=decls,result_kind=local['result_kind'],gate=gate,source_audit=se,fake_closure_scan=x['fake_closure_scan'],named_standard_axioms=x['named_standard_axioms'],exact_raw_LF_Git_evidence=d(R/'reviewer.exact.bindings.json'),exact_Git_inputs=x['git_input_count'],whole_math_review_reused=x['whole_math_review'],whole_math_bindings=42,original_math_freeze=27,private_providers=10,statement_seal=dict(bytes=877,raw_LF_sha256='4e9395eb1ff6054d2cc09ad4d938668d577935fb1a6c574a2e2c69dbe1d838f1'),proof_scope='Actual full Boolean all-coordinate flip energy limit factor4 under same normalized count law and Gaussian variance1. Only compact C2 caller assumptions; B/K/law/L1/limit internally derived. N0 fullenergy0/N1 fullenergy4 stress preserved and reused by exact bytes.',conceptual_mirror_audit=local['conceptual_mirror_audit'],remaining_boundary=x['remaining_boundary'],before_snapshots=snaps,repository_ProofSeal='pending serialized37 integration',leases=dict(read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED'),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
saved=put(R/'verified.json',receipt)
evidence=dict(gate=gate,verifier_id=V,verified_commit=C,source_audit=se,fake_closure_scan=x['fake_closure_scan'],lean_declarations=decls,publication_declarations=decls,conceptual_mirror_audit=local['conceptual_mirror_audit'],verification_receipt=saved,remaining_boundary=x['remaining_boundary'],independent_verifier_role=True)
advance.transition_advance(A,'VERIFIED',worker_id=V,evidence=evidence)
assert advance.current_advances()[A]['state']=='VERIFIED' and [a for a,z in advance.current_advances().items() if z['state']=='STABILIZING']==stabilizing
done=put(R/'reviewer.exact.transition.json',dict(status='CLOSED',advance_id=A,verified_commit=C,verifier_id=V,verification_receipt=saved,cell_projection_left_to_root=True,sole_STABILIZING_preserved=stabilizing))
lp=R/'reviewer.exact.lease.json';before=R/'reviewer.exact.lease.open.raw.snapshot.json';assert not before.exists();before.write_bytes(lp.read_bytes());lp.write_bytes((json.dumps(dict(status='CLOSED',verifier_id=V,verified_commit=C,read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED',initial_manifest=d(before),transition=done),indent=2)+'\n').encode())
print(json.dumps(dict(status='VERIFIED',verified_commit=C,receipt=saved,gate_counts=counts,git_inputs=x['git_input_count'],fake=x['fake_closure_scan'],all_leases='CLOSED'),ensure_ascii=False))
