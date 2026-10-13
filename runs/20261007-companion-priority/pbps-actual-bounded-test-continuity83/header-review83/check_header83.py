from pathlib import Path
import copy,datetime,difflib,hashlib,json,os,re,subprocess
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83';O=B/'header-review83';H=B/'header83.proposed.lean'
P=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean';S=R/'runs/20261007-companion-priority/pbps-bounded-test-preread83'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def txt(p):return p.read_text(encoding='utf8')
def load(p):return json.loads(txt(p))
assert info(H)['RAW_sha256']=='1bf2b24f0ba521449aba10ac3559a27c4db7f2eab0df89c98587f623695b07ff'
assert info(P)['RAW_sha256']=='f2bbb2a495ff6af2f2d1d73f77c498ccf16406bb0b07d20b8437631afb1a7bde'
h=txt(H);p=txt(P)
def binders(t):
 a=t.index('    {E : Type*}');return t[a:t.index(' : Prop :=',a)]
def defs(t):
 a=t.index('    let ');z=t.index('    ∃ Z',a);parts=re.split(r'(?=^    let )',t[a:z],flags=re.M)
 return {re.match(r'    let (\S+) ',v)[1]:v.rstrip() for v in parts if v}
assert binders(h)==binders(p) and defs(h)==defs(p) and len(defs(h))==11
marker='            δ ≤ ‖Z y xRef z₀ t sample - z₀‖}) (𝓝 0) (𝓝 0)))'
def old(t):return t[t.index('    ∃ Z'):t.index(marker)+len(marker)]
assert old(h)==old(p)
assert h.count('private def ')==1 and '\ntheorem ' not in h and not re.search(r'\b(sorry|admit|axiom)\b',h)
overlay=load(S/'independent-topology83/proposed-minimal-topology-overlay83.json');original=load(S/'source_proof_graph83.json');supp=load(S/'optional-route-topology-supplement83.json');effective=load(S/'source_proof_graph83.reviewed-effective.json')
expected=copy.deepcopy(original['edges']+supp['added_edges'])
for e in expected:
 if e['id'] in {'E83-29','E83-30'}:e['status']='OPTIONAL_ROUTE_AND_INGREDIENT'
 if e['id']=='E83-28':e.update(overlay['patches'][2]['after'])
assert effective['edges']==expected and effective['nodes']==original['nodes'] and effective['reviewed_junctions']==overlay['junctions']
save('definition-readback83.json',dict(status='PASS',header=info(H),actual82=info(P),original_six_binders_exact=True,eleven_actual_definitions_exact=True,
 literal_definitions=defs(h),expanded_analytic_binders=binders(h),all_actual82_phase_defect_tail_clauses_preserved=True,
 tuple_association='((E x E) x (E x E)) x NNReal x sample, right-associated product after first factor; projections a.1.1.1,a.1.1.2,a.1.2,a.2.1,a.2.2 unchanged.',
 test_quantifiers='For each deterministic y,xRef,z0, every continuous real f, every real M>=0 globally bounding |f|; every finite t measurable/integrable composition and estimate; ordinary NNReal neighborhood0 expectation limit.',
 new_public_provider_premises=[],test_class='Explicit ASTIS C_b extension of source C_c, continuity and bound are test-class binders only.',
 source_overlay_mechanically_exact=True,effective_graph=info(S/'source_proof_graph83.reviewed-effective.json'),no_theorem_BODY=True))
parents=[P,R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
mathlibpaths=[R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Set.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntegrableOn.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean']
paths=[H,B/'prospective-statement83.json',*parents,R/'lean-toolchain',R/'lake-manifest.json',*mathlibpaths,S/'source_freeze83.closed-raw-manifest.json',S/'source_inventory83.json',S/'source_proof_graph83.json',S/'optional-route-topology-supplement83.json',S/'source_proof_graph83.reviewed-effective.json',S/'independent-topology83/proposed-minimal-topology-overlay83.json']
frozen=[info(q) for q in paths];mathlib=subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip();assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze83.json',dict(reviewer_id='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=frozen,fixed_mathlib_commit=mathlib,HEAD_observed_not_exact_commit_admission=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),scope='Complete prospective header mathematics/type review only; no83 proof search, production/shared/state/Seal/VERIFIED.'))
snap=O/'header83.exactraw.lean'
with snap.open('xb') as f:f.write(H.read_bytes())
tail='\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity';assert h.count(tail)==1
checks='\n#check actual_bounded_test_expectation_continuity_statement\n#check Integrable.of_bound\n#check integral_mono_ae\n#check norm_integral_le_integral_norm\n#check integral_indicator_const\n'
probe_text=h.replace(tail,checks+tail);assert probe_text.replace(checks,'')==h
probe=O/'Header83CompletePrivatePropLocalCheck.lean'
with probe.open('x',encoding='utf8',newline='\n') as f:f.write(probe_text)
with (O/'local-check-only.diff').open('x',encoding='utf8',newline='\n') as f:f.writelines(difflib.unified_diff(h.splitlines(True),probe_text.splitlines(True),fromfile='header83.proposed.lean',tofile=probe.name))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(probe)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'typecheck83.stdout.log').open('xb') as out,(O/'typecheck83.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('Complete private header foreground PID',child.pid,flush=True);code=child.wait()
save('typecheck83.receipt.json',dict(status='PASS' if code==0 else 'FAIL',command_argv=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),header=info(H),exact_snapshot=info(snap),complete_named_private_Prop_probe=info(probe),only_overlay='Local #check for complete named private Prop and four real existing API signatures before existing section end. Entire original private Prop unchanged, no syntax/mathematical repair or theorem placeholder.',overlay_diff=info(O/'local-check-only.diff'),stdout=info(O/'typecheck83.stdout.log'),stderr=info(O/'typecheck83.stderr.log'),proof_BODY=False))
for q,e in zip(paths,frozen):assert info(q)==e
print('COMPLETE PRIVATE HEADER EXIT',code,flush=True)
raise SystemExit(code)
