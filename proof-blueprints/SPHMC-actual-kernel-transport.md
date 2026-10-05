# SPHMC actual Gaussian numerical kernel transport

One SAU: ASTIS-SA-20261006-SPHMCActualKernelTransport. Shared cell ASTIS-SHARED-randomized-map-transport exists before the actual consumer cell ASTIS-SW-SPHMC-actual-kernel-transport advances. Root is sole Lean writer, original sole stabilization lane/PR313.

Primary arXiv:2609.06906v1 Proposition4.7 (4.13), Theorem4.5 proof HTML529-545/590-615. Shared prerequisite is raw Kantorovich measure theory, not a separately numbered source theorem. Current pinned Lean4.33.0 / Mathlib db584cd6d46c92f209a44c0f1c829460d327499d.

Shared floor searched: Samplinglib Measure/Transport and CommonNoiseContraction; actual FirstOrderDifference/ActualContraction and source Q; Mathlib map/product/lintegral/kernel composition and ENNReal scaled infimum. Existing invariant_map_comap is invariance, not transport contraction. No CommonNoiseContraction module card was present; existing KernelTransport card and technical-lemma README checked. Reuse public joint-noise marginal theorems unchanged, no private copies. Shared lifting has actual SPHMC consumer and planned Chewi nonlinear common-noise sampling updates.

Reusable leaf contract: RandomizedMapTransport.transportCost_randomized_map_le, normed Borel group E, second-countable, measurable Phi and extended cost, all three laws probability, finite nonzero A. No optimizer/finite moments. State/noise same space is API boundary. Actual consumer discharges its pointwise premise for full numerical Phi. Minimal new shared import CommonNoiseContraction; route imports actual contraction and kernel measure composition.

Route in five steps: (1) real S#(gamma×Gamma), with public marginal rewrites; (2) measurable nonnegative integral cost and noise mass1; (3) positive finite multiplier commutes with raw infimum, including infinite cost; (4) actual Phi measurability/Markov K and integrated product-pushforward law; (5) actual source sqrtQ contraction squared with delta>0, then shared lifting.

Failure policy: after repeated same-shape failures diagnose mathematical statement/API/measure representatives; never add moment/invariance/optimizer premises merely to compile. First shared attempt failed only because rw selected LHS transport infimum; conv_rhs corrected the target, no statement change. First actual attempt had doc-comment/set_option syntax and wrong ofReal API spelling; direct positive-factor lemma fixed them, no mathematical change. Raw attempts retained.

Focused3717 PASS; genuine nonconstant f(x)=3x²/8+sin(x)/8 exercises full actual Markov law and transport for every probability input. Production/shared declarations standard propext/Classical.choice/Quot.sound only. Full independent proof/anonymous decoder/anti-anchored source/exact committed verification and serial aggregate remain separate.

Conceptual-mirror audit none-found: same-space probabilistic lifting, no cross-domain metric/energy transport. Existing mirrors/frontiers/cycles/source inventories preserved. No abstract supplied-kernel consumer, max-norm substitution, TV-to-unbounded-cost transfer or full-paper claim.

Actual Gaussian exact-gradient numerical K at the explicit normalized global C2 curvature interface. Actual f=V_eta smoothing/C2/curvature remains separate. No target invariance/stationarity, numerical target bias, stochastic Khat/Kbar, local errors/history/expected query cost, Wp/proxy-warmness/initialization, PBPS or either complete main/composition result. TV proximity does not transfer unbounded cost.
