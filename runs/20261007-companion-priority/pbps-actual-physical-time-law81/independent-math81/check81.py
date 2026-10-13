from pathlib import Path
import hashlib,json,re,datetime,subprocess,os,sys
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81';O=B/'independent-math81'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel.ideal_half_turn_returned_position_kernel'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def txt(p):return p.read_text(encoding='utf-8')
raw=M.read_bytes();s=txt(M);h=txt(B/'header81.proposed.lean');seal=json.loads(txt(B/'root.statement-seal81.json'))
assert info(M)['RAW_sha256']=='5b3d639fbc49e06715ae8f768d5a5c714b7844dc20c5e5a8a16cb564e823df2f'
assert info(B/'header81.proposed.lean')['RAW_sha256']=='c3d1ad6107ad0aa812a99461d7dc48720ba83709104f699a908a77a89bec1e76'
def prop(t):return t[t.index('private def '):t.index('\n\n',t.index('          Z y w.1.1 (x, w.1.2) tπ w.2 = Φ'))].rstrip()
assert prop(s)==prop(h)
assert prop(s)[len('private def '):]+'\n'==seal['expanded_literal_Prop']
public=s[s.index('\ntheorem ')+1:]
def binders(t):
 start=t.index('    {E : Type*}');end=t.index(' : Prop :=',start) if ' : Prop :=' in t[start:] else t.index(' :\n    ideal_',start)
 return t[start:end]
assert binders(s)==binders(public)
assert s.count('private def ')==1 and s.count('\ntheorem ')==1
def lets(t,indent,end):
 found=list(re.finditer(r'^'+(' '*indent)+r'let (\S+)\s*:',t,re.M));d={}
 for i,m in enumerate(found):
  stop=found[i+1].start() if i+1<len(found) else t.index(end,m.start())
  d[m.group(1)]='\n'.join(v[indent:] if v.startswith(' '*indent) else v for v in t[m.start():stop].rstrip().splitlines())
 return d
hd=lets(prop(s),4,'    ∃ Z');body=public[public.index(':= by')+len(':= by'):public.index('  have h80')]
bd=lets(body+'  have h80',2,'  have h80');assert hd==bd and len(hd)==15
names=['P','ε','c','Φ','S','rate','Λ','τ','next','record','eventTime']
p80=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean'
p79=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean'
p76=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
p75=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean'
p73=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'
p77=R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
pG=R/'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean'
pA=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean'
d80=lets(txt(p80).split('\nset_option maxHeartbeats')[0],4,'    ∃ Z')
d79=lets(txt(p79).split('\nset_option maxHeartbeats')[0],4,'    ∀ y')
assert {n:hd[n] for n in names}==d80==d79
fd=lets(txt(p76).split('\nset_option maxHeartbeats')[0],4,'    (∀ y');common=names[2:]
assert all(hd[n]==fd[n] for n in common)
save('statement-definition-audit81.json',dict(status='PASS',module=info(M),seal=info(B/'root.statement-seal81.json'),private_Prop_exact_sealed_header=True,sealed_expanded_literal_Prop_exact=True,public_six_binders_exact_private=True,body_fifteen_lets_exact_private=True,all_eleven_actual_lets_exact80_and79=names,nine_common_actual_lets_exact76=common,new_public_provider_premises=[],public_theorem_count=1,private_specification_count=1))
snap=O/'module81.exactraw.lean'
with snap.open('xb') as f:f.write(raw)
extra='\n#print axioms '+D+'\n#check '+D+'\n'+'''open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let proofStem := "AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel.ideal_half_turn_returned_position_kernel"
  let mut todo := #[`AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel.ideal_half_turn_returned_position_kernel]
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
      logInfo m!"KERNEL_VALUE_CONSTANT_COUNT {name}: {value.getUsedConstants.size}"
      for dep in value.getUsedConstants do
        if dep.toString.startsWith proofStem then
          todo := todo.push dep
        else if dep.toString.startsWith "AutoSamplingTheory." && !externalDeps.contains dep then
          externalDeps := externalDeps.push dep
          logInfo m!"EXTERNAL_ASTIS_DEPENDENCY {dep}"
  logInfo m!"LOCAL_PROOF_CONSTANT_COUNT {seen.size}"
'''
probe=O/'FreshWholeModuleAxiomsKernelClosure81.lean'
with probe.open('xb') as f:f.write(raw+extra.encode('utf-8'))
parents=[p80,p79,p76,p75,p73,p77,pG,pA,R/'AutoSamplingTheory/TechnicalLemmas/Analysis/HessianStrongConvexity.lean',R/'AutoSamplingTheory/TechnicalLemmas/Analysis/StrongConvexGibbsIntegrability.lean']
paths=[M,*parents,B/'root.statement-seal81.json',B/'header81.proposed.lean',B/'mathematics-freeze81.json',B/'focused81-attempt5/receipt.json',R/'lean-toolchain',R/'lake-manifest.json',probe]
frozen=[info(p) for p in paths]
mathlib=subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip()
assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze81.json',dict(reviewer='/root/exact_verify77',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=frozen,fixed_mathlib=mathlib,head_observed_not_exact_commit_admission=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(probe)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'fresh-whole-module.stdout.log').open('xb') as so,(O/'fresh-whole-module.stderr.log').open('xb') as se:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=so,stderr=se)
 print('Fresh complete-source foreground PID',child.pid,flush=True);code=child.wait()
save('fresh-whole-module.receipt.json',dict(command_argv=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),full_source_prefix_exact=True,source=info(M),probe=info(probe),stdout=info(O/'fresh-whole-module.stdout.log'),stderr=info(O/'fresh-whole-module.stderr.log'),canonical_olean_written=False,native_reasoning_trajectory_claimed=False))
print('FRESH SOURCE EXIT',code,flush=True)
if code:raise SystemExit(code)
log=txt(O/'fresh-whole-module.stdout.log');ax=re.search(r'depends on axioms:\s*\[([^\]]+)\]',log,re.S);assert ax
axioms=[v.strip() for v in ax.group(1).split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'}
deps=re.findall(r'EXTERNAL_ASTIS_DEPENDENCY (\S+)',log);local=re.findall(r'^LOCAL_PROOF_CONSTANT (\S+)',log,re.M)
count=int(re.search(r'LOCAL_PROOF_CONSTANT_COUNT (\d+)',log)[1]);assert count==len(local)
save('kernel-dependency-summary81.json',dict(status='PASS',module=info(M),axioms=axioms,actual_transitive_local_proof_constants=local,local_proof_constant_count=count,external_ASTIS_dependencies=deps,closure_algorithm='Traverse theorem kernel values via ConstantInfo.value? true and Expr.getUsedConstants, recursively following every target-prefixed generated proof constant.',fresh_complete_source=True,receipt=info(O/'fresh-whole-module.receipt.json')))
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis
hits=astis.forbidden_pattern_hits()
save('fake-closure-scan81.json',dict(status='PASS' if not hits else 'FAIL',algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M),aggregate_Lake_gate_not_run=True))
assert not hits
for e in frozen:assert info(R/e['path'])==e
print('EXACT SOURCE / STANDARD THREE / KERNEL CLOSURE / FAKECLOSURE PASS',flush=True)
