# Source-only preproduction packet: Optimization Exercise 4.1, revision 2

Status: proposal, not a Statement Seal, publication review, or admitted QA.
Primary source: Sinho Chewi, *Lectures on Optimization*, arXiv:2605.07006v1,
149 pages, PDF SHA-256
9e28afeacb0121b79691fadc6af9c145ccd787bffd2cf9c3f2310806112e644b.
This packet restates the mathematics in original language.
Source and printed/PDF page agree for all anchors below.

## Exact interface for review

[Type-only Lean](chewi-exercise-4-1-statement-v2.lean), SHA-256
e63d11ff7cfbeda444a69fde27726fe40a9c3f140dfddaacb45cc80bc38dd513.
Here D = d+1; the source's coordinate k has Lean index k−1. WithLp.toLp 2
preserves the entries and uses the Euclidean norm. Quantifier order:
every dimension D and iteration N with 1 ≤ N, 2N+1 ≤ D; every positive
β and prescribed x₀; then the literal translated quadratic and its affine
minimizer (both fixed independently of any run); finally every sequence
starting at x₀ with x(n+1)−x₀ in the real span of the actual gradients at
x(0), …, x(n). The output verifies convexity, C¹, minimization, the global
β upper model of Definition 1.12, and the distance comparison
‖x(N)−x★‖² ≥ (1/8)‖x₀−x★‖² for that same witness.

The run-level quantification expresses the span restriction on each
deterministic run of Definition 4.3; it does not claim a randomized-oracle
lower bound. C¹ is proved from the quadratic, not assumed. The explicit
1/8 is a valid universal exercise-gap constant, not source-attributed or sharp.

## Independent source proof topology

| ID | Source anchor and role |
| --- | --- |
| M | NODE: [p. 26](https://arxiv.org/pdf/2605.07006v1#page=26), Def. 4.3, deterministic affine-gradient-span algorithm model. |
| D | NODE: p. 26, Thm. 4.4 setting; fixes dimension, iteration, β and prescribed start for the exercise. |
| T | NODE: [p. 27](https://arxiv.org/pdf/2605.07006v1#page=27), translate the start to zero. |
| T1 | SOURCE_GAP: translation preserves the genuine gradients (identity derivative), their affine spans, minimizer, upper model and distances. This is a proof obligation, not a caller premise. |
| F | NODE: p. 27, tridiagonal/path quadratic with witness dimension n=D. |
| H | NODE: p. 27, Hessian form; sums of squares and the two appearances of each coordinate give the two-sided Hessian bound. Convexity uses [Prop. 1.6, p. 8](https://arxiv.org/pdf/2605.07006v1#page=8), α=0; smoothness uses [Def. 1.12 (1.7) and Prop. 1.13, p. 11](https://arxiv.org/pdf/2605.07006v1#page=11). Prop. 1.13's proof is omitted in the source. C¹ follows from the explicit polynomial. An exact quadratic remainder is an alternative way to justify the upper model. |
| V | NODE: p. 27, nested prefix spaces V_r and zero-start membership. |
| G | NODE: p. 27, at a point in V_r the coordinate gradient shows membership in V_(r+1). Use r<D; at step n<N, r≤N−1. At the right edge the padded value is zero. |
| I | NODE: p. 27, apply the affine-span rule after centering, and induct to obtain V_N. |
| P | NODE: [pp. 27–28](https://arxiv.org/pdf/2605.07006v1#page=27), solve the stationary tridiagonal system and get the affine profile. Convexity and the zero gradient certify minimization via [Lemma 1.9, p. 10](https://arxiv.org/pdf/2605.07006v1#page=10); no uniqueness premise. The exact edge-energy difference also suffices. |
| X | NODE: [p. 28](https://arxiv.org/pdf/2605.07006v1#page=28), Exercise 4.1 asks for the squared-distance comparison using the same witness. |
| X1 | SOURCE_GAP: untouched tail, reindexed from the last coordinate, gives the fraction S(D−N)/S(D) of the initial squared norm, where S(r)=sum of j² for 1≤j≤r. Bound it below by 1/8 since D≤2(D−N); never assume the needed tail estimate. |

Consumer edges: T and F feed T1; F feeds H, G and P; V feeds G
(the formula is evaluated on prefix-supported input), and both V and G
feed I. M and T1 feed I: translation of the span rule precedes
zero-start induction. H feeds P's stationary-point interpretation.
D, I and P feed X1. H, P, T1 and X1 feed X. D fixes the dimension of F
before any iterates are considered. These are mathematical source edges,
not claims about a compiled Lean dependency graph.

Excluded: §4.1, Thm. 4.5, Exercise 4.2, restrictions between path objectives
in different dimensions, exact minimal values, the auxiliary upper bound
on the initial distance, the choice D asymptotic to N, and the N⁻²
function-value lower bound. No unrestricted or randomized oracle model.

Review independently from the primary source and this exact type-only packet.
Do not read prototype code or earlier decisions. Accept or identify concrete
source/typing/scope/graph gaps; the verdict is not a proof or QA admission.
