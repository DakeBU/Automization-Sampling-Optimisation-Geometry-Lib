from pathlib import Path
import json,hashlib,subprocess,sys,re,datetime
sys.path.insert(0,'tools')
import astis_publication as pub,astis_advance as advance,astis,publication_reader
R=Path('runs/20261007-companion-priority/gaussian-compact-entropy');C='11d72a92db9366586f006ed22a4a78db37e7bb1c';P='421496a5de7355830c0b4904ea10f33722ed3602';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def pin(row):
 x=d(row['path']);assert x['raw_sha256']==row['raw_sha256'],(x,row)
 if 'lf_sha256' in row:assert x['lf_sha256']==row['lf_sha256'],(x,row)
 return x
def put(p,x):
 assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
def old(p):return subprocess.check_output(['git','show',P+':'+p])
def dif(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else dif(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):return [p] if len(a)!=len(b) else [q for i,(x,y) in enumerate(zip(a,b)) for q in dif(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==P
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
g=j(R/'reviewer.repository.gates.json');assert g['checked_commit']==C and len(g['results'])==6 and g['compiler']=='CLOSED'
for row in g['results']:assert row['returncode']==0;pin(row)
assert re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.repository.aggregate.log').read_text(encoding='utf-8'))==['9142','9413']
assert 'ASTIS check passed' in (R/'reviewer.repository.aggregate.log').read_text(encoding='utf-8')
prior=j(R/'reviewer.exact.bindings.json');verified=j(R/'verified.json');assert verified['verified_commit']==P and verified['verification_status']=='passed-scoped'
assert d(R/'verified.json')['raw_sha256']=='8e3fddc67db664544d2522062161f9ecf86ed57d822699faf21321ab7426ec3b'
admin=[];unchanged=0
for row in prior['exact_currentGit_inputs']:
 if d(row['path'])['raw_sha256']==row['raw_sha256']:unchanged+=1;continue
 assert row['path']=='research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-compact-entropy.json'
 before=json.loads(old(row['path']));now=j(row['path']);changes=dif(before,now)
 assert set(changes)=={'/status','/evidence/execution_boundary','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review','/purification/dead_code_audit'}
 assert before['status']=='proved_locally' and now['status']=='independently_verified' and now['purification']['status']=='pending'
 assert now['evidence']['independent_verification']==(R/'verified.json').as_posix() and isinstance(now['evidence']['independent_verification'],str)
 assert now['evidence']['independent_verification_details']['verified_commit']==P
 bs=R/'reviewer.repository.cell.before.GitLF.snapshot.json';ns=R/'reviewer.repository.cell.current.raw.snapshot.json';assert not bs.exists() and not ns.exists();bs.write_bytes(old(row['path']));ns.write_bytes(Path(row['path']).read_bytes())
 admin.append({'exact_pointers':changes,'before_GitLF':d(bs),'current_raw':d(ns),'statement_source_parents_and_binding_unchanged':True})
assert unchanged==351 and len(admin)==1
math=j(R/'whole-proof-review/math.review.json');pin(math['input_bindings']);bindings=j(math['input_bindings']['path']);assert len(bindings['inputs'])==36
for row in bindings['inputs']:pin(row)
freeze=j(R/'math-freeze.json');assert len(freeze['inputs'])==22
for row in freeze['inputs']:pin(row)
plan=j(R/'publication-plan.json');decls=plan['mathematical_declarations'];pub.check_advance(decls,reviewed=True)
state=advance.current_advances();assert state[verified['advance_id']]['state']=='VERIFIED' and state[verified['advance_id']]['latest_evidence']['verifier_id']==V
assert [k for k,v in state.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
data=pub.inputs();item=next(x for x in pub.load() if x['id']==plan['slugs'][0]);b=next(x for x in item['bindings'] if x['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]]
source=j(R/'source.0.review.json');packet=j(R/'source.0.reviewer-packet.json');assert pub.digest({k:v for k,v in source.items() if k!='review_run_sha256'})==source['review_run_sha256']
assert pub.binding_digest(item,b,data)==prior['source_binding_sha256']==source['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,b,data)==packet['candidate_publication_context'] and audit['source_review']['review_run_sha256']==prior['source_review_run_sha256'] and audit['state']=='accepted'
assert j(R/'anonymous-decoder/run.json')['decoder_run_sha256']==prior['decoder_run_sha256']
roots=['AutoSamplingTheory/TechnicalLemmas.lean','Tests.lean','Tests/Basic.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean'];added=[]
for p in roots[:2]:
 a=old(p).decode().splitlines();n=Path(p).read_text(encoding='utf-8').splitlines();assert all(x in n for x in a);added += [x for x in n if x not in a]
assert set(added)=={'import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy','import Tests.GaussianCompactEntropy'}
assert old(roots[2]).replace(b' = 479 :=',b' = 480 :=').replace(b'\r\n',b'\n')==Path(roots[2]).read_bytes().replace(b'\r\n',b'\n')
registry=Path(roots[3]).read_text(encoding='utf-8');oldreg=old(roots[3]).decode();assert registry.count('status := LemmaMemoryStatus.formalizedLocal')==oldreg.count('status := LemmaMemoryStatus.formalizedLocal')+1
assert registry.count('localDecl := "'+decls[0]+'"')==1
assert Path(freeze['inputs'][0]['path']).read_text(encoding='utf-8').splitlines()[0]=='import AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT'
assert not any('Bernoulli' in x for x in Path(freeze['inputs'][0]['path']).read_text(encoding='utf-8').splitlines() if x.startswith('import'))
technical='research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl';a=old(technical).decode().splitlines();n=Path(technical).read_text(encoding='utf-8').splitlines();assert n[:len(a)]==a and len(n)==len(a)+1
addedrow=json.loads(n[-1]);assert decls[0] in json.dumps(addedrow)
integration=j(R/'integration.json');assert integration['verified_proof_commit']==P and integration['aggregate_summary']=={'root_build_jobs':9142,'tests_build_jobs':9413,'registry_leaves':480}
for check in integration['checks']:
 pin(check['log'])
 if 'status' in check:pin(check['status']);assert j(check['status']['path'])['exit_code']==0
 else:assert check['exit_code']==0
assert re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'aggregate.log').read_text(encoding='utf-8'))==['9142','9413']
assert '480' in (R/'site-build.log').read_text(encoding='utf-8')
assert '12 chapters, 881 modules, 4664 declarations' in (R/'site-check.log').read_text(encoding='utf-8')
graph=j('_site/data/underlying-lean-graph.json');site=j('_site/data/site-data.json');assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
graphcheck=j(R/'graph.0.json');assert pub.graph_report(graphcheck['cell'],Path('_site'))==graphcheck==integration['graph_check']
assert {'source':'module:AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT','target':'module:AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy','relation':'imports'} in integration['structural_branch']
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files()
changed=subprocess.check_output(['git','diff','--name-only',P,C],text=True).splitlines();assert len(changed)==57
nonrun={p for p in changed if not p.startswith('runs/')};assert nonrun==set(roots)|{'docs/companion-papers-handoff.md','research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-compact-entropy.json',technical,'website/content/samplewiki_companion_frontiers.json'}
q=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=q.communicate(('\n'.join(C+':'+p for p in changed)+'\n').encode());assert q.returncode==0
offset=0;gitrows=[]
for p in changed:
 e=out.index(b'\n',offset);n=int(out[offset:e].split()[-1]);offset=e+1;blob=out[offset:offset+n];offset+=n+1;live=Path(p).read_bytes();raw=p.startswith('runs/')
 assert (blob==live if raw else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),p
 gitrows.append(dict(d(p),git_blob_sha256=sha(blob),mode='raw-exact' if raw else 'LF-exact'))
evidence=put(R/'reviewer.repository.bindings.json',{'checked_commit':C,'verified_proof_commit':P,'prior_independent_exact_evidence':d(R/'reviewer.exact.bindings.json'),'prior352_inputs_unchanged':351,'allowed_one_cell_admin_projection':admin,'whole_math36_bindings_unchanged':True,'original22_freeze_unchanged':True,'current_source_reviewed_binding_sha256':prior['source_binding_sha256'],'current_source_review_run_sha256':source['review_run_sha256'],'source_and_decoder_review_raw_bytes_preserved':True,'shared_imports':added,'Registry_actual_leaf_count':480,'TestsBasic_actual_count':480,'added_technical_registry':addedrow,'integration':d(R/'integration.json'),'root_static_checks_input_logs_hash_verified':True,'graph_report':d(R/'graph.0.json'),'current_graph_digest':graph['publication_inputs_sha256'],'current_graph_counts':graph['counts'],'all57_changed_Git_inputs':gitrows,'generated_site_inputs':[d('_site/data/underlying-lean-graph.json'),d('_site/data/site-data.json')],'generated_site_git_stamp':{'commit':site['git']['commit'],'dirty_files_count':len(site['git']['dirty_files']),'commit_published':site['git']['commit_published']},'generated_site_historical_gate_stamp':site['gate'],'fresh_canonical_fake_scan':{'files':len(files),'hits':0},'named_standard_axioms_reused_from_identical_compiled_proof':['propext','Classical.choice','Quot.sound'],'reader_delivery_boundary':integration['reader_inspection'],'source_scope':'Actual compact C2 observer/entropy limits; direct compiled actual35 parent only, no direct Bernoulli formal edge or new conceptual certificate.'})
scope={'schema_version':1,'status':'accepted-scoped','verification_status':'passed-scoped','checked_commit':C,'verifier_id':V,'seal_kind':'repository ProofSeal36','verified_proof_commit':P,'previous_independent_verification':d(R/'verified.json'),'fresh_repository_gates':g,'raw_LF_Git_inputs':evidence,'scope':'Same independently verified authored compact-C2 count/Gaussian L1 and successor observer/entropy limits now exercised through actual production/Test root imports and Registry480/Tests.Basic; exact source bindings, current structural graph and fresh whole-repository Lean/source/fake gates. No new mathematical proof credit or VERIFIED/STABILIZING transition.','remaining_boundary':['Fullflip-energy factor4, GaussianLSI, noncompact/Hilbert domain extension/T2/FIRST4.6 and both complete main results/composition/query costs remain open.','Full Test-inline/copy/download/browser/rendered/live delivery, independent ExpositionSeal and postmerge PURIFIED remain separate.','Exact11d remoteCI/mainmerge/live are not certified; committed prior a63 four-workflow receipt is historical evidence only.','Generated site truthfully records precommit421+dirty and an older unmatched historical gate stamp; fresh exact11d repository gates establish this scoped ProofSeal without relabelling generated metadata.','Future37 source-only untracked folders excluded from36 mathematical/source/repository credit.'],'canonical_mutations':False,'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED'},'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
receipt=put(R/'reviewer.repository.ProofSeal.json',scope)
runbasis={'actor':V,'checked_commit':C,'parent_proof_commit':P,'gates':d(R/'reviewer.repository.gates.json'),'bindings':evidence,'ProofSeal':receipt,'status':'CLOSED','scope':'repository36 only; independent exact proof/source review reused by unchanged bytes'}
run=put(R/'reviewer.repository.run.json',dict(runbasis,deterministic_run_sha256=pub.digest(runbasis),hash_recipe='pub.digest all fields except deterministic_run_sha256/hash_recipe'))
leasepath=R/'reviewer.repository.lease.json';initial=R/'reviewer.repository.lease.open.raw.snapshot.json';assert not initial.exists();initial.write_bytes(leasepath.read_bytes())
leasepath.write_bytes((json.dumps({'status':'CLOSED','checked_commit':C,'verifier_id':V,'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED','initial_manifest':d(initial),'receipt':receipt,'deterministic_run':run},ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':'accepted-scoped','checked_commit':C,'receipt':receipt,'all_leases':'CLOSED','canonical_mutations':False},ensure_ascii=False))
