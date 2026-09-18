import AutoSamplingTheory.Core
import AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Taylor
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Generator
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolev
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay
import AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates
import AutoSamplingTheory.TechnicalLemmas.Geometry.GeodesicConvexity
import AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity
import AutoSamplingTheory.TechnicalLemmas.Geometry.MetricCurve
import AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.DonskerVaradhan
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.KLDensity
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.Renyi
import AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs
import AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral
import AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity
import AutoSamplingTheory.TechnicalLemmas.Measure.KantorovichDual
import AutoSamplingTheory.TechnicalLemmas.Measure.Product
import AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym
import AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel
import AutoSamplingTheory.TechnicalLemmas.Probability.KernelInvariance
import AutoSamplingTheory.TechnicalLemmas.Measure.Transport
import AutoSamplingTheory.TechnicalLemmas.Probability.LawMap
import AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses

/-!
# Technical lemma memory registry

The registry is the compiled Lean side of ASTIS technical lemma memory.  It
records which reusable lemmas exist locally, what upstream/source material
motivated them, and which proof backend they support.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas

inductive LemmaMemoryStatus where
  | formalizedLocal
  | portCandidate
  | sourceGap
  | referenceOnly
deriving Repr, DecidableEq

/-- Metadata for a lemma-memory entry.  The executable proof is the declaration
named in `localDecl`; this structure is only the retrieval record used by
agents and documentation exports. -/
structure LemmaMemoryEntry where
  key : String
  localDecl : String
  upstreamDecl : String
  upstreamFile : String
  status : LemmaMemoryStatus
  tags : List String
  saldUse : String
  note : String
deriving Repr, DecidableEq

def sltSourceAnchor (file decl note : String) : SourceAnchor :=
  sourceAnchor
    ("slt-" ++ file ++ "-" ++ decl)
    "externalLean"
    "https://github.com/YuanheZ/lean-stat-learning-theory"
    (file ++ ":" ++ decl)
    note

def analysisMemory : List LemmaMemoryEntry := [
  {
    key := "analysis.optimisation.uniform-regularization",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.UniformRegularization.uniform_accuracy_and_query_bound",
    upstreamDecl := "QuadraticRegularizationTransfer.exists_minimizer_radius_and_accuracy; QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness; QuadraticRegularizationOracle.simulate_regularized",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section4.1 Lemma4.2",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "optimisation", "regularization", "oracle", "uniform-complexity"],
    saldUse := "Uniform convex solver accuracy and actual normalized query bound from a uniform strongly convex program.",
    note := "Proper Hilbert; positive small-error regime; natural-valued budget and finite deterministic execution. No Phi monotonicity. Full source model/domain adapters remain."
  },
  {
    key := "analysis.optimisation.regularization-oracle",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle.simulate_regularized",
    upstreamDecl := "QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness; Nat.succ_le_succ",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section1.1 and Section4.1 Lemma4.2",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "optimisation", "regularization", "oracle", "query-count"],
    saldUse := "Actual adaptive first-order oracle execution with one original reply per regularized reply.",
    note := "Finite deterministic query-fuel semantics; exact state/outcome/count preservation. Halt and exhaustion distinct. No class-uniform solver/budget or full Lemma4.2 closure."
  },
  {
    key := "analysis.optimisation.regularization-first-order",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness",
    upstreamDecl := "strongConvexOn_iff_convex; LinearMap.convexOn; HasFDerivAt.norm_sq; LipschitzWith.dist_le_mul",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section4.1 Lemma4.2 proof",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "regularization", "smoothness"],
    saldUse := "Actual regularized curvature and gradient Lipschitz shift at first-order regularity.",
    note := "Differentiable convex Hilbert objective with genuine beta-Lipschitz gradient. Nonnegative precision includes zero. No C2/Hessian, minimizer or oracle/class theorem."
  },
  {
    key := "analysis.optimisation.regularization-transfer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationTransfer.exists_minimizer_radius_and_accuracy",
    upstreamDecl := "IsCompact.exists_isMinOn; isCompact_closedBall; Metric.mem_closedBall; dist_eq_norm",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section4.1 Lemma4.2 proof",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "optimisation", "regularization", "minimizer", "accuracy"],
    saldUse := "Construct actual regularized minimum and transfer radius and objective approximation.",
    note := "Continuous proper normed group, supplied original minimum, positive radius and precision. No convexity/C2 assumed; no uniqueness, curvature/smoothness, solver or oracle/class closure."
  },
  {
    key := "analysis.optimisation.restart-log-complexity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.RestartLogComplexity.logarithmic_accuracy_and_cost",
    upstreamDecl := "RestartReduction.radius_accuracy_and_cost; Nat.le_ceil; Nat.ceil_eq_zero; Real.log_le_log_iff; Real.log_pow",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section4.1 Lemma4.1 proof",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "restart", "complexity"],
    saldUse := "Actual logarithmic restart horizon, final accuracy and explicit certified call-cost bounds.",
    note := "Positive radius, C1 Hilbert, supplied minimizer/base solver. N0 retains final call. Global two-term cost; pure-log3/log4 bound only under phi comparison and q>=4. No formal oracle/class realization."
  },
  {
    key := "analysis.optimisation.restart-reduction",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.RestartReduction.radius_accuracy_and_cost",
    upstreamDecl := "StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn; IsLocalMin.fderiv_eq_zero; Nat.rec",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section4.1 Lemma4.1 proof",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "restart"],
    saldUse := "Actual radius-halving restart, final objective accuracy and cumulative certified solver cost.",
    note := "Positive upper radius, C1 Hilbert, supplied minimizer/base solver; exact finite N phi(8kappa)+phi(kappa). No phi monotonicity, oracle-machine or full logarithmic reduction claim; N0 retains polishing."
  },
  {
    key := "analysis.gradient-descent.distance-complexity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentComplexity.distance_le_of_log_bound",
    upstreamDecl := "GradientDescentContraction.gradient_descent_distance_bound; Real.log_le_iff_le_exp",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section3 Theorem3.3 following rate paragraph",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "gradient-descent"],
    saldUse := "Actual reciprocal-step gradient iterates reach distance accuracy under the exact logarithmic budget.",
    note := "Positive alpha,beta,epsilon; threshold only R>0, zero radius and zero iterations retained. C1 Hilbert upper-model generalization; supplied minimizer. Sufficient count, not optimal complexity or companion-paper progress."
  },
  {
    key := "analysis.gradient-descent.convex-normalized-value",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates.convex_value_le",
    upstreamDecl := "Theorem3.4; GradientDescentValue.gradient_descent_weighted_value_bound",
    upstreamFile := "Chewi Lectures on Optimization arXiv2605.07006v1 Section3",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "gradient-descent"],
    saldUse := "Normalized actual-iterate function-value rate from existing weighted parent.",
    note := "Positive h,N; arbitrary comparator; source beta reciprocal specialization tested; no analytic alpha limit."
  },
  {
    key := "analysis.gradient-descent.strong-normalized-value",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates.strongly_convex_value_le",
    upstreamDecl := "Theorem3.4; GradientDescentValue.gradient_descent_weighted_value_bound",
    upstreamFile := "Chewi Lectures on Optimization arXiv2605.07006v1 Section3",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "gradient-descent"],
    saldUse := "Normalized actual-iterate function-value rate from existing weighted parent.",
    note := "Rational q0 extension and exact inverse power only q>0; source singular domain independently reviewed."
  },
  {
    key := "analysis.gradient-flow.last-time-lyapunov",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowLastIterate.lyapunov_and_rates",
    upstreamDecl := "Exercise2.1; ConvexityC2.gradient_mono_iff_fderiv2_lower; StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section2; Mathlib.Analysis.ODE.Gronwall",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "gradient-flow"],
    saldUse := "Actual convex-flow Lyapunov antitonicity and last-time gradient-square/value upper bounds.",
    note := "Hessian positivity derived; C2 Hilbert and right-time generalization explicit. Positive-time normalized coefficients 1/t squared and 1/(4t); nonsmooth sharpness and Exercise2.2 remain separate."
  },
  {
    key := "analysis.gradient-flow.attained-stationarity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowStationarity.exists_min_norm_le",
    upstreamDecl := "Corollary2.8; IsCompact.exists_isMinOn; le_gronwallBound_of_liminf_deriv_right_le",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section2; Mathlib.Analysis.ODE.Gronwall",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "optimisation", "gradient-flow", "stationarity"],
    saldUse := "Attained minimum of actual gradient norm over a positive time interval, bounded by the square root of initial objective gap divided by time.",
    note := "C1 Hilbert and right-time generalization explicit; global minimum and actual flow supplied. No convexity, PL, existence, final-time gradient or full trajectory convergence claim."
  },
  {
    key := "analysis.gradient-flow.convex-value-rate",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowValue.value_le",
    upstreamDecl := "Theorem2.4; firstOrder_lower_bound_of_strongConvexOn; le_gronwallBound_of_liminf_deriv_right_le",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section2; Mathlib.Analysis.ODE.Gronwall",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "gradient-flow"],
    saldUse := "Actual convex gradient trajectory objective rate with direct zero-curvature branch on finite forward intervals.",
    note := "Positive observation time: printed t0 quotient singularity has independent domain-clarification review. Hilbert/differentiability/right-time generalization explicit; minimum and flow supplied; no analytic parameter-limit or existence claim."
  },
  {
    key := "analysis.gradient-flow.pair-contraction",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowContraction.norm_sub_le",
    upstreamDecl := "Theorem2.2; gradient_inner_lower_bound_of_strongConvexOn; HasDerivWithinAt.norm_sq; le_gronwallBound_of_liminf_deriv_right_le",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section2; Mathlib.Analysis.ODE.Gronwall",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "optimisation", "gradient-flow"],
    saldUse := "Two actual gradient trajectories contract with exact curvature rate on finite forward intervals.",
    note := "Source alpha>=0 retained. C2 Euclidean setting generalized to differentiable Hilbert objective and right derivatives; no minimum or nonzero distance needed. No existence, extension or stochastic-flow claim."
  },
  {
    key := "analysis.gradient-flow.pl-dissipation-decay",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowPL.dissipation_and_decay",
    upstreamDecl := "Lemma2.1 and Corollary2.6; HasFDerivAt.comp_hasDerivWithinAt; le_gronwallBound_of_liminf_deriv_right_le",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1 Section2; Mathlib.Analysis.ODE.Gronwall",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "PL", "optimisation", "gradient-flow"],
    saldUse := "Actual Hilbert gradient dynamics yield objective dissipation and PL exponential value decay on a finite forward interval.",
    note := "Source C2 Euclidean setting generalized to differentiable Hilbert objective and right derivatives. Terminal continuity retained; no negative-time dynamics, existence/uniqueness, point-distance or stochastic-flow claim."
  },
  {
    key := "analysis.strong-convex.nonlinear-pl-pullback",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexPLPullback.exists_minimizer_and_pl",
    upstreamDecl := "Exercise2.3 (numerical PL inequality component)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "PL", "optimisation"],
    saldUse := "Strong convexity and adjoint Jacobian coercivity yield a numerical PL bound for a differentiable nonlinear composite, with a lifted global minimizer.",
    note := "Differentiable Hilbert extension; sigma0 is degenerate. Does not assert composite C1 regularity, full positive-modulus PL definition, convexity, uniqueness or algorithm convergence."
  },
  {
    key := "analysis.gradient-descent.convex-gap-sharpness",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexGradientGapSharpness.quadratic_gap_lower_bound",
    upstreamDecl := "Exercise3.3 (convex function-value order in Theorem3.4)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "quadratic", "optimisation"],
    saldUse := "Horizon-dependent admissible quadratic gives exact actual GD gap and beta/(16(N+1)) lower bound at step1/beta.",
    note := "Class beta need not be tight. Witness depends on N; no fixed-objective reciprocal tail, optimal constant, full exercise or adaptive/oracle lower bound."
  },
  {
    key := "analysis.gradient-descent.sharpness",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentSharpness.exists_quadratic_worst_case",
    upstreamDecl := "Exercise3.3 (fixed-step distance sharpness of Exercise3.2)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "quadratic", "optimisation"],
    saldUse := "Actual scalar quadratic witnesses the endpoint envelope at every iteration count and its balanced minimax factor, with all function-class certificates proved.",
    note := "Positive alpha<=beta are valid class bounds, not both tight constants of the witness. Fixed-step distance sharpness only; no full-section or variable/adaptive/oracle lower bound."
  },
  {
    key := "analysis.quadratic-gd.iterate",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent.quadratic_gradient_iterate",
    upstreamDecl := "Exercise3.3 (exact trajectories component)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "quadratic", "optimisation"],
    saldUse := "Actual centered-quadratic gradient derived by differentiation and symmetry; trajectory is the update operator power.",
    note := "Symmetric continuous Hilbert operator generalizes the positive-definite Euclidean source. Identities only: no stability, spectral endpoint existence, full-section sharpness or companion-paper completion."
  },
  {
    key := "analysis.quadratic-gd.eigenmode",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent.quadratic_eigenmode",
    upstreamDecl := "Exercise3.3 (exact trajectories component)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "quadratic", "optimisation"],
    saldUse := "Given a mode relation, exact trajectory, absolute-value norm factor and squared objective factor; zero vector and unstable steps included.",
    note := "Symmetric continuous Hilbert operator generalizes the positive-definite Euclidean source. Identities only: no stability, spectral endpoint existence, full-section sharpness or companion-paper completion."
  },
  {
    key := "analysis.gradient-step.endpoint-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.gradient_step_endpoint_bound",
    upstreamDecl := "Exercise3.2",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "smoothness", "optimisation"],
    saldUse := "Actual-gradient endpoint curvature bound from C2 Hessian bounds, symmetry, Rayleigh norm and explicit segment FTC.",
    note := "C2 actual-gradient Hilbert extension; explicit parameter domains. Uniform curvature envelope, not an objective-specific optimal step, iterate convergence or companion-paper completion."
  },
  {
    key := "analysis.gradient-step.optimal-step",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.optimal_gradient_step",
    upstreamDecl := "Exercise3.2",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "smoothness", "optimisation"],
    saldUse := "Balanced step 2/(alpha+beta) gives factor (beta-alpha)/(alpha+beta), minimizing the endpoint envelope over all real steps.",
    note := "C2 actual-gradient Hilbert extension; explicit parameter domains. Uniform curvature envelope, not an objective-specific optimal step, iterate convergence or companion-paper completion."
  },
  {
    key := "analysis.gradient-descent.sum-sq",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentStationarity.gradient_descent_sum_sq_bound",
    upstreamDecl := "Theorem3.7 and proof",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "smoothness", "optimisation"],
    saldUse := "Actual-iterate accumulated squared-gradient bound via canonical descent and finite telescoping; no minimum needed.",
    note := "Actual gradient and global quadratic upper model; Hilbert algebraic generalization. Explicit domain overlay independently accepted. Best iterate, not last iterate, global optimality or companion-paper completion."
  },
  {
    key := "analysis.gradient-descent.stationarity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentStationarity.exists_gradient_descent_norm_le",
    upstreamDecl := "Theorem3.7 and proof",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "smoothness", "optimisation"],
    saldUse := "Nonconvex best-iterate gradient-norm guarantee from actual updates, supplied global minimum, positive step and nonempty horizon.",
    note := "Actual gradient and global quadratic upper model; Hilbert algebraic generalization. Explicit domain overlay independently accepted. Best iterate, not last iterate, global optimality or companion-paper completion."
  },
  {
    key := "analysis.gradient-descent.step-descent",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentBasic.gradient_step_descent_of_quadratic_upper_bound",
    upstreamDecl := "Lemma3.1",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "smoothness", "optimisation"],
    saldUse := "Canonical public extraction of existing actual-gradient descent; reused by energy/value and PL consumers.",
    note := "Actual totalized gradient in global upper/PL models, h>=0,beta*h<=1; real Hilbert and signed-moduli algebraic extension. Source step repair independently accepted. No convexity, optimizer existence or companion-paper claim."
  },
  {
    key := "analysis.gradient-descent.pl-value",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentPL.gradient_descent_pl_value_bound",
    upstreamDecl := "Theorem3.6",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "smoothness", "optimisation"],
    saldUse := "Actual iterate PL final-value rate; supplied global minimum handles both signs of geometric coefficient.",
    note := "Actual totalized gradient in global upper/PL models, h>=0,beta*h<=1; real Hilbert and signed-moduli algebraic extension. Source step repair independently accepted. No convexity, optimizer existence or companion-paper claim."
  },
  {
    key := "analysis.gradient-descent.comparator-energy",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentValue.gradient_step_energy_bound",
    upstreamDecl := "Theorem3.4 (3.1),(3.3)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "smoothness", "optimisation"],
    saldUse := "Arbitrary-comparator energy inequality and actual parent of weighted final value.",
    note := "C1 complete real Hilbert space and global curvature/upper models; h>=0,beta*h<=1, weighted alpha*h<=1. Whole-module review includes private descent; source step gap separately reviewed. No full inverse-rate or companion-paper claim."
  },
  {
    key := "analysis.gradient-descent.weighted-value",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentValue.gradient_descent_weighted_value_bound",
    upstreamDecl := "Theorem3.4 weighted proof after Lemma3.5",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "smoothness", "optimisation"],
    saldUse := "Actual Nth gradient iterate, signed comparator gap and finite geometric weights; normalized rates exercised in Tests.",
    note := "C1 complete real Hilbert space and global curvature/upper models; h>=0,beta*h<=1, weighted alpha*h<=1. Whole-module review includes private descent; source step gap separately reviewed. No full inverse-rate or companion-paper claim."
  },
  {
    key := "analysis.gradient-descent.step-contraction",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentContraction.gradient_step_contraction",
    upstreamDecl := "Theorem3.3 single-step inequality",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "smoothness", "optimisation"],
    saldUse := "Actual parent of the iterated distance theorem.",
    note := "C1 complete real inner-product space; global strong convexity and quadratic upper model. Nonnegative step and division-free beta*h<=1 explicit. Source gap independently reviewed; no logarithmic complexity or companion-paper theorem."
  },
  {
    key := "analysis.gradient-descent.distance-rate",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentContraction.gradient_descent_distance_bound",
    upstreamDecl := "Theorem3.3 iterated distance paragraph",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "smoothness", "optimisation"],
    saldUse := "Actual Nth gradient iterate around a global minimizer, with geometric and exponential distance control.",
    note := "C1 complete real inner-product space; global strong convexity and quadratic upper model. Nonnegative step and division-free beta*h<=1 explicit. Source gap independently reviewed; no logarithmic complexity or companion-paper theorem."
  },
  {
    key := "analysis.convex-smooth.bregman-gradient",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexSmoothGradient.gradient_gap_sq_le_bregman",
    upstreamDecl := "Exercise3.1 (3.4), positive reciprocal domain",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "smoothness", "optimisation"],
    saldUse := "Actual parent of cocoercivity; positive-domain reciprocal consumer.",
    note := "C1 convex global quadratic upper model on a complete real inner-product space. Positive reciprocal scope and Hilbert generalization explicit; scaled cocoercivity and Lipschitz include beta=0. Not a SALD or companion-paper theorem."
  },
  {
    key := "analysis.convex-smooth.cocoercivity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexSmoothGradient.gradient_cocoercive",
    upstreamDecl := "Exercise3.1 (3.5), including zero modulus",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "smoothness", "optimisation"],
    saldUse := "Actual parent of Lipschitz; nonexpansive gradient-step consumer.",
    note := "C1 convex global quadratic upper model on a complete real inner-product space. Positive reciprocal scope and Hilbert generalization explicit; scaled cocoercivity and Lipschitz include beta=0. Not a SALD or companion-paper theorem."
  },
  {
    key := "analysis.convex-smooth.gradient-lipschitz",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexSmoothGradient.gradient_lipschitz",
    upstreamDecl := "Exercise3.1 Cauchy-Schwarz conclusion",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "convexity", "smoothness", "optimisation"],
    saldUse := "Actual consumer of prior C1 single-sided smoothness equivalence with convexity; zero-modulus gradient constancy.",
    note := "C1 convex global quadratic upper model on a complete real inner-product space. Positive reciprocal scope and Hilbert generalization explicit; scaled cocoercivity and Lipschitz include beta=0. Not a SALD or companion-paper theorem."
  },
  {
    key := "analysis.smoothness.c1-upper-equivalence",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothnessEquivalences.upper_model_iff_gradient_upper",
    upstreamDecl := "Definition1.12 (1.7), Proposition1.13 C1 clause",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "smoothness", "Hessian", "optimisation"],
    saldUse := "Actual parent of C2 equivalence; beta0 non-Lipschitz concave boundary test",
    note := "Complete real inner-product space and signed beta explicitly generalize the source. Uses actual derivatives and signed convexity parents on -f. No convexity assumption or Lipschitz-gradient conclusion; independent source review accepted the boundary."
  },
  {
    key := "analysis.smoothness.c2-hessian-equivalence",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothnessEquivalences.upper_model_iff_fderiv2_upper",
    upstreamDecl := "Proposition1.13 C2 Hessian clause",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "smoothness", "Hessian", "optimisation"],
    saldUse := "Actual gradient-step descent consumer from Hessian upper bound; signed sharp quadratic test",
    note := "Complete real inner-product space and signed beta explicitly generalize the source. Uses actual derivatives and signed convexity parents on -f. No convexity assumption or Lipschitz-gradient conclusion; independent source review accepted the boundary."
  },
  {
    key := "analysis.calculus.segment-hessian-integral",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC2.gradient_sub_inner_eq_integral_fderiv2",
    upstreamDecl := "Proposition1.6 final Hessian FTC identity",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "CONV", "Hessian", "optimisation"],
    saldUse := "Actual parent of gradient-Hessian equivalence; reversed quadratic segment test",
    note := "Complete real inner-product-space generalization; C2 derives genuine continuous, interval-integrable Hessian pairings."
  },
  {
    key := "analysis.strong-convexity.gradient-hessian-equivalence",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC2.gradient_mono_iff_fderiv2_lower",
    upstreamDecl := "Proposition1.6 (1.5)-(1.6), derivative limit and FTC",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "CONV", "Hessian", "optimisation"],
    saldUse := "Actual parent of source C2 specialization; signed quadratic curvature test",
    note := "Signed modulus permitted. Cancels only positive directional parameter; independent derivative and source audits completed."
  },
  {
    key := "analysis.strong-convexity.c2-hessian-equivalence",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC2.strongConvexOn_iff_fderiv2_lower",
    upstreamDecl := "Proposition1.6 part2, (1.3)-(1.6)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "CONV", "Hessian", "optimisation"],
    saldUse := "Source C2 theorem; joins unchanged C1 equivalences and stationary-point growth consumer",
    note := "Whole finite-dimensional Euclidean space, nonnegative modulus, genuine C2. Completes the selected part2 boundary, not a chapter or Riemannian analogue."
  },
  {
    key := "analysis.calculus.segment-gradient-integral",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC1.sub_eq_integral_gradient",
    upstreamDecl := "Proposition 1.6 proof: segment FTC identity",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "gradient", "FTC", "shared"],
    saldUse := "Actual parent of the two-segment integral converse; reversed-segment quadratic test",
    note := "C1 derives continuous, interval-integrable gradient pairing. Complete real inner-product-space generalization; source boundary separately reviewed."
  },
  {
    key := "analysis.strong-convexity.gradient-integral-converse",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC1.strongConvexOn_univ_of_gradient_mono_integral",
    upstreamDecl := "Proposition 1.6 (1.5) to (1.3)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "CONV", "gradient", "FTC", "shared"],
    saldUse := "Actual parent of the exact C1 equivalence adapter; signed quadratic normalization tested",
    note := "Source integral proof with explicit Hilbert-space and signed-modulus generalizations. Cancels only s(1-t)>0; endpoints and integrability handled. No C2 claim."
  },
  {
    key := "analysis.strong-convexity.c1-equivalences",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC1.convexity_equivalences",
    upstreamDecl := "Proposition 1.6 part 1, (1.3)-(1.5)",
    upstreamFile := "Chewi Lectures on Optimization arXiv:2605.07006v1",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "CONV", "gradient", "equivalence", "optimisation"],
    saldUse := "Whole-space Euclidean C1 source theorem; stationary-point quadratic-growth and zero-dimension consumers",
    note := "Nonnegative modulus retained; exact source C1 equivalence independently reviewed. Reuses the shared first-order bound and new integral converse. The separate ConvexityC2 module now supplies the C2/Hessian equivalence; this entry itself covers C1 only."
  },
  {
    key := "analysis.strong-convexity.first-order-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn",
    upstreamDecl := "Strong_Convex_second_lower",
    upstreamFile := "Optlib/Convex/StronglyConvex.lean@5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "CONV", "strong-convexity", "gradient", "first-order", "shared"],
    saldUse := "Parent of gradient_inner_lower_bound_of_strongConvexOn; intended Optimization Proposition 1.6 (1.4) and sampling convex-potential adapters",
    note := "Existing ASTIS theorem admitted to Registry during PR #248 integration, not a new proof. Domain-local Hilbert-space supplied-gradient interface with arbitrary real modulus; not the whole source equivalence. Optlib mathematical provenance: Chenyi Li and Ziyu Wang, Apache-2.0; ASTIS proof uses the existing geodesic first-order lemma."
  },
  {
    key := "analysis.strong-convexity.gradient-inner-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn",
    upstreamDecl := "Strong_Convex_lower",
    upstreamFile := "Optlib/Convex/StronglyConvex.lean@5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "CONV", "strong-convexity", "gradient", "monotonicity", "shared"],
    saldUse := "Positive-modulus gradient injectivity in Tests.Shared.StrongConvexFirstOrder; intended Optimization Proposition 1.6 (1.5) and gradient-flow contraction adapters",
    note := "PR #248 by andyjm3: sum the ASTIS first-order bounds in both directions. Arbitrary real modulus; only the injectivity consumer needs positivity. No reverse implication, Hessian equivalence, flow theorem, Gibbs invariance or new conceptual transport certificate is claimed."
  },
  {
    key := "analysis.strong-convexity.of-gradient-inner-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound",
    upstreamDecl := "Lower_Strong_Convex",
    upstreamFile := "Optlib/Convex/StronglyConvex.lean@5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["CALC", "CONV", "strong-convexity", "gradient", "monotonicity", "shared"],
    saldUse := "Shared converse for optimization gradient criteria; signed quadratic and closed-domain midpoint consumers in Tests.Shared.StrongConvexGradientConverse",
    note := "Domain-local ambient-gradient criterion with arbitrary real modulus. Optlib statement provenance: Chenyi Li and Ziyu Wang, Apache-2.0. ASTIS proof uses Mathlib scalar derivative monotonicity along a segment. No complete Chewi equivalence or textbook integral proof is claimed."
  },
  {
    key := "analysis.integrability.of-real-lintegral-finite",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_ofReal_ne_top_of_integrable_nonneg",
    upstreamDecl := "lintegral_ofReal_ne_top_iff_integrable",
    upstreamFile := "Mathlib.MeasureTheory.Function.L1Space.Integrable",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "lintegral", "ENNReal", "ofReal", "nonnegative"],
    saldUse := "Chewi DENS/ANALYSIS root: turn real-valued tail integrability estimates into finite ENNReal density integrals",
    note := "Generic bridge used by Gibbs and future Renyi/Hellinger finite-integral leaves."
  },
  {
    key := "analysis.integrability.gaussian-quadratic-tail",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_mul_norm_sq",
    upstreamDecl := "GaussianFourier.integrable_cexp_neg_mul_sq_norm_add",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "Lebesgue", "Gaussian-tail", "quadratic", "finite-dimensional"],
    saldUse := "Chewi DENS/CONV root: finite-dimensional Lebesgue integrability of `exp (-a * ‖x‖^2)` for coercive Gibbs envelopes",
    note := "Mathlib-backed high-dimensional Gaussian tail integrability leaf; extracted from the complex Fourier Gaussian API."
  },
  {
    key := "analysis.integrability.shifted-gaussian-quadratic-tail",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_add_mul_norm_sq",
    upstreamDecl := "integrable_exp_neg_mul_norm_sq / Real.exp_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "Lebesgue", "Gaussian-tail", "quadratic", "shifted"],
    saldUse := "Chewi DENS/CONV root: integrability of shifted quadratic envelopes `exp (-(a‖x‖^2+b))`",
    note := "Keeps additive constants in coercive lower potentials separate from the Gaussian tail theorem."
  },
  {
    key := "analysis.integrability.centered-gaussian-quadratic-tail",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_add_mul_norm_sub_sq",
    upstreamDecl := "integrable_exp_neg_add_mul_norm_sq / Integrable.comp_sub_right",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; Mathlib.MeasureTheory.Group.Integral",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "Lebesgue", "Gaussian-tail", "quadratic", "centered"],
    saldUse := "Chewi DENS/CONV root: integrability of translated quadratic envelopes `exp (-(a‖x-m‖^2+b))`",
    note := "Fills the center-translation gap for mode-centered strongly convex Gibbs envelopes; does not claim a general coercive-tail theorem."
  },
  {
    key := "analysis.integrability.laplace-absolute-linear-tail",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.integrable_exp_neg_add_mul_abs",
    upstreamDecl := "integrableOn_exp_mul_Ioi / integrableOn_exp_mul_Iic / integrableOn_union",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.ImproperIntegrals; Mathlib.MeasureTheory.Integral.IntegrableOn",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "Lebesgue", "Laplace-tail", "absolute-value", "one-dimensional"],
    saldUse := "Chewi DENS/CONV root: integrability of one-dimensional Laplace tails `exp (-(a|x|+b))` for log-concave non-strongly-convex examples",
    note := "Splits the real line into `Iic 0` and `Ioi 0`; this is a one-dimensional nonquadratic envelope, not a general coercive theorem."
  },
  {
    key := "analysis.integrability.gaussian-quadratic-tail-normalizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_mul_norm_sq_eq",
    upstreamDecl := "GaussianFourier.integral_rexp_neg_mul_sq_norm / ofReal_integral_eq_lintegral_ofReal",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform; Mathlib.MeasureTheory.Integral.Bochner.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "Lebesgue", "Gaussian-tail", "quadratic", "normalizer"],
    saldUse := "Chewi DENS/CONV root: exact ENNReal normalizer for finite-dimensional quadratic Gaussian tails",
    note := "Stronger than finiteness; exposes the normalizing constant needed by explicit Gibbs densities."
  },
  {
    key := "analysis.integrability.shifted-gaussian-quadratic-tail-normalizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_add_mul_norm_sq_eq",
    upstreamDecl := "lintegral_exp_neg_mul_norm_sq_eq / integral_const_mul / Real.exp_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "Lebesgue", "Gaussian-tail", "quadratic", "shifted", "normalizer"],
    saldUse := "Chewi DENS/CONV root: exact ENNReal normalizer for shifted quadratic Gibbs envelopes",
    note := "Tracks additive constants explicitly instead of hiding them in finite-envelope hypotheses."
  },
  {
    key := "analysis.integrability.centered-gaussian-quadratic-tail-normalizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_add_mul_norm_sub_sq_eq",
    upstreamDecl := "lintegral_exp_neg_add_mul_norm_sq_eq / lintegral_sub_right_eq_self",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; Mathlib.MeasureTheory.Group.Integral",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "Lebesgue", "Gaussian-tail", "quadratic", "centered", "normalizer"],
    saldUse := "Chewi DENS/CONV root: exact ENNReal normalizer for translated finite-dimensional quadratic Gibbs envelopes",
    note := "Uses Lebesgue translation invariance to reuse the explicit quadratic normalizer; still only covers quadratic tails."
  },
  {
    key := "analysis.integrability.laplace-absolute-linear-tail-finite-lintegral",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_add_mul_abs_ne_top",
    upstreamDecl := "integrable_exp_neg_add_mul_abs / lintegral_ofReal_ne_top_of_integrable_nonneg",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "lintegral", "ENNReal", "Laplace-tail", "absolute-value"],
    saldUse := "Chewi DENS/CONV root: finite ENNReal integral for one-dimensional absolute-linear lower-potential envelopes",
    note := "Finite-tail theorem for Laplace-type examples; the exact one-dimensional normalizer is recorded as a separate stronger leaf."
  },
  {
    key := "analysis.integrability.laplace-absolute-linear-tail-real-normalizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.integral_exp_neg_add_mul_abs_eq",
    upstreamDecl := "integral_exp_mul_Ioi / integral_exp_mul_Iic / setIntegral_union",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.ImproperIntegrals; Mathlib.MeasureTheory.Integral.Bochner.Set",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "Lebesgue", "Laplace-tail", "absolute-value", "normalizer", "one-dimensional"],
    saldUse := "Chewi DENS/CONV root: exact real integral `∫ exp (-(a|x|+b)) = 2 exp(-b)/a` for Laplace examples",
    note := "Splits the real line into the two exponential half-lines; this is exact only in one dimension."
  },
  {
    key := "analysis.integrability.laplace-absolute-linear-tail-ennreal-normalizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_add_mul_abs_eq",
    upstreamDecl := "integral_exp_neg_add_mul_abs_eq / ofReal_integral_eq_lintegral_ofReal",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; Mathlib.MeasureTheory.Integral.Bochner.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "integrability", "lintegral", "ENNReal", "Laplace-tail", "absolute-value", "normalizer"],
    saldUse := "Chewi DENS root: exact ENNReal normalizer for normalized one-dimensional Laplace Gibbs densities",
    note := "Consumer-facing normalizer for `withDensity`; does not imply any multidimensional coercive theorem."
  },
  {
    key := "measure.gibbs-density.explicit-laplace-normalized-probability",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_exp_neg_add_mul_abs",
    upstreamDecl := "lintegral_exp_neg_add_mul_abs_eq / isProbabilityMeasure_withDensity_normalized_gibbs",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Laplace-tail", "absolute-value", "normalizer", "probability-measure"],
    saldUse := "Chewi DENS/CONV root: construct explicitly normalized one-dimensional Laplace-type Gibbs laws",
    note := "Exact-probability version of the Laplace example; base measure is Lebesgue on `ℝ`."
  },
  {
    key := "measure.gibbs-density.explicit-quadratic-normalized-probability",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sq",
    upstreamDecl := "lintegral_exp_neg_add_mul_norm_sq_eq / isProbabilityMeasure_withDensity_normalized_gibbs",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Lebesgue", "quadratic", "normalizer", "probability-measure"],
    saldUse := "Chewi DENS/CONV root: construct the explicitly normalized finite-dimensional quadratic Gibbs law",
    note := "Useful consumer-facing version for Gaussian-reference Gibbs targets and Langevin invariant-law statements."
  },
  {
    key := "measure.gibbs-density.explicit-centered-quadratic-normalized-probability",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sub_sq",
    upstreamDecl := "lintegral_exp_neg_add_mul_norm_sub_sq_eq / isProbabilityMeasure_withDensity_normalized_gibbs",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Lebesgue", "quadratic", "centered", "normalizer", "probability-measure"],
    saldUse := "Chewi DENS/CONV root: construct explicitly normalized mode-centered quadratic Gibbs laws",
    note := "Consumer-facing centered Gaussian law bridge; log-concavity geometry and later stationarity are separate leaves."
  },
  {
    key := "measure.gibbs-density.integral-finite-quadratic-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_ae_quadratic_lower_bound",
    upstreamDecl := "lintegral_exp_neg_add_mul_norm_sq_ne_top / lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "Lebesgue", "coercivity", "quadratic-lower-bound", "finite"],
    saldUse := "Chewi DENS/CONV root: prove finite Gibbs normalizer on finite-dimensional Lebesgue space from a quadratic lower bound on the potential",
    note := "First concrete Lebesgue coercivity envelope leaf; stronger nonquadratic/coercive tails remain future analysis leaves."
  },
  {
    key := "measure.gibbs-density.integral-finite-centered-quadratic-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound",
    upstreamDecl := "lintegral_exp_neg_add_mul_norm_sub_sq_ne_top / lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "Lebesgue", "coercivity", "quadratic-lower-bound", "centered", "finite"],
    saldUse := "Chewi DENS/CONV root: prove finite Gibbs normalizer from a mode-centered quadratic lower bound on the potential",
    note := "Adds the translated quadratic lower-bound case needed by strongly convex targets with nonzero minimizer; general coercive envelopes remain future work."
  },
  {
    key := "measure.gibbs-density.normalized-probability-quadratic-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_quadratic_lower_bound",
    upstreamDecl := "lintegral_gibbsDensityENNReal_ne_zero / lintegral_gibbsDensityENNReal_ne_top_of_ae_quadratic_lower_bound",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Lebesgue", "coercivity", "quadratic-lower-bound", "probability-measure"],
    saldUse := "Chewi DENS/CONV root: construct normalized finite-dimensional Lebesgue Gibbs targets from measurable potentials with quadratic lower bounds",
    note := "Turns the first concrete coercivity normalizer into the normalized target law consumed by Langevin and KL/FI branches."
  },
  {
    key := "measure.gibbs-density.normalized-probability-centered-quadratic-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_centered_quadratic_lower_bound",
    upstreamDecl := "lintegral_gibbsDensityENNReal_ne_zero / lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Lebesgue", "coercivity", "quadratic-lower-bound", "centered", "probability-measure"],
    saldUse := "Chewi DENS/CONV root: construct normalized finite-dimensional Lebesgue Gibbs targets from measurable potentials with centered quadratic lower bounds",
    note := "This is the normalized target-law handoff for strongly convex potentials after a minimizer/mode has been exposed."
  },
  {
    key := "measure.gibbs-density.integral-finite-strong-convex-minimizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer",
    upstreamDecl := "centered_quadratic_lower_bound_of_strongConvexOn_minimizer / lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity; AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "strong-convexity", "minimizer", "quadratic-lower-bound", "finite"],
    saldUse := "Chewi DENS/CONV root: prove finite Gibbs normalizer from strong convexity once a global minimizer is exposed",
    note := "Uses the compiled midpoint `k/4` lower envelope; the sharper first-order `k/2` envelope remains a separate future leaf."
  },
  {
    key := "measure.gibbs-density.normalized-probability-strong-convex-minimizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_normalized_gibbs_of_strongConvexOn_minimizer",
    upstreamDecl := "lintegral_gibbsDensityENNReal_ne_zero / lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "strong-convexity", "minimizer", "probability-measure"],
    saldUse := "Chewi DENS/CONV/SDE root: construct normalized finite-dimensional Gibbs targets for strongly convex potentials with a known minimizer",
    note := "Direct consumer-facing target-law constructor for strongly log-concave finite-dimensional Langevin branches."
  },
  {
    key := "measure.gibbs-density.integral-finite-absolute-linear-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_gibbsDensityENNReal_ne_top_of_ae_abs_linear_lower_bound",
    upstreamDecl := "lintegral_exp_neg_add_mul_abs_ne_top / lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "Laplace-tail", "absolute-linear-lower-bound", "finite"],
    saldUse := "Chewi DENS/CONV root: prove finite one-dimensional Gibbs normalizer from an absolute-linear lower bound",
    note := "First compiled nonquadratic Lebesgue Gibbs envelope; full multidimensional/general coercive envelopes remain todo-red."
  },
  {
    key := "measure.gibbs-density.normalized-probability-absolute-linear-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_abs_linear_lower_bound",
    upstreamDecl := "lintegral_gibbsDensityENNReal_ne_zero / lintegral_gibbsDensityENNReal_ne_top_of_ae_abs_linear_lower_bound",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Laplace-tail", "absolute-linear-lower-bound", "probability-measure"],
    saldUse := "Chewi DENS/CONV/SDE root: construct normalized one-dimensional Gibbs targets with Laplace-type tails",
    note := "Source-facing probability bridge for Chewi's log-concave but non-strongly-log-concave Laplace examples."
  }
]

