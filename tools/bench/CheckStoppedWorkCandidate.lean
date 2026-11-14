import Lean

open Lean

/-- Inspect only the two locally generated, repository-controlled modules.
The required Linux run separately compares and kernel-checks the solution. -/
def main : IO Unit := do
  initSearchPath (← findSysroot)
  let challenge ← importModules #[{ module := `Challenge }] {}
  let solution ← importModules #[{ module := `Solution }] {}
  let candidateNamespace := "SamplingOptimisationGeometryBench."
  let model := [
    candidateNamespace ++ "ConditionalBudgetTransfer.historyFiltration",
    candidateNamespace ++ "AveragedBudget.bitMass",
    candidateNamespace ++ "PaddedCounterexample.paddedTable",
    candidateNamespace ++ "PaddedCounterexample.terminalCharge"]
    ++ (["Path", "History", "Table", "readPrefix", "historyFiltration",
      "cylinder", "mass", "Realizes", "Supports", "ratio", "likelihood",
      "chiSquare", "conditionalBudget", "budgetProcess"].map
        (fun name => candidateNamespace ++ "BinaryPrefixLikelihood." ++ name))
    ++ ["SogBenchCandidate.Positive", "SogBenchCandidate.Negative", "SogBenchCandidate.ProposedTarget"]
  for key in model do
    let n := key.toName
    let some c := challenge.find? n | throw (IO.userError s!"Missing challenge definition {n}")
    let some s := solution.find? n | throw (IO.userError s!"Missing reference definition {n}")
    unless c.type == s.type && c.value? == s.value? do
      throw (IO.userError s!"Challenge/reference expression drift at {n}")
  for key in [candidateNamespace ++ "BinaryPrefixLikelihood.binary_stopped_work_transfer",
              candidateNamespace ++ "PaddedCounterexample.binary_padded_averaged_budget_counterexample"] do
    if challenge.contains key.toName then
      throw (IO.userError s!"Answer leaked into challenge: {key}")
    unless solution.contains key.toName do
      throw (IO.userError s!"Reviewed answer missing from reference: {key}")
  let some c := challenge.find? `sogBenchTarget | throw (IO.userError "Missing challenge target")
  let some s := solution.find? `sogBenchTarget | throw (IO.userError "Missing reference target")
  unless c.type == s.type && c.type == mkConst `SogBenchCandidate.ProposedTarget do
    throw (IO.userError "Fixed conjunction target drift")
  IO.println s!"Matched {model.length} model/target definitions and the fixed theorem type."
