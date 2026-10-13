import AutoSamplingTheory.Probability

/-!
# SDE and discretization contracts
-/

namespace AutoSamplingTheory

structure ItoDiffusionContract where
  id : String
  forwardSde : String
  marginalPath : String
  reversePath : String
  velocityFormula : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.contractOnly
deriving Repr, DecidableEq

structure FokkerPlanckContract where
  id : String
  lawName : String
  equation : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.obligation
deriving Repr, DecidableEq

structure EulerMaruyamaContract where
  id : String
  updateFormula : String
  interpolationFormula : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.contractOnly
deriving Repr, DecidableEq

structure DiscretizationErrorContract where
  id : String
  localDefect : String
  boundShape : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.obligation
deriving Repr, DecidableEq

end AutoSamplingTheory
