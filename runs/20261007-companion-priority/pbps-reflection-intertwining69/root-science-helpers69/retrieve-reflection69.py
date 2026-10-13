from pathlib import Path
import hashlib,json,subprocess,os
root=Path.cwd();pre=Path('runs/20261007-companion-priority/pbps-reflection-rotation-preproof69')
out=pre/'library-retrieval69';out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
names=['lean-toolchain','lake-manifest.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.md','AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean']
rows=[]
for i,name in enumerate(names):
 b=Path(name).read_bytes();q=out/f'{i}.exactraw.snapshot';q.write_bytes(b)
 rows.append(dict(path=name,raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),exact_snapshot=q.as_posix()))
cmd=['rg','-n','intertwin|star B.*D|block_algebra|adjoint_comp|adjoint_adjoint','AutoSamplingTheory/TechnicalLemmas','AutoSamplingTheory/ExampleCases/ProximalBPS','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean','-g','*.lean']
q=subprocess.run(cmd,capture_output=True);assert q.returncode==0
(out/'search.stdout.exactraw.log').write_bytes(q.stdout);(out/'search.stderr.exactraw.log').write_bytes(q.stderr)
result=dict(status='FIXED_LIBRARY_AND_ACTUAL_PARENT_SEARCHED_NO_PROOF_SEARCH',actual_pid=os.getpid(),command=cmd,exit_code=q.returncode,inputs=rows,
 same_actual_parent='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation',
 existing_block_result='ReflectionL2 has a theorem-local generic block_algebra producing star B D=-A star B. It is a local proof ingredient, not an exported callable declaration. Its existential actual reflection theorem cannot be applied to silently replace the already fixed SAME U.',
 intended_reuse=['Original-input ActualRootCommutation parent and its SAME U/P/A0/Inv/B0/V0/R witnesses','Mathlib ContinuousLinearMap.adjoint_comp and adjoint inner identities','The actual conditional projection and ambient adjoint adapters already compiled locally'],
 no_new_shared_leaf_claim=True,no_SLT_OpenAI_or_external_floating_source=True,no_statement_change=True,no_SAU_or_Lean_write=True)
(pre/'root.library-retrieval69.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS69 fixed library retrieval; reuse SAME actual parent; theorem-local block algebra is not a new exported declaration.')
