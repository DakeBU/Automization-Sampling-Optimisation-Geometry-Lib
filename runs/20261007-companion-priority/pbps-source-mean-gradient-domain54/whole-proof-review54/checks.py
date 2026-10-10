from review import *
assert load(O/'compiler.lease.json')['status']=='CLOSED'
sealed=load('runs/20261007-companion-priority/pbps-source-mean-gradient-domain-preproof54/statement-seals.accepted.json')
sig=sealed['signatures'][0]
prod='AutoSamplingTheory/ExampleCases/ProximalBPS/SourceMeanGradientDomain.lean';test='Tests/ProximalBPSSourceMeanGradientDomain.lean'
b=path(prod).read_bytes().replace(b'\r\n',b'\n');start=b.index(b'theorem literal_source_mean_in_closed_gradient');end=b.index(b' := by',start);header=b[start:end]+b'\n'
assert header==sig['signature_text'].encode() and len(header)==1448 and sha(header)==sig['signature_lf_sha256']=='19de42336148aa900917e6c77753325145d6010dfd1718c1625b2b9a8f7ce595'
assert path(prod).read_bytes()==path(B/'prod.1.source.raw.snapshot.lean').read_bytes() and path(test).read_bytes()==path(B/'Tests.4.source.raw.snapshot.lean').read_bytes()
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
dependencies=[prod,test,'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/LiteralReflectedMean.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalGradient.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedC1GradientDomain.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CompactC1GradientDomain.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean']
scan=[]
for p in dependencies:
 co=astis.strip_lean_comments_and_strings(path(p).read_text(encoding='utf-8'));hits=[n for n,l in enumerate(co.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;scan.append(dict(input=pin(p),fake_closure_hits=hits))
co=astis.strip_lean_comments_and_strings(path(prod).read_text(encoding='utf-8'));assert not re.search(r'\b(private|axiom|instance)\b',co)
for name in ['actual_macroscopic_gradient_energy_blocks','gaussian_marginal_gradient_closable','reflected_gibbs_mean_c1','c1_in_closed_gradient']:assert name in co
log=path(O/'focused.log').read_text(encoding='utf-8');assert 'Build completed successfully (3898 jobs).' in log and 'Replayed Tests.ProximalBPSSourceMeanGradientDomain' in log and 'Replayed AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain' in log
printed=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log);assert len(printed)==6
for n,axs in printed:assert set(re.findall(r'[A-Za-z_.]+',axs))=={'propext','Classical.choice','Quot.sound'}
assert 'sorryAx' not in log
negative=[]
for name,exit in [('prod.0',1),('prod.1',0),('Tests.0',1),('Tests.1',1),('Tests.2',1),('Tests.3',1),('Tests.4',0)]:
 s=load(B/(name+'.status.json'));l=load(B/(name+'.compiler.lease.json'));raw=path(B/(name+'.log')).read_bytes();source=path(B/(name+'.source.raw.snapshot.lean')).read_bytes()
 assert s['exit_code']==exit and l['status']=='CLOSED' and l['exit_code']==exit and sha(raw)==s['log_raw_sha256'] and sha(source)==s['source_raw_sha256']
 stripped=astis.strip_lean_comments_and_strings(source.decode('utf-8'));assert not astis.FORBIDDEN_REGEX.search(stripped)
 if exit==0:assert b'sorryAx' not in raw
 negative.append(dict(attempt=name,status=pin(B/(name+'.status.json')),source=pin(B/(name+'.source.raw.snapshot.lean')),log=pin(B/(name+'.log')),lease=pin(B/(name+'.compiler.lease.json')),exit_code=exit,failed_only_compiler_sorryAx=b'sorryAx' in raw))
native=[]
native_specs=[('pbps-source-mean-gradient-domain-preproof-review54/reviewer.statement.run.json','statement_review_run_sha256'),('pbps-source-mean-gradient-domain-sourcegraph54/run.json',None),('pbps-source-mean-gradient-domain-topology-overlay54/run.json',None),('pbps-source-mean-gradient-domain-topology-review54/reviewer.topology.run.json','review_run_binding_sha256'),('pbps-source-mean-gradient-domain-topology-review54/repaired.reviewer.topology.run.json','review_run_binding_sha256')]
base=R/'runs/20261007-companion-priority'
for p,payload_field in native_specs:
 d=load(base/p);full=logical({k:v for k,v in d.items() if k!='run_sha256'});assert full==d['run_sha256']
 row=dict(input=pin(base/p),full_self_field='run_sha256',full_logical_sha256=full,full_recipe='Sorted compact UTF8 ensure_ascii=False allow_nan=False entire object minus run_sha256; no newline')
 if payload_field:assert logical(d['run_binding_payload'])==d[payload_field];row.update(payload_field=payload_field,payload_sha256=d[payload_field],payload_recipe='Sorted compact UTF8 ensure_ascii=False allow_nan=False exact run_binding_payload; no newline')
 native.append(row)
topology=load(base/'pbps-source-mean-gradient-domain-preproof54/topology-seals.accepted.json')
for e in topology['strict_adoption_bindings']:assert equal(e)
assert topology['signature_lf_sha256']==sig['signature_lf_sha256']
leases=[]
for folder,name in [('pbps-source-mean-gradient-domain-preproof-review54','reviewer.statement.lease.json'),('pbps-source-mean-gradient-domain-sourcegraph54','lease.json'),('pbps-source-mean-gradient-domain-topology-overlay54','lease.json'),('pbps-source-mean-gradient-domain-topology-review54','reviewer.topology.lease.json'),('pbps-source-mean-gradient-domain-topology-review54','repaired.reviewer.topology.lease.json')]:
 p=base/folder/name;ld=load(p);assert ld['read']==ld['write']=='CLOSED' and ld.get('Python',ld.get('python'))=='CLOSED' and ld['compiler'] in {'CLOSED','NOT_STARTED_CLOSED'};assert ld.get('status','CLOSED')=='CLOSED';leases.append(dict(input=pin(p),actual_native_fields=ld))
mapping=load(base/'pbps-source-mean-gradient-domain-topology-review54/repaired.corrective-mapping.json')
for label in ['pinned_actual_original_before','pinned_actual_successor_after','retained_incidental_excluded_record']:
 e=mapping[label];raw=path(e['path']).read_bytes();fragment=raw[e['start_utf8_byte0']:e['end_utf8_byte0_exclusive']];assert sha(raw)==e['whole_raw_sha256'] and sha(fragment)==e['fragment_raw_sha256'] and sha(fragment.replace(b'\r\n',b'\n'))==e['fragment_lf_sha256']
mathlib_files=['Mathlib/Topology/Algebra/Module/LinearPMap.lean','Mathlib/LinearAlgebra/LinearPMap.lean','Mathlib/Analysis/Calculus/Gradient/Basic.lean','Mathlib/MeasureTheory/Function/LpSpace/Basic.lean','Mathlib/MeasureTheory/Function/LpSeminorm/Defs.lean','Mathlib/MeasureTheory/Integral/DominatedConvergence.lean','Mathlib/Analysis/Normed/Lp/SmoothApprox.lean','Mathlib/Analysis/Calculus/ContDiff/Convolution.lean','Mathlib/Analysis/Calculus/BumpFunction/Convolution.lean']
math=[];rev='db584cd6d46c92f209a44c0f1c829460d327499d';mp=R/'.lake/packages/mathlib';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=mp,text=True).strip()==rev
for p in mathlib_files:
 blob=subprocess.check_output(['git','show',rev+':'+p],cwd=mp);current=path(mp/p).read_bytes();assert blob.replace(b'\r\n',b'\n')==current.replace(b'\r\n',b'\n');math.append(dict(input=pin(mp/p),pinned_Git_LF_sha256=sha(blob.replace(b'\r\n',b'\n')),current_LF_equal=True))
