import json,os,pathlib,re,shutil,subprocess,sys,traceback
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from math66 import R,O,D,H,BASE,ACTOR,read,write,pin,check,frozen,sha,canon,now
try:
 assert read(O/'structural-math-check.result.json')['status']=='PASS';lake=shutil.which('lake');assert lake
 manifest=read(O/'inputs.manifest.json');critical=manifest['inputs'][1:7];pre=[]
 for x in critical:check(x['original']);pre.append(pin(x['original']['path']))
 api=read(O/'inputs.api-supplement.json');assert api['Mathlib_commit']=='db584cd6d46c92f209a44c0f1c829460d327499d'
 for x in api['inputs']:check(x['original'])
 write('compiler.pre-pins.json',{'checked_base':BASE,'candidate_commit':'UNCOMMITTED','actual_runner_pid':os.getpid(),'critical_current_RAW_LF':pre,'API_input_pins':api,'utc':now()});stages=[]
 commands=[('lake-build',[lake,'build','Tests.ProximalBPSAmbientAdjointCorrector'],'Focused Lake dependency/build check; replay/cache is explicitly distinguished from fresh compilation'),('fresh-main',[lake,'env','lean','AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean'],'Fresh Lean producer proof check via direct lake env lean; reused unchanged imported dependencies'),('fresh-Test',[lake,'env','lean','Tests/ProximalBPSAmbientAdjointCorrector.lean'],'Fresh Lean genuine consumer proof check and exact two public axiom diagnostics')]
 for label,cmd,meaning in commands:
  started=now()
  with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:
   p=subprocess.Popen(cmd,cwd=R,stdout=out,stderr=err);print(json.dumps({'event':'COMPILER_START','label':label,'actual_foreground_pid':p.pid,'actual_runner_pid':os.getpid(),'meaning':meaning}),flush=True);code=p.wait()
  row={'label':label,'command':cmd,'actual_foreground_pid':p.pid,'actual_runner_pid':os.getpid(),'started_utc':started,'finished_utc':now(),'exit_code':code,'terminal_closed':True,'meaning':meaning,'stdout':pin(O/(label+'.stdout.log')),'stderr':pin(O/(label+'.stderr.log'))};write(label+'.receipt.json',row);stages.append(row);print(json.dumps({'event':'COMPILER_TERMINAL','label':label,'actual_pid':p.pid,'exit_code':code,'terminal_closed':True}),flush=True);assert code==0
  for x in critical:check(x['original'])
 build=(O/'lake-build.stdout.log').read_text(encoding='utf-8',errors='replace');fresh=(O/'fresh-Test.stdout.log').read_text(encoding='utf-8',errors='replace');assert 'Build completed successfully (3946 jobs).' in build
 axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]+)\]",fresh,re.S);names=['AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition','Tests.ProximalBPSAmbientAdjointCorrector.genuine_actual_global_corrector_consumer'];assert len(axioms)==2 and {n for n,a in axioms}==set(names)
 parsed=[]
 for n,a in axioms:
  aset=[s.strip() for s in a.replace('\n',' ').split(',')];assert set(aset)=={'propext','Classical.choice','Quot.sound'} and len(aset)==3;parsed.append({'declaration':n,'exact_axioms':aset,'standard3_only':True})
 diagnostics=[]
 for label,_,_ in commands:
  text=(O/(label+'.stdout.log')).read_text(encoding='utf-8',errors='replace')+(O/(label+'.stderr.log')).read_text(encoding='utf-8',errors='replace');assert not re.search(r'\berror:|declaration uses .sorry.|unsolved goals',text);diagnostics.append({'label':label,'warning_count':len(re.findall(r'\bwarning:',text)),'errors':0,'complete_logs_retained':True})
 post=[pin(x['original']['path']) for x in critical];assert pre==post;write('compiler.post-pins.json',{'critical_current_RAW_LF':post,'unchanged_from_pre':True,'utc':now()})
 write('focused.result.json',{'schema':'independent-math66-focused-fresh-compiler-v1','status':'PASS','checked_base':BASE,'candidate_commit':'UNCOMMITTED','actual_focused_runner_pid':os.getpid(),'stages':stages,'Lake_jobs':3946,'Lake_replay_present':('Replayed' in build),'fresh_main_proof_compiled':True,'fresh_genuine_Test_proof_compiled':True,'cache_boundary':'Lake build may replay. Both exact current source files were separately passed to fresh Lean compiler; dependencies reused. Actual Test fresh stdout supplies standard3 for both public declarations.','exact_public_axiom_parsing':parsed,'diagnostics':diagnostics,'compiler_pre_and_post_current_RAW_LF_equal':True,'no_source_or_canonical_or_ledger_writes':True,'utc':now()})
 print(json.dumps({'status':'PASS','actual_runner_pid':os.getpid(),'jobs':3946,'fresh_main_and_Test':True,'two_public_declarations_standard3_only':True}),flush=True)
except Exception as e:
 write('focused.failure.json',{'status':'FAIL','actual_pid':os.getpid(),'exception':repr(e),'traceback':traceback.format_exc(),'utc':now()});raise