def gaussianMemory : List LemmaMemoryEntry := [
  {
    key := "gaussian.product.coordinate-law",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.map_eval_stdGaussianPi",
    upstreamDecl := "map_eval_stdGaussianPi",
    upstreamFile := "SLT/GaussianMeasure.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "coordinate-law", "brownian-increment"],
    saldUse := "normalized scalar coordinate law in the Brownian/Ito EM backend",
    note := "ASTIS-native product-Gaussian coordinate projection theorem."
  },
  {
    key := "gaussian.product.coordinate-integrable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.integrable_eval_stdGaussianPi",
    upstreamDecl := "integrable_eval_stdGaussianPi",
    upstreamFile := "SLT/GaussianMeasure.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "integrability", "coordinate", "brownian-increment"],
    saldUse := "Brownian/Ito coordinate integrability for scalar Taylor moment and generator leaves",
    note := "Cycle 203 lower_3 ASTIS-owned port; uses Mathlib Gaussian exponential integrability and Measure.map transport."
  },
  {
    key := "gaussian.product.coordinate-square-integrable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.integrable_sq_eval_stdGaussianPi",
    upstreamDecl := "integrable_sq_eval_stdGaussianPi",
    upstreamFile := "SLT/GaussianMeasure.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "integrability", "quadratic-moment", "brownian-increment"],
    saldUse := "Brownian/Ito coordinate square integrability for polynomial moment leaves",
    note := "Cycle 203 lower_3 ASTIS-owned port; reuses the local quadratic Gaussian integrability lemma."
  },
  {
    key := "gaussian.product.linear-form-integrable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.integrable_linearForm_stdGaussianPi",
    upstreamDecl := "finite-sum closure of integrable_eval_stdGaussianPi",
    upstreamFile := "Mathlib.MeasureTheory.Function.L1Space.Integrable; ASTIS Gaussian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "product-gaussian", "linear-form", "integrability", "brownian-increment", "Esscher"],
    saldUse := "finite-dimensional Gaussian linear-function integrability before MGF, Esscher tilt, and Brownian increment packaging",
    note := "Small ASTIS-owned closure lemma; keeps product-Gaussian linear forms separate from exponential tilt/MGF work."
  },
  {
    key := "gaussian.product.coordinate-mean-zero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.integral_eval_stdGaussianPi",
    upstreamDecl := "integral_eval_stdGaussianPi",
    upstreamFile := "SLT/GaussianMeasure.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "mean", "coordinate", "brownian-increment"],
    saldUse := "coordinate mean-zero rewrite for Brownian/Ito scalar Taylor moment leaves",
    note := "Cycle 203 lower_3 ASTIS-owned port; combines product-coordinate law with the local centered Gaussian mean."
  },
  {
    key := "gaussian.product.linear-form-mean-zero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.integral_linearForm_stdGaussianPi",
    upstreamDecl := "finite-sum closure of integral_eval_stdGaussianPi",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Basic; ASTIS Gaussian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "product-gaussian", "linear-form", "mean-zero", "brownian-increment", "Esscher"],
    saldUse := "zero-mean finite-dimensional Gaussian linear forms before centered tilt/MGF and generator algebra",
    note := "Compiled finite-sum closure of centered coordinate means; full Gaussian Esscher density identity remains a separate target."
  },
  {
    key := "gaussian.product.linear-form-mgf",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.integral_exp_linearForm_stdGaussianPi",
    upstreamDecl := "mgf_gaussianReal / integral_fintype_prod_eq_prod",
    upstreamFile := "Mathlib.Probability.Distributions.Gaussian.Real; Mathlib.MeasureTheory.Integral.Pi; external AST GaussianMGF.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "product-gaussian", "linear-form", "MGF", "Esscher", "Chewi"],
    saldUse := "Chewi GAUSS root: compute finite product-Gaussian exponential moments for tilt normalizers and Brownian increment laws",
    note := "ASTIS-owned finite-product MGF leaf distilled from the external GaussianMGF proof route; full density shift remains separate."
  },
  {
    key := "gaussian.product.centered-esscher-normalizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.integral_exp_centered_linearForm_stdGaussianPi",
    upstreamDecl := "integral_exp_linearForm_stdGaussianPi plus elementary exponential algebra",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "product-gaussian", "Esscher", "tilt", "normalization", "Chewi"],
    saldUse := "Chewi GAUSS root: certify the centered exponential tilt has mass one before proving the shifted density/change-of-measure identity",
    note := "This is the compiled normalizer half of finite-dimensional Esscher; it does not yet prove the withDensity shifted-Gaussian identity."
  },
  {
    key := "gaussian.scalar.esscher-shift-density",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.gaussianReal_withDensity_exp_shift",
    upstreamDecl := "gaussianReal_of_var_ne_zero / gaussianPDFReal algebra",
    upstreamFile := "Mathlib.Probability.Distributions.Gaussian.Real; external AST GaussianShift.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "Esscher", "withDensity", "density-shift", "Chewi"],
    saldUse := "Chewi GAUSS root: one-dimensional Gaussian exponential tilt shifts the mean",
    note := "ASTIS-owned scalar density identity; product versions consume the finite-pi withDensity decomposition leaf."
  },
  {
    key := "gaussian.product.esscher-shift-density",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi_withDensity_exp_shift",
    upstreamDecl := "gaussianReal_withDensity_exp_shift / pi_withDensity_prod",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian; external AST GaussianShift.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "product-gaussian", "Esscher", "withDensity", "density-shift", "Chewi"],
    saldUse := "Chewi GAUSS root: finite product-Gaussian centered exponential tilt equals the shifted product Gaussian law",
    note := "Completes the shifted-density half of finite-dimensional Esscher; integral change-of-measure and Euclidean/path-space packaging remain separate."
  },
  {
    key := "gaussian.product.esscher-change-of-measure",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi_shift_integral",
    upstreamDecl := "stdGaussianPi_withDensity_exp_shift / integral_withDensity_eq_integral_toReal_smul",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap; external AST GaussianShift.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "product-gaussian", "Esscher", "change-of-measure", "Girsanov", "Chewi"],
    saldUse := "Chewi GAUSS/PATH root: rewrite integrals under finite shifted product Gaussians as centered product-Gaussian weighted integrals",
    note := "Finite-dimensional product-Gaussian change-of-measure is compiled; EuclideanSpace pushforward, stdGaussian, and path-space/Girsanov packaging are separate entries."
  },
  {
    key := "gaussian.euclidean.pushforward-esscher-change-of-measure",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussianPi_shift_integral_map_toLp",
    upstreamDecl := "pi_gaussianReal_shift_integral / integral_map / WithLp.toLp",
    upstreamFile := "Mathlib.Probability.Distributions.Gaussian.Multivariate; AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "EuclideanSpace", "product-gaussian", "Esscher", "change-of-measure", "Girsanov", "Chewi"],
    saldUse := "Chewi GAUSS/PATH root: transport finite shifted product-Gaussian change-of-measure through the EuclideanSpace `WithLp.toLp 2` interface",
    note := "Compiled coordinate-exponent pushforward bridge; canonical `stdGaussian` inner-product form and path-space/Girsanov packaging are separate entries."
  },
  {
    key := "gaussian.euclidean.stdGaussian-esscher-change-of-measure",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.stdGaussian_shift_integral_map_toLp",
    upstreamDecl := "stdGaussianPi_shift_integral_map_toLp / map_pi_eq_stdGaussian / EuclideanSpace inner and norm coordinates",
    upstreamFile := "Mathlib.Probability.Distributions.Gaussian.Multivariate; Mathlib.Analysis.InnerProductSpace.PiL2",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "stdGaussian", "EuclideanSpace", "Esscher", "change-of-measure", "Girsanov", "Chewi"],
    saldUse := "Chewi GAUSS/PATH root: express finite-dimensional Gaussian Esscher change-of-measure against Mathlib `stdGaussian` with inner-product/norm exponent",
    note := "Compiled canonical finite-dimensional Hilbert-space form; Brownian/path-space Girsanov packaging remains separate."
  },
  {
    key := "gaussian.unit-variance.nnreal",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.nnrealVarianceOneOfGaussianRealUnitLaw",
    upstreamDecl := "variance_id_gaussianReal",
    upstreamFile := "Mathlib.Probability.Distributions.Gaussian.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "variance", "NNReal"],
    saldUse := "turn scalar Gaussian law and variance-field definition into normalized variance one",
    note := "Uses Mathlib Gaussian variance locally; no SLT import."
  },
  {
    key := "gaussian.quadratic-bound-integrable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian.integrable_const_mul_sq_gaussianReal_zero",
    upstreamDecl := "integrable_exp_mul_gaussianReal / integrable_pow_of_integrable_exp_mul",
    upstreamFile := "Mathlib.Probability.Distributions.Gaussian.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["gaussian", "integrability", "quadratic-bound", "brownian-increment"],
    saldUse := "supply normalized-remainder bound integrability once the source identifies remainderBound as C * z^2",
    note := "Cycle 196 lower_3 ASTIS-owned Gaussian quadratic integrability support; no SLT import."
  }
]

def taylorMemory : List LemmaMemoryEntry := [
  {
    key := "taylor.hessian.source-field-to-opnorm",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Taylor.hessianOpNormOfSourceHessianField",
    upstreamDecl := "deriv2_bounded_of_compactlySupported",
    upstreamFile := "SLT/GaussianPoincare/TaylorBound.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["taylor", "hessian", "source-contract"],
    saldUse := "convert source-supplied selected-test Hessian representative into downstream Hessian operator-norm bound",
    note := "Does not prove that the SALD source supplies the Hessian field; it only packages the local bridge once supplied."
  },
  {
    key := "taylor.fderiv-hessian-to-iterated",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Taylor.iteratedFDerivTwoOpNormOfFDerivFDerivOpNorm",
    upstreamDecl := "taylor_order_one / TaylorBound proof idiom",
    upstreamFile := "SLT/GaussianPoincare/TaylorBound.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["taylor", "iteratedFDeriv", "hessian"],
    saldUse := "feed selected-line Taylor bounds from a Hessian operator-norm field",
    note := "ASTIS-owned Mathlib bridge."
  },
  {
    key := "brownian.quadratic-variation-normalization",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Taylor.quadraticVariationNormalizationOfCoeffDefAndVarianceOne",
    upstreamDecl := "not upstream; extracted from SALD local proof needs",
    upstreamFile := "ASTIS/SALD cycles 174-176",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["brownian", "ito", "quadratic-variation", "normalization"],
    saldUse := "assemble quadratic coefficient and variance-one fields without re-assuming the downstream normalization",
    note := "Pure algebraic bridge made reusable for later SDE papers."
  }
]