dump(O/'checks.json',dict(status='PASS',actual_python_pid=os.getpid(),signature=sig,current_signature_LF_bytes=len(header),current_signature_LF_sha256=sha(header),production=pin(prod),Tests=pin(test),production_lines=len(b.splitlines()),Test_lines=len(path(test).read_bytes().splitlines()),actual_four_parent_calls=True,no_private_provider_or_extra_instance=True,fake_closure_scan=scan,focused_status=pin(O/'focused.status.json'),actual_focused_compiler_pid=load(O/'focused.status.json')['process_id'],focused_exit=0,focused_jobs=3898,target_and_production_replayed=True,force_rebuild=False,printed_axioms=[dict(declaration=n,axioms=sorted(re.findall(r'[A-Za-z_.]+',a))) for n,a in printed],preserved_negatives=negative,preproof_native_logical_runs=native,preproof_actual_CLOSED_leases=leases,T54_original_to_successor_operatively_corrected=True,Mathlib_current_pinned_files=math,source_final_verdict_or_decoder_read=False,future55_reads=False))
strict('inputs.post-analysis.json')
print(json.dumps(dict(status='PASS',signature_LF_bytes=len(header),strict552='PASS',native_runs=len(native),standard_axiom_prints=len(printed),original_failures_preserved=5,actual_python_pid=os.getpid())))
