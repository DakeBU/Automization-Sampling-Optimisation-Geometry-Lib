from pathlib import Path
import hashlib,json
base=Path('runs/20261007-companion-priority');pre=base/'pbps-bounce-rate-preproof74';r=base/'pbps-actual-bounce-rate74'
assert json.loads((r/'preproof-admission.json').read_bytes())['status']=='CLAIMED_EXPLORING_NOT_PROVED'
assert json.loads((r/'publication-packet-before-proof.receipt.json').read_bytes())['exit_code']==0
assert json.loads((r/'frontier-before-proof.receipt.json').read_bytes())['exit_code']==0
header=(pre/'header74.proposed.lean').read_bytes();assert hashlib.sha256(header).hexdigest()=='d72435795cd225af382948e8da683b6eb4b9e5b05509f8e3b0d10a3ed5a5a96e'
text=header.decode();literal=text[text.index('    Measurable (fun a'):text.index('\ntheorem actual_bounce_rate_energy_laws')].rstrip()
proof='''
  let c : E → E → E := fun y xRef => y - η • gradient V xRef
  let h : E → E → E := fun xRef x => gradient V x - gradient V xRef
  let R : E → E → E := fun n p => p - (2 * inner ℝ p n / ‖n‖ ^ 2) • n
  let S : E → (E × E) → (E × E) := fun xRef z => (z.1, R (h xRef z.1) z.2)
  let rate : E → (E × E) → ℝ := fun xRef z =>
    Real.sqrt η * max 0 (inner ℝ z.2 (h xRef z.1))
  let H : E → E → (E × E) → ℝ := fun y xRef z =>
    (η⁻¹ * ‖z.1 - c y xRef‖ ^ 2 + ‖z.2‖ ^ 2) / 2
  change
'''+literal+'''
  letI : CompleteSpace E := FiniteDimensional.complete ℝ E
  have hLip : LipschitzWith β (gradient V) := by
    simpa using
      (AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
        (m := α) (L := β) (r := 0) hV hH (0 : E)).2
  have hgrad : Continuous (gradient V) := hLip.continuous
  have hRzero (p : E) : R 0 p = p := by simp [R]
  have hRreflect (n p : E) : R n p = (ℝ ∙ n)ᗮ.reflection p := by
    rw [Submodule.reflection_orthogonal_apply, Submodule.reflection_singleton_apply]
    simp only [real_inner_comm n p, two_smul, add_smul, neg_sub]
    dsimp [R]
    simp only [div_eq_mul_inv, mul_smul, add_smul]
    module
  have hRlaws (n p : E) : R n (R n p) = p ∧ ‖R n p‖ = ‖p‖ ∧
      inner ℝ (R n p) n = -inner ℝ p n := by
    refine ⟨?_, ?_, ?_⟩
    · simp only [hRreflect, Submodule.reflection_reflection]
    · rw [hRreflect]; exact LinearIsometryEquiv.norm_map _ _
    · by_cases hn : n = 0
      · simp [hn]
      · have hn2 : ‖n‖ ^ 2 ≠ 0 := pow_ne_zero _ (norm_ne_zero_iff.mpr hn)
        dsimp [R]
        rw [inner_sub_left, real_inner_smul_left, real_inner_self_eq_norm_sq]
        field_simp [hn2] <;> ring
  have hSmeas : Measurable (fun a : E × (E × E) => S a.1 a.2) := by
    dsimp [S, R, h]
    fun_prop
  have hratecont : Continuous (fun a : E × (E × E) => rate a.1 a.2) := by
    dsimp [rate, h]
    fun_prop
  have hSlaws (xRef : E) (z : E × E) :
      (S xRef z).1 = z.1 ∧ S xRef (S xRef z) = z := by
    refine ⟨rfl, ?_⟩
    exact Prod.ext rfl (hRlaws (h xRef z.1) z.2).1
  have hHbounce (y xRef : E) (z : E × E) : H y xRef (S xRef z) = H y xRef z := by
    dsimp [H, S]
    rw [(hRlaws (h xRef z.1) z.2).2.1]
  have hrateflip (xRef : E) (z : E × E) :
      rate xRef (S xRef z) = Real.sqrt η * max 0 (-inner ℝ z.2 (h xRef z.1)) := by
    dsimp [rate, S]
    rw [(hRlaws (h xRef z.1) z.2).2.2]
  have hratelaws (xRef : E) (z : E × E) : 0 ≤ rate xRef z ∧
      rate xRef (S xRef z) = Real.sqrt η * max 0 (-inner ℝ z.2 (h xRef z.1)) ∧
      rate xRef z - rate xRef (S xRef z) = Real.sqrt η * inner ℝ z.2 (h xRef z.1) := by
    refine ⟨mul_nonneg (Real.sqrt_nonneg _) (le_max_left _ _), hrateflip xRef z, ?_⟩
    rw [hrateflip]
    dsimp [rate]
    by_cases hi : 0 ≤ inner ℝ z.2 (h xRef z.1)
    · rw [max_eq_right hi, max_eq_left (by linarith)]
      ring
    · rw [max_eq_left (le_of_not_ge hi), max_eq_right (by linarith)]
      ring
  have hzero (xRef x p : E) (hh : h xRef x = 0) :
      S xRef (x,p) = (x,p) ∧ rate xRef (x,p) = 0 := by
    simp [S, rate, hh, hRzero]
  have hHnonneg (y xRef : E) (z : E × E) : 0 ≤ H y xRef z := by
    exact div_nonneg (add_nonneg (mul_nonneg (inv_nonneg.mpr hη.le) (sq_nonneg _))
      (sq_nonneg _)) (by norm_num)
  refine ⟨hSmeas, hratecont, hratecont.measurable, hRzero, hRlaws,
    hSlaws, hHbounce, hratelaws, hzero, ?_⟩
  intro y xRef z₀
  refine ⟨hHnonneg y xRef z₀, ?_⟩
  intro z heq
  have hsum : η⁻¹ * ‖z.1 - c y xRef‖ ^ 2 + ‖z.2‖ ^ 2 = 2 * H y xRef z₀ := by
    change (η⁻¹ * ‖z.1 - c y xRef‖ ^ 2 + ‖z.2‖ ^ 2) / 2 = _ at heq
    linarith
  have hp2 : ‖z.2‖ ^ 2 ≤ 2 * H y xRef z₀ := by
    have := mul_nonneg (inv_nonneg.mpr hη.le) (sq_nonneg ‖z.1 - c y xRef‖)
    linarith
  have hxweighted : η⁻¹ * ‖z.1 - c y xRef‖ ^ 2 ≤ 2 * H y xRef z₀ := by
    nlinarith [sq_nonneg ‖z.2‖]
  have hx2 : ‖z.1 - c y xRef‖ ^ 2 ≤ 2 * η * H y xRef z₀ := by
    calc
      ‖z.1 - c y xRef‖ ^ 2 = η * (η⁻¹ * ‖z.1 - c y xRef‖ ^ 2) := by
        rw [← mul_assoc, mul_inv_cancel₀ (ne_of_gt hη), one_mul]
      _ ≤ η * (2 * H y xRef z₀) := mul_le_mul_of_nonneg_left hxweighted hη.le
      _ = _ := by ring
  have hp : ‖z.2‖ ≤ Real.sqrt (2 * H y xRef z₀) := Real.le_sqrt_of_sq_le hp2
  have hx : ‖z.1 - c y xRef‖ ≤ Real.sqrt (2 * η * H y xRef z₀) :=
    Real.le_sqrt_of_sq_le hx2
  refine ⟨hp, hx, ?_⟩
  have htriangle : ‖z.1 - xRef‖ ≤ ‖z.1 - c y xRef‖ + ‖c y xRef - xRef‖ := by
    calc
      ‖z.1 - xRef‖ = ‖(z.1 - c y xRef) + (c y xRef - xRef)‖ := by
        congr 1
        abel
      _ ≤ _ := norm_add_le _ _
  have hnormal : ‖h xRef z.1‖ ≤ (β : ℝ) *
      (Real.sqrt (2 * η * H y xRef z₀) + ‖c y xRef - xRef‖) := by
    calc
      ‖h xRef z.1‖ ≤ (β : ℝ) * ‖z.1 - xRef‖ := hLip.norm_sub_le z.1 xRef
      _ ≤ _ := mul_le_mul_of_nonneg_left (htriangle.trans (add_le_add_right hx _)) β.coe_nonneg
  have hpair : max 0 (inner ℝ z.2 (h xRef z.1)) ≤ ‖z.2‖ * ‖h xRef z.1‖ :=
    max_le (mul_nonneg (norm_nonneg _) (norm_nonneg _)) (real_inner_le_norm _ _)
  calc
    rate xRef z ≤ Real.sqrt η * (‖z.2‖ * ‖h xRef z.1‖) :=
      mul_le_mul_of_nonneg_left hpair (Real.sqrt_nonneg _)
    _ ≤ Real.sqrt η * (Real.sqrt (2 * H y xRef z₀) *
        ((β : ℝ) * (Real.sqrt (2 * η * H y xRef z₀) + ‖c y xRef - xRef‖))) :=
      mul_le_mul_of_nonneg_left
        (mul_le_mul hp hnormal (norm_nonneg _) (Real.sqrt_nonneg _)) (Real.sqrt_nonneg _)
    _ = _ := by ring

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate
'''
dest=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean');assert not dest.exists();dest.write_text(text+proof,encoding='utf8',newline='\n')
print('Implementation74 written under exact sealed header; focused Lean and independent reviews still required.')
