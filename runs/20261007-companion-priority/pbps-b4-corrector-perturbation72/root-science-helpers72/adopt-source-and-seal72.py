from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72');o=r/'independent-header-source72'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(lf)==z['LF_sha256'],z['path']
 if 'LF_bytes' in z:assert len(lf)==z['LF_bytes']
def new(p,x):assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='881322b8b2abbf6293294d26447d92422b7429190999a2243dacb662f9a70430'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['canonical_Git_ledger_Goal_old_CLOSED_writes']
assert lease['owned_count']==254 and lease['bound_layer_count']==253
m=load(o/'owned-manifest.json');assert sha((o/'owned-manifest.json').read_bytes())==lease['native_manifest_RAW_sha256']=='aecafa71ac46afb86877a711b797260401c97956281d1aa986cbb05ae7b354f4'
assert sha(can(m['files']))==m['entries_canonical_sha256']==lease['entries_canonical_sha256']
files={p.relative_to(o).as_posix():p for p in o.rglob('*') if p.is_file()};assert len(files)==254 and set(files)=={z['path'] for z in lease['bindings']}|{'lease.final.json'}
assert set(files)=={z['path'] for z in m['files']}|{'owned-manifest.json','lease.final.json'}
for z in lease['bindings']:
 b=files[z['path']].read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256']
 assert files[z['path']].stat().st_mtime_ns<=files['lease.final.json'].stat().st_mtime_ns
run=load(o/'source-header72.run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='0035a46f67ff6f200d464a80b46e93cfb7102a4c97a92d36053c2f092e1cfe22'
stage=load(o/'stageA.freeze.run72.json');assert sha(can({k:v for k,v in stage.items() if k!='run_sha256'}))==stage['run_sha256']==run['StageA_whole_logical_run_sha256']=='41b3c1bfabc979034e1874b84759d21e7db6af1a2ec14544048c033c684a9253'
for z in run['records']+stage['records']:check(z)
payload=load(o/'complete-named-review-decision-input-payload72.json');assert sha((o/'complete-named-review-decision-input-payload72.json').read_bytes())=='3d9e0d764989c8ff9d83428e36da4f6be3efa93b877a98f5fc06520fcd8567e4'
d=load(o/'source-header72.decision.json');assert payload['complete_native_run']==run and payload['complete_decision']==d
assert payload['complete_RAW_review_utf8'].encode()==(o/'source-header72.review.RAW.md').read_bytes()
assert d['decision']=='accept_prospective_headers_source_facing_only' and d['independent_from_formalizer_and_math_reviewer'] and not d['required_repairs'] and not d['blocking_deltas']
assert d['all6callers12witnesses_oldclauses_retained'] and d['actual_rrho_H_K_B27_B28_not_claimed'] and not d['generic_B21_dependency']
for key in ['generic_header','actual_header','source_expectations_frozen_before_headers','source_graph_frozen_before_headers','all27_obligation_decisions','exact_parent_retention','generic_actual_primitive_map','full_RAW_review']:check(d[key])
manifest=load(o/'stageB.exact-header-input-manifest72.json');assert len(manifest['inputs'])==3
for z in manifest['inputs']:
 check(z);b=Path(z['path']).read_bytes()
 if 'snapshot' in z:assert (o/z['snapshot']).read_bytes()==b and (o/z['LF_snapshot']).read_bytes()==b.replace(b'\r\n',b'\n')
 else:
  assert z['path']=='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean' and len(z['fragments'])==2 and not z['parent_BODY_reread']
  for f in z['fragments']:
   raw=b[f['RAW_start']:f['RAW_end_exclusive']];assert len(raw)==f['RAW_bytes'] and sha(raw)==f['RAW_sha256']
   assert (o/f['snapshot']).read_bytes()==raw and (o/f['LF_snapshot']).read_bytes()==raw.replace(b'\r\n',b'\n')
primary=load(o/'stageA.primary-input-manifest72.json');check(primary['primary']);b=Path(primary['primary']['path']).read_bytes()
for z in primary['regions']:
 raw=b[z['RAW_start']:z['RAW_end_exclusive']];assert sha(raw)==z['RAW_sha256'] and len(raw)==z['RAW_bytes']
 assert (o/z['snapshot']).read_bytes()==raw and (o/z['LF_snapshot']).read_bytes()==raw.replace(b'\r\n',b'\n')
math=load(r/'root.header-math72.adoption.json');assert math['native_owned_files']==13 and math['native_inputs']==5 and not math['mathematical_repairs']
mr=load(r/'independent-header-math72/run72.json');assert sha((r/'independent-header-math72/review72.named.md').read_bytes())==mr['named_review_sha256']==math['named_complete_review_RAW_sha256']
proposal=load(r/'header72.proposal.json');assert [x['RAW_sha256'] for x in proposal['headers']]==[d['actual_header']['RAW_sha256'],d['generic_header']['RAW_sha256']]
new(r/'root.header-source72.adoption.json',dict(status='INDEPENDENT_PROSPECTIVE72_SOURCE_HEADERS_ONLY_ADOPTED',actual_root_PID=os.getpid(),native_files=254,current_candidate_parent_inputs=3,native_whole_logical_run_sha256=h,StageA_whole_logical_run_sha256=stage['run_sha256'],native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),source_counts=run['counts'],required_repairs=[],sourceblind=False,implementation_source_fidelity=False,proved=False,VERIFIED=False))
new(r/'root.statement-seal72.json',dict(schema_version=1,status='SEALED_BEFORE_PROOF_SEARCH_NOT_A_PROOF',actual_root_PID=os.getpid(),source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',proposed_files=proposal['proposed_files'],declarations=proposal['public_declarations'],exact_headers=proposal['headers'],source_anchor='PBPS B20 and Appendix B4 Ex28--Ex34 perturbation algebra; future actual B27/B28 adapter',source_graph=d['source_graph_frozen_before_headers'],source_expectations=d['source_expectations_frozen_before_headers'],binder_audit=(o/'source-header72.decision.json').as_posix(),math_audit=(r/'independent-header-math72/run72.json').as_posix(),library_retrieval=(r/'library-retrieval72/retrieval.json').as_posix(),mathematical_delta='Same C: C(u+Gamma0 r,v-A0 r)-C(u,v)=inner(u,Inv r)+norm(r)^2/2; generic complete-real-Hilbert leaf plus actual original-six-input/twelve-witness consumer.',generic_B21_parent=False,actual_integration_parent='ASTIS-SW-PBPS-actual-corrector-change',parent_exact_VERIFIED_required_before_claim=True,additional_analytic_public_premises=[],additional_regularity=[],rank_zero_allowed=True,alphaeta_one_allowed=True,signature_policy='Exact declarations, binders and full private literal are fixed by the two RAW headers. Proof-only tactic imports may extend the import block without changing any statement. Any mathematical statement change requires independent review.',failure_policy='After repeated same-shape failures diagnose mathematical statement/type/API; never add caller assumptions.',truth_boundary='No proof/compile/SAU/VERIFIED yet. Generic r is not actual r_rho; actual H/K/B27/B28, full B4/H1/main/errors/cost/composition and all whole-paper/Goal/Exposition/PURIFIED/main/live remain open.',claimed=False,proved=False))
print('PASS72 prospective source CLOSED254 and math CLOSED13 adopted; exact two statements SEALED before proof; no claim/Lean/implementation fidelity.')
