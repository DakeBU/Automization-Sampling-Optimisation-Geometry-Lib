exec(open('runs/20261007-companion-priority/gaussian-product-entropy/reviewer.exact.gate.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
import sys,re,html
sys.path.insert(0,'tools')
import astis_publication as pub,astis_advance as advance,astis
import publication_reader
C='7e02d986a20af81d3c9ea027b3dcded6a8c25ffa';P='913438726472dcac2483cefbe6b4b2f4746cbe74'
def old(q):return subprocess.check_output(['git','show',P+':'+q])
def pin(row,p=None):
 x=d(p or row['path']);assert x['raw_sha256']==row['raw_sha256'],(x,row)
 if 'lf_sha256' in row:assert x['lf_sha256']==row['lf_sha256'],(x,row)
 return x
def diff(a,b,k=''):
 if type(a)!=type(b):return [k]
 if isinstance(a,dict):return [z for key in sorted(a.keys()|b.keys()) for z in ([k+'/'+key] if key not in a or key not in b else diff(a[key],b[key],k+'/'+key))]
 if isinstance(a,list):return [k] if len(a)!=len(b) else [z for i,(x,y) in enumerate(zip(a,b)) for z in diff(x,y,k+'/'+str(i))]
 return [] if a==b else [k]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C and subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==P
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
g=j(R/'reviewer.repository.gates.json');assert g['checked_commit']==C and g['all_pass'] and len(g['results'])==6
for row in g['results']:pin(row);assert row['returncode']==0
jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.repository.aggregate.log').read_text());assert jobs==['9145','9419'] and 'ASTIS check passed' in (R/'reviewer.repository.aggregate.log').read_text()
verified=j(R/'verified.json');assert verified['verified_commit']==P and verified['verification_status']=='passed-scoped' and d(R/'verified.json')['raw_sha256']=='2ceaedca3d8658a07c8723ab82a2014b1c5e827bcdc6e981ff26372ec96a6879'
prior=j(R/'reviewer.exact.bindings.json');unchanged=0;drifts=[]
cell='research-wiki/frontier-cells/ASTIS-SW-SPHMC-bounded-product-entropy.json';slt='research-wiki/cited-results/SLT_reuse_audit.md'
for row in prior['exact_Git_inputs']:
 if d(row['path'])['raw_sha256']==row['raw_sha256']:unchanged+=1;continue
 q=row['path'];assert q in [cell,slt]
 before=old(q);current=Path(q).read_bytes()
 a=R/f'reviewer.repository.changed.{len(drifts):02d}.before.Git.snapshot';b=R/f'reviewer.repository.changed.{len(drifts):02d}.current.raw.snapshot';assert not a.exists() and not b.exists();a.write_bytes(before);b.write_bytes(current)
 if q==cell:
  pre=json.loads(before);now=j(q);paths=diff(pre,now)
  assert set(paths)=={'/blocked/reason','/evidence/execution_boundary','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review','/purification/dead_code_audit','/status'}
  assert pre['status']=='proved_locally' and now['status']=='independently_verified' and now['purification']['status']=='pending'
  assert now['evidence']['independent_verification']==(R/'verified.json').as_posix() and now['evidence']['independent_verification_details']['verified_commit']==P
  drifts.append(dict(path=q,before=d(a),current=d(b),admin_paths=paths))
 else:
  lf_old=before.replace(b'\r\n',b'\n');lf_new=current.replace(b'\r\n',b'\n');assert lf_new.startswith(lf_old) and b'\r\r\n' not in current
  addition=lf_new[len(lf_old):];assert b'actual bounded binary product entropy checkpoint' in addition and P.encode() in addition
  addon=R/'reviewer.repository.SLT.appended.LF.snapshot.txt';assert not addon.exists();addon.write_bytes(addition)
  drifts.append(dict(path=q,before=d(a),current=d(b),normalized_original_prefix_unchanged=True,old_CR_count=before.count(b'\r'),current_CRLF_count=current.count(b'\r\n'),appended=d(addon),scope='Existing source/prior checkpoint text retained exactly under LF normalization. Mechanical LF->CRLF serialization plus append-only39 checkpoint; historical raw source input is not claimed current-unchanged.'))
assert unchanged==658 and len(drifts)==2
math=j(R/'whole-proof-review/math.review.json');pin(math['input_bindings']);mb=j(math['input_bindings']['path']);freeze=j(R/'math-freeze.json');assert len(mb['inputs'])==31 and len(freeze['inputs'])==26
for row in mb['inputs']+freeze['inputs']:pin(row)
plan=j(R/'publication-plan.json');decls=plan['mathematical_declarations'];pub.check_advance(decls,reviewed=True)
state=advance.current_advances();assert state[verified['advance_id']]['state']=='VERIFIED' and state[verified['advance_id']]['latest_evidence']['verifier_id']==V
assert [a for a,z in state.items() if z['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
data=pub.inputs();item=next(z for z in pub.load() if z['id']==plan['slugs'][0]);binding=next(z for z in item['bindings'] if z['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]];source=j(R/'source.0.review.json');packet=j(R/'source.0.reviewer-packet.json')
assert pub.binding_digest(item,binding,data)==prior['publication_binding_sha256']==source['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,binding,data)==packet['candidate_publication_context']==audit['publication_context'] and audit['state']=='accepted' and audit['source_review']['review_run_sha256']==prior['source_review_run_sha256']
dec=j(R/'anonymous-decoder/run.json');result=j(R/'anonymous-decoder/result0.json');assert pub.digest(dec['canonical_basis'])==dec['decoder_run_sha256']==prior['decoder_run_sha256']
assert dec['canonical_basis']['independent_reconstruction']=={k:result[k] for k in dec['canonical_basis']['independent_reconstruction']}
assert isinstance(dec['original_input_bindings'],dict) and j(R/'anonymous-decoder/lease.json')['status']=='CLOSED'
roots=['AutoSamplingTheory/TechnicalLemmas.lean','Tests.lean','Tests/Basic.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean'];imports=[]
for q in roots[:2]:
 a=old(q).decode().splitlines();n=Path(q).read_text().splitlines();assert all(z in n for z in a);imports += [z for z in n if z not in a]
assert set(imports)=={'import AutoSamplingTheory.TechnicalLemmas.InformationTheory.ProductEntropy','import Tests.ProductEntropy'}
assert old(roots[2]).replace(b' = 482 :=',b' = 483 :=').replace(b'\r\n',b'\n')==Path(roots[2]).read_bytes().replace(b'\r\n',b'\n')
reg=Path(roots[3]).read_text();assert reg.count('status := LemmaMemoryStatus.formalizedLocal')==old(roots[3]).decode().count('status := LemmaMemoryStatus.formalizedLocal')+1 and reg.count('localDecl := "'+decls[0]+'"')==1
assert all(z.startswith('import Mathlib.') for z in Path(freeze['inputs'][0]['path']).read_text().splitlines()[:4])
technical='research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl';a=old(technical).decode().splitlines();n=Path(technical).read_text(encoding='utf-8').splitlines();assert n[:len(a)]==a and len(n)==len(a)+1 and decls[0] in n[-1]
ledger='runs/substantive_advances.jsonl';a=old(ledger).decode().splitlines();n=Path(ledger).read_text(encoding='utf-8').splitlines();assert n[:len(a)]==a and len(n)==len(a)+1;event=json.loads(n[-1]);assert event['advance_id']==verified['advance_id'] and event['state']=='VERIFIED'
changes=subprocess.check_output(['git','diff','--name-only',P,C],text=True).splitlines()
canonical=[q for q in changes if not q.startswith('runs/')]
assert set(canonical)==set(roots+[technical,cell,slt,'docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json'])
handoff='docs/companion-papers-handoff.md';assert Path(handoff).read_bytes().replace(b'\r\n',b'\n').startswith(old(handoff).replace(b'\r\n',b'\n'))
execution='website/content/samplewiki_companion_frontiers.json';exchanges=diff(json.loads(old(execution)),j(execution));assert all(z.startswith('/execution/') for z in exchanges)
integration=j(R/'integration.json');assert integration['verified_proof_commit']==P and integration['aggregate_summary']==dict(root_build_jobs=9145,tests_build_jobs=9419,registry_leaves=483)
for z in integration['checks']:
 pin(z['log'])
 if 'status' in z:pin(z['status']);assert j(z['status']['path'])['exit_code']==0
 else:assert z['exit_code']==0
assert re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'aggregate.log').read_text())==jobs
assert '483 compiled local leaves, 887 modules, 4705 declarations' in (R/'site-build.log').read_text() and '12 chapters, 887 modules, 4705 declarations' in (R/'site-check.log').read_text()
graph=j('_site/data/underlying-lean-graph.json');site=j('_site/data/site-data.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
gc=j(R/'graph.0.json');assert pub.graph_report(gc['cell'],Path('_site'))==gc==integration['graph_check']
for edge in integration['structural_branch']:assert any(all(z.get(k)==v for k,v in edge.items()) for z in graph['edges']),edge
page=Path('_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html');page_text=page.read_text(encoding='utf-8');start=page_text.index('<section id="bounded-product-entropy"');depth=0
for match in re.finditer(r'</?section\b[^>]*>',page_text[start:]):
 depth+=-1 if match.group().startswith('</') else 1
 if depth==0:end=start+match.end();break
fragment=page_text[start:end];codes=[html.unescape(z) for z in re.findall(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',fragment,re.S)]
assert len(codes)==2 and re.sub(r'\s+','',codes[1]) in re.sub(r'\s+','',Path(freeze['inputs'][0]['path']).read_text(encoding='utf-8'))
for title in [z['title'] for u in j('website/content/declaration_lessons/bounded-product-entropy.json')['units'] for z in u['steps']]:assert title in fragment
assert fragment.count('Corresponding Lean step')==6 and 'Lean proof · bounded_product_entropy_subadditivity' in fragment
fs=R/'reviewer.repository.reader.branch.raw.snapshot.html';assert not fs.exists();fs.write_bytes(fragment.encode())
reader=put(R/'reviewer.repository.reader.static.json',dict(checked_commit=C,branch=d(fs),source_page=d(page),six_formula_steps=True,folded_actual_public_proof_matches_canonical=True,private_body_and_Test_source_inline_not_certified=True,Test_theorem_tails_inline=False,rendered_visual_browser_live_QA=False,generated_site_git=site['git'],historical_gate_stamp=site['gate'],boundary='Static limited branch accepted; full Test/copy/download/source bundles/rendered-browser/live/Exposition/PURIFIED not established.'))
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files()
selected=set(changes)|{freeze['inputs'][0]['path'],freeze['inputs'][1]['path'],'website/content/declaration_lessons/bounded-product-entropy.json','website/content/publications/bounded-product-entropy.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-BoundedProductEntropy.json'}
gitrows=[];proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=proc.communicate(('\n'.join(C+':'+v for v in sorted(selected))+'\n').encode());assert proc.returncode==0;offset=0
for q in sorted(selected):
 e=out.index(b'\n',offset);h=out[offset:e].split();assert h[-1]!=b'missing';size=int(h[-1]);offset=e+1;blob=out[offset:offset+size];offset+=size+1;live=Path(q).read_bytes();assert (blob==live if q.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),q
 gitrows.append(dict(d(q),git_raw_sha256=sha(blob),git_lf_sha256=sha(blob.replace(b'\r\n',b'\n')),raw_exact=blob==live))
evidence=put(R/'reviewer.repository.bindings.json',dict(checked_commit=C,verified_proof_commit=P,exact_prior_inputs=660,prior_raw_unchanged=unchanged,declared_administrative_successors=drifts,original26_math_whole31_unchanged=True,whole_math_review=d(R/'whole-proof-review/math.review.json'),verified_receipt=d(R/'verified.json'),changed_files=changes,exact_shared_Git_inputs=gitrows,root_imports=imports,Registry_leaf_count=483,technical_registry_single_actual_append=True,ledger_only_independent_VERIFIED_append=True,handoff_prefix_retained=True,companion_execution_only_changed_paths=exchanges,integration=d(R/'integration.json'),source_current_binding_sha256=audit['publication_binding_sha256'],source_review_run_sha256=source['review_run_sha256'],decoder_run_sha256=dec['decoder_run_sha256'],source95_current_files_not_all_claimed_unchanged=True,graph=dict(raw=d('_site/data/underlying-lean-graph.json'),publication_inputs_sha256=graph['publication_inputs_sha256'],node_count=len(graph['nodes']),edge_count=len(graph['edges']),actual_branch=integration['structural_branch'],graph_report=gc),generated_site_stamp=site['git'],historical_generated_gate_stamp=site['gate'],fake_scan=dict(status='PASS',files=len(files),hits=0),named_standard_axioms_reused=verified['named_standard_axioms'],independent_static_branch=reader))
seal=dict(schema_version=1,status='accepted-scoped',verification_status='passed-scoped',checked_commit=C,verifier_id=V,seal_kind='repository ProofSeal39',verified_proof_commit=P,previous_independent_verification=d(R/'verified.json'),fresh_repository_gates=g,raw_LF_Git_inputs=evidence,scope='Same independently VERIFIED bounded heterogeneous binary product entropy, including true joint/all-slice/marginal domains and zero mass/fibers, now exercised through actual shared production/Test roots and Registry483. All15 internal providers owner-covered; exact source-blind/source bindings and small formal/source graph contracts retained with fresh mandatory repository Lean/fake/source gates.',remaining_boundary=['Only bounded binary entropy producer. Unbounded/finite tensorization, finite/Hilbert/noncompact GaussianLSI, T2/FIRST4.6, both paper mains/querycosts/composition remain open.','Static six-formula/folded public Lean and structural graph acceptance is scoped; full private/Test-inline/copy/download/source bundles/browser/rendered/live/ExpositionSeal/postmerge PURIFIED remain separate.','Current39 remote CI/main merge/deployment/live not certified; earlier38 c4 CI is distinct historical evidence. Generated site precommit+dirty and historical gate stamp recorded honestly.','No new VERIFIED/STABILIZING transition or mathematical completion credit; future40 untracked source-only folders excluded.'],canonical_mutations=False,leases=dict(read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED'),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
saved=put(R/'reviewer.repository.ProofSeal.json',seal)
basis=dict(actor=V,checked_commit=C,parent_proof_commit=P,gates=d(R/'reviewer.repository.gates.json'),bindings=evidence,ProofSeal=saved,status='CLOSED');run=put(R/'reviewer.repository.run.json',dict(basis,deterministic_run_sha256=pub.digest(basis)))
lp=R/'reviewer.repository.lease.json';initial=R/'reviewer.repository.lease.open.raw.snapshot.json';assert not initial.exists();initial.write_bytes(lp.read_bytes());lp.write_bytes((json.dumps(dict(status='CLOSED',checked_commit=C,verifier_id=V,read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED',initial_manifest=d(initial),receipt=saved,run=run),indent=2)+'\n').encode())
print(json.dumps(dict(status='accepted-scoped',checked_commit=C,receipt=saved,shared_Git_inputs=len(gitrows),fake_files=len(files),fake_hits=0,all_leases='CLOSED',canonical_mutations=False),indent=2))
