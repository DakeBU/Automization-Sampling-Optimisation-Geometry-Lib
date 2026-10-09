from pathlib import Path
import hashlib,json,datetime,subprocess
out=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-root-preproof64/independent-primary64');repo=Path('E:/Samplinglib')
files=[
('production','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean'),
('production','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRoot.lean'),
('production','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRootUnique.lean'),
('production','AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean'),
('production','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean'),
('production','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean'),
('production','AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean'),
('production','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean'),
('Test-reference-only','Tests/GaussianMarginalPoincare.lean'),
('Test-reference-only','Tests/ProximalBPSMacroscopicRange.lean'),
('Test-reference-only','Tests/ProximalBPSCenteredDefect.lean'),
('Test-reference-only','Tests/ProximalBPSMacroscopicDefectRoot.lean'),
('fixed-Mathlib','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/StarOrder.lean'),
('fixed-Mathlib','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean'),
('fixed-Mathlib','.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean'),
('fixed-Mathlib','.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Order.lean'),
('fixed-Mathlib','.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Banach.lean'),
('fixed-Mathlib','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean'),
('fixed-Mathlib','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean'),
('pin','lean-toolchain'),('pin','lake-manifest.json')]
receipt=[]
for i,(kind,rel) in enumerate(files):
 raw=(repo/rel).read_bytes();lf=raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n');name=f'api-pin-{i:02d}-{Path(rel).stem}'
 (out/(name+'.raw.txt')).write_bytes(raw);(out/(name+'.lf.txt')).write_bytes(lf)
 receipt.append({'kind':kind,'path':str(repo/rel),'relative_path':rel,'bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),'lf_sha256':hashlib.sha256(lf).hexdigest(),'raw_snapshot':str(out/(name+'.raw.txt')),'lf_snapshot':str(out/(name+'.lf.txt')),'scope':'read-only current dependency/API evidence; no independent compile or source-verdict admission'})
oleans=[]
for name in ['GaussianMarginalPoincare','ProximalBPSMacroscopicRange','ProximalBPSCenteredDefect','ProximalBPSMacroscopicDefectRoot']:
 p=repo/'.lake/build/lib/lean/Tests'/(name+'.olean')
 if p.exists():
  b=p.read_bytes();oleans.append({'path':str(p),'bytes':len(b),'raw_sha256':hashlib.sha256(b).hexdigest(),'mtime_utc':datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),'qualification':'Existing binary observed only; neither freshly rebuilt nor independently source-alignment verified in this preread.'})
seal=json.loads((out/'source-first-graph-seal.json').read_text())
record={'schema':1,'actual_pin_read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_first_graph_seal_sha256':hashlib.sha256((out/'source-first-graph-seal.json').read_bytes()).hexdigest(),'sealed_graph_sha256':seal['graph_sha256'],'read_current_after_primary_graph_seal':True,'workspace_commit_observed':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'Mathlib_revision_observed':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo/'.lake/packages/mathlib',text=True).strip(),'no_Lean_authored_or_compile_run':True,'files':receipt,'existing_Test_binary_observations':oleans}
(out/'bounded-current-api-pins.json').write_bytes((json.dumps(record,indent=2)+'\n').encode('utf8'))
print(json.dumps({'workspace_commit':record['workspace_commit_observed'],'Mathlib':record['Mathlib_revision_observed'],'file_count':len(receipt),'Test_artifacts':len(oleans),'api_pins_sha256':hashlib.sha256((out/'bounded-current-api-pins.json').read_bytes()).hexdigest()},indent=2))
