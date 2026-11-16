import AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereInducedPathDistance
open Lean Meta Elab Command
set_option format.width 120
set_option pp.fullNames true
set_option pp.universes false
set_option pp.proofs true
run_elab do
  let ci ← getConstInfo ``AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereInducedPathDistance.unit_sphere_induced_riemannianEDist_eq_arccos
  forallTelescope ci.type fun _ body => do
    let body ← whnf body
    let lhs := body.getAppArgs[1]!
    unless lhs.getAppFn.constName? == some ``Manifold.riemannianEDist do
      throwError "Unexpected proposition structure"
    for arg in lhs.getAppArgs, i in List.range lhs.getAppArgs.size do
      logInfo m!"ARG_{i}\nTYPE: {← inferType arg}\nVALUE: {arg}"
