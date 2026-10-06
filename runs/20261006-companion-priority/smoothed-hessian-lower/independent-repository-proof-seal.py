import pathlib,json,hashlib,subprocess,sys,datetime,re
sys.path.insert(0,'tools')
import astis,astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
R=pathlib.Path('runs/20261006-companion-priority/smoothed-hessian-lower')
C='c61471ea83188f7959c6b0b9966803f967d4db84';B='d8f540f5b4409387b839f7ccfb50fd3297af4c70';V='picard_commit_verifier_20261005'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def F(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':p.as_posix(),'raw_sha256':H(b),'lf_sha256':H(LF(b)),'bytes':len(b)}
def J(p):return json.loads(pathlib.Path(p).read_text(encoding='utf8'))
def G(args):return subprocess.check_output(['git']+args)
def W(p,x):pathlib.Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def diff(a,b,p=''):
 if type(a)!=type(b):return [{'field':p,'before':a,'after':b}]
 if isinstance(a,dict):return sum([diff(a.get(k),b.get(k),p+'/'+k)for k in sorted(set(a)|set(b))],[])
 if isinstance(a,list):
  if len(a)!=len(b):return [{'field':p,'before':a,'after':b}]
  return sum([diff(x,y,p+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))],[])
 return [] if a==b else [{'field':p,'before':a,'after':b}]
assert G(['rev-parse','HEAD']).decode().strip()==C
assert G(['rev-parse',C+'^']).decode().strip()==B
m=J(R/'math-review.json');v=J(R/'verified.json');i=J(R/'integration.json');cl=J(R/'claim.json');ex=J(R/'exact-admission-reconciliation.json')
assert v['verified_commit']==B and v['verification_status']=='passed-scoped'
assert i['verified_proof_commit']==i['checked_working_head']==B
files=G(['diff','--name-only',B,C]).decode().splitlines()
sh={
'AutoSamplingTheory/ExampleCases.lean':'import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianBounds',
'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities.lean':'import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsLinearCovarianceUpper',
'Tests.lean':'import Tests.SmoothedHessianBounds'}
assert sorted(p for p in files if p.endswith('.lean'))==sorted(sh)
imports=[]
for p,line in sh.items():
 before=G(['show',B+':'+p]);after=G(['show',C+':'+p]);assert LF(after)==line.encode()+b'\n'+LF(before)
 assert LF(pathlib.Path(p).read_bytes())==LF(after)
 snap=R/('repository-proof-seal.'+pathlib.Path(p).name+'.input.raw.snapshot')
 assert not snap.exists();snap.write_bytes(pathlib.Path(p).read_bytes())
 imports.append({'path':p,'only_new_line':line,'current':F(p),'before_git_raw_sha256':H(before),'current_git_raw_sha256':H(after),'current_git_LF_sha256':H(LF(after)),'current_raw_snapshot':F(snap)})
stable=[]
for q in m['frozen_inputs']:
 f=F(q['path']);assert all(f[k]==q[k] for k in ['raw_sha256','lf_sha256']),q['path']
 assert pathlib.Path(q['path']).read_bytes()==pathlib.Path(q['snapshot']['path']).read_bytes()
 stable.append(f)
assert len(stable)==54
for p in cl['lean_files']+['Tests/SmoothedHessianBounds.lean','website/content/declaration_lessons/gibbs-linear-covariance-upper.json','website/content/declaration_lessons/sphmc-smoothed-hessian-bounds.json']:
 assert G(['show',B+':'+p])==G(['show',C+':'+p]),p
sources=[]
for s in ex['accepted_source_bindings']:
 p=s['audit']['path'];raw=pathlib.Path(p).read_bytes();assert H(raw)==s['audit']['raw_sha256']
 assert G(['show',C+':'+p])==G(['show',B+':'+p])
 a=J(p);pn=s['source_packet']['path'];pk=J(pn);rs=J(s['source_result']['path'])
 assert pk==rt.semantic_reviewer_packet(a)
 assert a['state']==a['source_review']['state']=='accepted'
 assert rt.sha256_json({k:x for k,x in rs.items() if k!='review_run_sha256'})==rs['review_run_sha256']==s['source_review_run_sha256']
 assert all(F(s[k]['path'])['raw_sha256']==s[k]['raw_sha256'] for k in ['source_packet','source_result','decoder_packet','decoder_result'])
 sources.append({'audit':F(p),'source_run':s['source_review_run_sha256'],'current_canonical_packet':pk['packet_sha256'],'publication_binding':a['publication_binding_sha256'],'whole_module_binding_unchanged':True})
