import sys,json,hashlib,subprocess,re
from pathlib import Path
sys.path.insert(0,'tools')
import astis,astis_publication as pub,astis_site,publication_reader,astis_advance as adv
R=Path('runs/20261007-companion-priority/gaussian-laplace-domain')
C='f4be544df21b14a1fdc3376fab4d073ae6557aa2';P='1f746dc634b95f780b7f5bffe04c50f9bb4f21e3';V='picard_commit_verifier_20261005'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def read(p):return json.loads(Path(p).read_bytes())
def fp(p):
 b=Path(p).read_bytes();return dict(path=str(p).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b))
def verify(x):
 y=fp(x['path'])
 for k in ('raw_sha256','lf_sha256','bytes'):
  if k in x:assert x[k]==y[k],(y['path'],k)
 return y
def git(*args):return subprocess.check_output(['git',*args])
def delta(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):return sum([delta(a.get(k),b.get(k),path+'/'+k) for k in sorted(set(a)|set(b))],[])
 return [] if a==b else [dict(path=path,before=a,after=b)]
assert git('rev-parse','HEAD').decode().strip()==C
assert subprocess.run(['git','merge-base','--is-ancestor',P,C]).returncode==0
v=read(R/'verified.json');m=read(R/'whole-math-review.json');claim=read(R/'claim.json');integration=read(R/'integration.json')
assert fp(R/'verified.json')['raw_sha256']=='c8cb7260b2720c39aa78e84370287b28d480d536699be09b6dc69d082251552a'
assert fp(R/'whole-math-review.json')['raw_sha256']=='7e669c59a1ebe9a4f8ab48a47463b3ca6674afe7bbd823b770fc3c17835dd276'
assert v['verified_commit']==P and v['verification_status']=='passed-scoped' and integration['verified_proof_commit']==P
for x in m['frozen_inputs']+m['reachable_source_inputs']+m['pinned_API_inputs']+m['primary_raw_inputs']:verify(x)
changed=git('diff','--name-only',P,C).decode().splitlines()
lean=[p for p in changed if p.endswith('.lean')]
expected=['AutoSamplingTheory/TechnicalLemmas/Probability.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean']
assert set(lean)==set(expected)
for p,import_line in [('AutoSamplingTheory/TechnicalLemmas/Probability.lean','import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential\n'),('Tests.lean','import Tests.GaussianLipschitzExponential\n')]:
 old=git('show',f'{P}:{p}');assert lf(Path(p).read_bytes())==import_line.encode()+lf(old)
old=git('show',f'{P}:Tests/Basic.lean')
assert lf(Path('Tests/Basic.lean').read_bytes())==lf(old).replace(b'formalizedTechnicalLemmaCount = 472',b'formalizedTechnicalLemmaCount = 473',1)
registry=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text(encoding='utf-8')
old=git('show',f'{P}:AutoSamplingTheory/TechnicalLemmas/Registry.lean').decode()
entry=re.search(r'  \{\n    key := "gaussian.lipschitz.signed-exponential-domain".*?\n  \},\n',registry,re.S).group()
assert registry.replace(entry,'',1)==old.replace('\r\n','\n')
assert 'Lem maMemoryStatus' not in entry and 'LemmaMemoryStatus.formalizedLocal' in entry
assert claim['declarations'][0] in entry and 'Domain only: no sharp coefficient' in entry
registry_memory=Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl')
oldmem=git('show',f'{P}:{registry_memory.as_posix()}')
newmem=registry_memory.read_bytes();assert lf(newmem).startswith(lf(oldmem))
add=lf(newmem)[len(lf(oldmem)):].splitlines();assert len(add)==1
row=json.loads(add[0]);assert row['local_decl']==claim['declarations'][0] and row['verified_commit']==P and row['status']=='formalized-local'
for p in changed:
 assert not p.startswith(('tools/','website/content/declaration_lessons/','website/content/publications/','research-wiki/semantic-roundtrip/audits/'))
 assert p not in ('lean-toolchain','lake-manifest.json','lakefile.lean')

checks=[]
for check in integration['checks']:
 assert check['exit_code']==0 and sha(Path(check['log']).read_bytes())==check['raw_sha256']
 checks.append(fp(check['log']))
