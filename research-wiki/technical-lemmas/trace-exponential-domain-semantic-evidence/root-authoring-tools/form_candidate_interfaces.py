"""Form only the next bounded interfaces; no theorem proof or ledger mutation."""
from pathlib import Path
import json,hashlib
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
p='''∀ {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι],
  ∀ {Ω : Type v} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ],
  ∀ (X : Ω → Matrix ι ι ℝ) (hX : AEStronglyMeasurable X μ),
  (∀ᵐ ω ∂μ, (X ω).IsHermitian) →
  ∀ C : ℝ, (∀ᵐ ω ∂μ, ‖X ω‖ ≤ C) →
  ∀ s : ℝ,
    let f : Ω → ℝ := fun ω => Matrix.trace (NormedSpace.exp (s • X ω))
    let B : ℝ := (Fintype.card ι : ℝ) * Real.exp (|s| * C)
    Integrable f μ ∧ (∀ᵐ ω ∂μ, 0 < f ω ∧ f ω ≤ B) ∧
      0 < ∫ ω, f ω ∂μ ∧ (∫ ω, f ω ∂μ) ≤ B
'''
old=(r/'.astis/huanjian-gc-matrix-laplace-20261114/T.proposition.sealed.v1.txt').read_text()
prefix=old.split('  ∀ s : ℝ, 0 < s →')[0]
t=prefix+'''  let Rstar : ℝ := 2 * r * (L + 1) / (d : ℝ)
  ∀ s : ℝ, ∀ useCos minus : Bool,
    let f : Ω → ℝ := fun ω => Matrix.trace (NormedSpace.exp (s • S useCos minus ω))
    let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
    Integrable f μ ∧ (∀ᵐ ω ∂μ, 0 < f ω ∧ f ω ≤ B) ∧
      0 < ∫ ω, f ω ∂μ ∧ (∫ ω, f ω ∂μ) ≤ B
'''
assert not (w/'P.candidate.v1.txt').exists()
for name,value in [('P',p),('T',t)]:
    (w/(name+'.candidate.v1.txt')).write_text(value)
header='''import AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder ENNReal
noncomputable section
universe u v
namespace GCTraceMgfDomainInterfaceOnly
'''
formation=header+'def CandidateP : Prop :=\n'+p+'\ndef CandidateT : Prop :=\n'+t+'\n#check CandidateP\n#check CandidateT\nend GCTraceMgfDomainInterfaceOnly\n'
(w/'InterfaceFormation.lean').write_text(formation)
record={'phase':'UNTRACKED_TYPE_FORMATION_ONLY_NO_PROOF_OR_ADMISSION',
 'reason':'GC.FINITE.MGF remains open beyond the previous positive-parameter private ingredient: all real parameters, strict positivity and an explicit r²-scaled bound are substantive residual obligations.',
 'candidate_scope':'One future canonical generic trace-exponential probability-domain lemma and one private literal four-family Gaussian consumer. No source Bernstein/C6/main-bound credit.',
 'prior_packet':'R15 proof/source accepted locally; exact reader parent-clipping correction and normal independent V remain separately pending. This pre-intake does not mutate its files, ledger, frontier or ownership.',
 'P_sha256':hashlib.sha256(p.encode()).hexdigest(),'T_sha256':hashlib.sha256(t.encode()).hexdigest(),
 'production_or_ledger_changes':0,'target_proof_search_started':False,
 'reuse_search_observation':{'actual_tool_chunk':'4778e6','exit_code':0,'scope':'Bounded declaration-head patterns over local probability/Gaussian source and pinned matrix/exponential Mathlib files. Found private positive-s ingredients; no exact matching complete public interface among inspected hits. Not an exhaustive absence assertion.'},
 'exact_next_gates':'Actual type formation -> exact seal and recursive binder/literal-definition audit -> independent source-only graph and distinct topology challenge -> only then proof search.'}
(w/'pre-intake.v1.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False))