def calculusMemory : List LemmaMemoryEntry := [
  {
    key := "analysis.calculus.smooth-unit-cutoff-eq-smoothTransition",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_smoothTransition",
    upstreamDecl := "GaussianSobolev.smoothCutoff_eq_smoothTransition",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.Calculus.BumpFunction.InnerProduct",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "smoothTransition", "unit-scale"],
    saldUse := "log-concave sampling Ch.1 cutoff root: expose the unit cutoff through Mathlib's smooth-transition formula",
    note := "Formula leaf only. It does not assert a scaled family, derivative bounds, tail passage, weighted IBP, or invariant law."
  },
  {
    key := "analysis.calculus.smooth-unit-cutoff-contDiff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_contDiff",
    upstreamDecl := "GaussianSobolev.smoothCutoff_contDiff",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.Calculus.BumpFunction.InnerProduct",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "ContDiff", "unit-scale"],
    saldUse := "log-concave sampling Ch.1 cutoff root: global smoothness of the reusable one-dimensional unit cutoff",
    note := "Smoothness leaf only. It gives no derivative-size estimate or integration theorem."
  },
  {
    key := "analysis.calculus.smooth-unit-cutoff-one-of-abs-le-one",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_one_of_abs_le_one",
    upstreamDecl := "GaussianSobolev.smoothCutoff_eq_one_of_le",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.SpecialFunctions.SmoothTransition",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "plateau", "unit-scale"],
    saldUse := "log-concave sampling Ch.1 cutoff root: identify the unit cutoff plateau on the closed unit interval",
    note := "Unit-scale value leaf only; no scaled derivative or tail claim."
  },
  {
    key := "analysis.calculus.smooth-unit-cutoff-zero-of-two-le-abs",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_eq_zero_of_two_le_abs",
    upstreamDecl := "GaussianSobolev.smoothCutoff_eq_zero_of_ge",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.SpecialFunctions.SmoothTransition",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "support", "unit-scale"],
    saldUse := "log-concave sampling Ch.1 cutoff root: the unit cutoff vanishes beyond radius two",
    note := "Pointwise vanishing leaf only; compactness and topological support are separate leaves."
  },
  {
    key := "analysis.calculus.smooth-unit-cutoff-mem-Icc",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_mem_Icc",
    upstreamDecl := "ContDiffBumpBase.mem_Icc",
    upstreamFile := "Mathlib.Analysis.Calculus.BumpFunction.InnerProduct",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "range", "unit-scale"],
    saldUse := "log-concave sampling Ch.1 cutoff root: pointwise [0,1] range of the unit cutoff",
    note := "Range leaf only; it does not provide monotonicity or derivative bounds."
  },
  {
    key := "analysis.calculus.smooth-unit-cutoff-deriv-bounded",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_deriv_bounded",
    upstreamDecl := "GaussianSobolev.smoothCutoff_deriv_bounded",
    upstreamFile := "SLT/GaussianSobolevDense/Cutoff.lean@d0f506f; Mathlib.Analysis.Calculus.ContDiff.Deriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "deriv", "uniform-bound", "unit-scale"],
    saldUse := "log-concave sampling Ch.1 cutoff root: choose one positive derivative bound before introducing the exhaustion scale",
    note := "One-dimensional compact-support bound. It supplies the scale-independent constant used by the radial first-derivative leaf."
  },
  {
    key := "analysis.calculus.smooth-unit-cutoff-second-deriv-continuous",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_secondDeriv_continuous",
    upstreamDecl := "ContDiff.iterate_deriv'",
    upstreamFile := "SLT/GaussianPoincare/TaylorBound.lean@d0f506f; Mathlib.Analysis.Calculus.ContDiff",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "second-derivative", "continuity", "SLT-port"],
    saldUse := "log-concave sampling Ch.1 second-order cutoff root: continuity input for a unit-scale Hessian bound",
    note := "ASTIS-owned adaptation of the audited SLT C_c^2 second-derivative continuity leaf."
  },
  {
    key := "analysis.calculus.smooth-unit-cutoff-second-deriv-compact-support",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_secondDeriv_hasCompactSupport",
    upstreamDecl := "HasCompactSupport.deriv",
    upstreamFile := "SLT/GaussianPoincare/TaylorBound.lean@d0f506f; Mathlib.Topology.Algebra.Support",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "second-derivative", "compact-support", "SLT-port"],
    saldUse := "log-concave sampling Ch.1 second-order cutoff root: compact-support input for a global derivative bound",
    note := "The fixed unit cutoff is differentiated twice; no radial scaling or Hessian estimate is claimed here."
  },
  {
    key := "analysis.calculus.smooth-unit-cutoff-second-deriv-bounded",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.smoothUnitCutoff_secondDeriv_bounded",
    upstreamDecl := "HasCompactSupport.exists_bound_of_continuous",
    upstreamFile := "SLT/GaussianPoincare/TaylorBound.lean@d0f506f; Mathlib.Topology.Algebra.Support",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "second-derivative", "uniform-bound", "SLT-port"],
    saldUse := "log-concave sampling Ch.1: choose the unit-scale constant before proving O(R^-2) radial Hessian/Laplacian bounds",
    note := "Compiled unit-scale bound only. The chain rule and radial Hessian/Laplacian scaling remain a separate red leaf."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-one-of-norm-le",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_eq_one_of_norm_le",
    upstreamDecl := "GaussianSobolev.smoothCutoffR_eq_one_of_norm_le",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "plateau", "closed-ball"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: the scale-R radial cutoff equals one on the radius-R closed ball",
    note := "Plateau-value leaf only. Uniform derivative and tail estimates remain red."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-zero-of-two-mul-le-norm",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_eq_zero_of_two_mul_le_norm",
    upstreamDecl := "GaussianSobolev.smoothCutoffR_eq_zero_of_norm_ge",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "support", "closed-ball"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: the scale-R radial cutoff vanishes at norm at least 2R",
    note := "Pointwise vanishing leaf only. It does not identify support equality."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-mem-Icc",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_mem_Icc",
    upstreamDecl := "GaussianSobolev.smoothCutoffR_nonneg plus smoothCutoffR_le_one",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "range"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: every radial cutoff value lies in [0,1]",
    note := "Range leaf only; scale positivity is not needed for this statement."
  },
  {
    key := "analysis.calculus.fderiv-norm-div-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.fderiv_norm_div_bound",
    upstreamDecl := "GaussianSobolev.fderiv_norm_div_bound",
    upstreamFile := "SLT/GaussianSobolevDense/Cutoff.lean@d0f506f; Mathlib.Analysis.Calculus.Deriv.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "fderiv", "Lipschitz", "scale"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: the totalized derivative of x maps to norm x divided by R has operator norm at most 1/R",
    note := "Valid on real normed spaces, including the origin through Mathlib's totalized fderiv. Genuine norm differentiability at the origin is not asserted."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-contDiff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_contDiff",
    upstreamDecl := "GaussianSobolev.smoothCutoffR_contDiff",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.Calculus.BumpFunction.InnerProduct",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "ContDiff", "inner-product-space"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: smoothness of the positive-scale radial cutoff on real inner-product spaces",
    note := "Requires an inner-product norm; no claim is made for arbitrary nonsmooth norms or for derivative magnitude."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-fderiv-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_fderiv_bound",
    upstreamDecl := "GaussianSobolev.smoothCutoffR_fderiv_bound, with scale-uniform quantifier order",
    upstreamFile := "SLT/GaussianSobolevDense/Cutoff.lean@d0f506f; Mathlib.Analysis.Calculus.FDeriv.Comp",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "fderiv", "O-R-inverse", "inner-product-space"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: one constant controls the first derivative of every positive-scale radial cutoff by C/R",
    note := "The existential constant precedes the radius quantifier. Hessian, Laplacian, dominated-tail, weighted-IBP, and invariance leaves remain separate."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-iterated-fderiv-two-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_iteratedFDeriv_two_bound",
    upstreamDecl := "ContinuousLinearMap.iteratedFDeriv_comp_right; HasCompactSupport.iteratedFDeriv; ContinuousMultilinearMap.norm_compContinuousLinearMap_le",
    upstreamFile := "Mathlib.Analysis.Calculus.ContDiff.{Bounds,FTaylorSeries}; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "iteratedFDeriv", "second-order", "O-R-inverse-squared"],
    saldUse := "log-concave sampling Ch.1 second-order exhaustion branch: one constant controls the second iterated Frechet derivative at every positive scale by C/R^2",
    note := "The unit-scale derivative field is bounded by continuity and compact support, then transported by exact linear dilation. Laplacian trace and any integral consumer remain separate."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-fderiv-zero-of-two-mul-le-norm",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_fderiv_eq_zero_of_two_mul_le_norm",
    upstreamDecl := "IsLocalMin.fderiv_eq_zero; radialSmoothCutoff_eq_zero_of_two_mul_le_norm; radialSmoothCutoff_mem_Icc",
    upstreamFile := "Mathlib.Analysis.Calculus.LocalExtr.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "fderiv", "derivative-support", "outer-radius", "boundary"],
    saldUse := "log-concave sampling Ch.1 cutoff exhaustion: the totalized first derivative vanishes on the closed outer region with norm at least 2R",
    note := "The boundary case uses the global-minimum characterization and Mathlib's totalized fderiv. It does not assert genuine differentiability of an arbitrary norm there, an integral tail limit, weighted IBP, or invariance."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-support-subset-closedBall",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_support_subset_closedBall",
    upstreamDecl := "GaussianSobolev.smoothCutoffR_support_subset",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "Function.support", "closed-ball"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: plain support of the scale-R cutoff is contained in the radius-2R closed ball",
    note := "Support containment, not equality. Box support and boundary-face handoffs remain separate."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-tsupport-subset-closedBall",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_tsupport_subset_closedBall",
    upstreamDecl := "radialSmoothCutoff_support_subset_closedBall plus closure_minimal",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "tsupport", "closed-ball"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: topological support remains inside the radius-2R closed ball",
    note := "Topological-support containment only; it does not claim a box-shaped tsupport or support equality."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-hasCompactSupport",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_hasCompactSupport",
    upstreamDecl := "GaussianSobolev.smoothCutoffR_hasCompactSupport",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "HasCompactSupport", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: positive-scale radial cutoffs have compact support in finite dimension",
    note := "Compact-support leaf only. No derivative, domination, integration, or invariant-law conclusion."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-tendsto-one",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.radialSmoothCutoff_tendsto_one",
    upstreamDecl := "GaussianSobolev.smoothCutoffR_tendsto_one",
    upstreamFile := "SLT/GaussianSobolevDense/Defs.lean@d0f506f",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "exhaustion", "Tendsto"],
    saldUse := "log-concave sampling Ch.1 exhaustion base: at each fixed point the radial cutoff is eventually one as R tends to infinity",
    note := "Pointwise eventual constancy only. It does not prove dominated convergence for cutoff errors or derivative terms."
  },
  {
    key := "analysis.calculus.exists-contDiff-eq-one-tsupport-subset",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff.exists_contDiff_eq_one_tsupport_subset",
    upstreamDecl := "exists_compact_between; IsOpen.exists_contDiff_support_eq; IsCompact.exists_forall_le'; Real.smoothTransition",
    upstreamFile := "Mathlib.Topology.Compactness.LocallyCompact; Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; Mathlib.Topology.Order.Compact; Mathlib.Analysis.SpecialFunctions.SmoothTransition",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "plateau", "compact", "open-set", "tsupport", "ContDiff"],
    saldUse := "log-concave sampling Ch.1 cutoff root: a compact set inside an open finite-dimensional neighborhood admits a smooth [0,1] plateau with compact support inside that neighborhood",
    note := "Generic compact-in-open plateau leaf. It supplies no exhausting sequence, derivative bounds, tail passage, weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.exists-contDiff-cutoff-eq-one-on-Icc-tsupport-subset-outer-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_cutoff_eq_one_on_Icc_tsupport_subset_outer_univ_pi_Ioo",
    upstreamDecl := "Cutoff.exists_contDiff_eq_one_tsupport_subset plus Icc_subset_univ_pi_Ioo_of_strict_bounds",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "cutoff", "plateau", "closed-box", "open-box", "tsupport", "ContDiff"],
    saldUse := "log-concave sampling Ch.1 finite-box route: one smooth compactly supported cutoff equals one on the entire inner closed Pi-box and is topologically supported in the outer open Pi-box",
    note := "One-cutoff box specialization only. Exhausting families with derivative bookkeeping, tail limits, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, and KL/FI remain red."
  },
  {
    key := "analysis.calculus.gradient-exp-neg-potential-chain-rule",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.hasGradientAt_expNegPotential_of_hasGradientAt",
    upstreamDecl := "HasGradientAt.hasFDerivAt / HasFDerivAt.neg / HasFDerivAt.exp",
    upstreamFile := "Mathlib.Analysis.Calculus.Gradient.Basic; Mathlib.Analysis.SpecialFunctions.ExpDeriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "gradient", "chain-rule", "exp-neg-potential"],
    saldUse := "Chewi SDE/DENS root: turn a supplied potential gradient `∇V` into the Gibbs-weight gradient `∇ exp(-V) = -exp(-V) • ∇V` before finite-coordinate Langevin divergence algebra",
    note := "Pointwise gradient chain-rule leaf only. It does not prove weighted divergence, product rules for `rho ∇f`, integration by parts, boundary decay, stationarity, reversibility, or invariant Gibbs law."
  },
  {
    key := "analysis.calculus.gradient-exp-neg-potential-mathlib-gradient-from-hasGradientAt",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_eq_of_hasGradientAt",
    upstreamDecl := "HasGradientAt.gradient plus hasGradientAt_expNegPotential_of_hasGradientAt",
    upstreamFile := "Mathlib.Analysis.Calculus.Gradient.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "gradient", "HasGradientAt", "Mathlib-gradient", "exp-neg-potential"],
    saldUse := "Chewi SDE/DENS root: rewrite Mathlib's total `gradient (exp(-V)) x` from a supplied `HasGradientAt V gradV x`, keeping the potential-gradient representative explicit",
    note := "Pointwise Mathlib-gradient selection leaf only. It uses uniqueness of gradients after the local chain rule; divergence, product rule, IBP, generator domains, invariant law, reversibility, and KL/FI remain red."
  },
  {
    key := "analysis.calculus.gradient-exp-neg-potential-coordinate-from-hasGradientAt",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_coordinate_eq_of_hasGradientAt",
    upstreamDecl := "gradient_expNegPotential_eq_of_hasGradientAt plus EuclideanSpace coordinate evaluation of scalar multiplication",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "gradient", "HasGradientAt", "EuclideanSpace", "coordinate"],
    saldUse := "Chewi SDE/DENS root: coordinate Gibbs-weight chain-rule equality from a supplied potential gradient representative before finite Euclidean weighted-divergence algebra",
    note := "Coordinate Mathlib-gradient display only. It does not prove coordinate product rules, the a.e. bridge or box-integrability assumptions needed by the compiled box divergence wrapper, Laplacian identities, IBP, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.gradient-exp-neg-potential-mathlib-gradient",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_eq_of_differentiableAt",
    upstreamDecl := "HasGradientAt.gradient plus hasGradientAt_expNegPotential_of_hasGradientAt",
    upstreamFile := "Mathlib.Analysis.Calculus.Gradient.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "gradient", "DifferentiableAt", "Mathlib-gradient", "exp-neg-potential"],
    saldUse := "Chewi SDE/DENS root: turn `DifferentiableAt ℝ V x` into the Mathlib total-gradient identity `gradient (exp(-V)) x = -exp(-V x) • gradient V x` before weighted-divergence handoffs",
    note := "Pointwise Mathlib-gradient display only. It removes the separate Gibbs-weight chain-rule hypothesis when `V` is differentiable at the point; divergence, product rule, IBP, generator domains, invariant law, reversibility, and KL/FI remain red."
  },
  {
    key := "analysis.calculus.gradient-exp-neg-potential-coordinate",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_coordinate_eq_of_differentiableAt",
    upstreamDecl := "gradient_expNegPotential_eq_of_differentiableAt plus EuclideanSpace coordinate evaluation of scalar multiplication",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "gradient", "EuclideanSpace", "coordinate", "DifferentiableAt"],
    saldUse := "Chewi SDE/DENS root: supply the coordinate Gibbs-weight chain-rule equality used by finite Euclidean Langevin weighted-divergence handoffs",
    note := "Coordinate chain-rule display only. It does not prove coordinate product rules, the a.e. bridge or box-integrability assumptions needed by the compiled box divergence wrapper, Laplacian identities, IBP, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.continuous-gradient-of-contDiff-one",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one",
    upstreamDecl := "ContDiff.continuous_fderiv plus the continuous inverse Riesz equivalence for `gradient`",
    upstreamFile := "Mathlib.Analysis.Calculus.ContDiff.Basic; Mathlib.Analysis.Calculus.Gradient.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "gradient", "ContDiff", "Continuous", "regularity", "test-function"],
    saldUse := "Chewi Ch.1 Langevin root: derive continuity of Mathlib's total gradient from global `C¹` regularity before the scalar generator display on boxes",
    note := "Global `C¹` to continuous Mathlib gradient only. It does not assert a closed-box `ContDiffOn` variant, field differentiability for `rho * fderiv f eᵢ`, weighted IBP, boundary cancellation, domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.gradient-coordinate-unit-line-derivative",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.hasGradientAt_coordinateUnit_hasLineDerivAt",
    upstreamDecl := "HasGradientAt.hasFDerivAt / HasFDerivAt.hasLineDerivAt / InnerProductSpace.toDual_apply_apply",
    upstreamFile := "Mathlib.Analysis.Calculus.Gradient.Basic; Mathlib.Analysis.Calculus.LineDeriv.Basic; AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "gradient", "line-derivative", "EuclideanSpace", "coordinate", "finite-dimensional"],
    saldUse := "Chewi SDE/ANALYSIS root: identify a coordinate-unit line derivative with the corresponding coordinate of a supplied Mathlib gradient before finite-coordinate Langevin generator algebra",
    note := "Pointwise gradient-coordinate bridge only. It does not prove divergence, weighted product rules, Laplacian identities, IBP, boundary decay, stationarity, reversibility, or invariant Gibbs law."
  },
  {
    key := "analysis.calculus.fderiv-apply-eq-inner-of-hasGradientAt",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_of_hasGradientAt",
    upstreamDecl := "HasGradientAt.hasFDerivAt plus HasFDerivAt.unique and InnerProductSpace.toDual_apply_apply",
    upstreamFile := "Mathlib.Analysis.Calculus.Gradient.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "gradient", "fderiv", "inner-product", "HasGradientAt", "pointwise"],
    saldUse := "Chewi Ch.1 calculus root: rewrite a pointwise Frechet derivative application through a supplied Mathlib gradient representative before coordinate Langevin displays",
    note := "Pointwise fderiv/gradient bridge only. It does not choose coordinate bases, define divergence, prove product rules, IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.fderiv-apply-eq-inner-gradient",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt",
    upstreamDecl := "DifferentiableAt.hasGradientAt plus fderiv_apply_eq_inner_of_hasGradientAt",
    upstreamFile := "Mathlib.Analysis.Calculus.Gradient.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "gradient", "fderiv", "inner-product", "DifferentiableAt", "pointwise"],
    saldUse := "Chewi Ch.1 calculus root: under `DifferentiableAt ℝ f x`, rewrite `fderiv ℝ f x v` as `inner ℝ (gradient f x) v`",
    note := "Pointwise total-gradient display only. It does not prove global smoothness, divergence, coordinate sums, IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.fderiv-coordinate-eq-gradient-coordinate",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt",
    upstreamDecl := "fderiv_apply_eq_inner_gradient_of_differentiableAt plus EuclideanSpace.inner_basisFun_real",
    upstreamFile := "Mathlib.Analysis.Calculus.Gradient.Basic; Mathlib.Analysis.InnerProductSpace.PiL2; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "gradient", "fderiv", "EuclideanSpace", "coordinate", "DifferentiableAt"],
    saldUse := "Chewi Ch.1 Langevin root: discharge the local bridge `fderiv ℝ f x eᵢ = (gradient f x) i` used by finite-coordinate generator displays",
    note := "Pointwise coordinate bridge only. It requires `DifferentiableAt ℝ f x`; differentiability of `fun y => fderiv ℝ f y` alone is not a substitute. It does not define divergence, prove that a coordinate sum is divergence, prove IBP/no-boundary terms, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.coordinate-divergence-sum-lineDeriv",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_lineDeriv",
    upstreamDecl := "definition of coordinateDivergence",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; Mathlib.Analysis.BoxIntegral.DivergenceTheorem pointwise summand shape",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "lineDeriv", "EuclideanSpace", "pointwise"],
    saldUse := "Chewi Ch.1 calculus root: name the finite-dimensional coordinate divergence convention `sum_i lineDeriv F_i x e_i` before Langevin divergence-form displays",
    note := "Definition/unfolding leaf only. It is pointwise and coordinate-dependent; it does not prove a divergence theorem, integration by parts, boundary cancellation, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.coordinate-divergence-fderiv-trace-sum",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt",
    upstreamDecl := "HasFDerivAt.hasLineDerivAt plus PiLp.proj component projection",
    upstreamFile := "Mathlib.Analysis.Calculus.LineDeriv.Basic; Mathlib.Analysis.Normed.Lp.PiLp; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "fderiv", "trace-style", "EuclideanSpace", "pointwise"],
    saldUse := "Chewi Ch.1 calculus root: align ASTIS coordinate divergence with the Mathlib divergence-theorem summand shape `sum_i F' e_i i` under `HasFDerivAt F F' x`",
    note := "Pointwise Frechet-derivative expansion only. It does not assert coordinate independence, prove the Mathlib divergence theorem, instantiate box/all-space integrability, prove IBP/no-boundary terms, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.coordinate-divergence-fderiv-default-summand",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt",
    upstreamDecl := "coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt plus DifferentiableAt.hasFDerivAt",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; Mathlib.MeasureTheory.Integral.DivergenceTheorem summand shape",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "fderiv", "DifferentiableAt", "EuclideanSpace", "pointwise"],
    saldUse := "Chewi Ch.1 calculus root: rewrite ASTIS `coordinateDivergence F x` to the exact default Mathlib `fderiv ℝ F x` summand shape before any integral divergence-theorem instantiation",
    note := "Pointwise bridge to the Bochner divergence theorem integrand only. It does not prove integrability on boxes, face terms, no-boundary cancellation, weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.withlp-continuousLinearEquiv-euclidean-single",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.continuousLinearEquiv_apply_euclideanSpace_single",
    upstreamDecl := "PiLp.continuousLinearEquiv_apply",
    upstreamFile := "Mathlib.Analysis.Calculus.FDeriv.WithLp; Mathlib.Analysis.Normed.Lp.PiLp",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "WithLp", "PiLp", "EuclideanSpace", "coordinate-unit"],
    saldUse := "Chewi Ch.1 calculus root: identify the Euclidean coordinate unit with the Pi-space `Pi.single` unit before transporting derivative traces through `WithLp`",
    note := "Representation bridge only. It does not prove differentiability, divergence, a.e. equality, integrability, IBP, boundary cancellation, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-comp-toLp-hasFDerivAt",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.hasFDerivAt_radialSmoothCutoff_comp_toLp",
    upstreamDecl := "PiLp.hasFDerivAt_toLp; HasFDerivAt.comp; radialSmoothCutoff_contDiff",
    upstreamFile := "Mathlib.Analysis.Calculus.FDeriv.WithLp; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "cutoff", "WithLp", "PiLp", "EuclideanSpace", "HasFDerivAt", "chain-rule"],
    saldUse := "Chewi Ch.1 cutoff-smul route: expose the Euclidean radial-cutoff derivative as a raw finite-Pi-space HasFDerivAt producer",
    note := "Pointwise derivative transport only. It proves no support, measurability, integrability, tail convergence, IBP, generator-domain, or invariant-law statement."
  },
  {
    key := "analysis.calculus.pilp-radial-cutoff-gradient-L1-tendsto-zero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.tendsto_integral_norm_fderiv_radialSmoothCutoff_comp_toLp_apply",
    upstreamDecl := "radialSmoothCutoff_fderiv_bound; hasFDerivAt_radialSmoothCutoff_comp_toLp; MeasureTheory.tendsto_integral_filter_of_dominated_convergence",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.{Cutoff,Divergence}; Mathlib.MeasureTheory.Integral.DominatedConvergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "cutoff", "WithLp", "PiLp", "L1", "Integrable", "dominated-convergence"],
    saldUse := "Chewi Ch.1 cutoff-smul route: make the cutoff-gradient cross term vanish in L1 for every integrable finite-Pi vector field",
    note := "Generic cutoff-gradient L1 limit only. The PiLp inverse-equivalence operator norm is retained explicitly; the theorem proves neither Gibbs/source-field integrability, main-term convergence, Gibbs tails, whole-space IBP, generator domains, nor invariant law."
  },
  {
    key := "analysis.calculus.pilp-radial-cutoff-main-integral-tendsto",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.tendsto_integral_radialSmoothCutoff_comp_toLp_smul",
    upstreamDecl := "radialSmoothCutoff_contDiff; radialSmoothCutoff_mem_Icc; radialSmoothCutoff_tendsto_one; MeasureTheory.tendsto_integral_filter_of_dominated_convergence",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.{Cutoff,Divergence}; Mathlib.MeasureTheory.Integral.DominatedConvergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "cutoff", "WithLp", "PiLp", "Integrable", "Bochner-integral", "dominated-convergence"],
    saldUse := "Chewi Ch.1 cutoff-smul route: pass the main integrable field through the PiLp-wrapped radial cutoff by dominated convergence",
    note := "Generic cutoff main-term limit only. It assumes the source field is Integrable and proves neither integrability of the concrete Langevin generator display, Gibbs tails, the cutoff-gradient cross term, whole-space IBP, generator domains, nor invariant law."
  },
  {
    key := "analysis.calculus.pilp-integrable-field-norm-tail-tendsto-zero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.tendsto_setIntegral_norm_norm_ge_comp_toLp",
    upstreamDecl := "MeasureTheory.tendsto_setIntegral_of_antitone",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Set; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "tail", "WithLp", "PiLp", "L1", "Integrable", "set-integral"],
    saldUse := "Chewi Ch.1 cutoff route: make the L1 norm of any integrable raw-Pi field vanish outside expanding Euclidean balls",
    note := "Generic antitone-set tail theorem only. It has no Gibbs, generator, weighted-IBP, generator-domain, stationarity, invariance, reversibility, or KL/FI semantics."
  },
  {
    key := "analysis.calculus.compact-support-whole-space-coordinate-divergence-zero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_wrapped_eq_zero_of_contDiff_of_hasCompactSupport",
    upstreamDecl := "MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable; HasCompactSupport; Bornology.IsBounded.subset_ball_lt; setIntegral_eq_integral_of_forall_compl_eq_zero",
    upstreamFile := "Mathlib.MeasureTheory.Integral.DivergenceTheorem; Mathlib.Topology.MetricSpace.Bounded; Mathlib.MeasureTheory.Integral.Bochner.Set; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "whole-space", "compact-support", "ContDiff", "zero-boundary", "PiLp"],
    saldUse := "Chewi Ch.1 weighted-IBP root: integrate the divergence of any compactly supported C1 finite-dimensional vector field over the whole space and obtain zero",
    note := "Reusable analytic no-boundary theorem. It encloses the compact support in a strict Pi-box and invokes the finite-box divergence theorem; it contains no Gibbs, generator-domain, semigroup, invariant-law, reversibility, or KL/FI semantics."
  },
  {
    key := "analysis.calculus.sum-smulRight-apply-pi-single-eq-apply",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.sum_smulRight_apply_pi_single_eq_apply",
    upstreamDecl := "pi_eq_sum_univ'; ContinuousLinearMap.map_sum; ContinuousLinearMap.map_smul",
    upstreamFile := "Mathlib.Algebra.BigOperators.Pi; Mathlib.Topology.Algebra.Module.FiniteDimension",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "trace", "smulRight", "Pi.single", "finite-dimensional", "cross-term"],
    saldUse := "Chewi Ch.1 divergence product route: collapse the standard-basis trace of the cutoff cross derivative to the scalar derivative applied to the vector field",
    note := "Finite-dimensional linear algebra only. It proves no product-rule hypothesis, measurability, integrability, convergence, boundary cancellation, IBP, or invariant-law result."
  },
  {
    key := "analysis.calculus.coordinate-divergence-wrapped-toPi-trace",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt",
    upstreamDecl := "PiLp.hasFDerivAt_ofLp / PiLp.hasFDerivAt_toLp / HasFDerivAt.comp",
    upstreamFile := "Mathlib.Analysis.Calculus.FDeriv.WithLp; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "WithLp", "Pi-space", "fderiv", "trace-style", "pointwise"],
    saldUse := "Chewi Ch.1 calculus root: transport a Pi-space `HasFDerivAt F F' x` into the ASTIS wrapped `EuclideanSpace` coordinate divergence trace formula",
    note := "Pointwise interface bridge only. It does not prove the derivative exists a.e., box integrability, face terms, no-boundary cancellation, weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.eventuallyEq-restrict-Icc-open-box-diff-countable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.eventuallyEq_restrict_Icc_of_eqOn_univ_pi_Ioo_diff_countable",
    upstreamDecl := "Measure.univ_pi_Ioo_ae_eq_Icc plus Set.Countable.ae_notMem",
    upstreamFile := "Mathlib.MeasureTheory.Integral.DivergenceTheorem; Mathlib.MeasureTheory.Constructions.Polish.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "measure", "eventuallyEq", "closed-box", "open-box", "countable-exception"],
    saldUse := "Chewi Ch.1 calculus root: turn equality on the open Pi-box away from a countable exceptional set into equality a.e. on the restricted closed box",
    note := "A.e. transport leaf only. It does not prove differentiability, integrability, a divergence theorem, IBP, no-boundary limits, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.coordinate-divergence-wrapped-toPi-trace-ae",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_wrapped_toPi_trace_ae_of_ae_hasFDerivAt",
    upstreamDecl := "coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "WithLp", "Pi-space", "a.e.", "HasFDerivAt"],
    saldUse := "Chewi Ch.1 calculus root: discharge the finite-box face-term wrapper's `hdiv_ae` equality from an explicit a.e. Pi-space differentiability hypothesis",
    note := "A.e. equality bridge only. It assumes the derivative exists a.e.; it does not prove box integrability, face terms, no-boundary cancellation, weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.coordinate-divergence-wrapped-toPi-trace-ae-off-countable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.coordinateDivergence_wrapped_toPi_trace_ae_of_hasFDerivAt_off_countable",
    upstreamDecl := "coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt plus eventuallyEq_restrict_Icc_of_eqOn_univ_pi_Ioo_diff_countable",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; Mathlib.MeasureTheory.Integral.DivergenceTheorem",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "WithLp", "Pi-space", "a.e.", "open-box", "countable-exception"],
    saldUse := "Chewi Ch.1 calculus root: discharge the finite-box face-term wrapper's `hdiv_ae` equality from Mathlib-style open-box/off-countable differentiability data",
    note := "This closes only the a.e. bridge assumption for the box wrapper. Box integrability, whole-space/no-boundary cancellation, weighted IBP, generator domains, invariant Gibbs law, reversibility, stationarity, and KL/FI dissipation remain red."
  },
  {
    key := "analysis.calculus.integrableOn-coordinate-divergence-wrapped-of-trace",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integrableOn_coordinateDivergence_wrapped_of_integrableOn_trace_of_hasFDerivAt_off_countable",
    upstreamDecl := "IntegrableOn.congr_fun_ae plus coordinateDivergence_wrapped_toPi_trace_ae_of_hasFDerivAt_off_countable",
    upstreamFile := "Mathlib.MeasureTheory.Integral.IntegrableOn; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "WithLp", "Pi-space", "IntegrableOn", "trace-style", "a.e.", "open-box"],
    saldUse := "Chewi Ch.1 calculus root: transfer Mathlib trace-summand `IntegrableOn` across the compiled a.e. bridge to the ASTIS wrapped coordinate-divergence integrand",
    note := "Integrability transfer only. It assumes trace integrability and differentiability off a countable set; it does not prove trace integrability for a concrete Langevin field, weighted IBP, no-boundary terms, generator domains, invariant law, reversibility, stationarity, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-trace-integrable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_of_integrableOn_trace_of_hasFDerivAt_off_countable",
    upstreamDecl := "MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable plus integrableOn_coordinateDivergence_wrapped_of_integrableOn_trace_of_hasFDerivAt_off_countable",
    upstreamFile := "Mathlib.MeasureTheory.Integral.DivergenceTheorem; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "box-divergence-theorem", "face-terms", "IntegrableOn", "trace-style", "finite-dimensional"],
    saldUse := "Chewi Ch.1 calculus root: finite-box signed face-term formula for ASTIS coordinateDivergence with only Mathlib trace-integrability as the integrability input",
    note := "Box-level signed face-term wrapper only. It derives the a.e. bridge and ASTIS-side integrability internally, but still assumes trace integrability. It does not prove trace integrability for the explicit Langevin field, whole-space/no-boundary cancellation, weighted IBP, generator domains, invariant Gibbs law, reversibility, stationarity, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-face",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable",
    upstreamDecl := "integral_coordinateDivergence_toPi_box_of_integrableOn_trace_of_hasFDerivAt_off_countable plus supplied zero signed-face term",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "coordinate-divergence", "box-divergence-theorem", "face-terms", "zero-face", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 finite-box weighted-IBP route: once the signed face term is explicitly zero, the ASTIS coordinate-divergence box integral is zero",
    note := "Conditional zero-face handoff only. It assumes the face term vanishes; it does not prove compact support, boundary decay, whole-space limits, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.signed-face-term-sum-zero-of-boundary-component-zero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_eq_zero_of_boundary_component_eq_zero",
    upstreamDecl := "integral_zero / Finset.sum_eq_zero via componentwise zero values on lower and upper faces",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "face-terms", "zero-face", "finite-box", "coordinate-divergence"],
    saldUse := "log-concave sampling Ch.1 boundary route: explicit zero normal components on all finite-box faces imply the signed face-term sum vanishes",
    note := "Boundary-value producer only. It assumes componentwise zero values on the faces; it does not prove compact support, tail decay, whole-space limits, weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-boundary-component",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_boundary_component_eq_zero",
    upstreamDecl := "integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable plus signedFaceTermSum_eq_zero_of_boundary_component_eq_zero",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "coordinate-divergence", "box-divergence-theorem", "zero-face", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 finite-box weighted-IBP route: if the vector field's normal component is zero on each lower and upper face, the ASTIS coordinate-divergence box integral is zero",
    note := "Finite-box conditional boundary handoff only. It still assumes trace integrability and open-box/off-countable differentiability; it does not derive compact support, tail decay, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.signed-face-term-sum-zero-of-update-boundary-component-zero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero",
    upstreamDecl := "signedFaceTermSum_eq_zero_of_boundary_component_eq_zero plus Function.update_eq_self on Fin.insertNth faces",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "Function.update", "face-terms", "zero-face", "finite-box"],
    saldUse := "log-concave sampling Ch.1 boundary route: update-to-boundary zero component hypotheses imply the finite-box signed face-term sum vanishes",
    note := "Update-shaped boundary-value producer only. It assumes zero components after replacing a coordinate by the face endpoint; it does not prove compact support, tail decay, whole-space limits, weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-update-boundary-component",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_update_boundary_component_eq_zero",
    upstreamDecl := "integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable plus signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "Function.update", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box weighted-IBP route: update-to-boundary zero component hypotheses imply the ASTIS coordinate-divergence box integral is zero",
    note := "Finite-box conditional update-boundary handoff only. It still assumes trace integrability and open-box/off-countable differentiability; it does not derive compact support, tail decay, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.update-boundary-component-zero-of-eq-zero-off-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.update_boundary_component_eq_zero_of_eq_zero_off_univ_pi_Ioo",
    upstreamDecl := "Set.mem_univ_pi plus endpoint self-inequality contradiction for Function.update boundary points",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "open-box", "Function.update", "zero-boundary", "finite-box"],
    saldUse := "log-concave sampling Ch.1 boundary route: off-open-box vanishing implies update-to-boundary normal components are zero",
    note := "Off-open-box boundary producer only. It assumes the vector field is already zero outside the open Pi-box; it does not prove compact support, cutoff support, tail decay, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.signed-face-term-sum-zero-of-eq-zero-off-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo",
    upstreamDecl := "update_boundary_component_eq_zero_of_eq_zero_off_univ_pi_Ioo plus signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "open-box", "face-terms", "zero-face", "finite-box"],
    saldUse := "log-concave sampling Ch.1 boundary route: off-open-box vanishing implies Mathlib's finite-box signed face-term sum is zero",
    note := "Signed face-term producer only. It assumes off-open-box vanishing; it does not prove compact support, tail decay, whole-space limits, weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-off-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_eq_zero_off_univ_pi_Ioo",
    upstreamDecl := "integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable plus signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "open-box", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box weighted-IBP route: off-open-box vanishing implies the ASTIS coordinate-divergence box integral is zero",
    note := "Finite-box off-open-box handoff only. It still assumes trace integrability and open-box/off-countable differentiability; it does not derive compact support, tail decay, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.eq-zero-off-univ-pi-Ioo-of-support-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.eq_zero_off_univ_pi_Ioo_of_support_subset_univ_pi_Ioo",
    upstreamDecl := "Function.support subset plus contradiction outside target set",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "support", "open-box", "finite-box"],
    saldUse := "log-concave sampling Ch.1 boundary route: a support subset of the open Pi-box implies the vector field is zero outside that open Pi-box",
    note := "Plain support-to-off-open-box producer only. It assumes the support subset; it does not prove compact support construction, cutoff support, tail decay, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.exists-contDiff-cutoff-tsupport-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_cutoff_tsupport_subset_univ_pi_Ioo",
    upstreamDecl := "exists_contDiff_tsupport_subset specialized to finite Pi-open boxes",
    upstreamFile := "Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smooth-cutoff", "ContDiff", "HasCompactSupport", "tsupport", "open-box", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 cutoff route: construct a local smooth real-valued cutoff whose topological support is contained in a finite Pi-open box and which equals one at a chosen interior point",
    note := "Local smooth-cutoff existence leaf only. It does not choose an exhausting cutoff family, prove concrete derivative formulas for the cutoff, pass to whole-space tail limits, prove weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.support-subset-univ-pi-Ioo-of-tsupport-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo",
    upstreamDecl := "subset_tsupport composed with finite Pi-open-box containment",
    upstreamFile := "Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "tsupport", "open-box", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 cutoff route: convert Mathlib topological-support containment for a scalar cutoff into the plain Function.support containment consumed by finite-box zero-face handoffs",
    note := "Support-API bridge only. It does not construct a cutoff, prove compactness, choose an exhausting cutoff family, prove derivative formulas, tail limits, weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.exists-contDiff-cutoff-support-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_cutoff_support_subset_univ_pi_Ioo",
    upstreamDecl := "exists_contDiff_cutoff_tsupport_subset_univ_pi_Ioo plus support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo",
    upstreamFile := "Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smooth-cutoff", "ContDiff", "HasCompactSupport", "support", "tsupport", "open-box", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 cutoff route: construct a local smooth cutoff with both topological support and plain Function.support contained in the finite Pi-open box",
    note := "Local smooth-cutoff packaging leaf only. It does not choose an exhausting cutoff family, prove concrete derivative formulas, pass to whole-space tail limits, prove weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.exists-contDiff-support-eq-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_support_eq_univ_pi_Ioo",
    upstreamDecl := "IsOpen.exists_contDiff_support_eq specialized to finite Pi-open boxes",
    upstreamFile := "Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smooth-cutoff", "ContDiff", "support", "support-eq", "open-box", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 cutoff/exhaustion route: construct a smooth [0,1]-valued function whose plain support is exactly a finite Pi-open box",
    note := "Exact plain-support open-box smooth function only. It does not prove compact support, topological-support containment, plateau equal to one on an inner closed box, an exhausting family, derivative bounds, tail limits, weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.positive-on-univ-pi-Ioo-of-support-eq-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.positive_on_univ_pi_Ioo_of_support_eq_univ_pi_Ioo",
    upstreamDecl := "Function.support equality plus range subset Set.Icc 0 1",
    upstreamFile := "Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "support-eq", "positivity", "open-box", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 cutoff/exhaustion route: turn exact open-box plain support and [0,1] range into strict positivity on the finite Pi-open box",
    note := "Support/range consequence only. It does not construct a cutoff, prove compact support, prove plateau behavior, choose an exhausting family, prove derivative bounds, tail limits, weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.Icc-subset-univ-pi-Ioo-of-forall-lt",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.Icc_subset_univ_pi_Ioo_of_strict_bounds",
    upstreamDecl := "coordinatewise order on Pi spaces plus strict outer bounds",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "closed-box", "open-box", "exhaustion", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 cutoff/exhaustion route: an inner closed Pi-box is contained in any coordinatewise strictly larger open Pi-box",
    note := "Closed-box/open-box containment bookkeeping only. It does not construct a cutoff, choose an exhausting family, prove derivative bounds, tail limits, weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.exists-contDiff-cutoff-support-subset-outer-univ-pi-Ioo-of-mem-Icc",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.exists_contDiff_cutoff_support_subset_outer_univ_pi_Ioo_of_mem_Icc",
    upstreamDecl := "Icc_subset_univ_pi_Ioo_of_strict_bounds plus exists_contDiff_cutoff_support_subset_univ_pi_Ioo",
    upstreamFile := "Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smooth-cutoff", "closed-box", "open-box", "support", "tsupport", "exhaustion", "finite-dimensional"],
    saldUse := "log-concave sampling Ch.1 cutoff/exhaustion route: every point of an inner closed Pi-box has a local smooth cutoff whose support and topological support lie in a strictly larger open Pi-box",
    note := "Local pointwise cutoff in an outer open box only. It does not construct one cutoff equal to one on the whole inner closed box, choose an exhausting cutoff family, prove derivative bounds, pass to whole-space tail limits, prove weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.signed-face-term-sum-zero-of-support-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo",
    upstreamDecl := "eq_zero_off_univ_pi_Ioo_of_support_subset_univ_pi_Ioo plus signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "support", "open-box", "face-terms", "zero-face", "finite-box"],
    saldUse := "log-concave sampling Ch.1 boundary route: a support subset of the open Pi-box implies Mathlib's finite-box signed face-term sum is zero",
    note := "Support-subset face-term producer only. It assumes the support subset; it does not prove compact support construction, cutoff support, tail decay, whole-space limits, weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-support-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo",
    upstreamDecl := "integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable plus signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "support", "open-box", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box weighted-IBP route: a support subset of the open Pi-box implies the ASTIS coordinate-divergence box integral is zero",
    note := "Finite-box support-subset handoff only. It still assumes trace integrability and open-box/off-countable differentiability, and it assumes the support subset; it does not derive compact support, tail decay, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.support-smul-subset-univ-pi-Ioo-of-cutoff-eq-zero-off-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo",
    upstreamDecl := "scalar zero outside open Pi-box implies zero smul vector field outside open Pi-box",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "smul", "open-box", "finite-box"],
    saldUse := "log-concave sampling Ch.1 cutoff route: a scalar cutoff vanishing outside the open Pi-box forces the cutoff-smul vector field to be supported in the open Pi-box",
    note := "Plain support-containment bridge only. It does not construct a smooth cutoff, prove HasCompactSupport, prove cutoff-smul regularity, tail decay, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.support-smul-subset-univ-pi-Ioo-of-scalar-support-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo",
    upstreamDecl := "scalar Function.support subset plus support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "smul", "open-box", "finite-box"],
    saldUse := "log-concave sampling Ch.1 cutoff route: a scalar cutoff supported in the open Pi-box forces the cutoff-smul vector field to be supported in the open Pi-box",
    note := "Scalar-support-to-vector-support bridge only. It uses Function.support, not topological compact support, and does not prove cutoff construction, cutoff-smul regularity, tail decay, whole-space weighted IBP, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.support-smul-subset-univ-pi-Ioo-of-scalar-tsupport-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.support_smul_subset_univ_pi_Ioo_of_scalar_tsupport_subset_univ_pi_Ioo",
    upstreamDecl := "support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo plus support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo",
    upstreamFile := "Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "tsupport", "smul", "open-box", "finite-box"],
    saldUse := "log-concave sampling Ch.1 cutoff route: a scalar cutoff with topological support inside the open Pi-box forces the cutoff-smul vector field to be plain-supported in that open box",
    note := "Direct tsupport-to-cutoff-smul support bridge only. It does not construct a cutoff, prove cutoff-smul regularity, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.continuousOn-smul-vectorField-of-continuousOn",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.continuousOn_smul_vectorField_of_continuousOn",
    upstreamDecl := "ContinuousOn.smul",
    upstreamFile := "Mathlib.Topology.Algebra.Module.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "ContinuousOn", "closed-box", "regularity"],
    saldUse := "log-concave sampling Ch.1 cutoff route: derive closed-box continuity of a cutoff-smul vector field from separate cutoff and vector-field continuity",
    note := "Closed-box continuity bridge only. It does not prove smooth cutoff construction, differentiability, trace integrability, boundary cancellation, weighted IBP, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.hasFDerivAt-smul-vectorField-of-hasFDerivAt",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.hasFDerivAt_smul_vectorField_of_hasFDerivAt",
    upstreamDecl := "HasFDerivAt.smul",
    upstreamFile := "Mathlib.Analysis.Calculus.FDeriv.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "HasFDerivAt", "product-rule", "regularity"],
    saldUse := "log-concave sampling Ch.1 cutoff route: pointwise product-rule Frechet derivative for the cutoff-smul vector field",
    note := "Pointwise derivative bridge only. It does not prove continuity, open-box/off-countable coverage, trace integrability, boundary cancellation, weighted IBP, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.hasFDerivAt-smul-vectorField-off-countable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.hasFDerivAt_smul_vectorField_off_countable",
    upstreamDecl := "hasFDerivAt_smul_vectorField_of_hasFDerivAt applied pointwise on open box minus a countable set",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "HasFDerivAt", "open-box", "countable-exception", "regularity"],
    saldUse := "log-concave sampling Ch.1 cutoff route: derive the divergence-theorem off-countable derivative hypothesis for a cutoff-smul field from separate cutoff and vector-field derivative hypotheses",
    note := "Off-countable derivative bridge only. It assumes a shared exceptional set and does not prove trace integrability, closed-box continuity, boundary cancellation, weighted IBP, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.signed-face-term-sum-smul-zero-of-cutoff-eq-zero-off-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_smul_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo",
    upstreamDecl := "support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo plus signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "face-terms", "zero-face", "finite-box"],
    saldUse := "log-concave sampling Ch.1 cutoff route: a scalar cutoff vanishing outside the open Pi-box implies the cutoff-smul finite-box signed face-term sum is zero",
    note := "Finite-box cutoff-smul face-term producer only. It does not prove smooth cutoff existence, regularity, trace integrability, tail limits, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.signed-face-term-sum-smul-zero-of-scalar-support-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_smul_eq_zero_of_scalar_support_subset_univ_pi_Ioo",
    upstreamDecl := "support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo plus signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "smul", "face-terms", "zero-face", "finite-box"],
    saldUse := "log-concave sampling Ch.1 cutoff route: scalar cutoff support inside the open Pi-box implies the cutoff-smul finite-box signed face-term sum is zero",
    note := "Finite-box scalar-support face-term producer only. It does not prove smooth cutoff existence, regularity, trace integrability, tail limits, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.signed-face-term-sum-smul-zero-of-scalar-tsupport-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.signedFaceTermSum_smul_eq_zero_of_scalar_tsupport_subset_univ_pi_Ioo",
    upstreamDecl := "support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo plus signedFaceTermSum_smul_eq_zero_of_scalar_support_subset_univ_pi_Ioo",
    upstreamFile := "Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "tsupport", "smul", "face-terms", "zero-face", "finite-box"],
    saldUse := "log-concave sampling Ch.1 cutoff route: scalar topological support inside the open Pi-box implies the cutoff-smul finite-box signed face-term sum is zero",
    note := "Finite-box scalar-tsupport face-term producer only. It does not prove smooth cutoff construction, cutoff-smul regularity, trace integrability, tail limits, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-cutoff-eq-zero-off-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo",
    upstreamDecl := "integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo plus support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: scalar cutoff vanishing outside the open Pi-box implies the cutoff-smul coordinate-divergence box integral is zero under the existing trace/differentiability assumptions",
    note := "Finite-box cutoff-smul handoff only. It still assumes continuity, open-box/off-countable differentiability, and trace integrability for the cutoff-smul field; it does not prove those regularity facts, smooth cutoff existence, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo",
    upstreamDecl := "integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo plus support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "smul", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: scalar cutoff support inside the open Pi-box implies the cutoff-smul coordinate-divergence box integral is zero under the existing trace/differentiability assumptions",
    note := "Finite-box scalar-support cutoff handoff only. It still assumes continuity, open-box/off-countable differentiability, and trace integrability for the cutoff-smul field; it does not prove those regularity facts, smooth cutoff existence, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-tsupport-subset-univ-pi-Ioo",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_tsupport_subset_univ_pi_Ioo",
    upstreamDecl := "support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo plus integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo",
    upstreamFile := "Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "tsupport", "smul", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: scalar cutoff topological support inside the open Pi-box implies the cutoff-smul coordinate-divergence box integral is zero under the existing trace/differentiability assumptions",
    note := "Finite-box scalar-tsupport cutoff handoff only. It still assumes continuity, open-box/off-countable differentiability, and trace integrability for the cutoff-smul field; it does not prove smooth cutoff construction, cutoff-smul regularity, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-cutoff-eq-zero-off-univ-pi-Ioo-regularity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_regularity",
    upstreamDecl := "continuousOn_smul_vectorField_of_continuousOn plus hasFDerivAt_smul_vectorField_off_countable plus integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "regularity", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: derive the cutoff-smul continuity and off-countable derivative hypotheses before applying the zero-face coordinate-divergence handoff",
    note := "Finite-box regularity handoff only. Trace integrability for the product-rule derivative remains explicit; it does not prove smooth cutoff construction, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo-regularity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_regularity",
    upstreamDecl := "continuousOn_smul_vectorField_of_continuousOn plus hasFDerivAt_smul_vectorField_off_countable plus integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "smul", "regularity", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: derive cutoff-smul regularity hypotheses before applying the scalar-support zero-face coordinate-divergence handoff",
    note := "Finite-box scalar-support regularity handoff only. Trace integrability for the product-rule derivative remains explicit; it does not prove smooth cutoff construction, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo-fderiv",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_fderiv",
    upstreamDecl := "scalar-support regularity handoff specialized to canonical fderiv field",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "smul", "fderiv", "regularity", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: replace the supplied vector-field derivative parameter by the canonical `fderiv ℝ G` in the scalar-support zero integral handoff",
    note := "Finite-box canonical-fderiv handoff only. It still assumes cutoff derivative data, continuity, trace integrability, and scalar support containment; it does not construct an exhausting cutoff family, prove tail decay, whole-space weighted IBP, generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integrableOn-smul-vectorField-trace-of-continuousOn",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integrableOn_smul_vectorField_trace_of_continuousOn",
    upstreamDecl := "ContinuousOn.integrableOn_compact on isCompact_Icc",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "trace-style", "IntegrableOn", "ContinuousOn", "closed-box"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: discharge compact-box integrability of the cutoff-smul product-rule trace from closed-box trace continuity",
    note := "Compact-box integrability handoff only. It assumes trace continuity and does not prove trace continuity from component assumptions, smooth cutoff construction, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-cutoff-eq-zero-off-univ-pi-Ioo-trace-continuous",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_trace_continuous",
    upstreamDecl := "integrableOn_smul_vectorField_trace_of_continuousOn plus integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_regularity",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "trace-style", "ContinuousOn", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: derive cutoff-smul regularity and compact-box trace integrability before applying the zero-face coordinate-divergence handoff",
    note := "Finite-box trace-continuity handoff only. It still assumes closed-box trace continuity and cutoff vanishing outside the open box; it does not prove smooth cutoff construction, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo-trace-continuous",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_trace_continuous",
    upstreamDecl := "integrableOn_smul_vectorField_trace_of_continuousOn plus integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_regularity",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "smul", "trace-style", "ContinuousOn", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: derive cutoff-smul regularity and compact-box trace integrability before applying the scalar-support zero-face coordinate-divergence handoff",
    note := "Finite-box scalar-support trace-continuity handoff only. It still assumes closed-box trace continuity and scalar Function.support containment; it does not prove smooth cutoff construction, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.continuousOn-smul-vectorField-trace-of-component-continuousOn",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.continuousOn_smul_vectorField_trace_of_component_continuousOn",
    upstreamDecl := "continuousOn_finset_sum plus scalar ContinuousOn.mul/add after expanding smulRight trace",
    upstreamFile := "Mathlib.Topology.Algebra.Group.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "trace-style", "ContinuousOn", "component", "closed-box"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: derive closed-box continuity of the cutoff-smul product-rule trace from exactly the diagonal component continuity hypotheses used by the trace summand",
    note := "Trace-continuity assembly only. It does not prove that the component fields are derivatives, does not identify the product-rule operator with canonical fderiv, and does not prove smooth cutoff construction, tail decay, whole-space weighted IBP, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.continuousOn-smul-vectorField-trace-of-components",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.continuousOn_smul_vectorField_trace_of_components",
    upstreamDecl := "continuousOn_smul_vectorField_trace_of_component_continuousOn plus ContinuousOn.clm_apply/component projection",
    upstreamFile := "Mathlib.Analysis.Normed.Operator.BoundedLinearMaps; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "trace-style", "ContinuousOn", "closed-box"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: convenience wrapper deriving trace continuity from CLM-valued continuity of χ' and G'",
    note := "Convenience trace-continuity wrapper only. It is stronger than the component-continuity leaf and still does not prove derivative existence, smooth cutoff construction, tail decay, weighted IBP, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-cutoff-eq-zero-off-univ-pi-Ioo-component-continuous",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_component_continuous",
    upstreamDecl := "continuousOn_smul_vectorField_trace_of_component_continuousOn plus trace-continuous zero-face handoff",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "smul", "component", "trace-style", "ContinuousOn", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: component trace continuity, regularity hypotheses, and cutoff vanishing imply the finite-box cutoff-smul coordinate-divergence integral is zero",
    note := "Finite-box component-continuity handoff only. It assumes derivative hypotheses and cutoff vanishing; it does not prove smooth cutoff construction, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo-component-continuous",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_component_continuous",
    upstreamDecl := "continuousOn_smul_vectorField_trace_of_component_continuousOn plus scalar-support trace-continuous zero-face handoff",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Langevin", "boundary", "cutoff", "support", "smul", "component", "trace-style", "ContinuousOn", "coordinate-divergence", "box-divergence-theorem", "zero-face"],
    saldUse := "log-concave sampling Ch.1 finite-box cutoff route: component trace continuity, regularity hypotheses, and scalar support containment imply the finite-box cutoff-smul coordinate-divergence integral is zero",
    note := "Finite-box scalar-support component-continuity handoff only. It assumes derivative hypotheses and scalar Function.support containment; it does not prove smooth cutoff construction, tail decay, whole-space weighted IBP, generator domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.integral-coordinate-divergence-toPi-box",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence.integral_coordinateDivergence_toPi_box_of_hasFDerivAt_off_countable",
    upstreamDecl := "MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable plus coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt",
    upstreamFile := "Mathlib.MeasureTheory.Integral.DivergenceTheorem; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "box-divergence-theorem", "face-terms", "IntegrableOn", "ae-equality", "finite-dimensional"],
    saldUse := "Chewi Ch.1 calculus root: integrate ASTIS coordinateDivergence over a finite Mathlib box and obtain only the signed face-term formula, assuming the a.e. bridge to Mathlib's trace integrand and box integrability explicitly",
    note := "Box-level signed face-term wrapper only. It assumes the finite-box continuity/off-countable differentiability hypotheses, an a.e. bridge from ASTIS coordinateDivergence to Mathlib's trace integrand, and IntegrableOn for the coordinate-divergence integrand. It does not derive that a.e. bridge, prove box integrability, prove whole-space/no-boundary cancellation, weighted IBP, generator domains, invariant Gibbs law, reversibility, stationarity, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.line-derivative-product-rule",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.hasLineDerivAt_mul",
    upstreamDecl := "HasDerivAt.mul applied to the line curve t ↦ x + t • v",
    upstreamFile := "Mathlib.Analysis.Calculus.LineDeriv.Basic; Mathlib.Analysis.Calculus.Deriv.Mul",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "line-derivative", "product-rule", "coordinate", "weighted-divergence", "NormedAlgebra"],
    saldUse := "Chewi SDE/ANALYSIS root: expose the generic algebra-valued line-derivative product rule before finite Euclidean weighted-divergence algebra",
    note := "Generic product-rule leaf only. It does not by itself discharge the current Langevin `hdiv` hypothesis; it does not identify `g` with a coordinate derivative of a test function, prove Hessian/iterated-derivative identities, define divergence, prove divergence-sum identities, IBP, boundary decay, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.line-derivative-rho-product-rule",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.hasLineDerivAt_rho_mul",
    upstreamDecl := "hasLineDerivAt_mul specialized to real-valued `rho * g`, reordered for weighted-divergence algebra",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "line-derivative", "product-rule", "rho", "coordinate", "weighted-divergence"],
    saldUse := "Chewi SDE/ANALYSIS root: isolate the product-rule component of a coordinate calculation `∂ᵢ (rho * g) = rho * ∂ᵢ g + (∂ᵢ rho) * g` before finite Euclidean weighted-divergence algebra",
    note := "Real-valued product-rule specialization only. It does not by itself discharge the current Langevin `hdiv` hypothesis; `g = ∂ᵢ f`, the diagonal Hessian/iterated derivative, divergence-sum identity, IBP, stationarity, reversibility, invariant Gibbs law, and KL/FI remain red."
  },
  {
    key := "analysis.calculus.line-derivative-rho-product-rule-lineDeriv",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_rho_mul_eq_of_hasLineDerivAt",
    upstreamDecl := "HasLineDerivAt.lineDeriv applied to hasLineDerivAt_rho_mul",
    upstreamFile := "Mathlib.Analysis.Calculus.LineDeriv.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "line-derivative", "product-rule", "rho", "coordinate", "weighted-divergence", "lineDeriv"],
    saldUse := "Chewi SDE/ANALYSIS root: convert supplied coordinate derivative facts for `rho` and `g` into the exact `lineDeriv` equality shape used by weighted-divergence displays",
    note := "Equality-form product-rule leaf only. It does not identify `g` with a coordinate derivative of a test function, prove Hessian/iterated-derivative identities, define divergence, prove divergence-sum identities, IBP, boundary decay, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.line-derivative-exp-neg-potential-product-coordinate",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_expNegPotential_mul_eq_of_differentiableAt",
    upstreamDecl := "DifferentiableAt.hasGradientAt; hasGradientAt_expNegPotential_of_hasGradientAt; hasGradientAt_coordinateUnit_hasLineDerivAt; lineDeriv_rho_mul_eq_of_hasLineDerivAt",
    upstreamFile := "Mathlib.Analysis.Calculus.LineDeriv.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "line-derivative", "product-rule", "exp-neg-potential", "EuclideanSpace", "coordinate"],
    saldUse := "Chewi SDE/DENS root: compute the coordinate-unit line derivative of `fun y => exp (-V y) * g y` from `DifferentiableAt ℝ V x` and a supplied coordinate derivative of `g`, narrowing the remaining Langevin `hdiv` branch to `g = ∂ᵢ f` and Hessian-coordinate wiring",
    note := "Pointwise coordinate product-rule leaf for the explicit Gibbs weight. It does not identify `g` with a coordinate derivative of a test function, prove the diagonal Hessian/iterated derivative, define divergence, prove divergence-sum identities, IBP, no-boundary terms, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.line-derivative-fderiv-apply-const-from-hasFDerivAt",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv",
    upstreamDecl := "HasFDerivAt.clm_apply plus HasFDerivAt.hasLineDerivAt",
    upstreamFile := "Mathlib.Analysis.Calculus.FDeriv.CompCLM; Mathlib.Analysis.Calculus.LineDeriv.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "line-derivative", "fderiv", "second-derivative", "Hessian", "coordinate"],
    saldUse := "Chewi SDE/ANALYSIS root: a supplied derivative of `fun y => fderiv ℝ f y` gives the line derivative of the first-derivative slice `fun y => fderiv ℝ f y v`",
    note := "Second-derivative wiring leaf only. It does not identify the supplied derivative with `iteratedFDeriv`, replace `fderiv ℝ f y eᵢ` by `(gradient f y) i`, define divergence, prove IBP, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.line-derivative-fderiv-apply-const-lineDeriv",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_fderiv_apply_const_eq_of_hasFDerivAt_fderiv",
    upstreamDecl := "HasLineDerivAt.lineDeriv applied to hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "lineDeriv", "fderiv", "second-derivative", "Hessian", "coordinate"],
    saldUse := "Chewi SDE/ANALYSIS root: equality-form line derivative of a first-derivative slice, usable as an input to later supplied weighted-product/divergence displays",
    note := "Equality-form second-derivative wiring leaf only. It does not identify `fderiv ℝ f` with a gradient coordinate, prove divergence, prove IBP, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.line-derivative-fderiv-apply-iteratedFDeriv-two",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_fderiv_apply_const_eq_iteratedFDeriv_two",
    upstreamDecl := "iteratedFDeriv_two_apply plus lineDeriv_fderiv_apply_const_eq_of_hasFDerivAt_fderiv",
    upstreamFile := "Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "lineDeriv", "fderiv", "iteratedFDeriv", "Hessian", "second-derivative"],
    saldUse := "Chewi SDE/ANALYSIS root: rewrite the line derivative of `fun y => fderiv ℝ f y v` as Mathlib's `iteratedFDeriv ℝ 2 f x ![w, v]` under differentiability of the total `fderiv` map at `x`",
    note := "Pointwise total-fderiv/lineDeriv leaf only. It rewrites a fixed `fderiv ℝ f · v` slice into Mathlib's total `iteratedFDeriv ℝ 2` representative at `x`. It does not assert `f` is globally C², does not prove classical Hessian symmetry, does not replace `fderiv ℝ f x eᵢ` by `(gradient f x) i`, does not define or sum divergence, and does not prove IBP, boundary decay, invariant Gibbs law, reversibility, or KL/FI dissipation."
  },
  {
    key := "analysis.calculus.line-derivative-fderiv-coordinate-iteratedFDeriv-two",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_fderiv_apply_coordinate_eq_iteratedFDeriv_two",
    upstreamDecl := "lineDeriv_fderiv_apply_const_eq_iteratedFDeriv_two specialized to EuclideanSpace coordinate units",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "EuclideanSpace", "coordinate", "lineDeriv", "fderiv", "iteratedFDeriv", "Hessian"],
    saldUse := "Chewi Ch.1 Langevin root: coordinate-unit line derivative of a first-derivative slice equals the diagonal `iteratedFDeriv` term used by finite-coordinate generator displays",
    note := "Pointwise total-fderiv/lineDeriv coordinate leaf only. It rewrites the coordinate-unit line derivative of the fixed `fderiv ℝ f · eᵢ` slice into Mathlib's `iteratedFDeriv ℝ 2` representative at `x`. It does not assert global C² regularity, classical Hessian symmetry, gradient-coordinate replacement, divergence, IBP, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.line-derivative-exp-neg-potential-fderiv-coordinate",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv.lineDeriv_expNegPotential_mul_fderiv_coordinate_eq",
    upstreamDecl := "lineDeriv_expNegPotential_mul_eq_of_differentiableAt plus lineDeriv_fderiv_apply_coordinate_eq_iteratedFDeriv_two",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "lineDeriv", "fderiv", "iteratedFDeriv", "Hessian", "EuclideanSpace", "coordinate"],
    saldUse := "Chewi Ch.1 Langevin root: compute the coordinate line derivative of `exp(-V) * fderiv f eᵢ`, producing the Gibbs-weighted diagonal iterated-derivative term and the potential-gradient product term",
    note := "Pointwise Gibbs-weight product-rule leaf for `lineDeriv_i (exp(-V) * fderiv f eᵢ)`. It discharges only the local `exp(-V)` derivative and the local total-fderiv slice derivative under the stated pointwise assumptions. Gradient-coordinate replacement, divergence operator/sum, Laplacian identification, IBP/no-boundary terms, stationarity, reversibility, invariant Gibbs law, and KL/FI remain separate obligations."
  },
  {
    key := "analysis.calculus.laplacian-std-orthonormal-basis",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian.laplacian_eq_sum_stdOrthonormalBasis",
    upstreamDecl := "InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis",
    upstreamFile := "Mathlib.Analysis.InnerProductSpace.Laplacian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Laplacian", "finite-dimensional", "stdOrthonormalBasis", "iteratedFDeriv"],
    saldUse := "Chewi SDE/ANALYSIS root: identify Mathlib's finite-dimensional Laplacian with the standard orthonormal-basis second-derivative sum used in Langevin generator displays",
    note := "Coordinate Laplacian bridge only. It does not prove gradients, divergence, integration by parts, boundary decay, stationarity, reversibility, or invariant Gibbs law."
  },
  {
    key := "analysis.calculus.laplacian-functional-std-orthonormal-basis",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian.laplacianFunctional_eq_of_stdOrthonormalBasis_sum",
    upstreamDecl := "laplacian_eq_sum_stdOrthonormalBasis",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Laplacian", "weak-generator", "finite-dimensional", "test-function"],
    saldUse := "Chewi SDE/ANALYSIS root: rewrite weak-generator or source-defined test-function Laplacian actions from coordinate second-derivative sums to Mathlib `Laplacian.laplacian`",
    note := "Functional handoff for definitions only; analytic weak-FP, IBP, and invariant-law statements remain separate red branches."
  },
  {
    key := "analysis.calculus.continuous-laplacian-of-contDiff-two",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian.continuous_laplacian_of_contDiff_two",
    upstreamDecl := "ContDiff.iteratedFDeriv_right plus Mathlib finite-dimensional Laplacian basis display",
    upstreamFile := "Mathlib.Analysis.InnerProductSpace.Laplacian; Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Laplacian", "ContDiff", "Continuous", "iteratedFDeriv", "regularity"],
    saldUse := "Chewi Ch.1 Langevin root: derive continuity of Mathlib's finite-dimensional total Laplacian from global `C²` regularity before closed-box integrability handoffs",
    note := "Global `C²` to continuous Mathlib Laplacian only. It does not assert a closed-box `ContDiffOn` variant, field differentiability, weighted IBP, boundary cancellation, domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "analysis.calculus.laplacian-finrank-iterated-fderiv-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian.norm_laplacian_le_finrank_mul_norm_iteratedFDeriv_two",
    upstreamDecl := "InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis; ContinuousMultilinearMap.le_opNorm",
    upstreamFile := "Mathlib.Analysis.InnerProductSpace.Laplacian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Laplacian", "iteratedFDeriv", "finrank", "trace-bound"],
    saldUse := "log-concave sampling Ch.1: turn an operator-norm second-derivative estimate into a Laplacian estimate with an explicit dimension factor",
    note := "Pointwise finite-dimensional trace bound only; no compact support, integrability, cutoff, or invariant-law statement is included."
  },
  {
    key := "analysis.calculus.radial-smooth-cutoff-laplacian-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian.radialSmoothCutoff_laplacian_bound",
    upstreamDecl := "radialSmoothCutoff_iteratedFDeriv_two_bound; norm_laplacian_le_finrank_mul_norm_iteratedFDeriv_two",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.{Cutoff,Laplacian}",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "cutoff", "radial", "Laplacian", "O-R-inverse-squared", "finrank"],
    saldUse := "log-concave sampling Ch.1 second-order exhaustion branch: radial cutoff Laplacian bound with explicit finrank times C/R^2",
    note := "Compiled second-order cutoff estimate. It remains independent of the external-blocked concrete Langevin semigroup/domain construction."
  }
]

