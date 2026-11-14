import Tests.GaussianComplexityFixedSpectrumGeometry
import Lean
open Matrix InnerProductSpace Lean
open scoped ContDiff
set_option autoImplicit false
set_option pp.universes true

def ExpectedPublic : Prop :=
∀ {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  ContDiff ℝ ∞ f ∧
    (∀ x : EuclideanSpace ℝ (Fin d),
      HasFDerivAt (gradient f) (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) A) x) ∧
    StrongConvexOn (Set.univ : Set (EuclideanSpace ℝ (Fin d))) 1 f ∧
    (∀ x y : EuclideanSpace ℝ (Fin d),
      ‖gradient f x - gradient f y‖ ≤ κ * ‖x - y‖) ∧
    f 0 = 0 ∧
    (∀ x : EuclideanSpace ℝ (Fin d), IsMinOn f Set.univ x ↔ x = 0)

example : ExpectedPublic :=
  @AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry

def ExpectedPrivate : Prop :=
∀ {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ) (O : Matrix.orthogonalGroup (Fin d) ℝ),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  let query : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
  @Measurable (EuclideanSpace ℝ (Fin d))
    (ℝ × EuclideanSpace ℝ (Fin d))
    (borel (EuclideanSpace ℝ (Fin d)))
    (borel (ℝ × EuclideanSpace ℝ (Fin d)))
    (fun x => (f x, query x))

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let wanted := env.constants.toList.filter fun (n, _) =>
    n.toString == "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry" ||
    n.toString.endsWith ".actual_first_order_oracle_measurable"
  unless wanted.length == 2 do throwError "expected exactly two audited constants, found {wanted.length}"
  for (n, ci) in wanted do
    let some value := ci.value? true | throwError "missing kernel proof value for {n}"
    let used := value.getUsedConstants
    let astis := used.filter fun k => k.toString.startsWith "AutoSamplingTheory."
    logInfo m!"DIRECT_ASTIS {n}: {astis}"
    logInfo m!"DIRECT_ALL {n}: {used}"
    logInfo m!"ACTUAL_TYPE {n}: {ci.type}"
    let axs ← Lean.collectAxioms n
    logInfo m!"KERNEL_AXIOMS {n}: {axs}"
    if n.toString.endsWith ".actual_first_order_oracle_measurable" then
      Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
        name := Name.mkSimple "IndependentPrivateLiteralTypeCheck"
        levelParams := []
        type := mkConst (Name.mkSimple "ExpectedPrivate")
        value := mkConst n
      }
      logInfo "PRIVATE_LITERAL_KERNEL_TYPE_APPLICATION_PASS"

#print axioms IndependentPrivateLiteralTypeCheck
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry
