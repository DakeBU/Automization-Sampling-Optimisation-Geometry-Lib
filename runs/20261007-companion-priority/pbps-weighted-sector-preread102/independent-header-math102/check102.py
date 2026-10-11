from prepare102 import *
import time,re
header=(P/'Header102.lean').read_bytes()
target=O/'FreshHeader102.lean';assert not target.exists();target.write_bytes(header)
queries=[
 ['rg','-n','weighted.*sector|sector.*weighted|withDensity.*Theta','AutoSamplingTheory/ExampleCases/ProximalBPS','AutoSamplingTheory/TechnicalLemmas'],
 ['rg','-n','withDensity|MeasurePreserving|lintegral_comp|change.of.variables','research-wiki/external-lean-libraries'],
 ['rg','-n','theorem lintegral_comp|lintegral_comp_emb','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Map.lean'],
 ['rg','-n','Measurable.exp|Measurable.ennreal_ofReal|theorem Measurable.mul ','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/SpecialFunctions/Basic.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Real.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Arithmetic.lean']]
results=[]
for q in queries:
 p=subprocess.run(q,cwd=R,capture_output=True);assert p.returncode in [0,1];results.append(dict(argv=q,exit_code=p.returncode,stdout=p.stdout.decode('utf8'),stderr=p.stderr.decode('utf8')))
save('independent-retrieval102.native.json',dict(kind='independent-bounded-retrieval',queries=results,catalog=info(R/'research-wiki/external-lean-libraries/README.md'),SLT_card=info(R/'research-wiki/external-lean-libraries/lean-stat-learning-theory.md'),decision='No existing actual weighted-sector theorem found in the bounded local search. Reuse public93/97/101 and fixed Mathlib measure-preserving lintegral API. External reference cards provide no needed extra port; their content is not a callable certificate.',no_external_port=True,no_new_library_dependency=True,search_scope_bounded=True))
save('pregraph-projection-erratum102.native.json',dict(kind='append-only-independent-pregraph-API-ordinal-clarification',original=info(O/'pregraph-reconstruction102.native.json'),field='hidden_regularity_contracts[0]',correction='The public actual_finite_count_path_law exports actual density measurability as the THIRD member of its terminal joint-measurability block, after Hist interpolation and actual Gamma. The second projection description matched the smaller internal data bundle, not the full public theorem. Use only the actual public theorem and its appropriately nested public conjunction.',public_statement_lines=[1968,1974],public_body_lines=[2123,2129],mathematical_route_unchanged=True,public_parent_unchanged='actual_finite_count_path_law',no_private_API_allowed=True,no_Lean_implementation_or_attempt=True))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(target.relative_to(R))]
start=time.time()
with (O/'fresh-type.stdout.log').open('xb') as out,(O/'fresh-type.stderr.log').open('xb') as err:p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
save('fresh-type-receipt102.native.json',dict(kind='independent-original-header-type-elaboration',command=argv,exit_code=p.returncode,seconds=time.time()-start,header=info(P/'Header102.lean'),exact_header_copy=info(target),exact_bytes_equal=header==target.read_bytes(),stdout=info(O/'fresh-type.stdout.log'),stderr=info(O/'fresh-type.stderr.log'),Lean='4.33.0',Mathlib_commit=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R).decode().strip(),type_only=True,no_theorem_proof=True))
assert p.returncode==0
print('PASS_FRESH_HEADER_TYPE_ONLY',sha(header),flush=True)
