from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/library-retrieval72');r.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
commands=[['rg','-n','--max-columns','180','--max-columns-preview','quadratic_corrector_perturbation|corrector_perturbation|C \\(u \\+|C \\(u\\+','AutoSamplingTheory','research-wiki/frontier-cells'],['rg','-n','--max-columns','180','--max-columns-preview','IsSelfAdjoint|Commute|Inv|A0\\*A0','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RootInverseCommutation.lean','AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean'],['rg','-n','--max-columns','180','--max-columns-preview','norm_add_sq_real|norm_sub_sq_real|real_inner_self_eq_norm_sq|def IsSymmetric|theorem.*isSymmetric',' .lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean'.strip(),'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean']]
# Resolve the existing parent module name before constructing any search argv.
parent=list(Path('AutoSamplingTheory/ExampleCases/ProximalBPS').glob('*Commutation.lean'))
assert len(parent)==1;commands[1][-2]=parent[0].as_posix()
rows=[]
for i,argv in enumerate(commands):
 q=subprocess.run(argv,capture_output=True);assert q.returncode in [0,1],q.stderr.decode()
 (r/f'{i}.stdout.exactraw.log').write_bytes(q.stdout);(r/f'{i}.stderr.exactraw.log').write_bytes(q.stderr)
 rows.append(dict(argv=argv,exit_code=q.returncode,stdout_RAW_sha256=sha(q.stdout),stderr_RAW_sha256=sha(q.stderr)))
paths=['lean-toolchain','lake-manifest.json','AutoSamplingTheory/Probability.lean','AutoSamplingTheory/SDE.lean','AutoSamplingTheory/TechnicalLemmas/Probability.lean','AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean',parent[0].as_posix(),'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean','research-wiki/technical-lemmas/README.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.md']
pins=[]
for name in paths:
 b=Path(name).read_bytes();pins.append(dict(path=name,RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n'))))
(r/'retrieval.json').write_text(json.dumps(dict(status='BOUNDED_LIBRARY_REUSE_SEARCH_BEFORE_72_SEAL',actual_PID=os.getpid(),searches=rows,inputs=pins,decision='Reuse actual71 same witnesses and produced inverse/commutation/square identity. Add one generic Hilbert perturbation leaf with a genuine original-input PBPS consumer, if prospective headers independently accepted. No matching local named perturbation target found in bounded search; no global absence proof.',source_plan='independent-source-first72/next-edge-proposal72.utf8.txt',proof_search=False,external_port=False,SLT_status_unchanged=True,claimed=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS72 bounded source/local/pinned Mathlib retrieval; no implementation/proof/claim.')