aggregate=Path(integration['checks'][0]['log']).read_text(encoding='utf-8')
assert 'Build completed successfully (9133 jobs)' in aggregate and 'Build completed successfully (9396 jobs)' in aggregate and 'ASTIS check passed' in aggregate
assert not re.search(r'^error:',aggregate,re.M)
diagnostic=read(R/'integration-registry-count-diagnostic.json')
assert sha(Path(diagnostic['failed_log']).read_bytes())==diagnostic['raw_sha256']
failed=Path(diagnostic['failed_log']).read_text(encoding='utf-8')
errors=[s for s in failed.splitlines() if s.startswith('error:')]
assert len(errors)==3 and 'Tests/Basic.lean:47' in errors[0] and 'native_decide' in errors[0]
assert 'Build completed successfully (9133 jobs)' in (R/'integration-basic-focused.log').read_text(encoding='utf-8')
markers={'publication':'Publication PASS: 189','semantic':'253 audits, 8 repair','frontier-integrated':'252 registered cells','process-memory-integrated':'passed','contributor-integrated':'affected declarations=72; changed cells=68','site-build':'864 modules, 4490 declarations','site-check':'864 modules, 4490 declarations'}
for name,marker in markers.items():assert marker in Path(next(c['log'] for c in integration['checks'] if c['name']==name)).read_text(encoding='utf-8')
pub.check_advance(claim['declarations'],reviewed=True);data=pub.inputs()
sources=read(R/'reviewer.exact.source-binding.json');source_checks=[]
for s in sources['source_reviews']:
 for key in ('review','reviewer_packet','whole_module','decoder_result'):verify(s[key])
 item,binding=next((i,b) for i in pub.load() for b in i['bindings'] if b['declaration']==s['declaration'])
 a=data['audits'][s['audit_id']];assert a['state']=='accepted' and a['source_review']['state']=='accepted'
 assert pub.binding_digest(item,binding,data)==s['publication_binding_sha256']
 assert pub.digest(pub.review_context(item,binding,data))==s['review_context_sha256']
 assert a['source_review']['review_run_sha256']==s['review_run_sha256']
 source_checks.append(dict(declaration=s['declaration'],audit_id=s['audit_id'],publication_binding_sha256=s['publication_binding_sha256'],review_run_sha256=s['review_run_sha256'],module=s['whole_module'],decoder_run_sha256=s['decoder_run_sha256']))
admin=[]
for i,cid in enumerate(claim['cells']):
 p=Path('research-wiki/frontier-cells')/(cid+'.json')
 before=json.loads(git('show',f'{P}:{p.as_posix()}'));current=read(p);changes=delta(before,current)
 allowed={'/status','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/evidence/source_range_disclosure','/graph_contribution/visual_review'}
 assert all(x['path'] in allowed for x in changes)
 assert current['status']=='independently_verified' and isinstance(current['evidence']['independent_verification'],str)
 assert current['evidence']['independent_verification_details']['verified_commit']==P
 assert current['evidence']['integration_receipt']==str(R/'integration.json').replace('\\','/')
 before_history=before.get('version_history');assert current.get('version_history')==before_history
 out=R/f'reviewer.repository.cell{i}.raw.snapshot.json';assert not out.exists();out.write_bytes(p.read_bytes())
 admin.append(dict(cell=cid,changes=changes,current=fp(p),raw_snapshot=fp(out)))
graphpath=Path('_site/data/underlying-lean-graph.json');graph=read(graphpath);sitepath=Path('_site/data/site-data.json');site=read(sitepath)
assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
assert len(graph['nodes'])==2091 and len(graph['edges'])==5470
assert integration['cell_metadata_frozen_before_final_graph'] is True
graphs=[]
for i,cid in enumerate(claim['cells']):
 live=pub.graph_report(cid,Path('_site'));saved=read(R/f'graph.{i}.json')
 assert live==saved==integration['graph_checks'][i]
 graphs.append(live)
edges={(e['source'],e['target'],e['relation']) for e in graph['edges']}
leaf='AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential'
consumer='AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FullRangeProximalGaussianOracle'
for a,b in [(leaf,consumer),(leaf,'AutoSamplingTheory.TechnicalLemmas.Probability'),(leaf,'Tests.GaussianLipschitzExponential'),('Tests.GaussianLipschitzExponential','Tests')]:
 assert ('module:'+a,'module:'+b,'imports') in edges
assert ('module:'+leaf,'decl:'+claim['declarations'][0],'declares') in edges
assert ('module:'+consumer,'decl:'+claim['declarations'][1],'declares') in edges
html=Path(integration['reader_inspection']['path']).read_text(encoding='utf-8')
for name in claim['declarations']:assert 'data-authored-declaration="'+name+'"' in html
files=astis.lean_source_files();hits=[]
for p in files:
 for n,line in enumerate(astis.strip_lean_comments_and_strings(p.read_text(encoding='utf-8')).splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):hits.append(dict(path=str(p),line=n,text=line))
