from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
pre=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70')
assert (r/'claim.json').is_file()
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean');assert not p.exists()
header=(pre/'header0-proposed-expanded.lean').read_text(encoding='utf-8')
parent=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean').read_text(encoding='utf-8')
start=parent.index('  classical\n')
initial=parent[start:parent.index('  let D : Hperp',start)]
initial=initial.replace('ActualRootCommutation.actual_same_root_inverse_commutation','ReflectionIntertwining.actual_reflection_intertwining')
initial=initial.replace('  have hGlobal := parentSlice65\n','  have hDparent := parentSlice65.1\n  have parentSlice66 := parentSlice65.2\n  have hIntertwineParent := parentSlice66.1\n  have hGlobal := parentSlice66.2\n')
tail=header[header.index('                          (∀ f : Lp'):].strip()
reassembly=parent[parent.index('  refine ⟨hμ, ?_⟩'):parent.index('\nend\nend AutoSamplingTheory')]
body=r'''  let D : Hperp →L[ℝ] Hperp := R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL
  have hD (h : Hperp) : (D h : Lp ℝ 2 J)=
      U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J)) := hDparent h
  have hIntertwine : V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) := hIntertwineParent
  letI : IsProbabilityMeasure μ := hμ
  letI : IsProbabilityMeasure J := hJ
  let F : E × E → E × E := fun z => (z.1,(2 : ℝ) • z.1-z.2)
  have hFmeas : Measurable F := by fun_prop
  have hFJ : Measure.map F J=J :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection.reflection_preserves_augmentation μ η hη).2
  have hUIntegral (u : Lp ℝ 2 J) : (∫ z, U u z ∂J)=∫ z, u z ∂J := by
    calc
      (∫ z, U u z ∂J)=(∫ z, u (F z) ∂J) := integral_congr_ae (hU u)
      _ = (∫ z, u z ∂Measure.map F J) :=
        (integral_map hFmeas.aemeasurable (by rw [hFJ]; exact (Lp.memLp u).aestronglyMeasurable)).symm
      _ = (∫ z, u z ∂J) := by rw [hFJ]
  have hPIntegral (u : Lp ℝ 2 J) : (∫ z, P u z ∂J)=∫ z, u z ∂J := by
    change (∫ z, (condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le u : E × E → ℝ) z ∂J)=_
    simpa only [Measure.restrict_univ] using
      (integral_condExpL2_eq (𝕜:=ℝ) (s:=Set.univ) measurable_snd.comap_le u
        MeasurableSet.univ (measure_ne_top J Set.univ))
  have hIntegrable (u : Lp ℝ 2 J) : Integrable u J :=
    MemLp.integrable (by norm_num : (1 : ℝ≥0∞) ≤ 2) (Lp.memLp u)
  have hSubIntegral (u v : Lp ℝ 2 J) :
      (∫ z, (u-v) z ∂J)=(∫ z, u z ∂J)-(∫ z, v z ∂J) :=
    (integral_congr_ae (Lp.coeFn_sub u v)).trans (integral_sub (hIntegrable u) (hIntegrable v))
  have hPself : IsSelfAdjoint P := isSelfAdjoint_starProjection HP
  let ι : HP0 →L[ℝ] Lp ℝ 2 J := HP.subtypeL ∘L HP0.subtypeL
  have hPι (u : HP0) : P (ι u)=ι u := hPf (u : HP)
  have hOrth (u : HP0) (h : Hperp) : inner ℝ (ι u) (h : Lp ℝ 2 J)=0 := by
    calc
      inner ℝ (ι u) (h : Lp ℝ 2 J)=inner ℝ (P (ι u)) (h : Lp ℝ 2 J) := by rw [hPι]
      _ = inner ℝ (ι u) (P (h : Lp ℝ 2 J)) := hPself.isSymmetric _ _
      _ = 0 := by rw [show P (h : Lp ℝ 2 J)=0 from h.property,inner_zero_right]
  have hMacro (u : HP0) : P (U (ι u))=ι (A0 u) := by
    change (A (u : HP) : Lp ℝ 2 J)=((A0 u : HP) : Lp ℝ 2 J)
    exact congrArg (fun x : HP => (x : Lp ℝ 2 J)) (hA0 u).symm
  have hMicro (u : HP0) : (B0 u : Lp ℝ 2 J)=U (ι u)-P (U (ι u)) := by
    rw [hB0]
    change U (P (ι u))-P (U (P (ι u)))=U (ι u)-P (U (ι u))
    rw [hPι]
  have hUι (u : HP0) : U (ι u)=ι (A0 u)+(B0 u : Lp ℝ 2 J) := by
    rw [hMicro,←hMacro]
    abel
  have hRmicro (h : Hperp) : R (h : Lp ℝ 2 J)=h := by
    apply Subtype.ext
    rw [hR,show P (h : Lp ℝ 2 J)=0 from h.property,sub_zero]
  have hRUm (u : HP0) : R (U (ι u))=B0 u := by
    apply Subtype.ext
    rw [hR]
    exact (hMicro u).symm
  have hVadjB (u : HP0) : V0.adjoint (B0 u)=ΓP0 u := by
    have hb := DFunLike.congr_fun hFactor u
    change B0 u=V0 (ΓP0 u) at hb
    rw [hb]
    exact DFunLike.congr_fun hVadj (ΓP0 u)
  have hΓself : IsSelfAdjoint ΓP0 := (show ΓP0.IsPositive from hPos0).isSelfAdjoint
  have hEnergy (u : HP0) : ‖A0 u‖^2+‖ΓP0 u‖^2=‖u‖^2 := by
    have h := congrArg (fun L : HP0 →L[ℝ] HP0 => inner ℝ (L u) u) hSquare0
    simp only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply,inner_add_left] at h
    rw [hA0self.isSymmetric (A0 u) u,hΓself.isSymmetric (ΓP0 u) u] at h
    simpa only [real_inner_self_eq_norm_sq] using h
  have hCross (u v : HP0) : inner ℝ (A0 u) (ΓP0 v)=inner ℝ (ΓP0 u) (A0 v) := by
    calc
      inner ℝ (A0 u) (ΓP0 v)=inner ℝ u (A0 (ΓP0 v)) := hA0self.isSymmetric _ _
      _ = inner ℝ u (ΓP0 (A0 v)) := congrArg (fun z : HP0 => inner ℝ u z) (DFunLike.congr_fun hComm0.eq v)
      _ = inner ℝ (ΓP0 u) (A0 v) := (hΓself.isSymmetric _ _).symm
'''
globalproof=r''' := by
    intro f hf
    obtain ⟨fP,hfP,hBf,hΓf,hBudget,hVBudget⟩ := hGlobal f hf
    let fperp : Hperp := R f
    let fV : HP0 := V0.adjoint fperp
    change B.adjoint (fperp : Lp ℝ 2 J)=HP0.subtypeL (ΓP0 fV) at hBf
    have hPfp : P f=ι fP :=
      (congrArg (fun x : HP => (x : Lp ℝ 2 J)) hfP).symm
    have hB0adjMicro : B0.adjoint fperp=ΓP0 fV := by
      apply Subtype.ext
      have h := (hAmbient (fperp : Lp ℝ 2 J)).symm.trans hBf
      rw [hRmicro] at h
      exact h
    let g : Lp ℝ 2 J := U (P f-(f-P f))
    have hgMean : (∫ z, g z ∂J)=0 := by
      change (∫ z, U (P f-(f-P f)) z ∂J)=0
      rw [hUIntegral]
      simp only [hSubIntegral,hPIntegral,hf,sub_self,sub_zero]
    obtain ⟨gP,hgP,hgtail⟩ := hGlobal g hgMean
    have hPgp : P g=ι gP :=
      (congrArg (fun x : HP => (x : Lp ℝ 2 J)) hgP).symm
    have hInput : P f-(f-P f)=ι fP-(fperp : Lp ℝ 2 J) := by
      change P f-(f-P f)=ι fP-(R f : Lp ℝ 2 J)
      rw [hR f,hPfp]
    have hgPformula : gP=A0 fP-ΓP0 fV := by
      apply ext_inner_left ℝ
      intro u
      calc
        inner ℝ u gP=inner ℝ (ι u) (ι gP) := rfl
        _ = inner ℝ (ι u) (P g) := by rw [hPgp]
        _ = inner ℝ (P (ι u)) g := (hPself.isSymmetric _ _).symm
        _ = inner ℝ (ι u) g := by rw [hPι]
        _ = inner ℝ (U (ι u)) (ι fP-(fperp : Lp ℝ 2 J)) := by
          change inner ℝ (ι u) (U (P f-(f-P f)))=_
          rw [hInput]
          exact (hUs.isSymmetric _ _).symm
        _ = inner ℝ (A0 u) fP-inner ℝ (B0 u) fperp := by
          rw [hUι,inner_add_left,inner_sub_right,inner_sub_right,
            hOrth (A0 u) fperp,
            show inner ℝ (B0 u : Lp ℝ 2 J) (ι fP)=0 from
              (real_inner_comm _ _).trans (hOrth fP (B0 u))]
          change (inner ℝ (A0 u) fP-0)+(0-inner ℝ (B0 u) fperp)=_
          ring
        _ = inner ℝ u (A0 fP)-inner ℝ u (ΓP0 fV) := by
          rw [hA0self.isSymmetric u fP,←B0.adjoint_inner_right,hB0adjMicro]
        _ = inner ℝ u (A0 fP-ΓP0 fV) := (inner_sub_right _ _ _).symm
    have hgVformula : V0.adjoint (R g)=ΓP0 fP+A0 fV := by
      change V0.adjoint (R (U (P f-(f-P f))))=_
      rw [hInput,map_sub,map_sub,hRUm,map_sub,hVadjB]
      have hd := DFunLike.congr_fun hIntertwine fperp
      change V0.adjoint (D fperp)= -(A0 fV) at hd
      change ΓP0 fP-V0.adjoint (D fperp)=_
      rw [hd,sub_neg_eq_add]
    have hgEnergy : ‖gP‖^2+‖V0.adjoint (R g)‖^2=‖fP‖^2+‖fV‖^2 := by
      rw [hgPformula,hgVformula,norm_sub_sq_real,norm_add_sq_real,hCross]
      nlinarith only [hEnergy fP,hEnergy fV]
    exact ⟨fP,hfP,hBf,hΓf,hBudget,hVBudget,hgMean,gP,hgP,hgPformula,hgVformula,hgEnergy⟩
  have hFinal :
      (∀ h : Hperp, (D h : Lp ℝ 2 J)=U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧
      V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) ∧
      '''+tail+r''' := ⟨hD,hIntertwine,hGlobal70⟩
'''
prefix='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining

/-!
# Actual PBPS projected reflection rotation

Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix B.3, the actual
projected rotation and two-component energy used in (B.21) and Lemma B.4.
The reflected observable and its conditional/polar components are actual
inputs and outputs. Mean preservation is proved internally from the same law.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

'''
text=prefix+header.rstrip()+' := by\n'+initial+body+'  have hGlobal70 :\n      '+tail+globalproof+reassembly+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation\n\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation\n'
p.write_text(text,encoding='utf-8',newline='\n')
(r/'implementation70.json').write_text(json.dumps(dict(actual_root_PID=os.getpid(),path=p.as_posix(),RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),sealed_public_header_unchanged=True,proof_uncompiled=True),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Wrote one actual projected-rotation proof against sealed full PUBLIC header; uncompiled, no mathematical acceptance.')
