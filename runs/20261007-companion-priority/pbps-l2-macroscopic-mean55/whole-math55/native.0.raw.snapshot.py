from common import *
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis
assert git('rev-parse','HEAD')==BASE
strict('inputs.post-analysis.json')
body='AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean';test='Tests/ProximalBPSL2MacroscopicMean.lean'
for p,n in [(body,'production.actual.raw.snapshot.lean'),(test,'Tests.actual.raw.snapshot.lean')]: (O/n).write_bytes(path(p).read_bytes())
b=path(body).read_bytes().replace(b'\r\n',b'\n');start=b.index(b'theorem actual_macroscopic_l2_mean');end=b.index(b' := by',start);header=b[start:end]+b'\n'
seal=load(R/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-preproof55/statement-seals.accepted.json');sig=seal['signatures'][0]
assert len(header)==sig['LF_bytes']==2526 and sha(header)==sig['signature_lf_sha256']=='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f' and header.decode()==sig['signature_text']
parents=[('AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean','MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks'),('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalGradient.lean','GaussianMarginalGradient.gaussian_marginal_gradient_closable'),('AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean','ReflectionL2.actual_reflection_block_identities'),('AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean','GaussianReflection.reflection_preserves_augmentation'),('AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean','GaussianConditionalKernel.exists_tilted_isCondKernel')]
text=path(body).read_text(encoding='utf-8'); assert all(call in text for p,call in parents)
assert len(re.findall(r'^theorem ',text,re.M))==1 and not re.search(r'^\s*(?:private\s+)?(?:def|axiom|opaque|instance|structure|lemma)\b',astis.strip_lean_comments_and_strings(text),re.M)
scan=[]
background=['AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean']
for p in [body,test]+[p for p,c in parents]+background:
 stripped=astis.strip_lean_comments_and_strings(path(p).read_text(encoding='utf-8'));hits=[n for n,l in enumerate(stripped.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits,p;scan.append(dict(input=pin(p),hits=hits))
log=path(O/'focused.log').read_text(encoding='utf-8'); assert 'Build completed successfully (3894 jobs).' in log and 'sorryAx' not in log
prints=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log);expected={TARGET,'Tests.ProximalBPSL2MacroscopicMean.actual_rough_difference_variance','Tests.ProximalBPSL2MacroscopicMean.rank_zero_actual_source_constant'}
assert len(prints)==3 and {n for n,a in prints}==expected and all(set(re.findall(r'[A-Za-z_.]+',a))=={'propext','Classical.choice','Quot.sound'} for n,a in prints)
api=['.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean','.lake/packages/mathlib/Mathlib/Probability/Kernel/Composition/IntegralCompProd.lean','.lake/packages/mathlib/Mathlib/Probability/Kernel/Composition/MeasureCompProd.lean','.lake/packages/mathlib/Mathlib/Probability/Kernel/Disintegration/StandardBorel.lean','.lake/packages/mathlib/Mathlib/Probability/Kernel/Disintegration/Basic.lean','.lake/packages/mathlib/Mathlib/Probability/Moments/Variance.lean','.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/LinearIsometry.lean']
root=R/'runs/20261007-companion-priority'; runs=[('phase-pbps-primary-preread55/source.preread.run.json','input_artifacts','outputs'),('pbps-l2-macroscopic-mean-preproof-review55/statement.signature-stage.run.json','input_artifacts','output_artifacts'),('pbps-l2-macroscopic-mean-preproof-review55/statement.typed-admission.run.json','input_artifacts','output_artifacts'),('pbps-l2-macroscopic-mean-sourcegraph55/run.json','inputs','outputs'),('pbps-l2-macroscopic-mean-sourcegraph55/repair-overlay55/run.json','inputs','outputs'),('pbps-l2-macroscopic-mean-topology-review55/reviewer.topology.run.json','inputs','outputs'),('pbps-l2-macroscopic-mean-topology-review55/repair-review55/reviewer.topology.repaired.run.json','inputs','outputs')]
native=[];nativepins=[]; failures=[]
for p,ik,ok in runs:
 d=load(root/p);entry=selfcheck(root/p)
 for kind in [ik,ok]:
  for e in d[kind]:
   if not equal(e):failures.append(dict(run=p,kind=kind,pin=e,current=pin(e['path'])))
   else:nativepins.append(dict(run=p,kind=kind,original=e,actual=pin(e['path']),ok=True))
 entry.update(actual_input_count=len(d[ik]),actual_output_count=len(d[ok]));native.append(entry)
dump('native.preflight.json',dict(full_runs=native,pin_checks=len(nativepins)+len(failures),matching=len(nativepins),unresolved_mismatches=failures))
assert not failures,[(e['run'],e['pin']['path']) for e in failures]
negative=load(root/'pbps-l2-macroscopic-mean-topology-review55/source-topology-review.json');repair=load(root/'pbps-l2-macroscopic-mean-topology-review55/repair-review55/source-topology-review.repaired.json')
selfcheck(root/'pbps-l2-macroscopic-mean-topology-review55/source-topology-review.json','review_run_sha256');selfcheck(root/'pbps-l2-macroscopic-mean-topology-review55/repair-review55/source-topology-review.repaired.json','review_run_sha256')
assert negative['status']=='BLOCKED_SCOPED_REPRESENTATION_ONLY' and len(negative['blockers'])==2 and not negative['mathematical_or_signature_blocker_found']
assert repair['status']=='ACCEPTED_SCOPED_SOURCE_ONLY_REPRESENTATION_REPAIR' and not repair['source_signature_or_mathematical_change'] and not repair['wrong_before_mapping_found'] and not repair['corrective_mapping_needed']
leases=[]
for e in load(B/'math-freeze.json')['inputs']:
 if e['path'].endswith('.lease.json') or e['path'].endswith('/lease.json'):
  d=load(e['path']);assert all(d.get(k,'CLOSED') in ['CLOSED','NOT_STARTED_CLOSED','NOT_STARTED'] for k in ['read','write','Python','python','compiler','read_lease','write_lease','Python_lease','compiler_lease']),e['path']
  assert d.get('status','CLOSED')!='OPEN';leases.append(dict(input=pin(e['path']),native_fields=d))
attempts=[]
for e in load(B/'math-freeze.json')['inputs']:
 if '/pbps-l2-macroscopic-mean55/focused.' in e['path'] and e['path'].endswith('.status.json'):
  st=load(e['path']);lp=e['path'].replace('.status.json','.log');cl=e['path'].replace('.status.json','.compiler.lease.json');lt=path(lp).read_text(encoding='utf-8');le=load(cl)
  assert st['exit_code']==le['exit_code'] and le['status']=='CLOSED'
  sorry='sorryAx' in lt
  if sorry:assert st['exit_code']!=0
  attempts.append(dict(status=pin(e['path']),log=pin(lp),lease=pin(cl),exit_code=st['exit_code'],failed_only_compiler_sorryAx=sorry))
assert len(attempts)==11
primary=load(root/'phase-pbps-primary-preread55/primary.contract.json');selfcheck(root/'phase-pbps-primary-preread55/primary.contract.json','review_run_sha256')
inventory=load(root/'phase-pbps-primary-preread55/primary.anchor-inventory.json'); selfcheck(root/'phase-pbps-primary-preread55/primary.anchor-inventory.json','inventory_run_sha256')
source=path(primary['source_snapshot']['path']).read_bytes(); assert equal(primary['source_snapshot'])
selected=[]
for a in inventory['anchors']:
 if a['source_item_id'] in ['S1.p1.1','S1.E1','A2.E1','A2.E2','A2.E4','A2.SS2.p1.1','A2.E8','A2.SS2.p2.2','A2.E9','A2.Thmtheorem1.p2.1','A2.E13']:
  assert equal(a['raw_fragment']);selected.append(dict(source_item_id=a['source_item_id'],lines=[a['physical_start'],a['physical_end']],actual_fragment=pin(a['raw_fragment']['path']),formula_alttexts=a['formula_alttexts'],source_raw_fragment=path(a['raw_fragment']['path']).read_text(encoding='utf-8')))
dump('primary.selected.actual.json',dict(primary_whole=pin(primary['source_snapshot']['path']),selected_anchors=selected,scope='Bounded actual original standing/B1/B9/B13 source passages, no decoder/source55 verdict; Gamma/fullrough statements remain residual.'))
dump('checks.json',dict(status='PASS',actual_python_PID=os.getpid(),checked_base_commit=BASE,precommit_not_scientific55_commit=True,exact_signature_LF_bytes=2526,exact_signature_LF_sha256=sha(header),production=pin(body),Tests=pin(test),actual_five_parent_calls=[dict(input=pin(p),call=c) for p,c in parents],no_private_producer_or_new_instance=True,fake_closure_scan=scan,actual_api_inputs=[pin(p) for p in api],focused_status=pin(O/'focused.status.json'),actual_compiler_PID=load(O/'focused.status.json')['process_id'],focused_exit=0,focused_jobs=3894,forced_rebuild=False,target_replayed='Replayed Tests.ProximalBPSL2MacroscopicMean' in log,axiom_closures=[dict(declaration=n,axioms=sorted(re.findall(r'[A-Za-z_.]+',a))) for n,a in prints],preproof_complete_native_runs=native,preproof_native_pin_checks=len(nativepins),preproof_actual_CLOSED_leases=leases,preserved_original_attempts=attempts,original_topology_T55_1_2_representation_negative_and_exact_repair=True,source_selected=pin(O/'primary.selected.actual.json'),decoder55_or_source55_verdict_read=False,canonical_edits=False,state_transition=False))
dump('native.actual-pin-checks.json',dict(status='PASS',checks=nativepins))
print(json.dumps(dict(status='PASS',frozen_originals=282,exact_signature=2526,actual_five_parents=5,preproof_full_runs=7,native_pin_checks=len(nativepins),original_attempts=len(attempts),actual_focused_PID=load(O/'focused.status.json')['process_id'],standard3_closures=3)))
