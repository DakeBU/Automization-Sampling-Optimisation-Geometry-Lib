from pathlib import Path
import json,hashlib
r=Path.cwd();e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence'
pf='AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean';tf='Tests/GaussianComplexityLaplaceTail.lean'
P='AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail.max_eigenvalue_tail_le_iInf_trace_exp'
T='AutoSamplingTheory.Tests.GaussianComplexityLaplaceTail.actual_source_four_sums_laplace_tail'
def code(p,a,b):
    data=(r/p).read_bytes();text=data.decode(); ls=text.splitlines(keepends=True)
    span=''.join(ls[a-1:b]).encode()
    return {'file':p,'source_sha256':hashlib.sha256(data).hexdigest(),
      'mathematical_commit':'1d1103af694b9663a72b0d610004ed85c7c6b527',
      'LF_lines_1based_inclusive':[a,b],'exact_span_sha256':hashlib.sha256(span).hexdigest()}
rows=[]
def add(ids,meaning,p,a,b,parents=(),kind='ACTUAL_NEW_COMPILED_IMPLEMENTATION'):
    rows.append({'source_nodes':ids,'mathematical_meaning':meaning,'implementation_kind':kind,
      'actual_code':code(p,a,b),'canonical_parent_calls':list(parents),'independent_source_discharge_status':'PENDING fresh source review; native compile/type/value proof already checked'})
add(['TR.CONVENTIONS','TR.REGULARITY','TR.DOMAIN'],'Finite nonempty real matrices, AE self-adjointness/measurability, unnormalized trace, and explicitly disclosed scalar extended-expectation domain.',pf,8,20)
add(['BG.SPECTRAL','TR.EXP','TR.TRACE.DOMINATION'],'CFC diagonalization, cyclic trace, attained maximum eigenvalue, and one positive summand below the full trace exponential.',pf,22,51,['Matrix.IsHermitian.cfc_eq','Matrix.IsHermitian.spectrum_real_eq_range_eigenvalues','Matrix.trace_mul_cycle','Matrix.trace_diagonal','Set.Nonempty.csSup_mem','Finset.single_le_sum'])
add(['BG.MEAS'],'Continuity of matrix exponential and finite-dimensional trace supplies AE measurability of the positive trace observable.',pf,69,79,['NormedSpace.exp_analytic'])
add(['BG.HOMOG','TR.EVENT'],'Positive s preserves the scalar threshold order; the spectral/trace comparison supplies AE event inclusion without a measurable eigenbasis selector.',pf,80,85)
add(['BG.MARKOV','TR.FIXED.MARKOV','BG.NONNEG.EXPECTATION','TR.FIXED'],'Apply nonnegative scalar Markov directly to trace exponential and divide by the finite positive exp(st). This combines the two source elementary inequalities rather than requiring an intermediate scalar eigenvalue-exponential integral.',pf,86,94,['MeasureTheory.measure_mono_ae','MeasureTheory.meas_ge_le_lintegral_div','ENNReal.ofReal_inv_of_pos','Real.exp_neg'])
add(['BG.INF','TR.PROP3.1'],'The same fixed-s inequality for every positive parameter yields the indexed infimum. The threshold remains any real number.',pf,55,68)
add(['GC.MODEL','GC.TRUNC','GC.MEAN','GC.CENTER'],'Literal original unconditional Gaussian product experiment, own-row inclusive cutoff, actual mean, centered matrices and paired index order.',tf,44,75)
add(['GC.FEATURE.NORM','GC.Y.REGULARITY','BG.GAUSSIAN.ROW.MEAN'],'Reused pre-existing compiled parents carry the genuine feature/radial/mean regularity dependency closure. T invokes these actual declarations, not a default-zero-integral or imported-but-unproved premise.',tf,115,127,
 ['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds'],kind='REUSE_OF_EXISTING_COMPILED_CANONICAL_PARENTS_NO_NEW_LEAF_CREDIT')
