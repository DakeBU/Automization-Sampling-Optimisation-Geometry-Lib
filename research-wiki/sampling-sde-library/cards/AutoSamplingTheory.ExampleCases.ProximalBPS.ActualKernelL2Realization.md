# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualKernelL2Realization

- File: `AutoSamplingTheory/ExampleCases/ProximalBPS/ActualKernelL2Realization.lean`
- Layer: route-local integration node
- Purpose: Identify the SAME actual phase process, probability-kernel fibers and arbitrary real-L2 observable evolution; derive invariant state fibers, AE positivity and fixed constant classes.
- Mathlib-quality status: Independently source/compiler verified; serialized integration and purification are separate gates.
- Verification: [exact source, tests, seven-slot audit and current integration](../../paper-contributions/PBPS/kernel-l2-realization-verification.json).

## Imports

- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2StrongContinuity`
- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel`
- `Mathlib.Probability.Kernel.Invariance`

## Representative Declarations And Exports

- `actual_kernel_l2_realization_statement` (private complete statement, not a separate leaf)
- `actual_kernel_l2_realization`

## Curated Formalized Memory Entries

- `pbps.actualKernelL2Realization` -> `actual_kernel_l2_realization` (arXiv2609.06905v1 A.1 and D.2, fixed-time observable realization only)

## Boundaries and Consumers

Future actual kernel/operator composition may consume this same-witness bridge.
No existing downstream Lean consumer is invented. Probability fibers do not
prove a process Markov property or a restart/semigroup law. Positivity here is
AE preservation of nonnegative observables, not positive-semidefiniteness of
the operator. Adjoint density evolution, independent-reference half-turn,
hypocoercivity, simulation errors and actual-input costs remain separate.
