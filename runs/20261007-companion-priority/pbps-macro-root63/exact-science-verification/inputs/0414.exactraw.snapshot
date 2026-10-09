from pathlib import Path
import json
pre=Path('runs/20261007-companion-priority/pbps-real-root-unique-preproof62');r=Path('runs/20261007-companion-priority/pbps-real-root-unique62');cfg=json.loads((r/'claim.json').read_bytes());seal=json.loads((pre/'root.statement-seal62.json').read_bytes())
assert seal['status']=='STATEMENT62_SEALED_NOT_PROVED_NOT_CLAIMED'
files=cfg['proposed_files'];assert all(not Path(p).exists() for p in files)
generic='''import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

open MeasureTheory
open scoped ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

'''+(pre/'header0.lean').read_text(encoding='utf-8').rstrip()+''' := by
  letI := IsStarNormal.instNonUnitalContinuousFunctionalCalculus
    (A := Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  letI : NonUnitalContinuousFunctionalCalculus ℂ
      (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) IsStarNormal :=
    NonUnitalClosedEmbeddingContinuousFunctionalCalculus.toNonUnitalContinuousFunctionalCalculus
  letI : NonUnitalContinuousFunctionalCalculus ℝ
      (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) IsSelfAdjoint :=
    IsSelfAdjoint.instNonUnitalContinuousFunctionalCalculus
      (A := Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  let ι : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
  let R : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
  let Q : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.imCLM.compLpL 2 μ
  obtain ⟨hNorm,_,Ac,hAc,hAf,hAi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ A hA
  obtain ⟨_,_,Bc,hBc,hBf,hBi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ B hB
  have hReal (u : Lp ℝ 2 μ) : A (A u) = B (B u) :=
    congrArg (fun D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ => D u) hSq
  have hComplexSquare : Ac*Ac = Bc*Bc := by
    apply ContinuousLinearMap.ext
    intro g
    change Ac (Ac g) = Bc (Bc g)
    calc
      Ac (Ac g) = ι (A (A (R g))) + Complex.I • ι (A (A (Q g))) := by
        rw [hAf g, map_add, map_smul, hAi, hAi]
      _ = ι (B (B (R g))) + Complex.I • ι (B (B (Q g))) := by
        rw [hReal (R g),hReal (Q g)]
      _ = Bc (Bc g) := by rw [hBf g, map_add, map_smul, hBi, hBi]
  have hAcNonneg : 0 ≤ Ac := (ContinuousLinearMap.nonneg_iff_isPositive Ac).mpr hAc
  have hBcNonneg : 0 ≤ Bc := (ContinuousLinearMap.nonneg_iff_isPositive Bc).mpr hBc
  have hSame : Ac = Bc :=
    (CFC.sqrt_unique hComplexSquare hAcNonneg).symm.trans (CFC.sqrt_unique rfl hBcNonneg)
  let e : Lp ℝ 2 μ →ₗᵢ[ℝ] Lp ℂ 2 μ :=
    { toLinearMap := ι.toLinearMap
      norm_map' := hNorm }
  apply ContinuousLinearMap.ext
  intro u
  apply e.injective
  change ι (A u) = ι (B u)
  rw [← hAi u, ← hBi u, hSame]

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.positive_square_roots_unique
'''
actual='''import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot
import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

'''+(pre/'header1.lean').read_text(encoding='utf-8').rstrip()+''' := by
  dsimp only
  obtain ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,T,hTs,hAll,hD,Γ,hΓ,hΓSq,hEnergy⟩ :=
    RealDefectRoot.actual_positive_real_defect_root hα hαβ hV hH hη hβη
  refine ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,T,hTs,hAll,hD,Γ,hΓ,hΓSq,hEnergy,?_⟩
  intro Γ' hΓ' hΓ'Sq
  exact AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.positive_square_roots_unique
    _ Γ' Γ hΓ' hΓ (hΓ'Sq.trans hΓSq.symm)

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique.actual_unique_positive_real_defect_root
'''
test=Path('Tests/ProximalBPSRealDefectRoot.lean').read_text(encoding='utf-8')
test=test.replace('ProximalBPS.RealDefectRoot','ProximalBPS.RealDefectRootUnique').replace('actual_positive_real_defect_root','actual_unique_positive_real_defect_root').replace('L2RealSquareRoot.exists_positive_real_square_root','L2RealSquareRootUnique.positive_square_roots_unique')
test=test.replace('is a contraction, even on the full scalar space.','is unique; every positive alternative with the same square has the same full scalar energy and is a contraction.')
test=test.replace('∀ u : Lp ℝ 2 ν, ‖Γ u‖ ≤ ‖u‖ ∧ ‖Γ u‖^2 = ‖u‖^2-‖T u‖^2 := by','∀ Γ\' : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,\n          Γ\'.IsPositive → Γ\'*Γ\' = ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) →\n          Γ\'=Γ ∧ ∀ u : Lp ℝ 2 ν, ‖Γ\' u‖ ≤ ‖u‖ ∧ ‖Γ\' u‖^2 = ‖u‖^2-‖T u‖^2 := by')
test=test.replace('hΓSq,hEnergy⟩ :=','hΓSq,hEnergy,hUnique⟩ :=').replace('  intro u\n  refine','  intro Γ\' hΓ\' hΓ\'Sq\n  have heq := hUnique Γ\' hΓ\' hΓ\'Sq\n  refine ⟨heq,?_⟩\n  rw [heq]\n  intro u\n  refine')
for p,s in zip(files,[generic,actual,test]):Path(p).write_text(s,encoding='utf-8',newline='\n')
print('Authored62 only3 owned new files; exact sealed two headers retained, no shared imports/Registry changes.')
