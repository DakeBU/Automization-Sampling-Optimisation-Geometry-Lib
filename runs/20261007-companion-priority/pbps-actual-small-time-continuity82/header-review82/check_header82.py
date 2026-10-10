from pathlib import Path
import hashlib,json,datetime,subprocess,os,re,difflib
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82';O=B/'header-review82';H=B/'header82.proposed.lean'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def txt(p):return p.read_text(encoding='utf8')
assert info(H)['RAW_sha256']=='0333cf3e488effe1fa6f516553bb1e63a3bb650bfe09aca234ed20375cf85e64'
P=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean';assert info(P)['RAW_sha256']=='bf8f66a8484fa82c46b26ac6b66a6c8484e6dd6465ac8587d7e27b2489e73a5c'
h=txt(H);p=txt(P)
def binders(t):
 start=t.index('    {E : Type*}');return t[start:t.index(' : Prop :=',start)]
def defs(t):
 start=t.index('    let ');end=t.index('    ∃ Z',start);parts=re.split(r'(?=^    let )',t[start:end],flags=re.M)
 return {re.match(r'    let (\S+) ',v)[1]:v.rstrip() for v in parts if v}
assert binders(h)==binders(p) and defs(h)==defs(p) and len(defs(h))==11
marker='        Z y xRef z₀ 0 sample = z₀)'
def oldconclusions(t):return t[t.index('    ∃ Z'):t.index(marker)+len(marker)]
assert oldconclusions(h)==oldconclusions(p)
assert h.count('private def ')==1 and '\ntheorem ' not in h and not re.search(r'\b(sorry|admit|axiom)\b',h)
save('definition-readback82.json',dict(status='PASS',header=info(H),actual80=info(P),six_original_binders_exact=True,eleven_actual_definitions_exact=True,actual_definitions=list(defs(h)),all_four_actual80_Z_properties_byte_text_preserved=True,expanded_binders=binders(h),literal_definitions=defs(h),new_public_provider_premises=[],new_conclusions='Measurable actual phase/harmonic defect with P.real bound1-exp(-Λ_t); measurable norm tail for δ>0 and convergence of its real probability as NNReal time tends to neighborhood0.',no_theorem_BODY=True))
parents=[P,R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
mathlibfiles=[R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Real.lean',R/'.lake/packages/mathlib/Mathlib/Probability/Distributions/Exponential.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Map.lean',R/'.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean']
paths=[H,B/'prospective-statement82.json',*parents,R/'lean-toolchain',R/'lake-manifest.json',*mathlibfiles]
frozen=[info(q) for q in paths]
assert subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze82.json',dict(reviewer='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=frozen,fixed_mathlib_commit='db584cd6d46c92f209a44c0f1c829460d327499d',HEAD_observed=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),scope='Prospective mathematical/type header review only; separate independent source-scope reviewer required. No Statement Seal/proof/state/admission created.'))
snap=O/'header82.exactraw.lean'
with snap.open('xb') as f:f.write(H.read_bytes())
tail='\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity'
assert h.count(tail)==1
probe_text=h.replace(tail,'\n#check actual_small_time_stochastic_continuity_statement\n'+tail)
assert probe_text.replace('\n#check actual_small_time_stochastic_continuity_statement\n','')==h
probe=O/'Header82FullPrivatePropLocalCheck.lean'
with probe.open('x',encoding='utf8',newline='\n') as f:f.write(probe_text)
with (O/'local-check-only.diff').open('x',encoding='utf8',newline='\n') as f:f.writelines(difflib.unified_diff(h.splitlines(True),probe_text.splitlines(True),fromfile='header82.proposed.lean',tofile=probe.name))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(probe)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'typecheck82.stdout.log').open('xb') as out,(O/'typecheck82.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('Complete private header foreground PID',child.pid,flush=True);code=child.wait()
save('typecheck82.receipt.json',dict(status='PASS' if code==0 else 'FAIL',command_argv=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),header=info(H),exact_snapshot=info(snap),complete_private_Prop_probe=info(probe),only_overlay='Local #check command before standalone section end; complete original named Prop unchanged; no syntax/mathematical repair.',overlay_diff=info(O/'local-check-only.diff'),stdout=info(O/'typecheck82.stdout.log'),stderr=info(O/'typecheck82.stderr.log'),proof_BODY=False))
for q,e in zip(paths,frozen):assert info(q)==e
print('COMPLETE PRIVATE HEADER EXIT',code,flush=True)
raise SystemExit(code)
