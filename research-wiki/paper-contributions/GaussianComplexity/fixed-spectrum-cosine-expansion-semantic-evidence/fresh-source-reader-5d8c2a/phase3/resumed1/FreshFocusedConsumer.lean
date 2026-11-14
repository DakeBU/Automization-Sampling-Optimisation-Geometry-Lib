import Tests.GaussianComplexityFixedSpectrumCosineExpansion
import Lean

open Lean Elab Command

partial def outerRefs (e : Expr) (ctx : List Name) (depth : Nat := 0)
    (s : Std.HashSet Name := {}) : Std.HashSet Name :=
  match e with
  | .bvar i => if depth ≤ i then match ctx[i-depth]? with
      | some n => s.insert n
      | none => s
    else s
  | .app f a => outerRefs a ctx depth (outerRefs f ctx depth s)
  | .lam _ t b _ | .forallE _ t b _ => outerRefs b ctx (depth+1) (outerRefs t ctx depth s)
  | .letE _ t v b _ => outerRefs b ctx (depth+1) (outerRefs v ctx depth (outerRefs t ctx depth s))
  | .mdata _ b | .proj _ _ b => outerRefs b ctx depth s
  | _ => s

partial def auditLets (e : Expr) (ctx : List Name := []) : CommandElabM Unit := do
  match e with
  | .letE n _ v b _ =>
    if ["hs", "hsg", "hlin", "heigen", "hscalar", "hexchange", "hfactor"].contains n.toString then
      logInfo m!"COMPILED_LOCAL_DEPENDENCIES {n}: {(outerRefs v ctx).toList}"
      if n.toString == "hexchange" then
        logInfo m!"EXCHANGE_VALUE_APP_HEAD {v.getAppFn}"
    auditLets v ctx
    auditLets b (n::ctx)
  | .lam n _ b _ | .forallE n _ b _ => auditLets b (n::ctx)
  | .app f a => auditLets f ctx; auditLets a ctx
  | .mdata _ b | .proj _ _ b => auditLets b ctx
  | _ => pure ()

run_cmd do
  let env ← getEnv
  let targets := env.constants.toList.filter fun (n, _) =>
    n.toString.startsWith "_private.Tests.GaussianComplexityFixedSpectrumCosineExpansion." &&
    n.toString.endsWith ".actual_inverse_grid_cosine_series"
  unless targets.length == 1 do throwError "Consumer count mismatch"
  for (_, ci) in targets do
    let .thmInfo ti := ci | throwError "Consumer not a theorem"
    auditLets ti.value
