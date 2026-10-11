from pathlib import Path
import ast,datetime,hashlib,json,os,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
PRE=R/'runs/20261007-companion-priority/pbps-next-history-extension-preread90'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean'
MR='6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text('utf8'))
def put(n,x):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
assert pin(M)['raw_sha256']==MR
seal=B/'root.statement-seal90.json';header=PRE/'header90.v2.proposed.lean'
assert pin(seal)['raw_sha256']=='29f7e3600b6712794943f3dc6b472dd8b53cb03435a803fe54d450c0396a9028'
ss=read(seal);assert ss['expanded_literal_Prop'].encode() in M.read_bytes()
assert ss['header']['raw_sha256']==pin(header)['raw_sha256']=='5c976dcfe91fe074db71ddbf13385086735c41c273e937b0c6ef432b7dba9037'
assert read(O/'primary-reread90.chronology.json')['production_BODY_read_yet'] is False
baseline=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89/pre-fetch89.workspace-RAW.json'
prior=read(baseline)['tracked_modified'];assert len(prior)==21
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
put('collaborator-preservation90.initial.json',{'baseline':pin(baseline),'all_21_match':True,'files':[pin(R/p) for p in prior]})
inputs=[M,seal,header,baseline,B/'focused/production2-explicit-tuple-API/receipt.json',
 PRE/'independent-header-math90/decision90.json',PRE/'independent-header-math90/closed-RAW-manifest90.json',
 PRE/'independent-header-math90/topology-admission90.json',PRE/'independent-topology90/independent-primary-math-reconstruction90.json',
 PRE/'independent-topology90/primary-first90.chronology.json',PRE/'source-proof-graph90.accepted-successor.json',
 PRE/'independent-source-first90/source-coverage90.native.json',PRE/'independent-topology-repair90/decision90.native.json',
 R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html',
 PRE/'independent-topology90/.private.primary90.full-A1-A2.exact-spans.json',
 R/'lean-toolchain',R/'lake-manifest.json',
 R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean',
 R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean',
 R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean',
 R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',
 R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',
 R/'runs/20261007-companion-priority/pbps-actual-conditional-next-wait-density89/independent-math89/prepare_and_compile89.py',
 R/'runs/20261007-companion-priority/pbps-actual-conditional-next-wait-density89/independent-math89/analyze_kernel89.py',
 R/'.lake/packages/mathlib/Mathlib/Data/Fin/Tuple/Basic.lean',
 R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Map.lean',
 R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Basic.lean',
 R/'tools/astis.py']
assert pin(R/'lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert pin(R/'lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
put('historical-probe-filename-lookup90.negative.json',{'status':'TYPED_REVIEWER_LOOKUP_ERROR_BEFORE_ANY_COMPILER','tool_chunk':'d1c626','exit_code':1,'attempted_missing_paths':['independent-math89/KernelProbe89.lean','independent-math89/run_kernel89.py'],'actual_files_then_read':['independent-math89/prepare_and_compile89.py','independent-math89/analyze_kernel89.py'],'mathematical_failure':False,'no_file_or_native_proof_record_changed':True})
put('input-freeze90.json',{'status':'FROZEN_BEFORE_INDEPENDENT_FULL_SOURCE_COMPILATION','created_utc':now(),'reviewer_id':'/root/exact_verify77','observed_head':head,'current_frozen_module':pin(M),'actual_inputs':[pin(p) for p in inputs],'whole_private_Prop_exact_seal':True,'primary_reread_before_BODY':pin(O/'primary-reread90.chronology.json'),'no_final_source_or_decoder_verdict_read':True,'publication_not_yet_read_or_frozen':True,'role':'Independent whole BODY mathematics and kernel review, no proof author/VERIFIED.'})
with (O/'module90.exactraw.lean').open('xb') as f:f.write(M.read_bytes())
template=R/'runs/20261007-companion-priority/pbps-actual-finite-history-tail-law87/independent-math87/prepare_and_compile87.py'
t=ast.parse(template.read_text('utf8'))
suffix=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='suffix' for x in n.targets))
suffix=suffix.replace('ActualFiniteHistoryTailLaw','ActualFiniteHistoryExtension').replace('actual_finite_history_tail_law','actual_finite_history_extension')
probe=O/'FreshWholeSourceKernelClosure90.lean'
with probe.open('xb') as f:f.write(M.read_bytes()+suffix.encode('utf8'))
put('instrumentation-origin90.json',{'template':pin(template),'transform':'Extract only generic literal Lean command suffix and replace exact module/theorem names; no hash/proof edits. Traverse owned generated constants then every ASTIS type/value dependency.','probe':pin(probe),'source_prefix_byte_identical':True})
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
for n,cmd in [('fresh-focused-build',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension']),('fresh-whole-source-kernel',[lake,'env',lean,str(probe)])]:
 start=now()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 put(n+'.receipt.json',{'command':cmd,'cwd':str(R),'observed_head':head,'actual_foreground_PID':child.pid,'exit_code':code,'terminal_closed':True,'started_utc':start,'finished_utc':now(),'source':pin(M),'probe':pin(probe) if n=='fresh-whole-source-kernel' else None,'stdout':pin(O/(n+'.stdout.log')),'stderr':pin(O/(n+'.stderr.log')),'native_reasoning_trajectory_claimed':False})
 print(n,'TERMINAL_EXIT',code,flush=True);assert code==0
assert pin(M)['raw_sha256']==MR
for e in read(O/'input-freeze90.json')['actual_inputs']:assert pin(R/e['path'])==e
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
print('FRESH_FOCUSED_AND_WHOLE_SOURCE_CLOSED_EXPOSITION_PENDING',flush=True)
