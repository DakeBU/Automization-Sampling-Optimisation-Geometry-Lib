"""Prepare only a prospective exact proposition, not a theorem proof or a claim."""
from pathlib import Path
import re,json,hashlib
root=Path.cwd();p=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
s=p.read_text(encoding='utf8');part=s.split('private def actual_finite_count_path_statement',1)[1].split('\ntheorem actual_finite_count_path_law',1)[0]
binders=part.split('  exact\n',1)[0]
context=part.split('  exact\n',1)[1].split('    ∃ Z :',1)[0]
blocks=re.findall(r'(?ms)^    let ([^ :]+).*?(?=^    let |\Z)',context)
chunks=re.split(r'(?m)(?=^    let )',context)
keep={'c','Φ','S','rate','Λ','τ','next','record','P','ε','Rec','Hist','Δ','Prefix','m','zAt','K','eventTime','I','Path','Ψ','Γ'}
chosen=[]
for c in chunks:
    if not c.strip():continue
    name=re.match(r'    let ([^ :]+)',c).group(1)
    if name in keep:chosen.append(c)
assert len(chosen)==len(keep)
binding='    ∃ Z :'+part.split('    ∃ Z :',1)[1].split('      (∀ n : ℕ, ∀ T : ℝ≥0,',1)[0]
tail='''    let wgt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ :=
      fun y xRef z₀ n T t =>
        Real.exp (-(∫ s in (0 : ℝ)..(T : ℝ),
          rate xRef (Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩))) *
        ∏ i : Fin n,
          rate xRef (Φ y xRef (t.val i -
            (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))
'''
end='''      (∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
        let ZT : (ℕ → ℝ) → Path T := fun u s => Z y xRef z₀ s.val u
        ∀ F : Path T → ℝ, Measurable F → ∀ M : ℝ, 0 ≤ M →
          (∀ p : Path T, |F p| ≤ M) →
          Integrable (fun u => F (ZT u)) P ∧
          (∀ n : ℕ, Integrable (fun t : Prefix n T =>
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t) (m n T)) ∧
          Summable (fun n : ℕ => |∫ t : Prefix n T,
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t ∂m n T|) ∧
          (∫ u, F (ZT u) ∂P) = ∑' n : ℕ, ∫ t : Prefix n T,
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t ∂m n T)
'''
pre=root/'runs/20261007-companion-priority/pbps-bounded-path-expansion-preread95';pre.mkdir(exist_ok=False)
head='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity

open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped NNReal ENNReal Topology Interval BigOperators
open scoped Classical
namespace PBPSBoundedPathExpansionCandidate95
set_option autoImplicit false

/-- Prospective proposition only; no proof or completion claim. -/
noncomputable def candidate_statement'''+binders+'  exact\n'+''.join(chosen)+tail+binding+end+'''
#check @candidate_statement
#print axioms candidate_statement
end PBPSBoundedPathExpansionCandidate95
'''
(pre/'Header95.lean').write_text(head,encoding='utf8',newline='\n')
(pre/'draft-provenance95.json').write_text(json.dumps(dict(status='UNSEALED_PROSPECTIVE_STATEMENT_ONLY',source='arXiv:2609.06905v1 Appendix A.1 (A.7)',actual93_module_RAW=hashlib.sha256(p.read_bytes()).hexdigest(),inherited_literal_definitions=sorted(keep),actual_process_binding='Exact joint measurability, covered-arc, uncovered fallback and AE initial condition clauses inherited literally from actual93.',new_statement='Complete bounded real coordinate-measurable path functional expansion with actual/sector integrability and absolute series convergence.',proof_search_started=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print(pre/'Header95.lean')
