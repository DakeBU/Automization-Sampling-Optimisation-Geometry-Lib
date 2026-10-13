from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;H=B/'header88.proposed.lean'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(Path(p).read_text('utf8'))
def put(n,x):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
assert pin(H)['raw_sha256']=='89890948b0716e9e8a0a4e4d5c634aa166361b7fb1575f57e751d49e024aeed3'
parent_paths=[R/('AutoSamplingTheory/ExampleCases/ProximalBPS/'+n+'.lean') for n in ['ActualHazardClock','ActualFiniteJumpRecursion','ActualFiniteHistoryTailLaw']]
h=H.read_text('utf8');p75,p76,p87=[p.read_text('utf8') for p in parent_paths]
def sig(s):return s[s.index('    {E : Type*}'):s.index(' : Prop :=')]
assert sig(h)==sig(p75)==sig(p76)==sig(p87)
def defs(s):
 s=s[s.index('private def '):];s=s[:s.index('\nset_option maxHeartbeats')] if '\nset_option maxHeartbeats' in s else s[:s.index('\n#check')]
 starts=list(re.finditer(r'^    let ([^\s:]+).*',s,re.M));out={}
 for i,m in enumerate(starts):
  if i+1==len(starts):break
  out[m.group(1)]=s[m.start():starts[i+1].start()].rstrip()
 # Last definition ends at top-level statement clause rather than theorem suffix.
 m=starts[-1];rest=s[m.start():];k=rest.index('\n    ∀ y xRef') if '\n    ∀ y xRef' in rest else None
 if k is not None:out[m.group(1)]=rest[:k].rstrip()
 return out
hd=defs(h);d75,d76,d87=[defs(s) for s in [p75,p76,p87]]
actual=['c','Φ','S','rate','Λ','τ','next','record'];shared=actual+['P','ε','history']
for n in actual:assert hd[n]==d76[n],n
for n in shared:assert hd[n]==d87[n],n
for n in ['c','Φ','rate','Λ','τ']:assert hd[n]==d75[n],n
assert list(hd)==shared+['liveSurvival','survivalWeight'] and len(hd)==13
assert not re.search(r'\b(sorry|axiom|admit)\b',h) and 'theorem ' not in h
baseline=B/'pre-fetch88.workspace-RAW.json';prior=read(baseline)['tracked_modified'];assert len(prior)==21
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
put('collaborator-preservation88.json',dict(baseline=pin(baseline),count=21,RAWs=[pin(R/p) for p in prior]))
inputs=[H,B/'header88.pre-review.json',baseline,*parent_paths,R/'lean-toolchain',R/'lake-manifest.json',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Map.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Order.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Independence/InfinitePi.lean',R/'.agents/skills/astis-semantic-roundtrip/SKILL.md',R/'.agents/skills/astis-substantive-advance/SKILL.md']
assert pin(R/'lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477' and pin(R/'lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
put('input-freeze88.json',dict(created_utc=now(),reviewer_id='/root/exact_verify77',observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),actual_math_inputs=[pin(p) for p in inputs],parent_read_scope='Actual75 complete private Prop and next private ingredient signature; actual76 complete private Prop/public signature and initial literal BODY definitions; actual87 complete private Prop/public signature. No88 production theorem BODY exists or is created.',source_topology_scope='Separate additional source-only audit; primary reconstruction after prior candidate exposure explicitly recorded before author graph read. No source author candidate acceptance verdict read.',proof_credit=False))
put('definition-readback88.json',dict(status='EXACT_SIX_BINDERS_AND_LITERAL_ACTUAL_DEFINITIONS_PRESERVED',six_analytic_binders=['hα','hαβ','hV','hH','hη','hβη'],binder_block_identical_to_parents75_76_87=True,thirteen_literal_definitions=list(hd),exact_eleven_shared87_definitions=shared,exact_eight_actual76_definitions=actual,exact_five_hazard75_definitions=['c','Φ','rate','Λ','τ'],line_ending_read_normalization_only=True,raw_file_bytes_unmodified=True,per_definition_text_sha256={n:hashlib.sha256(s.encode()).hexdigest() for n,s in hd.items()},live_guard='live last record: finite duration u < actual extended tau(clipped fresh real clock); stopped: False. No fictitious next phase or wait after stop.',weight='live: ENNReal.ofReal(exp(-literal Lambda(state,u))); stopped:0. All finite histories allowed, including structurally inconsistent abstract histories; pointwise hazard laws apply to any phase.',test_class='Measurable d is the admissible deterministic history-duration function class; MeasurableSet A is the admissible history event class. Neither is an extra analytic PBPS hypothesis or a proof/provider certificate.',association='Full history Fin(n+1)→tagged finite records; joint event domain History×(Nat→Real). Last record indexn and next raw tail0=w n match exactly.'))
snap=O/'header88.exactraw.snapshot.lean'
with snap.open('xb') as f:f.write(H.read_bytes())
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
lake=R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe';lean=R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe';cmd=[str(lake),'env',str(lean),str(snap)];start=now()
with (O/'whole-header-typecheck88.stdout.log').open('xb') as out,(O/'whole-header-typecheck88.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('whole-header-typecheck88 foreground PID',child.pid,flush=True);code=child.wait()
put('whole-header-typecheck88.receipt.json',dict(command=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),header=pin(H),exact_snapshot=pin(snap),stdout=pin(O/'whole-header-typecheck88.stdout.log'),stderr=pin(O/'whole-header-typecheck88.stderr.log'),toolchain=pin(R/'lean-toolchain'),lake_manifest=pin(R/'lake-manifest.json'),complete_named_private_Prop=True,proof_credit=False))
for p in inputs:assert pin(p) in read(O/'input-freeze88.json')['actual_math_inputs']
for p,v in prior.items():assert pin(R/p)['raw_sha256']==v
print('whole-header-typecheck88 TERMINAL_EXIT',code,flush=True);assert code==0
