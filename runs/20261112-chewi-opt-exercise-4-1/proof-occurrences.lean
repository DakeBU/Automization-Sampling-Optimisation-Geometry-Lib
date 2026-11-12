import AutoSamplingTheory.ExampleCases.LowerBounds.GradientSpanDistance

/- Exact owner-local proof-body occurrence audit. This does not prove mathematical necessity,
   statement-level implication, or a complete transitive dependency closure. -/
open Lean in
run_cmd do
  let env ← getEnv
  let root := `AutoSamplingTheory.ExampleCases.LowerBounds.GradientSpanDistance.exercise_4_1
  let pref := "_private.AutoSamplingTheory.ExampleCases.LowerBounds.GradientSpanDistance."
  let mut queue := #[root]
  let mut idx := 0
  let mut shared : Std.HashSet Name := {}
  for _ in [:128] do
    if idx ≥ queue.size then break
    let n := queue[idx]!
    idx := idx + 1
    let some info := env.find? n | throwError "Missing proof body node"
    let some body := info.value? (allowOpaque := true) | continue
    for k in body.getUsedConstants do
      let s := k.toString
      if s.startsWith pref then
        if !queue.contains k then queue := queue.push k
      else if s.startsWith "AutoSamplingTheory." then
        shared := shared.insert k
  if idx < queue.size then throwError "Local proof trace budget exhausted"
  logInfo m!"Local exact proof-body traversal: {idx} owner constants"
  for n in shared.toArray do
    logInfo m!"Shared proof-body occurrence: {n}"
