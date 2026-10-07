import pathlib,json,hashlib,subprocess,sys,re,gzip,os
from datetime import datetime,timezone
ROOT=pathlib.Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean52';OUT=P/'repository-seal52';OUT.mkdir(exist_ok=True)
COMMIT='75a53e2353a9eec5b810669527195618d54636f0';SCI='a18cd1cf8e8310f228391d4c53a2ac8f1a8900ec';ADV='ASTIS-SA-20261007-GaussianReflectedMean';DECL='AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean.gaussian_reflected_mean_c1';CELL='ASTIS-SHARED-gaussian-reflected-mean'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'website/scripts'))
from tools.astis_advance import current_advances
from tools import astis_publication
import publication_reader
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,o):p.write_text(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def logical(obj,key):
 d=dict(obj);h=d.pop(key);assert sha(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())==h;return h
def vp(e):
 p=pathlib.Path(e['path']);p=p if p.is_absolute() else ROOT/p;a=pin(p)
 for k in ['raw_sha256','lf_sha256','bytes']:
  if k in e:assert a[k]==e[k],str(p)+' '+k
 return a
write(OUT/'lease.json',{'status':'OPEN','owner':'whole_math52','scope':'Read-only scoped repository ProofSeal52 at exact integration commit; writes only owned repository-seal52 outputs','opened_utc':now(),'compiler':'NOT_STARTED_CLOSED','Python_pid':os.getpid(),'integration_commit':COMMIT})
assert git('rev-parse','HEAD').decode().strip()==COMMIT and not git('status','--porcelain','--untracked-files=no').strip()
assert subprocess.run(['git','merge-base','--is-ancestor',SCI,COMMIT],cwd=ROOT).returncode==0
allchanges=git('diff','--name-only',SCI,COMMIT).decode().splitlines()
assert not any(re.search(r'(pbps-reflected-density-.*53|phase-pbps-primary-preread53)',n) for n in allchanges)
scientific=['AutoSamplingTheory/TechnicalLemmas/Measure/GaussianReflectedMean.lean','Tests/ProximalBPSGaussianReflectedMean.lean','lean-toolchain','lake-manifest.json','website/content/declaration_lessons/gaussian-reflected-mean.json','website/content/publications/gaussian-reflected-mean.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianReflectedMean.json']
unchanged=[]
for n in scientific:
 a=git('show',SCI+':'+n);b=git('show',COMMIT+':'+n);assert a==b
 assert sha(b.replace(b'\r\n',b'\n'))==pin(ROOT/n)['lf_sha256']
 unchanged.append({'current':pin(ROOT/n),'scientific_blob_sha256':sha(a),'integration_blob_sha256':sha(b),'same_git_blob':True})
prod=(ROOT/scientific[0]).read_text(encoding='utf-8');test=(ROOT/scientific[1]).read_text(encoding='utf-8')
assert len(prod.splitlines())==179 and len(test.splitlines())==84
sig=prod[prod.index('theorem gaussian_reflected_mean_c1'):].split('\n := by',1)[0]+'\n';assert len(sig.encode())==497 and sha(sig.encode())=='50ca5c7e0b5aed0f892d2e686fd276b11a586b30745d8edd2d5c1256d7e09d11'
frozen=read(P/'math-freeze.json');strict=[vp(e) for e in frozen['inputs']];assert len(strict)==333
source=read(P/'source.0.review.json');m={r['input_path'].replace('\\','/'):r['snapshot'] for r in source['raw_snapshot_bindings']};strictsource=[]
for e in source['input_artifacts']:
 a=vp(m[e['path'].replace('\\','/')]);assert all(a[k]==e[k] for k in ['raw_sha256','lf_sha256','bytes']);strictsource.append({'original':e,'snapshot':a})
assert len(strictsource)==347
native=[];logicalhashes=[]
for folder in ['whole-proof-review52','exact-verification52']:
 l=read(P/folder/'lease.json');assert l['status']=='CLOSED'
 for e in l['actual_final_outputs']:native.append(vp(e))
 r=read(P/folder/'run.json');h=logical(r,'run_sha256');logicalhashes.append({'file':pin(P/folder/'run.json'),'run_sha256':h})
for n,key in [('source.0.review.json','review_run_sha256'),('reviewer.source.run.json','run_sha256'),('reviewer.source.lease.json','lease_run_sha256'),('source.review.lease.json','lease_run_sha256')]:
 logicalhashes.append({'file':pin(P/n),'logical_sha256':logical(read(P/n),key),'self_hash_field':key})
decoder=read(P/'anonymous-decoder/run.json');logicalhashes.append({'file':pin(P/'anonymous-decoder/run.json'),'run_sha256':logical(decoder,'run_sha256')})
assert sha(json.dumps(decoder['run_binding_payload'],ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())==decoder['decoder_run_sha256']==source['decoder_run_sha256']
for e in read(P/'anonymous-decoder/binding-receipt.json')['output_artifacts']:native.append(vp(e))
for n in ['whole-proof-review52/compiler.lease.json','reviewer.source.lease.json','source.review.lease.json','anonymous-decoder/lease.json','exact-verification52/lease.json']:assert read(P/n)['status']=='CLOSED'
audit=read(ROOT/scientific[-1]);audit=audit['audits'][0] if 'audits' in audit else audit
item=next(i for i in astis_publication.load() if i['id']=='gaussian-reflected-mean');binding=item['bindings'][0]
assert astis_publication.binding_digest(item,binding)==audit['publication_binding_sha256']==source['publication_binding_sha256']
assert astis_publication.review_context(item,binding)==audit['publication_context']==source['current_review_context']
assert audit['state']=='accepted' and source['verdict']=='equivalent-after-elaboration' and not source['blocking'] and not source['deltas'] and not source['repairs'] and not source['source_excess']
cell=read(ROOT/'research-wiki/frontier-cells'/f'{CELL}.json');assert cell['status']=='independently_verified'
state=current_advances();assert state[ADV]['state']=='VERIFIED'
stabilizing=[k for k,v in state.items() if v['state']=='STABILIZING'];assert stabilizing==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
rows=[json.loads(l) for l in (ROOT/'runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines()];target=[r for r in rows if r.get('advance_id')==ADV];verified=[r for r in target if r.get('to_state')=='VERIFIED'];assert len(verified)==1 and verified[0]['worker_id']=='whole_math52' and verified[0]['evidence']['verified_commit']==SCI
statuses=[];labels=['tests','mandatory','pycompile','whitespace','publication','semantic','frontier','contributor','site-build','official-graph','graph','site-check'];lease=read(P/'root.integration.1.lease.json');assert lease['status']=='CLOSED' and lease['exit_code']==0 and lease['compiler']=='CLOSED' and lease['Python']=='CLOSED' and lease['read']=='CLOSED' and lease['write']=='CLOSED'
last=None
for label in labels:
 sp=P/f'integration.1.{label}.status.json';lp=P/f'integration.1.{label}.log';s=read(sp);assert s['exit_code']==0 and s['proof_commit']==SCI and sha(lp.read_bytes())==s['log_raw_sha256'];assert s['started_utc']<=s['finished_utc']
 if last is not None:assert s['started_utc']>=last
 last=s['finished_utc'];statuses.append({'label':label,'status':pin(sp),'log':pin(lp),'exit_code':0,'command':s['command'],'started_utc':s['started_utc'],'finished_utc':s['finished_utc']})
assert last<=lease['closed_utc'];assert len(list(P.glob('integration.1.*.status.json')))==12
testslog=(P/'integration.1.tests.log').read_text(encoding='utf-8');mandatory=(P/'integration.1.mandatory.log').read_text(encoding='utf-8');assert 'Build completed successfully (9439 jobs).' in testslog and 'ASTIS check passed' in mandatory and 'Build completed successfully (9155 jobs).' in mandatory and 'Build completed successfully (9439 jobs).' in mandatory
registry=(ROOT/'AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text(encoding='utf-8');assert len(re.findall(r'status\s*:=\s*LemmaMemoryStatus\.formalizedLocal',registry))==493 and DECL in registry
assert 'formalizedTechnicalLemmaCount = 493 := by native_decide' in (ROOT/'Tests/Basic.lean').read_text(encoding='utf-8')
agg=(ROOT/'AutoSamplingTheory/TechnicalLemmas.lean').read_text(encoding='utf-8');assert 'import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean' in agg
clean=re.sub(r'/\-.*?\-/','',agg,flags=re.S);clean=re.sub(r'--[^\n]*','',clean);assert not re.search(r'\b(theorem|def|lemma|instance|axiom)\b',clean)
assert 'import Tests.ProximalBPSGaussianReflectedMean' in (ROOT/'Tests.lean').read_text(encoding='utf-8')
measure='AutoSamplingTheory/TechnicalLemmas/Measure.lean';assert git('show',COMMIT+':'+measure)==git('show','origin/main:'+measure)==git('show',SCI+':'+measure)
diagnosis=read(P/'integration-import-route.diagnosis.json');negative=read(P/'integration.publication.status.json');neglog=P/'integration.publication.log';assert negative['exit_code']==1 and sha(neglog.read_bytes())==diagnosis['negative_log_sha256']==negative['log_raw_sha256'];assert 'integrable_of_measure_eq' in neglog.read_text(encoding='utf-8')
notes=read(P/'integration.notes.json');assert notes['registry_count']==493 and notes['root_jobs']==9155 and notes['test_jobs']==9439
for e in notes['checks']+notes['shared_files']:vp(e)
w=read(P/'integration-whitespace52/diagnosis.json');vp(w['gzip']);raw=gzip.decompress((ROOT/w['gzip']['path']).read_bytes());assert sha(raw)==w['full_negative_raw_sha256'] and len(raw)==w['full_negative_raw_bytes'] and w['full_staged_exit']==2 and len(w['findings'])==305 and len(w['immutable_raw_artifacts'])==5 and w['authored_exit']==0
for e in w['immutable_raw_artifacts']:vp(e)
exclusions=[x for x in w['authored_command'] if x.startswith(':(exclude)')];assert len(exclusions)==5 and all(x[10:]==e['path'] for x,e in zip(exclusions,w['immutable_raw_artifacts']))
wc=['git','-c','core.whitespace=cr-at-eol','diff',SCI,COMMIT,'--check','--','.',*exclusions];wr=subprocess.run(wc,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(OUT/'authored-whitespace.log').write_bytes(wr.stdout);assert wr.returncode==0
graphpath=ROOT/'_site/data/underlying-lean-graph.json';graph=read(graphpath);assert graph['publication_inputs_sha256']==publication_reader.graph_input_digest()
saved=read(P/'integration.1.graph.log');current=astis_publication.graph_report(CELL,ROOT/'_site');assert saved==current and current['contributions'][0]['node']=='decl:'+DECL and current['contributions'][0]['omitted_connections']==0
visual=read(P/'visual.inspection.json');vpics=[]
for e in visual['artifacts']:
 a=pin(ROOT/e['portable_path']);assert a['raw_sha256']==e['raw_sha256'] and a['bytes']==e['bytes'];vpics.append(a)
for n in ['cdp.capture.json','proof.capture.json']:assert read(P/'visual-inspection52'/n)['ownedBrowserExit']['code']==0
assert len(visual['viewed_images'])==4 and visual['DOM']['initially_closed_Lean_disclosures']==11 and visual['DOM']['rendered_math_containers']==8
write(OUT/'strict-input-bindings.json',{'integration_commit':COMMIT,'scientific_commit':SCI,'current_HEAD':COMMIT,'tracked_tree_clean':True,'changed_owned_paths':allchanges,'new53_paths_integration_count':0,'scientific_packet_unchanged':unchanged,'strict_math333':strict,'strict_source347_originals':strictsource,'native_owned_output_bindings':native,'native_logical_hashes':logicalhashes,'aggregate_statuses':statuses,'root_lease':pin(P/'root.integration.1.lease.json'),'portable_visuals':vpics,'graph':pin(graphpath),'graph_publication_inputs_sha256':graph['publication_inputs_sha256']})
write(OUT/'graph-one-hop.json',current)
write(OUT/'visual-review.json',{'reviewer':'whole_math52','viewed_actual_portable_images':['cdp.pbps.png','cdp.branch.png','proof.proof.png','proof.proof-late.png'],'source':pin(P/'visual.inspection.json'),'images':[pin(P/'visual-inspection52'/n) for n in visual['viewed_images']],'findings':['Attributed generic probability/finite Hilbert/rank0/compact C1 literal posterior/reflection theorem and every-y normalized N/Z statement visibly retained.','The displayed six steps retain both derivative signs, genuine compact bounds/L1, common domination, continuous integrated derivative, positive normalizer and actual PBPS/noncentered rank0 consumers.','Exact graph focus visibly names the compiled shared declaration; solid structural and dashed incomplete source/reference semantics are explicit.','Long derivative display uses horizontal scrolling; large graph labels wrap heavily; source statement is repeated and some residual administrative prose still says reviews pending. These are visible preserved exposition debts, not new mathematical credit.'],'acceptance_boundary':'Four local desktop captures inspected; no physical-device/mobile/live/copy/download/full-reader or independent Exposition Seal/PURIFIED claim.'})
receipt={'schema_version':1,'reviewer':'whole_math52','verdict':'ACCEPT_SCOPED_REPOSITORY_PROOFSEAL52','integration_commit':COMMIT,'scientific_commit':SCI,'advance_id':ADV,'scope':'Repository ProofSeal for exactly the actual literal reflected Gaussian posterior compact-C1 observer mean leaf, source normalization/dominated derivative proof and its genuine PBPS/rank0 Tests. Read-only seal; no recompile, reproof, new VERIFIED transition or canonical edits.','scientific_preservation':{'production_lines':179,'sealed_header_LF_bytes':497,'Test_lines':84,'same_a18_proof_Test_publication_lesson_audit_toolchain_manifest_Git_blobs':True,'strict_math333_original_pins':True,'strict_source347_original_snapshot_pins':True,'whole_math_source_blind_exact_native_raw_LF_logical_checks':True},'independent_verification_state':{'cell_status':'independently_verified','advance_state':'VERIFIED','VERIFIED_count':1,'VERIFIED_author':'whole_math52','VERIFIED_scientific_commit':SCI,'sole_STABILIZING_owner':stabilizing[0],'canonical_cell':pin(ROOT/'research-wiki/frontier-cells'/f'{CELL}.json')},'aggregate_acceptance':{'attempt':1,'actual_serial_gates':12,'all_exit_zero':True,'root_build_jobs':9155,'Tests_build_jobs':9439,'registry_count':493,'root_lease':pin(P/'root.integration.1.lease.json'),'status_and_log_binding':pin(OUT/'strict-input-bindings.json'),'interpretation':'Actual preserved serial gate logs and CLOSED0 root lease reviewed; no new Lean invocation was needed.'},'import_route':{'diagnosis':pin(P/'integration-import-route.diagnosis.json'),'original_failed_publication':pin(P/'integration.publication.status.json'),'original_failed_log':pin(neglog),'classification':'IMPLEMENTATION_FAILED','mathematical_change':False,'repair_checked':'Measure compatibility module exactly equals origin/main and a18. Identical new52 import lives only in declaration-free TechnicalLemmas aggregator; root Tests imports actual focused Test; Registry and Basic count493 genuinely exercised.','attempt1_publication_pass':True},'whitespace':{'diagnosis':pin(P/'integration-whitespace52/diagnosis.json'),'gzip':vp(w['gzip']),'negative_exit':2,'negative_findings':305,'explicit_immutable_paths':5,'authored_exact_commit_command':wc,'authored_exact_commit_exit':0,'authored_log':pin(OUT/'authored-whitespace.log'),'blanket_folder_exclusion':False,'full_staged_whitespace_PASS':False},'graph':{'graph':pin(graphpath),'current_inputs_digest_exact':True,'publication_inputs_sha256':graph['publication_inputs_sha256'],'official_one_hop_exact_match':True,'one_hop':pin(OUT/'graph-one-hop.json'),'truth_boundary':'Solid module/declaration structure does not assert theorem implication; source/reference/audit overlays remain distinct and incomplete scans are explicit. No conceptual transport certificate claimed.'},'visual_review':pin(OUT/'visual-review.json'),'source_normalization_and_derivative_boundary':'The same specified all-y quadratic tilt/reflection is normalized by genuine positive Z; weighted numerator derivative and derivative continuity are proved internally with compact/Gaussian domination, retaining negative affine-reflection and likelihood terms. Generic input/compact C1/rank0 scope is an attributed analytic generalization, not a printed full PBPS theorem or arbitrary AE representative assertion.','unchanged_source_admission':{'audit':'ASTIS-RT-20261007-GaussianReflectedMean','verdict':'equivalent-after-elaboration','publication_binding_sha256':source['publication_binding_sha256'],'current_full_review_context_exact':True,'no_excess_or_repairs':True,'blindness':'Anonymous statement/source-text-blind reconstruction with inherited general source identities explicitly disclosed; strict identity blindness not claimed.'},'new53_boundary':'New53 prereads/proposals remain untracked and absent from integration diff; no new53 content inspected.','remaining_open':['Source-volume EVERY-y SAME-S adapter and actual Tf closed-gradient membership.','Rough B.13/Gamma/hypocoercivity/main/error/nonexplosion results.','Four whole papers, actual-input composition and expected-query costs.','Main merge, live deployment, full-reader/mobile/copy/download and PURIFIED/Exposition Seal acceptance.'],'blockers':[],'completed_utc':now()}
write(OUT/'ProofSeal52.json',receipt)
assert git('rev-parse','HEAD').decode().strip()==COMMIT and not git('status','--porcelain','--untracked-files=no').strip()
write(OUT/'final-state.json',{'commit':COMMIT,'tracked_tree_still_clean':True,'advance_state':current_advances()[ADV]['state'],'cell_status':read(ROOT/'research-wiki/frontier-cells'/f'{CELL}.json')['status'],'no_canonical_write':True,'no_compiler_started':True,'checked_utc':now()})
run={'schema_version':1,'reviewer':'whole_math52','integration_commit':COMMIT,'scientific_commit':SCI,'verdict':receipt['verdict'],'input_bindings':pin(OUT/'strict-input-bindings.json'),'outputs':[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name not in ['run.json','lease.json']],'compiler_started':False,'completed_utc':now(),'logical_hash_recipe':'SHA256 UTF8 sorted compact ensure_ascii=False JSON run minus run_sha256; actual serialized raw/LF file is bound by final closed lease.'}
run['run_sha256']=sha(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode());write(OUT/'run.json',run)
lease=read(OUT/'lease.json');lease.update(status='CLOSED',compiler='NOT_STARTED_CLOSED',Python='CLOSED',read='CLOSED',write='CLOSED',closed_utc=now(),run_sha256=run['run_sha256'],actual_final_outputs=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='lease.json'],final_operation='Actual closed reviewer lease written last after scoped ProofSeal/run/all input-output pins.');write(OUT/'lease.json',lease)
print(json.dumps({'verdict':receipt['verdict'],'commit':COMMIT,'ProofSeal':pin(OUT/'ProofSeal52.json'),'run':pin(OUT/'run.json'),'run_sha256':run['run_sha256'],'lease':pin(OUT/'lease.json'),'all12gates':'PASS','registry':493,'compiler_started':False}))
