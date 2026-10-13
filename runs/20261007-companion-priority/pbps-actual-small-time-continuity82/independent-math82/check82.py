from pathlib import Path
import hashlib,json,re,datetime,subprocess,os,sys
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82';O=B/'independent-math82'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity.actual_small_time_stochastic_continuity'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def txt(p):return p.read_text(encoding='utf8')
raw=M.read_bytes();s=txt(M);h=txt(B/'header82.proposed.lean');seal=load(B/'root.statement-seal82.json')
assert info(M)['RAW_sha256']=='a5d0303f2f426e0029ddec2fbd56ba8f95670ce533e560d18e473c6111ef74d0'
def prop(t):
 a=t.index('private def ');end=t.index('\n\nset_option',a) if '\n\nset_option' in t[a:] else t.index('\n\nend',a);return t[a:end].rstrip()
assert prop(s)==prop(h) and prop(s)[len('private def '):]+'\n'==seal['expanded_literal_Prop']
public=s[s.index('\ntheorem ')+1:]
def binders(t):
 a=t.index('    {E : Type*}');return t[a:t.index(' : Prop :=',a) if ' : Prop :=' in t[a:] else t.index(' :\n    actual_',a)]
assert binders(s)==binders(public)
def lets(t,indent,end):
 found=list(re.finditer(r'^'+(' '*indent)+r'let (\S+)\s*:',t,re.M));d={}
 for i,m in enumerate(found):
  stop=found[i+1].start() if i+1<len(found) else t.index(end,m.start());d[m.group(1)]='\n'.join(v[indent:] if v.startswith(' '*indent) else v for v in t[m.start():stop].rstrip().splitlines())
 return d
hd=lets(prop(s),4,'    ∃ Z');body=public[public.index(':= by')+len(':= by'):public.index('  obtain ⟨Z')]
assert hd==lets(body+'  obtain ⟨Z',2,'  obtain ⟨Z') and len(hd)==11
names=['ActualPhysicalTimeMeasurability','ActualHazardClock','ActualHarmonicFlow'];parents=[R/('AutoSamplingTheory/ExampleCases/ProximalBPS/'+n+'.lean') for n in names]
parent77=R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean';parents.append(parent77)
assert hd==lets(txt(parents[0]).split('\nset_option maxHeartbeats')[0],4,'    ∃ Z')
marker='        Z y xRef z₀ 0 sample = z₀)'
def zproperties(t):return t[t.index('    ∃ Z'):t.index(marker)+len(marker)]
assert zproperties(s)==zproperties(txt(parents[0]))
save('statement-definition-audit82.json',dict(status='PASS',module=info(M),header=info(B/'header82.proposed.lean'),seal=info(B/'root.statement-seal82.json'),complete_private_Prop_exact_sealed_header=True,public_six_binders_exact_private=True,eleven_initial_BODY_lets_exact_private_and80=list(hd),all_four80_Z_properties_preserved=True,new_public_provider_premises=[],public_theorem_count=s.count('\ntheorem '),private_specification_count=s.count('private def ')))
with (O/'module82.exactraw.lean').open('xb') as f:f.write(raw)
extra='\n#print axioms '+D+'\n#check '+D+'\n'+'''open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let stem := "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity.actual_small_time_stochastic_continuity"
  let mut todo := #[`AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity.actual_small_time_stochastic_continuity]
  let mut seen : Array Name := #[]
  let mut externalDeps : Array Name := #[]
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if !seen.contains name then
      seen := seen.push name
      logInfo m!"LOCAL_PROOF_CONSTANT {name}"
      let some ci := env.find? name | throwError "Missing local proof constant"
      let some value := ci.value? true | throwError "Missing local proof value"
      for dep in value.getUsedConstants do
        if dep.toString.startsWith stem then
          todo := todo.push dep
        else if dep.toString.startsWith "AutoSamplingTheory." && !externalDeps.contains dep then
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
            if dep.toString.startsWith "AutoSamplingTheory." then
              logInfo m!"TRANSITIVE_ASTIS_EDGE {name} -> {dep}"
              projectTodo := projectTodo.push dep
  logInfo m!"TRANSITIVE_ASTIS_CONSTANT_COUNT {projectSeen.size}"
'''
probe=O/'FreshWholeModuleAxiomsKernelClosure82.lean'
with probe.open('xb') as f:f.write(raw+extra.encode('utf8'))
paths=[M,*parents,B/'header82.proposed.lean',B/'root.statement-seal82.json',B/'mathematics-freeze82.json',R/'lean-toolchain',R/'lake-manifest.json',probe]
frozen=[info(p) for p in paths];mathlib=subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip();assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze82.json',dict(reviewer='/root/exact_verify77',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=frozen,fixed_mathlib=mathlib,head_observed_not_exact_admission=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),blind_or_source_verdict_read=False))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(probe)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'fresh-whole-module.stdout.log').open('xb') as out,(O/'fresh-whole-module.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('Fresh complete source foreground PID',child.pid,flush=True);code=child.wait()
save('fresh-whole-module.receipt.json',dict(command_argv=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),full_source_prefix_exact=True,source=info(M),probe=info(probe),stdout=info(O/'fresh-whole-module.stdout.log'),stderr=info(O/'fresh-whole-module.stderr.log'),canonical_olean_written=False,native_reasoning_trajectory_claimed=False))
print('FRESH SOURCE EXIT',code,flush=True)
if code:raise SystemExit(code)
log=txt(O/'fresh-whole-module.stdout.log');ax=re.search(r'depends on axioms:\s*\[([^\]]+)\]',log,re.S);assert ax;axioms=[v.strip() for v in ax[1].split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'}
deps=re.findall(r'EXTERNAL_ASTIS_DEPENDENCY (\S+)',log);expected={'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'};assert set(deps)==expected,deps
local=re.findall(r'^LOCAL_PROOF_CONSTANT (\S+)',log,re.M);transitive=re.findall(r'^TRANSITIVE_ASTIS_CONSTANT (\S+)',log,re.M);edges=re.findall(r'^TRANSITIVE_ASTIS_EDGE (\S+) -> (\S+)',log,re.M)
assert len(local)==int(re.search(r'LOCAL_PROOF_CONSTANT_COUNT (\d+)',log)[1]);assert len(transitive)==int(re.search(r'TRANSITIVE_ASTIS_CONSTANT_COUNT (\d+)',log)[1])
save('kernel-dependency-summary82.json',dict(status='PASS',module=info(M),axioms=axioms,actual_transitive_local_proof_constants=local,local_proof_constant_count=len(local),external_ASTIS_dependencies=deps,expected_four_parent_frontier_exact=True,transitive_imported_ASTIS_kernel_constants=transitive,transitive_imported_ASTIS_kernel_edges=edges,closure_algorithm='Read theorem values using ConstantInfo.value? true; traverse all target-prefixed generated proofs, then recursively traverse all ASTIS-valued dependencies of the four external producers. Std3axioms from complete theorem kernel closure.',fresh_complete_source=True,receipt=info(O/'fresh-whole-module.receipt.json')))
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan82.json',dict(status='PASS' if not hits else 'FAIL',algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M),aggregate_gate_not_run=True));assert not hits
for e in frozen:assert info(R/e['path'])==e
print('EXACT SOURCE / AXIOMS / LOCAL+TRANSITIVE ASTIS KERNEL CLOSURE / FAKECLOSURE PASS',flush=True)
