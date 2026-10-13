"""Prospective statement only, after independent source topology and exact repair."""
from pathlib import Path
import hashlib,json
pre=Path(__file__).parent;r=pre.parent/'pbps-actual-outer-bounded-l2-continuity84';r.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());adoption=load(pre/'root.topology-adoption84.json');assert not adoption['proof'] and adoption['dependency_DAG_acyclic']
for key in ['effective_graph','effective_inventory']:
 p=Path(adoption[key]['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==adoption[key]['RAW_sha256']
source=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean').read_text(encoding='utf8')
start=source.index('private def actual_bounded_test_expectation_continuity_statement');end=source.index('/-- Actual PBPS bounded real tests',start)
original=source[start:end].rstrip();block=original.replace('actual_bounded_test_expectation_continuity_statement','actual_outer_bounded_l2_continuity_statement',1)
addition='''
 ∧
      (let q : E → Measure E := fun y =>
         (volume : Measure E).tilted (fun x => -V x - ‖x - y‖ ^ 2 / (2 * η))
       let ν : E → Measure (E × E) := fun y => (q y).prod (stdGaussian E)
       (∀ y : E, IsProbabilityMeasure (q y) ∧ IsProbabilityMeasure (ν y)) ∧
       (∀ y xRef : E, ∀ f : (E × E) → ℝ, Continuous f →
         ∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |f z| ≤ M) →
           let A : ℝ≥0 → (E × E) → ℝ := fun t z₀ =>
             ∫ sample, f (Z y xRef z₀ t sample) ∂P
           (∀ t : ℝ≥0, Measurable (A t) ∧
             Integrable (fun z₀ : E × E => (A t z₀ - f z₀) ^ 2) (ν y) ∧
             (∀ z₀ : E × E, (A t z₀ - f z₀) ^ 2 ≤ 4 * M ^ 2)) ∧
           Tendsto (fun t : ℝ≥0 =>
             ∫ z₀, (A t z₀ - f z₀) ^ 2 ∂(ν y)) (𝓝 0) (𝓝 0)))
'''
head='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity
import AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! Prospective exact statement84 only; no theorem proof or admission.
PBPS arXiv2609.06905v1 AppendixA.1 Ex22 bounded-test outer square-integral ingredient.
All six original analytic conditions and the entire actual83 phase contract remain.
Exact conditional Gibbs x Gaussian probability normalization, state measurability,
square integrability, explicit4M2 domination and the outer zero-time limit are outputs.
The source uses C_c; C_b with an explicit global bound is an attributed ASTIS extension.
All-L2 AE operator/invariance/Jensen/contraction/density/Markov/main/cost remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

'''
p=r/'header84.proposed.lean';p.write_text(head+block+addition+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity\n',encoding='utf8',newline='\n')
(r/'header84.preparation.json').write_text(json.dumps(dict(status='PROSPECTIVE_HEADER_ONLY_INDEPENDENT_REVIEW_PENDING',path=p.as_posix(),RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,source_parent_private_Prop_prefix_exact_except_name=True,source_parent_RAW_sha256=hashlib.sha256(Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean').read_bytes()).hexdigest(),reviewed_source_topology=adoption,no_BODY=True,StatementSeal=False,claim_created=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print(p.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size,'bytes; no84 BODY or admission')
