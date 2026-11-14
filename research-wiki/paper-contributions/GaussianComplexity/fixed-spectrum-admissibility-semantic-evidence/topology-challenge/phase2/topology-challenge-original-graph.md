# Independent coverage and topology challenge — original graph

Reviewer: `/root/fs_admiss_topology_challenge`. This is a distinct review of
the graph author's frozen source-only extraction, against my own raw-source
phase-1 reconstruction and the admitted exact precision signature. It does
not inspect a target proof, target API, Test, root audit, previous source
verdict, or graph-author private rationale.

Reviewed graph SHA-256:
`087371c7140770ca54fa99783977c47f5649627ebdd5811c3d129fed3f2e1055`.
Reviewed graph-author freeze SHA-256:
`b3b9107bc1d68aff6cfd596134f00a5e6256f455bdca3bbb95498ac19ef545de`.
Coverage SHA-256:
`35b6f8ef7bc110216db59e3503c3c5f0264c580ff4be088929eb3da0076e80a1`.
Matching SHA-256:
`7f9a94c01c06fc1b11fd60e622837f78032d40201ae86f032b98796856475b98`.

## Raw coverage and exclusions

I independently reparsed the pinned raw HTML using BeautifulSoup and rendered
math from its original `alttext`. All 146 coverage rows carrying source IDs
refer to actual raw elements and match their normalized raw text; every
declared text hash also matches. All 66 synthetic heading/caption/citation
rows match same-kind raw elements in their declared source subtree. The count
is 212 dispositions, 36 NODE and 176 EXCLUDED.

The full S1/S2/S4/C.4 paragraph/display inventory has no missing substantive
unit. The only table wrappers absent from the coverage IDs are `S4.EGx1` and
`S4.EGx2`, which contain no independent additional formula: their formula
contents are precisely the already inventoried `S4.Ex16` and
`S4.Ex18`/`S4.Ex19`, respectively. For this review those two group wrappers
are EXCLUDED as structural containers with all mathematical children covered.
This is not an exclusion of any mathematical assertion.

The exact local domain paragraph, Eq. (11), the actual rotated matrix and
target context, public-spectrum context, named lemma, order/group/class
definitions, the actual consumer paragraph `S4.SS3.p2.1`, all four C.4 proof
paragraphs, and `A3.Ex160` are represented. The three parts of C.4 are not
compressed into just the named sandwich conclusion: smoothness/Hessian and
curvature, the positive quadratic/unique minimizer, the actual Gaussian,
Gaussian integration, determinant substitution, and known normalizer all
survive as nodes or explicit background obligations.

The sibling Krylov representation, uniform cosine concentration, target
moments, lower-bound test/contradiction and limitations arguments do not feed
admissibility and are justifiably excluded from this bounded closure. The
source's [22] citation gives construction provenance and separate Krylov
background; C.4's elementary admissibility proof does not invoke a theorem
from it. Its exclusion as an external prerequisite is justified. TV details
are not needed to conclude pointwise matrix admissibility. Retaining the
uniform-accuracy definition and exact use site is sufficient to show the
consumer direction, without claiming the lower bound is proved.

Some source paragraphs contain several claims, so source-region selection
must remain granular. In particular the selected `rotated-precision` node
contains the literal matrix along with Haar/seed and Gaussian context. Its
selected-producer label does not mean the producer constructs a Haar
experiment or proves the target law. The explicit matching and truth
boundaries correctly keep those claims pending. The same care applies to the
mixed introductory/consumer paragraphs. Coverage labels alone are never
formal completion credit.

## Source-route topology

The graph has 34 nodes and 16 edges. Independent graph traversal finds no
dangling ID and no cycle. Tracing the named lemma backward reaches exactly
the local hard parameters, cosine grid, angle bounds, cosine bounds,
eigenvalue bounds, real orthogonal matrix/literal rotated precision and
conjugated bounds, together with four visible unproved internal bridges:
grid arithmetic, cosine background, affine envelope, and orthogonal
congruence. No calculus, Gaussian, normalizer, query, δ, ε, or concentration
parent is needed to infer the sandwich.

The source offers a single route for this lemma. Its AND-edges describe the
joint prerequisites of the same argument; no competing sufficient route has
been flattened into a false AND. The auxiliary analytic branches go outward
from the common matrix result and actual potential. The lower-bound
application edge points from admissibility/class membership to restriction
of the uniform guarantee, never backward. The SLC explanatory edge is
explicitly labeled compatibility explanation, so it does not infer a full
lower bound merely from potential regularity.

The source's compressed symmetry, norm preservation, diagonal
quadratic-form calculation, finite-square inverse identities and exact index
arithmetic remain internal obligations. The four selected SOURCE_GAP nodes
are not mathematical counterexamples, new source premises, or compiled
providers. κ≥2 supplies a positive affine scale, and the one-based source
coordinate is correctly matched to the zero-based half-grid. Exact lower 1
and upper κ are preserved. The source does not require the finite grid to
attain either endpoint or have actual condition number equal to κ.

For appended branches, positive-definite inverse meaning, finite positive
normalization, the Lebesgue/Gaussian convention, derivative criteria, and
determinant conjugacy remain explicit unproved background. A later consumer
must discharge them internally for any claimed actual Gaussian/density
statement; no theorem-shaped hypothesis can replace them.

## Bounded issue requiring a graph successor or repair overlay

The node `sg:fs-admiss:determinant-invariance` states both
`det(OΛOᵀ)=det Λ` and “hence” the full formula
`Z_A=(2π)^(d/2)(det Λ)^(−1/2)`.
Its incoming edge `edge:fs-admiss:determinant` has only the literal rotated
matrix, orthogonality and determinant background as parents. These suffice
for determinant invariance, but they do not suffice for the node's Z equality.
The latter also uses the existing `normalizer-integral` result. The issue is
a missing dependency for an actual asserted downstream source formula.

Two valid repairs are to add `normalizer-integral` as a prerequisite for that
full node, or to restrict the determinant node's claim to determinant
invariance and leave the Z substitution to a separate combination with the
normalizer result. Neither repair may drop the Z assertion from coverage or
add a public producer premise. The frozen original graph must remain intact;
an immutable successor or explicit repair overlay is required.

This blocks unconditional approval of the *full original graph*, not the
mathematical source compatibility of the unchanged precision seal. No other
blocking coverage or topology issue was found. Full phase-2 approval remains
pending independent review of the exact frozen repair. The Gaussian consumer
remains planned/unaudited, all proofs remain unproved here, and no source-V
or theorem-completion verdict is issued.
