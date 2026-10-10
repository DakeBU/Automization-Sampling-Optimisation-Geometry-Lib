from pathlib import Path
import hashlib,json
R=Path('E:/Samplinglib');D=Path(__file__).parent
h=(D/'header86.proposed.lean').read_text(encoding='utf-8');seal=json.loads((D/'root.statement-seal86.json').read_bytes())
assert hashlib.sha256(h.encode()).hexdigest()==seal['header']['raw_sha256']
p=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean';assert not p.exists()
helper='''
-- Internal FTC ingredient of the sealed finite-density anchor; not the public result.
private theorem first_density_setIntegral
    (l : ℝ → ℝ) (hl : Continuous l) (t : ℝ) (ht : 0 ≤ t) :
    (∫ s in Set.Ioc 0 t, l s * Real.exp (-(∫ u in (0 : ℝ)..s, l u))) =
      1 - Real.exp (-(∫ u in (0 : ℝ)..t, l u)) := by
  let L : ℝ → ℝ := fun s => ∫ u in (0 : ℝ)..s, l u
  have hL (s : ℝ) : HasDerivAt L (l s) s :=
    intervalIntegral.integral_hasDerivAt_right (hl.intervalIntegrable _ _)
      hl.stronglyMeasurable.stronglyMeasurableAtFilter hl.continuousAt
  have hcL : Continuous L := fun s => (hL s).continuousAt
  have hd (s : ℝ) :
      HasDerivAt (fun s => 1 - Real.exp (-L s))
        (l s * Real.exp (-L s)) s := by
    convert (HasDerivAt.const_sub 1 (hL s).neg.exp) using 1 <;> ring
  have hdC : Continuous (fun s => l s * Real.exp (-L s)) :=
    hl.mul hcL.neg.exp
  have hf := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le ht
    ((continuous_const.sub hcL.neg.exp).continuousOn)
    (fun s _ => hd s) (hdC.intervalIntegrable _ _)
  rw [intervalIntegral.integral_of_le ht] at hf
  simpa [L] using hf
'''
end='\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw\n'
assert h.endswith(end)
p.write_text(h[:-len(end)]+helper+end,encoding='utf-8',newline='\n')
print('Created source-sealed statement and internal FTC provider only; public anchor BODY pending')
