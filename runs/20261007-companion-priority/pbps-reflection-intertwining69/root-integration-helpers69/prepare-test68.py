from pathlib import Path
import json, hashlib

pre = Path('runs/20261007-companion-priority/pbps-sharp-energy-preproof68')
r = Path('runs/20261007-companion-priority/pbps-sharp-energy68')
old = Path('Tests/ProximalBPSActualRootCommutation.lean').read_text(encoding='utf-8')
name = 'genuine_actual_modified_energy_equivalence'
decl = old[old.index('theorem genuine_actual_corrector_coefficient_consumer'):old.index('\nend\nend Tests.')]
decl = decl.replace('genuine_actual_corrector_coefficient_consumer', name)
decl = decl.replace('ActualRootCommutation.actual_same_root_inverse_commutation', 'SharpCorrectorEnergy.actual_sharp_corrector_bound')
decl = decl.replace('hSquare0,hCommInv,B0,hB0', 'hSquare0,hCommInv,hKself,hCoefficient,hPair,B0,hB0')
start = decl.index('  change (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →')
end = decl.index('  refine ⟨hμ, ?_⟩')
decl = decl[:start]+'''  let γ : ℝ := 2*Real.sqrt ((α : ℝ)*η)/(1+(α : ℝ)*η)
  change 0 < γ at hγ
  let C : HP0 → HP0 → ℝ := fun u v =>
    (1/2 : ℝ)*(‖u‖^2-‖v‖^2)-inner ℝ ((A0*Inv) u) v
  change (∀ u v : HP0, |C u v| ≤ (‖u‖^2+‖v‖^2)/(2*γ)) at hPair
  change (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
    ∃ fP : HP0,
      HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
      let fperp : Hperp := R f
      let fV : HP0 := V0.adjoint fperp
      B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
      HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
      ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖ ∧
      ‖fP‖^2+‖fV‖^2≤‖f‖^2 ∧ |C fP fV|≤‖f‖^2/(2*γ)) at hGlobal
'''+decl[end:]
decl = decl.replace('hCommInv,hKself,hCoefficient,?_⟩', 'hCommInv,hKself,hCoefficient,hPair,?_⟩')
assert decl.count('  exact hGlobal') == 1
decl = decl.replace('  exact hGlobal', '''  intro f hf
  obtain ⟨fP,hfP,hBf,hΓf,hPyth,hNormV,hBudget,hCorrector⟩ := hGlobal f hf
  let fperp : Hperp := R f
  let fV : HP0 := V0.adjoint fperp
  refine ⟨fP,hfP,hBf,hΓf,hPyth,hNormV,hBudget,hCorrector,?_⟩
  intro omegaWeight hWeight hWeightGamma
  let L : ℝ := ‖f‖^2+omegaWeight*C fP fV
  have hPerturbation : |L-‖f‖^2| ≤ (omegaWeight/(2*γ))*‖f‖^2 := by
    have hId : L-‖f‖^2=omegaWeight*C fP fV := by dsimp only [L]; ring
    rw [hId,abs_mul,abs_of_pos hWeight]
    calc
      omegaWeight*|C fP fV| ≤ omegaWeight*(‖f‖^2/(2*γ)) :=
        mul_le_mul_of_nonneg_left hCorrector hWeight.le
      _ = (omegaWeight/(2*γ))*‖f‖^2 := by ring
  have hWeightBound : omegaWeight/(2*γ) ≤ (1/2 : ℝ) := by
    apply (div_le_iff₀ (by positivity : 0 < 2*γ)).2
    nlinarith only [hWeightGamma]
  have hHalf : (omegaWeight/(2*γ))*‖f‖^2 ≤ (1/2 : ℝ)*‖f‖^2 :=
    mul_le_mul_of_nonneg_right hWeightBound (sq_nonneg _)
  have hBoth := abs_le.mp (hPerturbation.trans hHalf)
  refine ⟨?_,?_,hPerturbation,hHalf⟩ <;> linarith only [hBoth.1,hBoth.2]''')
dest = Path('Tests/ProximalBPSSharpCorrectorEnergy.lean')
assert not dest.exists()
prefix = '''import AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy

/-!
# An original-input consumer of the actual sharp PBPS corrector bound

Lemma B.3, arXiv:2609.06905v1: the same actual globally centered f has
modified energy between one half and three halves of its squared L2 norm.
All constants, witnesses and original callers are retained in the literal Prop.
-/
namespace Tests.ProximalBPSSharpCorrectorEnergy
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

'''
body = prefix+(pre/'statement2.definition.lean').read_text(encoding='utf-8')+'\n\n'+decl+'''

end
end Tests.ProximalBPSSharpCorrectorEnergy

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity
#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound
#print axioms Tests.ProximalBPSSharpCorrectorEnergy.genuine_actual_modified_energy_equivalence
'''
dest.write_text(body, encoding='utf-8', newline='\n')
(r/'test-preparation68.json').write_text(json.dumps(dict(status='PROOF_CANDIDATE_NOT_COMPILED',
    exact_literal_Prop=(pre/'statement2.definition.lean').as_posix(),
    calls_actual_production=True, original_inputs_retained=True,
    raw_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Wrote exact sealed full literal Test statement and actual modified-energy proof candidate.')
