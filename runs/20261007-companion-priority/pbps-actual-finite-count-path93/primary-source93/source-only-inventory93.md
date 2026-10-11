# Independent primary-first inventory: bounded finite-count complete history/path ingredient

Reviewer: primary_source93. This artifact was written before reading production Lean, authored lessons, decoder output, prior semantic decisions, repair verdicts, or the proposed source graph. It is a source-only scope inventory, not source acceptance.

Primary pin: runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html. SHA-256 d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760 verified from bytes. Header lines 258-281 identifies arXiv:2609.06905v1, 7 September 2026, Accelerated High-Accuracy Sampling from a Warm Start via the Proximal Bouncy Particle Sampler; Fan Chen, Sinho Chewi, Jianfeng Lu, Matthew S. Zhang. License field says arXiv.org perpetual non-exclusive license. This is evidence of the snapshot's declared version, attribution and license, not an independent authenticity check of arXiv. It does not license ASTIS to reproduce the complete paper. The following is reviewer-authored mathematical paraphrase.

## Objects and quantifiers independently recovered

The source setting is finite-dimensional Euclidean position and momentum, V in C2 with 0 < alpha <= beta and Hessian between alpha I and beta I (Introduction); Section 2.2 selects 0 < eta <= 1/beta. Fix y and reference xref, and an arbitrary deterministic initial pair z0=(x0,p0). For the bounded ingredient take n any natural number and a finite nonnegative observation horizon t. Source A.7 covers bounded measurable path functionals; a measure identity restricted to the exactly-n event is an equivalent finite-count formulation once the measurable path carrier is stated. The local construction only uses eta>0 and continuity/Lipschitz control of the gradient; omitting convexity or the upper bound on eta can be a documented local generalization, never an assertion that the whole paper drops them.

c=y-eta grad V(xref); h(x)=grad V(x)-grad V(xref); lambda(x,p)=sqrt(eta) max(p dot h(x),0). Phi is the explicit harmonic rotation about c, with position coefficient sqrt(eta) and momentum coefficient -1/sqrt(eta). S(x,p)=(x,R_h(x) p), with R_h the orthogonal reflection for h nonzero and R_0=I. This zero-normal convention is meaningful and permits a Borel but potentially discontinuous bounce map.

Independent unit-rate exponential E_1,E_2,... drive the integrated-hazard threshold infimum A.1, initially T_0=0. Each finite wait is added to the previous time and followed by flow then reflection (A.2); an empty hitting set means infinite wait and termination. Within an inter-event interval [T_j,T_{j+1}), the path is the harmonic flow from the post-jump state at T_j. Thus values at event times are post-jump values; factors in A.7 instead use pre-jump values. A finite-clock realization and any off-domain default values need to agree with this construction on their stated legal support.

Ordered prescribed histories lie in Delta_n(t)={0<t1<...<tn<t}; Delta_0 is the single empty history. Prescribed paths follow Phi and apply S at those times. The exactly-n complete-history law includes survival from tn to the observation endpoint t. A law of n ordered arrivals alone omits this last factor and is not this bounded complete-history ingredient. The finite product needs n+1 independent clocks: n to produce the arrivals and one for no next event by t. Dependence on later clocks must disappear from this event/path.

For a fixed legal prescribed history, the density contribution is the exponential of minus the whole-path integrated rate, multiplied by every pre-jump rate. The complete-path statement evaluates a measurable functional on the entire restriction to [0,t], not only at t. A coordinate-cylinder formulation is an ASTIS carrier choice and must be identified as such; its promotion to stronger path sigma-algebras needs a separate bridge.

## Required source regions and proof dependencies