pub.check_advance(cl['declarations'],reviewed=True)
# Root's actual integrated compile logs are exact committed evidence; fresh broad compile would only repeat unchanged work.
rootchecks=[]
for q in i['checks']:
 assert q['exit_code']==0
 f=F(q['log']);assert f['raw_sha256']==q['raw_sha256']
 assert G(['show',C+':'+q['log']])==pathlib.Path(q['log']).read_bytes()
 rootchecks.append({**q,'log_hashes':f,'Git_exact_raw':True})
ag=pathlib.Path(R/'aggregate.log').read_text(encoding='utf8')
assert 'Build completed successfully (9129 jobs).'in ag and 'Build completed successfully (9389 jobs).'in ag
assert '$ lake build Tests'in ag and '$ lake build'in ag and 'ASTIS check passed'in ag
assert 'sorryAx'not in ag
targetaxioms=re.findall(r"'(?:AutoSamplingTheory\.TechnicalLemmas\.FunctionalInequalities\.GibbsLinearCovarianceUpper\.gibbs_linear_covariance_upper|AutoSamplingTheory\.ExampleCases\.SmoothedPicardHMC\.SmoothedHessianBounds\.smoothed_hessian_bounds|Tests\.SmoothedHessianBounds\.[^']+)' depends on axioms: \[([^]]*)\]",ag)
assert len(targetaxioms)==6 and all(set(x.strip()for x in a.split(','))=={'propext','Classical.choice','Quot.sound'}for a in targetaxioms)
# Independently fresh static whole repository fake-closure scan with exact Git source binding.
fakefiles=[p.relative_to(pathlib.Path.cwd()).as_posix()for p in astis.lean_source_files()]
assert not astis.forbidden_pattern_hits()
tracked=set(G(['ls-tree','-r','--name-only',C]).decode().splitlines());assert all(p in tracked for p in fakefiles)
requests=[C+':'+p for p in fakefiles]
batch=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(requests)+'\n').encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
cursor=0; fake_inventory=[]
for p in fakefiles:
 end=batch.index(b'\n',cursor);head=batch[cursor:end].split();assert head[1]==b'blob',head
 size=int(head[2]);start=end+1;blob=batch[start:start+size];cursor=start+size+1
 raw=pathlib.Path(p).read_bytes();assert LF(blob)==LF(raw),p
 fake_inventory.append({'working':F(p),'Git_raw_sha256':H(blob),'Git_LF_sha256':H(LF(blob))})
assert cursor==len(batch)
fakep=R/'repository-proof-seal.fake-closure-scan.json'
W(fakep,{'checked_commit':C,'method':'fresh astis.forbidden_pattern_hits full production/Test/root scan; all inputs checked against current Git normalized source blobs','file_count':len(fakefiles),'hits':[],'source_files':fake_inventory})
# Bound independent cells' verification and integration administration, without touching state/evidence.
cellrec=[]
for cid in cl['cells']:
 p='research-wiki/frontier-cells/'+cid+'.json'
 before=json.loads(G(['show',B+':'+p]));current=J(p);ds=diff(before,current)
 allowed={'/status','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt','/graph_contribution/visual_review'}
 assert all(q['field']in allowed for q in ds),ds
 assert current['status']=='independently_verified'
 assert isinstance(current['evidence']['independent_verification'],str)
 assert current['evidence']['independent_verification']==(R/'verified.json').as_posix()
 assert current['evidence']['integration_receipt']==(R/'integration.json').as_posix()
 cellrec.append({'path':p,'current':F(p),'allowed_diffs':ds})
