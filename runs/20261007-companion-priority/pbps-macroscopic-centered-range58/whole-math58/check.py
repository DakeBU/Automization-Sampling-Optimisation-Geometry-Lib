from common import *
sys.stdout.reconfigure(encoding='utf8');sys.path.insert(0,str(R));sys.path.insert(0,str(R/'tools'))
from tools import astis
rows=load(B/'math-freeze.json')['inputs'];assert len(rows)==72
inputs={};checks=[];selfs=[]
def current(p):a=pin(p);inputs[a['path']]=a;return a
for e in rows:
 a=current(e['path']);assert same(e,a);checks.append(dict(original=e,actual=a))
current(B/'math-freeze.json')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==BASE
files=['AutoSamplingTheory/TechnicalLemmas/Measure/L2PullbackRange.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean','Tests/ProximalBPSMacroscopicRange.lean'];names=['l2_pullback_range_eq_lpMeas','actual_macroscopic_centered_range','actual_centered_macro_contraction_and_defect_gap'];seals=['generic-prospective-statement.txt','prospective-statement.txt','consumer-prospective-statement.txt'];signatures=[]
for f,n,s in zip(files,names,seals):
 code=path(f).read_bytes().replace(b'\r\n',b'\n').decode('utf8');start=code.index('theorem '+n);end=code.index(' := by',start);header=(code[start:end]+'\n').encode();sealed=(R/'runs/20261007-companion-priority/pbps-macro-range-preproof58'/s).read_bytes().replace(b'\r\n',b'\n');assert header==sealed,(f,len(header),len(sealed));signatures.append(dict(declaration=n,actual_header_bytes=len(header),actual_header_LF_sha256=sha(header),exact_original_seal=current(R/'runs/20261007-companion-priority/pbps-macro-range-preproof58'/s),current_source=current(f)))
api=['Mathlib/MeasureTheory/Function/FactorsThrough.lean','Mathlib/MeasureTheory/Function/ConditionalExpectation/AEMeasurable.lean','Mathlib/MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean','Mathlib/MeasureTheory/Function/LpSeminorm/Basic.lean','Mathlib/MeasureTheory/Function/LpSpace/Basic.lean','Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean']
api_pins=[current(R/'.lake/packages/mathlib'/p) for p in api];current(R/'tools/astis.py')
for d,n in [('pbps-macro-range-preproof-review58','reviewer.run.json'),('pbps-macro-range-preproof-review58','lease.json')]:
 p=R/'runs/20261007-companion-priority'/d/n;x=load(p);field='content_self_sha256';h=logical({k:v for k,v in x.items() if k!=field});assert h==x[field];selfs.append(dict(input=current(p),self_field=field,logical_sha256=h,recipe='Entire complete object minus ONLY named top-level field; sorted compact UTF8 JSON')); 
 if n=='lease.json':assert x['status']=='CLOSED'
prior=R/'runs/20261007-companion-priority/pbps-marginal-poincare57/verified.json';p=load(prior);assert p['status']=='VERIFIED' and p['verifier_id']=='whole_math52_exact57';assert logical({k:v for k,v in p.items() if k!='verified_sha256'})==p['verified_sha256'];selfs.append(dict(input=current(prior),self_field='verified_sha256',logical_sha256=p['verified_sha256'],recipe='Entire native object minus ONLY verified_sha256; bounded existing57 certificate reuse, no recursive replay'))
status=load(O/'focused.status.json');cl=load(O/'compiler.lease.json');assert status['actual_exit_code']==0 and cl['status']=='CLOSED' and cl['actual_compiler_exit_code']==0
log=(O/'focused.log').read_text(encoding='utf8');assert 'Build completed successfully (3908 jobs)' in log and pin(O/'focused.log')['raw_sha256']==status['log']['raw_sha256']
prefixes=['AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange.','AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange.','Tests.ProximalBPSMacroscopicRange.']
closures=[dict(declaration=n,axioms=[z.strip() for z in a.split(',')]) for n,a in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",log,re.S) if any(n.startswith(p) for p in prefixes)];assert len(closures)==3 and all(set(x['axioms'])=={'propext','Classical.choice','Quot.sound'} for x in closures)
fake=[]
for f in files+['AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean','Tests/GaussianMarginalPoincare.lean']:
 code=astis.strip_lean_comments_and_strings(path(f).read_text(encoding='utf8'));hits=[i for i,l in enumerate(code.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;fake.append(dict(input=current(f),findings=hits))
rootroutes=[]
for n in ['generic.0','generic.1','macro.0','macro.1','tests.0','tests.1','tests.2']:
 st=load(B/(n+'.status.json'));ls=load(B/(n+'.compiler.lease.json'));assert ls['status']=='CLOSED' and ls['exit_code']==st['exit_code'];assert pin(B/(n+'.log'))['raw_sha256']==st['log_raw_sha256'];rootroutes.append(dict(route=n,status=current(B/(n+'.status.json')),lease=current(B/(n+'.compiler.lease.json')),log=current(B/(n+'.log')),actual_PID=st['process_id'],actual_exit_code=st['exit_code'],failed_elaboration_only_sorryAx=('sorryAx' in (B/(n+'.log')).read_text(encoding='utf8')) if st['exit_code'] else False))
assert [x['actual_exit_code'] for x in rootroutes]==[1,0,1,0,1,1,0]
assert 'sorryAx' not in log
dump('checks.json',dict(status='PASS_COMPLETE_PRECOMMIT_MATHEMATICS58',checked_base_commit=BASE,original_pin_count=72,actual_original_pin_checks=checks,exact_signatures=signatures,pinned_API_files=api_pins,native_bounded_parent_selfchecks=selfs,current_successful_closures=closures,fake_closure_scan=fake,root_retained_actual_routes=rootroutes,independent_focused_status=status,actual_compiler_closed=pin(O/'compiler.lease.json'),complete_mathematical_reasons=pin(O/'mathematical-reasons.json'),actual_private_helpers=0,all_three_new_bodies_reviewed=True,original_proof_and_statement_unchanged=True,postproof_source_decoder_verdict_read=False,no_source_fidelity_verdict=True,no_VERIFIED_transition=True,no_canonical_edit=True))
dump('inputs.json',dict(status='PASS',original_count=72,actual_distinct_count=len(inputs),inputs=[inputs[k] for k in sorted(inputs)],recipe='Actual exact raw and only CRLF pairs -> LF; exact byte lengths. No recursive old snapshot inventories or administrative hash fallback.'))
print(json.dumps(dict(status='PASS_COMPLETE_PRECOMMIT_MATHEMATICS58',original_count=72,distinct_inputs=len(inputs),exact_signatures=[dict(name=x['declaration'],bytes=x['actual_header_bytes'],lf_sha256=x['actual_header_LF_sha256']) for x in signatures],actual_compiler_PID=status['actual_compiler_PID'],actual_exit_code=0,jobs=3908,standard_axiom_closures=len(closures),fake_scan_files=len(fake))))
