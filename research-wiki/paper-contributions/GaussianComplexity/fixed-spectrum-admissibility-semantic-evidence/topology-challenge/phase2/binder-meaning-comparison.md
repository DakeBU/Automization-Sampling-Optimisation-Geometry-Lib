# Phase 2 binder and meaning challenge — topology pending

Reviewer: `/root/fs_admiss_topology_challenge`, independent of the formalizer
and independent source-graph author. This compares only the admitted exact
statement and minimal standard definition context to my previously frozen
source-first reconstruction. It does not approve a proof or source-V status.
No target proof/API or root proposed audit was opened.

Frozen phase 1: `phase1/freeze.json`, SHA-256
`b3dadd1fc6800cf8f670502429c70911bc8bbb8879e2af6275ac9d0c08a7e3f7`.
Admitted seal raw SHA-256:
`ab68d72daa52e4607be3acf310b93cb0ad20c3638cd8062078805e3a33eccab0`.
Signature UTF-8 SHA-256:
`186231307d4c41acba15a1098c56518120394295cf048f504fed6f8ea50018d5`.
The parent has not yet delivered an independent source graph/coverage packet;
all topology decisions and the final phase-2 freeze remain pending.

## Binder expansion

| Logical input | Expanded meaning | Classification | Finding |
| --- | --- | --- | --- |
| `{d : ℕ}` | A finite integer dimension, represented by a natural number | TYPING | Matches the finite real source carrier |
| `hd : 2 ≤ d` | Local hard-family dimension bound | SOURCE, construction context | Exactly S4.1; no large-d condition added |
| `{κ : ℝ}` | Real spectral-bound parameter | TYPING | Matches source parameter |
| `hκ : 2 ≤ κ` | Local hard-family parameter range | SOURCE, construction context | Exactly S4.1; no δ-dependent upper bound added |
| `O : Matrix.orthogonalGroup (Fin d) ℝ` | A square real matrix satisfying both transpose inverse identities | SOURCE with standard finite-square representation | Full real O(d), both determinant components; no Haar/genericity/algorithm premise |

The outer proposition is otherwise a literal `let θ`, `let A` and an output
conjunction. These lets are definitions, not extra hypotheses. No project-owned
Prop alias, theorem-shaped assumption bundle, witness, smoothness certificate,
inverse certificate, PSD certificate, Gaussian integral certificate, or
normalization premise is present. EXCESS count: **zero in the admitted exact
signature**.

The group alias expands as `orthogonalGroup := unitaryGroup`,
`unitaryGroup := unitary (Matrix ...)`, and the latter carrier is
`star O * O = 1 ∧ O * star O = 1`. The matrix star is conjugate transpose;
over real scalars this is transpose. The source defines O(d) using
`OᵀO = I`. On square finite real matrices that implies invertibility and hence
the second identity. Conversely the admitted type immediately gives the
source identity. Requiring the standard two-sided group carrier therefore
does not exclude a source matrix. This equivalence is a semantic fact of the
fixed finite carrier; any required implementation bridge belongs inside the
proof, not in an additional source binder. No determinant-sign constraint is
present.

## Definition and carrier expansion

`Matrix (Fin d) (Fin d) ℝ` is literally `Fin d → Fin d → ℝ`.
The admitted angle is `((i.val : ℝ) + 1/2) * π / (d : ℝ)`.
Under source index `i_source = i.val+1`, this is exactly
`(i_source−1/2)π/d`. The contextual `d≥2` supplies denominator positivity;
it is not supplied by another binder. The displayed diagonal definition has
these eigenvalues on its diagonal and zero off it. The admitted `A` is the
literal product `O * Λ * O.transpose` in the same order as source Eq. (11).

`PosSemidef M` expands to Hermitian symmetry and nonnegativity of

`Σ_i Σ_j star(x_i) * M_ij * x_j`

for every finitely supported coordinate function. `PosDef M` adds strict
positivity for every nonzero such function. For real scalars the star on a
coordinate is the identity. On `Fin d`, every ordinary coordinate vector has
finite support: its nonzero coordinates form a subset of a finite set.
Conversely each Finsupp gives an ordinary coordinate vector. The sums therefore
range over all real vectors and give the usual quadratic form. This is not a
sparse-vector restriction and it does not need a source finite-support
assumption.

