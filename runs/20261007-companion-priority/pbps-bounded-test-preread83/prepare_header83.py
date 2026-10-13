from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83');r.mkdir(exist_ok=False)
p=Path('runs/20261007-companion-priority/pbps-actual-small-time-continuity82/header82.proposed.lean');b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='0333cf3e488effe1fa6f516553bb1e63a3bb650bfe09aca234ed20375cf85e64'
s=b.decode().replace('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability','import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity\nimport Mathlib.MeasureTheory.Integral.Bochner.Set').replace('Prospective exact statement82 only; no theorem proof or admission.','Prospective exact statement83 only; no theorem proof or admission.').replace('AppendixA.1 Ex22 small-time continuity ingredient.','AppendixA.1 Ex22 bounded-test expectation ingredient.').replace('The first-event defect probability and zero-time stochastic continuity are the\nnew obligations.','Measurable/integrable bounded continuous tests, the2M expectation defect estimate\nand zero-time expectation convergence are new obligations.').replace('ActualSmallTimeContinuity\nopen','ActualBoundedTestContinuity\nopen').replace('actual_small_time_stochastic_continuity_statement','actual_bounded_test_expectation_continuity_statement')
end='\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity\n';assert s.endswith(end)
addition='''
 ∧
      (∀ y xRef : E, ∀ z₀ : E × E,
        ∀ f : (E × E) → ℝ, Continuous f →
        ∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |f z| ≤ M) →
          (∀ t : ℝ≥0,
            Measurable (fun sample : ℕ → ℝ => f (Z y xRef z₀ t sample)) ∧
            Integrable (fun sample : ℕ → ℝ => f (Z y xRef z₀ t sample)) P ∧
            |(∫ sample, f (Z y xRef z₀ t sample) ∂P) -
                f (Φ y xRef (t : ℝ) z₀)| ≤
              2 * M * (1 - Real.exp (-Λ y xRef z₀ t))) ∧
          Tendsto (fun t : ℝ≥0 => ∫ sample, f (Z y xRef z₀ t sample) ∂P)
            (𝓝 0) (𝓝 (f z₀)))
'''
s=s[:-len(end)]+addition+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity\n'
(r/'header83.proposed.lean').write_text(s,encoding='utf8',newline='\n')
(r/'prospective-statement83.json').write_text(json.dumps(dict(status='PROSPECTIVE_EXACT_PROP_FOR_INDEPENDENT_REVIEW',source='arXiv2609.06905v1 AppendixA.1 Ex22, p6.1-p6.2',header_RAW_sha256=hashlib.sha256((r/'header83.proposed.lean').read_bytes()).hexdigest(),original_six_analytic_binders_unchanged=True,tests='Every continuous real f on product phase; every real M>=0 bounding abs(f) globally. Explicit ASTIS C_b elaboration of source C_c test class, not an added dynamics assumption.',retains='All original11 literal definitions and actual82 full jointly Borel/covered/fallback/fixed-parameter commonAE/init/defect/stochastic-continuity clauses.',new='Actual f(Z_t) measurable/integrable for each finite t; absolute expectation defect <=2M actualfirsteventbound; expectation tends f(z0) at ordinary nonpunctured NNReal0.',proof_started=False,seal=False,implementation_file_created=False,truth_boundary='Fixed deterministic parameters/test/bound; no uniform event/limit, unbounded-test expectation, AS path convergence, full L2/Markov/restart/semigroup/invariance/hypocoercivity/implementation/error/cost/composition/main or reader visual/PURIFIED/live.'),indent=2)+'\n',encoding='utf8',newline='\n')
print('Prospective whole-Prop83 only; RAW',hashlib.sha256((r/'header83.proposed.lean').read_bytes()).hexdigest())
