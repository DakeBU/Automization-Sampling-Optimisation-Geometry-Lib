from pathlib import Path
import hashlib,json
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64'
seal=json.loads((r/'test.statement-seal64.json').read_bytes());h=r/'test.header64.lean'
assert hashlib.sha256(h.read_bytes()).hexdigest()==seal['header_raw_sha256']
src=(root/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean').read_text(encoding='utf-8')
prefix=src.split(':= by',1)[1].split('  have hBase :=',1)[0]
body=prefix+'''  have hBase := AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse.actual_centered_root_order_inverse
    (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hBase
  rcases hBase with
    ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,
      T,hTs,hAll,hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,
      q,hqa,hTq,hq,hCenter,hΓPq,hγ,ΓP0,hΓP0,hPos0,hOrder0,hUnit,
      Inv,hLeft,hRight,hNormInv⟩
  let A : HP →L[ℝ] HP := HP.orthogonalProjectionOnto ∘L U.toContinuousLinearMap ∘L HP.subtypeL
  let B : HP →L[ℝ] Lp ℝ 2 J :=
    (((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P)*U.toContinuousLinearMap*P) ∘L HP.subtypeL
  let ΓP : HP →L[ℝ] HP := e.conjStarAlgEquiv Γ
  let qP : HP := e q
  let HP0 := (innerSL ℝ qP).ker
  letI : NormedAddCommGroup HP0 := HP0.normedAddCommGroup
  letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace
  have hGramLocal : B.adjoint ∘L B=ΓP*ΓP := hGram
  have hPosLocal : ΓP.IsPositive := hΓP
  refine ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,hAll,
    hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,q,hqa,hTq,hq,hCenter,hΓPq,hγ,
    ΓP0,hΓP0,hPos0,hOrder0,hUnit,Inv,hLeft,hRight,hNormInv,?_⟩
  intro f
  let g : HP0 := Inv f
  have hg : ΓP0 g=f := congrArg (fun C : HP0 →L[ℝ] HP0 => C f) hRight
  have hb := B.apply_norm_sq_eq_inner_adjoint_right (g : HP)
  have hr := ΓP.apply_norm_sq_eq_inner_adjoint_right (g : HP)
  rw [hGramLocal] at hb
  rw [hPosLocal.isSelfAdjoint.adjoint_eq] at hr
  have hNorm : ‖B (g : HP)‖=‖ΓP (g : HP)‖ :=
    (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp (hb.trans hr.symm)
  refine ⟨?_,hPB (g : HP)⟩
  calc
    ‖B (HP0.subtypeL (Inv f))‖=‖ΓP (g : HP)‖ := hNorm
    _ = ‖ΓP0 g‖ := congrArg (fun z : HP => ‖z‖) (hΓP0 g).symm
    _ = ‖f‖ := congrArg (fun z : HP0 => ‖z‖) hg
'''
text='''import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology
namespace Tests.ProximalBPSCenteredRootOrderInverse
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

-- Original-input consumer: normalized actual leakage preserves the norm and lies in ker P.
-- This tests the same bounded inverse without assuming a gap, root or polar isometry.
'''+h.read_text(encoding='utf-8').rstrip()+' := by'+body+'''
end
end Tests.ProximalBPSCenteredRootOrderInverse

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order
#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse.actual_centered_root_order_inverse
#print axioms Tests.ProximalBPSCenteredRootOrderInverse.genuine_actual_centered_inverse_consumer
'''
p=root/'Tests/ProximalBPSCenteredRootOrderInverse.lean';assert not p.exists();p.write_text(text,encoding='utf-8',newline='\n')
print('Test64 written against independently sealed original theorem inputs plus separately sealed real normalized-leakage consumer. No root imports/Registry/publication status edited.')
