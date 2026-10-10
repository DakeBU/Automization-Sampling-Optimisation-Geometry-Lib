"""Prepare a source-facing prospective statement; no theorem BODY or proof credit."""
from pathlib import Path
import hashlib
import json
run = Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78')
source = run / 'source-preread78/source-freeze78.json'
assert hashlib.sha256(source.read_bytes()).hexdigest() == 'e61716072be6f95420594e513116277f4313214587d2eedab68e26a4bdc5f211'
parent = Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean')
raw = parent.read_text(encoding='utf8')
statement = raw.split('private def actual_fixed_reference_finite_jump_recursion_statement', 1)[1]
binders, rest = statement.split('    let c :', 1)
defs = '    let c :' + rest.split('    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0,', 1)[0]
energy, clock = defs.split('    let H :', 1)
clock = clock.split('    let Λ :', 1)[1]
defs = energy + '    let Λ :' + clock
header = '''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
import Mathlib.Topology.Order.WithTop

/-! Prospective statement only, PBPS arXiv2609.06905v1 Appendix A.1 Ex9.
Source standing analytic conditions and exact stopped recurrence are retained.
Actual inputs use the canonical Exp(1) product. No supplied stochastic/cap/time
certificate and no global physical-time process, Markov or invariance claim. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

def actual_fixed_reference_event_time_nonaccumulation_statement'''
header += binders + '''    let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
    let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun ω k => Real.toNNReal (ω k)
''' + defs + '''    ∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ ω ∂P,
      (∀ t : ℝ≥0, ∀ᶠ n : ℕ in atTop,
        (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε ω) n) ∧
      (∀ t : ℝ≥0, {n : ℕ | eventTime y xRef z₀ (ε ω) n ≤ (t : WithTop ℝ≥0)}.Finite)

#check actual_fixed_reference_event_time_nonaccumulation_statement
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation
'''
p = run / 'header78.proposed.lean'
assert not p.exists()
p.write_text(header, encoding='utf8', newline='\n')
manifest = {
    'status': 'PROSPECTIVE_NO_PROOF', 'header': p.as_posix(),
    'header_RAW_sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
    'source_freeze': source.as_posix(),
    'source_freeze_RAW_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'six_analytic_source_binders_unchanged': True,
    'new_provider_premises': [], 'literal_objects': ['P', 'epsilon', 'c', 'Phi', 'S', 'rate', 'Lambda', 'tau', 'next', 'record', 'eventTime'],
    'parameter_quantification': 'For every fixed deterministic y,xRef,z0, almost every canonical product sample; no uncountable event intersection is assumed.',
    'conclusions': ['Every finite horizon is eventually exceeded by actual event times.', 'Only finitely many event indices lie below each finite horizon, including index0.'],
    'source_to_implementation': 'Exact finite-parent definitions copied definitionally, H/C omitted from statement because they are proof ingredients to be produced internally.',
    'type_check': 'pending', 'independent_header_reviews': 'pending', 'statement_seal': 'pending',
    'theorem_BODY_created': False, 'Goal_complete': False,
}
(run / 'header78.prospective-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8')
print(p.as_posix())
