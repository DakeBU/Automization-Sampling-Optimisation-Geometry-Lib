from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
R=Path('E:/Samplinglib'); O=Path(__file__).parent; B=O.parent
def info(p):
 p=Path(p); b=p.read_bytes(); return dict(path=p.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f: json.dump(d,f,ensure_ascii=False,indent=2); f.write('\n')
def run(label,cmd):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(); env=os.environ.copy();env['PYTHONUTF8']='1'
 env.pop('ELAN_TOOLCHAIN',None)
 q=subprocess.run(cmd,cwd=R,env=env,capture_output=True)
 for s in ['stdout','stderr']:(O/(label+'.'+s+'.log')).write_bytes(getattr(q,s))
 receipt=dict(command=cmd,cwd=str(R),started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=q.returncode,terminal_closed=True,foreground=True,stdout=info(O/(label+'.stdout.log')),stderr=info(O/(label+'.stderr.log')))
 save(label+'.receipt.json',receipt);print(label,q.returncode,flush=True);return q.returncode
h=B/'header85.proposed.lean';raw=h.read_bytes();assert hashlib.sha256(raw).hexdigest()=='b2e1c43e0f7d3877096546181f06e10177486cf126bc98df16d201d5b040bb04'
parent=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean'
assert info(parent)['RAW_sha256']=='bf8f66a8484fa82c46b26ac6b66a6c8484e6dd6465ac8587d7e27b2489e73a5c'
text=raw.decode(); p=parent.read_text(encoding='utf8'); normalize=lambda x:re.sub(r'\s+','',x)
ps=p[p.index('private def '):p.index('\n\n\nset_option maxHeartbeats')].replace('actual_physical_time_measurable_phase_statement','actual_phase_transition_kernel_statement')
hs=text[text.index('private def '):text.index('\n      ∧ (∃ K')]
assert normalize(ps)==normalize(hs)
names=re.findall(r'^    let ([^ :]+)',hs,re.M);assert names==['P','ε','c','Φ','S','rate','Λ','τ','next','record','eventTime']
save('definition-readback85.json',dict(status='EXACT_FULL_ACTUAL80_PREFIX_EXCEPT_PRIVATE_NAME',header=info(h),actual80=info(parent),eleven_literal_definitions=names,analytic_binders=['hα','hαβ','hV','hH','hη','hβη'],comparison='Entire original private Prop through final AE initialization clause, whitespace-normalized; no definitions or clauses omitted.',assumptions_added=[]))
(O/'header85.exact.snapshot.lean').write_bytes(raw)
checks='\n#check actual_phase_transition_kernel_statement\n#check ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase\n#check AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws\n#check ProbabilityTheory.Kernel.id\n#check ProbabilityTheory.Kernel.const\n#check ProbabilityTheory.Kernel.prod\n#check ProbabilityTheory.Kernel.id_prod_apply\n#check ProbabilityTheory.Kernel.map_apply\n#check MeasureTheory.Measure.map_apply\n#check MeasureTheory.Measure.map_congr\n#check MeasureTheory.integral_map\n#check MeasureTheory.integrable_map_measure\n#check MeasureTheory.Integrable.mono\n'
pos=text.index('\nend\nend AutoSamplingTheory.')
(O/'header85.local-checks.lean').write_text(text[:pos]+checks+text[pos:],encoding='utf8',newline='\n')
save('local-check-overlay85.json',dict(original=info(h),exact_snapshot=info(O/'header85.exact.snapshot.lean'),local_checks=info(O/'header85.local-checks.lean'),only_change='Insert local #check commands after complete private definition, before section/namespace end. No repair, mathematical proposition change, theorem BODY, proof tactic, placeholder, or state write.',inserted_text=checks))
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
assert run('fixed-toolchain-version',[lean,'--version'])==0
codes={}
for label,name in [('complete-exact-header','header85.exact.snapshot.lean'),('complete-header-local-checks','header85.local-checks.lean')]:codes[label]=run(label,[lake,'env','lean',str(O/name)])
save('header-run85.json',dict(status='TERMINAL_COMPLETE',reviewer_id='/root/exact_verify77',checked_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),header=info(h),parent=info(parent),lake=info(lake),lean=info(lean),toolchain=info(R/'lean-toolchain'),manifest=info(R/'lake-manifest.json'),mathlib_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R/'.lake/packages/mathlib',text=True).strip(),exit_codes=codes,proof_search=False,no_production_or_shared_state_write=True))
print(json.dumps(codes))
