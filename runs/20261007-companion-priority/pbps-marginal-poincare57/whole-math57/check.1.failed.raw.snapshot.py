from common import *
assert git('rev-parse','HEAD')==BASE
originals=strict('inputs.post-analysis.json')
prod=path('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean')
test=path('Tests/GaussianMarginalPoincare.lean')
txt=prod.read_bytes().replace(b'\r\n',b'\n')
sig=txt[txt.index(b'theorem actual_gaussian_marginal_centered_poincare'):txt.index(b' := by',txt.index(b'theorem actual_gaussian_marginal_centered_poincare'))]+b'\n'
sealed=path('runs/20261007-companion-priority/pbps-marginal-poincare-preproof57/prospective-statement.txt').read_bytes().replace(b'\r\n',b'\n')
assert sig==sealed and len(sig)==1244
(O/'exact-statement.lf.txt').write_bytes(sig)
sf=load(O/'native-diagnosis.0.json'); assert len(sf['self_checks'])==47 and all(x['match'] for x in sf['self_checks'])
oldoutputs=load(O/'closed-output-diagnosis.0.json');assert oldoutputs['count']==540 and all(x['ok'] for x in oldoutputs['checks'])
closed=[]
for e in originals:
 if 'lease' in pathlib.Path(e['path']).name and e['path'].endswith('.json') and '.open.' not in e['path']:
  d=load(e['path']);assert d.get('state',d.get('status'))=='CLOSED';closed.append(pin(e['path']))
statuses=[]
for n,code in [('production.0',0),('tests.0',1),('tests.1',1),('tests.2',1),('tests.3',1),('tests.4',0)]:
 d=load(B/(n+'.status.json'));assert d['exit_code']==code
 statuses.append(dict(status=pin(B/(n+'.status.json')),data=d,accepted=code==0))
status=load(O/'focused.status.json');assert status['exit_code']==0 and status['process_id']==54196
cl=load(O/'compiler.lease.json');assert cl['status']=='CLOSED' and cl['exit_code']==0
log=(O/'focused.log').read_text(encoding='utf-8');assert 'Build completed successfully (3904 jobs).' in log
axioms=[]
for name,ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log,re.S):
 a=[x.strip() for x in ax.replace('\n',' ').split(',')];assert set(a)=={'propext','Classical.choice','Quot.sound'}
 axioms.append(dict(declaration=name,axioms=a))
assert len(axioms)==2 and axioms[0]['declaration']==TARGET
parents=load(B/'math-freeze.json')['actual_ASTIS_parents']+load(B/'math-freeze.json')['actual_test_parents']
parentfiles=[str(x).rsplit('.',1)[0].replace('.','/')+'.lean' for x in parents]
assert all(path(p).is_file() for p in parentfiles)
scans=[]
def strip(s):
 # Nested Lean block comments and line comments, preserving positions.
 out=[];i=0;depth=0
 while i<len(s):
  if s[i:i+2]=='/-':depth+=1;i+=2;continue
  if depth and s[i:i+2]=='-/':depth-=1;i+=2;continue
  if depth:i+=1;continue
  if s[i:i+2]=='--':
   j=s.find('\n',i);i=len(s) if j<0 else j;continue
  out.append(s[i]);i+=1
 assert depth==0
 return ''.join(out)
for p in [prod,test]+[path(p) for p in parentfiles]:
 code=strip(p.read_text(encoding='utf-8'))
 hits=re.findall(r'\b(?:axiom|sorry|admit)\b|Prop\s*:=\s*True|:=\s*trivial\b',code)
 assert not hits,(p,hits);scans.append(dict(input=pin(p),authored_fake_closure_hits=hits))
assert re.findall(r'\b(?:private\s+)?theorem\s+(\w+)',strip(prod.read_text(encoding='utf-8')))==['actual_gaussian_marginal_centered_poincare']
body=prod.read_text(encoding='utf-8').split(' := by',1)[1];tcode=test.read_text(encoding='utf-8')
assert all(p in body or '.'.join(p.rsplit('.',2)[-2:]) in body for p in parents[:6])
assert all(p.rsplit('.',2)[1]+'.'+p.rsplit('.',1)[1] in tcode for p in parents[6:])
extra=['.lake/packages/mathlib/Mathlib/LinearAlgebra/LinearPMap.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',
 '.lake/packages/mathlib/Mathlib/Probability/Kernel/Disintegration/Basic.lean',
 '.lake/packages/mathlib/Mathlib/Probability/Kernel/Composition/IntegralCompProd.lean',
 'runs/20261007-companion-priority/pbps-rough-mean-gradient56/whole-math56/receipt.json',
 'runs/20261007-companion-priority/pbps-rough-mean-gradient56/whole-math56/run.json',
 'runs/20261007-companion-priority/pbps-rough-mean-gradient56/whole-math56/lease.json']
prior=[selfcheck(extra[4],'receipt_sha256'),selfcheck(extra[5]),selfcheck(extra[6],'lease_sha256')]
assert load(extra[4])['verdict']=='ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER'
assert load(extra[6])['status']=='CLOSED'
pre=load(extra[4]);pre_rows=pre['inputs']
for p in parentfiles[-2:]:
 match=[x for x in pre_rows if x.get('path')==p];assert len(match)==1 and equal(match[0]),p
proofinputs=originals+[pin(B/'math-freeze.json')]+[pin(p) for p in extra]
unique={path(e['path']).as_posix():e for e in proofinputs}
dump('input.manifest.json',dict(schema_version=1,original_freeze_count=602,distinct_count=len(unique),inputs=list(unique.values()),raw_recipe='SHA256 exact file bytes',LF_recipe='SHA256 replace CRLF byte pairs only with LF',historical_input_substitution='NONE; all602 current exact originals directly matched'))
checks=dict(status='PASS',checked_base_commit=BASE,exact_signature=dict(bytes=1244,lf_sha256=sha(sig),matches_original_seal=True),
 original_pin_count=602,distinct_input_count=len(unique),native_whole_object_self_checks=sf['self_checks'],prior_review_self_checks=prior,
 original_closed_output_checks=oldoutputs,actual_prior_CLOSED_leases=closed,retained_compile_statuses=statuses,
 fake_closure_scan=scans,axiom_closures=axioms,focused_build=status,compiler_closed=cl,
 all_eight_actual_parent_calls_used=True,no_private_or_extra_production_helpers=True,
 historical_OPEN_snapshots='Preserved lease.open.json artifacts; their corresponding actual lease.json is CLOSED. No claim historical opening artifacts are terminal leases.',
 parent_reuse='Complete prior56 mathematical review reused unchanged; both actual55/56 production files match its exact inputs. Six existing public parents checked at current bodies/contracts; no copied private proof.',
 source_review_boundary='Read independently presealed statement/primary/topology and distinct consumer overlay only. No final57 source verdict, decoder output, or source admission inferred.',
 no_canonical_or_proof_edit=True,no_VERIFIED_transition=True)
dump('checks.json',checks)
print(json.dumps(dict(status='PASS',originals=602,distinct_inputs=len(unique),native_self=47,prior_self=3,closed_original_outputs=540,closed_leases=len(closed),signature_sha256=sha(sig),axioms=axioms)))
