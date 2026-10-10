from pathlib import Path
import hashlib, json

base=Path('runs/20261007-companion-priority')
pre=base/'pbps-reflection-rotation-preproof69'; r=base/'pbps-reflection-intertwining69'
assert json.loads((r/'preproof-admission.json').read_bytes())['status']=='CLAIMED_EXPLORING_NOT_PROVED'
dest=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean')
assert not dest.exists()
old=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean').read_text(encoding='utf-8')
private=(pre/'statement0.definition.lean').read_text(encoding='utf-8').rstrip()
public=(pre/'header0-public.lean').read_text(encoding='utf-8').rstrip()
prefix=old[old.index('  classical\n',old.index('theorem actual_sharp_corrector_bound\n')):old.index('  have hKself :')]
tail=old[old.index('  unfold actual_sharp_corrector_bound_statement\n'):old.index('\n\n\nend\n')]
tail=tail.replace('actual_sharp_corrector_bound_statement','actual_reflection_intertwining_statement')
tail=tail.replace('hCommInv,hKself,hCoefficient,hPair,?_','hCommInv,?_')
body=r'''  let D : Hperp →L[ℝ] Hperp := R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL
  have hD (h : Hperp) : (D h : Lp ℝ 2 J)=
      U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J)) := hR (U (h : Lp ℝ 2 J))
  letI : IsProbabilityMeasure μ := hμ
  obtain ⟨ρ,hρ,hρf,U2,hU2,hU2i,hU2s,hρp,hBB,hBD,hBE⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2.actual_reflection_block_identities μ hη
  have hU2eq : U2=U := by
    apply LinearIsometry.ext
    intro f
    apply Lp.ext
    exact (hU2 f).trans (hU f).symm
  subst U2
  let AJ : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J := P*U.toContinuousLinearMap*P
  let BA : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J := (1-P)*U.toContinuousLinearMap*P
  let DA : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J := (1-P)*U.toContinuousLinearMap*(1-P)
  have hBDtyped : BA.adjoint ∘L DA= -(AJ ∘L BA.adjoint) := hBD
  have hPself : IsSelfAdjoint P := isSelfAdjoint_starProjection HP
  have hAJself : IsSelfAdjoint AJ := by
    change star (P*U.toContinuousLinearMap*P)=P*U.toContinuousLinearMap*P
    simp only [star_mul,hPself.star_eq,hUs.star_eq,mul_assoc]
  let ι : HP0 →L[ℝ] Lp ℝ 2 J := HP.subtypeL ∘L HP0.subtypeL
  have hBambient (u : HP0) : BA (ι u)=(B0 u : Lp ℝ 2 J) := (hB0 u).symm
  have hAambient (u : HP0) : AJ (ι u)=ι (A0 u) := by
    change P (U (P ((u : HP) : Lp ℝ 2 J)))=((A0 u : HP) : Lp ℝ 2 J)
    rw [hPf]
    change (A (u : HP) : Lp ℝ 2 J)=((A0 u : HP) : Lp ℝ 2 J)
    exact congrArg (fun x : HP => (x : Lp ℝ 2 J)) (hA0 u).symm
  have hDambient (h : Hperp) : DA (h : Lp ℝ 2 J)=(D h : Lp ℝ 2 J) := by
    change U ((h : Lp ℝ 2 J)-P (h : Lp ℝ 2 J))-
      P (U ((h : Lp ℝ 2 J)-P (h : Lp ℝ 2 J)))=(D h : Lp ℝ 2 J)
    rw [show P (h : Lp ℝ 2 J)=0 from h.property,sub_zero]
    exact (hD h).symm
  have hB0intertwine : B0.adjoint ∘L D= -(A0 ∘L B0.adjoint) := by
    apply ContinuousLinearMap.ext
    intro h
    apply ext_inner_left ℝ
    intro u
    change inner ℝ u (B0.adjoint (D h))=inner ℝ u (-(A0 (B0.adjoint h)))
    calc
      inner ℝ u (B0.adjoint (D h))=inner ℝ (B0 u) (D h) := B0.adjoint_inner_right u (D h)
      _ = inner ℝ (BA (ι u)) (DA (h : Lp ℝ 2 J)) := by rw [hBambient,hDambient]; rfl
      _ = inner ℝ (ι u) (BA.adjoint (DA (h : Lp ℝ 2 J))) := (BA.adjoint_inner_right _ _).symm
      _ = inner ℝ (ι u) (-(AJ (BA.adjoint (h : Lp ℝ 2 J)))) := by
        have hb := DFunLike.congr_fun hBDtyped (h : Lp ℝ 2 J)
        change BA.adjoint (DA (h : Lp ℝ 2 J))= -(AJ (BA.adjoint (h : Lp ℝ 2 J))) at hb
        rw [hb]
      _ = -inner ℝ (AJ (ι u)) (BA.adjoint (h : Lp ℝ 2 J)) := by
        simpa only [inner_neg_right,hAJself.adjoint_eq] using
          congrArg Neg.neg (AJ.adjoint_inner_right (ι u) (BA.adjoint (h : Lp ℝ 2 J)))
      _ = -inner ℝ (BA (AJ (ι u))) (h : Lp ℝ 2 J) := by rw [BA.adjoint_inner_right]
      _ = -inner ℝ (B0 (A0 u)) h := by rw [hAambient,hBambient]; rfl
      _ = -inner ℝ (A0 u) (B0.adjoint h) := by rw [B0.adjoint_inner_right]
      _ = inner ℝ u (-(A0 (B0.adjoint h))) := by
        simpa only [inner_neg_right,hA0self.adjoint_eq] using
          (congrArg Neg.neg (A0.adjoint_inner_right u (B0.adjoint h))).symm
  have hVadjEq : V0.adjoint=Inv ∘L B0.adjoint := by
    rw [hVdef,ContinuousLinearMap.adjoint_comp,hInvSelf.adjoint_eq]
  have hIntertwine : V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) := by
    calc
      V0.adjoint ∘L D=Inv ∘L (B0.adjoint ∘L D) := by rw [hVadjEq,ContinuousLinearMap.comp_assoc]
      _ = Inv ∘L (-(A0 ∘L B0.adjoint)) := by rw [hB0intertwine]
      _ = -(A0 ∘L V0.adjoint) := by
        apply ContinuousLinearMap.ext
        intro h
        change Inv (-(A0 (B0.adjoint h)))= -(A0 (V0.adjoint h))
        rw [map_neg,hVadjEq]
        change -(Inv (A0 (B0.adjoint h)))= -(A0 (Inv (B0.adjoint h)))
        exact congrArg Neg.neg (DFunLike.congr_fun hCommInv.eq (B0.adjoint h)).symm
  have hFinal :
      (∀ h : Hperp, (D h : Lp ℝ 2 J)=U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧
      V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) ∧
      (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →
        ∃ fP : HP0,
          HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f ∧
          let fperp : Hperp := R f
          let fV : HP0 := V0.adjoint fperp
          B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) ∧
          HP0.subtypeL (ΓP0 fV)=ΓP (HP0.subtypeL fV) ∧
          ‖f‖^2=‖fP‖^2+‖fperp‖^2 ∧ ‖fV‖≤‖fperp‖) := ⟨hD,hIntertwine,hGlobal⟩
'''
head='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation

/-!
# Actual PBPS reflection intertwining

Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix B.1 and B.3,
the full micro-space intertwining used in (B.21) and Lemma B.4.
The private literal statement preserves all original inputs and witnesses.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

'''
ending='''

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining
'''
text=head+private+'\n\n'+public+' := by\n'+prefix+body+tail+ending
assert 'SharpCorrectorEnergy' not in text and 'HilbertCorrectorBound' not in text
dest.write_text(text,encoding='utf-8',newline='\n')
print('Created sealed actual full-micro69 target; no axiom, placeholder, new assumption or sharp-energy dependency.')