add(['GC.RADIUS','GC.SUM.BOUND'],'Exact Ex111 separate Y/EY estimates enter through the radius parent; their triangle bound gives the Ex112 centered radius. |w|≤1 and |sign|=1 give a finite uniform norm bound for all four sums.',tf,123,156)
add(['GC.SELFADJOINT'],'Finite real scalar sums of actual Hermitian centered matrices preserve Hermiticity and measurability for all four cases.',tf,157,163)
add(['GC.FINITE.MGF'],'Internal CFC norm and positivity lemmas, then finite trace-exponential Bochner integrability under the original probability law.',tf,12,42)
add(['GC.FINITE.MGF'],'Use the actual sum norm bound to obtain matrix exponential integrability; the continuous linear trace map gives scalar integrability and nonnegativity.',tf,165,180)
add(['GC.FOUR'],'Apply public P to each literal signed weighted sum, select the fixed positive s, and use actual finite nonnegative trace expectation to convert lintegral to ofReal of the Bochner integral.',tf,181,191,[P,'MeasureTheory.ofReal_integral_eq_lintegral_ofReal'])
out={'schema_version':1,'status':'ROOT_AUTHORED_ACTUAL_SOURCE_LEAN_MAP; INDEPENDENT_FRESH_REVIEW_PENDING',
 'public_canonical_node':P,'associated_private_consumer':T,'new_public_nodes':1,
 'preproof_graph':'preproof-originals/source-graph.repaired.v2.1.json',
 'preproof_graph_sha256':'71f8e77ffc3ef686997e42b96f268ab191591f53dd161f5507dc6024cb308ab9',
 'original_graph_not_rewritten':True,'rows':rows,
 'explicit_sufficient_route':{'source_route':'scalar positive-threshold event -> Markov on exp(s λmax) -> spectral trace domination -> expectation monotonicity -> fixed s -> inf',
 'actual_route':'AE positive-threshold event inclusion directly into the trace-exponential event -> scalar nonnegative Markov on that trace observable -> reciprocal exponential -> inf',
 'relation':'Composition of the same source elementary comparisons; no new source binder, operator-exponential monotonicity or independent-sum product identity.'},
 'downstream_open':[{'node':'GC.NORM.EVENT','reason':'The source strict operator-norm > event to union of ± algebraic λmax ≥ events is outside sealed T, is not a T parent and is not discharged here.'},
 {'node':'GC.BERNSTEIN.CONSUMER','reason':'Independent-sum/Lieb/master-tail trace-MGF upper bound and exact Bernstein constants remain future mathematics.'}],
 'proof_ingredients_are_dependencies_not_new_target_assumptions':True,
 'purification_debt':'T128–133 contains unused local positivity calculations; retained immutable proof snapshot, no extra public credit; post-merge purification is separate.'}
(e/'source-lean-correspondence.authored-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
mem={'normal_state':'EXPLORING','advance':'ASTIS-SA-20261114-MatrixLaplaceTail','owner':'huanjian_20261114_matrix_laplace_tail',
 'mathematical_progress':'P and actual four-family T compiled; independent immutable native literal/type+value/kernel/q0/four Bool cases passed.',
 'public_progress_commit':'b3da3101e19255327ccedbc49730915f578e10e5','public_scope':'Compiled local mathematics only; actual remote readback observed.',
 'current_authored_context':'78798da7b9d1fd42fc4512bfe90663a140b438852b4996c6a5f48b7031b5c62a',
 'current_reader':'reader-preview-v3; native browser and independent visual acceptance pending',
 'next':['Finish exact-v3 independent source/whole-module/seven-slot and native reader acceptance','Complete portable evidence and bounded publication/frontier/contributor/semantic checks','One normal ROOT PROVED_LOCAL, then separate independent normal VERIFIED if all actual gates pass','Push accepted owned evidence via safe public lineage'],
 'global_open':'Both complete main lower bounds remain unclosed. Full Bernstein/C6 and oracle/TV/precision/cap/expected-cost/main/site/purification/whole-Goal acceptance remain separate.',
 'preservation':'No new Goal, no detached ASTIS, no old ledger/frontier reset or old owner takeover. Old foreign protection baseline remains local-only.'}
(e/'local-cycle-memory.json').write_text(json.dumps(mem,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'mapped_rows':len(rows),'open_norm_event_retained':True,'one_public_node':True}))
