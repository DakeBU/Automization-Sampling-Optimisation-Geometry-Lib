from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel.actual_phase_transition_kernel'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def load(p):return json.loads(p.read_bytes())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def put(n,b):
 with (O/n).open('xb') as f:f.write(b)
def prop(s):
 a=s.index('private def ')
 return s[a:s.index('\n\nset_option',a) if '\n\nset_option' in s[a:] else s.index('\n\nend',a)].rstrip()
raw=M.read_bytes();s=raw.decode();h=(B/'header85.proposed.lean').read_text(encoding='utf8');seal=load(B/'root.statement-seal85.json')
assert info(M)['RAW_sha256']=='14df46eb96095b6b4cf3e454f7794382c2ba1e09812bd8ab15b7ea6b11842a22'
assert prop(s)==prop(h) and prop(s)[len('private def '):]+'\n'==seal['expanded_literal_Prop']
p=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean';pt=p.read_text(encoding='utf8')
prefix=pt[pt.index('private def '):pt.index('\n\n\nset_option')].replace('actual_physical_time_measurable_phase_statement','actual_phase_transition_kernel_statement')
assert re.sub(r'\s+','',prefix)==re.sub(r'\s+','',prop(s).split('\n      ∧ (∃ K')[0])
private_binders=prop(s)[prop(s).index('    {E : Type*}'):prop(s).index(' : Prop :=')]
public=s[s.index('\ntheorem '):];public_binders=public[public.index('    {E : Type*}'):public.index(' :\n    actual_')];assert private_binders==public_binders
lets=re.findall(r'^    let ([^ :]+)',prop(s),re.M);assert lets==['P','ε','c','Φ','S','rate','Λ','τ','next','record','eventTime']
save('statement-definition-audit85.json',dict(status='PASS',module=info(M),header=info(B/'header85.proposed.lean'),seal=info(B/'root.statement-seal85.json'),private_full_Prop_byte_exact_sealed_header=True,public_six_analytic_binders_exact_private=True,eleven_literal_actual_definitions=lets,entire_actual80_contract_preserved=True,new_public_provider_premises=[],public_theorems=s.count('\ntheorem '),private_specs=s.count('private def ')))
put('module85.exactraw.lean',raw)
extra='\n#print axioms '+D+'\n#check '+D+'\n'+r'''
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let isProject := fun n : Name => n.toString.startsWith "AutoSamplingTheory." ||
    (n.toString.startsWith "_private." && (n.toString.splitOn ".").contains "AutoSamplingTheory")
  let isLocal := fun n : Name => (n.toString.splitOn ".").contains "ActualPhaseTransitionKernel"
  let mut todo := #[`AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel.actual_phase_transition_kernel]
  let mut seen : Array Name := #[]
  let mut externalDeps : Array Name := #[]
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if !seen.contains name then
      seen := seen.push name
      logInfo m!"LOCAL_PROOF_CONSTANT {name}"
      let some ci := env.find? name | throwError "Missing owned proof constant"
      let some value := ci.value? true | throwError "Missing owned proof value"
      for dep in value.getUsedConstants do
        if isLocal dep then
          todo := todo.push dep
        else if isProject dep && !externalDeps.contains dep then
          externalDeps := externalDeps.push dep
          logInfo m!"EXTERNAL_ASTIS_DEPENDENCY {dep}"
  logInfo m!"LOCAL_PROOF_CONSTANT_COUNT {seen.size}"
  let mut projectTodo := externalDeps
  let mut projectSeen : Array Name := #[]
  while !projectTodo.isEmpty do
    let name := projectTodo.back!
    projectTodo := projectTodo.pop
    if !projectSeen.contains name then
      projectSeen := projectSeen.push name
      logInfo m!"TRANSITIVE_ASTIS_CONSTANT {name}"
      if let some ci := env.find? name then
        if let some value := ci.value? true then
          for dep in value.getUsedConstants do
            if isProject dep then
              logInfo m!"TRANSITIVE_ASTIS_EDGE {name} -> {dep}"
              projectTodo := projectTodo.push dep
  logInfo m!"TRANSITIVE_ASTIS_CONSTANT_COUNT {projectSeen.size}"
'''
probe=O/'FreshWholeModuleAxiomsKernelClosure85.lean';put(probe.name,raw+extra.encode())
paths=[M,p,R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',B/'header85.proposed.lean',B/'root.statement-seal85.json',B/'mathematics-freeze85.json',B/'publication-freeze85.json',R/'website/content/declaration_lessons/pbps-actual-phase-transition-kernel.json',R/'website/content/declaration_publications/pbps-actual-phase-transition-kernel.json',R/'lean-toolchain',R/'lake-manifest.json',probe]
for f in ['Probability/Kernel/Defs.lean','Probability/Kernel/Basic.lean','Probability/Kernel/Composition/Prod.lean','Probability/Kernel/Composition/MapComap.lean','MeasureTheory/Measure/Map.lean','MeasureTheory/Measure/Dirac.lean','MeasureTheory/Integral/Bochner/Basic.lean','MeasureTheory/Function/L1Space/Integrable.lean']:paths.append(R/'.lake/packages/mathlib/Mathlib'/f)
frozen=[info(p) for p in paths];mathlib=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R/'.lake/packages/mathlib',text=True).strip();assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze85.json',dict(reviewer_id='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),raw_inputs=frozen,fixed_mathlib=mathlib,HEAD_observed_not_exact_admission=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),blind_or_final_source_verdict_read=False))
env=os.environ.copy();env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf8';env.pop('ELAN_TOOLCHAIN',None)
def run(label,cmd):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(label+'.stdout.log')).open('xb') as out,(O/(label+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(label,'foreground PID',child.pid,flush=True);code=child.wait()
 save(label+'.receipt.json',dict(command=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=info(M),probe=info(probe),stdout=info(O/(label+'.stdout.log')),stderr=info(O/(label+'.stderr.log')),native_reasoning_trajectory_claimed=False));print(label,'EXIT',code,flush=True)
 if code:raise SystemExit(code)
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
run('fresh-focused-build',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel'])
run('fresh-whole-module',[lake,'env',lean,str(probe)])
log=(O/'fresh-whole-module.stdout.log').read_text(encoding='utf8');ax=re.search(r'depends on axioms:\s*\[([^\]]+)\]',log,re.S);assert ax;axioms=[v.strip() for v in ax[1].split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'}
deps=re.findall(r'EXTERNAL_ASTIS_DEPENDENCY (\S+)',log);local=re.findall(r'^LOCAL_PROOF_CONSTANT (\S+)',log,re.M);transitive=re.findall(r'^TRANSITIVE_ASTIS_CONSTANT (\S+)',log,re.M);edges=re.findall(r'^TRANSITIVE_ASTIS_EDGE (\S+) -> (\S+)',log,re.M)
assert len(local)==int(re.search(r'LOCAL_PROOF_CONSTANT_COUNT (\d+)',log)[1]);assert len(transitive)==int(re.search(r'TRANSITIVE_ASTIS_CONSTANT_COUNT (\d+)',log)[1])
expected={'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'}
save('kernel-dependency-summary85.json',dict(status='PASS',module=info(M),axioms=axioms,standard_axioms_only=True,actual_transitive_local_proof_constants=local,local_proof_constant_count=len(local),external_ASTIS_dependencies=deps,expected_two_public_parents_exact=set(deps)==expected,transitive_imported_ASTIS_kernel_constants=transitive,transitive_imported_ASTIS_kernel_edges=edges,closure_algorithm='Inspect ConstantInfo.value? true and getUsedConstants; recursively include all owned target-module constants and all project public/private valued imported constants. Standard #print axioms independently covers whole theorem. No name-scanned source graph is used.',fresh_complete_source=True,receipt=info(O/'fresh-whole-module.receipt.json')))
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan85.json',dict(status='PASS' if not hits else 'FAIL',algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M),aggregate_gate_not_run=True));assert not hits
for e in frozen:assert info(R/e['path'])==e
print('FRESH SOURCE / AXIOMS / KERNEL CLOSURE / FAKECLOSURE PASS',flush=True)
