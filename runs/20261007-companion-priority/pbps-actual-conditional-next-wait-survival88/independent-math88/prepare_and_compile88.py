from pathlib import Path
import ast, datetime, hashlib, json, os, subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean'
MR='2f509ce49343d349f7a9fb21d2f7b1697c1a6de942353f6cd8ff16d522911569'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival.actual_conditional_next_wait_survival'
P88=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-preread88'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text('utf8'))
def put(n,x):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
assert pin(M)['raw_sha256']==MR
seal=B/'root.statement-seal88.json';header=P88/'header88.proposed.lean'
ss=read(seal);assert ss['expanded_literal_Prop'].encode() in M.read_bytes()
assert ss['header']['raw_sha256']==pin(header)['raw_sha256']=='89890948b0716e9e8a0a4e4d5c634aa166361b7fb1575f57e751d49e024aeed3'
baseline=P88/'pre-fetch88.workspace-RAW.json';prior=read(baseline)['tracked_modified'];assert len(prior)==21
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
put('collaborator-preservation88.json',dict(baseline=pin(baseline),count=21,RAWs=[pin(R/p) for p in prior]))
inputs=[M,header,seal,baseline,B/'focused/production6-sum-observable-equality/receipt.json',B/'publication-freeze88.json',
 R/'website/content/declaration_lessons/pbps-actual-conditional-next-wait-survival.json',R/'website/content/publications/pbps-actual-conditional-next-wait-survival.json',
 P88/'header-math88/decision88.json',P88/'header-math88/closed-RAW-manifest88.json',P88/'header-math88/topology-review88.json',P88/'header-math88/definition-readback88.json',
 P88/'independent-source-first88/source-proof-slice88.native.json',P88/'independent-source-first88/source-coverage88.native.json',P88/'independent-source-first88/source-first88.freeze.native.json',
 R/'lean-toolchain',R/'lake-manifest.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',
 R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Map.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Indicator.lean',
 R/'.agents/skills/astis-substantive-advance/SKILL.md',R/'.agents/skills/astis-semantic-roundtrip/SKILL.md']
assert pin(R/'lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert pin(R/'lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
put('input-freeze88.json',dict(status='FROZEN_BEFORE_INDEPENDENT_FULL_SOURCE_COMPILATION',created_utc=now(),reviewer_id='/root/exact_verify77',observed_head=head,current_frozen_module=pin(M),actual_inputs=[pin(p) for p in inputs],source_slice_only=True,no_final_source_or_decoder_verdict_read=True,whole_private_Prop_exact_seal=True,seal_source_review_fields='Paths/RAW identities present in seal seen; their source verdict contents not opened.',mathematical_role='Full BODY independent mathematics and exposition; not prospective-header-only acceptance or exact science VERIFIED admission.'))
with (O/'module88.exactraw.lean').open('xb') as f:f.write(M.read_bytes())
for p,n in [(R/'website/content/declaration_lessons/pbps-actual-conditional-next-wait-survival.json','lesson88.original.exactraw.json'),(R/'website/content/publications/pbps-actual-conditional-next-wait-survival.json','publication88.original.exactraw.json')]:
 with (O/n).open('xb') as f:f.write(p.read_bytes())
# Reuse only our previously accepted command instrumentation, not its verdict or proof.
template=R/'runs/20261007-companion-priority/pbps-actual-finite-history-tail-law87/independent-math87/prepare_and_compile87.py'
t=ast.parse(template.read_text('utf8'))
suffix=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='suffix' for x in n.targets))
suffix=suffix.replace('ActualFiniteHistoryTailLaw','ActualConditionalNextWaitSurvival').replace('actual_finite_history_tail_law','actual_conditional_next_wait_survival')
probe=O/'FreshWholeSourceKernelClosure88.lean'
with probe.open('xb') as f:f.write(M.read_bytes()+suffix.encode('utf8'))
put('instrumentation-origin88.json',dict(template=pin(template),transform='Extract only literal suffix constant; replace exact module/theorem identifiers. No prior theorem proof or verdict reused. Instrumentation traverses owned generated constants then recursively all project type/value dependencies.',probe=pin(probe),source_prefix_byte_identical=True))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
for n,cmd in [('fresh-focused-build',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival']),('fresh-whole-source-kernel',[lake,'env',lean,str(probe)])]:
 start=now()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 put(n+'.receipt.json',dict(command=cmd,cwd=str(R),observed_head=head,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),source=pin(M),probe=pin(probe) if n=='fresh-whole-source-kernel' else None,stdout=pin(O/(n+'.stdout.log')),stderr=pin(O/(n+'.stderr.log')),native_reasoning_trajectory_claimed=False))
 print(n,'TERMINAL_EXIT',code,flush=True);assert code==0
assert pin(M)['raw_sha256']==MR
for e in read(O/'input-freeze88.json')['actual_inputs']:assert pin(R/e['path'])==e
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
print('FRESH WHOLE SOURCE AND FOCUSED COMPILE CLOSED',flush=True)