def measureMemory : List LemmaMemoryEntry := [
  {
    key := "measure.wasserstein.chewi-definition-1-3-4",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace.wassersteinDistance",
    upstreamDecl := "Chewi Definition 1.3.4",
    upstreamFile := "Log-Concave Sampling, book page 20 / PDF page 32",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Wasserstein", "W2", "quadratic-cost", "coupling", "ENNReal"],
    saldUse := "Chewi Definition 1.3.4 root: define W2 as the positive square root of quadratic Kantorovich cost",
    note := "Exact extended-real value definition; metric properties and finite-second-moment finiteness are separate theorems."
  },
  {
    key := "measure.wasserstein.chewi-display-1-3-5",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace.wassersteinDistance_sq",
    upstreamDecl := "Chewi display (1.3.5)",
    upstreamFile := "Log-Concave Sampling, book page 20 / PDF page 32",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Wasserstein", "W2", "quadratic-cost", "source-display"],
    saldUse := "Chewi display (1.3.5): rewrite W2 squared as the quadratic coupling infimum",
    note := "Actual ENNReal rpow calculation; no optimal coupling is assumed."
  },
  {
    key := "measure.wasserstein.chewi-definition-1-3-12",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace.IsAbsolutelyContinuousFiniteSecondMoment",
    upstreamDecl := "Chewi Definition 1.3.12",
    upstreamFile := "Log-Concave Sampling, book page 25 / PDF page 37",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Wasserstein", "P2ac", "absolute-continuity", "second-moment", "Lebesgue"],
    saldUse := "Chewi Definition 1.3.12 root: package probability normalization, finite second moment, and Lebesgue absolute continuity",
    note := "Exact measure-class definition; no Wasserstein metric, optimal map, or gradient-flow theorem is asserted."
  },
  {
    key := "measure.wasserstein.quadratic-optimal-coupling",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolation.IsQuadraticOptimalCoupling",
    upstreamDecl := "Chewi Definition 1.3.25 / quadratic Kantorovich attainment",
    upstreamFile := "Log-Concave Sampling, book page 30 / PDF page 42",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Wasserstein", "optimal-coupling", "quadratic-cost", "attainment"],
    saldUse := "state that a prescribed coupling actually attains the quadratic Kantorovich infimum before constructing displacement interpolation",
    note := "This predicate does not prove that an optimizer exists; it records marginal feasibility and exact attainment."
  },
  {
    key := "measure.wasserstein.displacement-interpolation",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolation.displacementInterpolation",
    upstreamDecl := "Chewi Definition 1.3.25 / law of (1-t)X0+tX1",
    upstreamFile := "Log-Concave Sampling, book page 30 / PDF page 42",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Wasserstein", "measure-map", "affine-interpolation", "McCann"],
    saldUse := "build the time-t law as the pushforward of a coupling by the affine endpoint map",
    note := "The endpoint identities are proved separately; constant speed and uniqueness remain Theorem 1.3.23."
  },
  {
    key := "measure.wasserstein.chewi-definition-1-3-25",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolation.IsWassersteinGeodesic",
    upstreamDecl := "Chewi Definition 1.3.25",
    upstreamFile := "Log-Concave Sampling, book page 30 / PDF page 42",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Wasserstein", "geodesic", "displacement-interpolation", "P2ac"],
    saldUse := "Chewi Definition 1.3.25 root: package P2ac endpoints, an optimal quadratic coupling, and its affine-law curve on [0,1]",
    note := "Source-faithful definition only; optimal-plan existence, metric constant speed, and uniqueness are not inferred."
  },
  {
    key := "measure.transport.chewi-definition-1-3-1",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost",
    upstreamDecl := "Chewi Definition 1.3.1",
    upstreamFile := "Log-Concave Sampling, book page 20 / PDF page 32",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Kantorovich", "optimal-transport", "coupling", "sInf", "ENNReal"],
    saldUse := "Chewi Definition 1.3.1 root: define the extended nonnegative Kantorovich transport cost over all couplings",
    note := "Exact optimization value; lower semicontinuity and existence of an optimal plan are separate theorem routes."
  },
  {
    key := "measure.transport.chewi-display-1-3-2",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost_eq_sInf",
    upstreamDecl := "Chewi display (1.3.2)",
    upstreamFile := "Log-Concave Sampling, book page 20 / PDF page 32",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Kantorovich", "optimal-transport", "coupling", "source-display"],
    saldUse := "Chewi display (1.3.2): expose the exact infimum over coupling costs",
    note := "Definitional source equality; no minimizer is claimed."
  },
  {
    key := "measure.transport.chewi-definition-1-3-6",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.KantorovichDual.dualTransportValue",
    upstreamDecl := "Chewi Definition 1.3.6",
    upstreamFile := "Log-Concave Sampling, book page 21 / PDF page 33",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "optimal-transport", "Kantorovich-dual", "potentials", "definition"],
    saldUse := "Chewi Definition 1.3.6 root: define the supremum of integrable dual-potential objectives under the product-a.e. cost constraint",
    note := "Strong duality, boundedness, and attainment are separate theorems; the source P2 quadratic setting supplies their analytic hypotheses."
  },
  {
    key := "measure.transport.chewi-display-1-3-7",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.KantorovichDual.dualTransportValue_eq_sSup",
    upstreamDecl := "Chewi display (1.3.7)",
    upstreamFile := "Log-Concave Sampling, book page 21 / PDF page 33",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "optimal-transport", "Kantorovich-dual", "sSup", "display"],
    saldUse := "Chewi display (1.3.7): expand the dual transport value into its exact feasible-potential supremum",
    note := "Definitional equality; no primal-dual equality or optimizer is asserted."
  },
  {
    key := "measure.transport.coupling-probability",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Transport.isProbabilityMeasure_of_isCoupling_left",
    upstreamDecl := "Measure.fst_univ",
    upstreamFile := "Mathlib.MeasureTheory.Measure.Prod",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "coupling", "probability-measure", "marginal", "optimal-transport"],
    saldUse := "Chewi Definition 1.3.1: recover the joint probability-measure interface from a prescribed probability marginal",
    note := "The first marginal suffices because its mass on the whole space equals the joint measure's total mass; the symmetric result follows from Measure.snd_univ if needed."
  },
  {
    key := "measure.transport.product-coupling",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Transport.isCoupling_prod",
    upstreamDecl := "Measure.fst_prod / Measure.snd_prod",
    upstreamFile := "Mathlib.MeasureTheory.Measure.Prod",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "coupling", "optimal-transport", "product-measure", "Wasserstein"],
    saldUse := "Chewi Definition 1.3.1 and Chapters 1/4: named coupling contract with a canonical independent-product witness",
    note := "Defines the reusable marginal contract and proves nonemptiness for probability marginals; it does not define transport cost, prove existence of an optimal plan, or establish Wasserstein metric properties."
  },
  {
    key := "measure.law-map.integral",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Probability.LawMap.lawMapIntegral",
    upstreamDecl := "Mathlib.MeasureTheory.Measure.map / integral_map",
    upstreamFile := "Mathlib measure/integration APIs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["measure-map", "law", "integral"],
    saldUse := "rewrite weak-test integrals under endpoint laws and EM interpolation laws",
    note := "Alias to a compiled ASTIS theorem in Probability.lean."
  },
  {
    key := "measure.law-map.dominated-derivative",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Probability.LawMap.lawMapIntegralHasDerivAtOfDominated",
    upstreamDecl := "hasDerivAt_integral_of_dominated_loc_of_deriv_le",
    upstreamFile := "Mathlib.Analysis.Calculus.ParametricIntegral",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["parametric-integral", "dominated-convergence", "weak-test"],
    saldUse := "transport dominated sample-space derivatives to law-level weak-test derivatives",
    note := "Key backend for EM weak Fokker--Planck and KL-derivative handoffs."
  },
  {
    key := "measure.conditional-distribution.integral",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel.condDistribIntegralNamedLawIntegral",
    upstreamDecl := "condDistrib / condExpKernel map orientation",
    upstreamFile := "Mathlib.Probability.Kernel.CondDistrib and Condexp",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["conditional-law", "kernel", "Bochner-integral"],
    saldUse := "conditional frozen drift and named-law conditional integral interface",
    note := "Compiled ASTIS conditional-law bridge from Probability.lean."
  },
  {
    key := "probability.kernel.invariant-powers",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Probability.KernelInvariance.invariant_pow",
    upstreamDecl := "Kernel.Invariant.comp / Measure.id_comp / pow_succ",
    upstreamFile := "Mathlib.Probability.Kernel.Invariance; Mathlib.Probability.Kernel.Composition.Comp",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["KERN", "MCMC", "DiscreteSampling", "invariance", "iteration"],
    saldUse := "Shared MCMC/discrete kernel floor: propagate one-step target invariance through any finite number of transitions",
    note := "Source-neutral reusable edge; no ergodicity, mixing or complexity conclusion. bind_pow_eq is its notation adapter and is not counted separately."
  },
  {
    key := "conditional-kernel.named-field-integral",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel.condDistribIntegralNamedFieldIntegral",
    upstreamDecl := "condDistrib / compProd_map_condDistrib / integral_congr_ae",
    upstreamFile := "Mathlib.Probability.Kernel.CondDistrib and MeasureTheory integral APIs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["conditional-law", "kernel", "Bochner-integral", "versioning"],
    saldUse := "turn a named conditional drift component version into the joint-law weak-generator integral",
    note := "Pro-assimilated leaf: conditional-pairing/versioning backend separated from weak FP and Ito."
  },
  {
    key := "measure.with-density.probability-normalization",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.isProbabilityMeasure_withDensity_of_lintegral_eq_one",
    upstreamDecl := "withDensity_apply / IsProbabilityMeasure",
    upstreamFile := "Mathlib.MeasureTheory.Measure.WithDensity; Mathlib.MeasureTheory.Measure.Typeclasses.Probability",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "withDensity", "normalization", "probability-measure", "density"],
    saldUse := "Chewi DENS/MEAS root: turn normalized Gibbs or tilted density contracts into a probability measure",
    note := "Small measure-normalization wrapper; concrete Gibbs integrability remains a separate analytic leaf."
  },
  {
    key := "measure.with-density.ofReal-exp-probability-normalization",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.isProbabilityMeasure_withDensity_ofReal_exp_of_integral_eq_one",
    upstreamDecl := "ofReal_integral_eq_lintegral_ofReal / isProbabilityMeasure_withDensity_of_lintegral_eq_one",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Basic; AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym; SLT/GaussianLSI/DualityEntropy.lean as proof-pattern provenance",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "SLT", "withDensity", "exponential-tilt", "probability-measure", "entropy-duality", "Girsanov"],
    saldUse := "log-concave sampling DENS/MEAS/PATH root: normalize real exponential tilts for entropy duality, Gibbs variational formulas, and finite-dimensional Girsanov/RN routes",
    note := "ASTIS-owned exponential-tilt normalization leaf. It assumes integrability and unit mass of `exp U`; it does not prove DV duality, Girsanov, or any entropy inequality."
  },
  {
    key := "measure.density.normalized-lintegral-one",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.lintegral_inv_lintegral_mul_eq_one",
    upstreamDecl := "lintegral_const_mul' / ENNReal.inv_mul_cancel",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Lebesgue.Add; Mathlib.Data.ENNReal.Inv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "density", "lintegral", "normalization", "ENNReal"],
    saldUse := "Chewi DENS/MEAS root: normalize any finite nonzero density before specializing to Gibbs densities",
    note := "Generic reciprocal-lintegral normalization; no concrete measurability or integrability proof is hidden."
  },
  {
    key := "measure.with-density.normalized-probability",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.isProbabilityMeasure_withDensity_normalized_lintegral",
    upstreamDecl := "lintegral_inv_lintegral_mul_eq_one / withDensity_apply / IsProbabilityMeasure",
    upstreamFile := "Mathlib.MeasureTheory.Measure.WithDensity; Mathlib.MeasureTheory.Integral.Lebesgue.Add",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "withDensity", "density", "normalization", "probability-measure"],
    saldUse := "Chewi DENS/MEAS root: construct probability targets from finite nonzero unnormalized densities",
    note := "Bridges generic density normalization to the `withDensity` probability-measure contract."
  },
  {
    key := "measure.pi.lintegral-product-factorization",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.lintegral_fintype_prod_eq_prod",
    upstreamDecl := "ENNReal analogue of integral_fintype_prod_eq_prod",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Pi; external AST PiWithDensity.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Measure.pi", "lintegral", "product", "ENNReal", "Fubini"],
    saldUse := "Chewi MEAS/DENS root: factor finite-product ENNReal densities before tensorized withDensity or Gaussian shift leaves",
    note := "Compiled ASTIS-owned finite-product ENNReal Fubini leaf; useful beyond Gaussian tilts."
  },
  {
    key := "measure.pi.with-density-product",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.pi_withDensity_prod",
    upstreamDecl := "lintegral_fintype_prod_eq_prod / withDensity_apply",
    upstreamFile := "Mathlib.MeasureTheory.Measure.WithDensity; external AST PiWithDensity.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Measure.pi", "withDensity", "product-density", "tensorization"],
    saldUse := "Chewi MEAS/DENS root: decompose finite product density tilts into coordinatewise withDensity measures",
    note := "Shared root for product Gaussian Esscher, product Gibbs, and tensorization-style density constructions."
  },
  {
    key := "measure.pi.update-coordinate-map",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Product.map_update_prod_pi",
    upstreamDecl := "SLT.EfronStein.map_update_prod_pi",
    upstreamFile := "SLT/EfronStein.lean; Mathlib.MeasureTheory.Constructions.Pi",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "SLT", "Measure.pi", "product-measure", "Function.update", "finite-coordinate"],
    saldUse := "Chewi MEAS/FI/SDE root: replace one coordinate of a finite product sample by an independent coordinate draw while preserving the product law",
    note := "Finite product probability map leaf only; no conditional expectation theorem, entropy, LSI, kernel selection, weak-FP, or stationarity statement."
  },
  {
    key := "measure.pi.update-coordinate-map-preserving",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Product.measurePreserving_update_prod_pi",
    upstreamDecl := "SLT.EfronStein.map_update_prod_pi",
    upstreamFile := "SLT/EfronStein.lean; Mathlib.MeasureTheory.Constructions.Pi",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "SLT", "Measure.pi", "product-measure", "Function.update", "Fubini", "conditional-slice"],
    saldUse := "Chewi tensorization and coordinate-slice roots: treat coordinate replacement as a `MeasurePreserving` map before moving between product integrals and slices",
    note := "Measure-preserving wrapper for finite product probability laws only; coordinate slice integrability, entropy subadditivity, LSI, and conditional kernels remain separate leaves."
  },
  {
    key := "measure.pi.update-coordinate-integral",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Product.integral_update_prod_pi_eq_integral",
    upstreamDecl := "SLT.EfronStein.integral_update_eq_integral",
    upstreamFile := "SLT/EfronStein.lean; Mathlib.MeasureTheory.Integral.Prod",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "SLT", "Measure.pi", "Bochner-integral", "product-measure", "Function.update", "Fubini"],
    saldUse := "Chewi MEAS/FI/SDE root: rewrite the two-step integral over a fresh coordinate and a product sample back to the original product-law integral",
    note := "Bochner integral transport leaf derived from the coordinate replacement map; does not prove conditional expectation identities, entropy subadditivity, LSI, or sampler weak-FP statements."
  },
  {
    key := "measure.pi.update-coordinate-slice-integrable-ae",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Product.integrable_update_slice_ae",
    upstreamDecl := "SLT.GaussianLSI.SubAddEnt.Basic.integrable_update_slice / Integrable.prod_left_ae",
    upstreamFile := "SLT/GaussianLSI/SubAddEnt/Basic.lean; Mathlib.MeasureTheory.Integral.Prod",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "SLT", "Measure.pi", "Bochner-integral", "product-measure", "Function.update", "Fubini", "slice-integrability"],
    saldUse := "Chewi FI/MEAS root: expose a.e. integrability of coordinate-replacement slices before tensorization, conditional entropy, and product functional-inequality arguments",
    note := "A.e. slice integrability only; no conditional expectation identity, entropy subadditivity, LSI, Markov kernel construction, or Gibbs invariant-law statement."
  },
  {
    key := "measure.with-density.absolute-continuity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.withDensity_absolutelyContinuous_base",
    upstreamDecl := "withDensity_absolutelyContinuous",
    upstreamFile := "Mathlib.MeasureTheory.Measure.WithDensity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "withDensity", "absolute-continuity", "RN"],
    saldUse := "Chewi DENS/MEAS root before RN derivative and density-comparison leaves",
    note := "Callable ASTIS wrapper for the base absolute-continuity fact of withDensity."
  },
  {
    key := "measure.with-density.map-measurable-equiv",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.measurableEquiv_map_withDensity",
    upstreamDecl := "Measure.map_apply / withDensity_apply / setLIntegral_map",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Lebesgue.Map; Mathlib.MeasureTheory.Measure.WithDensity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "withDensity", "measure-map", "measurable-equivalence", "density-transport"],
    saldUse := "Chewi MEAS/PATH root: transport explicit densities through coordinate changes such as product coordinates to EuclideanSpace cylinders",
    note := "Generic Mathlib-ready transport leaf; it keeps density pushforward separate from any Gaussian or path-space theorem."
  },
  {
    key := "measure.rn-deriv.reconstruction",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.withDensity_rnDeriv_eq_of_absolutelyContinuous",
    upstreamDecl := "Measure.withDensity_rnDeriv_eq",
    upstreamFile := "Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Radon-Nikodym", "withDensity", "absolute-continuity"],
    saldUse := "Chewi DENS/MEAS root for recognizing supplied density/RN derivative representations",
    note := "Thin Mathlib-facing RN reconstruction leaf."
  },
  {
    key := "measure.gibbs-density.pointwise-positive-finite",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal_pos",
    upstreamDecl := "ENNReal.ofReal_pos / ENNReal.ofReal_lt_top / Real.exp_pos",
    upstreamFile := "Mathlib.Data.ENNReal.Real; Mathlib.Analysis.SpecialFunctions.Exp",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "positivity", "ENNReal"],
    saldUse := "Chewi DENS/MEAS root: expose positivity and finiteness of the Gibbs shape before integral contracts",
    note := "Companion finite-value theorem is `gibbsDensityENNReal_lt_top`; integral nonzero remains a measure-level hypothesis."
  },
  {
    key := "measure.gibbs-density.aemeasurable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.aemeasurable_gibbsDensityENNReal",
    upstreamDecl := "Real.measurable_exp / AEMeasurable.ennreal_ofReal",
    upstreamFile := "Mathlib.MeasureTheory.Function.SpecialFunctions.Basic; Mathlib.MeasureTheory.Constructions.BorelSpace.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "measurability", "ENNReal"],
    saldUse := "Chewi DENS/MEAS root: turn a measurable/a.e.-measurable potential into a measurable Gibbs density",
    note := "Keeps the measurable potential contract separate from convexity and integrability."
  },
  {
    key := "measure.gibbs-density.normalized-toReal-logconcave-convex-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_normalized_gibbsDensityENNReal_toReal_of_convexOn",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_of_convexOn / ENNReal.toReal_mul / ENNReal.toReal_inv",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "toReal", "log-concavity", "convex-potential", "normalization"],
    saldUse := "Chewi DENS/CONV root: view an ENNReal normalized Gibbs density with finite nonzero normalizer as a positive real log-concave density shape",
    note := "Requires supplied `Z ≠ 0` and `Z ≠ ∞`; it does not prove the normalizer exists or that a probability law has been constructed."
  },
  {
    key := "measure.gibbs-density.normalized-toReal-logconcave-strong-convex-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_normalized_gibbsDensityENNReal_toReal_of_strongConvexOn",
    upstreamDecl := "convexOn_of_strongConvexOn_nonneg / logConcaveOn_normalized_gibbsDensityENNReal_toReal_of_convexOn",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity; AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "toReal", "log-concavity", "strong-convexity", "normalization"],
    saldUse := "Chewi DENS/CONV root: expose normalized ENNReal Gibbs densities of strongly convex potentials as real log-concave shapes once `Z` is finite and nonzero",
    note := "Geometry/typing bridge only; finite normalizer, minimizer existence, invariant law, and PI/LSI remain separate obligations."
  },
  {
    key := "measure.gibbs-density.lintegral-normalized-toReal-logconcave-convex-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_lintegral_normalized_gibbsDensityENNReal_toReal_of_convexOn",
    upstreamDecl := "logConcaveOn_normalized_gibbsDensityENNReal_toReal_of_convexOn with `Z = ∫⁻ gibbsDensity`",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "toReal", "lintegral", "log-concavity", "convex-potential"],
    saldUse := "Chewi DENS/CONV root: match the source notation `Z^{-1} exp(-V)` when a finite nonzero Gibbs integral has already been proved",
    note := "The finite and nonzero lintegral hypotheses are inputs, not consequences of convexity."
  },
  {
    key := "measure.gibbs-density.lintegral-normalized-toReal-logconcave-strong-convex-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_lintegral_normalized_gibbsDensityENNReal_toReal_of_strongConvexOn",
    upstreamDecl := "logConcaveOn_normalized_gibbsDensityENNReal_toReal_of_strongConvexOn with `Z = ∫⁻ gibbsDensity`",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "toReal", "lintegral", "log-concavity", "strong-convexity"],
    saldUse := "Chewi DENS/CONV root: expose strong-convex Gibbs density shapes under a supplied finite nonzero Gibbs integral",
    note := "Requires `0 ≤ k`; sharp growth, minimizer existence, and finite normalization remain separate leaves."
  },
  {
    key := "measure.gibbs-density.lintegral-normalized-toReal-logconcave-strong-convex-minimizer",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_lintegral_normalized_gibbsDensityENNReal_toReal_of_strongConvexOn_minimizer",
    upstreamDecl := "lintegral_gibbsDensityENNReal_ne_zero / lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer / logConcaveOn_lintegral_normalized_gibbsDensityENNReal_toReal_of_strongConvexOn",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity; AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["log-concave-sampling", "Gibbs", "density", "toReal", "lintegral", "log-concavity", "strong-convexity", "minimizer"],
    saldUse := "log-concave sampling DENS/CONV root: combine the strong-convex minimizer finite-normalizer leaf with the normalized real log-concavity shape",
    note := "Convenience composition for finite-dimensional strongly convex targets with an exposed minimizer. It does not prove minimizer existence, invariant law, PI/LSI, or sampler convergence."
  },
  {
    key := "measure.gibbs-density.explicit-laplace-toReal-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity.logConcaveOn_normalized_laplace_gibbsDensityENNReal_toReal",
    upstreamDecl := "convexOn_univ_const_mul_abs_add / logConcaveOn_normalized_gibbsDensityENNReal_toReal_of_convexOn",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Laplace-tail", "toReal", "log-concavity", "normalizer", "one-dimensional"],
    saldUse := "Chewi DENS/CONV root: source-facing one-dimensional Laplace `ENNReal` Gibbs density as a real log-concave normalized shape",
    note := "Uses the explicit positive Laplace constant; the exact integral equality is provided by the separate Integrability normalizer leaf."
  },
  {
    key := "measure.gibbs-density.withDensity-integral-rewrite",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral.integral_withDensity_inv_mul_gibbsDensityENNReal_eq_integral_inv_mul_exp_smul",
    upstreamDecl := "integral_withDensity_eq_integral_toReal_smul₀ / gibbsDensityENNReal_lt_top",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral; Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Bochner-integral", "test-function-integral", "toReal"],
    saldUse := "Chewi MEAS/DENS/SDE root: rewrite Bochner integrals under a Gibbs withDensity measure as density-weighted base-measure integrals",
    note := "Algebraic Bochner-integral bridge only; stationarity, reversibility, KL/FI decay, and finite normalizer proofs remain separate leaves."
  },
  {
    key := "measure.gibbs-density.lintegral-withDensity-integral-rewrite",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral.integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul",
    upstreamDecl := "integral_withDensity_inv_mul_gibbsDensityENNReal_eq_integral_inv_mul_exp_smul with `Z = ∫⁻ gibbsDensity`",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Bochner-integral", "lintegral", "test-function-integral"],
    saldUse := "Chewi MEAS/DENS/SDE root: match the source density notation `Z^{-1} exp(-V(x)) dx` inside Bochner test-function integrals",
    note := "Consumes the nonzero normalizer hypothesis; if the goal needs a probability law, combine with the finite-normalizer probability leaf."
  },
  {
    key := "measure.gibbs-density.lintegral-withDensity-integral-rewrite-nonzero-base",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral.integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul_of_neZero",
    upstreamDecl := "integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul / lintegral_gibbsDensityENNReal_ne_zero",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "Bochner-integral", "lintegral", "nonzero-base-measure"],
    saldUse := "Chewi MEAS/DENS/SDE root: use textbook-shaped `Z = ∫ exp(-V)` Gibbs density inside Bochner test-function integrals without separately passing the nonzero-normalizer proof",
    note := "Derives only nonzero normalizer from `[NeZero μ]` and a.e.-measurability; finite normalizer and probability-measure status remain separate."
  },
  {
    key := "measure.gibbs-density.normalized-probability",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs",
    upstreamDecl := "isProbabilityMeasure_withDensity_normalized_lintegral",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym; Mathlib.MeasureTheory.Measure.WithDensity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "normalization", "probability-measure"],
    saldUse := "Chewi DENS/MEAS root: construct normalized Gibbs target measures once finite nonzero integral contracts are supplied",
    note := "First concrete Gibbs-density bridge; still does not prove coercivity or integrability of a specific potential."
  },
  {
    key := "measure.gibbs-density.integral-nonzero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_zero",
    upstreamDecl := "lintegral_eq_zero_iff' / Filter.eventually_false_iff_eq_bot / Real.exp_pos",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Lebesgue.Basic; Mathlib.Order.Filter.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "lintegral", "nonzero"],
    saldUse := "Chewi DENS/MEAS root: discharge the nonzero half of a Gibbs normalization constant over a nonzero base measure",
    note := "Requires a.e.-measurable potential and nonzero base measure; no growth or finiteness assumption is used."
  },
  {
    key := "measure.gibbs-density.integral-finite-envelope",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_top_of_ae_le",
    upstreamDecl := "lintegral_mono_ae / ne_top_of_le_ne_top",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Lebesgue.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "lintegral", "envelope", "finite"],
    saldUse := "Chewi DENS/MEAS root: reduce Gibbs integrability to a finite ENNReal envelope",
    note := "This is the target interface for later coercivity, tail, or quadratic-growth leaves."
  },
  {
    key := "measure.gibbs-density.potential-envelope-pointwise",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.gibbsDensityENNReal_le_of_potential_ge",
    upstreamDecl := "Real.exp_le_exp / ENNReal.ofReal_le_ofReal",
    upstreamFile := "Mathlib.MeasureTheory.Function.SpecialFunctions.Basic; Mathlib.Data.ENNReal.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "potential", "envelope", "monotonicity"],
    saldUse := "Chewi DENS/CONV root: turn a potential lower bound into a pointwise density envelope",
    note := "If `W ≤ V`, then `exp (-V) ≤ exp (-W)` as an ENNReal density."
  },
  {
    key := "measure.gibbs-density.integral-finite-potential-envelope",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge",
    upstreamDecl := "gibbsDensityENNReal_ae_le_of_ae_potential_ge / lintegral_gibbsDensityENNReal_ne_top_of_ae_le",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs; Mathlib.MeasureTheory.Integral.Lebesgue.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "potential", "lintegral", "envelope", "finite"],
    saldUse := "Chewi DENS/CONV root: prove finite normalization for `V` from an integrable lower-potential envelope `W`",
    note := "This is the compiled intermediate target before concrete coercivity or tail-growth leaves."
  },
  {
    key := "measure.gibbs-density.finite-measure-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_ge_const",
    upstreamDecl := "lintegral_const_lt_top / lintegral_gibbsDensityENNReal_ne_top_of_ae_le / lintegral_gibbsDensityENNReal_ne_zero",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs; Mathlib.MeasureTheory.Integral.Lebesgue.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "density", "finite-measure", "lower-bound", "normalization", "compact-domain"],
    saldUse := "Chewi DENS/CONV root: normalize Gibbs laws on finite or truncated base measures from a measurable potential with an a.e. constant lower bound",
    note := "Concrete compact-domain envelope leaf; full Lebesgue coercivity/growth tail integrability remains a separate analytic theorem."
  },
  {
    key := "measure.gibbs-density.normalized-probability-envelope",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_le",
    upstreamDecl := "lintegral_gibbsDensityENNReal_ne_zero / lintegral_gibbsDensityENNReal_ne_top_of_ae_le",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs; Mathlib.MeasureTheory.Measure.WithDensity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "normalization", "envelope", "probability-measure"],
    saldUse := "Chewi DENS/MEAS root: turn a measurable potential plus finite envelope into a normalized Gibbs probability measure",
    note := "Keeps coercivity/growth work isolated as the proof of the envelope bound."
  },
  {
    key := "measure.gibbs-density.normalized-probability-potential-envelope",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_potential_ge",
    upstreamDecl := "lintegral_gibbsDensityENNReal_ne_zero / lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs; Mathlib.MeasureTheory.Measure.WithDensity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "withDensity", "potential", "normalization", "envelope", "probability-measure"],
    saldUse := "Chewi DENS/CONV root: construct the normalized target law once a lower-potential integrable envelope is supplied",
    note := "Useful for Chewi coercivity/growth proofs because the analytic tail estimate only has to provide `W ≤ V` and finite integral for `exp(-W)`."
  }
]



