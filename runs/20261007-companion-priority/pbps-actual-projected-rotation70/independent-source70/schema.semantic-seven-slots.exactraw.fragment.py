SEMANTIC_SLOTS = (
    "objects",
    "domains",
    "quantifiers",
    "assumptions",
    "conclusion",
    "scopes",
    "constant_dependencies",
)
SLOT_RELATIONS = {
    "same",
    "equivalent",
    "explicit-elaboration",
    "stronger-in-lean",
    "weaker-in-lean",
    "missing-from-lean",
    "missing-from-source",
    "different",
    "not-audited",
}
VERDICTS = {
    "pending",
    "exact",
    "equivalent-after-elaboration",
    "implicit-assumption-exposed",
    "lean-strengthened-assumptions",
    "lean-weakened-conclusion",
    "domain-mismatch",
    "quantifier-mismatch",
    "source-underspecified",
    "possible-source-error",
}
AUDIT_STATES = {
    "draft",
    "blind-reconstructed",
    "semantic-diffed",
    "source-reviewed",
    "accepted",
    "rejected",
}
REVIEW_STATES = {"pending", "accepted", "needs-revision", "rejected"}
REPAIR_CLASSES = {
    "micro-correction",
    "assumption-addition",
    "domain-clarification",
