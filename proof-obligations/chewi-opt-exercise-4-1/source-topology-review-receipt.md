# Independent prospective source-topology review receipt

Coordinator's transcription of the independent source-topology review by
exercise_41_source_topology_4d. This is not a compile, semantic-roundtrip,
or Bench editorial verdict.

- The reviewer rejected revision 1's missing C¹ convention, the missing
  dependency from the prefix space into the coordinate-gradient computation,
  and the missing dependency from translated gradients into the zero-start
  induction. The first packet and type probe are retained unchanged.
- The reviewer accepted revision 2, SHA-256
  24836c3fe2d07d00096c437bdb78adfa836162c69ca305717a9b443c172af70d,
  its type-probe text SHA-256
  e63d11ff7cfbeda444a69fde27726fe40a9c3f140dfddaacb45cc80bc38dd513,
  and the independently fetched primary PDF SHA-256
  9e28afeacb0121b79691fadc6af9c145ccd787bffd2cf9c3f2310806112e644b.
  Continuous differentiability and the global upper model match Definition
  1.12. The exact witness, quantifier order, two boundary values and
  deterministic run-level gradient-span scope were confirmed.
- The standalone revision 2 type probe failed on a missing Mathlib import.
  The subsequent exact signature probe restores the import, inlines the
  local aliases, and passes without changing the mathematical scope.
  See the [Statement Seal](chewi-exercise-4-1-statement-seal-v1.md).

The later independent semantic and compiler review is recorded under
runs/20261112-chewi-opt-exercise-4-1. It independently checked the actual
compiled theorem; this prospective receipt cannot substitute for it.