def functionalInequalityMemory : List LemmaMemoryEntry := [
  {
    key := "functional-inequality.gibbs-local-l2",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedLocalL2.lp_locallyMemLp_volume",
    upstreamDecl := "memLp_two_iff_integrable_sq_norm; integrable_tilted_iff; absolutelyContinuous_tilted",
    upstreamFile := "Mathlib MeasureTheory; authored PBPS arXiv2609.06905v1 Appendix C.1 prerequisite",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["MEAS", "FI", "Gibbs", "local-integrability"],
    saldUse := "Actual weak-resolvent solution, gradient and forcing acquire compact unweighted L2 inputs.",
    note := "Continuous potential and finite Gibbs normalization; arbitrary normed additive target. No global L2 bound, H2, Poincare or paper completion."
  },
  {
    key := "functional-inequality.chewi-definition-1-2-19",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Generator.SatisfiesPoincare",
    upstreamDecl := "Chewi Definition 1.2.19",
    upstreamFile := "Log-Concave Sampling, book page 16 / PDF page 28",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Poincare", "generator", "Dirichlet-form", "variance", "definition"],
    saldUse := "Chewi Definition 1.2.19 root: state the general generator Poincare inequality on every finite-integral observable",
    note := "Exact reversible-generator formulation. The gradient-energy specialization and PI-to-decay equivalence are separate theorem routes."
  },
  {
    key := "functional-inequality.chewi-definition-1-2-25",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Generator.SatisfiesLogSobolev",
    upstreamDecl := "Chewi Definition 1.2.25",
    upstreamFile := "Log-Concave Sampling, book page 18 / PDF page 30",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-Sobolev", "generator", "Dirichlet-form", "density", "definition"],
    saldUse := "Chewi Definition 1.2.25 root: state KL(rho mu || mu) <= (C/2) E(rho,log rho) for every admissible normalized density",
    note := "Exact density-generator formulation with positivity, normalization, and finite entropy/energy conditions explicit. KL decay is a separate theorem route."
  },
  {
    key := "gronwall.chewi-lemma-1-2-20",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.chewi_lemma_1_2_20",
    upstreamDecl := "le_gronwallBound_of_liminf_deriv_right_le / gronwallBound_ε0",
    upstreamFile := "Mathlib.Analysis.ODE.Gronwall; Log-Concave Sampling, book page 16 / PDF page 28",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gronwall", "differential-inequality", "exponential-bound", "Chapter-1"],
    saldUse := "Chewi Lemma 1.2.20: turn g'(t) ≤ c g(t) on [0,T] into g(t) ≤ g(0) exp(ct)",
    note := "Source-faithful differentiable scalar specialization of Mathlib's more general one-sided-slope Gronwall theorem."
  },
  {
    key := "semigroup-decay.from-arbitrary-time",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.exponential_decay_of_scaled_dissipation_from",
    upstreamDecl := "le_gronwallBound_of_liminf_deriv_right_le / time translation",
    upstreamFile := "Mathlib.Analysis.ODE.Gronwall",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "functional-inequality", "semigroup", "dissipation", "shifted-time", "exponential-decay"],
    saldUse := "propagate a coercive energy-dissipation inequality exponentially between arbitrary starting and terminal times",
    note := "Shifted-time strengthening of the zero-time Gronwall leaf; the concrete energy and dissipation remain explicit inputs."
  },
  {
    key := "semigroup-decay.converse-from-shifted-exponential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.scaled_dissipation_of_exponential_decay",
    upstreamDecl := "IsLocalMaxOn.hasFDerivWithinAt_nonpos / one_mem_posTangentConeAt_iff_frequently",
    upstreamFile := "Mathlib.Analysis.Calculus.LocalExtr.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "functional-inequality", "semigroup", "converse", "right-derivative", "Fermat"],
    saldUse := "recover instantaneous coercivity from exponential decay valid after every starting time",
    note := "Uses a one-sided local-maximum comparison with the exponential envelope; this is the scalar converse mechanism, not a concrete semigroup construction."
  },
  {
    key := "semigroup-decay.chewi-theorem-1-2-21-scalar-equivalence",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.chewi_theorem_1_2_21_scalar_equivalence",
    upstreamDecl := "Chewi Theorem 1.2.21, scalar energy-dissipation equivalence",
    upstreamFile := "Log-Concave Sampling, book page 16 / PDF page 28",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Poincare", "variance", "semigroup", "equivalence", "exponential-decay"],
    saldUse := "equate Poincare-style coercivity with shifted variance-style exponential decay under the exact -2 dissipation identity",
    note := "Full scalar equivalence. Instantiating variance for a reversible Markov semigroup and extending from a smooth core remain downstream."
  },
  {
    key := "semigroup-decay.chewi-theorem-1-2-22-scalar-equivalence",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.chewi_theorem_1_2_22_scalar_equivalence",
    upstreamDecl := "Chewi Theorem 1.2.22, scalar energy-dissipation equivalence",
    upstreamFile := "Log-Concave Sampling, book page 17 / PDF page 29",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Poincare", "chi-square", "semigroup", "equivalence", "exponential-decay"],
    saldUse := "equate Poincare-style coercivity with shifted chi-square-style exponential decay under the exact -2 dissipation identity",
    note := "The density/Radon-Nikodym realization of chi-square is not hidden in this scalar theorem."
  },
  {
    key := "semigroup-decay.chewi-theorem-1-2-26-scalar-equivalence",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.chewi_theorem_1_2_26_scalar_equivalence",
    upstreamDecl := "Chewi Theorem 1.2.26, scalar entropy-dissipation equivalence",
    upstreamFile := "Log-Concave Sampling, book page 18 / PDF page 30",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-Sobolev", "KL", "Fisher-information", "equivalence", "exponential-decay"],
    saldUse := "equate LSI-style coercivity with shifted KL exponential decay under the exact entropy-dissipation identity",
    note := "Full scalar equivalence. Concrete density regularity, KL/FI differentiation, and domain closure remain downstream."
  },
  {
    key := "semigroup-decay.scaled-dissipation",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.exponential_decay_of_scaled_dissipation",
    upstreamDecl := "le_gronwallBound_of_liminf_deriv_right_le / gronwallBound_ε0",
    upstreamFile := "Mathlib.Analysis.ODE.Gronwall",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "functional-inequality", "semigroup", "dissipation", "Gronwall", "exponential-decay"],
    saldUse := "generic scalar bridge from a coercive energy-dissipation inequality to exponential semigroup decay",
    note := "Uses an exact one-sided HasDerivWithinAt identity and Mathlib Gronwall; it does not construct the concrete variance, KL, or Fisher-information curve."
  },
  {
    key := "semigroup-decay.chewi-theorem-1-2-21-forward",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.chewi_theorem_1_2_21_forward",
    upstreamDecl := "Chewi Theorem 1.2.21, forward implication",
    upstreamFile := "Log-Concave Sampling, book page 16 / PDF page 28",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Poincare", "variance", "semigroup", "exponential-decay", "forward"],
    saldUse := "derive variance-style decay at rate 2/C from Poincare coercivity and the -2 Dirichlet-energy dissipation identity",
    note := "Source-faithful forward direction only; the converse and the concrete reversible-semigroup identification remain obligations."
  },
  {
    key := "semigroup-decay.chewi-theorem-1-2-22-forward",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.chewi_theorem_1_2_22_forward",
    upstreamDecl := "Chewi Theorem 1.2.22, forward implication",
    upstreamFile := "Log-Concave Sampling, book page 17 / PDF page 29",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Poincare", "chi-square", "semigroup", "exponential-decay", "forward"],
    saldUse := "derive chi-square-style decay at rate 2/C from Poincare coercivity and the -2 energy dissipation identity",
    note := "The theorem deliberately reuses the scalar PI decay mechanism and does not assert a concrete density evolution."
  },
  {
    key := "semigroup-decay.chewi-theorem-1-2-26-forward",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay.chewi_theorem_1_2_26_forward",
    upstreamDecl := "Chewi Theorem 1.2.26, forward implication",
    upstreamFile := "Log-Concave Sampling, book page 18 / PDF page 30",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-Sobolev", "KL", "Fisher-information", "semigroup", "exponential-decay", "forward"],
    saldUse := "derive KL-style decay at rate 2/C from LSI coercivity and the entropy-dissipation identity KL'=-FI",
    note := "Source-faithful forward direction only; density regularity, concrete entropy dissipation, and the converse remain explicit."
  }
]

