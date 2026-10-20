# Candidate Populations

Exploratory proof routes and candidate decompositions for active research
targets such as PRIVATE.

This directory is the ASTIS adaptation of the EoH-style population idea:
initialize candidate routes, vary them, evaluate them against an explicit
acceptance predicate, select useful survivors, and archive rejected directions.

Rules:

- Use candidate populations only in `exploratoryProof` mode or for proof
  attempts around a fixed lemma.
- Do not use mutation/crossover to change a `faithfulPaper` theorem,
  assumption, constant, or source proof target.
- Candidate scores are search guidance only.  Acceptance still requires
  compiled Lean plus explicit source correspondence, or the candidate remains a
  proof obligation.
