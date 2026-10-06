import json,hashlib,subprocess,re,sys,datetime
from pathlib import Path
sys.path.insert(0,'tools')
import astis,astis_publication as pub,astis_advance as adv,publication_reader
R=Path('runs/20261007-companion-priority/gaussian-sharp-concentration')
C='c0696fcc0fcfbd67eed79ad6e965260647ccbf66'
P='2f4e0ba92d7233f07e93822897d2d275da46799e';V='picard_commit_verifier_20261005'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def read(p):return json.loads(Path(p).read_bytes())
def fp(p):
 b=Path(p).read_bytes();return dict(path=str(p).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b))
def verify(x):
 y=fp(x['path'])
 for k in ['raw_sha256','lf_sha256','bytes']:
  if k in x:assert x[k]==y[k],(x['path'],k)
 return y
def git(*args):return subprocess.check_output(['git',*args])
def delta(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):return sum([delta(a.get(k),b.get(k),p+'/'+k) for k in sorted(set(a)|set(b))],[])
 return [] if a==b else [dict(path=p,before=a,after=b)]
def emit(n,d):
 p=R/n;b=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists():assert p.read_bytes()==b,str(p)
 else:p.write_bytes(b)
 return fp(p)
assert git('rev-parse','HEAD').decode().strip()==C
assert git('rev-parse',C+'^').decode().strip()==P
assert not git('diff','--name-only').strip()
vr=read(R/'verified.json');m=read(R/'whole-math-review.json');claim=read(R/'claim.json');plan=read(R/'publication-plan.json');integration=read(R/'integration.json')
assert fp(R/'verified.json')['raw_sha256']=='d648f1b40e7bf103cdcc4a9720b48d3e38dec92adde8119f88fd12108ffc6bb1'
assert vr['verified_commit']==P and vr['verification_status']=='passed-scoped'
assert integration['verified_proof_commit']==integration['checked_working_head']==P
assert sha((R/'whole-math-review.json').read_bytes())=='a38785c2e632ea049e1e5d0621bc6523f8538af3ead7fd37a9684a02aa78754f'
assert integration['toolchain']==Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()==integration['mathlib_commit']=='db584cd6d46c92f209a44c0f1c829460d327499d'
stable=set(claim['lean_files']+claim['test_files'])
for s in vr['source_reviews']:
 for k in ['review','packet','whole_module']:verify(s[k]);stable.add(s[k]['path'])
for x in read(R/'math-freeze.exposition-repaired.json')['inputs']:verify(x);stable.add(x['path'])
for x in read(R/'reviewer.math.dependencies.json')['files']+read(R/'reviewer.math.dependencies.supplement.json'):verify(x)
for p in stable:assert lf(git('show',f'{P}:{p}'))==lf(Path(p).read_bytes()),p
changed=git('diff','--name-only',P,C).decode().splitlines()
lean=[p for p in changed if p.endswith('.lean')]
expected=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean']
assert set(lean)==set(expected)
for p in ['AutoSamplingTheory/TechnicalLemmas/Probability.lean','Tests.lean','AutoSamplingTheory/ExampleCases.lean']:
 assert lf(Path(p).read_bytes())==lf(git('show',f'{P}:{p}'))
