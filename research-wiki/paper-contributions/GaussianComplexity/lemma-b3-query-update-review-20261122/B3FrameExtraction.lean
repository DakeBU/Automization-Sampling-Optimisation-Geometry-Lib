import B3FrameUpdate
import B3ResidualUpdate

open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames

set_option autoImplicit false

/-- The actual old draw has the updated forward and inverse factorizations, with the
two new frames selected by the query direction and the normalized *observed response*. -/
theorem query_frame_reconstruction {n r : ℕ} (D R : O ((n+2)+r))
    (W : O (n+2)) (Q : S (n+2) → O (n+2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (a : Vec r) {s : ℝ} (hs : s ≠ 0) (u : S (n+2)) :
    let c := s • WithLp.ofLp u.val
    let yForward := act (framed D R W) (act D (splitVec r a c))
    let yInverse := act (framed D R W)⁻¹ (act R (splitVec r a c))
    framed D R W =
        framed (extendFrame D (Q u)) (extendFrame R (Q (decodeResponse R s yForward)))
          (residualEmbed (n+1) (extractResidual Q hfirst u W)) ∧
      framed D R W =
        framed (extendFrame D (Q (decodeResponse D s yInverse))) (extendFrame R (Q u))
          (residualEmbed (n+1) (extractResidual Q hfirst u W⁻¹)⁻¹) := by
  dsimp only
  rcases normalized_responses D R W a s u with ⟨hf, hi⟩
  rw [hf, hi, decode_encodeResponse R a hs, decode_encodeResponse D a hs,
    residualEmbed_extractResidual, residualEmbed_extractResidual_inverse]
  simp only [framed, extendFrame, map_mul, map_inv, _root_.mul_inv_rev]
  constructor <;> group

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