1. (2.4), (3.4), (3.8), (3.9), and A.1 lines 2860-2887: exact reflection convention, center, residual force, flow and rate; prerequisites of every history/path definition.
2. A.1 lines 2889-2911, equations (A.1)-(A.2): independent clocks, hitting time, recursion, termination and between-event state. These supply the actual-input law rather than an assumed ordered-history density.
3. A.1 lines 2914-2972: preserved shifted harmonic energy gives a finite pathwise rate bound; finite waits dominate independent exponentials divided by that bound; zero bound gives no jumps; SLLN yields non-explosion. These are parent dependencies when connecting to the infinite process, not fresh premises of a finite-count theorem. Davis 1984 Section 2 is cited for the integrated-hazard construction. This review will not re-audit unchanged parent proofs.
4. A.1 lines 3148-3159: ordered simplex and prescribed path definition. These dictate strict arrival order and the post-/pre-jump distinction.
5. A.7 lines 3159-3169: iteration of clocks yields the path integral over every fixed finite-count sector. Finite arrival-law induction and terminal survival are substantive dependencies even though the source compresses them to a sentence.
6. A.7 lines 3171-3173: simplex volume and uniform pathwise rate bound give absolute convergence of the sum. This is required for full A.7 but excluded from this finite-count result unless explicitly proved separately.
7. A.2 lines 3327-3335: joint Borel flow, rate and bounce; Borel integrated hazard continuous and nondecreasing in time; rational threshold criterion; Borel jump times and post-jump states. These justify, rather than assume, measurability of the recursion.
8. A.2 lines 3336-3339: truncations converge almost surely to the terminal state by non-explosion, with zero on the exceptional undefined-limit set. This supports infinite-process terminal measurability, outside the finite-count identity itself.
9. A.2 lines 3342-3364: integrate the jointly Borel conditional reference density with momentum and clock laws; then conditional reversibility, Fubini and L2 density give the augmented operator. This is a downstream consumer, not established by the bounded ingredient.

## Explicit ASTIS mathematical completions

A.1/A.7 do not explicitly name an exactly-n finite-clock event. Its measurable predicate, use of n+1 clock coordinates, independent tail integration, and the equality between the finite recursion and the complete-history law are ASTIS expansions of source bookkeeping, not direct source quotations.

Endpoint conventions must be proved: E_j>0 almost surely excludes zero waits; strict t_j<t and no next jump by t distinguish open/closed events; equality of an exponential clock with a fixed integrated hazard has probability zero conditionally on its preceding history. A continuous nondecreasing hazard need not be strictly increasing or unbounded; threshold-infimum reasoning must allow plateaus and an infinite wait. An unproved strict-monotonicity or finite-wait assumption is excess. t=0 and n=0 need their actual empty-history/no-event semantics.

The graph of elapsed time and post-jump state at each finite step, the measurable finite tuple map, finite recursion coherence when one clock is appended, and survival-event disintegration are ASTIS completions. They may be proved from source inputs/parents; they must not become theorem-shaped hypotheses on a public actual-input statement.

The piecewise path evaluation map is jointly Borel in finite history and fixed observation coordinate, with the correct post-jump choice at equality. A Pi/coordinate measurable path carrier, measurable pushforward, and agreement of random and prescribed paths on the exactly-n event are ASTIS completions. Path equality must cover every coordinate in the intended [0,t] restriction; unconstrained real-time values are an extension convention, not additional source content. Equality of terminal pushforwards alone cannot discharge a path-valued claim.

Multiplying arc survivals into exp(-integral_0^t lambda) requires finite additivity/change of variables of integrals and endpoint-nullness. The bound needed for density/finite integrability comes from preserved energy, not a new source binder.

## Exclusions and acceptance boundary

Excluded from this bounded ingredient: countable summation over n/full bounded-functional A.7; total probability normalization via non-explosion; construction/uniqueness/Markov property of the infinite PDMP; path-reversal change of variables and rate balance (A.3)-(A.6),(A.8); invariant measure, semigroup strong continuity and L2 operator identities; averaging over Gaussian momentum/reference laws; full A.2 joint half-turn kernel and augmented operator; bounce complexity, caps and query cost; PBPS/SPHMC composition and complete paper results. These remain visible downstream boundaries even if the finite-count identity is accepted.

Final review must independently compare objects, domains, quantifiers, assumptions, conclusion, scopes/senses, and constant dependencies in a fresh canonical anti-anchored reviewer packet with completed blind reconstruction. Acceptance must bind exact packet, whole production module, publication context and authored proof regions. This inventory grants none of those later approvals.
