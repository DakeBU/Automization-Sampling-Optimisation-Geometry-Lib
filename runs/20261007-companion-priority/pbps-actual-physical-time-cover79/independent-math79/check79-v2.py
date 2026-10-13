"""Independent full-source elaboration, exact seal/definition and dependency audit."""
from pathlib import Path
import hashlib,json,re,datetime,subprocess,os,sys
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79';O=B/'independent-math79';O.mkdir(parents=True,exist_ok=True)
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover'
P=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean';F=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(n,x):
 p=O/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raw=M.read_bytes();s=raw.decode();header=(B/'header79.proposed.lean').read_text(encoding='utf-8');seal=load(B/'root.statement-seal79.json')
assert info(B/'header79.proposed.lean')['RAW_sha256']=='4b3b12a9e83195cfca5c02466b51f838b0e175fad23a9665ab32df7553968a1a'
def prop(t):return t[t.index('private def '):t.index('\n\n',t.index('        ∃! a :'))]
assert prop(s)==prop(header)
public=s[s.index('theorem actual_fixed_reference_physical_time_cover'):]
def binders(t):return t[t.index('    {E : Type*}'):min(t.index(x) for x in [' :\n    actual_', ' : Prop :='] if x in t)]
assert binders(s)==binders(public)
assert s.count('private def ')==1 and s.count('\ntheorem ')==1
def lets(t,indent,end):
 found=list(re.finditer(r'^'+(' '*indent)+r'let (\S+)\s*:',t,re.M));d={}
 for i,m in enumerate(found):
  stop=found[i+1].start() if i+1<len(found) else t.index(end,m.start())
  text=t[m.start():stop];d[m.group(1)]='\n'.join(line[indent:] if line.startswith(' '*indent) else line for line in text.rstrip().splitlines())
 return d
hd=lets(prop(s),4,'    ∀ y');pd=lets(prop(P.read_text(encoding='utf-8')),4,'    ∀ y')
assert hd==pd and len(hd)==11
body=public[public.index(':= by')+len(':= by'):];bd=lets(body,2,'  change ∀ y')
assert hd==bd
f=F.read_text(encoding='utf-8');fp=f[:f.index('\nset_option maxHeartbeats')]
fd=lets(fp,4,'    (∀ y')
common=['c','Φ','S','rate','Λ','τ','next','record','eventTime']
for k in common:assert hd[k]==fd[k]
for key in ['header','source_first_freeze','source_graph_overlay','header_math','source_topology_review','definition_audit','typecheck']:
 e=seal[key];assert info(R/e['path'])['RAW_sha256']==e['RAW_sha256'],key
save('statement-definition-audit79.json',dict(status='PASS_EXACT_SEAL_SIX_BINDERS_ELEVEN_ACTUAL_DEFINITIONS',module=info(M),sealed_header=info(B/'header79.proposed.lean'),
 private_prop_byte_equal_sealed_header=True,public_six_binder_block_exact_private=True,body_eleven_definitions_exact_private=True,all_eleven_exact_parent78=True,
 nine_recurrence_definitions_exact_parent76=common,no_new_public_provider_premises=True,public_theorem_count=1,private_specification_count=1))
snapshot=O/'module79.exactraw.lean';assert not snapshot.exists();snapshot.write_bytes(raw)
probe=O/'FreshWholeModuleAxiomsDependencies79.lean'
extra='\n#print axioms '+D+'\n#check '+D+'\n'+'''open Lean Elab Command in
run_cmd do
  let some ci := (← getEnv).find? `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover | throwError "Missing target"
  let some value := ci.value? | throwError "Missing theorem BODY"
  for name in value.getUsedConstants do
    if name.toString.startsWith "AutoSamplingTheory." then
      logInfo m!"ASTIS_DIRECT_DEPENDENCY {name}"
  logInfo m!"DIRECT_CONSTANT_COUNT {value.getUsedConstants.size}"
'''
assert not probe.exists();probe.write_bytes(raw+extra.encode())
paths=[M,P,F,B/'root.statement-seal79.json',B/'header79.proposed.lean',R/'lean-toolchain',R/'lake-manifest.json',probe]
frozen=[info(p) for p in paths]
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze79.json',dict(reviewer='/root/exact_verify77',inputs=frozen,head_at_freeze=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
 fixed_mathlib='db584cd6d46c92f209a44c0f1c829460d327499d',scope='Independent mathematics only; no exact-commit VERIFIED admission'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
cmd=[lake,'env',lean,str(probe)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'fresh-whole-module.stdout.log').open('xb') as out,(O/'fresh-whole-module.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('Fresh full-source foreground PID',child.pid,flush=True);code=child.wait()
save('fresh-whole-module.receipt.json',dict(command=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,
 started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=frozen,stdout=info(O/'fresh-whole-module.stdout.log'),stderr=info(O/'fresh-whole-module.stderr.log'),
 full_source_prefix_exact=True,canonical_olean_written=False,native_reasoning_trajectory_claimed=False))
print('FRESH FULL SOURCE EXIT',code,flush=True)
if code:raise SystemExit(code)
log=(O/'fresh-whole-module.stdout.log').read_text(encoding='utf-8')
axioms=re.search(r"depends on axioms:\s*\[([^\]]+)\]",log,re.S);assert axioms,log[-3000:]
names=[x.strip() for x in axioms.group(1).split(',')];assert set(names)=={'propext','Classical.choice','Quot.sound'}
dependencies=re.findall(r'ASTIS_DIRECT_DEPENDENCY (\S+)',log)
expected=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation.actual_fixed_reference_event_time_nonaccumulation']
assert set(dependencies)==set(expected),dependencies
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis
hits=astis.forbidden_pattern_hits()
save('fake-closure-scan79.json',dict(reviewer='/root/exact_verify77',algorithm='tools.astis.forbidden_pattern_hits same production scan as astis.py check',
 scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M),aggregate_Lake_gate_not_run=True))
assert not hits
assert M.read_bytes()==raw
for e in frozen:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
save('fresh-compiler-dependency-summary79.json',dict(status='PASS_FULL_SOURCE_STANDARD_THREE_EXACT_ACTUAL_PARENTS',module=info(M),axioms=names,
 direct_ASTIS_dependencies=dependencies,public_stochastic_provider_premises=[],receipt=info(O/'fresh-whole-module.receipt.json'),
 direct_unused_import='UnitExponentialProduct imported explicitly but no direct BODY dependency; actual78 already supplies input-event escape. Optional later import cleanup only.',
 fake_closure_scan=info(O/'fake-closure-scan79.json'),proof_reviewer='/root/exact_verify77',source_review=False,VERIFIED=False,Goal_complete=False))
print('FRESH ELABORATION / AXIOMS / ACTUAL DEPENDENCIES / FAKECLOSURE PASS',flush=True)
