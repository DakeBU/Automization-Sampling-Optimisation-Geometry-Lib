from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw.actual_finite_first_event_law'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def put(n,b):
 with (O/n).open('xb') as f:f.write(b)
raw=M.read_bytes();assert hashlib.sha256(raw).hexdigest()=='cb8bd3e3ed053d114c6871ceaff24ab7782b46be405d69afe7174e0f4b7721d5'
s=raw.decode().replace('\r\n','\n');h=(B/'header86.proposed.lean').read_text('utf8');seal=json.loads((B/'root.statement-seal86.json').read_text('utf8'))
def prop(t):
 a=t.index('private def ');z=t.index('\n\n-- Internal FTC',a) if '\n\n-- Internal FTC' in t[a:] else t.index('\n\nend',a)
 return t[a:z].rstrip()
assert prop(s)==prop(h)
assert prop(s)[len('private def '):]+'\n'==seal['expanded_literal_Prop']
pb=prop(s)[prop(s).index('    {E : Type*}'):prop(s).index(' : Prop :=')]
public=s[s.index('\ntheorem actual_finite_first_event_law'):];qb=public[public.index('    {E : Type*}'):public.index(' :\n    actual_')]
assert pb==qb
lets=re.findall(r'(?m)^    let (\S+)\s*:',prop(s));assert lets==['P','ε','c','Φ','S','rate','Λ','τ','U','F','A','d','ρ','J']
save('statement-definition-audit86.json',dict(status='PASS',created_utc=now(),module=pin(M),header=pin(B/'header86.proposed.lean'),seal=pin(B/'root.statement-seal86.json'),full_private_Prop_exact=True,public_six_original_binders_exact=True,all14_literal_definitions=lets,new_public_provider_premises=[],public_theorems=1,private_ingredients=re.findall(r'(?m)^private theorem (\S+)',s)))
put('module86.exactraw.lean',raw)
# Reuse only a previously tested inspection algorithm, not prior mathematics/results.
previous=R/'runs/20261007-companion-priority/pbps-actual-phase-transition-kernel85/independent-math85/FreshWholeModuleAxiomsKernelClosure85.lean'
algorithm=previous.read_text('utf8').split('open Lean Elab Command in\nrun_cmd do\n',1)[1]
algorithm=algorithm.replace('ActualPhaseTransitionKernel','ActualFiniteFirstEventLaw').replace('actual_phase_transition_kernel','actual_finite_first_event_law')
algorithm=algorithm.replace('let mut externalDeps : Array Name := #[]','let mut externalDeps : Array Name := #[]\n  let mut genericDeps : Array Name := #[]')
algorithm=algorithm.replace('  logInfo m!"LOCAL_PROOF_CONSTANT_COUNT {seen.size}"','        else if !isProject dep && !genericDeps.contains dep then\n          genericDeps := genericDeps.push dep\n          logInfo m!"GENERIC_DEPENDENCY {dep}"\n  logInfo m!"LOCAL_PROOF_CONSTANT_COUNT {seen.size}"')
extra='\nnamespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw\n'
for name in ['first_density_setIntegral','first_density_measure_mass','first_density_measure_Iic','finite_wait_mass','finite_wait_real_cdf']:
 extra+='#print axioms '+name+'\n'