assert not hits
assert adv.current_advances()[claim['advance_id']]['state']=='VERIFIED'
assert [k for k,x in adv.current_advances().items() if x['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
# Exact Git blobs bind all immutable current run evidence, including failed logs and raw snapshots.
paths=set(git('ls-files','-z',str(R)).decode().split('\0'));paths.discard('')
paths.update(claim['lean_files']+claim['test_files']+expected)
paths.update(s['path'] for s in sources['source_union'] if not s['path'].startswith('.lake/'))
paths.update(git('ls-files','-z','runs/20261007-companion-priority/anonymous-decoder-29').decode().split('\0'));paths.discard('')
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);raw=0
git_evidence=[]
for p in sorted(paths):
 proc.stdin.write(f'{C}:{p}\n'.encode());proc.stdin.flush();header=proc.stdout.readline().decode().split();assert header[1]=='blob',p
 blob=proc.stdout.read(int(header[2]));assert proc.stdout.read(1)==b'\n';b=Path(p).read_bytes()
 israw=p.startswith('runs/');raw+=int(israw)
 assert (blob==b if israw else lf(blob)==lf(b)),p
 git_evidence.append(dict(path=p,git_raw_sha256=sha(blob),working=fp(p),raw_required=israw))
proc.stdin.close();assert proc.wait()==0
assert git('rev-parse','HEAD').decode().strip()==C
assert not git('diff','--name-only').strip()
out=R/'repository-proof-seal.json';assert not out.exists()
result=dict(schema_version=1,status='accepted-scoped',verification_status='passed-scoped',checked_commit=C,repository_commit=C,verified_proof_commit=P,verifier_id=V,owner_is_not_verifier=True,scope='Packet29 necessary Gaussian Laplace-domain producer and same actual proximal/Gaussian-output consumer, repository integration only',mathematical_review_reused=fp(R/'whole-math-review.json'),exact_verification_reused=fp(R/'verified.json'),production_Test_signature_lessons_publication_audits_math_unchanged=True,shared_Lean_delta=dict(files=expected,imports='Exactly two new import lines',Registry='Exactly one true independently verified formalizedLocal domain entry',Basic='Only registry count472->473; all original examples retained'),registry_memory_row=row,
 gate=dict(authoritative_complete_aggregate=checks[0],root_jobs=9133,Tests_jobs=9396,no_independent_compiler_or_rebuild=True,metadata_logs=checks[1:],failed_attempt_preserved=dict(diagnostic=fp(R/'integration-registry-count-diagnostic.json'),failed_log=fp(Path(diagnostic['failed_log'])),specific_error=errors,focused_Basic_repair=fp(R/'integration-basic-focused.log')),target_standard_axioms_reused=v['standard_axioms']),
 source_bindings_current=source_checks,publication_reviewed_true='passed current exact targets',cell_admin_reconciliation=admin,graph=dict(current=fp(graphpath),site_inventory=fp(sitepath),canonical_publication_inputs_sha256=graph['publication_inputs_sha256'],nodes=2091,edges=5470,current_bounded_checks=graphs,real_new_import_edges_checked=True,static_reader_targets_checked=True,rendered_visual_QA='open; static only'),fake_closure_scan=dict(canonical_files=len(files),hits=hits,scanner='Canonical comments/strings stripped astis.FORBIDDEN_REGEX'),Git_evidence=dict(files=len(paths),immutable_raw_artifacts=raw,records=git_evidence),metadata_gate_counts=integration['metadata_checks'],
 remaining_boundary=['Actual first Bochner moment and signed directional centered exponential L1 only. Sharp eta*norm(u)^2/2 MGF, bias, FIRST W2/LSI/T2/fullLemma4.2, posterior jointkernel/higher smoothing/Picard/Wp/warmness/initialization/main/querycost/composition remain open.','No ExpositionSeal/PURIFIED, Copy/Download controls, rendered visual QA, own-head remote CI, merge or live deployment acceptance from this repository ProofSeal.','Packet30 untracked preproof-only inputs excluded; no future mathematical/API search/implementation/completion credit.','Previous28 remote CI in this shared commit is historical exact previous-head evidence only, not current29 CI.'],original_stabilization_owner_preserved=True,permitted_writes='Own repository evidence only; no cells/ledger/shared/source changes',leases=dict(compiler='CLOSED; no compiler started',sessions='CLOSED',read='CLOSED',write='CLOSED after receipt'))
out.write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(status='accepted-scoped',checked_commit=C,receipt=fp(out),canonical_fake_files=len(files),Git_files=len(paths),raw_artifacts=raw,leases='CLOSED')))
