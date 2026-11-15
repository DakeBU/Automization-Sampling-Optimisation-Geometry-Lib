"""Choose a smaller deterministic canonical producer before any seal or proof."""
from pathlib import Path
import json,hashlib
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
p='''∀ {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι],
  ∀ (A : Matrix ι ι ℝ), A.IsHermitian → ∀ s : ℝ,
    0 < Matrix.trace (NormedSpace.exp (s • A)) ∧
      Matrix.trace (NormedSpace.exp (s • A)) ≤
        (Fintype.card ι : ℝ) * Real.exp (|s| * ‖A‖)
'''
t=(w/'T.candidate.v1.txt').read_text().replace('(∀ᵐ ω ∂μ, 0 < f ω ∧ f ω ≤ B)','(∀ ω, 0 < f ω ∧ f ω ≤ B)')
for name,value in [('P',p),('T',t)]:
    out=w/(name+'.candidate.v2.txt');assert not out.exists();out.write_text(value)
header='''import AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder ENNReal
noncomputable section
universe u
namespace GCTraceMgfDomainMinimalInterfaceOnly
'''
formation=header+'def CandidateP : Prop :=\n'+p+'\ndef CandidateT : Prop :=\n'+t+'\n#check CandidateP\n#check CandidateT\nend GCTraceMgfDomainMinimalInterfaceOnly\n'
(w/'InterfaceFormation.v2.lean').write_text(formation)
record={'phase':'UNTRACKED_SMALLER_TYPE_FORMATION_ONLY_NO_SEAL_PROOF_OR_ADMISSION',
 'scope_choice':'Choose the deterministic all-real strict trace-exponential/cardinality bound as the single canonical producer. Derive all actual Gaussian regularity, domination, integrability and ordinary integral positivity/cap inside the private literal consumer. Avoid a larger generic probability-domain public wrapper.',
 'source_boundary_correction':'The GC.FINITE.MGF bridge is pointwise on the literal Gaussian experiment; the v2 consumer asks pointwise, rather than merely a.e., positivity and cap. Existing canonical Radius/Structure interfaces supply pointwise premises internally. This is a pre-seal statement design correction, not a proof-driven weakening.',
 'v1_preserved':'Candidate v1 and actual successful type-only receipt remain unchanged. No v1 statement was sealed/admitted/proved.',
 'P_sha256':hashlib.sha256(p.encode()).hexdigest(),'T_sha256':hashlib.sha256(t.encode()).hexdigest(),
 'source_Boundary':'All real s, both weights and signs, q=0, ordinary nonnormalized trace and matrix dimensionr²; capr² exp(|s|dRstar). No matrix MGF subadditivity/Lieb/Bernstein/C6/main bound.',
 'target_proof_search_started':False,'production_or_ledger_changes':0}
(w/'minimal-interface-selection.v2.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False))