oldbasic=lf(git('show',f'{P}:Tests/Basic.lean'))
assert lf(Path('Tests/Basic.lean').read_bytes())==oldbasic.replace(b'formalizedTechnicalLemmaCount = 473',b'formalizedTechnicalLemmaCount = 474',1)
regpath='AutoSamplingTheory/TechnicalLemmas/Registry.lean';reg=Path(regpath).read_text(encoding='utf8');oldreg=lf(git('show',f'{P}:{regpath}')).decode()
entry=re.search(r'  \{\n    key := "gaussian.lipschitz.sharp-standard-mgf".*?\n  \},\n',reg,re.S).group()
assert reg.replace(entry,'',1)==oldreg
assert plan['mathematical_declarations'][0] in entry and 'LemmaMemoryStatus.formalizedLocal' in entry
assert 'No Gaussian LSI/T2' in entry
mem='research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl'
oldmem=lf(git('show',f'{P}:{mem}'));newmem=lf(Path(mem).read_bytes());assert newmem.startswith(oldmem)
rows=newmem[len(oldmem):].splitlines();assert len(rows)==1
row=json.loads(rows[0]);assert row['local_decl']==plan['mathematical_declarations'][0] and row['verified_commit']==P and row['status']=='formalized-local'
for p in changed:
 assert not p.startswith(('tools/','website/content/declaration_lessons/','website/content/publications/','research-wiki/semantic-roundtrip/audits/'))
 assert p not in ['lean-toolchain','lake-manifest.json','lakefile.lean']
checks=[]
for x in integration['checks']:
 assert x['exit_code']==0 and sha(Path(x['log']).read_bytes())==x['raw_sha256']
 checks.append(dict(name=x['name'],fingerprint=fp(x['log']),exit_code=0))
rootagg=Path(integration['checks'][0]['log']).read_text(encoding='utf8')
fresh=read(R/'reviewer.repository.aggregate.result.json');assert fresh['checked_commit']==C and fresh['returncode']==0
assert sha(Path(fresh['log']).read_bytes())==fresh['raw_sha256']
agg=Path(fresh['log']).read_text(encoding='utf8')
for text in [rootagg,agg]:
 assert 'Build completed successfully (9133 jobs)' in text and 'Build completed successfully (9396 jobs)' in text and 'ASTIS check passed' in text
 assert not re.search(r'^error:',text,re.M)
markers={'publication':'Publication PASS: 190','semantic':'256 audits, 8 repair','frontier-integrated':'253 registered cells','contributor-integrated':'affected declarations=73; changed cells=69','process-memory-integrated':'passed','site-build':'474 compiled local leaves, 864 modules, 4544 declarations','site-check':'864 modules, 4544 declarations'}
for n,s in markers.items():assert s in Path(next(x['log'] for x in integration['checks'] if x['name']==n)).read_text(encoding='utf8'),n
sitefail=read(R/'site-domain-object-repair.json');failed=Path(sitefail['failed_log']);assert failed.exists() and sitefail['new_object']=='concept:probability'
assert "ValueError: Cross-domain contract invariant failed" in failed.read_text(encoding='utf8')
assert "set(edge['tails'] + edge['heads']) <= ids" in failed.read_text(encoding='utf8')
pub.check_advance(vr['publication_declarations']+vr['metadata_only_revalidation'],reviewed=True);data=pub.inputs();sources=[]
for s in vr['source_reviews']:
 item,b=next((i,b) for i in pub.load() for b in i['bindings'] if b['declaration']==s['declaration'])
 a=data['audits'][s['audit_id']];assert a['state']==a['source_review']['state']=='accepted'
 assert pub.binding_digest(item,b,data)==s['publication_binding_sha256']
 assert pub.digest(pub.review_context(item,b,data))==s['review_context_sha256']
 assert a['source_review']['review_run_sha256']==s['review_run_sha256']
 ap='research-wiki/semantic-roundtrip/audits/'+s['audit_id']+'.json';stable.add(ap)
 assert lf(Path(ap).read_bytes())==lf(git('show',f'{P}:{ap}'))
 sources.append(dict(declaration=s['declaration'],mathematical_credit=s['mathematical_credit'],audit_id=s['audit_id'],current_binding=s['publication_binding_sha256'],review_context_sha256=s['review_context_sha256'],review_run_sha256=s['review_run_sha256'],whole_module=s['whole_module'],decoder=s['decoder'],decoder_run_sha256=s['decoder_run_sha256']))
