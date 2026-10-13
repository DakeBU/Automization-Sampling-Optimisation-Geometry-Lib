from pathlib import Path
r=Path(__file__).parent
s=Path('runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83/seal_and_claim83.py').read_text(encoding='utf8')
replacements=[
 ('pbps-bounded-test-preread83','pbps-outer-bounded-l2-preread84'),
 ('independent-review-adoption83','independent-review-adoption84'),
 ('header83.proposed','header84.reviewed'),
 ('1bf2b24f0ba521449aba10ac3559a27c4db7f2eab0df89c98587f623695b07ff','5c4e379caa337d1ac903d509eca30ef7db7b1905715c7a65b878afb33f9d2ded'),
 ("assert not load(r/'prospective-statement83.json')['proof_started']","assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean').exists()"),
 ('ASTIS-SA-20261010-PBPSActualBoundedTestContinuity','ASTIS-SA-20261011-PBPSActualOuterBoundedL2Continuity'),
 ('ASTIS-SA-20261010-PBPSActualSmallTimeContinuity','ASTIS-SA-20261010-PBPSActualBoundedTestContinuity'),
 ('ASTIS-SW-PBPS-actual-bounded-test-continuity','ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity'),
 ('ASTIS-SW-PBPS-actual-small-time-continuity','ASTIS-SW-PBPS-actual-bounded-test-continuity'),
 ('ActualBoundedTestContinuity.lean','ActualOuterBoundedL2Continuity.lean'),
 ('ActualBoundedTestContinuity.actual_bounded_test_expectation_continuity','ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity'),
 ('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity','lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity'),
 ('source_freeze83.closed-raw-manifest.json','source_freeze84.raw-manifest.json'),
 ('source_proof_graph83.reviewed-effective.json','source_proof_graph84.reviewed-effective.json'),
 ('source_inventory83.json','source_inventory84.reviewed-effective.json'),
 ('root.topology-adoption83.json','root.topology-adoption84.json'),
 ("r/'retrieval83/reuse-decision83.json'","pre/'retrieval84-v2/reuse-decision84.json'"),
 ('root.statement-seal83','root.statement-seal84'),
 ('publication-packet-before-proof83','publication-packet-before-proof84'),
 ('frontier-before-proof83','frontier-before-proof84'),
 ]
for a,b in replacements:
 assert a in s,a
 s=s.replace(a,b)
start=s.index('parents=');end=s.index('\ndelta=',start)
s=s[:start]+"parents=[base+'ActualBoundedTestContinuity.actual_bounded_test_expectation_continuity',base+'GibbsAugmentation.normalized_augmentation_density','AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']"+s[end:]
def assign(name,value):
 global s
 start=s.index(name+'=');end=s.index('\n',start)
 s=s[:start]+name+'='+repr(value)+s[end:]
delta='Under original six analytic hypotheses, retain the entire actual83 physical phase and derive exact conditional Gibbs-times-Gaussian probability, state measurability of actual clock expectations, integrable square differences bounded by4M2, and their outer integral convergence to0 at ordinary NNReal0 for every bounded continuous real test.'
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 AppendixA.1 Ex22 p6.1-p6.2. ASTIS explicit bounded-continuous extension of the source compactly supported continuous test class; bounded outer square-integral ingredient only.'
boundary='Retains actual83 full joint measurable physical phase, covered/fallback/commonAE/init/defect/smalltime/test clauses and literal eleven definitions. Exact q_y=volume.tilted(-V-quadratic), nu_y=q_y.prod(stdGaussian) probability derived internally. Fixed y and xRef; actual independent Exp1 clock expectation, state measurability,4M2 domination and bounded-test outer square-integral zero-time limit. No invariant-law, contraction or density premise. All-L2 AE operator/Jensen/contraction/density, phase invariance, restart/Markov/semigroup/hypocoercivity, implementation/error/unbounded cost/composition/main/PURIFIED/live/whole-Goal remain OPEN.'
assign('delta',delta);assign('anchor',anchor);assign('boundary',boundary)
s=s.replace('Actual82 phase/defect; bounded integrability; integrate discrepancy on defect via existing Mathlib; continuous actual flow/hazard and squeeze.','Actual83 pointwise expectation; derive exact q and nu probability with existing Gibbs/Gaussian kernel; measurable parameter integral;4M2 square bound; finite-probability filter DCT.')
s=s.replace('Actual PBPS bounded-test integrability and expectation continuity','Actual PBPS bounded-test outer square-integral continuity')
s=s.replace('Source AppendixA.1 Ex22 p6.1-p6.2 pointwise clock expectation before outer-state L2 dominated convergence.','Source AppendixA.1 Ex22 p6.2 outer square-integral bounded-test step before all-L2 invariant-operator/contraction/density extension.')
s=s.replace('Continuous real f and forall global nonnegative M bound are the explicitly attributed ASTIS C_b test class, extending source C_c; no probability/integral estimate premise.','Continuous real f and forall global nonnegative M bound are the explicitly attributed ASTIS C_b class extending source C_c; exact q/nu normalization and all integral conclusions are outputs, with no invariant-law premise.')
s=s.replace('Literal actual eleven definitions and every actual82 phase clause retained, same probability input and deterministic fallback.','Literal actual eleven definitions and every actual83 phase clause retained; same actual clock input, deterministic fallback, exact conditional tilt q and Gaussian product nu.')
s=s.replace('Independent30inventory/17nodes/30relations:29dependencies and1boundary association; reviewed AND within optional branch and OR across sufficient branches. Header accepted; BODY source review still OPEN.','Independent47inventory/23nodes/39relations:37dependencies including5futureOPEN and2excludedassociations; normalization OR routes internally AND, outer DCT inputs AND. Exact topology and one-line syntax overlays independently accepted; BODY source review still OPEN.')
s=s.replace('Source pointwise expectation step suppresses bounded-test integrability and explicit2M first-event integral estimate. Full outerL2 extension excluded.','Source bounded-test outer square-integral step suppresses exact-law normalization, parameter-integral measurability and4M2 domination. All-L2 extension requires independent invariance/contraction/density and is excluded.')
s=s.replace('Pinned primary Ex22, actual82/75/73/UnitExponentialProduct and fixed Mathlib','Pinned primary Ex22, actual83/GibbsAugmentation/GaussianConditionalKernel/UnitExponentialProduct and fixed Mathlib')
s=s.replace("['Retain all actual physical-phase clauses and exceptional conventions.','Measurable bounded tests on actual probability input are integrable.']","['Retain all actual83 physical-phase clauses and exceptional conventions.','Derive exact conditional Gibbs and Gaussian product probability internally.','Parameter-integral measurability and finite-probability4M2 dominated convergence.']")
s=s.replace('Actual82 has no bounded-test integration or expectation limit.','Actual83 has fixed-state expectation convergence, no outer square-integral convergence.')
s=s.replace('actual-defect/2M-indicator-integral/hazard-flow-continuity/expectation-squeeze','actual83-pointwise/exact-conditional-law/state-measurability/4M2/filter-DCT')
s=s.replace("['actual82-phase-defect','bounded-test-integrability','2M-indicator-integral','hazard-flow-continuity','expectation-limit']","['actual83-phase-expectation','exact-q-nu-probability','state-expectation-measurability','4M2-domination','outer-square-integral-limit']")
s=s.replace("print('83 exact independently reviewed statement sealed and claimed; no proof credit')","print('84 exact independently reviewed statement sealed and claimed; no proof credit')")
dest=r/'seal_and_claim84.py';assert not dest.exists();dest.write_text(s,encoding='utf8',newline='\n')
