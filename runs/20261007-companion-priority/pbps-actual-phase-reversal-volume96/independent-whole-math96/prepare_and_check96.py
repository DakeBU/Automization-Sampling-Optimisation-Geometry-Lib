from pathlib import Path
import hashlib, json, os, re, subprocess, time
root=Path('E:/Samplinglib')
out=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def put(name,obj):
 p=out/name; assert not p.exists(),p
 p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
pre='runs/20261007-companion-priority/pbps-phase-reversal-volume-preread96/'
run='runs/20261007-companion-priority/pbps-actual-phase-reversal-volume96/'
prod='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseReversalVolume.lean'
paths=[prod,pre+'Header96.lean',pre+'root.statement-seal96.json',pre+'independent-header-math96/header-math-decision96.native.json',pre+'independent-header-math96/closed-RAW-manifest96.native.json',run+'checks96/production-build/receipt.json',
'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',
'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',
'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Projection/Reflection.lean',
'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Haar/InnerProductSpace.lean',
'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',
'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',
'lean-toolchain','lake-manifest.json']
(out/'inputs').mkdir(exist_ok=False)
inputs=[]
for i,path in enumerate(paths):
 b=(root/path).read_bytes();p=out/'inputs'/f'{i:02d}.{Path(path).name}.exactraw';p.write_bytes(b)
 inputs.append({'path':path,'raw_sha256':sha(b),'bytes':len(b),'snapshot':p.relative_to(root).as_posix()})
assert inputs[0]['raw_sha256']=='4b144dfa25d9521803e37518b8a6386fff08396c5804e410e9be593d46833a7b'
assert inputs[1]['raw_sha256']=='7a3d1929ccc6f1ae01ac3187040ad032515df7af0d627636d646d7f4df382a91'
seal=json.loads((root/paths[2]).read_bytes())
p=(root/prod).read_text(encoding='utf-8')
h=(root/paths[1]).read_text(encoding='utf-8')
literal=p.split('private def actual_phase_reversal_volume_statement',1)[1].split('\nvariable {E',1)[0].strip()
hliteral=h.split('def candidate',1)[1].split('\n#check candidate',1)[0].strip()
assert literal==hliteral==seal['expanded_literal_Prop']
assert json.loads((root/paths[5]).read_bytes())['exit_code']==0
binders=hliteral.split(' : Prop :=',1)[0]
fq='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws'
header_body='\n'.join(x for x in h.splitlines() if not x.startswith('import '))
witness='\nnamespace IndependentWholeMath96\nopen MeasureTheory InnerProductSpace\nopen scoped ContDiff NNReal ENNReal\nnoncomputable section\nset_option autoImplicit false\ntheorem sealed_header_witness\n    '+binders+' :\n    PBPSPhaseReversalVolumeCandidate96.candidate hα hαβ hV hH hη hβη := by\n  exact '+fq+' hα hαβ hV hH hη hβη\nend\nend IndependentWholeMath96\n#print axioms '+fq+'\n#print axioms IndependentWholeMath96.sealed_header_witness\n#check @'+fq+'\n'
combined=(root/prod).read_bytes()+('\n'+header_body+'\n'+witness).encode()
cp=out/'FreshExactSourceAndHeader96.lean';cp.write_bytes(combined)
scan={x:bool(re.search(x,p)) for x in [r'\bsorry\b',r'\badmit\b',r'\baxiom\b',r'\bunsafe\b',r'\bnative_decide\b',r'Prop\s*:=\s*True',r':=\s*trivial']}
assert not any(scan.values()),scan
put('prepared-inputs96.native.json',{'inputs':inputs,'literal_header_equals_private_statement_equals_seal':True,'full_production_bytes_are_kernel_input_prefix':combined.startswith((root/prod).read_bytes()),'fake_closure_scan':scan,'mathlib_commit':subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=root,text=True).strip(),'observed_repository_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'kernel_input_raw_sha256':sha(combined),'kernel_input_bytes':len(combined)})
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
argv=[str(root/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(cp.relative_to(root))]
t=time.monotonic()
with (out/'fresh-kernel.stdout.log').open('wb') as so,(out/'fresh-kernel.stderr.log').open('wb') as se:
 result=subprocess.run(argv,cwd=root,env=env,stdout=so,stderr=se)
receipt={'argv':argv,'exit_code':result.returncode,'seconds':time.monotonic()-t,'ELAN_TOOLCHAIN_removed':True,'target_raw_sha256':inputs[0]['raw_sha256'],'kernel_input_raw_sha256':sha(combined),'source_rehashed_unchanged':sha((root/prod).read_bytes())==inputs[0]['raw_sha256'],'manifest_rehashed_unchanged':sha((root/'lake-manifest.json').read_bytes())==inputs[-1]['raw_sha256']}
put('fresh-kernel-receipt96.native.json',receipt)
print(json.dumps(receipt))
print((out/'fresh-kernel.stdout.log').read_text(encoding='utf-8'))
print((out/'fresh-kernel.stderr.log').read_text(encoding='utf-8'))
