# OpenAI Math assimilation protocol for Samplinglib

Status: active intake protocol, 2026-10-07.

This protocol governs material taken from `openai/math` into Samplinglib. It extends, rather than replaces, the theorem-publication, proof-digestion, evidence-routed-memory, encoder-denoiser, and Functor-Hypergraph rules already required by this repository.

## 1. Upstream pin and trust boundary

The first reviewed upstream snapshot is:

- repository: `openai/math`;
- commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`;
- upstream release date: 2026-10-06;
- upstream formalization license: Apache-2.0.

Never cite a floating `main` as evidence. Every intake record must keep the upstream commit, module path, relevant blob/tree SHA when available, source-preprint anchor, and license/NOTICE obligation.

An upstream Lean theorem is evidence that a proposition compiled in the upstream environment. It is **not** automatically:

1. the same statement as a Samplinglib theorem;
2. a valid replacement for Chewi/SampleWiki source semantics;
3. a canonical local definition;
4. a proof dependency in the local Lean Graph; or
5. evidence that an entire paper, chapter, or route has been formalized locally.

## 2. Four intake classes

Every candidate must be classified before code is moved.

- `canonical-leaf`: a source-independent lemma/API that should live in Samplinglib's shared technical layer after local proof or a reviewed compatible adapter.
- `adapter-backed`: a useful upstream definition/theorem whose semantics differ from the local canonical API; admit only after an explicit adapter and equivalence/implication theorem.
- `source-route`: a source-specific theorem family that deserves a textbook/frontier route and graph nodes, but must not be mistaken for shared foundations.
- `provenance-only`: useful source, benchmark, negative example, or future route; no local formal theorem claim.

The default is `provenance-only`. Promotion requires evidence.

## 3. Mandatory semantic gate

For every promoted declaration, record four statements separately:

1. the paper/source statement;
2. the exact upstream Lean statement;
3. the proposed local canonical statement;
4. the source-blind reconstruction of the local Lean statement.

Then audit, binder by binder:

- spaces and measurable structures;
- probability normalization and reference measure;
- smoothness/regularity;
- convexity, strong-convexity, Hessian, curvature, and minimizer assumptions;
- metric/divergence and normalization;
- oracle information and adaptivity;
- deterministic versus expected budgets;
- error criterion (TV, KL, Wasserstein, chi-square, etc.);
- asymptotic quantifiers and constants.

The existing invariant remains absolute:

> proof ingredient = dependency edge; source hypothesis = theorem binder.

A theorem available upstream is a potential producer edge. It never legalizes adding its conclusion as an extra public premise to a source-facing theorem.

## 4. No namespace transplant

Do not copy `OAI.*` wholesale into production. First search Mathlib and existing `AutoSamplingTheory/TechnicalLemmas`, `Probability.lean`, `SDE.lean`, Chewi routes, optimisation routes, and geometry routes.

Prefer, in order:

1. existing local/Mathlib theorem;
2. one generalized local leaf with multiple consumers;
3. a narrow adapter to an upstream-style object;
4. a source-specific local theorem;
5. only then a faithful local port of a larger upstream dependency closure.

A copied implementation detail that has one paper-specific consumer stays source-local. A mathematical lemma with two genuine consumers should be generalized and placed in the shared spine.

## 5. Priority A: well-conditioned log-concave sampling

The first high-priority cluster is
`lean/OAI/Probability/LogConcave` (upstream tree SHA
`23908d6dd9eb7b5dc7fd141c9c849607c422eb27`) together with the preprint
*Subpolynomial query complexity for well-conditioned log-concave sampling*.

### 5.1 Preserve the exact model boundary

The upstream model fixes (V\in C^2(\mathbb R^d)), (V(0)=0),
(\nabla V(0)=0), and
(I\preceq \nabla^2 V(x)\preceq 2I). A first-order query returns
((V(x),\nabla V(x))). Algorithms may be adaptive and randomized, have
unrestricted real computation between queries, and are required to have a
deterministic query cap on every execution. The target error is TV at most
(1/10).

These are route-specific binders. Do **not** bake them into Samplinglib's
generic notions of log-concavity, sampler, or oracle.

The source-facing frontier node should expose separately:

- (Q(d)\le C_\varepsilon d^\varepsilon) for every (\varepsilon>0);
- (Q(d)\ge c\log d) for large (d);
- optimal dimension exponent (\gamma_*=0).

Do not paraphrase this as a polylogarithmic algorithm, a practical running-time
bound, or a bit-complexity result.

### 5.2 Extract the proof graph by mechanism, not file order

Build the local route with the following AND spine and explicit OR subroutes.

1. **Near-quadratic conditional law.** Gaussian conditioning converts a
   restricted conditional sample into a weak perturbation of a Gaussian.
2. **Gaussian interpolation / conditional velocity.** The transport velocity
   is a conditional gradient mean.
3. **Dimension-controlled jets.** Poincare + multivariate Appell/cumulant
   estimates control every nontrivial tensor split without paying a fresh
   dimension factor at each derivative.
4. **Stationary centering flow.** A skew drift preserves the product law and
   converts a path integral of conditional means into Gaussian-centered mean
   information.
5. **Finite nested-mean compiler.** Query-preserving center translations and a
   covariance reduction absorb Gaussian center noise exactly.
6. **Numerical realization.** High-order quadrature/Picard formulae are
   compiled into finitely many first-order queries.
7. **Proximal return to target.** A contracting Gaussian proximal chain reaches
   the noised target; variance-halving conditioning removes the remaining
   Gaussian noise.
8. **Independent lower-bound route.** Rotational/Krylov information, explicit
   spectra, transcript control, and a separating statistic yield the logarithmic
   lower bound.

This structure must appear in the Source Proof Graph. The Lean Graph may have a
different topology.

### 5.3 First shared leaves to investigate

Before porting paper-specific code, prioritize these candidate reusable leaves:

- Poincare-to-vector/tensor variance interfaces;
- all-split cumulant bounds;
- Gaussian conditional-mean derivative identities;
- conditional integration-by-parts identities;
- Lipschitz transport-flow facts;
- invariant skew-flow identities;
- Wasserstein contraction under a strongly convex conditional;
- Gaussian smoothing from Wasserstein error to TV where hypotheses match;
- query-preserving Gaussian seed translation/covariance absorption;
- deterministic routine-tree/query-cap bookkeeping;
- adaptive first-order transcript abstractions and lower-bound information
  interfaces.

Generalize only after the exact paper theorem compiles in a source-faithful
form or a faithful upstream-to-local adapter is proved.

### 5.4 Local placement

- source-specific theorem route: `research-wiki/`, paper/frontier records, and a
  dedicated source-facing Lean namespace when implementation begins;
- generic probability/analysis leaves: `AutoSamplingTheory/TechnicalLemmas/`;
- generic SDE/flow leaves: the existing SDE technical spine;
- oracle/query-complexity abstractions: a shared technical module only if they
  have more than one real consumer;
- reader exposition: normal Samplinglib textbook/frontier format, not an
  upstream code browser.

The Chewi textbook remains the primary pedagogical spine. This OpenAI result is
a research-frontier route that should reuse Chewi foundations and feed reusable
lemmas back into them; it must not overwrite Chewi theorem identities.

## 6. Priority B: Riemannian geometry and optimal transport

High-value upstream clusters include:

- `OAI/Geometry/WeakMTW` (tree SHA
  `944c98c51c879dab2dfd96afb3711c8150fa2a97`);
- `OAI/Analysis/BiholderTransport`;
- `OAI/Geometry/Riemannian/HarmonicCore` (Riemannian tree SHA
  `12faf71a8a3cb28634ca9152ff5a5af3cd374f4b`);
- `OAI/Analysis/RCDHeat`.

For `WeakMTW`, separate at least these layers before reuse:

1. manifold / tangent / metric primitives;
2. complete geodesics, exponential endpoint, injectivity domain;
3. cost (d^2/2) and first/second variation;
4. normal coordinates and geodesic-flow interfaces;
5. MTW curvature;
6. support/envelope/collision arguments;
7. global-support and transport regularity theorems.

Never merge weak MTW, sectional/Ricci curvature, geodesic convexity,
displacement convexity, or Bakry-Emery curvature into one predicate merely
because they participate in superficially similar convergence arguments.
Conceptual mirrors belong in the Functor Hypergraph with explicit hypothesis
maps and failure boundaries.

## 7. Priority C: discrete sampling and mixing

Create a distinct discrete-sampling route for, at minimum:

- `OAI/Probability/BinarySweep`;
- `OAI/Probability/CoordinateSweeps`;
- `OAI/Probability/Contingency`;
- `OAI/Probability/SwitchChain`;
- `OAI/Probability/ThorpShuffle` plus the Thorp compatibility/results/routing
  clusters;
- `OAI/Probability/StrongRayleigh`.

Do not force these into the Langevin/SDE branch. Their shared graph should be
built around mechanisms such as conditional resampling, contraction,
spectral/energy decay, couplings, comparison, negative dependence, and
TV-from-(L^2), with dashed conceptual bridges to continuous sampling until a
formal adapter theorem exists.

## 8. Optimisation intake rule

The upstream `OAI/Optimization` directory is currently not a broad continuous
optimisation library. Do not create a misleading “OpenAI optimisation import”
badge. Optimisation-relevant primitives should instead be mined from the actual
clusters that contain them—convex geometry, transport, variational arguments,
matrix inequalities, projected/subgradient arguments—and admitted theorem by
theorem when they strengthen the existing optimisation textbook graph.

## 9. Graph contract

Every OpenAI intake item gets:

- an upstream source node identified by commit + path;
- a source-statement node;
- zero or more local canonical-definition nodes;
- explicit adapter/equivalence edges;
- local compiled dependency edges only after local Lean verification;
- dashed conceptual-mirror edges otherwise.

For a theorem with alternative proof routes, encode an OR-node. For a proof
requiring several ingredients, retain the full AND-tail. Never flatten a
hyperedge into multiple independent implications.

Useful new candidate families include:

- `family:gaussian-conditioning-smooths`;
- `family:all-split-cumulant-control`;
- `family:conditional-mean-transport`;
- `family:query-preserving-randomness-transport`;
- `family:proximal-contraction`;
- `family:oracle-information-lower-bound`;
- `family:discrete-energy-mixing`.

These are conceptual until their exact local substrates are reviewed.

## 10. CI and review gate

An OpenAI-derived contribution is not publishable until all ordinary Samplinglib
gates pass plus the following evidence exists:

- pinned upstream commit/path/SHA and license record;
- source-preprint anchor;
- upstream statement seal;
- local statement seal;
- definition/hypothesis diff;
- reuse search result;
- local Lean build evidence;
- independent source-blind reconstruction;
- anti-anchored source review;
- graph delta classification;
- reader-facing source/Lean/natural-language correspondence;
- purification pass removing duplicate wrappers and paper-local definitions that
  should have been shared.

A direct copy that compiles but bypasses this evidence is rejected.

## 11. Updating to a later OpenAI snapshot

Never silently advance the pin. A later snapshot is a new intake event:

1. record old and new commits;
2. diff only admitted upstream closures first;
3. classify semantic versus implementation-only changes;
4. re-run statement/definition audits for semantic changes;
5. preserve the old source reconstruction;
6. update adapters and local proofs;
7. only then advance the canonical intake record.

This makes upstream evolution auditable and prevents a moving external branch
from mutating Samplinglib's mathematical meaning.

## Upstream verification-status gate

The OpenAI repository explicitly contains results at different verification
stages. File presence is not a proof-status badge. For each source route, inspect
`lean/formalization.yaml`, its Comparator challenge/config when present, and
the exact solution declaration. Record one of: `comparator-backed`,
`lean-present-not-comparator-audited`, or `manuscript-only`.

Examples at the pinned snapshot include comparator-backed
`OAI.LogConcaveSampling.exact_source_main`,
`OAI.WeakMTWTransport.uniform_biHolder_transport`, and
`OAI.binary_sweep_contraction_and_mixing`. A manuscript-only or un-audited
candidate remains provenance-only until our own local gate is completed.

## Additional audited routes from the catalog sweep

The intake map also records several routes that are too important to leave as
generic future candidates:

- `OAI/Geometry/WeakHessian`: comparator-backed RCD/metric-measure weak-Hessian,
  heat-flow and transport infrastructure. Audit it against the existing
  Riemannian/optimal-transport/Bakry-Emery spine before choosing canonical APIs.
- `OAI/MathematicalPhysics/CriticalMixing`: comparator-backed heat-bath/Glauber
  mixing at critical SK. This is a source route for discrete MCMC and a source
  of candidate Dirichlet-form, entropy, spectral and TV-mixing leaves; do not
  generalize the spin-glass-specific hypotheses away.
- *A dimension-free logarithmic Sobolev inequality for subgaussian log-concave
  measures*: currently manuscript-only in this audit. It belongs in the
  functional-inequality provenance graph and should be mapped to Chewi/LSI/
  Bakry-Emery material, but it must not receive a verified-Lean badge until a
  comparator-backed formalization is located or a local one is completed.

Coordinate sweeps, Switch Chain, and the Thorp developments have explicit
Comparator-backed endpoints. Their reusable content should be mined below the
paper-specific theorem level: conditional resampling, finite-law semantics,
spectral/energy decay, TV conversion, comparison, and routing/compatibility.

