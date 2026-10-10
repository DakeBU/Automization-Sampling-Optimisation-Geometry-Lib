from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72')
sha=lambda b:hashlib.sha256(b).hexdigest()
def new(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
old=Path('runs/20261007-companion-priority/pbps-corrector-change-preproof71/header71.named-literal.proposed.lean').read_text(encoding='utf8')
assert old.endswith('  unfold actual_corrector_change_statement\n')
actual=old.replace('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation','import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange\nimport AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation',1)
actual=actual.replace('ActualCorrectorChange\nopen','ActualCorrectorPerturbation\nopen',1).replace('actual_corrector_change','actual_corrector_perturbation')
before='                                C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2)'
after='''                                C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2 ∧
                                (∀ u v r : HP0,
                                  C (u+ΓP0 r) (v-A0 r)-C u v=
                                    inner ℝ u (Inv r)+‖r‖^2/2))'''
assert actual.count(before)==1;actual=actual.replace(before,after,1)
actual=actual.replace('  unfold actual_corrector_perturbation_statement\n','')
actual=actual.replace('# Actual PBPS corrector change under the actual reflection step','# Actual PBPS corrector perturbation on the same centered space',1)
actual=actual.replace('projected rotation and two-component energy used in (B.21) and Lemma B.4.','B.4 unnumbered perturbation algebra (Ex28--Ex34), keeping all earlier\nactual projected rotation and B.21 conclusions.',1)
leaf='''import Mathlib.Analysis.InnerProductSpace.Adjoint

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation
noncomputable section
open scoped RealInnerProductSpace
set_option autoImplicit false

theorem quadratic_corrector_perturbation
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    [CompleteSpace H]
    (A G Inv : H →L[ℝ] H)
    (hA : IsSelfAdjoint A) (hG : IsSelfAdjoint G)
    (hInv : IsSelfAdjoint Inv) (hAInv : Commute A Inv)
    (hInvG : Inv * G = 1) (hGInv : G * Inv = 1)
    (hSquares : A * A + G * G = 1)
    (u v r : H) :
    let C : H → H → ℝ := fun u v =>
      (‖u‖^2 - ‖v‖^2)/2 - inner ℝ (A (Inv u)) v
    C (u + G r) (v - A r) - C u v =
      inner ℝ u (Inv r) + ‖r‖^2/2
'''
for name,text in [('header72.actual.named-literal.proposed.lean',actual),('header72.generic.proposed.lean',leaf)]:
 p=r/name;assert not p.exists();p.write_text(text,encoding='utf8',newline='\n')
new(r/'header72.proposal.json',dict(status='PROSPECTIVE_HEADERS_ONLY_NOT_SEALED_NOT_CLAIMED',actual_root_PID=os.getpid(),checked_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),headers=[dict(path=(r/n).as_posix(),RAW_sha256=sha((r/n).read_bytes()),LF_sha256=sha((r/n).read_bytes().replace(b'\r\n',b'\n'))) for n in ['header72.actual.named-literal.proposed.lean','header72.generic.proposed.lean']],proposed_files=['AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorPerturbation.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorPerturbation.lean'],public_declarations=['AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.quadratic_corrector_perturbation','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.actual_corrector_perturbation'],same_actual_six_callers_twelve_common_witnesses=True,retained_all71_conclusions=True,only_new_actual_formula=after,pure_algebra_B21_parent=False,actual_consumer_retains71_and_uses_generic_leaf=True,scope='For all u,v,r on the SAME produced HP0 and same C/A0/Inv. Arbitrary r is not claimed to be actual r_rho. Generic seven same-map structural properties are internally available to original-input actual consumer.',additional_analytic_public_premises=[],proof_search=False,compiled=False,claimed=False,source_verdict=False,VERIFIED=False))
print('PASS prospective72 exact generic and original-input consumer headers only; not sealed, claimed or proved.')