def stochasticProcessMemory : List LemmaMemoryEntry := [
  {
    key := "localization.chewi-proposition-1-1-13",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CanonicalLocalizationTheorem.chewi_proposition_1_1_13",
    upstreamDecl := "Chewi Proposition 1.1.13",
    upstreamFile := "Log-Concave Sampling, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "stopping-time", "progressive-L2"],
    saldUse := "package the canonical energy first-hitting times, terminal convergence, and stopped global-L2 bound into the exact Chapter 1 source result",
    note := "Display (1.1.14) and Proposition 1.1.16 remain separate theorem routes; both are now compiled, so this entry records only the canonical localization component."
  },
  {
  key := "localization.chewi-display-1-1-14",
  localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CanonicalStoppedItoIntegral.chewi_display_1_1_14",
  upstreamDecl := "Chewi display (1.1.14)",
  upstreamFile := "Log-Concave Sampling, book page 7 / PDF page 19",
  status := LemmaMemoryStatus.formalizedLocal,
  tags := ["Chewi", "Ito", "localization", "stopped-integral", "continuous-martingale"],
  saldUse := "package each canonical energy truncation as a globally L2 Ito integrand whose Ito process is adapted, continuous, martingale, and compatible with deterministic-time restriction",
  note := "This compiles the intermediate stopped-global-Ito display. Arbitrary random-stopping consistency and cross-horizon gluing are discharged separately by Proposition 1.1.16."
},
{
  key := "localization.chewi-proposition-1-1-16",
  localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ChewiProposition1_1_16.chewi_proposition_1_1_16",
  upstreamDecl := "Chewi Proposition 1.1.16",
  upstreamFile := "Log-Concave Sampling, book page 7 / PDF page 19",
  status := LemmaMemoryStatus.formalizedLocal,
  tags := ["Chewi", "Ito", "local-martingale", "localization", "random-stopping", "continuous-paths"],
  saldUse := "package random-stopping consistency, cross-horizon overlap, localized martingale coherence, and pathwise gluing into the source local-Ito continuous-local-martingale result",
  note := "Uses the canonical localizers from Proposition 1.1.13; stopped-integral compatibility, stopping-graph nullity, and cross-horizon gluing are all compiled."
},
  {
    key := "localization.completed-integrand-progressive",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompletedIntegrand.completedIntegrand_stronglyProgressive",
    upstreamDecl := "Progressiveness after completing the null bad-path set",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "completion", "progressive"],
    saldUse := "replace nonintegrable sample paths by zero while preserving the progressive sigma-algebra",
    note := "The source local-L2 domain assumes only almost-sure finite path energy. Usual-condition completeness makes the null replacement measurable at every filtration time."
  },
  {
    key := "localization.energy-stopped-path-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.EnergyStoppedIntegrand.integral_energyStoppedIntegrand_sq_le",
    upstreamDecl := "Pathwise square-energy bound after canonical stopping",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "stopped-integrand", "energy-bound"],
    saldUse := "bound each stopped path by its canonical energy level before taking expectation",
    note := "The threshold representation is proved equivalent almost everywhere in time to stopping before the equality-level localizer. No expected-energy hypothesis is used."
  },
  {
    key := "localization.stopped-progressive-l2",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.EnergyStoppedProgressiveL2.stoppedProgressiveL2",
    upstreamDecl := "Global progressive product-L2 membership after energy stopping",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "progressive-L2", "Tonelli"],
    saldUse := "feed each canonical stopped integrand into the global Ito integral constructed in Theorem 1.1.8",
    note := "Tonelli integrates the pathwise level bound over the probability measure. The stopped-integral identity and local-martingale consistency remain downstream."
  },
  {
    key := "localization.completed-energy-process",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompletedEnergy.continuous_completedEnergy",
    upstreamDecl := "Everywhere-continuous completed accumulated energy",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "completion", "continuous-path"],
    saldUse := "replace the null set of nonintegrable paths without losing filtration measurability",
    note := "Usual-condition completeness makes the null bad set measurable at every time; all completed paths are continuous, monotone, and nonnegative."
  },
  {
    key := "localization.canonical-energy-stopping-time",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CanonicalEnergyStoppingTime.canonicalLocalizingTime_isChewiStoppingTime",
    upstreamDecl := "Stopping-time property of the canonical integer energy localizer",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "stopping-time", "first-hit"],
    saldUse := "supply the stopping-time component of Chewi's canonical localizing sequence",
    note := "The first equality-level time is characterized by a fixed-time completed-energy threshold event; the proof uses continuity and the intermediate value theorem."
  },
  {
    key := "localization.canonical-localizer-monotone-terminal",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CanonicalEnergyLocalizer.tendsto_canonicalLocalizingTime",
    upstreamDecl := "Monotone canonical localizers eventually equal the terminal horizon",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "monotone", "Tendsto"],
    saldUse := "establish pathwise monotonicity and terminal convergence of the canonical localizing sequence",
    note := "Once the integer level exceeds finite terminal completed energy, its equality-level set is empty and the localizer equals T. Stopped-integrand global L2 and the stopped-integral identity remain downstream."
  },
  {
    key := "localization.canonical-stopped-energy-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CanonicalEnergyLocalizer.completedEnergy_at_canonicalLocalizingTime_le",
    upstreamDecl := "Canonical localizer bounds stopped completed energy by n+1",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "energy-bound", "stopped-integrand"],
    saldUse := "provide the deterministic energy bound needed to place every stopped integrand in global product L2",
    note := "The bound is exact on reached levels and uses terminal fallback when the level is not reached. Progressive stopped-integrand measurability remains downstream."
  },
  {
    key := "analysis.prefix-integral-continuity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Analysis.PrefixIntegral.continuous_prefixIntegral",
    upstreamDecl := "Continuity of finite-horizon moving prefix integrals",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "analysis", "Bochner-integral", "continuity", "localization"],
    saldUse := "supply the analytic continuity theorem for accumulated square energy",
    note := "The proof uses dominated convergence on the repository's finite NNReal time measure and treats the moving endpoint singleton as a null set."
  },
  {
    key := "localization.energy-path-continuity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.EnergyPathContinuity.continuous_accumulatedEnergyReal_ae",
    upstreamDecl := "Almost-sure continuity of accumulated progressive square energy",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "energy", "continuity"],
    saldUse := "justify the first-hitting canonical localizer by a continuous monotone energy path",
    note := "The theorem starts from progressive measurability and almost-sure finite path energy; the stopping-time and stopped-integrand theorems remain downstream."
  },
  {
    key := "localization.fixed-time-energy-measurability",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LocalProgressiveL2.accumulatedEnergyReal_stronglyMeasurable",
    upstreamDecl := "Fixed-time filtration measurability of accumulated square energy",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "progressive", "filtration", "energy"],
    saldUse := "make canonical energy-hitting events measurable at each observation time",
    note := "The source domain assumes only almost-sure finite path energy, not finite expected energy. Continuity and the first-hitting stopping-time theorem remain downstream."
  },
  {
    key := "localization.accumulated-energy-monotonicity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.AccumulatedEnergy.accumulatedEnergy_mono",
    upstreamDecl := "Monotonicity of accumulated pathwise square energy",
    upstreamFile := "Log-Concave Sampling, Proposition 1.1.13, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "energy", "stopping-time"],
    saldUse := "supply the monotone nonnegative path-energy process used by the canonical localizing sequence",
    note := "This is an exact ENNReal integral leaf. Fixed-time filtration measurability, path continuity on the finite-energy set, and the first-hitting stopping time remain downstream."
  },
  {
    key := "brownian-motion.chewi-definition-1-1-1",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.IsStandardBrownianMotion",
    upstreamDecl := "ProbabilityTheory.HasLaw / ProbabilityTheory.iIndepFun / ProbabilityTheory.gaussianReal / Chewi Definition 1.1.1",
    upstreamFile := "Mathlib.Probability.Distributions.Gaussian.Basic; Mathlib.Probability.Independence.Basic; Log-Concave Sampling, book page 4 / PDF page 16",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Brownian-motion", "Gaussian", "independent-increments", "continuous-paths"],
    saldUse := "Chewi Definition 1.1.1 root: expose zero start, independent increments, centered isotropic Gaussian increment laws, and almost-sure path continuity",
    note := "The vector Gaussian law is stated through every continuous-linear projection, matching Mathlib's coordinate-free Gaussian interface. Existence and construction remain separate theorems."
  },
  {
    key := "ito-integral.usual-filtration-conditions",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2.SatisfiesUsualConditions",
    upstreamDecl := "Complete right-continuous filtered probability space",
    upstreamFile := "Log-Concave Sampling, book page 4 / PDF page 16; Mathlib.Probability.Process.Filtration",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "filtration", "complete", "right-continuous"],
    saldUse := "package the usual filtration conditions required by continuous-time stochastic calculus",
    note := "Completeness is stated as inclusion of every ambient measure-null set at every time; right continuity reuses Mathlib's right-continuation interface."
  },
  {
    key := "ito-integral.progressive-l2-domain",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2.ProgressiveL2Integrand",
    upstreamDecl := "Progressive globally square-integrable stochastic integrand",
    upstreamFile := "Log-Concave Sampling, Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "progressive", "L2", "product-measure"],
    saldUse := "retain filtration information together with the probability-time L2 representative used by Ito completion",
    note := "This is the source domain, not an Ito-integral existence theorem; adapted elementary density and continuous martingale construction remain downstream."
  },
  {
    key := "ito-integral.progressive-l2-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2Algebra.toLp_smul",
    upstreamDecl := "Real vector-space closure of progressive L2 integrands",
    upstreamFile := "Log-Concave Sampling, construction in Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "progressive", "L2", "linearity"],
    saldUse := "assemble linear combinations of progressive square-integrable integrands while preserving their canonical product-space Lp representatives",
    note := "Zero, addition, negation, subtraction, and real scalar multiplication are constructed with exact toLp compatibility. This does not provide elementary density or the Ito extension."
  },
  {
    key := "ito-integral.progressive-l2-restriction",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2.ProgressiveL2Integrand.norm_restrictAt_le",
    upstreamDecl := "L2 contraction under terminal-time restriction",
    upstreamFile := "Log-Concave Sampling, Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "progressive", "restriction", "L2-contraction"],
    saldUse := "define time-indexed terminal Ito maps without increasing integrand energy",
    note := "Restriction uses a strict endpoint representative, equivalent to the closed interval convention under Lebesgue time measure."
  },
  {
    key := "ito-elementary.same-grid-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoAlgebra.elementaryItoIntegral_sub",
    upstreamDecl := "Linearity of elementary Ito integration on a fixed adapted time grid",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "linearity", "common-grid"],
    saldUse := "keep differences of same-grid elementary approximants inside the elementary Ito domain",
    note := "Zero, negation, scalar multiplication, addition, and subtraction are constructed with pointwise and finite-integral linearity. Common-grid refinement and density remain downstream obligations."
  },
  {
    key := "ito-elementary.progressive-l2-embedding",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoEmbedding.toProgressiveL2",
    upstreamDecl := "Elementary adapted processes lie in the progressive L2 integrand domain",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "progressive", "L2"],
    saldUse := "compare elementary approximants and general progressive integrands in one product-space L2 domain",
    note := "Joint strong measurability, strong progressiveness, a finite coefficient bound, and product-space MemLp are proved before constructing the canonical embedding. Density remains open."
  },
  {
    key := "ito-elementary.terminal-l2-isometry",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoL2.norm_elementaryItoTerminalToLp",
    upstreamDecl := "Elementary terminal Ito map is an L2 isometry",
    upstreamFile := "Log-Concave Sampling, displays (1.1.5)--(1.1.6), book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "L2", "linear-isometry"],
    saldUse := "transfer Cauchy control from same-grid elementary integrands to terminal stochastic sums",
    note := "Both sides are actual Lp elements and their norms are proved equal from the expectation-level isometry. Adapted density, common refinement, and completion remain downstream."
  },
  {
    key := "ito-elementary.terminal-l2-inner-isometry",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoL2.inner_elementaryItoTerminalToLp",
    upstreamDecl := "Elementary Ito inner-product isometry on a common grid",
    upstreamFile := "Log-Concave Sampling, displays (1.1.5)--(1.1.9), book pages 5--6 / PDF pages 17--18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "L2", "inner-product", "isometry"],
    saldUse := "transport Hilbert-space Cauchy and orthogonality arguments from elementary integrands to terminal stochastic integrals",
    note := "Derived by polarization from the actual norm isometry after proving same-grid addition on both Lp sides. Different-grid refinement and general completion remain open."
  },
  {
    key := "ito-integral.coefficient-l2-truncation",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CoefficientTruncation.tendsto_clipNat_toLp",
    upstreamDecl := "Bounded truncation approximation in L2",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "L2", "truncation", "dominated-convergence"],
    saldUse := "replace square-integrable real coefficients by bounded measurable coefficients without changing their L2 limit",
    note := "The clipping map is proved measurable, norm dominated, eventually pointwise equal, and convergent in the actual Lp space. Adapted elementary density still requires time discretization and filtration-aware approximation."
  },
  {
    key := "ito-integral.progressive-l2-truncation",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2Truncation.tendsto_clipped_toLp",
    upstreamDecl := "Bounded progressive truncation in product-space L2",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "progressive", "L2", "truncation", "product-measure"],
    saldUse := "reduce a progressive square-integrable process to uniformly bounded progressive processes in product-space L2",
    note := "Clipping is lifted to the full ProgressiveL2Integrand structure and convergence is proved in its actual Lp representative. Causal time regularization and elementary density remain open."
  },
  {
    key := "ito-integral.dyadic-clipped-elementary-construction",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SampledElementaryApproximation.sampledClippedDyadic",
    upstreamDecl := "Dyadic bounded adapted left-step approximation object",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "dyadic-grid", "adapted", "truncation"],
    saldUse := "construct genuine bounded elementary adapted processes from deterministic left-endpoint samples of a progressive L2 process",
    note := "The strict grid, left-endpoint filtration measurability, coefficient bound, and terminal endpoint are proved. L2 time-regularization, convergence, and the diagonal density theorem remain open."
  },
  {
    key := "ito-integral.lagged-dyadic-adapted-average",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LaggedDyadicApproximation.laggedDyadicApprox_isElementaryAdapted",
    upstreamDecl := "Lagged dyadic cell-average approximation by bounded adapted elementary processes",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18; Mathlib.MeasureTheory.Integral.Prod",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "dyadic-grid", "adapted", "Bochner-integral"],
    saldUse := "regularize progressive L2 integrands causally: average a clipped process over the preceding cell and use that coefficient on the next cell",
    note := "Parameterized Bochner measurability is proved from progressive measurability after an explicit zero extension, and every coefficient is bounded by the clipping level. L2 convergence of the lagged averages remains open."
  },
  {
    key := "ito-integral.lagged-dyadic-l2-convergence",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LaggedDyadicConvergence.tendsto_laggedDyadicApprox_toLp_clipped",
    upstreamDecl := "Lagged dyadic adapted averages converge in product-space L2",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "dyadic", "adapted", "L2-convergence"],
    saldUse := "replace a bounded progressive integrand by causal elementary adapted processes in the actual product L2 space",
    note := "Lebesgue differentiation, active-cell geometry, product-a.e. transfer, and dominated convergence are all explicit."
  },
  {
    key := "ito-integral.progressive-elementary-density",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2Density.progressiveL2_elementary_dense",
    upstreamDecl := "Bounded dyadic elementary adapted processes are dense in progressive L2",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "density", "progressive", "fast-diagonal"],
    saldUse := "supply fast nested-grid elementary approximants for terminal completion and pathwise Borel-Cantelli control",
    note := "The noncomputable diagonal chooses increasing truncation and dyadic levels with summable quantitative errors."
  },
  {
    key := "ito-integral.dyadic-refinement",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement.norm_terminal_sub_eq_process_sub",
    upstreamDecl := "Common dyadic refinement preserves elementary processes and Ito terminal sums",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "dyadic", "refinement", "isometry"],
    saldUse := "compare heterogeneous elementary approximants on a shared grid without changing either L2 representative",
    note := "Coefficient replication, filtration monotonicity, finite Brownian-increment telescoping, and the distance isometry are proved."
  },
  {
    key := "ito-integral.terminal-isometry",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTerminalCompletion.itoIntegralTerminal_norm",
    upstreamDecl := "General terminal Ito integral by L2 completion",
    upstreamFile := "Log-Concave Sampling, Theorem 1.1.8 and display (1.1.9), book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "L2-completion", "terminal-map", "isometry"],
    saldUse := "extend elementary stochastic integration uniquely and linearly to every progressive globally square-integrable integrand",
    note := "The definition uses completeness of Lp; the universal approximation theorem removes dependence on the canonical choice sequence."
  },
  {
    key := "ito-integral.elementary-martingale",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoProcess.elementaryItoProcess_martingale",
    upstreamDecl := "Elementary Ito integral process is a continuous martingale",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "martingale", "continuous-paths"],
    saldUse := "lift terminal elementary sums to adapted time-indexed martingales before taking the uniform path limit",
    note := "Conditional mean-zero future increments prove the martingale identity; Brownian path continuity proves a.e. continuity."
  },
  {
    key := "ito-integral.doob-l2",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ContinuousDoobL2.doobL2_continuous",
    upstreamDecl := "Doob L2 maximal control for continuous martingales",
    upstreamFile := "Log-Concave Sampling, proof of Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "Doob", "maximal-inequality", "continuous-martingale"],
    saldUse := "turn summable terminal L2 approximation errors into summable uniform path-deviation events",
    note := "The finite discrete inequality is proved first and then extended to continuous paths through nested dyadic observation grids."
  },
  {
    key := "ito-integral.continuous-martingale",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.itoIntegralProcess_martingale",
    upstreamDecl := "Continuous adapted general Ito integral process",
    upstreamFile := "Log-Concave Sampling, Theorem 1.1.8, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "Borel-Cantelli", "continuous-martingale", "restriction"],
    saldUse := "construct the actual continuous martingale version and identify every fixed time with the restricted terminal completion",
    note := "A summable Doob-Borel-Cantelli argument gives a uniform path limit; usual-condition completeness makes the null-set patch adapted."
  },
  {
    key := "ito-integral.chewi-theorem-1-1-8",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.chewi_theorem_1_1_8",
    upstreamDecl := "Chewi Theorem 1.1.8",
    upstreamFile := "Log-Concave Sampling, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "progressive", "martingale", "uniqueness"],
    saldUse := "provide the source-facing existence, adaptedness, martingale, continuity, fixed-time compatibility, isometry, and indistinguishability interface",
    note := "This theorem packages constructed objects and proved properties; it assumes no abstract stochastic-integral contract."
  },
  {
    key := "ito-integral.chewi-display-1-1-9",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.chewi_display_1_1_9",
    upstreamDecl := "Chewi display (1.1.9)",
    upstreamFile := "Log-Concave Sampling, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "isometry", "fixed-time", "L2"],
    saldUse := "rewrite every fixed-time stochastic-integral second moment as the product-space energy of the time-restricted integrand",
    note := "The strict endpoint convention differs from the closed interval only on a null singleton and is the exact Lean representative used by restrictAt."
  },
  {
    key := "brownian-motion.filtration-contract",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.IsBrownianMotionWithFiltration",
    upstreamDecl := "Brownian motion relative to a filtration",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17; Mathlib.Probability.BrownianMotion.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian-motion", "filtration", "adapted", "independent-increments"],
    saldUse := "ensure future Brownian increments are independent of the whole past sigma-algebra used by adapted coefficients",
    note := "This strengthens bare independent increments by making the filtration explicit; it does not claim existence for an arbitrary enlarged filtration."
  },
  {
    key := "brownian-motion.conditional-increment-mean-zero",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.IsBrownianMotionWithFiltration.condExp_increment_eq_zero",
    upstreamDecl := "Conditional mean-zero Brownian increment",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17; Mathlib.Probability.ConditionalExpectation",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian-motion", "conditional-expectation", "filtration", "martingale-increment"],
    saldUse := "remove future increments after conditioning on the left-endpoint filtration",
    note := "Derived from filtration-level independence and the centered Brownian law under an explicit probability-measure instance."
  },
  {
    key := "brownian-motion.increment-second-moment",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.IsBrownianMotionWithFiltration.integral_increment_sq",
    upstreamDecl := "Brownian increment second moment",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17; Mathlib.Probability.BrownianMotion.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian-motion", "second-moment", "variance", "Ito"],
    saldUse := "replace an increment-square expectation by its elapsed time",
    note := "Uses Mathlib's Brownian covariance formula and keeps the ordered nonnegative-time subtraction explicit."
  },
  {
    key := "brownian-motion.conditional-increment-second-moment",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.IsBrownianMotionWithFiltration.condExp_increment_sq",
    upstreamDecl := "Conditional Brownian increment second moment",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17; Mathlib.Probability.ConditionalExpectation",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian-motion", "conditional-expectation", "second-moment", "filtration", "Ito"],
    saldUse := "evaluate the conditional variance of a future Brownian increment at the left endpoint",
    note := "The square-increment sigma-algebra is explicitly shown to be below the increment sigma-algebra before applying conditional-expectation independence."
  },
  {
    key := "ito-elementary.chewi-display-1-1-2",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIntegral.chewi_display_1_1_2",
    upstreamDecl := "Chewi display (1.1.2)",
    upstreamFile := "Log-Concave Sampling, book page 4 / PDF page 16",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "adapted", "finite-sum"],
    saldUse := "source-faithful elementary adapted-process root for the Ito construction",
    note := "The structure records a strict grid, left-endpoint filtration measurability, and bounded coefficients; no L2 completion is claimed."
  },
  {
    key := "ito-elementary.chewi-display-1-1-3",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIntegral.chewi_display_1_1_3",
    upstreamDecl := "Chewi display (1.1.3)",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "Brownian-increment", "elementary-process", "finite-sum"],
    saldUse := "finite-sum definition used before proving orthogonality and the elementary Ito isometry",
    note := "This is the exact stopped Brownian-increment sum for an elementary process; the isometry and L2 extension remain downstream."
  },
  {
    key := "ito-elementary.weighted-increment-second-moment",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIsometry.integral_weightedIncrement_sq",
    upstreamDecl := "Adapted weighted Brownian-increment diagonal term",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "adapted", "Brownian-increment", "second-moment"],
    saldUse := "factor each diagonal Ito-isometry term into coefficient energy and clipped interval length",
    note := "The coefficient is left-endpoint measurable and independent of the future increment; both factors are proved integrable."
  },
  {
    key := "ito-elementary.weighted-increment-orthogonality",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIsometry.integral_weightedIncrement_mul_eq_zero",
    upstreamDecl := "Orthogonality of distinct adapted weighted Brownian increments",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "adapted", "orthogonality", "filtration"],
    saldUse := "eliminate cross terms in finite elementary stochastic-integral squares",
    note := "The proof orders the intervals, proves the earlier weighted term is measurable at the later left endpoint, and factors against the centered future increment."
  },
  {
    key := "ito-elementary.chewi-display-1-1-5",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIsometry.chewi_display_1_1_5",
    upstreamDecl := "Chewi display (1.1.5)",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "elementary-process", "orthogonality", "finite-sum"],
    saldUse := "expand the square of an elementary stochastic integral and retain only diagonal terms",
    note := "This is an expectation identity, not merely a finite-sum algebra lemma; integrability and cross-term orthogonality are proved."
  },
  {
    key := "ito-elementary.process-l2-energy-value",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIsometry.processL2Energy_value",
    upstreamDecl := "Elementary-process product-space L2 energy",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "L2", "product-measure", "time-measure"],
    saldUse := "evaluate elementary-process energy as the sum of coefficient energies times clipped cell lengths",
    note := "Disjoint time cells are integrated against the stopped NNReal Lebesgue measure and then Tonelli identifies the product-space energy."
  },
  {
    key := "ito-elementary.chewi-display-1-1-6",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIsometry.chewi_display_1_1_6",
    upstreamDecl := "Chewi display (1.1.6)",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "isometry", "elementary-process", "L2"],
    saldUse := "identify the second moment of the elementary Ito integral with its product-space integrand energy",
    note := "The equality is stated in ENNReal to match the repository's nonnegative process-energy interface; general L2 completion remains downstream."
  },
  {
    key := "ito-elementary.chewi-display-1-1-7",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIntegral.chewi_display_1_1_7",
    upstreamDecl := "Chewi display (1.1.7)",
    upstreamFile := "Log-Concave Sampling, book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "L2", "product-measure", "Tonelli"],
    saldUse := "canonical product-space energy for square-integrable stochastic integrands",
    note := "Uses ENNReal and Tonelli under explicit joint a.e. measurability; finiteness remains a visible inequality rather than a totalized integral."
  },
  {
    key := "ito-local.chewi-display-1-1-10",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIntegral.chewi_display_1_1_10",
    upstreamDecl := "Chewi display (1.1.10)",
    upstreamFile := "Log-Concave Sampling, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Ito", "localization", "L2", "almost-sure"],
    saldUse := "local square-integrability premise for canonical stopping and localized stochastic integration",
    note := "Exact ENNReal almost-sure finiteness condition; construction of the canonical localizing sequence and localized Ito integral remain downstream."
  },
  {
    key := "markov-semigroup.chewi-definition-1-2-1",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.MarkovSemigroup.markovOperator",
    upstreamDecl := "Chewi Definition 1.2.1",
    upstreamFile := "Log-Concave Sampling, book page 10 / PDF page 22",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Markov-semigroup", "transition-kernel", "conditional-expectation", "definition"],
    saldUse := "Chewi Definition 1.2.1 root: define P_t f(x) by integration against the conditional transition kernel",
    note := "Exact kernel conditional-law operator; constructing kernels from a concrete SDE remains separate."
  },
  {
    key := "martingale.chewi-definition-1-1-4",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Martingale.IsChewiMartingale",
    upstreamDecl := "MeasureTheory.Martingale / Chewi Definition 1.1.4",
    upstreamFile := "Mathlib.Probability.Martingale.Basic; Log-Concave Sampling, book page 5 / PDF page 17",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "martingale", "filtration", "conditional-expectation", "adapted"],
    saldUse := "Chewi Definition 1.1.4 root: connect the source adapted conditional-expectation law to Mathlib Martingale",
    note := "Exact real continuous-time predicate; continuity of sample paths and local martingale localization are separate properties."
  },
  {
    key := "stopping-time.chewi-definition-1-1-11",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.StoppingTime.IsChewiStoppingTime",
    upstreamDecl := "MeasureTheory.IsStoppingTime / Chewi Definition 1.1.11",
    upstreamFile := "Mathlib.Probability.Process.Stopping; Log-Concave Sampling, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "stopping-time", "filtration", "measurability", "continuous-time"],
    saldUse := "Chewi Definition 1.1.11 root: connect the source event measurability condition to Mathlib's stopping-time API",
    note := "Exact continuous nonnegative-time predicate with possible infinity; localization and stopped Ito integrals remain downstream."
  },
  {
    key := "localization.chewi-definition-1-1-12",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Localization.IsLocalizingSequence",
    upstreamDecl := "MeasureTheory.ProgMeasurable / MeasureTheory.IsStoppingTime / Chewi Definition 1.1.12",
    upstreamFile := "Mathlib.Probability.Process.Adapted; Mathlib.Probability.Process.Stopping; Log-Concave Sampling, book page 6 / PDF page 18",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "localizing-sequence", "stopping-time", "progressive", "L2", "almost-sure"],
    saldUse := "Chewi Definition 1.1.12 root: expose progressive measurability, stopped L2 finiteness, monotone stopping times, and the almost-sure terminal-time limit",
    note := "Exact definition over nonnegative time. Construction of the canonical hitting-time sequence is Proposition 1.1.13 and remains separate."
  },
  {
    key := "localization.chewi-definition-1-1-15",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Localization.IsLocalMartingale",
    upstreamDecl := "MeasureTheory.Adapted / MeasureTheory.stoppedProcess / MeasureTheory.Martingale / Chewi Definition 1.1.15",
    upstreamFile := "Mathlib.Probability.Martingale.Basic; Mathlib.Probability.Process.Stopping; Log-Concave Sampling, book page 7 / PDF page 19",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "local-martingale", "stopping-time", "stopped-process", "adapted"],
    saldUse := "Chewi Definition 1.1.15 root: define local martingales through an increasing a.s.-divergent stopping sequence and centered stopped martingales",
    note := "Exact definition; continuity and the theorem that localized Ito integrals satisfy it remain separate properties."
  },
  {
    key := "reversibility.chewi-definition-1-2-10",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Reversibility.IsReversible",
    upstreamDecl := "Chewi Definition 1.2.10",
    upstreamFile := "Log-Concave Sampling, book page 13 / PDF page 25",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "reversibility", "Hilbert-space", "self-adjoint", "semigroup"],
    saldUse := "Chewi Definition 1.2.10 root: state semigroup reversibility as symmetry on the L2(pi) Hilbert space",
    note := "Exact Hilbert-space predicate; constructing the concrete L2(pi) semigroup and invariant law remains downstream."
  },
  {
    key := "carre-du-champ.chewi-definition-1-2-12",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp.carreDuChamp",
    upstreamDecl := "Chewi Definition 1.2.12",
    upstreamFile := "Log-Concave Sampling, book page 14 / PDF page 26",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "carre-du-champ", "generator", "Dirichlet-form"],
    saldUse := "Chewi Definition 1.2.12 root: expose the bilinear generator expression used by reversibility and functional-inequality arguments",
    note := "Exact algebraic source definition for a real linear generator; positivity and diffusion identities are separate theorems."
  },
  {
    key := "carre-du-champ.chewi-lemma-1-2-13",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp.carreDuChamp_nonneg_of_markov_jensen_rightGenerator",
    upstreamDecl := "Chewi Lemma 1.2.13",
    upstreamFile := "Log-Concave Sampling, book page 14 / PDF page 26",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "carre-du-champ", "Markov-Jensen", "right-generator", "nonnegative"],
    saldUse := "Chewi Lemma 1.2.13: derive pointwise Gamma nonnegativity from the Markov Jensen inequality and the actual right-generator limits",
    note := "The proof takes the nonnegative Jensen-gap quotient to its right limit; it requires separate generator limits for f and f squared and right continuity of the orbit."
  },
  {
    key := "carre-du-champ.chewi-theorem-1-2-14",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp.fundamental_integration_by_parts",
    upstreamDecl := "Chewi Theorem 1.2.14",
    upstreamFile := "Log-Concave Sampling, book page 14 / PDF page 26",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "carre-du-champ", "integration-by-parts", "stationarity", "reversibility"],
    saldUse := "Chewi Theorem 1.2.14: derive symmetry of the Dirichlet form and its integrated-Gamma representation from stationary and symmetric generator identities",
    note := "All three expanded Gamma terms carry explicit integrability hypotheses; the concrete semigroup supplies stationarity and symmetry separately."
  },
  {
    key := "carre-du-champ.chewi-corollary-1-2-15",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp.negativeGenerator_quadratic_nonneg",
    upstreamDecl := "Chewi Corollary 1.2.15",
    upstreamFile := "Log-Concave Sampling, book page 14 / PDF page 26",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "generator", "nonnegative", "Dirichlet-form", "carre-du-champ"],
    saldUse := "Chewi Corollary 1.2.15: turn pointwise Gamma nonnegativity and stationary integration by parts into nonnegativity of the negative-generator quadratic form",
    note := "Consumes the exact Theorem 1.2.14 leaf; proving Gamma nonnegative from Markov Jensen is Lemma 1.2.13 and remains separate."
  },
  {
    key := "carre-du-champ.chewi-definition-1-2-28",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp.iteratedCarreDuChamp",
    upstreamDecl := "Chewi Definition 1.2.28",
    upstreamFile := "Log-Concave Sampling, book page 18 / PDF page 30",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "carre-du-champ", "Gamma2", "generator"],
    saldUse := "Chewi Definition 1.2.28 root: define the iterated carre du champ consumed by the Bakry-Emery criterion",
    note := "Exact algebraic source definition; concrete Langevin Hessian identification remains downstream."
  },
  {
    key := "carre-du-champ.chewi-definition-1-2-29",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp.SatisfiesBakryEmery",
    upstreamDecl := "Chewi Definition 1.2.29",
    upstreamFile := "Log-Concave Sampling, book page 19 / PDF page 31",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Bakry-Emery", "curvature-dimension", "Gamma2"],
    saldUse := "Chewi Definition 1.2.29 root: state CD(alpha,infinity) with the source positivity requirement on alpha",
    note := "Exact predicate only; the Bakry-Emery implication and concrete Langevin curvature calculation are separate theorem routes."
  },
  {
    key := "markov-semigroup.chewi-lemma-1-2-2",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.MarkovSemigroup.chewi_lemma_1_2_2",
    upstreamDecl := "Kernel.lintegral_id' / Kernel.lintegral_comp",
    upstreamFile := "Mathlib.Probability.Kernel.Basic; Mathlib.Probability.Kernel.Composition.Comp; Chewi Lemma 1.2.2",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Markov-semigroup", "transition-kernel", "Chapman-Kolmogorov"],
    saldUse := "Chewi Chapter 1.2 root: derive the observable semigroup laws from identity and Chapman-Kolmogorov transition kernels",
    note := "Compiled kernel-to-operator theorem. It does not construct a concrete diffusion kernel or prove time continuity."
  },
  {
    key := "markov-semigroup.constant-preservation",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.MarkovSemigroup.markovOperator_const",
    upstreamDecl := "lintegral_const with probability-kernel mass one",
    upstreamFile := "Mathlib.Probability.Kernel.Basic; Mathlib.MeasureTheory.Integral.Lebesgue.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Markov-operator", "constant-preservation", "probability-kernel"],
    saldUse := "Record the conservative Markov-operator law P_t 1 = 1",
    note := "The ENNReal observable type encodes nonnegativity; the Markov instance supplies total mass one."
  },
  {
    key := "markov-semigroup.monotonicity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.MarkovSemigroup.markovOperator_apply_mono",
    upstreamDecl := "lintegral_mono",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Lebesgue.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Markov-operator", "monotonicity", "lintegral"],
    saldUse := "Order-preserving interface for semigroup comparison and contraction arguments",
    note := "Pointwise monotonicity on measurable ENNReal-valued observables."
  },
  {
    key := "feller-semigroup.kernel-operator-contraction",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FellerSemigroup.norm_fellerOperator_apply_le",
    upstreamDecl := "norm_integral_le_of_norm_le_const",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Basic; Mathlib.Topology.ContinuousMap.Bounded.Normed",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Feller", "Markov-operator", "contraction", "sup-norm"],
    saldUse := "Place transition-kernel operators on the bounded-continuous sup-norm space",
    note := "The norm bound is derived from probability-kernel integration, not postulated as an operator contract."
  },
  {
    key := "feller-semigroup.chewi-display-1-2-11",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FellerSemigroup.sq_fellerOperator_apply_le",
    upstreamDecl := "ConvexOn.map_integral_le / Even.convexOn_pow",
    upstreamFile := "Mathlib.Analysis.Convex.Integral; Mathlib.Analysis.Convex.Mul; Chewi display (1.2.11)",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Feller", "Markov-operator", "Jensen", "carre-du-champ"],
    saldUse := "Supply the finite-time Jensen gap used to prove non-negativity of the carre du champ",
    note := "The square inequality is proved by Jensen integration under the probability transition kernel; it is not stored as a semigroup-contract assumption."
  },
  {
    key := "feller-semigroup.operator-semigroup-law",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FellerSemigroup.fellerOperator_add",
    upstreamDecl := "Kernel.integral_comp",
    upstreamFile := "Mathlib.Probability.Kernel.Composition.IntegralCompProd",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Feller", "continuous-linear-map", "Chapman-Kolmogorov", "semigroup"],
    saldUse := "Convert Chapman-Kolmogorov into composition of bounded continuous linear operators",
    note := "This is the concrete kernel-to-operator bridge needed before the norm-topology generator layer."
  },
  {
    key := "feller-semigroup.continuous-linear-semigroup",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FellerSemigroup.continuousLinearSemigroupOfFeller",
    upstreamDecl := "fellerOperator_zero / fellerOperator_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FellerSemigroup",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Feller", "continuous-linear-semigroup", "generator-boundary"],
    saldUse := "Supply the exact ContinuousLinearSemigroup consumed by the right-generator definitions",
    note := "Strong continuity in time and concrete diffusion construction remain explicit downstream obligations."
  },
  {
    key := "operator-generator.chewi-definition-1-2-3",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGenerator.HasRightGeneratorAt",
    upstreamDecl := "Chewi Definition 1.2.3",
    upstreamFile := "Log-Concave Sampling, book page 11 / PDF page 23",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "generator", "right-derivative", "Tendsto", "domain"],
    saldUse := "Chewi Definition 1.2.3 root: state the infinitesimal generator as an actual right difference-quotient limit",
    note := "Exact norm-topology relation on the explicit generator domain; concrete differential-operator identification remains separate."
  },
  {
    key := "operator-generator.domain-invariance",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGenerator.generatorDomain_map",
    upstreamDecl := "ContinuousLinearMap.continuous / Tendsto.comp / semigroup commutation",
    upstreamFile := "Mathlib.Analysis.Normed.Operator.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "generator", "domain", "semigroup", "Tendsto"],
    saldUse := "Chewi Definition 1.2.3 root: preserve the right-generator domain under P_t",
    note := "Abstract norm-topology generator theorem; no closed differential Langevin operator is identified."
  },
  {
    key := "operator-generator.kolmogorov-backward-right",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGenerator.kolmogorov_backward_right",
    upstreamDecl := "rightDifferenceQuotient_map / Tendsto.comp",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGenerator; Mathlib.Analysis.Normed.Operator.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Kolmogorov-backward", "right-derivative", "generator", "semigroup"],
    saldUse := "Chewi Proposition 1.2.5 root: prove the right orbit quotient tends to P_t Lf",
    note := "Actual one-sided Tendsto theorem; the forward equation and concrete Langevin generator remain downstream."
  },
  {
    key := "operator-generator.strong-continuity-right-orbit",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain.StronglyContinuousSemigroup.tendsto_op_add",
    upstreamDecl := "ContinuousLinearSemigroup.op_add_apply / ContinuousLinearMap.continuous",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain; Mathlib.Analysis.Normed.Operator.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "strong-continuity", "semigroup", "right-orbit", "Tendsto"],
    saldUse := "Chewi Definition 1.2.1 topology leaf: propagate strong continuity at zero to every right-shifted orbit",
    note := "Abstract orbit-continuity theorem. It does not prove that a concrete Langevin or general Feller semigroup is strongly continuous on a selected observable space."
  },
  {
    key := "operator-generator.right-limit-unique",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain.hasRightGeneratorAt_unique",
    upstreamDecl := "tendsto_nhds_unique",
    upstreamFile := "Mathlib.Topology.Sequences; Mathlib.Topology.Order.DenselyOrdered",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "generator", "right-derivative", "uniqueness", "Tendsto"],
    saldUse := "Chewi Definition 1.2.3 root: make the norm-topology right-generator relation single-valued",
    note := "Uniqueness uses the nontrivial positive-time filter at zero; generator existence remains encoded by domain membership."
  },
  {
    key := "operator-generator.domain-submodule",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain.generatorDomainSubmodule",
    upstreamDecl := "hasRightGeneratorAt_zero / hasRightGeneratorAt_add / hasRightGeneratorAt_smul",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "generator", "domain", "submodule", "linearity"],
    saldUse := "Package the right-generator domain as a real submodule before constructing the infinitesimal operator",
    note := "This is an algebraic domain theorem for an abstract continuous-linear semigroup, not a closedness or smooth-core theorem."
  },
  {
    key := "operator-generator.linear-map",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain.rightGenerator",
    upstreamDecl := "hasRightGeneratorAt_unique / generatorDomainSubmodule",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "generator", "linear-map", "domain", "right-derivative"],
    saldUse := "Chewi Definition 1.2.3 root: bundle the unique infinitesimal generator value as a linear map on its domain",
    note := "The codomain is the ambient normed space. Continuity, closedness, and equality with the Langevin differential expression are not asserted."
  },
  {
    key := "operator-generator.bundled-domain-commutation",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain.rightGenerator_map",
    upstreamDecl := "generatorDomain_map / hasRightGeneratorAt_unique",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGenerator",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "generator", "semigroup", "commutation", "invariant-domain"],
    saldUse := "Chewi Proposition 1.2.5 root: state L(P_t f)=P_t(Lf) using the canonical bundled generator",
    note := "The theorem applies on the abstract right-generator domain preserved by the semigroup."
  },
  {
    key := "operator-generator.kolmogorov-backward-bundled",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain.kolmogorov_backward_right_generator",
    upstreamDecl := "kolmogorov_backward_right / rightGeneratorValue_spec",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGeneratorDomain; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.OperatorGenerator",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Kolmogorov-backward", "generator", "right-derivative", "bundled-domain"],
    saldUse := "Chewi Proposition 1.2.5 root: expose the right backward equation without an existential generator witness",
    note := "Actual one-sided norm-limit theorem on the bundled domain; it does not identify a concrete Langevin generator or prove a forward equation."
  },
  {
    key := "weak-generator.sample-to-law-derivative",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator.weakGeneratorFromSampleDerivative",
    upstreamDecl := "law-map integral rewrite plus supplied Ito-generator derivative",
    upstreamFile := "Mathlib Measure.map / ASTIS lawIntegralHasDerivAtOfMeasureMapEqAndSample",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["weak-generator", "weak-FP", "law-map", "HasDerivAt", "SDE"],
    saldUse := "rewrite frozen EM/Ito sample-space weak-test derivative into a named law-level weak-generator identity",
    note := "Pro-assimilated leaf: does not prove Ito, density PDE, or conditional drift construction."
  },
  {
    key := "fokker-planck.scalar-divergence-rewrite",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra.fpRewriteScalarAlgebra",
    upstreamDecl := "elementary scalar algebra after supplied FP/divergence identities",
    upstreamFile := "local Mathlib ring proof",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["weak-FP", "Fokker-Planck", "scalar-algebra", "divergence"],
    saldUse := "post-process supplied weak FP and score-split identities before Fisher/IBP handoff",
    note := "Small Mathlib-ready algebra leaf; analytic PDE hypotheses remain explicit contracts."
  },
  {
    key := "fisher.ibp.scalar-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra.fisherIbpAlgebra",
    upstreamDecl := "elementary scalar algebra after supplied IBP identities",
    upstreamFile := "local Mathlib ring proof",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Fisher-information", "IBP", "scalar-algebra"],
    saldUse := "combine two no-boundary IBP identities into the Fisher/cross-term display",
    note := "Small Mathlib-ready algebra leaf; no-boundary/divergence theorem remains a separate analytic contract."
  },
  {
    key := "langevin.gibbs-weighted-generator-hasDerivAt-1d",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.hasDerivAt_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d",
    upstreamDecl := "ordinary product rule plus derivative of exp(-V)",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.ExpDeriv; Mathlib.Analysis.Calculus.Deriv.Mul",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "generator", "one-dimensional", "pointwise-calculus"],
    saldUse := "Chewi SDE/DENS root: pointwise bridge from the 1D overdamped generator `f'' - V' * f'` to the derivative of the Gibbs-weighted test derivative",
    note := "This is only a pointwise ordinary-derivative calculation. Stationarity, reversibility, IBP, boundary terms, generator domains, and invariant-law proofs remain separate red obligations."
  },
  {
    key := "langevin.gibbs-weighted-generator-deriv-1d",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.deriv_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d",
    upstreamDecl := "hasDerivAt_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "generator", "one-dimensional", "deriv"],
    saldUse := "Chewi SDE/DENS root: rewrite `(exp(-V) f')'` as the Gibbs weight times the 1D overdamped generator expression",
    note := "Derivative-form wrapper only; it does not assert integration by parts, zero boundary term, stationarity, reversibility, or a normalized Gibbs law."
  },
  {
    key := "langevin.gibbs-weighted-divergence-generator-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.weightedDivergence_gibbsWeight_langevinGenerator_algebra",
    upstreamDecl := "inner-product algebra after supplied product rule and Gibbs-weight gradient identity",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; Mathlib.Analysis.InnerProductSpace.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "generator", "divergence-form", "inner-product", "algebra"],
    saldUse := "Chewi SDE/DENS root: assemble `div (rho ∇f) = rho * (lapF - <∇V, ∇f>)` once product-rule and chain-rule facts are supplied",
    note := "Supplied-hypothesis algebra only. It does not define or prove gradient, divergence, Laplacian, product rule, chain rule, IBP, boundary decay, stationarity, reversibility, or invariant Gibbs law."
  },
  {
    key := "langevin.exp-neg-weighted-divergence-generator-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.expNeg_weightedDivergence_langevinGenerator_algebra",
    upstreamDecl := "weightedDivergence_gibbsWeight_langevinGenerator_algebra with `rho = exp (-Vx)`",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs-weight", "exp-neg-potential", "divergence-form", "algebra"],
    saldUse := "Chewi SDE/DENS root: source-facing `exp(-V)` weighted-divergence algebra before the invariant Gibbs and reversibility proof branches",
    note := "Thin source-facing wrapper only; all analytic facts about `∇ exp(-V)`, divergence theorem, no-boundary terms, domains, and invariant laws remain red obligations."
  },
  {
    key := "langevin.finite-coordinate-weighted-divergence-generator-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteCoord_weightedDivergence_langevinGenerator_algebra",
    upstreamDecl := "finite-coordinate summation algebra after supplied coordinate product and chain rules",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; Mathlib.Algebra.BigOperators.Fin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-coordinate", "Gibbs-weight", "divergence-form", "Laplacian", "algebra"],
    saldUse := "Chewi SDE/DENS root: aggregate coordinate identities `∂ᵢ(rho ∂ᵢf)` into the finite-sum Langevin divergence-form expression",
    note := "Supplied-hypothesis finite-sum algebra only. It does not define/prove partial derivatives, gradients, divergence, Laplacian, product rule, chain rule, IBP, boundary decay, stationarity, reversibility, or invariant Gibbs law."
  },
  {
    key := "langevin.finite-coordinate-named-weighted-divergence-generator-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteCoord_named_weightedDivergence_langevinGenerator_algebra",
    upstreamDecl := "finiteCoord_weightedDivergence_langevinGenerator_algebra plus supplied names for divergence, Laplacian, and gradient inner-product sums",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-coordinate", "Laplacian", "gradient-inner-product", "divergence-form", "algebra"],
    saldUse := "Chewi SDE/DENS root: source-facing finite-coordinate handoff to named `divWeighted = rho * (lapF - innerGradVGradF)`",
    note := "Names the coordinate sums only after they are supplied as hypotheses; true Euclidean `grad/div/laplace` API wrappers and analytic regularity remain red obligations."
  },
  {
    key := "langevin.finite-coordinate-toLp-inner-weighted-divergence-generator-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteCoord_toLpInner_weightedDivergence_langevinGenerator_algebra",
    upstreamDecl := "finite-coordinate Langevin algebra plus EuclideanSpace `WithLp.toLp 2` inner-product coordinate bridge",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-coordinate", "EuclideanSpace", "WithLp.toLp", "gradient-inner-product", "algebra"],
    saldUse := "Chewi SDE/DENS root: rewrite finite-coordinate Langevin divergence algebra with Mathlib `EuclideanSpace` inner-product notation after coordinate representatives are supplied",
    note := "Coordinate-to-inner-product notation bridge only; it does not define/prove gradients, divergence, Laplacian, IBP, stationarity, reversibility, or invariant Gibbs law."
  },
  {
    key := "langevin.finite-coordinate-euclidean-inner-weighted-divergence-generator-algebra",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteCoord_euclideanInner_weightedDivergence_langevinGenerator_algebra",
    upstreamDecl := "finite-coordinate Langevin algebra plus direct `EuclideanSpace` inner-product coordinate bridge",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-coordinate", "EuclideanSpace", "gradient-inner-product", "algebra"],
    saldUse := "Chewi SDE/DENS root: source-facing finite-dimensional handoff to `divWeighted = rho * (lapF - inner ℝ gradV gradF)`",
    note := "Direct Euclidean inner-product wrapper after supplied coordinate product-rule, chain-rule, and Laplacian identities; analytic generator and invariant-law theorems remain red."
  },
  {
    key := "langevin.finite-euclidean-generator-basis-display",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_langevinGenerator_basisDisplay",
    upstreamDecl := "InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis plus EuclideanSpace inner-product coordinate bridge",
    upstreamFile := "Mathlib.Analysis.InnerProductSpace.Laplacian; AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-dimensional", "EuclideanSpace", "generator-display", "Laplacian", "gradient-inner-product", "basisFun"],
    saldUse := "Chewi SDE/ANALYSIS root: pointwise finite-dimensional display of the formal differential expression `Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x)` using Mathlib's `EuclideanSpace.basisFun` coordinate basis",
    note := "Pointwise display leaf only using Mathlib's total `gradient` and `Laplacian.laplacian` definitions. It does not prove divergence, product rules for `rho ∇f`, IBP, boundary decay, generator domains, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "langevin.finite-euclidean-generator-coordinate-display",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_langevinGenerator_coordinateDisplay",
    upstreamDecl := "finiteEuclidean_langevinGenerator_basisDisplay plus EuclideanSpace.basisFun_apply",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; Mathlib.Analysis.InnerProductSpace.PiL2",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-dimensional", "EuclideanSpace", "generator-display", "Laplacian", "gradient-inner-product", "coordinate-unit"],
    saldUse := "Chewi SDE/ANALYSIS root: pointwise coordinate-unit display of the formal Langevin differential expression `Δ f - <∇V, ∇f>` as diagonal second derivatives minus the gradient-coordinate inner-product sum",
    note := "Explicit coordinate-unit display only. It requires `[DecidableEq ι]` to unfold `EuclideanSpace.basisFun` to `EuclideanSpace.single i 1`; it does not assert divergence, IBP, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "langevin.finite-euclidean-weighted-divergence-basis-handoff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff",
    upstreamDecl := "finiteCoord_weightedDivergence_langevinGenerator_algebra plus finiteEuclidean_langevinGenerator_basisDisplay",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-dimensional", "EuclideanSpace", "weighted-divergence", "supplied-hypothesis", "basisFun", "handoff"],
    saldUse := "Chewi SDE/DENS root: after coordinate product-rule and Gibbs-weight chain-rule facts are supplied, rewrite the finite weighted-divergence sum as `rho * (Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x))` using the basis display",
    note := "Supplied-hypothesis handoff only. It does not prove coordinate product rules, the a.e. bridge or box-integrability assumptions needed by the compiled box divergence wrapper, IBP, boundary decay, semigroup generator theorem, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "langevin.finite-euclidean-weighted-divergence-coordinate-handoff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_weightedDivergence_langevinGenerator_coordinateHandoff",
    upstreamDecl := "finiteCoord_weightedDivergence_langevinGenerator_algebra plus finiteEuclidean_langevinGenerator_coordinateDisplay",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-dimensional", "EuclideanSpace", "weighted-divergence", "supplied-hypothesis", "coordinate-unit", "handoff"],
    saldUse := "Chewi SDE/DENS root: explicit coordinate-unit handoff from supplied coordinate divergence/product-rule and Gibbs-weight chain-rule facts to the Mathlib expression `rho * (Δ f - <∇V, ∇f>)`",
    note := "Coordinate-unit supplied-hypothesis handoff only. It does not prove divergence theorem, product rule, IBP, no-boundary term, semigroup/Ito generator result, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "langevin.finite-euclidean-exp-neg-weighted-divergence-basis-handoff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_basisHandoff",
    upstreamDecl := "finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff plus gradient_expNegPotential_coordinate_eq_of_differentiableAt",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-dimensional", "EuclideanSpace", "Gibbs-weight", "weighted-divergence", "DifferentiableAt", "basisFun", "handoff"],
    saldUse := "Chewi SDE/DENS root: basis-coordinate handoff from supplied divergence sum and coordinate product-rule facts to `exp(-V x) * (Laplacian.laplacian f x - inner ℝ (gradient V x) (gradient f x))`, with the Gibbs-weight chain-rule coordinate equality discharged from `DifferentiableAt ℝ V x`",
    note := "Discharges only the Gibbs-weight chain-rule hypothesis used by the earlier supplied-hypothesis handoff. Coordinate product rules, the a.e. bridge and box-integrability assumptions needed by the compiled box divergence wrapper, IBP, boundary decay, semigroup/Ito generator theorem, stationarity, reversibility, invariant Gibbs law, and KL/FI remain red."
  },
  {
    key := "langevin.finite-euclidean-exp-neg-weighted-divergence-coordinate-handoff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_coordinateHandoff",
    upstreamDecl := "finiteEuclidean_weightedDivergence_langevinGenerator_coordinateHandoff plus gradient_expNegPotential_coordinate_eq_of_differentiableAt",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-dimensional", "EuclideanSpace", "Gibbs-weight", "weighted-divergence", "DifferentiableAt", "coordinate-unit", "handoff"],
    saldUse := "Chewi SDE/DENS root: coordinate-unit handoff from supplied divergence sum and coordinate product-rule facts to `exp(-V x) * (Δ f - <∇V, ∇f>)`, with the Gibbs-weight chain-rule coordinate equality discharged from `DifferentiableAt ℝ V x`",
    note := "Discharges only the Gibbs-weight chain-rule hypothesis for the coordinate-unit display. It does not prove divergence theorem, coordinate product rule, IBP/no-boundary term, semigroup/Ito generator result, stationarity, reversibility, invariant Gibbs law, or KL/FI dissipation."
  },
  {
    key := "langevin.finite-euclidean-exp-neg-lineDeriv-fderiv-coordinate-sum-display",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display",
    upstreamDecl := "lineDeriv_expNegPotential_mul_fderiv_coordinate_eq plus finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_coordinateHandoff",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-dimensional", "EuclideanSpace", "Gibbs-weight", "lineDeriv", "fderiv", "coordinate-sum", "generator-display", "coordinate-unit"],
    saldUse := "Chewi Ch.1 Langevin root: aggregate the compiled coordinate line-derivative calculation for `exp(-V) * fderiv f eᵢ` into the finite Euclidean `exp(-V x) * (Δ f - <∇V, ∇f>)` display",
    note := "Pointwise finite-coordinate sum display only. It discharges the coordinate product-rule/diagonal second-derivative branch for the explicit field `exp(-V) * fderiv f eᵢ`, but keeps the gradient-coordinate bridge `fderiv ℝ f x eᵢ = (gradient f x) i` as a hypothesis. It does not define a divergence operator, assert that the sum is a divergence, prove IBP/no-boundary terms, semigroup/Ito generator domains, stationarity, reversibility, invariant Gibbs law, or KL/FI."
  },
  {
    key := "langevin.finite-euclidean-exp-neg-lineDeriv-fderiv-coordinate-sum-display-differentiable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display_of_differentiableAt",
    upstreamDecl := "finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display plus fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "finite-dimensional", "EuclideanSpace", "Gibbs-weight", "lineDeriv", "fderiv", "coordinate-sum", "generator-display", "DifferentiableAt"],
    saldUse := "Chewi Ch.1 Langevin root: coordinate-sum display for `exp(-V) * fderiv f eᵢ` with the local `fderiv`-coordinate-to-`gradient`-coordinate bridge discharged from `DifferentiableAt ℝ f x`",
    note := "Pointwise finite-coordinate sum display only. It removes the earlier supplied `hgradF` hypothesis by adding the explicit assumption `DifferentiableAt ℝ f x`. It does not assert that differentiability of `fun y => fderiv ℝ f y` implies differentiability of `f`; it does not define divergence, prove that the sum is divergence, prove IBP/no-boundary terms, semigroup/Ito generator domains, stationarity, reversibility, invariant Gibbs law, or KL/FI."
  },
  {
    key := "langevin.coordinate-divergence-exp-neg-fderiv-display",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.coordinateDivergence_expNeg_fderivCoordinateField_langevinGenerator_display_of_differentiableAt",
    upstreamDecl := "coordinateDivergence_eq_sum_lineDeriv plus finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display_of_differentiableAt",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "coordinate-divergence", "finite-dimensional", "EuclideanSpace", "Gibbs-weight", "fderiv", "generator-display", "DifferentiableAt"],
    saldUse := "Chewi Ch.1 Langevin root: rewrite the explicit Gibbs-weighted first-derivative coordinate field through ASTIS `coordinateDivergence` and recover `exp(-V x) * (Delta f - <grad V, grad f>)` pointwise",
    note := "Named coordinate-divergence display only. It packages the compiled pointwise coordinate sum; it does not prove Mathlib's divergence theorem, weighted IBP, boundary decay, semigroup/Ito generator domains, invariant Gibbs law, reversibility, or KL/FI."
  },
  {
    key := "langevin.trace-exp-neg-fderiv-coordinate-field-display",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt",
    upstreamDecl := "coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt plus coordinateDivergence_expNeg_fderivCoordinateField_langevinGenerator_display_of_differentiableAt",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "trace-style", "Pi-space", "Gibbs-weight", "fderiv", "generator-display", "HasFDerivAt"],
    saldUse := "Chewi Ch.1 Langevin root: pointwise handoff from Mathlib's Pi-space finite-box trace summand for the explicit field `exp(-V) * fderiv f eᵢ` to the scalar display `exp(-V) * (Delta f - <grad V, grad f>)`",
    note := "Pointwise trace-display handoff only. It assumes the explicit Pi-space field has the supplied Frechet derivative and the needed pointwise differentiability hypotheses. It does not prove differentiability on a box, continuity, integrability, a divergence theorem, boundary cancellation, weighted IBP, generator domains, invariant Gibbs law, reversibility, stationarity, or KL/FI."
  },
  {
    key := "langevin.integrableOn-trace-exp-neg-fderiv-coordinate-field-continuous",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn",
    upstreamDecl := "ContinuousOn.integrableOn_compact on Set.Icc plus trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt and IntegrableOn.congr_fun",
    upstreamFile := "Mathlib.MeasureTheory.Function.LocallyIntegrable; Mathlib.MeasureTheory.Integral.IntegrableOn; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "IntegrableOn", "trace-style", "closed-box", "ContinuousOn", "Gibbs-weight", "generator-display"],
    saldUse := "Chewi Ch.1 Langevin root: finite closed-box handoff proving Mathlib trace-summand `IntegrableOn` for the explicit Gibbs-weighted fderiv-coordinate field when the scalar Langevin display is already continuous on the box",
    note := "Finite closed-box regularity handoff only. It assumes the trace/display equality hypotheses and continuity of the displayed scalar RHS; it does not prove RHS continuity, field differentiability, whole-space integrability, boundary cancellation, weighted IBP, generator domains, invariant Gibbs law, reversibility, stationarity, or KL/FI."
  },
  {
    key := "langevin.continuousOn-exp-neg-generator-rhs-components",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.continuousOn_expNeg_langevinGenerator_rhs_of_components",
    upstreamDecl := "ContinuousOn.rexp / ContinuousOn.mul / ContinuousOn.sub / ContinuousOn.inner",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.Exp; Mathlib.Analysis.InnerProductSpace.Continuous; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "ContinuousOn", "closed-box", "Gibbs-weight", "generator-display", "components"],
    saldUse := "Chewi Ch.1 Langevin root: assemble component continuity of `V`, `Delta f`, `grad V`, and `grad f` into continuity of the scalar display `exp(-V) * (Delta f - <grad V, grad f>)` on a finite Pi-box",
    note := "Component-continuity assembly only. It does not derive those component continuity hypotheses from a ContDiff/test-function class, does not prove field differentiability, integrability, IBP, boundary cancellation, domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "langevin.integrableOn-trace-exp-neg-fderiv-coordinate-field-components",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integrableOn_trace_expNeg_fderivCoordinateField_of_component_continuousOn",
    upstreamDecl := "continuousOn_expNeg_langevinGenerator_rhs_of_components plus integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "IntegrableOn", "trace-style", "closed-box", "ContinuousOn", "components", "Gibbs-weight"],
    saldUse := "Chewi Ch.1 Langevin root: finite closed-box trace `IntegrableOn` handoff for the explicit Gibbs-weighted fderiv-coordinate field under component continuity plus the existing trace/display differentiability hypotheses",
    note := "Finite closed-box handoff under component continuity only. It still assumes the explicit Pi-space field derivative and pointwise differentiability hypotheses; it does not derive them from a test-function class and does not prove whole-space integrability, IBP, boundary cancellation, domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "langevin.continuousOn-exp-neg-generator-rhs-contDiff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.continuousOn_expNeg_langevinGenerator_rhs_of_contDiff",
    upstreamDecl := "continuousOn_expNeg_langevinGenerator_rhs_of_components plus continuous_gradient_of_contDiff_one and continuous_laplacian_of_contDiff_two",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "ContinuousOn", "ContDiff", "closed-box", "Gibbs-weight", "generator-display", "components"],
    saldUse := "Chewi Ch.1 Langevin root: derive closed-box continuity of `exp(-V) * (Delta f - <grad V, grad f>)` from global `C¹/C²` hypotheses",
    note := "Component continuity is now discharged from global `ContDiff` regularity. The explicit Pi-space field derivative, trace integrability without that derivative, whole-space integrability, weighted IBP, boundary cancellation, domains, invariant law, reversibility, and KL/FI remain separate obligations."
  },
  {
    key := "langevin.integrableOn-trace-exp-neg-fderiv-coordinate-field-contDiff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff",
    upstreamDecl := "integrableOn_trace_expNeg_fderivCoordinateField_of_component_continuousOn plus global `ContDiff` component regularity",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "IntegrableOn", "ContDiff", "trace-style", "closed-box", "Gibbs-weight"],
    saldUse := "Chewi Ch.1 Langevin root: close finite-box trace `IntegrableOn` from global `C¹/C²` regularity once the explicit Pi-space field derivative is supplied",
    note := "Finite-box trace handoff under `ContDiff ℝ 1 V`, `ContDiff ℝ 2 f`, and supplied field derivative only. It does not prove that field derivative, whole-space integrability, weighted IBP, boundary cancellation, domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "langevin.hasFDerivAt-exp-neg-fderiv-coordinate-field-contDiff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.hasFDerivAt_expNeg_fderivCoordinateField_of_contDiff",
    upstreamDecl := "DifferentiableAt.hasFDerivAt, differentiableAt_pi, PiLp.hasFDerivAt_toLp, product/chain differentiability",
    upstreamFile := "Mathlib.Analysis.Calculus.FDeriv.Prod; Mathlib.Analysis.Calculus.FDeriv.WithLp; Mathlib.Analysis.SpecialFunctions.ExpDeriv; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "HasFDerivAt", "ContDiff", "Pi-space", "Gibbs-weight", "fderiv", "regularity"],
    saldUse := "Chewi Ch.1 Langevin root: discharge the explicit Pi-space field differentiability input for `z ↦ exp(-V(toLp z)) * fderiv f (toLp z) eᵢ` from global `C¹/C²` regularity",
    note := "The derivative representative is Mathlib's `fderiv` of the field, not a closed-form Jacobian. It does not prove a divergence theorem, whole-space integrability, weighted IBP, boundary cancellation, domains, invariant law, reversibility, or KL/FI."
  },
  {
    key := "langevin.integrableOn-trace-exp-neg-fderiv-coordinate-field-contDiff-fderiv",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff_fderiv",
    upstreamDecl := "integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff plus hasFDerivAt_expNeg_fderivCoordinateField_of_contDiff",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "IntegrableOn", "ContDiff", "HasFDerivAt", "fderiv", "trace-style", "closed-box"],
    saldUse := "Chewi Ch.1 Langevin root: finite-box trace `IntegrableOn` for the canonical `fderiv` trace of the explicit Gibbs-weighted first-derivative field under global `C¹/C²` regularity",
    note := "This removes the supplied field-derivative hypothesis only for the canonical `fderiv` representative. It remains finite-box regularity, not boundary cancellation, weighted IBP, generator-domain semantics, invariant law, reversibility, or KL/FI."
  },
  {
    key := "langevin.integrable-exp-neg-fderiv-coordinate-source-field",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integrable_expNeg_fderivCoordinateField_of_lintegral_expNeg_ne_top_of_fderiv_norm_le",
    upstreamDecl := "lintegral_ofReal_ne_top_iff_integrable, PiLp.volume_preserving_toLp, Integrable.smul_bdd, ContinuousLinearMap.le_opNorm",
    upstreamFile := "Mathlib.MeasureTheory.Function.L1Space.Integrable; Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Integrable", "whole-space", "Gibbs-weight", "fderiv", "coordinate-field", "bounded-derivative"],
    saldUse := "Chewi Ch.1 Example 1.2.8 cutoff route: discharge the concrete `Integrable G volume` premise for `G = exp(-V) * fderiv f` in raw Pi coordinates from finite Gibbs mass and a bounded first derivative",
    note := "Whole-space source-field integrability only. It uses genuine `C¹` regularity for `fderiv`, transports the scalar Gibbs weight through the volume-preserving PiLp bridge, and bounds the raw Pi sup norm coordinatewise. It does not prove a Gibbs tail, cutoff main-term convergence, weighted IBP, generator/semigroup domains, stationarity, invariant law, reversibility, or any second-order cutoff estimate."
  },
  {
    key := "langevin.integrable-exp-neg-generator-rhs-compact-test",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport",
    upstreamDecl := "Continuous.integrable_of_hasCompactSupport, notMem_tsupport_iff_eventuallyEq, InnerProductSpace.laplacian_congr_nhds",
    upstreamFile := "Mathlib.MeasureTheory.Function.LocallyIntegrable; Mathlib.Analysis.Calculus.FDeriv.Const; Mathlib.Analysis.InnerProductSpace.Laplacian; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Integrable", "whole-space", "Gibbs-weight", "generator-display", "compact-support", "test-function"],
    saldUse := "Chewi Ch.1 Example 1.2.8 cutoff route: prove whole-space integrability of the exact Euclidean display `exp(-V) * (Delta f - <grad V, grad f>)` for a C_c^2 test function and a C^1 potential",
    note := "Concrete generator-display integrability on EuclideanSpace. Compact support is imposed on the test function; no bounded gradient of the potential and no finite Gibbs-mass premise is needed. The theorem does not prove a cutoff limit, Gibbs tail, weighted IBP, generator/semigroup domains, stationarity, invariance, reversibility, or KL/FI."
  },
  {
    key := "langevin.integrable-exp-neg-generator-rhs-compact-test-raw-pi",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integrable_expNeg_langevinGenerator_rhs_comp_toLp_of_contDiff_of_hasCompactSupport",
    upstreamDecl := "integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport plus PiLp.volume_preserving_toLp",
    upstreamFile := "Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Integrable", "whole-space", "Gibbs-weight", "generator-display", "compact-support", "PiLp"],
    saldUse := "Chewi Ch.1 Example 1.2.8 cutoff route: expose concrete generator-display integrability in the raw finite-Pi coordinate shape consumed by radial-cutoff dominated convergence",
    note := "Volume-preserving coordinate transport of the Euclidean compact-test theorem. It does not itself take the radial-cutoff limit or prove Gibbs tails, weighted IBP, generator/semigroup domains, stationarity, invariance, reversibility, or KL/FI."
  },
  {
    key := "langevin.integrable-exp-neg-weight-raw-pi",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integrable_expNeg_comp_toLp_of_lintegral_expNeg_ne_top",
    upstreamDecl := "lintegral_ofReal_ne_top_iff_integrable plus PiLp.volume_preserving_toLp",
    upstreamFile := "Mathlib.MeasureTheory.Function.L1Space.Integrable; Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs", "Integrable", "whole-space", "PiLp", "weight"],
    saldUse := "Chewi Ch.1 Gibbs-tail route: transport finite unnormalized Gibbs mass to an Integrable raw-Pi scalar weight shared by cutoff and tail consumers",
    note := "Integrability transport only. It does not prove tail convergence, generator-display integrability, weighted IBP, domains, stationarity, invariance, reversibility, or KL/FI."
  },
  {
    key := "langevin.gibbs-weight-tail-tendsto-zero-raw-pi",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.tendsto_setIntegral_expNeg_norm_ge_comp_toLp_of_lintegral_expNeg_ne_top",
    upstreamDecl := "integrable_expNeg_comp_toLp_of_lintegral_expNeg_ne_top plus tendsto_setIntegral_norm_norm_ge_comp_toLp",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs", "tail", "whole-space", "PiLp", "set-integral", "Tendsto"],
    saldUse := "Chewi Ch.1 Example 1.2.8 cutoff route: prove that finite unnormalized Gibbs mass outside expanding Euclidean balls tends to zero in raw-Pi coordinates",
    note := "Concrete Gibbs-tail convergence only. It does not assemble the cutoff divergence identity, prove whole-space weighted IBP, supply generator/semigroup domains, or establish stationarity, invariance, reversibility, or KL/FI."
  },
  {
    key := "langevin.whole-space-gibbs-weighted-generator-ibp-compact-test",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin.integral_expNeg_langevinGenerator_rhs_eq_zero_of_contDiff_of_hasCompactSupport",
    upstreamDecl := "integral_coordinateDivergence_wrapped_eq_zero_of_contDiff_of_hasCompactSupport plus trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt and PiLp.volume_preserving_toLp",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs", "weighted-IBP", "whole-space", "compact-support", "generator", "EuclideanSpace"],
    saldUse := "Chewi Ch.1 Example 1.2.8: justify the omitted whole-space integration-by-parts identity integral exp(-V) * (Delta f - inner (grad V) (grad f)) = 0 for C_c^2 tests",
    note := "Compiled analytic core identity. Compact test support removes the boundary without a finite Gibbs-mass hypothesis. Closed-generator domains, semigroup differentiation, invariant probability law, reversibility, and KL/FI dissipation remain separate."
  },
  {
    key := "analysis.calculus.laplacian-product-rule",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinCarreDuChamp.laplacian_mul",
    upstreamDecl := "fderiv_mul / iteratedFDeriv_two_apply / OrthonormalBasis.sum_inner_mul_inner",
    upstreamFile := "Mathlib.Analysis.Calculus.FDeriv.Mul; Mathlib.Analysis.InnerProductSpace.Laplacian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Laplacian", "product-rule", "gradient", "C2"],
    saldUse := "Chewi Example 1.2.17 root: expand Delta(fg) with the two cross-gradient terms",
    note := "Generic finite-dimensional C2 product rule; no Langevin potential or measure is required."
  },
  {
    key := "analysis.calculus.gradient-product-rule",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinCarreDuChamp.gradient_mul",
    upstreamDecl := "fderiv_mul / InnerProductSpace.gradient",
    upstreamFile := "Mathlib.Analysis.Calculus.FDeriv.Mul; Mathlib.Analysis.Calculus.Gradient.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "gradient", "product-rule", "differentiable"],
    saldUse := "Chewi Example 1.2.17 root: expand the drift action on a product before cancellation",
    note := "Generic differentiable product rule expressed in Mathlib's gradient API."
  },
  {
    key := "langevin.chewi-example-1-2-17",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinCarreDuChamp.langevinCarreDuChamp_eq_inner",
    upstreamDecl := "Chewi Example 1.2.17",
    upstreamFile := "Log-Concave Sampling, book page 15 / PDF page 27",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "carre-du-champ", "gradient", "Dirichlet-form"],
    saldUse := "Chewi Example 1.2.17: identify the formal Langevin carre du champ with the gradient inner product",
    note := "Actual C2 product-rule proof for the displayed differential operator; closed semigroup-generator identification remains separate."
  },
  {
    key := "langevin-generator.compactly-supported-c2-core",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator.CompactlySupportedC2",
    upstreamDecl := "ContDiff and HasCompactSupport",
    upstreamFile := "Mathlib.Analysis.Calculus.ContDiff.Defs; Mathlib.Topology.Algebra.Support; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "generator", "domain", "core", "C2", "compact-support"],
    saldUse := "Chewi Ch.1 generator-domain branch: name the C_c^2 test core on which the whole-space Gibbs-weighted IBP theorem is proved",
    note := "Domain predicate only. It does not claim closability, closed-generator membership beyond the core, semigroup generation, invariance, or reversibility."
  },
  {
    key := "langevin-generator.displayed-operator",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator.operator",
    upstreamDecl := "Laplacian.laplacian and gradient",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.{Gradient,Laplacian}; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "generator", "operator", "Laplacian", "gradient"],
    saldUse := "Chewi Ch.1 generator-domain branch: name the displayed differential action Delta f - inner (grad V) (grad f) independently of any operator-domain claim",
    note := "Formal differential operator only. Genuine generator semantics are supplied by CoreContract rather than inferred from this definition."
  },
  {
    key := "langevin-generator.core-domain-contract",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator.CoreContract",
    upstreamDecl := "CompactlySupportedC2 and LangevinGenerator.operator",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "generator", "domain", "contract", "core", "operator-agreement"],
    saldUse := "Chewi Ch.1 generator-domain branch: require a candidate generator domain to contain C_c^2 and its action to agree there with the displayed Langevin operator",
    note := "Honest core-domain interface. It deliberately does not construct a closed operator or prove that a Markov semigroup satisfies the contract; the semigroup bridge remains separate."
  },
  {
    key := "langevin-generator.normalized-gibbs-annihilates-compact-c2-core",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator.integral_operator_normalizedGibbs_eq_zero_on_compactlySupportedC2",
    upstreamDecl := "integral_expNeg_langevinGenerator_rhs_eq_zero_of_contDiff_of_hasCompactSupport plus GibbsIntegral integral_withDensity rewrite",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.{Langevin,LangevinGenerator}; AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "generator", "Gibbs", "normalized", "core", "infinitesimal-stationarity"],
    saldUse := "Chewi Ch.1 Example 1.2.8 to Corollary 1.2.9: prove normalized Gibbs expectation of the displayed generator is zero on the C_c^2 test core",
    note := "Compiled core-level infinitesimal stationarity. It is not semigroup invariance: Langevin evolution generally does not preserve compact support, so a domain-extension/core theorem or martingale-problem uniqueness remains necessary."
  },
  {
    key := "weak-generator.invariance-on-tests",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator.IsInvariantOn",
    upstreamDecl := "MeasureTheory.integral",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "semigroup", "invariance", "measure", "test-class"],
    saldUse := "Chewi Ch.1 invariant-law branch: state invariance for nonnegative times on an explicit test class before any measure-extensionality upgrade",
    note := "Definition only. It does not assert that a test class determines measures or that a supplied operator family is Markov."
  },
  {
    key := "weak-generator.integrated-semigroup-generator-contract",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator.IntegratedSemigroupGeneratorContract",
    upstreamDecl := "HasDerivWithinAt on Ici and ContinuousOn on finite intervals",
    upstreamFile := "Mathlib.Analysis.Calculus.MeanValue; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "semigroup", "generator", "domain", "right-derivative", "integral-pairing"],
    saldUse := "Chewi Ch.1 operator branch: package identity, semigroup law, domain preservation, pairing continuity, and right-generator derivative without extending time to a group",
    note := "Explicit semigroup/domain contract. It is not constructed for the Langevin SDE here; positivity, mass preservation, strong continuity, and the concrete SDE realization remain separate when needed."
  },
  {
    key := "weak-generator.semigroup-domain-to-invariance",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator.isInvariantOn_of_integral_generator_eq_zero",
    upstreamDecl := "constant_of_has_deriv_right_zero",
    upstreamFile := "Mathlib.Analysis.Calculus.MeanValue; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "semigroup", "generator", "domain", "invariance", "mean-zero"],
    saldUse := "Chewi Ch.1 Corollary 1.2.9 route: turn domain preservation, the integrated generator derivative, and zero generator mean into semigroup invariance on the domain",
    note := "Compiled abstract bridge. A concrete Langevin invariant law still requires constructing the semigroup contract and extending the Gibbs mean-zero identity from C_c^2 to its semigroup-stable domain."
  },
  {
    key := "langevin-generator.conditional-normalized-gibbs-core-invariance",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.LangevinGenerator.isInvariantOn_normalizedGibbs_on_compactlySupportedC2",
    upstreamDecl := "integral_operator_normalizedGibbs_eq_zero_on_compactlySupportedC2 plus isInvariantOn_of_integral_generator_eq_zero",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.{LangevinGenerator,WeakGenerator}",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Langevin", "Gibbs", "semigroup", "generator", "core", "conditional-invariance"],
    saldUse := "Chewi Ch.1 Corollary 1.2.9 route: compose Gibbs core annihilation with an explicit integrated-semigroup contract on C_c^2",
    note := "Compiled conditional core-level bridge. It does not construct the Langevin semigroup and does not extend equality from C_c^2 to a measure-determining or semigroup-stable domain."
  },
  {
    key := "girsanov.finite-gaussian-cylinder-integral",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Girsanov.finiteGaussianGirsanovCylinderIntegral",
    upstreamDecl := "stdGaussian_shift_integral_map_toLp / finite-dimensional Gaussian Esscher",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian; Chewi finite-dimensional Girsanov cylinder route",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Girsanov", "Gaussian", "cylindrical", "path-space", "change-of-measure"],
    saldUse := "Chewi PATH root: package the finite-dimensional Gaussian change-of-measure as a cylindrical Girsanov likelihood ratio before full Brownian path-space RN derivatives",
    note := "Compiled finite-dimensional PATH-facing wrapper; does not assert filtrations, martingales, Novikov, Ito, or continuous-time Brownian path-space Girsanov."
  },
  {
    key := "girsanov.finite-gaussian-cylinder-rn-density",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Girsanov.finiteGaussianGirsanovCylinderMeasure_eq_withDensity",
    upstreamDecl := "measurableEquiv_map_withDensity / pi_gaussianReal_withDensity_exp_shift / map_pi_eq_stdGaussian",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym; AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Girsanov", "Radon-Nikodym", "withDensity", "Gaussian", "cylindrical", "path-space"],
    saldUse := "Chewi PATH root: identify the finite-dimensional cylindrical shifted Gaussian path measure as a withDensity tilt of centered stdGaussian",
    note := "Measure-level RN-style finite-dimensional Girsanov identity; full Brownian path-space RN derivative remains a separate analytic theorem."
  }
]

