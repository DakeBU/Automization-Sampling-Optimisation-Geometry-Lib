from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd(); d=root/'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60'
d.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p); b=p.read_bytes(); z=b.replace(b'\r\n',b'\n'); return dict(path=p.relative_to(root).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(z))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
generic='''theorem exists_positive_complex_lift
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (hD : D.IsPositive) :
    let ι : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
    let R : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
    let Q : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.imCLM.compLpL 2 μ
    let C : Lp ℂ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.conjCLE.toContinuousLinearMap.compLpL 2 μ
    (∀ u : Lp ℝ 2 μ, ‖ι u‖ = ‖u‖) ∧
    (∀ g : Lp ℂ 2 μ, C g = g ↔ ∃ u : Lp ℝ 2 μ, ι u = g) ∧
    ∃ Dc : Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ,
      Dc.IsPositive ∧
      (∀ g : Lp ℂ 2 μ, Dc g = ι (D (R g)) + Complex.I • ι (D (Q g))) ∧
      (∀ u : Lp ℝ 2 μ, Dc (ι u) = ι (D u)) ∧
      (∀ g : Lp ℂ 2 μ, C (Dc g) = Dc (C g))'''
actual='''theorem actual_positive_defect_complex_lift
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let ι : Lp ℝ 2 ν →L[ℝ] Lp ℂ 2 ν := Complex.ofRealCLM.compLpL 2 ν
    let R : Lp ℂ 2 ν →L[ℝ] Lp ℝ 2 ν := Complex.reCLM.compLpL 2 ν
    let Q : Lp ℂ 2 ν →L[ℝ] Lp ℝ 2 ν := Complex.imCLM.compLpL 2 ν
    let C : Lp ℂ 2 ν →L[ℝ] Lp ℂ 2 ν := Complex.conjCLE.toContinuousLinearMap.compLpL 2 ν
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
        IsSelfAdjoint T ∧
        (∀ u : Lp ℝ 2 ν, ‖T u‖ ≤ ‖u‖ ∧
          (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
          (∫ y, T u y ∂ν) = ∫ y, u y ∂ν) ∧
        ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T).IsPositive ∧
        (∀ u : Lp ℝ 2 ν, ‖ι u‖ = ‖u‖) ∧
        (∀ g : Lp ℂ 2 ν, C g = g ↔ ∃ u : Lp ℝ 2 ν, ι u = g) ∧
        ∃ Dc : Lp ℂ 2 ν →L[ℂ] Lp ℂ 2 ν,
          Dc.IsPositive ∧
          (∀ g : Lp ℂ 2 ν, Dc g =
            ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) (R g)) +
            Complex.I • ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) (Q g))) ∧
          (∀ u : Lp ℝ 2 ν, Dc (ι u) = ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) u)) ∧
          (∀ g : Lp ℂ 2 ν, C (Dc g) = Dc (C g))'''
imports='''import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
import Mathlib.Analysis.Complex.Basic
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
set_option autoImplicit false
set_option maxHeartbeats 1000000
'''
for i,h in enumerate([generic,actual]):
 (d/f'header{i}.lean').write_text(h+'\n',encoding='utf-8',newline='\n')
 # Exact binders/conclusion checked as a Prop-valued expression; no proof search.
 name=h.splitlines()[0].split()[1]
 exp=h.replace('theorem '+name,'fun',1).replace(' :\n',' =>\n',1)
 (d/f'elab{i}.lean').write_text(imports+'#check ('+exp+' : _)\n',encoding='utf-8',newline='\n')
contract=dict(status='UNPROVED_STATEMENT_CANDIDATE_NOT_SEALED',headers=[pin(d/f'header{i}.lean') for i in range(2)],type_probes=[pin(d/f'elab{i}.lean') for i in range(2)],parent_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),source_version='arXiv:2609.06905v1',anchor='Appendix D.1 real Hilbert conventions and positive square-root background; B.10-B.11 actual all-macro square-root prerequisite, attributed ASTIS complexification completion, not a printed paper theorem.',primary_contract=pin(root/'runs/20261007-companion-priority/pbps-centered-defect59/next-root-source-scout60/primary.required-objects.json'),scout_only=pin(root/'runs/20261007-companion-priority/pbps-centered-defect59/next-root-source-scout60/next-edge.source-contract.json'),binder_audit={'canonical_node':'Arbitrary measurable Ω and measure μ, real bounded positive D as the exact generic mathematical input. No probability, finite measure, finite-dimensional L2, Nontrivial or CFC premise. Positivity includes symmetry.','paper_consumer':'Only original C2/two Hessians/positive alpha/order/positive capped eta with finite real Hilbert/Borel extension. SAME actual kernel T and D are internally obtained from independently verified59; no D/operator/positivity certificate binder. Rank0 and alphaeta1 retained.'},definition_audit='Actual ofReal/re/im/conjugation scalar maps composed on the SAME quotient Lp spaces by Mathlib compLpL; literal Dc formula and fixed-point range, no defaults, conditional representatives or abstract supplied embedding.',consumer='Actual PBPS D=I-T*T. Later actual all-macro positive root and B11; centered root order/inverse/polar distinct; generic canonical real-to-complex interface also supports exact real reversible-MCMC positive operators.',truth_boundary='No root, real descent of complex CFC root, uniqueness, Gamma0/B15/B16, weakH1/dynamics/main/error/querycost/composition, paper or Goal closure.',owned_files=['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/DefectComplexLift.lean','Tests/ProximalBPSDefectComplexLift.lean'],no_proof_search_yet=True)
write(d/'statement-candidate.json',contract)
print(d.as_posix())
