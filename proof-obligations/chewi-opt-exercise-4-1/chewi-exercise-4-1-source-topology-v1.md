# Source-only preproduction packet: Chewi Optimization Exercise 4.1

Status: proposal for independent source review, not a Statement Seal, verified
publication, Lean implementation graph, or admitted benchmark question.

- Primary: Sinho Chewi, *Lectures on Optimization*, arXiv:2605.07006v1,
  §4.2, Exercise 4.1, [printed/PDF p. 28](https://arxiv.org/pdf/2605.07006v1#page=28).
  Definition 4.3 and Theorem 4.4 are on p. 26; the path construction and the
  relevant proof steps are on pp. 27–28.
- Edition fingerprint already pinned in Bench's `chewi-optimization-v1` book
  record: 149 PDF pages; SHA-256
  `9e28afeacb0121b79691fadc6af9c145ccd787bffd2cf9c3f2310806112e644b`.
  This packet uses original restatement and bibliographic anchors only.
- Interface proposal: [type-only Lean](chewi-exercise-4-1-statement-v1.lean),
  file SHA-256 `fb2caaac44657e3e3f6c232d3c568989548f6108baa070a4b2e12f5746e2a1aa`.
  Lean variable `d` is one below the source dimension; write `D=d+1`.
  `Fin` is zero-indexed, so source coordinate `k` has Lean index `k-1`.
  `castSucc` and `succ` embed adjacent indices into the next larger `Fin`.
  `WithLp.toLp 2` installs the Euclidean norm without changing coordinates.

## Statement and binder proposal

For every integer dimension D and iteration count N with 1 ≤ N and 2N+1 ≤ D,
every β > 0 and start x₀ in Euclidean D-space, use the source's translated path
quadratic. In coordinates v = y−x₀ its value is β/4 times
half of [v₁² + sum of adjacent squared differences + v_D²], minus βv₁/4.
The chosen minimizer is x₀ plus the vector with coordinate 1−k/(D+1).
The candidate interface exposes convexity, differentiability and the global
β quadratic upper model, and verifies that this point minimizes the function.
Every trajectory with x(0)=x₀ and x(n+1)−x₀ in the real linear span of the first
n+1 actual gradients satisfies squared distance at time N at least one eighth
of its initial squared distance to that point.

- SOURCE: N bounds, positive β, arbitrary prescribed x₀, actual trajectory
  start, exact affine gradient-span condition.
- TYPING: finite real Euclidean coordinates and natural iteration/indices.
- No extra smoothness, convexity, tail, or source witness assumption:
  these are conclusions or internal proof ingredients. Differentiability
  certifies that the gradients are genuine rather than totalized defaults.
- Proposed exact constant 1/8 is an explicit universal realization of
  the exercise's comparison, not a claim about the sharp constant.
- Literal formulas: the objective and chosen minimizer are expanded `let`
  expressions, not chosen abstractly from an existence assertion.

## Source-only topology

| ID | Disposition and source location |
| --- | --- |
| M | NODE: §4.2 Definition 4.3, exact affine gradient-span model. |
| D | NODE: Theorem 4.4, dimension, iteration, smoothness constant and initial-point setting inherited by Exercise 4.1. |
| T | NODE: first sentence of Theorem 4.4 proof, translate the start to zero. The details of transporting the gradient-span condition and distances are SOURCE_GAP T1. |
| F | NODE: Theorem 4.4 proof, finite tridiagonal/path quadratic formula at n=D. |
| H | NODE: Hessian quadratic-form display, nonnegativity and upper bound by β times squared norm, supplying convexity and smoothness. |
| V | NODE: prefix subspaces V_n, their nesting and zero-start membership. |
| G | NODE: coordinate gradient display gives one-step support expansion. |
| I | NODE: use the affine span rule after translation and induct to obtain V_N membership. |
| P | NODE: solve the stationary tridiagonal system and read its affine-profile minimizer. Existence follows also from convexity and a vanishing gradient; no uniqueness assumption is needed for this exercise. |
| X | NODE: Exercise 4.1 requests the distance comparison using that same witness. |
| X1 | SOURCE_GAP: the exercise gives no solution; bound the distance by the untouched tail of the affine minimizer and compare with its entire squared norm under D ≥ 2N+1. |

Consumer-site edges: M and T meet at I; F feeds H, G and P; H justifies class
membership and the stationary minimizer interpretation at P; V and G feed I;
D, I and P feed the tail calculation X1, which with T1 and class membership
establishes X. The source chooses a witness before considering an arbitrary
trajectory; there is no dependence of F on a returned transcript.

Excluded: all results of §4.1 and Theorem 4.5; the restriction f_N=f_D on V_N,
exact minimal values and N⁻² function-value error estimate in the latter part
of Theorem 4.4's proof (not needed for the requested squared distance);
acceleration commentary and Exercise 4.2. No unrestricted deterministic or
randomized oracle lower bound. Do not attribute the tail constant or an
alternative source-gap proof to the author.

## Independent review request

Review this exact packet and type-only statement against the pinned source,
without reading any implementation Lean, prior review, or informal proof
scratch. Check the exact inherited quantifiers and algorithm model, all
coefficients/boundary conventions, minimizer selection, same-witness condition,
scope of omitted source paragraphs, and source-use edges. Return any repair
requests, concrete missing regions or false dependency edges. Acceptance here
is only source topology and prospective interface, never a Lean or QA verdict.