def klDensityMemory : List LemmaMemoryEntry := [
  {
    key := "kl-density.pointwise-derivative-simplify",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.InformationTheory.KLDensity.klPointwiseDerivSimplify",
    upstreamDecl := "pointwise real-field algebra for d/ds q log(q/p)",
    upstreamFile := "local Mathlib field_simp/ring proof",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["KL", "density", "log", "pointwise-algebra"],
    saldUse := "separate KL density derivative algebra from dominated differentiation and density regularity assumptions",
    note := "Pro-assimilated leaf; positivity/nonzero and domination stay explicit."
  },
  {
    key := "kl-density.remove-mass-term",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.InformationTheory.KLDensity.klDerivativeRemoveMassTerm",
    upstreamDecl := "mass-conservation derivative simplification",
    upstreamFile := "local Mathlib HasDerivAt congruence/simp proof",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["KL", "density", "mass-conservation", "HasDerivAt"],
    saldUse := "remove the integral qdot term in KL differentiation after mass conservation is supplied",
    note := "Small derivative-target rewrite; mass conservation itself remains a separate theorem or hypothesis."
  }
]

def renyiDensityMemory : List LemmaMemoryEntry := [
  {
    key := "renyi-density.integrand-positivity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.InformationTheory.Renyi.renyiIntegrand_pos",
    upstreamDecl := "Real.rpow_pos_of_pos / Real.rpow_nonneg",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.Pow.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Renyi", "density", "positivity", "rpow"],
    saldUse := "Chewi DENS/FI root: expose Renyi integrand positivity before integral and derivative contracts",
    note := "Companion nonnegative theorem is `renyiIntegrand_nonneg`; full Renyi divergence remains separate."
  },
  {
    key := "renyi-density.integrand-measurable",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.InformationTheory.Renyi.measurable_renyiIntegrandENNReal",
    upstreamDecl := "Real.continuous_rpow_const / Measurable.ennreal_ofReal",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.Pow.Continuity; Mathlib.MeasureTheory.Constructions.BorelSpace.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Renyi", "density", "measurability", "ENNReal"],
    saldUse := "Chewi DENS/FI root: turn measurable density representatives into a measurable Renyi lintegrand",
    note := "Requires order `a ∈ [0,1]`; representative choice and absolute continuity stay explicit."
  },
  {
    key := "renyi-density.integral-finite-envelope",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.InformationTheory.Renyi.lintegral_renyiIntegrandENNReal_ne_top_of_ae_le",
    upstreamDecl := "lintegral_mono_ae / ne_top_of_le_ne_top",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Lebesgue.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Renyi", "density", "lintegral", "envelope", "finite"],
    saldUse := "Chewi DENS/FI root: reduce Renyi integrability to a finite ENNReal envelope",
    note := "This mirrors the Gibbs finite-envelope contract and keeps tail/domination estimates outside the algebra leaf."
  },
  {
    key := "renyi-density.pointwise-derivative",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.InformationTheory.Renyi.hasDerivAt_renyiIntegrand",
    upstreamDecl := "HasDerivAt.rpow_const / HasDerivAt.mul",
    upstreamFile := "Mathlib.Analysis.SpecialFunctions.Pow.Deriv",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Renyi", "density", "pointwise-derivative", "rpow"],
    saldUse := "Chewi chapter 6 root: isolate pointwise Renyi derivative algebra before dominated differentiation under the integral",
    note := "Positivity/nonzero, domination, and path-space regularity remain explicit source contracts."
  }
]

