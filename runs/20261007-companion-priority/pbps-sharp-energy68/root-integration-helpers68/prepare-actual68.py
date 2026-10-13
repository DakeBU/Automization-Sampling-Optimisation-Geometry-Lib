from pathlib import Path
import json, hashlib

pre = Path('runs/20261007-companion-priority/pbps-sharp-energy-preproof68')
r = Path('runs/20261007-companion-priority/pbps-sharp-energy68')
old = Path('Tests/ProximalBPSActualRootCommutation.lean').read_text(encoding='utf-8')
name = 'actual_sharp_corrector_bound'
decl = old[old.index('theorem genuine_actual_corrector_coefficient_consumer'):old.index('\nend\nend Tests.')]
decl = decl.replace('genuine_actual_corrector_coefficient_consumer', name)
insertion = '''  let γ : ℝ := 2*Real.sqrt ((α : ℝ)*η)/(1+(α : ℝ)*η)
  change 0 < γ at hγ
  change ‖Inv‖ ≤ 1/γ at hNormInv
  let C : HP0 → HP0 → ℝ := fun u v =>
    (1/2 : ℝ)*(‖u‖^2-‖v‖^2)-inner ℝ ((A0*Inv) u) v
  have hPair (u v : HP0) : |C u v| ≤ (‖u‖^2+‖v‖^2)/(2*γ) := by
    have h := AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity
      (A0*Inv) Inv hKself hInvSelf hCoefficient (1/γ) (by positivity) hNormInv u v
    change |C u v| ≤ ((1/γ)/2)*(‖u‖^2+‖v‖^2) at h
    calc
      |C u v| ≤ ((1/γ)/2)*(‖u‖^2+‖v‖^2) := h
      _ = (‖u‖^2+‖v‖^2)/(2*γ) := by field_simp; ring
'''
assert decl.count('  refine ⟨hμ, ?_⟩') == 1
decl = decl.replace('  refine ⟨hμ, ?_⟩', insertion+'  refine ⟨hμ, ?_⟩')
decl = decl.replace('hCommInv,hKself,hCoefficient,?_⟩', 'hCommInv,hKself,hCoefficient,hPair,?_⟩')
assert decl.count('  exact hGlobal') == 1
decl = decl.replace('  exact hGlobal', '''  intro f hf
  obtain ⟨fP,hfP,hBf,hΓf,hPyth,hNormV⟩ := hGlobal f hf
  let fperp : Hperp := R f
  let fV : HP0 := V0.adjoint fperp
  have hBudget : ‖fP‖^2+‖fV‖^2 ≤ ‖f‖^2 := by
    have hs := (sq_le_sq₀ (norm_nonneg fV) (norm_nonneg fperp)).2 hNormV
    nlinarith only [hPyth, hs]
  refine ⟨fP,hfP,hBf,hΓf,hPyth,hNormV,hBudget,?_⟩
  exact (hPair fP fV).trans (div_le_div_of_nonneg_right hBudget (by positivity))''')
dest = Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean')
assert not dest.exists()
prefix = '''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation
import AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound

/-!
# The actual PBPS sharp first-corrector estimate

Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix B.3, (B.20)--(B.24).
The private literal statement expands every original input and every witness;
it introduces no mathematical provider. Production uses production parents.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

'''
body = prefix+(pre/'statement1.definition.lean').read_text(encoding='utf-8')+'\n\n'+decl+'''

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound
'''
dest.write_text(body, encoding='utf-8', newline='\n')
(r/'actual-preparation68.json').write_text(json.dumps(dict(status='PROOF_CANDIDATE_NOT_COMPILED',
    exact_literal_Prop=(pre/'statement1.definition.lean').as_posix(),
    prior_Test_used_as_internal_coefficient_proof_not_imported=True,
    production_imports_Tests=False, raw_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Wrote exact sealed full literal actual statement and substantive sharp-bound proof candidate.')
