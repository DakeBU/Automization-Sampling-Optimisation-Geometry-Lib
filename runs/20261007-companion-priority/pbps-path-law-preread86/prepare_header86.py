"""Statement-only preparation; execute only after distinct exact topology repair review."""
from pathlib import Path
import hashlib,json
R=Path('E:/Samplinglib');pre=Path(__file__).parent;r=pre.parent/'pbps-actual-finite-first-event-law86'
a=json.loads((pre/'root.topology-adoption86.json').read_bytes())
assert a['accepted'] and a['dependency_DAG_acyclic'] and not a['proof']
for k in ['effective_graph','effective_inventory']:
 p=R/a[k]['path']; assert hashlib.sha256(p.read_bytes()).hexdigest()==a[k]['raw_sha256']
parent=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean'
s=parent.read_text(encoding='utf-8');start=s.index('private def actual_phase_transition_kernel_statement');end=s.index('    let next :',start)
block=s[start:end].replace('actual_phase_transition_kernel_statement','actual_finite_first_event_law_statement',1)
assert 'theorem ' not in block
extra='''    let U : E → E → (E × E) → (ℕ → ℝ) → WithTop ℝ≥0 :=
      fun y xRef z sample => τ y xRef z (ε sample 0)
    let F : E → E → (E × E) → (ℕ → ℝ) → ℝ :=
      fun y xRef z sample => ((U y xRef z sample).untopD 0 : ℝ≥0)
    let A : E → E → (E × E) → ℝ≥0 → Set (ℕ → ℝ) :=
      fun y xRef z T => {sample | (0 : WithTop ℝ≥0) < U y xRef z sample ∧
        U y xRef z sample ≤ (T : WithTop ℝ≥0)}
    let d : E → E → (E × E) → ℝ → ℝ := fun y xRef z s =>
      rate xRef (Φ y xRef s z) * Real.exp (-Λ y xRef z (Real.toNNReal s))
    let ρ : E → E → (E × E) → ℝ≥0 → Measure ℝ := fun y xRef z T =>
      (volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))).withDensity
        (fun s => ENNReal.ofReal (d y xRef z s))
    let J : E → E → (E × E) → ℝ → (ℝ≥0 × (E × E)) :=
      fun y xRef z s => (Real.toNNReal s, S xRef (Φ y xRef s z))
    ∀ y xRef : E, ∀ z : E × E,
      Measurable (U y xRef z) ∧ Measurable (F y xRef z) ∧
      Measurable (J y xRef z) ∧
      (∀ T : ℝ≥0,
        MeasurableSet (A y xRef z T) ∧
        Measure.map (F y xRef z) (P.restrict (A y xRef z T)) = ρ y xRef z T ∧
        Measure.map (fun sample => J y xRef z (F y xRef z sample))
          (P.restrict (A y xRef z T)) = Measure.map (J y xRef z) (ρ y xRef z T) ∧
        IsFiniteMeasure (ρ y xRef z T) ∧
        (ρ y xRef z T).real Set.univ = 1 - Real.exp (-Λ y xRef z T) ∧
        ρ y xRef z T Set.univ ≤ 1 ∧
        (∀ h : (ℝ≥0 × (E × E)) → ℝ, Measurable h →
          ∀ M : ℝ, 0 ≤ M → (∀ a, |h a| ≤ M) →
            Integrable h (Measure.map (J y xRef z) (ρ y xRef z T)) ∧
            Integrable (fun sample => h (J y xRef z (F y xRef z sample)))
              (P.restrict (A y xRef z T)) ∧
            Integrable (fun s => h (J y xRef z s) * d y xRef z s)
              (volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))) ∧
            (∫ sample, h (J y xRef z (F y xRef z sample))
                ∂P.restrict (A y xRef z T)) =
              ∫ s, h (J y xRef z s) * d y xRef z s
                ∂volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))))
'''
prefix='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-! Prospective statement only. Actual first finite PBPS event, Appendix A.1
(A.1),(A.2) and the first density factor implicit in (A.7), arXiv2609.06905v1.
The finite subprobability and marked-test packaging is attributed ASTIS completion.
Literal actual Exp1 coordinate0, stopped wait and zero-normal identity reflection
are retained. F defaults to0 only outside the restricted positive finite event;
missing probability includes waits beyond T or infinite, without renormalization.
Full path law, unused-tail conditioning, reversal, invariance, semigroup/allL2,
implementation, error, unbounded expected query cost, main/composition remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

'''
r.mkdir(exist_ok=False);p=r/'header86.proposed.lean'
p.write_text(prefix+block+extra+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw\n',encoding='utf-8',newline='\n')
z={'status':'PROSPECTIVE_HEADER_ONLY_INDEPENDENT_REVIEW_PENDING','path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'literal_original_P_epsilon_c_Phi_S_rate_Lambda_tau_unchanged':True,'source_parent_raw_sha256':hashlib.sha256(parent.read_bytes()).hexdigest(),'reviewed_topology':a,'no_BODY':True,'StatementSeal':False,'claim_created':False}
(r/'header86.preparation.json').write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:z[k] for k in ['status','path','raw_sha256','bytes']}))
