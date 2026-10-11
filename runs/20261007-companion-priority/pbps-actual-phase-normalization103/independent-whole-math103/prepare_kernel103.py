from pathlib import Path
import json,hashlib,re,subprocess,os,time
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-phase-normalization-preread103'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization'
sha=lambda b:hashlib.sha256(b).hexdigest()
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def load(p):return json.loads(Path(p).read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
raw=M.read_bytes();header=(PRE/'Header103.lean').read_bytes();seal=load(PRE/'root.statement-seal103.json')
assert sha(raw)=='c7806ada54ca78514a75ea1d13ed4bf08e5af4e92546d9ba0165683d77b36af4'
assert sha(header)=='af63f42611e180b198e069c2e636ddf48ee529524ecf3a292c51bf28111fb60d'
assert info(PRE/'root.statement-seal103.json')['raw_sha256']=='ba1ff7c905e61907c4ed33ee79e11f8fd94ea1e24ea9aa3043af46b3e3caaa22'
text=raw.decode().replace('\r\n','\n');ht=header.decode().replace('\r\n','\n')
literal=ht.split('def candidate',1)[1].split('\n#check candidate')[0].strip()
prod_literal=text.split('private def actual_phase_normalization_statement',1)[1].split('\n\n/--',1)[0].strip()
assert literal==prod_literal==seal['expanded_literal_Prop']
binders=ht.split('def candidate',1)[1].split(' : Prop := by',1)[0]
header_without_imports=b''.join(x for x in header.splitlines(keepends=True) if not x.startswith(b'import '))
witness=('\nnamespace IndependentExactHeader103\nopen MeasureTheory InnerProductSpace ProbabilityTheory\nopen scoped ContDiff NNReal ENNReal Classical\nnoncomputable section\nset_option autoImplicit false\ntheorem sealed_header_witness'+binders+' : PBPSPhaseNormalizationCandidate103.candidate hα hαβ hV hH hη hβη := by\n  exact '+D+' hα hαβ hV hH hη hβη\n#print axioms sealed_header_witness\nend\nend IndependentExactHeader103\n').encode()
k=O/'FreshExactProductionAndHeader103.lean';k.write_bytes(raw+b'\n'+header_without_imports+witness);assert k.read_bytes()[:len(raw)]==raw
assert not re.search(rb'^import .*ActualPhaseNormalization',k.read_bytes(),re.M)
parents=['AutoSamplingTheory/TechnicalLemmas/Analysis/HessianStrongConvexity.lean','AutoSamplingTheory/TechnicalLemmas/Analysis/StrongConvexGibbsIntegrability.lean','AutoSamplingTheory/TechnicalLemmas/Analysis/Integrability.lean','AutoSamplingTheory/TechnicalLemmas/Measure/IsotropicGaussianDensity.lean','AutoSamplingTheory/TechnicalLemmas/Measure/Gibbs.lean']
fixed=['.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/WithDensity.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean','.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Pow/Real.lean','lean-toolchain','lake-manifest.json','tools/astis.py']
prior=[PRE/'Header103.lean',PRE/'root.statement-seal103.json',PRE/'independent-header-math103/header-math-decision103.native.json',PRE/'independent-header-math103/source-topology-admission103.native.json',PRE/'independent-header-math103/closed-RAW-review103.native.json']
trials=[]
for name in ['assembly1','assembly2','assembly3','production1']:
 for name2 in ['receipt.json','stdout.log','stderr.log']:
  p=B/'focused103'/name/name2
  if p.exists():trials.append(p)
inputs=[M]+prior+[R/x for x in parents+fixed]+trials
save('prepared-inputs103.native.json',dict(status='EXACT_INPUTS_FROZEN_BEFORE_INDEPENDENT_KERNEL',production=info(M),header=info(PRE/'Header103.lean'),seal=info(PRE/'root.statement-seal103.json'),inputs=[info(p) for p in inputs],kernel=info(k),exact_production_byte_prefix=True,original_header_candidate_bytes_without_imports=True,target_module_not_imported=True,expanded_literal_Prop_exact=True,baseline_git=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),mathlib_commit=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R).decode().strip()))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(k)];start=time.time()
with (O/'fresh-kernel.stdout.log').open('xb') as out,(O/'fresh-kernel.stderr.log').open('xb') as err:p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
save('fresh-kernel-receipt103.native.json',dict(exit_code=p.returncode,command=argv,seconds=time.time()-start,production_raw_sha256=sha(raw),header_raw_sha256=sha(header),kernel=info(k),terminal_closed=True,target_module_not_imported=True,production_exact_byte_prefix=True,original_sealed_header_witness=True,no_new_proof_implementation=True))
assert p.returncode==0
print('PASS independent exact-byte production and original Header103 kernel witness',flush=True)
