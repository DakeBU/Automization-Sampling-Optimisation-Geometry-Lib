from pathlib import Path
import hashlib,json,re,datetime,subprocess,os,sys
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84';O=B/'independent-math84'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def txt(p):return p.read_text(encoding='utf8')
def put(n,b):
 with (O/n).open('xb') as f:f.write(b)
def prop(t):
 a=t.index('private def ');end=t.index('\n\nset_option',a) if '\n\nset_option' in t[a:] else t.index('\n\nend',a);return t[a:end].rstrip()
def binders(t):
 a=t.index('    {E : Type*}');return t[a:t.index(' : Prop :=',a) if ' : Prop :=' in t[a:] else t.index(' :\n    actual_',a)]
def lets(t,indent,end):
 found=list(re.finditer(r'^'+(' '*indent)+r'let (\S+)\s*:',t,re.M));d={}
 for i,m in enumerate(found):
  stop=found[i+1].start() if i+1<len(found) else t.index(end,m.start());d[m.group(1)]='\n'.join(v[indent:] if v.startswith(' '*indent) else v for v in t[m.start():stop].rstrip().splitlines())
 return d
raw=M.read_bytes();s=txt(M);h=txt(B/'header84.reviewed.lean');seal=load(B/'root.statement-seal84.json')
assert info(M)['RAW_sha256']=='8fd35db26717f46313fc53dd90691828b11c9d78cdcc4a62f68c8d59273cc2bd'
assert prop(s)==prop(h) and prop(s)[len('private def '):]+'\n'==seal['expanded_literal_Prop']
public=s[s.index('\ntheorem ')+1:];assert binders(s)==binders(public)
hd=lets(prop(s),4,'    ∃ Z');assert len(hd)==11
names=['ActualBoundedTestContinuity','GibbsAugmentation'];parents=[R/('AutoSamplingTheory/ExampleCases/ProximalBPS/'+n+'.lean') for n in names]
parents += [R/'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
old=prop(txt(parents[0]));assert hd==lets(old,4,'    ∃ Z');assert binders(s)==binders(old)
marker='            (𝓝 0) (𝓝 (f z₀)))'
assert prop(s)[prop(s).index('    ∃ Z'):prop(s).index(marker)+len(marker)]==old[old.index('    ∃ Z'):]
body=public[public.index(':= by')+len(':= by'):public.index('  obtain ⟨Z')]
bd=lets(body+'  obtain ⟨Z',2,'  obtain ⟨Z');assert set(bd)=={'P','q','ν'} and bd['P']==hd['P']
assert re.sub(r'\s+','',bd['q'])==re.sub(r'\s+','', 'let q : E → Measure E := fun y => (volume : Measure E).tilted (fun x => -V x - ‖x - y‖ ^ 2 / (2 * η))')
assert re.sub(r'\s+','',bd['ν'])==re.sub(r'\s+','', 'let ν : E → Measure (E × E) := fun y => (q y).prod (stdGaussian E)')
save('statement-definition-audit84.json',dict(status='PASS',module=info(M),header=info(B/'header84.reviewed.lean'),seal=info(B/'root.statement-seal84.json'),complete_private_Prop_exact_sealed_header=True,public_six_binders_exact_private_and83=True,eleven_actual_lets_exact83=list(hd),entire83_phase_defect_tail_test_prefix_exact=True,body_P_q_nu_literal_exact=True,new_public_provider_premises=[],public_theorem_count=s.count('\ntheorem '),private_specification_count=s.count('private def ')))
put('module84.exactraw.lean',raw)
oldscript=txt(R/'runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83/independent-math83/check83-v2.py')
start=oldscript.index("extra='\\n#print axioms '");end=oldscript.index("probe=O/",start)
segment=oldscript[start:end].replace('ActualBoundedTestContinuity.actual_bounded_test_expectation_continuity','ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity')
exec(segment)
probe=O/'FreshWholeModuleAxiomsKernelClosure84.lean';put(probe.name,raw+extra.encode('utf8'))
mathlibs=[R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean']
paths=[M,*parents,*mathlibs,B/'header84.reviewed.lean',B/'root.statement-seal84.json',B/'mathematics-freeze84.json',R/'lean-toolchain',R/'lake-manifest.json',probe]
frozen=[info(p) for p in paths];mathlib=subprocess.check_output(['git','-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD']).decode().strip();assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
save('input-freeze84.json',dict(reviewer='/root/exact_verify77',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=frozen,fixed_mathlib=mathlib,head_observed_not_exact_admission=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),blind_or_source_verdict_read=False))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
def run(label,cmd):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(label+'.stdout.log')).open('xb') as out,(O/(label+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(label,'foreground PID',child.pid,flush=True);code=child.wait()
 save(label+'.receipt.json',dict(command_argv=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=info(M),probe=info(probe),stdout=info(O/(label+'.stdout.log')),stderr=info(O/(label+'.stderr.log')),native_reasoning_trajectory_claimed=False))
 print(label,'EXIT',code,flush=True)
 if code:raise SystemExit(code)
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
run('fresh-focused-build',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity'])
run('fresh-whole-module',[lake,'env',lean,str(probe)])
log=txt(O/'fresh-whole-module.stdout.log');ax=re.search(r'depends on axioms:\s*\[([^\]]+)\]',log,re.S);assert ax;axioms=[v.strip() for v in ax[1].split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'}
deps=re.findall(r'EXTERNAL_ASTIS_DEPENDENCY (\S+)',log)
expected={'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity.actual_bounded_test_expectation_continuity','AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation.normalized_augmentation_density','AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'}
assert set(deps)==expected,deps
local=re.findall(r'^LOCAL_PROOF_CONSTANT (\S+)',log,re.M);transitive=re.findall(r'^TRANSITIVE_ASTIS_CONSTANT (\S+)',log,re.M);edges=re.findall(r'^TRANSITIVE_ASTIS_EDGE (\S+) -> (\S+)',log,re.M)
assert len(local)==int(re.search(r'LOCAL_PROOF_CONSTANT_COUNT (\d+)',log)[1]);assert len(transitive)==int(re.search(r'TRANSITIVE_ASTIS_CONSTANT_COUNT (\d+)',log)[1])
save('kernel-dependency-summary84.json',dict(status='PASS',module=info(M),axioms=axioms,actual_transitive_local_proof_constants=local,local_proof_constant_count=len(local),external_ASTIS_dependencies=deps,expected_four_parent_frontier_exact=True,transitive_imported_ASTIS_kernel_constants=transitive,transitive_imported_ASTIS_kernel_edges=edges,closure_algorithm='ConstantInfo.value? true; recurse target-prefixed generated proofs, then all ASTIS-valued imported dependencies; #print axioms covers whole theorem.',fresh_complete_source=True,receipt=info(O/'fresh-whole-module.receipt.json')))
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan84.json',dict(status='PASS' if not hits else 'FAIL',algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M),aggregate_gate_not_run=True));assert not hits
for e in frozen:assert info(R/e['path'])==e
print('ALL FRESH SOURCE / AXIOMS / KERNEL CLOSURE / FAKECLOSURE PASS',flush=True)
