import B3FrameExtraction

open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock

namespace TransposeWitness

private noncomputable def turn : O 2 :=
  ⟨!![(0 : ℝ), -1; 1, 0], by
    apply (Matrix.mem_orthogonalGroup_iff (Fin 2) ℝ).2
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply, Fin.sum_univ_two]⟩

theorem inverse_differs : turn⁻¹ ≠ turn := by
  intro h
  have he := congrArg (fun W : O 2 => W.val 0 1) h
  change (1 : ℝ) = -1 at he
  norm_num at he

/-- Omitting the transpose from the inverse reconstruction gives a different
latent matrix for this orthogonal residual, in every pair of ambient frames. -/
theorem omitted_transpose_changes_reconstruction (D R : O 3) (Q : S 3 → O 3) (u z : S 3) :
    framed (r := 0) D R (assemble (n := 1) Q u z turn)⁻¹ ≠
      framed (r := 0) (extendFrame D (Q z)) (extendFrame R (Q u)) (residualEmbed 2 turn) := by
  rw [inverse_frame_update]
  intro he
  unfold framed at he
  have hmid := mul_left_cancel (mul_right_cancel he)
  change residualEmbed 2 turn⁻¹ = residualEmbed 2 turn at hmid
  have hl := congrArg (fun G : O 3 => lowerBlock G.val) hmid
  rw [lowerBlock_residualEmbed, lowerBlock_residualEmbed] at hl
  exact inverse_differs (Subtype.ext hl)

#print axioms omitted_transpose_changes_reconstruction

end TransposeWitness
