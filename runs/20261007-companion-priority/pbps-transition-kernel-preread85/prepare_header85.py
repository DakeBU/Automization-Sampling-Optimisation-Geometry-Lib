"""Prospective actual-law interface only; no Statement Seal or proof search."""
from pathlib import Path
import hashlib,json
pre=Path(__file__).parent;r=pre.parent/'pbps-actual-phase-transition-kernel85'
load=lambda p:json.loads(Path(p).read_bytes())
a=load(pre/'root.topology-adoption85.json');assert a['dependency_DAG_acyclic'] and not a['proof']
for k in ['effective_graph','effective_inventory']:
 assert hashlib.sha256(Path(a[k]['path']).read_bytes()).hexdigest()==a[k]['RAW_sha256']
parent=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean')
s=parent.read_text(encoding='utf8');start=s.index('private def actual_physical_time_measurable_phase_statement')
end=s.index('\n\nset_option maxHeartbeats',start)
block=s[start:end].rstrip().replace('actual_physical_time_measurable_phase_statement','actual_phase_transition_kernel_statement',1)
assert 'theorem actual_physical_time' not in block and 'set_option' not in block
addition='''
      ∧ (∃ K : Kernel (((E × E) × (E × E)) × ℝ≥0) (E × E),
        IsMarkovKernel K ∧
        (∀ y xRef : E, ∀ z₀ : E × E, ∀ t : ℝ≥0,
          K (((y, xRef), z₀), t) = Measure.map (Z y xRef z₀ t) P) ∧
        (∀ y xRef : E, ∀ z₀ : E × E, ∀ t : ℝ≥0,
          ∀ B : Set (E × E), MeasurableSet B →
            K (((y, xRef), z₀), t) B = P ((Z y xRef z₀ t) ⁻¹' B)) ∧
        (∀ y xRef : E, ∀ z₀ : E × E,
          K (((y, xRef), z₀), 0) = Measure.dirac z₀) ∧
        (∀ y xRef : E, ∀ z₀ : E × E, ∀ t : ℝ≥0,
          ∀ g : (E × E) → ℝ, Measurable g →
            ∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |g z| ≤ M) →
              Integrable g (K (((y, xRef), z₀), t)) ∧
              Integrable (fun sample => g (Z y xRef z₀ t sample)) P ∧
              (∫ z, g z ∂K (((y, xRef), z₀), t)) =
                ∫ sample, g (Z y xRef z₀ t sample) ∂P))
'''
prefix='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability
import Mathlib.Probability.Kernel.Composition.Prod
import Mathlib.Probability.Kernel.Composition.MapComap

/-! Prospective statement85 only. PBPS arXiv2609.06905v1 AppendixA.1 actual
transition laws and bounded measurable tests. ASTIS all-finite jointly indexed
probability-kernel packaging; the six original analytic conditions and eleven
literal algorithm definitions, actual iidExp1 P and full actual80 Z contract remain.
The SAME actual Z supplies every fiber law, zero-time Dirac initialization and
bounded Borel real-test integrability/expectation transfer. IsMarkovKernel means
probability fibers only, not process Markov/restart/Chapman-Kolmogorov.
Invariance/path-reversal/fullL2/hypocoercivity/implementation/cost/main remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

'''
r.mkdir(exist_ok=False);p=r/'header85.proposed.lean'
p.write_text(prefix+block+addition+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel\n',encoding='utf8',newline='\n')
(r/'header85.preparation.json').write_text(json.dumps(dict(status='PROSPECTIVE_HEADER_ONLY_INDEPENDENT_REVIEW_PENDING',path=p.as_posix(),RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,source_parent_private_Prop_prefix_exact_except_name=True,source_parent_RAW_sha256=hashlib.sha256(parent.read_bytes()).hexdigest(),reviewed_source_topology=a,no_BODY=True,StatementSeal=False,claim_created=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print(p.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size,'bytes; prospective only')
