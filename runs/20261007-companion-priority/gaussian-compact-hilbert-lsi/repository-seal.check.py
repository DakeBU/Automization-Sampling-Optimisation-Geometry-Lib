exec(open('runs/20261007-companion-priority/gaussian-compact-hilbert-lsi/repository-seal.gates.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
import sys,re,difflib,html
sys.path.insert(0,'tools')
import astis,astis_publication as pub,astis_advance as advance,publication_reader
P='8c44529058e9a7e3ad58951550f45785639d5036'
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
verified=j(R/'verified.json');assert verified['verified_commit']==P and verified['verification_status']=='passed-scoped' and d(R/'verified.json')['raw_sha256']=='f433cf5fa0ea95437d5eedb7e8519040750673cda00213d77864826c1dec5792'
prior=j(R/'reviewer.exact.bindings.json');unchanged=0;drifts=[]
cell='research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-compact-hilbert-lsi.json';slt='research-wiki/cited-results/SLT_reuse_audit.md'
for row in prior['exact_Git_inputs']:
 if d(row['path'])['raw_sha256']==row['raw_sha256']:unchanged+=1;continue
 q=row['path'];assert q in [cell,slt];before=old(q);current=Path(q).read_bytes()
 a=R/f'repository-seal.changed.{len(drifts):02d}.before.Git.snapshot';b=R/f'repository-seal.changed.{len(drifts):02d}.current.raw.snapshot';assert not a.exists() and not b.exists();a.write_bytes(before);b.write_bytes(current)
 if q==cell:
  pre=json.loads(before);now=j(q);paths=diff(pre,now)
  assert set(paths)=={'/blocked/reason','/evidence/execution_boundary','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review','/purification/dead_code_audit','/status'}
  assert pre['status']=='proved_locally' and now['status']=='independently_verified' and now['purification']['status']=='pending'
  assert now['evidence']['independent_verification']==(R/'verified.json').as_posix() and now['evidence']['independent_verification_details']['verified_commit']==P
  drifts.append(dict(path=q,before=d(a),current=d(b),admin_paths=paths))
 else:
  lo=before.replace(b'\r\n',b'\n');ln=current.replace(b'\r\n',b'\n');assert ln.startswith(lo) and b'\r\r\n' not in current
  assert b'GaussianCompactHilbertLogSobolev.compact_stdGaussian_logSobolev' in ln[len(lo):] and P.encode() in ln[len(lo):]
  drifts.append(dict(path=q,before=d(a),current=d(b),normalized_original_prefix_unchanged=True,scope='Append-only41 memory successor, not an unchanged current historical source input.'))
assert unchanged==439 and len(drifts)==2
freeze=j(R/'math-freeze.json');mb=j(R/'whole-proof-review/inputs.json');assert len(freeze['inputs'])==39 and len(mb['bindings'])==70
for row in freeze['inputs']:pin(row)
for row in mb['bindings']:pin(row);pin(row,row['raw_snapshot'])
plan=j(R/'publication-plan.json');decls=plan['mathematical_declarations'];pub.check_advance(decls,reviewed=True)
data=pub.inputs();item=next(z for z in pub.load() if z['id']==plan['slugs'][0]);binding=next(z for z in item['bindings'] if z['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]];source=j(R/'source.0.review.json');packet=j(R/'source.0.reviewer-packet.json')
assert pub.binding_digest(item,binding,data)==prior['publication_binding_sha256']==source['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,binding,data)==packet['candidate_publication_context']==audit['publication_context'] and audit['state']=='accepted' and audit['source_review']['review_run_sha256']==prior['source_review_run_sha256']
assert d(R/'anonymous-decoder/run.json')['raw_sha256']==prior['decoder_run_sha256'] and j(R/'anonymous-decoder/lease.json')['status']=='CLOSED'
assert source['whole_module_covered'] and source['private_declarations_covered']==['pullback_energy']
state=advance.current_advances();assert state[verified['advance_id']]['state']=='VERIFIED' and state[verified['advance_id']]['latest_evidence']['verifier_id']==V
assert [a for a,z in state.items() if z['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
roots=['AutoSamplingTheory/TechnicalLemmas.lean','Tests.lean','Tests/Basic.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean'];imports=[]
for q in roots[:2]:
 a=old(q).decode().splitlines();n=Path(q).read_text().splitlines();assert all(z in n for z in a);imports += [z for z in n if z not in a]
assert set(imports)=={'import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev','import Tests.GaussianCompactHilbertLogSobolev'}
assert old(roots[2]).replace(b' = 484 :=',b' = 485 :=').replace(b'\r\n',b'\n')==Path(roots[2]).read_bytes().replace(b'\r\n',b'\n')
reg=Path(roots[3]).read_text();assert reg.count('status := LemmaMemoryStatus.formalizedLocal')==old(roots[3]).decode().count('status := LemmaMemoryStatus.formalizedLocal')+1 and reg.count('localDecl := "'+decls[0]+'"')==1
technical='research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl';a=old(technical).decode().splitlines();n=Path(technical).read_text(encoding='utf-8').splitlines();assert n[:len(a)]==a and len(n)==len(a)+1 and decls[0] in n[-1]
ledger='runs/substantive_advances.jsonl';a=old(ledger).decode().splitlines();n=Path(ledger).read_text(encoding='utf-8').splitlines();assert n[:len(a)]==a and len(n)==len(a)+1;event=json.loads(n[-1]);assert event['advance_id']==verified['advance_id'] and event['to_state']=='VERIFIED'
changes=subprocess.check_output(['git','diff','--name-only',P,C],text=True).splitlines();canonical=[q for q in changes if not q.startswith('runs/')]
assert set(canonical)==set(roots+[technical,cell,slt,'docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json'])
handoff='docs/companion-papers-handoff.md';op=difflib.SequenceMatcher(a=old(handoff).decode().replace('\r\n','\n').splitlines(keepends=True),b=Path(handoff).read_text(encoding='utf-8').splitlines(keepends=True),autojunk=False).get_opcodes()
assert all(tag in ['equal','insert'] for tag,*_ in op) and sum(j2-j1 for tag,i1,i2,j1,j2 in op if tag=='insert')==42
execution='website/content/samplewiki_companion_frontiers.json';exchanges=diff(json.loads(old(execution)),j(execution));assert all(z.startswith('/execution/') for z in exchanges)
integration=j(R/'integration.json');assert integration['verified_proof_commit']==P and integration['aggregate_summary']==dict(root_build_jobs=9147,tests_build_jobs=9423,registry_leaves=485)
for z in integration['checks']:
 pin(z['log'])
 if 'status' in z:pin(z['status']);assert j(z['status']['path'])['exit_code']==0
 else:assert z['exit_code']==0
jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'aggregate.log').read_text());assert jobs==['9147','9423'] and 'ASTIS check passed' in (R/'aggregate.log').read_text()
assert j(R/'aggregate.status.json')['command']==['tools/astis.py','check'] and j(R/'root.integration.lease.json')['status']=='CLOSED'
g=j(R/'repository-seal.gates.json');assert g['checked_commit']==C and g['all_pass'] and len(g['results'])==5
for row in g['results']:pin(row);assert row['returncode']==0
coverage=[]
for line in (R/'repository-seal.publication.log').read_text(encoding='utf-8').splitlines():
 if line.startswith('Private implementation coverage: '):
  row=json.loads(line[len('Private implementation coverage: '):])
  if row['file']==freeze['inputs'][0]['path']:coverage.append(row);assert row['owner']==decls[0]
assert len(coverage)==1
graph=j('_site/data/underlying-lean-graph.json');site=j('_site/data/site-data.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
gc=j(R/'graph.0.json');assert pub.graph_report(gc['cell'],Path('_site'))==gc==integration['graph_check']
for edge in integration['structural_branch']:assert any(all(z.get(k)==v for k,v in edge.items()) for z in graph['edges']),edge
assert '485 compiled local leaves, 891 modules, 4727 declarations' in (R/'site-build.log').read_text() and '12 chapters, 891 modules, 4727 declarations' in (R/'site-check.log').read_text()
page=Path('_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html');t=page.read_text(encoding='utf-8');start=t.index('<section id="gaussian-compact-hilbert-lsi"');depth=0
for m in re.finditer(r'</?section\b[^>]*>',t[start:]):
 depth+=-1 if m.group().startswith('</') else 1
 if depth==0:end=start+m.end();break
fragment=t[start:end];codes=[html.unescape(z) for z in re.findall(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',fragment,re.S)]
assert len(codes)==2 and re.sub(r'\s+','',codes[1]) in re.sub(r'\s+','',Path(freeze['inputs'][0]['path']).read_text(encoding='utf-8'))
for title in [z['title'] for u in j('website/content/declaration_lessons/gaussian-compact-hilbert-lsi.json')['units'] for z in u['steps']]:assert title in fragment
assert fragment.count('Corresponding Lean step')==7
fs=R/'repository-seal.reader.branch.raw.snapshot.html';assert not fs.exists();fs.write_bytes(fragment.encode())
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files()
selected=set(changes)|{freeze['inputs'][0]['path'],freeze['inputs'][1]['path'],'website/content/declaration_lessons/gaussian-compact-hilbert-lsi.json','website/content/publications/gaussian-compact-hilbert-lsi.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianCompactHilbertLogSobolev.json'}
gitrows=[];pr=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=pr.communicate(('\n'.join(C+':'+v for v in sorted(selected))+'\n').encode());assert pr.returncode==0;offset=0
for q in sorted(selected):
 e=out.index(b'\n',offset);h=out[offset:e].split();assert h[-1]!=b'missing';size=int(h[-1]);offset=e+1;blob=out[offset:offset+size];offset+=size+1;live=Path(q).read_bytes();assert (blob==live if q.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),q
 gitrows.append(dict(d(q),git_raw_sha256=sha(blob),git_lf_sha256=sha(blob.replace(b'\r\n',b'\n')),raw_exact=blob==live))
evidence=put(R/'repository-seal.bindings.json',dict(checked_commit=C,verified_proof_commit=P,prior_exact_Git_inputs=441,prior_raw_unchanged=unchanged,declared_administrative_successors=drifts,original39_math_whole70_unchanged=True,whole_math_review=d(R/'whole-proof-review/math.review.json'),verified_receipt=d(R/'verified.json'),changed_files=changes,exact_shared_Git_inputs=gitrows,root_imports=imports,Registry_leaf_count=485,technical_registry_single_actual_append=True,ledger_only_independent_VERIFIED_append=True,handoff_original_lines_retained=True,companion_execution_only_changed_paths=exchanges,integration=d(R/'integration.json'),source_current_binding_sha256=audit['publication_binding_sha256'],source_review_run_sha256=source['review_run_sha256'],decoder_RAW_run_sha256=prior['decoder_run_sha256'],source108_current_files_not_all_claimed_unchanged=True,graph=dict(raw=d('_site/data/underlying-lean-graph.json'),publication_inputs_sha256=graph['publication_inputs_sha256'],node_count=len(graph['nodes']),edge_count=len(graph['edges']),actual_branch=integration['structural_branch'],graph_report=gc),generated_site_stamp=site['git'],historical_generated_gate_stamp=site['gate'],fake_scan=dict(status='PASS',files=len(files),hits=0),private_owner_coverage=coverage,named_standard_axioms_reused=verified['named_standard_axioms'],static_reader=dict(branch=d(fs),page=d(page),seven_formula_steps=True,folded_public_Lean_exact=True,full_Test_copy_download_browser_live_certified=False)))
mandatory=dict(reused_current_shared_root_gate=True,command=['python','tools/astis.py','check'],working_head_at_execution=P,checked_committed_shared_source=C,actual_root_jobs=9147,actual_Test_jobs=9423,status=pin(integration['checks'][0]['status']),raw_log=pin(integration['checks'][0]['log']),root_foreground_lease=d(R/'root.integration.lease.json'),why_no_repeat='Exact committed shared imports/Registry/Tests and production match the just completed foreground root gate. Prior complete mathematics/source and focused/direct proofs unchanged. Independent fresh current metadata/source/fake/graph checks performed.',independent_compiler_started=False)
seal=dict(schema_version=1,status='accepted-scoped',verification_status='passed-scoped',checked_commit=C,verifier_id=V,seal_kind='repository ProofSeal41',verified_proof_commit=P,previous_independent_verification=d(R/'verified.json'),fresh_metadata_source_gates=g,required_repository_Lean_gate=mandatory,raw_LF_Git_inputs=evidence,scope='Actual compact finite-dimensional real Hilbert stdGaussian LSI2, signed/rank0/zero functions and actual32 cutoff consumer; genuine shared root/Test imports and Registry485 now accepted. All math/source/blind/seal/publication bindings unchanged; one private energy provider owner-covered. No new mathematical credit.',remaining_boundary=['Noncompact exhaustion/coherent33 KL/Fisher, Gaussian T2/FIRST4.6, both papers main/error/work/cost/composition remain open.','Static seven formula steps/folded actual public Lean and current structural graph accepted only; full Test/source/copy/download/bundles/rendered/browser/Exposition/PURIFIED/live remain open.','Generated-site precommit8c445+dirty and historical gate stamp recorded honestly. Exact remoteCI is a separate single snapshot; no merge/deployment/live claim.','No VERIFIED duplication/newSTABILIZING/canonical modification.'],canonical_mutations=False,leases=dict(read='CLOSED',write='CLOSED',compiler='NOT_STARTED_CLOSED',Python='CLOSED'),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
saved=put(R/'repository-seal.ProofSeal.json',seal);basis=dict(actor=V,checked_commit=C,parent_proof_commit=P,gates=d(R/'repository-seal.gates.json'),bindings=evidence,ProofSeal=saved,status='CLOSED');run=put(R/'repository-seal.run.json',dict(basis,deterministic_run_sha256=pub.digest(basis)))
lp=R/'repository-seal.lease.json';opening=R/'repository-seal.lease.open.raw.snapshot.json';assert not opening.exists();opening.write_bytes(lp.read_bytes());lp.write_bytes((json.dumps(dict(status='CLOSED',checked_commit=C,verifier_id=V,read='CLOSED',write='CLOSED',compiler='NOT_STARTED_CLOSED',Python='CLOSED',initial_manifest=d(opening),receipt=saved,run=run),indent=2)+'\n').encode())
print(json.dumps(dict(status='accepted-scoped',checked_commit=C,receipt=saved,shared_Git_inputs=len(gitrows),fake_files=len(files),fake_hits=0,all_leases='CLOSED',canonical_mutations=False),indent=2))
