from pathlib import Path
import json, os

p = Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean')
out = Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
b = p.read_bytes()
(out / 'module.before.exactraw.lean').write_bytes(b)
s = b.decode('utf8')
old = '''  rcases actual_hazard_primitive_laws hα hαβ hV hH hη hβη with
    ⟨hΛ, hΛmeas, hInt, hbasic, hcaps⟩'''
new = '''  have hp :
      Continuous (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
        Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
        Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
      (∀ y xRef : E, ∀ z : E × E, ∀ t : ℝ≥0,
        IntervalIntegrable (fun s : ℝ => rate xRef (Φ y xRef s z)) volume 0 (t : ℝ)) ∧
      (∀ y xRef : E, ∀ z : E × E,
        Λ y xRef z 0 = 0 ∧ (∀ t : ℝ≥0, 0 ≤ Λ y xRef z t) ∧
        Monotone (Λ y xRef z)) ∧
      (∀ y xRef : E, ∀ z : E × E, 0 ≤ C y xRef z ∧
        ∀ t : ℝ≥0, Λ y xRef z t ≤ C y xRef z * (t : ℝ)) :=
    actual_hazard_primitive_laws hα hαβ hV hH hη hβη
  rcases hp with ⟨hΛ, hΛmeas, hInt, hbasic, hcaps⟩'''
assert s.count(old) == 1
s = s.replace(old, new)
old = '''        exfalso
        simpa using h'''
assert s.count(old) == 1
s = s.replace(old, '''        exact False.elim (WithTop.not_top_le_coe t h)''')
assert s.count('intermediate_value_Icc (zero_le q)') == 1
s = s.replace('intermediate_value_Icc (zero_le q)',
              'intermediate_value_Icc (show (0 : ℝ≥0) ≤ q from bot_le)')
old = '      hτmeas.comp (measurable_const.prodMk (measurable_const.prodMk measurable_real_toNNReal))'
new = '''      hτmeas.comp
        (show Measurable (fun e : ℝ => ((y, xRef), z, Real.toNNReal e)) from
          measurable_const.prodMk (measurable_const.prodMk measurable_real_toNNReal))'''
assert s.count(old) == 1
s = s.replace(old, new)
p.write_text(s, encoding='utf8', newline='\n')
(out / 'diagnosis.json').write_text(json.dumps(dict(
    actual_root_PID=os.getpid(), failure_class='API_BLOCKED',
    failures=['Explicit WithTop top inequality API needed',
              'zero_le is an implicit fact, not a function',
              'Expanded private-helper lets prevent simp matching named cumulative hazard',
              'Unconstrained tuple constants trigger costly definitional matching in map measurability'],
    repair='Give the primitive result its exact folded local type before destructuring; use explicit top inequality and NNReal nonnegativity APIs; constrain the complete measurable input map.',
    same_sealed_statement=True, no_added_hypotheses=True,
    unchanged_local_heartbeat_budget=1200000,
    full_theorem_compiled=False, independently_reviewed=False,
    Goal_complete=False), ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
