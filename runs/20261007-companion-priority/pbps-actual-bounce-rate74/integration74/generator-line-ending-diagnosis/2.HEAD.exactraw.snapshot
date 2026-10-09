# Mathlib-Ready Leaf Lemma Protocol

ASTIS treats every reusable SDE/Sampling background result as a possible future
Mathlib contribution.  The immediate rule is more modest: before a lemma is
called by a SALD or RMFLD proof, it must be an ASTIS-owned Lean declaration
that builds locally, or it must be recorded as an explicit proof obligation.

Reference target: https://mathlib-initiative.org/

## Core Rule

One lower-agent packet should target one small theorem.  The packet must fit in
one agent context window and must include more than the theorem statement:

- proposed declaration name and namespace;
- existing local APIs and Mathlib declarations to try first;
- minimal imports;
- hidden regularity contracts;
- intended proof route in at most seven steps;
- source anchor or upstream theorem reference;
- failure policy.

The lower agent should not repeatedly redesign the statement.  If the same
target fails two or three times for the same reason, treat that as a
mathematical signal: look for a missing assumption, a false statement, a
wrong representative, a typeclass mismatch, or a counterexample.

## Mathlib-Ready Shape

A leaf is Mathlib-ready when it has these properties.

| Check | Required behavior |
|---|---|
| Generality | State the reusable mathematical fact, not a SALD-specific wrapper. |
| Minimal assumptions | Expose only the regularity actually used by the proof. |
| Local API | Reuse existing Mathlib names before inventing ASTIS names. |
| Naming | Prefer descriptive names that would still make sense outside SALD. |
| Proof route | Keep one stable proof route unless reviewer identifies a real statement issue. |
| Import discipline | Use the smallest reasonable imports and avoid hidden project dependencies. |
| Callability | Status becomes callable only after `lake build` covers the declaration. |

SALD-specific theorem boundaries still belong in paper-contribution memory.
Only reusable facts such as law-map integrals, dominated derivative transfer,
conditional-kernel pairings, KL/FI algebra, weak Fokker--Planck statements,
Gaussian moments, Ito/Taylor remainders, and integration-by-parts identities
belong in technical lemma memory.

## Hidden Regularity Contracts

Paper prose often hides assumptions behind phrases such as "standard",
"smooth", "by Fokker--Planck", or "by integration by parts".  In Lean these
must be explicit contracts.  Common contracts include:

- measurability or `AEStronglyMeasurable`;
- integrability or domination for exchanging limits and integrals;
- finite measure, probability measure, sigma-finiteness, or nonempty space;
- continuity, differentiability, `ContDiff`, bounded Hessian, or compact
  support;
- positivity or nonzero density hypotheses for logarithms and KL terms;
- no-boundary, compact-support, or decay assumptions for integration by parts;
- a fixed conditional-distribution representative when conditional laws are
  used.

When a hidden regularity fact is needed in more than one proof, promote it to
`AutoSamplingTheory/TechnicalLemmas/*` and register it under
`research-wiki/technical-lemmas/`.

## Local Mathlib Search Discipline

Before writing a new technical lemma, middle and lower agents should search
the local Mathlib checkout and ASTIS memory:

```bash
rg -n "condDistrib|map.*integral|HasDerivAt|Kullback|Fisher|Gaussian" .lake/packages/mathlib/Mathlib AutoSamplingTheory
rg -n "theorem|lemma" AutoSamplingTheory/TechnicalLemmas research-wiki/technical-lemmas
```

If Mathlib already has the theorem, the ASTIS leaf should be a thin usage
proof or notation bridge.  If Mathlib has only nearby infrastructure, the
ASTIS leaf should be written in a way that could later be upstreamed.
