import AutoSamplingTheory.TechnicalLemmas.Probability.RandomScanHeatBathReversibility

/-!
Trusted operator-only probe: independently of the selected public graph,
follow the private balance theorem actually referenced by the compiled
reversibility proof. Do not put the private node into the public task slice.
-/

open Lean in
run_cmd do
  let env ← getEnv
  let reversible :=
    `AutoSamplingTheory.TechnicalLemmas.Probability.RandomScanHeatBath.randomScan_isReversible
  let pointwise :=
    `AutoSamplingTheory.TechnicalLemmas.Probability.RandomScanHeatBath.randomScan_apply_singleton
  let sourceName :=
    `AutoSamplingTheory.TechnicalLemmas.Probability.RandomScanHeatBath.singleton_balance
  let some proof := (env.find? reversible).bind (fun info => info.value? (allowOpaque := true))
    | throwError "Missing compiled reversibility proof"
  let direct := proof.getUsedConstants
  if direct.contains pointwise then
    throwError "Pointwise formula now occurs directly; the old boundary example is stale"
  let candidates := direct.filter fun name => privateToUserName? name == some sourceName
  unless candidates.size == 1 do
    throwError "Expected one actual private singleton-balance constant"
  let balance := candidates[0]!
  let some (.thmInfo info) := env.find? balance
    | throwError "Private balance constant is not an imported theorem"
  unless info.value.getUsedConstants.contains pointwise do
    throwError "Private balance proof no longer calls the pointwise law"
  let rows := Json.mkObj [
    ("public_target", toJson reversible.toString),
    ("private_bridge", toJson balance.toString),
    ("bridge_source_name", toJson sourceName.toString),
    ("pointwise_law", toJson pointwise.toString),
    ("pointwise_occurs_directly_in_public_target", toJson false)]
  logInfo m!"SOG_RANDOM_SCAN_PRIVATE_V1 {rows.compress}"
