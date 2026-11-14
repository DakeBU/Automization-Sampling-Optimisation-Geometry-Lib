#!/usr/bin/env python3
"""Prepare this reviewer's packet-bound result; no canonical mutation here."""
from pathlib import Path
import datetime, gzip, hashlib, json, os, subprocess, sys

ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=Path(__file__).resolve().parent
BASE=OUT.parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import astis_site

def sha(b):return hashlib.sha256(b).hexdigest()
def jb(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def put(n,x):(OUT/n).write_bytes(jb(x))
packet=json.loads((BASE/'fresh-reviewer-input.json').read_bytes())
phase1=OUT.parent/'phase1/source-expectations.json'
phase2=OUT.parent/'phase2/source-versus-blind-comparison.json'
assert sha(phase1.read_bytes())=='9200b0c66a9339f3b8198b3128fffac25032c593080e956bf08356c0311d637c'
assert sha(phase2.read_bytes())=='3319ee82fecc1c5fab860338c036f20f0ba773a9461875d30a86e636409155c7'
earlier=json.loads(phase2.read_bytes())
closure=json.loads((OUT/'actual-source-closure-and-fakeclosure.json').read_bytes())
declarations=astis_site.scan_project_sources()[1]
by_name={d.full_name:d for d in declarations}
GC='AutoSamplingTheory.ExampleCases.GaussianComplexity.'
TL='AutoSamplingTheory.TechnicalLemmas.'
def producer(name):
 d=by_name[name]
 assert not d.has_placeholder
 return {'declaration':name,'file':d.source_file,'line':d.source_line,
  'raw_module_sha256':sha((ROOT/d.source_file).read_bytes())}

mapping=[
 {'id':'O1','status':'discharged-in-actual-compiled-dependencies','producers':[
  TL+'Probability.OrthogonalHaar.orthogonalHaar_spec',GC+'DeterminantComponents.component_probabilities'],
  'review':'Full Haar constructor is the normalized whole compact group. A fixed row reflection exchanges the measurable determinant components, giving their exact half masses. component_probabilities yields the two twice-restricted probabilities from n>0, derived from hn.'},
 {'id':'O2','status':'discharged-in-actual-compiled-dependencies','producers':[
  GC+'DeterminantFamily.singleBlockPrecision_regular',GC+'DeterminantFamily.blockPrecision_regular',GC+'GaussianLawDensity.gaussian_law_eq_density',GC+'GaussianBlockLaw.actual_conditional_block_product',TL+'Measure.GaussianPrecisionDensity.multivariateGaussian_eq_withDensity_of_posDef'],
  'review':'Actual orthogonal precision matrices have the source spectral lower bound and are positive definite. GaussianBlockLaw identifies the genuine block inverse and uses positive-semidefinite inverse covariance in its characteristic-function calculation. GaussianLawDensity consumes the positive-definite precision-density theorem. The total inverse/Gaussian off-support extension is never used as source covariance mathematics.'},
 {'id':'O3','status':'discharged-in-actual-compiled-dependencies','producers':[
  GC+'GaussianMixtureLaws.actual_mixture_laws',GC+'AveragedBlockLaw.actual_averaged_block_product'],
  'review':'The Gaussian family is measurably identified with continuous precision densities. The tuple-to-precision pushforward is continuous; its compact range gives positive-definite support. The actual bind is a probability, and independent fixed-sign tuple averaging yields the actual product target law, rather than assuming it.'},
 {'id':'O4','status':'discharged-in-current-target-and-actual-compiled-dependencies','producers':[
  GC+'AveragedBlockLaw.actual_averaged_block_product',GC+'AffinityTensorization.actual_affinity_tensorization',TL+'InformationTheory.DensityAffinity.normalized_density_tv_affinity',GC+'TVAmplification.actual_averaged_tv_lower_bound'],
  'review':'Target hp/hm install actual probability instances. ht supplies absolute continuity. Mathlib IntegralRNDeriv gives genuine L1, mass one and event-density integrals. hset identifies exactly the actual event discrepancy set. The shared normalized-density theorem proves empty-event nonemptiness, boundedness, equality with one-half L1, and the lower affinity comparison. No infinity or unbounded-sup fallback supplies the bound.'},
 {'id':'O5','status':'discharged-in-actual-compiled-dependencies-with-recorded-equivalent-routes','producers':[
  GC+'SingleBlockSeparation.single_block_separation',GC+'ActualTotalVariation.actual_radial_test_tv',GC+'EvaluatedGaussian.selected_gaussian_value',GC+'GaussianExpectation.actual_gaussian_transform',GC+'DeterminantCancellation.signed_sqrt_det_integral',GC+'SphericalPoisson.spherical_poisson_moments',GC+'NumericSeparation.explicit_ratio_ge_exponential',GC+'SingleBlockAffinity.single_block_affinity_bound'],
  'review':'The actual Gaussian/Haar mixture radial test yields actual event TV, and the evaluated actual Gaussian integral gives Eq24. The B.7 sharp ratio and coarse 1/2 exp(-5n/sqrtκ) bound are then proved. SingleBlockAffinity uses normalized actual mixture densities, the shared TV/affinity inequality, and a verified log domain to obtain both Eq25 inequalities. No estimate is a new public premise. See route differences below; the general external Poisson representation is not claimed proved.'},
 {'id':'O6','status':'discharged-in-actual-compiled-dependencies','producers':[
  GC+'GaussianBlockLaw.actual_conditional_block_product',GC+'AveragedBlockLaw.actual_averaged_block_product',GC+'MixtureDensities.actual_mixture_densities',GC+'ProductDensity.actual_product_density',GC+'AffinityTensorization.actual_affinity_tensorization',TL+'InformationTheory.DensityAffinity.normalized_density_tv_affinity'],
  'review':'Actual Gaussian block laws and independent averaging produce Eq6. ProductDensity proves the literal contiguous split preserves Lebesgue volume, identifies actual normalized product densities, and proves the dimension-zero residual density is 1. AffinityTensorization relates actual ambient RN densities a.e. to those densities and factors the genuine affinity into a^k with residual mass 1. The final target uses the same a and actual law density conventions.'},
 {'id':'O7','status':'discharged-by-typed-construction-and-current-target-arithmetic','producers':[
  GC+'DeterminantFamily.blockPrecision',GC+'ProductDensity.actual_product_density',GC+'TVAmplification.actual_averaged_tv_lower_bound'],
  'review':'blockCoordinates/e use Nat.div_add_mod to construct the exact dimension equivalence. prodComm then finProdFinEquiv gives j*n+a; residual concatenation gives k*n+b. The exact anonymous expanded proposition compiles against the production theorem. The final natural-power monotonicity uses a≥0 and Real.exp_nat_mul/ring gives precisely k/8 and -10n/sqrtκ. k≥1 is source-derived but the power step works for every natural k, so no extra positivity premise is required.'},
]
for row in mapping:row['producers']=[producer(n) for n in row['producers']]

gap_targets={
 'G-FloorRemainder':['O7'], 'G-PrecisionGaussianKernel':['O2','O3'],
 'G-MixtureDensities':['O1','O3','O6'], 'G-ActualLawFactorization':['O3','O6'],
 'G-RepresentativeL1':['O4','O6'], 'G-CSAndExpansion':['O4','O5'],
 'G-SquaredBound':['O5'], 'G-LogExponential':['O5'],
 'G-TensorDensityCoordinates':['O6','O7'], 'G-SqrtProductTonelli':['O6'],
 'G-ResidualNormalization':['O6'], 'G-TVOverlap':['O4'], 'G-MinSqrtOrder':['O4'],
 'G-PowerExponential':['O7'], 'G-B6Standard':['O5'], 'G-B7Fubini':['O5'],
 'G-B6Application':['O5'], 'G-HaarSpherePoisson':['O5'], 'G-B7ScalarDomains':['O5'],
 'G-ActualProbabilitySup':['O1','O2','O3','O4'],
}
graph_path=BASE/'source-only-review/exact-seal-source-graph-v3.json'
graph=json.loads(graph_path.read_bytes())
gaps=[n for n in graph['source_nodes'] if n['kind']=='SOURCE_GAP']
assert {n['id'] for n in gaps}==set(gap_targets)
gap_map=[{'source_gap':n['id'],'source_meaning':n['meaning'],'mapped_obligations':gap_targets[n['id']],
 'literal_source_step_limit':('The displayed min-overlap identity is not separately exported by this final module. The checked half-L1 pointwise/integrated route is sufficient and explicitly disclosed in the lesson.' if n['id'] in {'G-TVOverlap','G-MinSqrtOrder'} else
 'The author general Poisson representation is an external source boundary; the implementation proves the two required moments by an explicit alternate mean-value/zero-flux route, without claiming the general theorem.' if n['id']=='G-HaarSpherePoisson' else
 'Source integrability uses the sharp minor bound 1; implementation compactness supplies a finite bound sufficient for cancellation, without exporting the sharp bound.' if n['id']=='G-B6Standard' else
 'Source scalar log-ratio integral estimate is replaced by tangent logarithm bounds with the same final constant; no exact integral estimate theorem is claimed.' if n['id']=='G-B7ScalarDomains' else
 'Actual compiled producers provide the needed sufficient conclusion; this does not change the source-only graph files or promote every source node to separately exported Lean credit.')}
 for n in gaps]

checks=[]
for p in sorted(OUT.glob('*.receipt.json')):
 r=json.loads(p.read_bytes())
 if 'exit_code' in r:
  assert r['exit_code']==0
  assert r['before']==r['after']
  assert r['before']['head']=='e4a1b8d60822706df62a7d4bab23814d7187c622'
  checks.append({'receipt':p.name,'receipt_sha256':sha(p.read_bytes()),'check':r['check'],'wall_seconds':r['wall_seconds'],'raw_log_sha256':r['raw_log_sha256'],'command':r['command']})
required={'fresh-target','fresh-test','fresh-affinity-parent','fresh-single-block-parent','fresh-actual-law-parent','independent-expanded-probe','fresh-density-comparison','fresh-product-density','fresh-b7-separation','fresh-haar-components','fresh-gaussian-block-law','fresh-determinant-cancellation','fresh-spherical-moments','fresh-gaussian-transform'}
assert required<={r['check'] for r in checks}
probe=gzip.decompress((OUT/'independent-expanded-probe.log.gz').read_bytes()).decode()
assert 'sorryAx' not in probe
assert probe.count('depends on axioms: [propext,')==6
source_names=['TVAmplification','AffinityTensorization','SingleBlockAffinity','AveragedBlockLaw','ProductDensity','MixtureDensities','DeterminantFamily','GaussianMixtureLaws','GaussianBlockLaw','SingleBlockSeparation','DeterminantComponents','BlockFamily','EvaluatedGaussian','ActualTotalVariation','SurfaceLaw','SelectedNumerator','GaussianExpectation','SphericalPoisson','GaussianLawDensity','NumericSeparation','DeterminantCancellation']
report={
 'kind':'Independent source, exact whole-module, compiled-parent and static candidate-reader review',
 'reviewer':'/root/ex72_fresh_source_v2',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'checked_metadata_head':'e4a1b8d60822706df62a7d4bab23814d7187c622',
 'immutable_math_candidate':'ebf76119351b23ef0718fc69aa5081515bab0b52',
 'source_edition':packet['candidate_publication_context']['source']['edition'],
 'raw_paper_sha256':'6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915',
 'phase1_expectation_sha256':sha(phase1.read_bytes()),'phase2_comparison_sha256':sha(phase2.read_bytes()),
 'full_reviewer_packet_raw_sha256':'848bf5545b0f4182bc1ec0f796fb3d2273aa5ef6ac7529b672b47ad9eec5fc80',
 'full_reviewer_packet_self_excluded_canonical_sha256':packet['packet_sha256'],
 'publication_binding_sha256':packet['publication_binding_sha256'],
 'current_context_receipt':json.loads((OUT/'current-publication-context-receipt.json').read_bytes()),
 'independence':{'formalizer':packet['roles']['formalizer'],'decoder':packet['roles']['blind_decoder'],'distinct_from_both':True,'source_first_then_blind_then_code_freezes_preserved':True,'prior_semantic_verdicts_read':False},
 'binder_audit':[
  {'binders':'d,n:ℕ; κ:ℝ','class':'TYPING','meaning':'Source integer dimensions and real condition number.'},
  {'binders':'hn:3≤n; hnd:n≤d; hκ:4≤κ','class':'STANDING','meaning':'Exactly §3.1/B.2 standing source domain, no oddness or query-budget restriction.'},
  {'binders':'letI measurable matrix space; let μ,ν,D,γ,M,δ','class':'TYPING/source-definition elaboration','meaning':'Local definitions, not logical premises. Exact explicit body checked by independent anonymous statement probe.'},
 ],
 'definition_audit':{'orthogonalHaar':'literal normalized full-Haar constructor with proven probability/specification','singleBlockPrecision_and_blockPrecision':'literal source Eqs.4/5 and exact contiguous coordinate elaboration','Gaussian_and_inverse':'total library constructors identified with intended covariance on the actual positive-definite support','RN_densities':'a.e. representatives with actual absolute continuity and finite-law L1/unit-mass facts','event_supremum':'normalized event TV after actual finite probability and exact event-density set equality','EXCESS_public_binders':[]},
 'whole_target_module_review':{'all_imports_scopes_and_source_body_reviewed':True,'public_declarations':1,'private_declarations':0,'scoped_logical_assumptions':[],'module_sha256':'9c96a4b80420bf114e700ed61f4adf88f79b85d24c4d21848e466d67b93ba431','test_sha256':'6bd58c4010c81dfa7948c9de1632c35fb0b14385bbdef5e5c28f5e1f2ca10cee','both_equal_immutable_ebf_git_objects':True},
 'entire_parent_module_texts_mathematically_read':[GC+n for n in source_names]+[TL+'InformationTheory.DensityAffinity',TL+'Probability.OrthogonalHaar'],
 'read_depth_limit':'All 48 project import-closure modules were snapshotted/hashed and sanitized-scanned. The listed module texts and the complete Test were mathematically inspected in full. The report does not claim line-by-line reproof of every transitive shared calculus/Mathlib theorem.',
 'seven_phase2_obligations':mapping,
 'source_graph_mapping':{'path':str(graph_path.relative_to(ROOT)),'sha256':sha(graph_path.read_bytes()),'source_gap_count':len(gap_map),'all_source_gap_ids_mapped':True,'gap_mapping':gap_map,'source_topology_compared_to_independent_phase1':True,'prior_topology_verdict_not_used':True,'boundary':'Source author topology stays distinct from the checked implementation route. No source graph status or foreign file is modified.'},
 'proof_route_differences':[
  'Source Ex72 uses TV=1-integral min followed by min≤sqrt. The canonical normalized-density theorem proves the equivalent integrated half-L1 pointwise inequality f+g-2sqrt(fg)≤|f-g|. The lesson explicitly explains this alternate algebraic route and does not claim a separately exported min-integral identity.',
  'Source A.1 cites general Poisson representation. SphericalPoisson proves precisely the two normalized spherical moments by harmonic Poisson-kernel mean value and zero flux of a pole-excluded potential. It explicitly does not prove or credit the cited general representation theorem; n=2 is an upstream extension, while this target retains n≥3.',
  'The source B.7 integral logarithm estimate is replaced by two log tangent bounds giving the same 3/sqrtκ intermediate and exact 5/sqrtκ final exponent.',
  'B.6 integrability of principal-minor weights uses compact-continuous boundedness instead of exporting the source sharp bound |minor|≤1. It proves the same cancellation with the same actual Haar law and Borel/L1 input.',
  'The actual [0,1] bounded-test comparison is implemented through a Bernoulli test kernel and the shared TV contraction theorem. Its factor is one, matching the source convention.',
 ],
 'compiler_checks':checks,
 'compiler_limit':'Fresh direct Lean source elaborations with isolated olean outputs, exact current HEAD/time/pin hashes and logs. No additional root build, Registry acceptance, whole-project gate or site build is invented.',
 'axioms':{'actual_target_and_five_critical_producers':['propext','Classical.choice','Quot.sound'],'sorryAx_or_custom_axioms':False,'probe_receipt':'independent-expanded-probe.receipt.json'},
 'fake_closure':{'closure_modules':48,'closure_lines':9465,'sanitized_matches':0,'extra_test_and_independent_probe_checked':True,'artifact':'actual-source-closure-and-fakeclosure.json'},
 'static_reader':{'structural_receipt':'static-reader-structural-receipt.json','exact_code_receipt':'static-reader-exact-code-receipt.json','three_exact_candidate_html_snapshots':True,'source_and_lesson_math_proof_checked':True,'source_attribution_domain_constants_and_residual_preserved':True,'statement_and_proof_closed_by_default':True,'embedded_statement_and_full_proof_exact_source_substrings':True,'downloaded_module_exact_current_source':True,'preview_status':'Existing ebf candidate; pending metadata and no current root gate recorded, correctly visible.','environmental_limit':'IAB unavailable. Chrome file:// action rejected by browser URL security policy, allowing only http/https and explicitly prohibiting workaround. No workaround/retry through another route. No live/rendered/mobile/actual-Chrome acceptance.','scope_confirmation':'Root confirmed exact static HTML/content/disclosure review is the source-V scope; live canonical-site acceptance belongs to later independent integration.'},
 'fidelity_judgment':'equivalent-after-elaboration',
 'blocking_mathematical_or_source_deltas':[],
 'repair_proposals':[],
 'source_V_boundary':'Only the actual Ex72 source-theorem edge. Later normal STAB, canonical root/site/gates, live Chrome, remote publication, purification, oracle/query lower bounds, whole-paper and whole-Goal completion remain separate.',
}
put('independent-review-run.json',report)
run_sha=sha((OUT/'independent-review-run.json').read_bytes())
slot_evidence={
 'objects':('explicit-elaboration','O1–O4 identify the full normalized-Haar sign priors, exact source precision maps and actual Gaussian binds. Independent explicit anonymous proposition compiles definitionally against the production theorem.'),
 'domains':('same','Production and expanded probe retain exactly natural d,n with 3≤n≤d and real κ≥4; all residuals including d%n=0. No T, ε or odd-n premise.'),
 'quantifiers':('equivalent','Universals match source construction for every admissible d,n,κ; the two sign instances and zero-based indices preserve the source quantification and fixed-sign independence.'),
 'assumptions':('explicit-elaboration','O1–O7 are produced internally by actual compiled dependencies. Only the three source-domain inequalities are public premises; no probability, L1, actual-law, B.7, affinity, or product premise is smuggled in.'),
 'conclusion':('equivalent','O4 gives exactly source TV for Mpos/Mneg; actual Ex71 plus actual Eq25 and the checked final natural-power calculation yield the exact Ex72 bound/direction, not a surrogate scalar theorem.'),
 'scopes':('explicit-elaboration','Source event/half-L1 TV, unsquared affinity, actual RN a.e. density meanings, finite event real masses, literal contiguous coordinates and zero-dimensional unit residual are all connected by O1–O7. Static lesson explicitly discloses the equivalent half-L1 proof route.'),
 'constant_dependencies':('same','The proof preserves 1/2 and 5 in actual B.7, then 1/4 and 10 under squaring, 1/8 under root/log conversion, and exactly k/8 in Ex72. No unrecorded constants or asymptotic replacement.'),
}
slots={}
for row in earlier['slot_comparisons']:
 name=row.get('contract_alias',row['slot']);relation,evidence=slot_evidence[name]
 slots[name]={'original':json.dumps(row['source_expectation'],ensure_ascii=False,sort_keys=True),
  'reconstructed':row['blind_reading'],'relation':relation,'evidence':evidence+' Exact producers, source-module hashes/lines, actual compile logs and route distinctions: '+str((OUT/'independent-review-run.json').relative_to(ROOT))+'.'}
deltas=[
 {'slot':'objects','severity':'informational','description':'Actual Gaussian/inverse, measure real values and real supremum are total library operations. Actual positive-definite support and normalized finite laws internally establish their source meaning.','evidence':'Independent phase2 O1–O4 concerns discharged by exact compiled producers and current target RN/event-set adapters in independent-review-run.json.'},
 {'slot':'scopes','severity':'informational','description':'The final proof uses an equivalent half-L1 integrated comparison rather than separately exporting the displayed min-overlap identity. The authored formula proof discloses that route.','evidence':'Complete DensityAffinity module and target hset/htv read; current lesson step3 matches actual proof, with exact static HTML/source extraction verified.'},
 {'slot':'constant_dependencies','severity':'informational','description':'Upstream analytic implementations use direct spherical moments, tangent log bounds and compactness-bounded minors as explicit sufficient alternatives to particular source background proof steps. The actual source parameters and final numerical constants remain unchanged.','evidence':'SphericalPoisson, NumericSeparation and DeterminantCancellation modules inspected; fresh source elaborations/axiom closure recorded; general external Poisson representation is not claimed formalized.'},
]
result={'semantic_slots':slots,'deltas':deltas,'verdict':'equivalent-after-elaboration','repairs':[],
 'reviewer':'/root/ex72_fresh_source_v2','independent_from_formalizer':True,'independent_from_decoder':True,
 'review_evidence':'Independent raw-source-first phase1 frozen 9200b0c66a9339f3b8198b3128fffac25032c593080e956bf08356c0311d637c; selective source-versus-blind phase2 frozen 3319ee82fecc1c5fab860338c036f20f0ba773a9461875d30a86e636409155c7 before full context. Exact whole-module/actual-parent/source/static-reader review and fresh source checks at metadata HEAD e4a1b8d60822706df62a7d4bab23814d7187c622, unchanged candidate source/Test ebf bytes, prove all seven phase2 concerns internally. See '+str((OUT/'independent-review-run.json').relative_to(ROOT))+' and its exact logs. Static content/disclosure acceptance only; live browser security rejection preserved and no live/current-site/root/remote/purification completion is claimed.',
 'review_run_sha256':run_sha,'reviewer_packet_sha256':packet['packet_sha256']}
put('review-result.json',result)
audit_path=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-tv-amplification.json'
raw_audit=audit_path.read_bytes();audit=json.loads(raw_audit)
assert audit['state']=='blind-reconstructed' and audit['source_review']['state']=='pending'
assert audit['lean']['formalizer']==packet['roles']['formalizer']
assert audit['reconstruction']['decoder']==packet['roles']['blind_decoder']
(OUT/'canonical-audit-before.raw.json.gz').write_bytes(gzip.compress(raw_audit,mtime=0))
audit.update({'state':'source-reviewed','semantic_slots':slots,'deltas':deltas,'verdict':result['verdict'],'repairs':[]})
audit['source_review']={'state':'accepted','reviewer':result['reviewer'],'independent_from_formalizer':True,'independent_from_decoder':True,'reviewer_packet_sha256':result['reviewer_packet_sha256'],'evidence':result['review_evidence'],'review_run_sha256':run_sha,'run_artifact':str((OUT/'review-result.json').relative_to(ROOT))}
assert audit['publication_binding_sha256']==packet['publication_binding_sha256']
assert audit['publication_context']==packet['candidate_publication_context']
put('proposed-canonical-audit.json',audit)
for name in ['independent-review-run.json','review-result.json','proposed-canonical-audit.json']:
 os.chmod(OUT/name,0o444)
print(json.dumps({'review_run_sha256':run_sha,'review_result_sha256':sha((OUT/'review-result.json').read_bytes()),'proposed_audit_sha256':sha((OUT/'proposed-canonical-audit.json').read_bytes()),'verdict':result['verdict'],'blocking_deltas':0,'canonical_files_changed':False},indent=2))
