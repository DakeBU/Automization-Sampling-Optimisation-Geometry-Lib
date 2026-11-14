"""First implementation of the sealed canonical real-matrix PSD expectation lemma."""
from pathlib import Path
import hashlib
import json

workspace = Path(__file__).resolve().parent
signature = (workspace / 'producer-signature.original.txt').read_bytes()
assert hashlib.sha256(signature).hexdigest() == '283e07e3c85b9a5cce5c3c40f574f23f593dfcca5e35be4d3e2800f378208b19'
assert json.loads((workspace / 'actual-intake-state-readback.json').read_bytes())['state'] == 'EXPLORING'
header = '''import Mathlib.Analysis.Convex.Integral
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.LinearAlgebra.Matrix.PosDef

/-! ASTIS-authored reusable background for positivity under expectation.
The full PSD cone geometry is proved here once. Concrete source applications
must derive integrability and AE positivity internally. Empty finite matrix
indices are permitted. This is not a printed generic theorem in the paper. -/

noncomputable section
open MeasureTheory
open scoped Matrix.Norms.L2Operator
set_option autoImplicit false

namespace AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral

theorem integral_posSemidef
'''
body = ''':= by
  classical
  let M := Matrix n n ℝ
  have PSD_closed : IsClosed {A : M | A.PosSemidef} := by
    have hermitian_closed : IsClosed {A : M | A.IsHermitian} := by
      change IsClosed {A : M | star A = A}
      exact isClosed_eq continuous_star continuous_id
    have quadratic_closed (v : n → ℝ) :
        IsClosed {A : M | 0 ≤ dotProduct (star v) (Matrix.mulVec A v)} := by
      apply isClosed_le continuous_const
      change Continuous (fun A : M => ∑ a, star (v a) * ∑ b, A a b * v b)
      fun_prop
    convert hermitian_closed.inter (isClosed_iInter quadratic_closed) using 1
    ext A
    simp [Matrix.posSemidef_iff_dotProduct_mulVec]
  have PSD_convex : Convex ℝ {A : M | A.PosSemidef} := by
    intro A hA B hB a b ha hb hab
    exact (hA.smul ha).add (hB.smul hb)
  exact PSD_convex.integral_mem PSD_closed hpos hf

end AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
'''
path = Path('AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveIntegral.lean')
with path.open('xb') as out:
    out.write(header.encode() + signature + body.encode())
print(json.dumps({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'exact_sealed_signature_unchanged': True}))