admin=[]
for i,cid in enumerate(plan['active_cells']):
 p=Path('research-wiki/frontier-cells')/(cid+'.json');old=read(R/f'reviewer.exact.cell{i}.before-verification.raw.snapshot.json');cur=read(p)
 assert old==json.loads(git('show',f'{P}:{p.as_posix()}'))
 differences=delta(old,cur)
 allowed=['/status','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review']
 assert all(x['path'] in allowed for x in differences)
 assert cur['status']=='independently_verified' and isinstance(cur['evidence']['independent_verification'],str)
 assert cur['evidence']['independent_verification_details']['verified_commit']==P
 assert cur['evidence']['integration_receipt']==(R/'integration.json').as_posix()
 assert cur.get('version_history')==old.get('version_history')
 snap=R/f'reviewer.repository.cell{i}.raw.snapshot.json'
 if snap.exists():assert snap.read_bytes()==p.read_bytes()
 else:snap.write_bytes(p.read_bytes())
 admin.append(dict(cell=cid,changes=differences,current=fp(p),raw_snapshot=fp(snap)))
graphpath=Path('_site/data/underlying-lean-graph.json');g=read(graphpath)
assert g['publication_inputs_sha256']==publication_reader.graph_input_digest()
assert len(g['nodes'])==2097 and len(g['edges'])==5485
assert integration['cell_metadata_frozen_before_final_graph'] is True
greports=[]
for i,cid in enumerate(plan['active_cells']):
 current=pub.graph_report(cid,Path('_site'));assert current==read(R/f'graph.{i}.json')==integration['graph_checks'][i];greports.append(current)
edges={(e['source'],e['target'],e['relation']) for e in g['edges']}
for target in plan['mathematical_declarations']:
 module=target.rsplit('.',1)[0];assert ('module:'+module,'decl:'+target,'declares') in edges
leaf='AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential';consumer='AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FullRangeProximalGaussianOracle'
for a,b in [(leaf,consumer),(leaf,'AutoSamplingTheory.TechnicalLemmas.Probability'),(leaf,'Tests.GaussianLipschitzExponential'),('Tests.GaussianLipschitzExponential','Tests')]:assert ('module:'+a,'module:'+b,'imports') in edges
functor=read('website/content/functor_hypergraph.json');memory=read('website/content/graph_memory_index.json');proposal=read(R/'conceptual-mirror.gaussian-symmetry.repaired.proposal.json');review=read(R/'conceptual-mirror.gaussian-symmetry.repaired.review.json')
bid='transport:gaussian-symmetry-pushforward';fid='family:gaussian-law-symmetry'
bridge=next(x for x in functor['hyperedges'] if x['id']==bid);family=next(x for x in memory['families'] if x['id']==fid)
assert bridge['formal_refs']==[] and bridge['status']=='not-Lean-certified'
assert bridge['review']['status']=='independently-reviewed' and bridge['review']['review_raw_sha256']==sha((R/'conceptual-mirror.gaussian-symmetry.repaired.review.json').read_bytes())
assert family['compiled_substrate_bindings']==[] and family['functor_edges']==[bid]
assert bridge['review']['independent_reviewer']==review['reviewer'] and review['independent_of_creator']
for k in ['formula','mechanism','hypothesis_map','conclusion_map','failure_boundary','source_ids']:assert bridge[k]==proposal['metadata'][k],k
discovery=adv.current_discoveries()[review['discovery_id']]
assert discovery['status']=='merged'
assert 'not Git PR merge or formal theorem implication' in discovery['latest_note']
old_disc=lf(git('show',f'{P}:runs/substantive_discoveries.jsonl'));new_disc=lf(Path('runs/substantive_discoveries.jsonl').read_bytes())
assert new_disc.startswith(old_disc)
added_disc=new_disc[len(old_disc):].splitlines();assert len(added_disc)==1
assert json.loads(added_disc[0])['discovery_id']==review['discovery_id']
assert any(x.get('discovery_id')==review['discovery_id'] and x.get('to_status')=='validated' for x in [json.loads(t) for t in old_disc.splitlines()])
mirror_edges=[e for e in g['edges'] if e['source']==bid or e['target']==bid]
assert len(mirror_edges)==5
assert all(e['relation'] in ['joint conceptual input','conditional conceptual output','reuse search candidate; not a proof dependency'] for e in mirror_edges)
assert not any(e['relation'] in ['imports','declares','depends on'] for e in mirror_edges)
oldfun=json.loads(git('show',f'{P}:website/content/functor_hypergraph.json'))
assert len(functor['objects'])==len(oldfun['objects'])+1==8
assert [x for x in functor['objects'] if x['id']!='concept:probability']==oldfun['objects']
beforeobj=read(R/'functor.before-domain-object.raw.snapshot.json')
assert [x for x in functor['objects'] if x['id']!='concept:probability']==beforeobj['objects']
assert functor['hyperedges']==beforeobj['hyperedges']
html=Path(integration['reader_inspection']['path']).read_text(encoding='utf8')
for target in plan['mathematical_declarations']:assert 'data-authored-declaration="'+target+'"' in html
allfiles=astis.lean_source_files();hits=[]
for p in allfiles:
 for n,line in enumerate(astis.strip_lean_comments_and_strings(p.read_text(encoding='utf8')).splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):hits.append(dict(path=str(p),line=n,text=line))
