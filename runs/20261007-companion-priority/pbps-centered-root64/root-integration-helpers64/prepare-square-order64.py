from pathlib import Path
root=Path.cwd();pre=root/'runs/20261007-companion-priority/pbps-centered-root-preproof64';r=root/'runs/20261007-companion-priority/pbps-centered-root64'
gate=(root/'.astis/pbps-centered-root64/type-gate64.py').read_text(encoding='utf-8-sig')
gate=gate.replace("root/'runs/20261007-companion-priority/pbps-centered-root-preproof64'/label", "root/'runs/20261007-companion-priority/pbps-centered-root64'/label")
gate=gate.replace("inputs=[pin(root/p) for p in math if (root/p).is_file()]", "math += [p for p in command if p.endswith('.lean') and (root/p).is_file()];math += ['runs/20261007-companion-priority/pbps-centered-root-preproof64/root.statement-seal64.json'];inputs=[pin(root/p) for p in dict.fromkeys(math) if (root/p).is_file()]")
(root/'.astis/pbps-centered-root64/proof-gate64.py').write_text(gate,encoding='utf-8',newline='\n')
base=(root/'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRootUnique.lean').read_text(encoding='utf-8')
imports=base[:base.index('theorem positive_square_roots_unique')].replace('L2RealSquareRootUnique','L2RealSquareOrder').replace('Rpow.Basic','Rpow.Order')
header=(pre/'header0.lean').read_text(encoding='utf-8')
body=''' := by
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
  obtain ⟨_,_,Dc,hDc,hDf,hDi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ (B*B-A*A) hSquareOrder
  have hComplexDiff : Bc*Bc-Ac*Ac=Dc := by
    apply ContinuousLinearMap.ext
    intro g
    change Bc (Bc g) - Ac (Ac g)=Dc g
    rw [hBf g,hAf g,map_add,map_smul,map_add,map_smul,hBi,hBi,hAi,hAi,hDf g]
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.mul_apply,map_sub]
    abel
  have hAcNonneg : 0 ≤ Ac := (ContinuousLinearMap.nonneg_iff_isPositive Ac).mpr hAc
  have hBcNonneg : 0 ≤ Bc := (ContinuousLinearMap.nonneg_iff_isPositive Bc).mpr hBc
  have hSqLe : Ac*Ac ≤ Bc*Bc := by
    apply (ContinuousLinearMap.le_def _ _).mpr
    rw [hComplexDiff]
    exact hDc
  have hLe : Ac ≤ Bc := by
    have h := CFC.sqrt_le_sqrt (Ac*Ac) (Bc*Bc) hSqLe
    simpa only [CFC.sqrt_mul_self hAcNonneg,CFC.sqrt_mul_self hBcNonneg] using h
  have hDiff : (Bc-Ac).IsPositive := (ContinuousLinearMap.le_def _ _).mp hLe
  let e : Lp ℝ 2 μ →ₗᵢ[ℝ] Lp ℂ 2 μ :=
    { toLinearMap := ι.toLinearMap, norm_map' := hNorm }
  have hInner (v w : Lp ℝ 2 μ) : (inner ℂ (ι v) (ι w)).re=inner ℝ v w := by
    rw [← real_inner_eq_re_inner]
    exact e.inner_map_map v w
  refine ⟨hB.isSymmetric.sub hA.isSymmetric,?_⟩
  intro u
  have h := hDiff.re_inner_nonneg_left (ι u)
  have hAction : (Bc-Ac) (ι u)=ι ((B-A) u) := by
    simp only [ContinuousLinearMap.sub_apply,hBi,hAi,map_sub]
  rw [hAction,hInner] at h
  exact h

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order
'''
p=r/'square-order-draft-v1.lean';assert not p.exists();p.write_text(imports+header.rstrip()+body,encoding='utf-8',newline='\n')
print('Prepared exact sealed-header64 square-order proof draft v1; source-first adoption and Statement Seal retained; no production file changed.')