extra+='end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw\n#print axioms '+D+'\n#check '+D+'\nopen Lean Elab Command in\nrun_cmd do\n'+algorithm
probe=O/'FreshWholeModuleAxiomsKernelClosure86.lean';put(probe.name,raw+extra.encode())
paths=[M,B/'header86.proposed.lean',B/'root.statement-seal86.json',B/'mathematics-freeze86.json',B/'focused-complete86.attempt1/receipt.json',R/'lean-toolchain',R/'lake-manifest.json',probe,previous,R/'runs/20261007-companion-priority/pbps-path-law-preread86/source-proof-graph86.reviewed-effective.json',R/'runs/20261007-companion-priority/pbps-path-law-preread86/source-inventory86.reviewed-effective.json']
for name in ['ActualHazardClock','ActualHarmonicFlow','ActualBounceRate']:paths.append(R/f'AutoSamplingTheory/ExampleCases/ProximalBPS/{name}.lean')
paths.append(R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean')
frozen=[pin(p) for p in paths];head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert head=='8280ef700ea01a1e94c9e7a3cba05a26b4156b56'
mathlib=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R/'.lake/packages/mathlib',text=True).strip();assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze86.json',dict(created_utc=now(),reviewer_id='/root/exact_verify77',checked_commit=head,scope='HEAD plus pinned working module, not exact science admission',raw_inputs=frozen,fixed_mathlib=mathlib,prior_probe_usage='Inspection algorithm only; all86 source elaborated freshly.',blind_or_final_source_verdict_read=False))
env=os.environ.copy();env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf8';env.pop('ELAN_TOOLCHAIN',None)
def run(label,cmd):
 start=now()
 with (O/(label+'.stdout.log')).open('xb') as out,(O/(label+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(label,'foreground PID',child.pid,flush=True);code=child.wait()
 save(label+'.receipt.json',dict(command=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),source=pin(M),probe=pin(probe),stdout=pin(O/(label+'.stdout.log')),stderr=pin(O/(label+'.stderr.log')),native_reasoning_trajectory_claimed=False));print(label,'EXIT',code,flush=True)
 if code:raise SystemExit(code)
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
run('fresh-focused-build',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw'])
run('fresh-whole-module',[lake,'env',lean,str(probe)])
log=(O/'fresh-whole-module.stdout.log').read_text('utf8')
axiom_blocks=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]+)\]",log,re.S)
assert len(axiom_blocks)==6
axioms=[dict(declaration=n,axioms=[x.strip() for x in a.split(',')]) for n,a in axiom_blocks]
assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in axioms)
deps=re.findall(r'EXTERNAL_ASTIS_DEPENDENCY (\S+)',log);local=re.findall(r'^LOCAL_PROOF_CONSTANT (\S+)',log,re.M);transitive=re.findall(r'^TRANSITIVE_ASTIS_CONSTANT (\S+)',log,re.M);edges=re.findall(r'^TRANSITIVE_ASTIS_EDGE (\S+) -> (\S+)',log,re.M);generic=re.findall(r'^GENERIC_DEPENDENCY (\S+)',log,re.M)
assert len(local)==int(re.search(r'LOCAL_PROOF_CONSTANT_COUNT (\d+)',log)[1]);assert len(transitive)==int(re.search(r'TRANSITIVE_ASTIS_CONSTANT_COUNT (\d+)',log)[1])
pub=[n for n in deps if n.startswith('AutoSamplingTheory.')];private=[n for n in deps if n.startswith('_private.')]
expected={f'AutoSamplingTheory.ExampleCases.ProximalBPS.{m}.{d}' for m,d in [('ActualHazardClock','actual_integrated_hazard_clock_laws'),('ActualHarmonicFlow','actual_harmonic_flow_laws'),('ActualBounceRate','actual_bounce_rate_energy_laws')]}
expected.add('AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws')
assert set(pub)==expected
save('kernel-dependency-summary86.json',dict(status='PASS',module=pin(M),axiom_blocks=axioms,standard_axioms_only=True,actual_owned_proof_constants=local,owned_count=len(local),external_project_constants=deps,actual_public_producer_parents=pub,private_spec_dependencies=private,exact_four_public_parents=True,generic_Mathlib_Lean_dependencies=generic,generic_count=len(generic),transitive_ASTIS_constants=transitive,transitive_ASTIS_edges=edges,transitive_count=len(transitive),edge_count=len(edges),algorithm='Recursive elaborated ConstantInfo.value? true/getUsedConstants from anchor, including generated/owned private constants; project closure separated from generic constants. Six fresh#print axioms blocks.',fresh_complete_source=True,receipt=pin(O/'fresh-whole-module.receipt.json')))
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan86.json',dict(status='PASS' if not hits else 'FAIL',algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=pin(M),aggregate_gate_not_run=True));assert not hits
for p in frozen:assert pin(R/p['path'])==p
print('WHOLE SOURCE / SIX AXIOM BLOCKS / FOUR REAL PARENTS / GENERATED CLOSURE / FAKECLOSURE PASS',flush=True)