`IsHermitian M` is `Mᴴ=M`; conjugate transpose is transpose followed by entrywise
star, so over ℝ it is ordinary symmetry. Matrix `1` is diagonal scalar 1, and
scalar action is entrywise. Thus `(A−1).PosSemidef` and
`(κ • (1 : Matrix ...)−A).PosSemidef` have precisely the meanings
`I≼A` and `A≼κI`, respectively. They are matrix/quadratic inequalities, not
entrywise inequalities.

There is no characterized object, choice, quotient, fallback, off-source
branch, or unspecified target law in the signature. The literal definitions
are source-equivalent on the sealed public carrier. This finding does not
audit any future Gaussian consumer definition.

## Conclusion comparison and the explicit PosDef consequence

The source's named Lemma 4.6 concludes the two Loewner bounds. The admitted
conclusion contains these and additionally `A.PosDef`. This is an explicit
**output consequence**, not an input. It does not strengthen the theorem's
assumptions. On the finite real carrier the lower sandwich bound entails it:
the quadratic form of A is the quadratic form of A−I plus the squared Euclidean
norm, which is positive on a nonzero vector; symmetry follows as well.
Accordingly the whole admitted conjunction is mathematically equivalent to
the source sandwich on this carrier, with positive definiteness exposed for
its downstream consumer. No source repair is needed for this conclusion
expansion, and no EXCESS binder is introduced by it.

This is a statement-equivalence judgment, not a checked implementation of that
consequence. The target remains type-only and unproved. In particular the
unused-binder warning in a Prop-only elaboration is not evidence that the
source domain conditions should be dropped.

## Seven-slot comparison

| Slot | Comparison with frozen phase 1 |
| --- | --- |
| Objects | Same literal cosine grid and conjugated precision; no covariance substituted for precision |
| Domains | Same d≥2, κ≥2, square real finite-dimensional matrices and full O(d) |
| Quantifiers | Arbitrary d, κ in source range and every O; no almost-sure or existence weakening |
| Assumptions | Exactly source contextual bounds and orthogonal carrier; zero EXCESS inputs |
| Conclusion | Exact two sandwich bounds plus a logically forced PosDef output; symmetry is represented by the definitions |
| Scopes/senses | Deterministic result, independent of an algorithm, seed, query cap, error, or probability event |
| Constants/dependencies | Literal 1, κ, half-grid and π; no hidden dimension threshold or δ-dependent restriction |

No blocking slot delta was found for this precision-admissibility statement.
This is not a completed post-proof semantic round trip: I have source exposure
and am ineligible to serve as its source-blind decoder.

## Consumer and full-source coverage boundaries

The seal explicitly calls its real Gaussian consumer **planned**, with the
interface to be audited after source/topology admission. That is accurate as
a status boundary. The precision theorem currently states neither an inverse
identity nor a probability-law identity. A later consumer must use the actual
literal A and establish, internally, that its actual inverse is a valid
covariance/precision for `N(0,A⁻¹)` or for the corresponding nondegenerate
density. Proving that some Gaussian exists, or accepting an arbitrary covariance
and an assumed equality to A⁻¹, would not meet that consumer description.
No concrete target law definition/API has been supplied here, so its eventual
source-equivalence remains open. This is a future consumer gate, not an extra
producer hypothesis and not a reason to block the current producer statement.

Likewise the producer statement does not conclude all of C.4. Its bounds and
produced PosDef do not by themselves certify a formal Hessian computation,
strong convexity/smoothness theorem, unique-minimizer theorem, Gaussian-law
identification, actual Gaussian integral, determinant equality, or
rotation-independent known normalizer. Those are substantive appendix source
regions and must remain explicit unproved/background/excluded-with-reason
items in full coverage, rather than disappearing behind “Lemma 4.6 accepted.”
The seal's stated truth boundary currently preserves that distinction.

## Pending decision

Binder/definition/meaning result: **no blocker found for the exact admitted
precision signature**. Target proof construction, Gaussian-consumer approval,
full-C.4 formalization, source-V acceptance, and topology approval are not
asserted. Await the independently authored source graph and complete source
coverage before issuing the final phase-2 challenge/freeze.
