"""Initialize the sealed full theorem implementation; no placeholder closures."""
from pathlib import Path
r=Path(__file__).parent;pre=r.parent/'pbps-bounded-path-expansion-preread95'
h=(pre/'Header95.lean').read_text(encoding='utf8')
signature=h.split('noncomputable def candidate_statement',1)[1].split('#check',1)[0].rstrip()
binders=signature.split(' : Prop := by',1)[0]
defs=signature.split('  exact\n',1)[1].split('    ∃ Z',1)[0]
conclusion='    ∃ Z'+signature.split('    ∃ Z',1)[1]
old=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean').read_text(encoding='utf8')
old=old.split('theorem actual_finite_count_path_law',1)[1]
bodydefs='  let c'+old.split('  let c',1)[1].split('  change',1)[0]
wgt='    let wgt'+defs.split('    let wgt',1)[1]
wgt='\n'.join(x[2:] for x in wgt.splitlines())+'\n'
bridges=(r/'bridge95.lean').read_text(encoding='utf8').split('private theorem signed_sector',1)[1]
proof='''
  obtain ⟨Z, hZM, hZarc, hZfallback, hZzero, hAll⟩ :=
    ActualFiniteCountPath.actual_finite_count_path_law hα hαβ hV hH hη hβη
  refine ⟨Z, hZM, hZarc, hZfallback, hZzero, ?_⟩
  intro y xRef z₀ T
  let ZT : (ℕ → ℝ) → Path T := fun u s => Z y xRef z₀ s.val u
  intro F hF M hM hbound
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  have hbase := (hAll 0 T).2.2.2 y xRef z₀
  have hZT : Measurable ZT := hbase.2.1
  have hN : Measurable (N y xRef z₀ T) := hbase.2.2.1
  have hi : Integrable (fun u => F (ZT u)) P :=
    ⟨(hF.comp hZT).aestronglyMeasurable,
      HasFiniteIntegral.of_bounded (Filter.Eventually.of_forall
        (fun u => by simpa only [Real.norm_eq_abs] using hbound (ZT u)))⟩
  have hsector (n : ℕ) :
      Integrable (fun t : Prefix n T => F (Γ y xRef z₀ n T t) *
        wgt y xRef z₀ n T t) (m n T) ∧
      (∫ u in {u | N y xRef z₀ T u = n}, F (ZT u) ∂P) =
        ∫ t : Prefix n T, F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t ∂m n T := by
    have hn := hAll n T
    obtain ⟨hHM, hZTM, hNM, hCM, hinterp, hident, hAE, hdisj, hcover,
      hlaw, htests, hmass, hmassbound⟩ := hn.2.2.2 y xRef z₀
    have hΓ : Measurable (Γ y xRef z₀ n T) := hn.2.1.comp
      (f := fun t : Prefix n T => (((y,xRef),z₀),t))
      (measurable_const.prodMk measurable_id)
    have hρ : Measurable (ρ y xRef z₀ n T) := hn.2.2.1.comp
      (f := fun t : Prefix n T => (((y,xRef),z₀),t))
      (measurable_const.prodMk measurable_id)
    have hK : Measurable (K y xRef z₀ n T) :=
      (ActualOrderedPrefix.actual_ordered_prefix_law hα hαβ hV hH hη hβη n T).2.2.1.comp
        (f := fun t : Prefix n T => (((y,xRef),z₀),t))
        (measurable_const.prodMk measurable_id)
    have hw (t : Prefix n T) : 0 ≤ wgt y xRef z₀ n T t := by
      apply mul_nonneg (Real.exp_nonneg _)
      exact Finset.prod_nonneg (fun i _ => mul_nonneg (Real.sqrt_nonneg _) (le_max_left _ _))
    have heq (t : Prefix n T) :
        ρ y xRef z₀ n T t = ENNReal.ofReal (wgt y xRef z₀ n T t) := by
      have hd := (ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite
        hα hαβ hV hH hη hβη y xRef z₀ n T t).2.2.2
      simpa only [Fin.snoc_castSucc] using hd
    exact signed_sector hHM hZTM hK hΓ hρ hw heq hlaw hF hi.integrableOn
  have hsum := signed_count_partition hN hi
  have heq (n : ℕ) := (hsector n).2
  refine ⟨hi, fun n => (hsector n).1, ?_, ?_⟩
  · simpa only [heq] using hsum.1
  · simpa only [heq] using hsum.2
'''
text='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity
import Mathlib.MeasureTheory.Integral.Bochner.Set

/-! Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1 (A.7).
Bounded real path functionals on the coordinate-product measurable path space.
The mass-partition proof is an explicit ASTIS completion of countable signed assembly. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion
open InnerProductSpace MeasureTheory ProbabilityTheory Set Filter
open scoped NNReal ENNReal Topology Interval BigOperators Classical
set_option autoImplicit false

private theorem signed_sector'''+bridges+'\nprivate noncomputable def actual_bounded_path_statement'+signature+'\n\n/-- Full bounded signed path expansion for the actual stopped-clock process. -/\ntheorem actual_bounded_path_functional_expansion'+binders+' :\n    actual_bounded_path_statement hα hαβ hV hH hη hβη := by\n  classical\n'+bodydefs+wgt+'  change\n'+conclusion+'\n'+proof+'\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion\n'
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedPathExpansion.lean');assert not p.exists()
p.write_text(text,encoding='utf8',newline='\n')
print('Wrote full sealed target and implementation attempt; no proof acceptance claimed')