assert not hits and len(allfiles)==864
assert adv.current_advances()[claim['advance_id']]['state']=='VERIFIED'
assert [k for k,x in adv.current_advances().items() if x['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
paths=set(git('ls-files','-z',R.as_posix()).decode().split('\0'));paths.discard('')
paths.update(stable);paths.update(expected);paths.update(changed)
paths.update(x['path'] for x in read(R/'reviewer.exact.source-binding.json')['source_inputs'] if not x['path'].startswith('.lake/'))
paths.update(git('ls-files','-z','runs/20261007-companion-priority/anonymous-decoder-30').decode().split('\0'));paths.discard('')
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);gitrecords=[]
for p in sorted(paths):
 proc.stdin.write(f'{C}:{p}\n'.encode());proc.stdin.flush();hdr=proc.stdout.readline().decode().split();assert hdr[1]=='blob',p
 blob=proc.stdout.read(int(hdr[2]));assert proc.stdout.read(1)==b'\n';b=Path(p).read_bytes();raw=p.startswith('runs/') and p not in ['runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl']
 assert blob==b if raw else lf(blob)==lf(b),p
 gitrecords.append(dict(path=p,git_blob_sha256=sha(blob),current=fp(p),raw_exact_required=raw))
proc.stdin.close();assert proc.wait()==0
assert git('rev-parse','HEAD').decode().strip()==C and not git('diff','--name-only').strip()
graphsnap=R/'reviewer.repository.current-graph.raw.snapshot.json';assert not graphsnap.exists();graphsnap.write_bytes(graphpath.read_bytes())
result=dict(schema_version=1,status='accepted-scoped',verification_status='passed-scoped',checked_commit=C,repository_commit=C,verified_proof_commit=P,verifier_id=V,owner_is_not_verifier=True,scope='Packet30 canonical sharp Gaussian Lipschitz centered MGF and same actual allpositive proximal Gaussian-gradient-output oracle: independent current repository ProofSeal only',exact_verification_reused=fp(R/'verified.json'),whole_math_review_reused=fp(R/'whole-math-review.json'),math_comment_overlay_reused=fp(R/'source.repair.overlay-review.json'),production_Test_signature_lessons_publications_audits_unchanged=True,shared_Lean_delta=dict(files=expected,imports='Existing canonical imports reused unchanged',Registry='Exactly one real independently VERIFIED sharp concentration leaf; count474',Basic='Only registry count473->474'),registry_memory_row=row,gate=dict(independent_fresh_complete_astis_gate=fresh,authoritative_root_logs=checks,root_jobs=9133,Tests_jobs=9396,current_cached_rebuild_run=True,whole_math_source_replay=False,standard_axioms_target_scope_reused=vr['standard_axioms'],full_repository_native_decide_scope_not_claimed_standard3_only=True),metadata_gate_counts=integration['metadata_checks'],source_bindings_current=sources,reviewed_publication_true='PASS exact two mathematical and unchanged domain metadata-only revalidation targets',cell_admin_reconciliation=admin,graph=dict(raw_current=fp(graphpath),raw_snapshot=fp(graphsnap),publication_inputs_sha256=g['publication_inputs_sha256'],nodes=len(g['nodes']),edges=len(g['edges']),bounded_current_reports=greports,actual_import_declaration_edges_checked=True,conceptual_bridge=dict(bridge_id=bid,family_id=fid,review=fp(R/'conceptual-mirror.gaussian-symmetry.repaired.review.json'),formal_refs=[],no_solid_Lean_implication_or_certified_functor=True,actual_edges=mirror_edges),static_reader_targets_present=True,rendered_visual_QA='Open; this seal is static/compiler/source-bound only'),site_failure_chain=dict(diagnostic=fp(R/'site-domain-object-repair.json'),failed_raw_log=fp(failed),preserved_before_raw_snapshot=fp(R/'functor.before-domain-object.raw.snapshot.json'),repair='Exactly missing eighth concept:probability object; bridge hypotheses/formula/review unchanged; renderer explicitly distinguishes independent source review from formal transport',successful_site_build=fp(R/'site-build.1.log')),fake_closure_scan=dict(canonical_files=len(allfiles),scanner='astis comment/string-stripped FORBIDDEN_REGEX',hits=hits),Git_evidence=dict(files=len(gitrecords),raw_artifacts=sum(x['raw_exact_required'] for x in gitrecords),records=gitrecords),remaining_boundary=['Actual sharp (4.3) with own Gaussian-gradient-output mean and retained (4.4)-(4.5) only; no smoothedgradient mean identity/bias (4.2), first W2 in (4.6)/LSI/T2/full Lemma4.2, RGO/HMC substitution, higher sampling bounds, PBPS dynamics/cost, mains or composition. TV proximity cannot transport unbounded expected cost.','Current repository aggregate/source/fake/graph gates accepted here. ExpositionSeal/postmerge PURIFIED/rendered QA/CopyDownload/current-head remote CI/merge/live are separately open.','Future source31 untracked preproof inputs excluded; no claim/API/implementation/completion credit from this packet30 seal.'],root_stale_pending_prose_not_promoted_to_actual_status=True,sole_stabilization_owner_preserved=True,permitted_writes='Own reviewer.repository.* receipts/snapshots/logs only; no production/cells/ledger/audits/site writes',leases=dict(compiler='CLOSED: independent foreground astis gate terminal0',read='CLOSED',write='CLOSED after owned receipt',Python_sessions='CLOSED'),created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
out=emit('reviewer.repository.ProofSeal.json',result)
run=emit('reviewer.repository.run.json',dict(status='passed-scoped',checked_commit=C,verified_proof_commit=P,verifier_id=V,ProofSeal=out,independent_complete_astis_gate=fresh,raw_frozen_graph=fp(graphsnap),Git_files=len(gitrecords),raw_artifacts=sum(x['raw_exact_required'] for x in gitrecords),canonical_fake_files=len(allfiles),current_source_targets=len(sources),current_graph_nodes=len(g['nodes']),current_graph_edges=len(g['edges']),leases='CLOSED'))
emit('reviewer.repository.lease.json',dict(status='CLOSED',checked_commit=C,read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',Python_sessions='CLOSED',ProofSeal=out,run=run,production_shared_cell_audit_ledger_site_writes=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
print(json.dumps(dict(status='accepted-scoped',checked_commit=C,ProofSeal=out,run=run,Git_files=len(gitrecords),raw_artifacts=sum(x['raw_exact_required'] for x in gitrecords),canonical_fake_files=len(allfiles),leases='CLOSED')))
