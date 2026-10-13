# SPHMC Gaussian functional background: pinned availability audit

Status: external reference only; no new ASTIS theorem, compilation or upstream
evaluation credit. Evidence is in
`runs/20261007-companion-priority/gaussian-functional-availability/`.

The actual consumers are SPHMC v1 §4.1 equation (4.6)'s first comparison
`W₂(r,γ) ≤ sqrt(FI(r|γ))`, and the centered Laplace bound used in the proof of
Lemma 4.2, §4.1 paragraph 5.2. The last two comparisons of (4.6) have their own
actual posterior/position/Fisher producer. They do not prove Gaussian T₂ or LSI.
The independent primary contract is
`runs/20261006-companion-priority/gaussian-functional-preread/source-primary.contract.json`.
It identifies Gaussian T₂ with coefficient 2 and Gaussian LSI with coefficient
1/2 in KL/Fisher normalization. No background theorem number is printed there.

## Local versus external boundaries

The ASTIS canonical LSI interface consumes an LSI certificate and admissibility,
score and Gamma pairing data. It is not a construction of the analytic Gaussian
inequality. Mathlib `ProbabilityTheory.IsGaussian.exists_integrable_exp_sq`
provides some positive exponential square moment. This can supply integrability
for exponential Lipschitz observables, but does not supply the sharp centered
Laplace constant, Gaussian T₂ or LSI. `HasSubgaussianMGF` likewise contains its
bound as data. Targeted local/API searches did not find an unconditional Gaussian
LSI/T₂ producer; this is not a claim of exhaustive absence throughout Mathlib.

The pinned SLT revision is `d0f506f0a695018265dccb33bcb05e2f5ca1c876`.
Its actual recorded toolchain is Lean 4.32.0, and its Mathlib revision is
`81a5d257c8e410db227a6665ed08f64fea08e997`.
The actual ASTIS pins remain Lean 4.33.0 / Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`.
Apache 2.0 license and all 24 reachable SLT source modules were fetched at the
pinned revision. Static import traversal completed with zero fetch failures and
zero textual fake-closure hits. This does not certify elaboration, indirect
axioms, upstream CI or correctness at ASTIS's pins.

## Exact candidate statements and definitions

`GaussianSobolevReal.gaussian_logSobolev_W12_real` assumes
`MemW12GaussianReal f (gaussianReal 0 1)`, real differentiability and continuity
of the actual Frechet derivative. It concludes
`Ent_γ(f²) ≤ 2 ∫ ‖Df‖² dγ`. Its Sobolev predicate is exactly the conjunction of
`MemLp f 2 γ` and `MemLp (fun x => fderiv ℝ f x) 2 γ`.

`GaussianLSI.gaussian_logSobolev_W12_pi` assumes
`MemW12GaussianPi n g (stdGaussianPi n)`, real differentiability, continuity of
each actual partial derivative, and integrability of `g² log(g²)`.
Its conclusion is `Ent_γ(g²) ≤ 2 ∫ gradNormSq n g dγ`.
Here `stdGaussianPi n = Measure.pi (fun _ => gaussianReal 0 1)`,
`partialDeriv i g x = fderiv ℝ g x (Pi.single i 1)`, and
`gradNormSq n g x = ∑ i, (partialDeriv i g x)²`.
The Sobolev predicate contains `MemLp g 2 γ` and every partial derivative in L².
Entropy is the ordinary real integral expression
`∫ f log f dγ - (∫ f dγ) log(∫ f dγ)`; totalized integrals do not themselves
establish finiteness. The proof uses genuine one-dimensional smooth-density
approximation and entropy tensorization; this audit does not replace those
proofs with a supplied LSI assumption.

## Minimal admission route, before any proof search

1. Choose an actual paper consumer and seal the exact local mathematical target.
2. Reconstruct source and candidate dependency graphs independently of Lean.
3. Port only the needed analytic spine into ASTIS TechnicalLemmas, with license
   attribution and API adaptation; do not install SLT as a Lake dependency.
4. Prove the consumer's Sobolev/entropy/derivative regularity from its actual
   potential and law; do not append these as extra public paper hypotheses.
5. For arbitrary finite Hilbert space, prove Gaussian law and Euclidean
   gradient-norm transport, including dimension zero, rather than silently
   interpreting the product Pi norm as the Euclidean norm.
6. Keep Gaussian T₂ and the KL/Fisher density adapter separate. They are not
   conclusions of the candidate function-entropy theorem.
7. Focused compile, independent mathematics and encoder–denoiser review,
   Registry/publication admission and the mandatory ASTIS gate precede any
   callable local truth claim.

The next small genuine domain edge may instead use existing Mathlib Fernique to
produce all signed exponential moments for the paper's actual Lipschitz Gaussian
observables. That establishes a necessary Laplace-domain fact, with the sharp
centered bound still open. Persistent API failure must return a typed smaller
boundary, not add a certificate or promote this reference audit to a theorem.

## Subsequent pinned concentration candidate search

The same pinned Git tree also contains `SLT/GaussianLipConcen.lean`.
Its complete static SLT import closure is 27 modules, with zero fetch failures
or textual fake-closure hits; see `lipschitz-candidate-closure.json` and the
original pinned Git-tree snapshot. The declaration
`GaussianLipConcen.lipschitz_cgf_bound` states the sharp centered bound
`cgf(f-E[f], t) ≤ t² L²/2` for EuclideanSpace, but has explicit inputs `0<n`
and `0<L`, besides actual Lipschitz continuity. These are not allowable new
restrictions on the source's arbitrary directional observable: direction zero
and dimension zero require internal separate proofs. Its associated
`lipschitz_exp_centered_integrable_E` has no positive-dimension/L restriction
and proves genuine all-signed integrability. This candidate gives an actual
LSI/Herbst/mollification spine to inspect before attempting a new concentration
proof. It remains external reference only, not an ASTIS theorem or CI result.
The necessary consumer-domain SAU must retain first-L1 and actual expectation
centering even if the later sharp CGF inequality is ported successfully.
