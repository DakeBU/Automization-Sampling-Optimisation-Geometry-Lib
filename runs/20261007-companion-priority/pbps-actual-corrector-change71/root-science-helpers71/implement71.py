from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');pre=Path('runs/20261007-companion-priority/pbps-corrector-change-preproof71')
assert (r/'claim.json').is_file();p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean');assert not p.exists()
header=(pre/'header71.named-literal.proposed.lean').read_text(encoding='utf8')
assert hashlib.sha256(header.encode()).hexdigest()=='2bef0d5cf364270b6f580288e966d9bb78310f646a7fe13b6f8855807e70f42c'
parent=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean').read_text(encoding='utf8')
start=parent.index('  classical\n');initial=parent[start:parent.index('  change (∀ f : Lp',start)]
initial=initial.replace('ReflectionIntertwining.actual_reflection_intertwining','ActualProjectedRotation.actual_projected_rotation')
blocks=parent[parent.index('  let D : Hperp',start):parent.index('  letI : IsProbabilityMeasure μ',start)]
energy=parent[parent.index('  have hΓself :'):parent.index('  have hGlobal70 :')]
literal=header[header.index('private def actual_corrector_change_statement'):header.index('\ntheorem actual_corrector_change')]
tail=literal[literal.index('                          (∀ f : Lp'):].strip()
reassembly=parent[parent.index('  refine ⟨hμ, ?_⟩'):parent.index('\nend\nend AutoSamplingTheory')]
algebra=r'''  let K : HP0 →L[ℝ] HP0 := A0 ∘L Inv
  have hInvΓ (u : HP0) : Inv (ΓP0 u)=u := by
    have h := DFunLike.congr_fun hLeft u
    simpa only [ContinuousLinearMap.mul_apply,ContinuousLinearMap.one_apply] using h
  have hΓInv (u : HP0) : ΓP0 (Inv u)=u := by
    have h := DFunLike.congr_fun hRight u
    simpa only [ContinuousLinearMap.mul_apply,ContinuousLinearMap.one_apply] using h
  have hCommEval (u : HP0) : A0 (ΓP0 u)=ΓP0 (A0 u) :=
    DFunLike.congr_fun hComm0.eq u
  have hCommInvEval (u : HP0) : A0 (Inv u)=Inv (A0 u) :=
    DFunLike.congr_fun hCommInv.eq u
  have hKΓ (u : HP0) : K (ΓP0 u)=A0 u := congrArg A0 (hInvΓ u)
  have hΓK (u : HP0) : ΓP0 (K u)=A0 u := by
    change ΓP0 (A0 (Inv u))=A0 u
    calc
      ΓP0 (A0 (Inv u))=A0 (ΓP0 (Inv u)) := (hCommEval (Inv u)).symm
      _ = A0 u := congrArg A0 (hΓInv u)
  have hKA (u : HP0) : K (A0 u)=A0 (K u) := by
    change A0 (Inv (A0 u))=A0 (A0 (Inv u))
    exact congrArg A0 (hCommInvEval u).symm
  have hSquareApply (u : HP0) : A0 (A0 u)+ΓP0 (ΓP0 u)=u := by
    have h := DFunLike.congr_fun hSquare0 u
    simpa only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply] using h
  have hKMixedVector (u : HP0) : A0 (K (A0 u))+ΓP0 (A0 u)=K u := by
    calc
      A0 (K (A0 u))+ΓP0 (A0 u)=K (A0 (A0 u))+K (ΓP0 (ΓP0 u)) :=
        congrArg₂ (fun x y : HP0 => x+y) (hKA (A0 u)).symm
          ((hCommEval u).symm.trans (hKΓ (ΓP0 u)).symm)
      _ = K (A0 (A0 u)+ΓP0 (ΓP0 u)) := (K.map_add _ _).symm
      _ = K u := congrArg K (hSquareApply u)
  have hMixed (u v : HP0) :
      inner ℝ (K (A0 u)) (A0 v)+inner ℝ (A0 u) (ΓP0 v)=inner ℝ (K u) v := by
    calc
      inner ℝ (K (A0 u)) (A0 v)+inner ℝ (A0 u) (ΓP0 v)=
          inner ℝ (A0 (K (A0 u))) v+inner ℝ (ΓP0 (A0 u)) v :=
        congrArg₂ (fun x y : ℝ => x+y)
          (hA0self.isSymmetric (K (A0 u)) v).symm
          (hΓself.isSymmetric (A0 u) v).symm
      _ = inner ℝ (A0 (K (A0 u))+ΓP0 (A0 u)) v := (inner_add_left _ _ _).symm
      _ = inner ℝ (K u) v := by rw [hKMixedVector]
  have hDiagL (u : HP0) : inner ℝ (K (A0 u)) (ΓP0 u)=‖A0 u‖^2 := by
    calc
      inner ℝ (K (A0 u)) (ΓP0 u)=inner ℝ (ΓP0 (K (A0 u))) u :=
        (hΓself.isSymmetric _ _).symm
      _ = inner ℝ (A0 (A0 u)) u := by rw [hΓK]
      _ = inner ℝ (A0 u) (A0 u) := hA0self.isSymmetric _ _
      _ = ‖A0 u‖^2 := real_inner_self_eq_norm_sq _
  have hDiagR (v : HP0) : inner ℝ (K (ΓP0 v)) (A0 v)=‖A0 v‖^2 := by
    rw [hKΓ,real_inner_self_eq_norm_sq]
  have hSwap (u v : HP0) : inner ℝ (ΓP0 u) (A0 v)=inner ℝ (A0 u) (ΓP0 v) :=
    (hCross u v).symm
  have hSwap2 (u v : HP0) : inner ℝ (A0 v) (ΓP0 u)=inner ℝ (A0 u) (ΓP0 v) :=
    (real_inner_comm _ _).trans (hSwap u v)
  have hCorrector (u v : HP0) :
      ((‖A0 u-ΓP0 v‖^2-‖ΓP0 u+A0 v‖^2)/2-
        inner ℝ (K (A0 u-ΓP0 v)) (ΓP0 u+A0 v))-
      ((‖u‖^2-‖v‖^2)/2-inner ℝ (K u) v)= -‖u‖^2+‖v‖^2 := by
    rw [norm_sub_sq_real,norm_add_sq_real,map_sub,inner_sub_left,
      inner_add_right,inner_add_right,hDiagL,hDiagR,hKΓ,hSwap2,hSwap]
    nlinarith only [hEnergy u,hEnergy v,hMixed u v]
'''
globalproof=r''' := by
    intro f hf
    obtain ⟨fP,hfP,hBf,hΓf,hBudget,hVBudget,hgMean,gP,hgP,hgPformula,hgVformula,hgEnergy⟩ :=
      hGlobal f hf
    refine ⟨fP,hfP,hBf,hΓf,hBudget,hVBudget,hgMean,gP,hgP,hgPformula,hgVformula,hgEnergy,?_⟩
    change ((‖gP‖^2-‖V0.adjoint (R (U (P f-(f-P f))))‖^2)/2-
        inner ℝ (K gP) (V0.adjoint (R (U (P f-(f-P f))))))-
      ((‖fP‖^2-‖V0.adjoint (R f)‖^2)/2-inner ℝ (K fP) (V0.adjoint (R f)))=
      -‖fP‖^2+‖V0.adjoint (R f)‖^2
    rw [hgPformula,hgVformula]
    exact hCorrector fP (V0.adjoint (R f))
'''
final='''  have hFinal :\n      (∀ h : Hperp, (D h : Lp ℝ 2 J)=U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧\n      V0.adjoint ∘L D= -(A0 ∘L V0.adjoint) ∧\n      '''+tail+' := ⟨hD,hIntertwine,hGlobal71⟩\n'
code=header+initial+blocks+energy+algebra+'  have hGlobal71 :\n      '+tail+globalproof+final+reassembly+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange\n\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange.actual_corrector_change\n'
assert code.startswith(header)
p.write_text(code,encoding='utf8',newline='\n')
(r/'implementation71.json').write_text(json.dumps(dict(status='FIRST_SEALED71_IMPLEMENTATION_NOT_COMPILED',actual_root_PID=os.getpid(),file=p.as_posix(),RAW_bytes=len(code.encode()),RAW_sha256=hashlib.sha256(code.encode()).hexdigest(),exact147line_header_retained=True,actual_parent70_not_reproved=True,no_new_public_premises=True,independently_verified=False),indent=2)+'\n',encoding='utf8')
print('PASS first complete intended71 proof written with exact sealed header; focused compiler check pending.')
