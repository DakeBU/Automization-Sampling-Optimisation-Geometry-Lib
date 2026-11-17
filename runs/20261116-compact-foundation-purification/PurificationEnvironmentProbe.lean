import AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder
import AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates
import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator
import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianDiffusionQuadraticVariation
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMixedQuadraticVariation
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianPredictableQuadraticVariationL2
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicBlockWeights
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicCutoffIncrements
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicWeightedLimits
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteVariationDyadicQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoActualTaylorRemainder
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoBoundedCellMultiplier
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCellMultiplier
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoContinuousRowQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicHessian
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicLinearTerm
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixCrossQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicTaylorRemainder
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicWeightedCovariation
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoElementaryRowQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanGradientWeights
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanTaylorRemainder
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoFiniteVariationQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoGeneratorIntegrability
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoInitializedDrift
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralElementaryIncrement
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridEnergy
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridStability
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralIncrement
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoStoppedRowQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTaylorGridRemainder
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressivePathEnergy
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereCoordinateSDE
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoFormula
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoIntegratedRows
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableCoordinateSDE
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableWeakForward
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereWeakForward
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMartingaleEvolution
import Mathlib.Tactic.MinImports

open Lean in
run_cmd do
  let selected : Array Name := #[
    `AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder,
    `AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates,
    `AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator,
    `AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianDiffusionQuadraticVariation,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMixedQuadraticVariation,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianPredictableQuadraticVariationL2,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicBlockWeights,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicCutoffIncrements,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicWeightedLimits,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteVariationDyadicQV,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoActualTaylorRemainder,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoBoundedCellMultiplier,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCellMultiplier,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoContinuousRowQV,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicHessian,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicLinearTerm,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixCrossQV,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicTaylorRemainder,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicWeightedCovariation,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoElementaryRowQV,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanGradientWeights,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanTaylorRemainder,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoFiniteVariationQV,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoGeneratorIntegrability,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoInitializedDrift,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralElementaryIncrement,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridEnergy,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridStability,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralIncrement,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoStoppedRowQV,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTaylorGridRemainder,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressivePathEnergy,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereCoordinateSDE,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoFormula,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoIntegratedRows,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableCoordinateSDE,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableWeakForward,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereWeakForward,
    `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMartingaleEvolution]
  let importSets : Array (Name × Array Name) := #[
    (`AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder, #[`Mathlib.Analysis.Calculus.ContDiff.Comp, `Mathlib.Analysis.Calculus.Deriv.Pow, `Mathlib.Analysis.Calculus.MeanValue, `Mathlib.Analysis.Normed.Operator.BoundedLinearMaps, `Mathlib.Topology.MetricSpace.Thickening]),
    (`AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates, #[`Mathlib.Analysis.InnerProductSpace.PiL2, `Mathlib.LinearAlgebra.Basis.Bilinear]),
    (`AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator, #[`AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise, `Mathlib.Analysis.InnerProductSpace.Laplacian]),
    (`AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise, #[`Mathlib.Analysis.InnerProductSpace.PiL2, `Mathlib.Analysis.InnerProductSpace.Calculus, `Mathlib.Tactic]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianDiffusionQuadraticVariation, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMixedQuadraticVariation, `Mathlib.Algebra.Order.Chebyshev]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMixedQuadraticVariation, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianPredictableQuadraticVariationL2, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.EuclideanBrownianCoordinates]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianPredictableQuadraticVariationL2, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianQuadraticVariationL2]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative, #[`Mathlib.MeasureTheory.Constructions.BorelSpace.Basic]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure, #[`Mathlib.MeasureTheory.Function.ConvergenceInMeasure, `Mathlib.MeasureTheory.OuterMeasure.BorelCantelli]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicBlockWeights, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicCutoffIncrements, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicWeightedLimits, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicBlockWeights, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure, `Mathlib.MeasureTheory.Function.StronglyMeasurable.Basic]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteVariationDyadicQV, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement, `Mathlib.Topology.EMetricSpace.BoundedVariation]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoActualTaylorRemainder, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanTaylorRemainder, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoBoundedCellMultiplier, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCellMultiplier, `Mathlib.MeasureTheory.Function.SimpleFuncDenseLp]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCellMultiplier, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.RandomStoppingProcessConsistency, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcessCongruence]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicLinearTerm, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicHessian, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoActualTaylorRemainder, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoContinuousRowQV, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoElementaryRowQV, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridStability]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicHessian, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative, `AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicWeightedCovariation, `Mathlib.Analysis.Calculus.ContDiff.Comp]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicLinearTerm, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoInitializedDrift, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanGradientWeights, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixCrossQV, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicCutoffIncrements, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoFiniteVariationQV]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicTaylorRemainder, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTaylorGridRemainder, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteTimeGrid, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicWeightedCovariation, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicWeightedLimits, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixCrossQV]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoElementaryRowQV, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianDiffusionQuadraticVariation, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralElementaryIncrement, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressivePathEnergy]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanGradientWeights, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcessAfterHorizon, `Mathlib.Analysis.Calculus.ContDiff.Comp]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.EuclideanBrownianCoordinates, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess, `Mathlib.Analysis.Normed.Lp.MeasurableSpace]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanTaylorRemainder, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicTaylorRemainder, `Mathlib.Analysis.InnerProductSpace.PiL2]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoFiniteVariationQV, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteVariationDyadicQV, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoStoppedRowQV]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoGeneratorIntegrability, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2, `AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates, `Mathlib.Analysis.Calculus.ContDiff.Comp, `Mathlib.MeasureTheory.Integral.Prod]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoInitializedDrift, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveDriftIntegral, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralElementaryIncrement, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridEnergy, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralIncrement]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridStability, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralGridEnergy, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcessCongruence]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralIncrement, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoStoppedRowQV, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoContinuousRowQV, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.RandomStoppingProcessConsistency]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoTaylorGridRemainder, #[`AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder, `Mathlib.MeasureTheory.Function.ConvergenceInMeasure, `Mathlib.MeasureTheory.Constructions.BorelSpace.Basic]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums, #[`AutoSamplingTheory.TechnicalLemmas.Analysis.PrefixIntegral, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoBoundedCellMultiplier, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement, `Mathlib.Topology.EMetricSpace.BoundedVariation]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressivePathEnergy, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoL2, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2Algebra]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereCoordinateSDE, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactProgressiveCoefficients, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereWeakForward]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoFormula, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula, `AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator, `Mathlib.MeasureTheory.Function.LocallyIntegrable]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoIntegratedRows, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula, `AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoGeneratorIntegrability]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableCoordinateSDE, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveCoefficientBounds, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereCoordinateSDE, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableWeakForward]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableWeakForward, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoIntegratedRows, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.TimeMeasureRealBridge, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMeasurableEvolution]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereWeakForward, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereItoFormula, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.TimeMeasureRealBridge, `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMartingaleEvolution]),
    (`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMartingaleEvolution, #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw, `Mathlib.Probability.Martingale.Basic])]
  let env ← getEnv
  let mut moduleMap : Std.HashMap Nat Name := {}
  for imp in env.header.moduleNames do
    moduleMap := moduleMap.insert ((env.getModuleIdx? imp).getD default) imp
  let moduleOf := fun n => match env.getModuleIdxFor? n with
    | some idx => (moduleMap.get? idx).getD .anonymous
    | none => .anonymous
  let mut rows : Array Json := #[]
  for (name, info) in env.constants.toList do
    let owner := moduleOf name
    if selected.contains owner then
      let kind := match info with
        | .thmInfo _ => "theorem"
        | .defnInfo _ => "definition"
        | .opaqueInfo _ => "opaque"
        | .axiomInfo _ => "axiom"
        | .ctorInfo _ => "constructor"
        | .recInfo _ => "recursor"
        | .inductInfo _ => "inductive"
        | .quotInfo _ => "quotient"
      let refs := fun (e : Expr) => e.getUsedConstants.map fun n =>
        Json.mkObj [("constant", toJson n.toString), ("module", toJson (moduleOf n).toString)]
      let body := match info.value? (allowOpaque := true) with
        | some b => refs b
        | none => #[]
      rows := rows.push (Json.mkObj [
        ("name", toJson name.toString), ("module", toJson owner.toString),
        ("kind", toJson kind), ("type_constants", Json.arr (refs info.type)),
        ("body_constants", Json.arr body)])
  let mut importRows : Array Json := #[]
  for (mod, imps) in importSets do
    importRows := importRows.push (Json.mkObj [
      ("module", toJson mod.toString),
      ("imports", toJson (imps.map Name.toString)),
      ("transitively_redundant_direct_imports", toJson ((env.findRedundantImports imps).toArray.map Name.toString))])
  logInfo m!"COMPACT_PURIFICATION_ENV_V1 {(Json.mkObj [("declarations",Json.arr rows),("import_coverage",Json.arr importRows)]).compress}"