def variationalMemory : List LemmaMemoryEntry := [
  {
    key := "dv.scaled-test.energy-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.InformationTheory.DonskerVaradhan.dvVariationalScaledTestEnergyBound",
    upstreamDecl := "Donsker--Varadhan one-sided variational consequence",
    upstreamFile := "Boucheron-style cited result / future SLT entropy-duality port",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["DV", "KL", "energy"],
    saldUse := "convert finite log-mgf and KL hypotheses into residual energy bounds",
    note := "Small compiled consequence; full DV theorem remains a cited-result obligation."
  },
  {
    key := "lsi.sqrt-density.fisher-chain",
    localDecl := "AutoSamplingTheory.lsiKlFiSqrtDensityFisherChainIntegralHandoffScalar",
    upstreamDecl := "LSI density and Fisher-information bookkeeping",
    upstreamFile := "Mathlib/SLT-inspired entropy and LSI proof shape",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["LSI", "FI", "density"],
    saldUse := "bookkeeping for LSI-to-KL/FI handoff after density assumptions are supplied",
    note := "Compiled scalar/integral algebra; full LSI analytic theorem remains an obligation."
  },
  {
    key := "poincare.variance",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance",
    upstreamDecl := "MeasureTheory.integral",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "variance", "definition"],
    saldUse := "shared Chapter 2 variance interface with the centering convention visible in Lean",
    note := "The integral is totalized; consumers must carry the separate admissibility hypotheses."
  },
  {
    key := "poincare.dirichlet-energy",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.dirichletEnergy",
    upstreamDecl := "Analysis.Calculus.gradient / MeasureTheory.integral",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; Mathlib.MeasureTheory.Integral.Bochner.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "Dirichlet-energy", "definition"],
    saldUse := "shared gradient-energy term for Poincare statements and later semigroup dissipation leaves",
    note := "This is the Euclidean/inner-product energy interface, not a closed Dirichlet-form construction."
  },
  {
    key := "poincare.admissible",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible",
    upstreamDecl := "MeasureTheory.Integrable",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "integrability", "domain"],
    saldUse := "prevent totalized integrals from hiding the variance and gradient-energy domain",
    note := "Function, centered square, and squared gradient integrability are all explicit."
  },
  {
    key := "poincare.satisfies",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Satisfies",
    upstreamDecl := "Poincare inequality, Chewi section 2.1",
    upstreamFile := "Log-Concave Sampling, Chapter 2",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "test-class", "interface"],
    saldUse := "typed replacement for string-only PI task contracts on an explicit test class",
    note := "Probability normalization is explicit; no concrete target measure is asserted to satisfy PI here."
  },
  {
    key := "poincare.variance-nonnegative",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_nonneg",
    upstreamDecl := "integral_nonneg_of_ae / sq_nonneg",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "variance", "nonnegative"],
    saldUse := "basic order leaf for variance estimates",
    note := "Proves nonnegativity of the explicit centered-square integral."
  },
  {
    key := "poincare.dirichlet-energy-nonnegative",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.dirichletEnergy_nonneg",
    upstreamDecl := "integral_nonneg_of_ae / sq_nonneg",
    upstreamFile := "Mathlib.MeasureTheory.Integral.Bochner.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "Dirichlet-energy", "nonnegative"],
    saldUse := "order-theoretic leaf used when changing Poincare constants",
    note := "No differentiability claim is needed because Mathlib derivatives are totalized."
  },
  {
    key := "poincare.constant-monotonicity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.mono_constant",
    upstreamDecl := "mul_le_mul_of_nonneg_right",
    upstreamFile := "Mathlib algebra/order API",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "constant", "monotonicity"],
    saldUse := "reuse a proved PI bound at any larger nonnegative constant",
    note := "Preserves the same test class and exact admissibility domain."
  },
  {
    key := "poincare.variance-bound-elimination",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_le",
    upstreamDecl := "Poincare.Satisfies",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "consumer", "interface"],
    saldUse := "stable consumer API for extracting the PI inequality",
    note := "Requires explicit test membership and admissibility."
  },
  {
    key := "poincare.test-class-monotonicity",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.mono_tests",
    upstreamDecl := "Set inclusion",
    upstreamFile := "Mathlib.Data.Set.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "chapter-2", "Poincare", "test-class", "monotonicity"],
    saldUse := "restrict a PI package to a smaller core or downstream test class",
    note := "Keeps probability normalization, constant, and admissibility unchanged."
  }
]

def geometryMemory : List LemmaMemoryEntry := [
  {
    key := "geometry.chewi-definition-1-3-26",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.GeodesicConvexity.IsAlphaGeodesicallyConvex",
    upstreamDecl := "Chewi Definition 1.3.26, condition 1",
    upstreamFile := "Log-Concave Sampling, book page 31 / PDF page 43",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "geodesic-convexity", "metric-space", "interpolation", "definition"],
    saldUse := "Chewi Definition 1.3.26 root: state alpha-geodesic convexity through the endpoint interpolation inequality along every selected geodesic",
    note := "The geodesic predicate remains an explicit parameter so Riemannian and Wasserstein realizations can supply their own constant-speed/domain conditions."
  },
  {
    key := "geometry.chewi-display-1-4-7",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.GeodesicConvexity.firstOrder_geodesicConvexity",
    upstreamDecl := "HasDerivAt.tendsto_slope / le_of_tendsto_of_tendsto",
    upstreamFile := "Mathlib.Analysis.Calculus.Deriv.Slope; Chewi display (1.4.7)",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "geodesic-convexity", "first-order-condition", "derivative", "Wasserstein"],
    saldUse := "Derive the first-order alpha-convexity inequality from the endpoint chord condition along a differentiable geodesic",
    note := "The proof takes the positive-time secant-slope limit. Concrete Riemannian or Wasserstein geometry must identify the path derivative with its gradient pairing."
  },
  {
    key := "geometry.chewi-definition-1-3-16",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.MetricCurve.IsAbsolutelyContinuousMetricCurve",
    upstreamDecl := "Chewi Definition 1.3.16 (informal)",
    upstreamFile := "Log-Concave Sampling, book page 26 / PDF page 38",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "metric-derivative", "absolutely-continuous-curve", "Wasserstein", "definition"],
    saldUse := "Chewi Definition 1.3.16 root: require a finite nonnegative punctured-neighborhood metric derivative at almost every time",
    note := "Matches the source's explicitly informal definition. The standard upper-gradient characterization and Wasserstein specialization remain theorem routes."
  },
  {
    key := "geometry.euclidean-space.inner-toLp-toLp-sum",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates.euclideanSpace_inner_toLp_toLp_eq_sum_mul",
    upstreamDecl := "PiLp.inner_apply",
    upstreamFile := "Mathlib.Analysis.InnerProductSpace.PiL2",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "EuclideanSpace", "inner-product", "coordinates", "WithLp.toLp", "finite-dimensional"],
    saldUse := "Chewi GAUSS/SDE root: bridge coordinate gradient representatives to Mathlib `EuclideanSpace` inner-product notation",
    note := "Pure finite-dimensional coordinate identity; it does not define gradients, divergence, Laplacian, or analytic regularity."
  },
  {
    key := "geometry.euclidean-space.inner-sum",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates.euclideanSpace_inner_eq_sum_mul",
    upstreamDecl := "PiLp.inner_apply",
    upstreamFile := "Mathlib.Analysis.InnerProductSpace.PiL2",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "EuclideanSpace", "inner-product", "coordinates", "finite-dimensional"],
    saldUse := "Chewi GAUSS/SDE root: expose the direct finite-coordinate formula for `inner ℝ u v` in `EuclideanSpace ℝ ι`",
    note := "Reusable notation bridge for Gaussian and Langevin finite-dimensional leaves; no calculus or measure statement is hidden here."
  },
  {
    key := "geometry.log-concavity.def",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn",
    upstreamDecl := "ConcaveOn / strictConcaveOn_log_Ioi",
    upstreamFile := "Mathlib.Analysis.Convex.Function; Mathlib.Analysis.Convex.SpecificFunctions.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "convex-analysis", "density"],
    saldUse := "Chewi CONV/DENS root: shared definition for positive density log-concavity leaves",
    note := "Small ASTIS-owned wrapper around Mathlib ConcaveOn with explicit positivity."
  },
  {
    key := "geometry.log-concavity.negative-log-potential-convex",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.convexOn_neg_log",
    upstreamDecl := "ConcaveOn.neg",
    upstreamFile := "Mathlib.Analysis.Convex.Function",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "negative-log", "convex-potential", "Gibbs", "density"],
    saldUse := "Chewi DENS/CONV/SDE root: extract the convex potential `-log f` from a positive log-concave density",
    note := "Converse interface to the existing `exp (-V)` log-concavity leaf; useful for Gibbs potentials, score/FI, and Langevin generator subtrees."
  },
  {
    key := "geometry.log-concavity.negative-log-potential-sublevel-convex",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.convex_sublevel_neg_log",
    upstreamDecl := "ConvexOn.quasiconvexOn / LogConcaveOn.convexOn_neg_log",
    upstreamFile := "Mathlib.Analysis.Convex.Quasiconvex; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "negative-log", "sublevel", "convex-set", "localization"],
    saldUse := "Chewi CONV/DENS root: turn log-concave density energy sublevels into convex sets",
    note := "Energy-sublevel counterpart to positive-density superlevel convexity; supports localization and warm-start geometry."
  },
  {
    key := "geometry.log-concavity.positive-ray-id",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_id_Ioi",
    upstreamDecl := "strictConcaveOn_log_Ioi",
    upstreamFile := "Mathlib.Analysis.Convex.SpecificFunctions.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "positive-ray", "convex-analysis"],
    saldUse := "Chewi CONV sanity leaf before density/Gibbs and Prekopa--Leindler ports",
    note := "Compiled one-dimensional leaf reusing Mathlib's strict concavity of log."
  },
  {
    key := "geometry.log-concavity.linear-precomposition",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.comp_linearMap",
    upstreamDecl := "ConcaveOn.comp_linearMap",
    upstreamFile := "Mathlib.Analysis.Convex.Function",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "linear-map", "preimage", "density", "coordinate"],
    saldUse := "Chewi CONV/DENS root: pull log-concave density factors through linear coordinate maps",
    note := "Preimage-domain transport leaf for coordinate projections, linear observations, and product-density factors."
  },
  {
    key := "geometry.log-concavity.affine-precomposition",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.comp_affineMap",
    upstreamDecl := "ConcaveOn.comp_affineMap",
    upstreamFile := "Mathlib.Analysis.Convex.Function",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "affine-map", "preimage", "density", "shift"],
    saldUse := "Chewi CONV/DENS root: preserve log-concavity under shifts and affine coordinate changes",
    note := "Vector-space affine transport leaf; useful for shifted Gaussian/Gibbs densities and restricted affine charts."
  },
  {
    key := "geometry.log-concavity.convex-superlevel",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.convex_superlevel",
    upstreamDecl := "ConcaveOn.quasiconcaveOn / Real.log_le_log_iff",
    upstreamFile := "Mathlib.Analysis.Convex.Quasiconvex; Mathlib.Analysis.SpecialFunctions.Log.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "superlevel", "convex-set", "restricted-oracle"],
    saldUse := "Chewi CONV/DENS root: identify positive-density superlevel sets as convex bodies for restrictions and localization",
    note := "Handles all real thresholds: nonpositive thresholds use positivity, positive thresholds use log monotonicity and concavity."
  },
  {
    key := "geometry.log-concavity.quasiconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.quasiconcaveOn",
    upstreamDecl := "QuasiconcaveOn / convex_superlevel",
    upstreamFile := "Mathlib.Analysis.Convex.Quasiconvex; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "quasiconcavity", "superlevel", "convex-set"],
    saldUse := "Chewi CONV root: expose log-concavity as quasiconcavity so all superlevel-set APIs become callable",
    note := "Small wrapper around `convex_superlevel`; useful for convex-body and restricted-Gaussian subtrees."
  },
  {
    key := "geometry.log-concavity.restrict-superlevel",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.restrict_superlevel",
    upstreamDecl := "LogConcaveOn.subset / LogConcaveOn.convex_superlevel",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "superlevel", "restriction", "restricted-oracle"],
    saldUse := "Chewi CONV/DENS root: preserve log-concavity when restricting a density to a convex superlevel body",
    note := "Consumer-facing restricted-density wrapper for localization, warm starts, restricted Gaussian oracles, and proximal subtrees."
  },
  {
    key := "geometry.log-concavity.positive-rescale",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.const_mul",
    upstreamDecl := "ConcaveOn.add / Real.log_mul",
    upstreamFile := "Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Log.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "normalization", "density"],
    saldUse := "Chewi DENS/CONV root: keep normalized-density positive constants out of later convexity proofs",
    note := "Separates positive scalar normalization from measure/integral normalization."
  },
  {
    key := "geometry.log-concavity.pointwise-product",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.mul",
    upstreamDecl := "ConcaveOn.add / Real.log_mul",
    upstreamFile := "Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Log.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "product", "density", "tensorization"],
    saldUse := "Chewi CONV/DENS root: multiply positive log-concave density factors on a shared domain",
    note := "Used before product-density, tilted-density, and normalized-density tensorization leaves."
  },
  {
    key := "geometry.log-concavity.nonnegative-rpow",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.rpow",
    upstreamDecl := "ConcaveOn.smul / Real.log_rpow",
    upstreamFile := "Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Pow.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "rpow", "density", "positive-function"],
    saldUse := "Chewi CONV/DENS root: nonnegative powers preserve positive log-concavity for density algebra",
    note := "Keeps exponent bookkeeping local before Renyi/Hellinger-style powered density consumers."
  },
  {
    key := "geometry.log-concavity.product-domain-product",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.LogConcaveOn.prod",
    upstreamDecl := "Convex.prod / ConcaveOn.add / Real.log_mul",
    upstreamFile := "Mathlib.Analysis.Convex.Basic; Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Log.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "log-concavity", "product-domain", "density", "tensorization"],
    saldUse := "Chewi CONV/DENS root: tensorize log-concave density factors over Cartesian product domains",
    note := "Small product-domain API used by future Prekopa, Gaussian product-density, and tensorization subtrees."
  },
  {
    key := "geometry.gibbs-density.convex-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_const_mul_exp_neg_of_convexOn",
    upstreamDecl := "ConvexOn.neg / Real.log_exp",
    upstreamFile := "Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Log.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "convex-potential", "log-concavity", "density"],
    saldUse := "Chewi DENS/CONV root for Gibbs target densities before withDensity normalization",
    note := "Compiled convex-analytic Gibbs leaf; no measure normalization or integrability is claimed."
  },
  {
    key := "geometry.convexity.absolute-value",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_abs",
    upstreamDecl := "convexOn_univ_norm / Real.norm_eq_abs",
    upstreamFile := "Mathlib.Analysis.Normed.Module.Convex",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "convexity", "absolute-value", "Laplace-tail", "one-dimensional"],
    saldUse := "Chewi CONV root: expose convexity of `|x|` for the one-dimensional Laplace density example",
    note := "Geometry counterpart of the exact one-dimensional Laplace normalizer; this is not a multidimensional norm-tail theorem."
  },
  {
    key := "geometry.convexity.absolute-linear-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_const_mul_abs_add",
    upstreamDecl := "convexOn_univ_abs / ConvexOn.smul / ConvexOn.add_const",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "convexity", "absolute-linear-potential", "Laplace-tail", "Gibbs"],
    saldUse := "Chewi CONV/DENS root: package `a|x|+b` with `0 ≤ a` as a convex Gibbs potential",
    note := "Keeps the convexity assumption for Laplace examples explicit before density normalization."
  },
  {
    key := "geometry.gibbs-density.absolute-linear-potential-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_exp_neg_abs_linear",
    upstreamDecl := "logConcaveOn_exp_neg_of_convexOn / convexOn_univ_const_mul_abs_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Laplace-tail", "log-concavity", "density", "one-dimensional"],
    saldUse := "Chewi CONV/DENS root: prove the unnormalized one-dimensional Laplace Gibbs shape is log-concave",
    note := "Geometry-only result; measure normalization is supplied by the exact Laplace normalizer leaves."
  },
  {
    key := "geometry.gibbs-density.absolute-linear-positive-rescale-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_const_mul_exp_neg_abs_linear",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_of_convexOn / convexOn_univ_const_mul_abs_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Laplace-tail", "log-concavity", "normalization", "density"],
    saldUse := "Chewi DENS/CONV root: preserve log-concavity after multiplying the Laplace shape by a positive normalizing constant",
    note := "Use with `analysis.integrability.laplace-absolute-linear-tail-ennreal-normalizer`; it does not construct a probability measure by itself."
  },
  {
    key := "geometry.gibbs-density.explicit-laplace-normalized-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_explicit_abs_linear_normalized_density",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_abs_linear / positivity of `2*exp(-b)/a`",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Laplace-tail", "log-concavity", "normalizer", "density"],
    saldUse := "Chewi DENS/CONV root: expose the explicitly normalized one-dimensional Laplace-type real density as log-concave",
    note := "Real-density geometry companion to the exact ENNReal normalizer and withDensity probability theorem."
  },
  {
    key := "geometry.strong-convexity.convex-potential-nonnegative-modulus",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity.convexOn_of_strongConvexOn_nonneg",
    upstreamDecl := "StrongConvexOn.mono / strongConvexOn_zero",
    upstreamFile := "Mathlib.Analysis.Convex.Strong",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "strong-convexity", "convexity", "convex-potential", "density"],
    saldUse := "Chewi CONV/DENS root: translate strongly convex potential assumptions into ordinary convex-potential geometry",
    note := "Uses Mathlib's strong-convexity monotonicity to lower the modulus to zero; requires `0 ≤ k`."
  },
  {
    key := "geometry.strong-convexity.gibbs-shape-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity.logConcaveOn_exp_neg_of_strongConvexOn",
    upstreamDecl := "convexOn_of_strongConvexOn_nonneg / logConcaveOn_exp_neg_of_convexOn",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "strong-convexity", "Gibbs", "log-concavity", "density"],
    saldUse := "Chewi DENS/CONV root: expose the unnormalized Gibbs density shape of a strongly convex potential as log-concave",
    note := "Geometry-only bridge; it does not claim a finite normalizer, invariant law, or functional inequality."
  },
  {
    key := "geometry.strong-convexity.normalized-gibbs-shape-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity.logConcaveOn_const_mul_exp_neg_of_strongConvexOn",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_of_convexOn / convexOn_of_strongConvexOn_nonneg",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "strong-convexity", "Gibbs", "log-concavity", "normalization", "density"],
    saldUse := "Chewi DENS/CONV root: keep positive scalar normalizers separate while preserving strong-convex Gibbs log-concavity",
    note := "Pairs with the normalized Gibbs probability branch after a positive normalizing constant has been constructed separately."
  },
  {
    key := "geometry.strong-convexity.minimizer-centered-quadratic-lower-bound",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity.centered_quadratic_lower_bound_of_strongConvexOn_minimizer",
    upstreamDecl := "StrongConvexOn / IsMinOn / UniformConvexOn midpoint inequality",
    upstreamFile := "Mathlib.Analysis.Convex.Strong; Mathlib.Order.Filter.Extr",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "strong-convexity", "minimizer", "quadratic-lower-bound", "Gibbs", "coercivity"],
    saldUse := "Chewi CONV/DENS root: expose the quadratic tail envelope used by strong log-concavity and Gibbs normalization",
    note := "Mathlib-native `StrongConvexOn` bridge with an explicit global minimizer; proves the robust midpoint `k/4` envelope."
  },
  {
    key := "geometry.convexity.norm-square",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_norm_sq",
    upstreamDecl := "norm_add_le / norm_smul / sq_le_sq₀",
    upstreamFile := "Mathlib.Analysis.Normed.Group.Basic; Mathlib.Analysis.Normed.MulAction; Mathlib.Algebra.Order.GroupWithZero.Unbundled.Basic",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "convexity", "norm-square", "quadratic", "normed-space"],
    saldUse := "Chewi CONV root: reusable convexity of the quadratic norm energy `‖x‖^2`",
    note := "Works in any real normed vector space; uses the triangle inequality and scalar Jensen algebra."
  },
  {
    key := "geometry.convexity.quadratic-norm-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_const_mul_norm_sq_add",
    upstreamDecl := "convexOn_univ_norm_sq / ConvexOn.smul / ConvexOn.add_const",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity; Mathlib.Analysis.Convex.Function",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "convexity", "quadratic-potential", "Gibbs", "density"],
    saldUse := "Chewi DENS/CONV root: package nonnegative quadratic norm potentials `a‖x‖^2+b` as convex",
    note := "This is the convex-geometry counterpart of the exact quadratic normalizer in Analysis.Integrability."
  },
  {
    key := "geometry.gibbs-density.quadratic-potential-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_exp_neg_quadratic_norm",
    upstreamDecl := "logConcaveOn_exp_neg_of_convexOn / convexOn_univ_const_mul_norm_sq_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "quadratic-potential", "log-concavity", "density"],
    saldUse := "Chewi DENS/CONV root: prove `exp (-(a‖x‖^2+b))` is log-concave before measure normalization",
    note := "Keeps log-concavity separate from Lebesgue integrability and probability-measure construction."
  },
  {
    key := "geometry.gibbs-density.quadratic-positive-rescale-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_const_mul_exp_neg_quadratic_norm",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_of_convexOn / convexOn_univ_const_mul_norm_sq_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "quadratic-potential", "normalization", "log-concavity", "density"],
    saldUse := "Chewi DENS/CONV root: positive scalar normalizers preserve quadratic Gibbs log-concavity",
    note := "This removes scalar-normalizer bookkeeping from later invariant-law and Prekopa-style leaves."
  },
  {
    key := "geometry.gibbs-density.explicit-quadratic-normalized-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_explicit_quadratic_normalized_density",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_quadratic_norm / Real.rpow_pos_of_pos",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity; Mathlib.Analysis.SpecialFunctions.Pow.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Lebesgue", "quadratic", "normalizer", "log-concavity", "finite-dimensional"],
    saldUse := "Chewi DENS/CONV root: connect the explicit finite-dimensional quadratic normalizer to log-concavity of the normalized density",
    note := "Geometric companion to `isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sq`; it claims density log-concavity, not a measure-level theorem."
  },
  {
    key := "geometry.convexity.shifted-quadratic-norm-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_const_mul_norm_sub_sq_add",
    upstreamDecl := "ConvexOn.comp_affineMap / convexOn_univ_const_mul_norm_sq_add",
    upstreamFile := "Mathlib.Analysis.Convex.Function; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "convexity", "shifted-quadratic", "Gibbs", "density", "affine-map"],
    saldUse := "Chewi DENS/CONV/GAUSS root: package shifted quadratic potentials `a‖x-m‖^2+b` as convex",
    note := "Uses affine precomposition of the centered quadratic norm potential; this is the geometry leaf behind shifted Gaussian/Gibbs densities."
  },
  {
    key := "geometry.gibbs-density.shifted-quadratic-potential-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_exp_neg_shifted_quadratic_norm",
    upstreamDecl := "logConcaveOn_exp_neg_of_convexOn / convexOn_univ_const_mul_norm_sub_sq_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "shifted-quadratic", "log-concavity", "density", "Gaussian"],
    saldUse := "Chewi DENS/CONV/GAUSS root: prove `exp (-(a‖x-m‖^2+b))` is log-concave before measure normalization",
    note := "Shifted counterpart of the centered quadratic Gibbs shape; measure-level translation invariance remains separate."
  },
  {
    key := "geometry.gibbs-density.shifted-quadratic-positive-rescale-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_const_mul_exp_neg_shifted_quadratic_norm",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_of_convexOn / convexOn_univ_const_mul_norm_sub_sq_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "shifted-quadratic", "normalization", "log-concavity", "density"],
    saldUse := "Chewi DENS/CONV/GAUSS root: positive scalar normalizers preserve shifted quadratic Gibbs log-concavity",
    note := "Keeps shifted-density scalar normalization separate from exact Lebesgue normalizer and withDensity probability leaves."
  },
  {
    key := "geometry.gibbs-density.explicit-shifted-quadratic-normalized-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_explicit_shifted_quadratic_normalized_density",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_shifted_quadratic_norm / Real.rpow_pos_of_pos",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity; Mathlib.Analysis.SpecialFunctions.Pow.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Gaussian", "shifted-quadratic", "normalizer", "log-concavity", "finite-dimensional"],
    saldUse := "Chewi DENS/CONV/GAUSS root: connect the explicit finite-dimensional quadratic normalizer to shifted density log-concavity",
    note := "Geometric shifted-density companion to exact quadratic normalizer leaves; it does not assert the translated Lebesgue integral identity."
  },
  {
    key := "geometry.convexity.pair-sub-quadratic-kernel-potential",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.convexOn_univ_const_mul_norm_fst_sub_snd_sq_add",
    upstreamDecl := "ConvexOn.comp_linearMap / convexOn_univ_const_mul_norm_sq_add",
    upstreamFile := "Mathlib.Analysis.Convex.Function; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "convexity", "pair-difference", "quadratic-kernel", "proximal", "coupling"],
    saldUse := "Chewi DENS/CONV/GAUSS/DISC root: package two-point potentials `a‖x-y‖^2+b` as convex on product space",
    note := "Uses the linear map `(x,y) ↦ x-y`; this is the geometry leaf behind Gaussian transition and proximal-kernel log-concavity."
  },
  {
    key := "geometry.gibbs-density.pair-sub-quadratic-kernel-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_exp_neg_pair_sub_quadratic_norm",
    upstreamDecl := "logConcaveOn_exp_neg_of_convexOn / convexOn_univ_const_mul_norm_fst_sub_snd_sq_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Gaussian-kernel", "pair-difference", "log-concavity", "proximal"],
    saldUse := "Chewi DENS/CONV/GAUSS/DISC root: prove `exp (-(a‖x-y‖^2+b))` is log-concave as a kernel shape",
    note := "Product-space kernel geometry only; transition-kernel measurability and conditional normalization remain separate leaves."
  },
  {
    key := "geometry.gibbs-density.pair-sub-quadratic-kernel-positive-rescale-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_const_mul_exp_neg_pair_sub_quadratic_norm",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_of_convexOn / convexOn_univ_const_mul_norm_fst_sub_snd_sq_add",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Gaussian-kernel", "normalization", "pair-difference", "log-concavity"],
    saldUse := "Chewi DENS/CONV/GAUSS/DISC root: positive constants preserve two-point Gaussian-kernel log-concavity",
    note := "Keeps scalar kernel constants separate from Markov kernel mass, detailed balance, and Lebesgue integral identities."
  },
  {
    key := "geometry.gibbs-density.explicit-pair-sub-quadratic-kernel-logconcave",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity.logConcaveOn_explicit_pair_sub_quadratic_kernel",
    upstreamDecl := "logConcaveOn_const_mul_exp_neg_pair_sub_quadratic_norm / Real.rpow_pos_of_pos",
    upstreamFile := "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity; Mathlib.Analysis.SpecialFunctions.Pow.Real",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Chewi", "Gibbs", "Gaussian-kernel", "proximal", "pair-difference", "normalizer", "log-concavity"],
    saldUse := "Chewi GAUSS/DISC root: log-concavity of finite-dimensional Gaussian-kernel shapes with the usual conditional normalizing constant",
    note := "This is not a probability-density theorem on product volume; it is the reusable convex-geometric kernel-shape leaf."
  }
]

def saldExtractedMemory : List LemmaMemoryEntry := [
  {
    key := "sald.gronwall.scalar-rewrites",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.SALDExtracted.gronwallExpProductRewriteScalar",
    upstreamDecl := "SALD appendix Gronwall proof plus elementary exponential algebra",
    upstreamFile := "AutoSamplingTheory/SALD.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Gronwall", "scalar-algebra", "SALD-extracted"],
    saldUse := "forward-KL and discrete forward-KL Gronwall display algebra",
    note := "Compiled in SALD and exposed through TechnicalLemmas.SALDExtracted."
  },
  {
    key := "sald.em-endpoint-law-handoff",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.SALDExtracted.discreteForwardKlEmEndpointLawPairHandoff",
    upstreamDecl := "SALD discrete EM endpoint law bookkeeping",
    upstreamFile := "AutoSamplingTheory/SALD.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Euler-Maruyama", "endpoint-law", "SALD-extracted"],
    saldUse := "endpoint-law pair handoff for discrete SALD/VA-SALD proofs",
    note := "SALD-derived local theorem exposed as a searchable memory item."
  },
  {
    key := "sald.brownian-normalization-bridges",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.SALDExtracted.selectedWeakTestNormalizedCoordinateLawOfStdGaussianVectorLaw",
    upstreamDecl := "SALD Brownian/Ito normalized-coordinate law bridge",
    upstreamFile := "AutoSamplingTheory/SALD.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian", "Ito", "Gaussian", "SALD-extracted"],
    saldUse := "active Brownian/Ito scalar generator backend and coordinate variance leaves",
    note := "Domain-specific SALD bridge; can be generalized later if reused."
  },
  {
    key := "sald.remainder-meas-gaussian-law",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.SALDExtracted.selectedWeakTestRemainderMeasOfStdGaussianVectorLaw",
    upstreamDecl := "SALD Brownian/Ito normalized-remainder measurability bridge",
    upstreamFile := "AutoSamplingTheory/SALD.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian", "Ito", "Gaussian", "measurability", "SALD-extracted"],
    saldUse := "discharge hRemainderMeas in the active Brownian/Ito Taylor moment backend",
    note := "Cycle 194 bridge transporting AEStronglyMeasurable across the normalized coordinate-law and variance equalities."
  },
  {
    key := "sald.remainder-bound-gaussian-law",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.SALDExtracted.selectedWeakTestRemainderBoundOfStdGaussianVectorLaw",
    upstreamDecl := "SALD Brownian/Ito normalized-remainder domination bridge",
    upstreamFile := "AutoSamplingTheory/SALD.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian", "Ito", "Gaussian", "domination", "SALD-extracted"],
    saldUse := "narrow hRemainderBound to normalized-coordinate-law domination in the active Brownian/Ito Taylor moment backend",
    note := "Cycle 194 bridge transporting ae domination across the normalized coordinate-law and variance equalities."
  },
  {
    key := "sald.remainder-bound-integrable-gaussian-law",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.SALDExtracted.selectedWeakTestRemainderBoundIntegrableOfStdGaussianVectorLaw",
    upstreamDecl := "SALD Brownian/Ito normalized-remainder dominating-bound integrability bridge",
    upstreamFile := "AutoSamplingTheory/SALD.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian", "Ito", "Gaussian", "integrability", "SALD-extracted"],
    saldUse := "narrow hRemainderBoundInt to normalized-coordinate-law integrability in the active Brownian/Ito Taylor moment backend",
    note := "Cycle 195 bridge transporting MeasureTheory.Integrable across the normalized coordinate-law and variance equalities."
  },
  {
    key := "sald.normalized-remainder-bound-int-quadratic",
    localDecl := "AutoSamplingTheory.TechnicalLemmas.SALDExtracted.selectedWeakTestNormalizedRemainderBoundIntOfQuadraticBound",
    upstreamDecl := "SALD Brownian/Ito normalized-remainder quadratic domination integrability bridge",
    upstreamFile := "AutoSamplingTheory/SALD.lean",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["Brownian", "Ito", "Gaussian", "integrability", "quadratic-bound", "SALD-extracted"],
    saldUse := "narrow hNormalizedRemainderBoundInt to hNormalizedRemainderBoundDef plus normalized-coordinate-law integrability",
    note := "Cycle 196 bridge from source-cited remainderBound = C * z ^ 2 to normalized-coordinate-law integrability."
  }
]

def portQueueMemory : List LemmaMemoryEntry := [
  {
    key := "dv.entropy-duality",
    localDecl := "",
    upstreamDecl := "entropy_duality",
    upstreamFile := "SLT/GaussianLSI/DualityEntropy.lean",
    status := LemmaMemoryStatus.portCandidate,
    tags := ["DV", "entropy", "KL"],
    saldUse := "Donsker--Varadhan variational backend for KL energy bounds",
    note := "Port only when DV becomes the active dynamic leaf."
  },
  {
    key := "lsi.product-gaussian",
    localDecl := "",
    upstreamDecl := "gaussian_logSobolev_W12_pi",
    upstreamFile := "SLT/GaussianLSI/TensorizedGLSI.lean",
    status := LemmaMemoryStatus.portCandidate,
    tags := ["LSI", "Gaussian", "product"],
    saldUse := "LSI-to-KL/FI backend when the faithful proof reaches this cited-result boundary",
    note := "Large theorem; keep as queue entry until a local ASTIS declaration compiles."
  }
]

def technicalLemmaMemory : List LemmaMemoryEntry :=
  analysisMemory ++ gaussianMemory ++ taylorMemory ++ calculusMemory ++ measureMemory ++ functionalInequalityMemory ++ stochasticProcessMemory ++
    klDensityMemory ++ renyiDensityMemory ++ variationalMemory ++ geometryMemory ++
    saldExtractedMemory ++ portQueueMemory

def formalizedTechnicalLemmaCount : Nat :=
  (technicalLemmaMemory.filter fun entry =>
    entry.status == LemmaMemoryStatus.formalizedLocal).length

end TechnicalLemmas
end AutoSamplingTheory
