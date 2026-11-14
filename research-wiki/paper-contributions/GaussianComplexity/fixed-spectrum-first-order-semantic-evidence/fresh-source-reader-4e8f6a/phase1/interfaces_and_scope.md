# Statement, calculus, normalizer, affine and oracle interfaces

These are source-derived semantic interfaces, not implementation APIs or a
Source Proof Graph. No candidate theorem was selected.

| Interface | Exact source scope and content | Required interpretation/bridge | Boundary to preserve |
|---|---|---|---|
| Global problem statement | §2: d≥1, κ≥1, symmetric precision A with I⪯A⪯κI; π_A=N(0,A⁻¹). | Positive definiteness from spectral lower bound; covariance is inverse precision. | This problem class is broader than the local fixed-spectrum family. |
| Local family statement | §4.1: d≥2, κ≥2, Chebyshev-midpoint spectrum; A=OΛOᵀ. | Λ diagonal, positive; O any real orthogonal matrix for pointwise facts. | No δ, q, ε or large-d premise is needed to state this family. |
| Printed admissibility statement | Lemma 4.6: every O∈O(d) gives I⪯A⪯κI. | Angle/cosine bounds, affine eigenvalue bounds and order under conjugation. | C.4's further calculus and normalization sentences are substantive source clauses beyond this short conclusion. |
| Calculus | C.4: V_A is C∞, Hessian A, 1-strongly convex, κ-smooth, V_A(0)=0 and unique minimum at 0. | Symmetric quadratic derivatives; conventional Euclidean curvature/smoothness definitions; quadratic lower bound. | Constants are admissible bounds, not claimed optimal constants. No higher-derivative assumption for nonquadratic targets is introduced. |
| Normalizer | C.4: Z_A=(2π)^(d/2)(det A)^(−1/2)=(2π)^(d/2)(det Λ)^(−1/2); known if spectrum public. | Positive definiteness/determinants; genuine Gaussian integral; det(OΛOᵀ)=det Λ for both determinant signs. | Z is the unnormalized density's integral, not reciprocal; independent of O for fixed Λ, not of d,κ or all A. It is not an oracle response. |
| Affine comparison | Remark 4.2: A_κ=(κ−1)A_2−(κ−2)I for the same O; one reply simulates the other. | Same d and cosine grid; nonzero κ−1; query known to simulator. | Same-O comparison is distinct from full-O universality; no pointwise relation between independently rotated matrices and no equality of target laws. |
| Exact oracle | §2 Eq. (1): (f_A(x),∇f_A(x))=(xᵀAx/2,Ax); equivalence to gradient-only and matrix–vector access. | Exact simulations at the same query; free scalar/vector arithmetic in this information model. | No A⁻¹x reply, noisy query or numerical bit-cost theorem. |
| Query cap | §2 Eq. (2): ∃one Alg, uniform ∀A TV bound, per-input output law averages seed; deterministic cap every input/seed. | Borel algorithms, input-independent randomness. | No expected-query objective is defined. Seed averaging in accuracy does not average the budget. |
| Main lower-bound statement | Theorem 4.1: ∀fixed δ∈(0,1), ∃d₀(δ), all d≥d₀, κ∈[2,d^(1−δ)], ε∈(0,1/10]; lower bound δ√κ log d/256. | Internal derivation of n<d, τ≤1/2, d−n≥√κ, τ≤β/4, Mβ²≥320 uniformly. | These derived proof conditions are dependencies, not additional source hypotheses; no ε-growth conclusion. |
| Algorithm statistic | Lemmas 4.3–4.4: law-preserving representation plus one event uniform over K_q. | Full-experiment coefficients; arbitrary output; orthogonality transfers diagonal quadratic form. | Average-over-input probability, not per-fixed-input rejection bound; no unsupported independence with O,X. |
| Target statistic | Lemma 4.5: exact finite-grid moments and variances, conditional bias bounds. | Y conditional on O rotates to N(0,Λ⁻¹); preserve n and d−n restrictions. | Ratio of means is not silently an expected ratio; the proof controls S_A directly by moments. |
| Main TV contradiction | §4.3: algorithm average acceptance≤.01, target every-input acceptance≥.9; inputwise TV then average. | E_A is polynomial-defined Borel event; measurable input-dependent kernel evaluation. | No single input-independent test or prior-marginal TV assumption needed. |
| Larger-κ method boundary | §4.4: K_q generically full when (q+1)²≥d; for n<d uniform D_n ratio≥1/√2. | Distinct spectrum/generic dimension; cosine-square identity. | Limitation of enlarged-space method, not proof that fixed-spectrum family lacks harder behavior. |
| Accuracy method boundary | §4.4: a≥c/√d, a<β≤exp(−2n/√κ) forces q=O(√κ log d). | Cited Bernstein calculation and mean/variance certificate; positive log arguments. | Fact C.6 not inspected; no universal impossibility theorem. Stronger bounds for the same family remain open. |

No original derivation of the Gaussian integral, the Hessian-definition
equivalences, the C.1–C.3 results, the generic-dimension lemma, or the cited
Bernstein calculation is supplied by this phase. Standard mathematical
interpretation makes their intended roles intelligible; it does not certify a
future formal proof or justify moving them into a source theorem's hypotheses.
