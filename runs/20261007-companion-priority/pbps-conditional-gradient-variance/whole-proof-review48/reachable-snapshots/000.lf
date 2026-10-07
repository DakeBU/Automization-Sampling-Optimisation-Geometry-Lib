import Std

/-!
# Core workflow and proof-obligation vocabulary

This module is intentionally conservative.  It gives the automation system a
compiled language for papers, source anchors, theorem contracts, and explicit
proof obligations.  Mathematical analysis that is not yet formalized must be
stored here as data, not closed by fake proofs.
-/

namespace AutoSamplingTheory

inductive ArtifactLanguage where
  | lean
  | latex
  | markdown
  | json
  | csv
deriving Repr, DecidableEq

inductive ProofStatus where
  | planned
  | sourceCited
  | contractOnly
  | obligation
  | formalized
  | blocked
deriving Repr, DecidableEq

inductive SourceKind where
  | paper
  | localTex
  | externalLean
  | mathlib
  | citedResult
  | experimentNote
deriving Repr, DecidableEq

/-- Stable pointer to the source of a mathematical claim. -/
structure SourceAnchor where
  key : String
  kind : SourceKind
  pathOrUrl : String
  label : String
  note : String
deriving Repr, DecidableEq

/-- An honest record for content that is not yet proved in Lean. -/
structure ProofObligation where
  id : String
  statement : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.obligation
  dependsOn : List String := []
  note : String := ""
deriving Repr, DecidableEq

/-- Paper theorem or lemma translated into a Lean-facing contract. -/
structure TheoremContract where
  id : String
  title : String
  mode : String
  source : SourceAnchor
  targetLean : String
  statementSummary : String
  proofStatus : ProofStatus := ProofStatus.contractOnly
  obligations : List ProofObligation := []
deriving Repr, DecidableEq

/-- A reusable proof-DAG block, usually one node in a paper proof. -/
structure ProofDagBlock where
  id : String
  interface : String
  source : SourceAnchor
  targetLean : String
  dependsOn : List String := []
  reusedBy : List String := []
  status : ProofStatus := ProofStatus.planned
deriving Repr, DecidableEq

/-- Patterns that are not allowed to close mathematical content. -/
def forbiddenProofPatterns : List String :=
  ["sorry", "admit", "axiom", "Prop := True", ":= trivial"]

def sourceAnchor (key kind pathOrUrl label note : String) : SourceAnchor where
  key := key
  kind :=
    match kind with
    | "paper" => SourceKind.paper
    | "localTex" => SourceKind.localTex
    | "externalLean" => SourceKind.externalLean
    | "mathlib" => SourceKind.mathlib
    | "citedResult" => SourceKind.citedResult
    | _ => SourceKind.experimentNote
  pathOrUrl := pathOrUrl
  label := label
  note := note

def localTexAnchor (key path label note : String) : SourceAnchor :=
  sourceAnchor key "localTex" path label note

end AutoSamplingTheory
