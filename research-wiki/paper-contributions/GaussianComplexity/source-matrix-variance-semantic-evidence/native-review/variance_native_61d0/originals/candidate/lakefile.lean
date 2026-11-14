import Lake
open Lake DSL

package auto_sampling_theory where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.33.0"

@[default_target]
lean_lib AutoSamplingTheory

lean_lib Tests
