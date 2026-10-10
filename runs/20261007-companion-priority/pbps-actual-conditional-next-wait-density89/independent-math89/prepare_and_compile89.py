from pathlib import Path
import ast,datetime,hashlib,json,os,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean'
MR='36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'
PRE=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text('utf8'))
def put(n,x):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
assert pin(M)['raw_sha256']==MR
seal=B/'root.statement-seal89.json';header=PRE/'header89.proposed.lean'
assert pin(seal)['raw_sha256']=='d810e6949956099186936ccdcbaf270c0a3a6572913ce1430c682ef5ae5ab5a7'
ss=read(seal);assert ss['expanded_literal_Prop'].encode() in M.read_bytes()
assert ss['header']['raw_sha256']==pin(header)['raw_sha256']=='47bb14ee9e720d22ddefa4645860d1fcd6a984cfaf2f64085e41eea1ccc9a696'
primary=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert pin(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
baseline=PRE/'pre-fetch89.workspace-RAW.json';prior=read(baseline)['tracked_modified'];assert len(prior)==21
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
put('collaborator-preservation89.json',dict(baseline=pin(baseline),RAWs=[pin(R/p) for p in prior],count=21,all_match=True))
inputs=[M,header,seal,primary,baseline,B/'focused/production6-explicit-order-comparisons/receipt.json',
 PRE/'header-math89/decision89.json',PRE/'header-math89/closed-RAW-manifest89.json',
 PRE/'header-math89/primary-source-reconstruction89.json',PRE/'header-math89/source-reconstruction89.chronology.jsonl',
 PRE/'header-math89/source-topology89.decision.json',PRE/'header-math89/source-topology89.closed-RAW-manifest.json',
 PRE/'independent-source-first89/source-proof-graph89.native.json',PRE/'independent-source-first89/source-coverage89.native.json',PRE/'independent-source-first89/source-first89.native.json',
 R/'lean-toolchain',R/'lake-manifest.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean',
 R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',
 R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',
 R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',
 R/'.lake/packages/mathlib/Mathlib/Probability/Kernel/WithDensity.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Kernel/Defs.lean',
 R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/WithDensity.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Restrict.lean',
 R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Map.lean',
 R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Map.lean',R/'tools/astis.py',
 R/'.agents/skills/astis-substantive-advance/SKILL.md',R/'.agents/skills/astis-semantic-roundtrip/SKILL.md']
assert pin(R/'lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert pin(R/'lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert head=='7c108c3181cee58bb9305445f903c5f71efda9c5'
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
put('input-freeze89.json',dict(status='FROZEN_BEFORE_INDEPENDENT_FULL_SOURCE_COMPILATION',created_utc=now(),reviewer_id='/root/exact_verify77',observed_head=head,current_frozen_module=pin(M),actual_inputs=[pin(p) for p in inputs],reused_primary_first_reconstruction_and_distinct_topology=True,whole_private_Prop_exact_seal=True,no_final_source_or_decoder_verdict_read=True,source_metadata_in_seal='Exact paths and RAW bindings seen, no final source or decoder verdict opened.',publication_not_yet_read_or_frozen=True,mathematical_role='Independent full BODY mathematics, later exact author exposition audit. Not proof author or VERIFIED admission.'))
with (O/'module89.exactraw.lean').open('xb') as f:f.write(M.read_bytes())
template=R/'runs/20261007-companion-priority/pbps-actual-finite-history-tail-law87/independent-math87/prepare_and_compile87.py'
t=ast.parse(template.read_text('utf8'))
suffix=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='suffix' for x in n.targets))
suffix=suffix.replace('ActualFiniteHistoryTailLaw','ActualConditionalNextWaitDensity').replace('actual_finite_history_tail_law','actual_conditional_next_wait_density')
probe=O/'FreshWholeSourceKernelClosure89.lean'
with probe.open('xb') as f:f.write(M.read_bytes()+suffix.encode('utf8'))
put('instrumentation-origin89.json',dict(template=pin(template),transform='Extract only the literal generic Lean command suffix. Replace exact module/theorem names, not embedded hashes or proofs. Traverses owned generated constants and recursively all ASTIS type/value dependencies.',probe=pin(probe),source_prefix_byte_identical=True))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
for n,cmd in [('fresh-focused-build',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity']),('fresh-whole-source-kernel',[lake,'env',lean,str(probe)])]:
 start=now()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 put(n+'.receipt.json',dict(command=cmd,cwd=str(R),observed_head=head,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),source=pin(M),probe=pin(probe) if n=='fresh-whole-source-kernel' else None,stdout=pin(O/(n+'.stdout.log')),stderr=pin(O/(n+'.stderr.log')),native_reasoning_trajectory_claimed=False))
 print(n,'TERMINAL_EXIT',code,flush=True);assert code==0
assert pin(M)['raw_sha256']==MR
for e in read(O/'input-freeze89.json')['actual_inputs']:assert pin(R/e['path'])==e
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
print('FRESH WHOLE SOURCE AND FOCUSED COMPILE CLOSED',flush=True)
