exec(open('runs/20261007-companion-priority/gaussian-flip-energy/reviewer.exact.check.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
import publication_reader,datetime
C='7e293eb0470ea6f97368bbdc539e70609cbb3598';P='c3bbf938a6d46de7d43036d9f066ba68a3e6be6f'
def old(q):return subprocess.check_output(['git','show',P+':'+q])
def put(path,x):
 assert not path.exists(),path
 path.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(path)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C and subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==P
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
g=j(R/'reviewer.repository.gates.json');assert g['checked_commit']==C and len(g['results'])==6 and all(z['returncode']==0 for z in g['results'])
for row in g['results']:pin(row)
assert re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.repository.aggregate.log').read_text())==['9143','9415'] and 'ASTIS check passed' in (R/'reviewer.repository.aggregate.log').read_text()
prior=j(R/'reviewer.exact.bindings.json');verified=j(R/'verified.json');assert verified['verified_commit']==P and verified['verification_status']=='passed-scoped' and d(R/'verified.json')['raw_sha256']=='b7471a96ba7013162ea8ded2f0bb742acc00c8ddf29fcefa8c0dcf897c0fd91a'
admin=[];unchanged=0
for row in prior['git_inputs']:
 if d(row['path'])['raw_sha256']==row['raw_sha256']:unchanged+=1;continue
 assert row['path']=='research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-flip-energy.json'
 before=json.loads(old(row['path']));now=j(row['path']);paths=dif(before,now)
 assert set(paths)=={'/status','/evidence/execution_boundary','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review','/purification/dead_code_audit'}
 assert before['status']=='proved_locally' and now['status']=='independently_verified' and now['purification']['status']=='pending'
 assert now['evidence']['independent_verification']==(R/'verified.json').as_posix() and now['evidence']['independent_verification_details']['verified_commit']==P
 a=R/'reviewer.repository.cell.before.GitLF.snapshot.json';b=R/'reviewer.repository.cell.current.raw.snapshot.json';assert not a.exists() and not b.exists();a.write_bytes(old(row['path']));b.write_bytes(Path(row['path']).read_bytes());admin.append(dict(paths=paths,before=d(a),current=d(b)))
assert unchanged==656 and len(admin)==1
math=j(R/'whole-proof-review/math.review.json');pin(math['input_bindings']);mb=j(math['input_bindings']['path']);freeze=j(R/'math-freeze.json');assert len(mb['inputs'])==42 and len(freeze['inputs'])==27
for row in mb['inputs']+freeze['inputs']:pin(row)
plan=j(R/'publication-plan.json');decls=plan['mathematical_declarations'];pub.check_advance(decls,reviewed=True)
state=advance.current_advances();assert state[verified['advance_id']]['state']=='VERIFIED' and state[verified['advance_id']]['latest_evidence']['verifier_id']==V and [a for a,z in state.items() if z['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
data=pub.inputs();item=next(z for z in pub.load() if z['id']==plan['slugs'][0]);binding=next(z for z in item['bindings'] if z['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]];source=j(R/'source.0.review.overlay1.json');packet=j(R/'source.0.reviewer-packet.overlay1.json')
assert pub.binding_digest(item,binding,data)==prior['publication_binding_sha256']==source['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,binding,data)==packet['candidate_publication_context']==audit['publication_context'] and audit['state']=='accepted' and audit['source_review']['review_run_sha256']==prior['source_review_run_sha256']
assert j(R/'anonymous-decoder/run.json')['decoder_run_sha256']==prior['decoder_run_sha256']
roots=['AutoSamplingTheory/TechnicalLemmas.lean','Tests.lean','Tests/Basic.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean'];imports=[]
for q in roots[:2]:
 a=old(q).decode().splitlines();n=Path(q).read_text().splitlines();assert all(z in n for z in a);imports += [z for z in n if z not in a]
assert set(imports)=={'import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy','import Tests.GaussianFlipEnergy'}
assert old(roots[2]).replace(b' = 480 :=',b' = 481 :=').replace(b'\r\n',b'\n')==Path(roots[2]).read_bytes().replace(b'\r\n',b'\n')
reg=Path(roots[3]).read_text();assert reg.count('status := LemmaMemoryStatus.formalizedLocal')==old(roots[3]).decode().count('status := LemmaMemoryStatus.formalizedLocal')+1 and reg.count('localDecl := "'+decls[0]+'"')==1
assert Path(freeze['inputs'][0]['path']).read_text().splitlines()[0]=='import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy'
technical='research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl';a=old(technical).decode().splitlines();n=Path(technical).read_text(encoding='utf-8').splitlines();assert n[:len(a)]==a and len(n)==len(a)+1 and decls[0] in n[-1]
integration=j(R/'integration.json');assert integration['verified_proof_commit']==P and integration['aggregate_summary']==dict(root_build_jobs=9143,tests_build_jobs=9415,registry_leaves=481)
for z in integration['checks']:
 pin(z['log'])
 if 'status' in z:pin(z['status']);assert j(z['status']['path'])['exit_code']==0
 else:assert z['exit_code']==0
assert re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'aggregate.log').read_text())==['9143','9415']
assert '481 compiled local leaves, 883 modules, 4677 declarations' in (R/'site-build.log').read_text() and '12 chapters, 883 modules, 4677 declarations' in (R/'site-check.log').read_text()
graph=j('_site/data/underlying-lean-graph.json');site=j('_site/data/site-data.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
gc=j(R/'graph.0.json');assert pub.graph_report(gc['cell'],Path('_site'))==gc==integration['graph_check']
edge=dict(source='module:AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy',target='module:AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy',relation='imports');assert edge in integration['structural_branch']
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files()
changed=subprocess.check_output(['git','diff','--name-only',P,C],text=True).splitlines();assert len(changed)==56
assert {q for q in changed if not q.startswith('runs/')}==set(roots)|{'docs/companion-papers-handoff.md','research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-flip-energy.json',technical,'website/content/samplewiki_companion_frontiers.json'}
gitrows=[]
for q in changed:
 blob=subprocess.check_output(['git','show',C+':'+q]);live=Path(q).read_bytes();assert (blob==live if q.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),q;gitrows.append(dict(d(q),git_blob_sha256=sha(blob),mode='raw-exact' if q.startswith('runs/') else 'LF-exact'))
evidence=put(R/'reviewer.repository.bindings.json',dict(checked_commit=C,verified_proof_commit=P,prior_exact657_inputs_unchanged=656,one_cell_admin=admin,whole_math42_and_original27_unchanged=True,current_source_binding_sha256=prior['publication_binding_sha256'],current_source_review_run_sha256=source['review_run_sha256'],source_decoder_overlay_raw_preserved=True,shared_imports=imports,Registry_leaf=481,TestsBasic=481,integration=d(R/'integration.json'),root_static_checks_hash_verified=True,graph_report=d(R/'graph.0.json'),graph_digest=graph['publication_inputs_sha256'],graph_counts=graph['counts'],changed_Git56_inputs=gitrows,generated_site_inputs=[d('_site/data/underlying-lean-graph.json'),d('_site/data/site-data.json')],generated_site_stamp=site['git'],historical_generated_gate_stamp=site['gate'],fake_scan=dict(status='PASS',files=len(files),hits=0),named_standard_axioms_reused=verified['named_standard_axioms'],reader_delivery_boundary=integration['reader_inspection']))
seal=dict(schema_version=1,status='accepted-scoped',verification_status='passed-scoped',checked_commit=C,verifier_id=V,seal_kind='repository ProofSeal37',verified_proof_commit=P,previous_independent_verification=d(R/'verified.json'),fresh_repository_gates=g,raw_LF_Git_inputs=evidence,scope='Same independently VERIFIED compact C2 actual full Boolean flip-energy factor4 producer exercised through shared production/Test roots and Registry481; genuine36 parent, actual N0/N1 tests, current source/overlay bindings, graph freshness and fresh mandatory repository Lean/fake/source gates.',remaining_boundary=['Compact GaussianLSI, Hilbert/noncompact domain extension, T2/FIRST4.6, both papers main results/composition/query costs remain open.','Static formula/folded Lean and structural graph inspection are accepted in this scope. Full Test-inline/copy/download/bundles/browser/rendered/live acceptance, independent ExpositionSeal and postmerge PURIFIED remain separate.','Exact37 remote CI, main merge, deployment/live are not certified; generated site precommit+dirty and historical gate stamp retained honestly.','No VERIFIED/STABILIZING transition or new mathematical proof credit; future38 source-only artifacts excluded.'],canonical_mutations=False,leases=dict(read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED'),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
saved=put(R/'reviewer.repository.ProofSeal.json',seal)
basis=dict(actor=V,checked_commit=C,parent_proof_commit=P,gates=d(R/'reviewer.repository.gates.json'),bindings=evidence,ProofSeal=saved,status='CLOSED');run=put(R/'reviewer.repository.run.json',dict(basis,deterministic_run_sha256=pub.digest(basis)))
lp=R/'reviewer.repository.lease.json';initial=R/'reviewer.repository.lease.open.raw.snapshot.json';assert not initial.exists();initial.write_bytes(lp.read_bytes());lp.write_bytes((json.dumps(dict(status='CLOSED',checked_commit=C,verifier_id=V,read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED',initial_manifest=d(initial),receipt=saved,run=run),indent=2)+'\n').encode())
print(json.dumps(dict(status='accepted-scoped',checked_commit=C,receipt=saved,all_leases='CLOSED',canonical_mutations=False),ensure_ascii=False))