# Exact fresh lightweight source/reader gates, no recompilation and no canonical mutations.
fresh=[]
for name,args in [('publication',['tools/astis_publication.py','check','--base','origin/main']),
 ('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check'])]:
 r=subprocess.run([sys.executable]+args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 lp=R/('repository-proof-seal.'+name+'.log');lp.write_bytes(r.stdout);assert r.returncode==0,r.stdout.decode()
 fresh.append({'command':[sys.executable]+args,'exit_code':r.returncode,'log':F(lp)})
graphs=[]
for name in ['graph-covariance.json','graph-hessian.json','graph24-domain.json','graph24-variance.json','graph24-score.json']:
 p=R/name;assert G(['show',C+':'+p.as_posix()])==p.read_bytes()
 j=J(p);assert j['status']=='graph coverage checked'
 graphs.append(F(p))
official=R/'official-graph-refresh.log';assert G(['show',C+':'+official.as_posix()])==official.read_bytes()
assert G(['-C','.lake/packages/mathlib','rev-parse','HEAD']).decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert pathlib.Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert adv.current_advances()[cl['advance_id']]['state']=='VERIFIED'
assert [k for k,z in adv.current_advances().items()if z['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
out={'schema_version':1,'kind':'independent-scoped-repository-proof-seal','advance_id':cl['advance_id'],'reviewer_id':V,
 'status':'accepted-scoped','verification_status':'passed-scoped','proof_seal_status':'repository-accepted-scoped',
 'checked_integration_commit':C,'verified_proof_commit':B,'verified_receipt':F(R/'verified.json'),'integration_receipt':F(R/'integration.json'),
 'integration_receipt_scope':'Root checked uncommitted integration on d8 parent; exact c614 Git diff proves precisely three added imports, unchanged reviewed source/tests/math/lessons plus permitted admin and preserved receipts. This independently pins root raw compile/static receipts to the exact shared integration commit.',
 'declarations':cl['declarations'],'statement_seals':F(R/'preproof/statement-seals.accepted.json'),
 'sealed_mathematical_scope':v['mathematical_scope'],'stable54_raw_LF_unchanged':stable,'source_audits_unchanged':sources,
 'aggregate_imports':imports,'repository_checks':rootchecks,'aggregate_summary':i['aggregate_summary'],
 'fresh_small_checks':fresh,'fresh_recompiled_by_this_reviewer':False,
 'reuse_reason':'Actual root lake build and Tests 9129/9389 passed against the precise shared import delta; entire prior independent mathematics, direct/Test/sharp-quadratic/source review matches exact unchanged bytes. No redundant aggregate/focused recompile or repeated math credit.',
 'fresh_static_repository_fake_closure_scan':F(fakep),'whole_repository_fake_scan_file_count':len(fakefiles),'fake_hits':[],
 'standard_axioms':['propext','Classical.choice','Quot.sound'],'actual_packet25_aggregate_axiom_prints':6,
 'graph_structural_checks':graphs,'official_graph_refresh_log':F(official),
 'cell_metadata_reconciliation':cellrec,'source_proof_coverage':v['coverage'],
 'proof_seal_requirements':{'statement_signature_matches':True,'actual_focused_and_repository_compile_evidence':True,'no_unauthorized_axiom_placeholder_fakeclosure':True,'binder_audit_source_no_EXCESS':True,
 'canonical_BOTH_curvature_and_explicit_L2_scope_retained':True,'all_required_conditional_premises_in_source_A_internally_produced':True,'independent_encoder_denoiser_accepted_current_whole_module':True,
 'source_graph_discharge_and_SOURCE_GAP_boundaries_explicit':True},
 'remaining_boundaries':['Repository ProofSeal accepted only for exact two declared scoped interfaces at c614; purification/ExpositionSeal/rendered visual QA/current-head remote CI/main merge/deployment remain separately unadmitted.',
 'Canonical BOTH-curvature isotropic covariance is not full anisotropic Brascamp-Lieb or full cited textbook reverse-Cramer-Rao proof. Source beta1/kappa>=1/0<eta<=1 and normalized U versus unnormalized V_eta additive logZ convention remain exact.',
 'Joint measurable posterior selectors, higher smoothing derivatives, normalized conditional score/marginal Poincare, PBPS remaining reflection/invariance/non-explosion/hypocoercivity/implementation/cost, Wp/proxy-warmness/history/query work, both main results and actual composition remain open. TV proximity never transfers unbounded cost.'],
 'future26_exclusion':'research-wiki/cited-results/Standardized_RGO_next_source_contract.md and runs/20261006-companion-priority/full-range-proximal/: content not read/admitted, not a current formal parent or proof seal input.',
 'no_advance_or_cell_mutations_by_this_review':True,'all_compiler_sessions_closed':True,'compiler_lease':'CLOSED','write_lease':'CLOSED',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
assert not (R/'repository-proof-seal.json').exists();W(R/'repository-proof-seal.json',out)
print(json.dumps({'status':out['status'],'checked_commit':C,'receipt':F(R/'repository-proof-seal.json'),'whole_repository_scan':len(fakefiles),'math54unchanged':len(stable),'aggregate':[9129,9389],'compiler_and_write_lease':'CLOSED'},ensure_ascii=False,indent=2))
