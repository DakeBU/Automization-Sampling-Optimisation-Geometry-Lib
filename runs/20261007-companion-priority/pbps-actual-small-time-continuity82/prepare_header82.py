from pathlib import Path
import hashlib,json
r=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean')
assert sha(p.read_bytes())=='bf8f66a8484fa82c46b26ac6b66a6c8484e6dd6465ac8587d7e27b2489e73a5c'
s=p.read_text(encoding='utf8').split('\n\nset_option maxHeartbeats',1)[0]
start=s.index('/-!');end=s.index('namespace ',start)
s=s[:start]+'''/-! Prospective exact statement82 only; no theorem proof or admission.
PBPS arXiv2609.06905v1 AppendixA.1 Ex22 small-time continuity ingredient.
The actual phase/recurrence and all original six analytic conditions are literal.
The first-event defect probability and zero-time stochastic continuity are the
new obligations. Markov/restart/semigroup/invariance/L2 and main/cost remain open. -/
'''+s[end:]
s=s.replace('namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability','namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity')
s=s.replace('private def actual_physical_time_measurable_phase_statement','private def actual_small_time_stochastic_continuity_statement')
s=s.replace('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover','import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability')
s+=''' ∧
      (∀ y xRef : E, ∀ z₀ : E × E,
        (∀ t : ℝ≥0,
          MeasurableSet {sample : ℕ → ℝ |
            Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ∧
          P.real {sample : ℕ → ℝ |
            Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ≤
              1 - Real.exp (-Λ y xRef z₀ t)) ∧
        (∀ δ : ℝ, 0 < δ →
          (∀ t : ℝ≥0, MeasurableSet {sample : ℕ → ℝ |
            δ ≤ ‖Z y xRef z₀ t sample - z₀‖}) ∧
          Tendsto (fun t : ℝ≥0 => P.real {sample : ℕ → ℝ |
            δ ≤ ‖Z y xRef z₀ t sample - z₀‖}) (𝓝 0) (𝓝 0)))

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity
'''
dest=r/'header82.proposed.lean';assert not dest.exists();dest.write_text(s,encoding='utf8',newline='\n')
(r/'prospective-statement82.json').write_text(json.dumps(dict(status='PROSPECTIVE_HEADER_ONLY_NOT_SEALED',proof_started=False,header_RAW_sha256=sha(dest.read_bytes()),actual80_literal_parent_RAW_sha256=sha(p.read_bytes()),theorem_delta='Actual first-event defect probability bound and zero-time stochastic continuity; original actual Z properties retained',domain='Neighborhood0 in NNReal is the relative finite nonnegative time limit; all source parameters fixed in each probability/limit',source='Exact primary v1 Ex22 and independently frozen36item/13node/20edge source82 graph',truth_boundary='No process Markov/restart/semigroup, invariance/L2/hypocoercivity, random-input alltime law, cost/error/composition/main result or wholeGoal completion'),indent=2)+'\n',encoding='utf8',newline='\n')
print('Prospective82 exact literal header only:',sha(dest.read_bytes()))
