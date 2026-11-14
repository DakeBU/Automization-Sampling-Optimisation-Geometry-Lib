"""Prepare anonymous literal statements and scoped source restatements; no verdicts."""
from pathlib import Path
import json, sys
sys.path.insert(0, 'tools')
import astis_semantic_roundtrip as rt

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
seal = json.loads((W / 'statement-seal.unclaimed.v1.json').read_bytes())
def create(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as f:
        json.dump(o, f, ensure_ascii=False, indent=2)
        f.write('\n')

pcontext = [
    'The type variable ranges over a finite nonempty index set; Fintype supplies its finite enumeration and DecidableEq decidable equality. The universe variable only specifies the universe of that index type.',
    'Matrix is the finite real matrix algebra on the displayed index set. Matrix multiplication is ordinary algebra multiplication, scalar multiplication is real scalar multiplication, and 1 is the identity matrix.',
    'For a real square matrix, IsHermitian means that its transpose equals itself. PosSemidef means positive semidefinite in the full quadratic-form sense, including self-adjointness; it is not an entrywise inequality.',
    'NormedSpace.exp on this real matrix algebra is its convergent matrix power-series exponential. It is not the entrywise real exponential. Real.exp is the scalar real exponential.',
    'The active matrix norm is the Euclidean L2 operator norm, with the ordinary finite-coordinate topology. The scalar real matrix algebra and rational-algebra structure are the standard ones.'
]
tcontext = pcontext[1:] + [
    'Fin n is the finite set of natural numbers strictly less than n; i.val is its zero-based natural index. Natural numbers embed into real numbers in the usual way.',
    'EuclideanSpace real (Fin n) is real n-dimensional Euclidean space with its Euclidean norm and Borel structure. WithLp.toLp 2 wraps coordinates as a Euclidean vector, and WithLp.ofLp recovers the same coordinates.',
    'stdGaussian is the centered Gaussian probability measure with identity covariance. Measure.pi is the displayed finite product measure on the function space. A measure in a displayed integral is exactly that measure, without implicit conditioning.',
    'Real.log is the natural logarithm and Real.sqrt is the nonnegative real square root. An if-test written with less-than-or-equal includes equality. Real inverses are totalized at zero in the usual field convention.',
    'Matrix.vecMulVec u v has entry u_i v_j. The Kronecker product has entry A_(i,k) B_(j,l) at row (i,j) and column (k,l); the paired indices preserve this displayed order.',
    'The displayed integrals are Bochner integrals in the corresponding finite matrix space. Their definition is totalized to zero for a nonintegrable integrand. Reconstruct the displayed proposition without adding integrability premises or conclusions.',
    'All local let definitions have the scope of the full subsequent proposition. Each universal real parameter and each finite row index has exactly the order displayed.'
]
texts = [
    'Real deterministic proof component of Tropp Lemma6.7 (author preprint revised15June2011, p25, with functional-calculus conventions p7-8): for every finite nonempty real square matrix A, if A is self-adjoint, I-A is positive semidefinite, and s>0, then I+sA+(exp(s)-s-1)A^2-exp(sA) is positive semidefinite. The upper spectral cap is one-sided; no lower eigenvalue bound, positivity of A, or two-sided norm bound is assumed. This is the real restriction of that deterministic component, not the full complex random-matrix MGF theorem.',
    'Authored private actual-Gaussian specialization of the normalized single-matrix MGF comparison in Tropp Lemma6.7 p25-26, independently matched external background for the uncited Bernstein invocation in Gaussian2610.20492v1 AppendixC.2Ex121. For every natural d,q with2q+1<d, includingq0, r=q+1 and Omega=(R^d)^r with the original unconditional product mu of r standard d-dimensional Gaussian column laws. The physical row Phi_i has coordinates omega_b(i). Define theta_i=(i-1/2)pi/d for source indicesi=1,...,d, t_i=(1,sqrt(2)cos(theta_i),...,sqrt(2)cos(q theta_i)), L=2r+3log(1000d), and Y_i=d^(-1)(Phi_i Phi_i^T tensor t_i t_i^T) on the inclusive own-row cutoff norm(Phi_i)^2<=L, zero otherwise. Define the actual mean_i=integral Y_i dmu, Z_i=Y_i-mean_i, rho=2r(L+1)/d, and X_i=rho^(-1)Z_i. Then for every real s>0 and each physical row i, exp((exp(s)-s-1) integral X_i^2 dmu)-integral exp(sX_i) dmu is positive semidefinite. rho positivity, zero mean, Hermitian structure, measurability/integrability, norm/spectral cap and expectation adapters are internally discharged, not extra theorem binders. No good-event conditioning, arbitrary replacement means, Bernstein sum tail, probability conclusion, weighted result or public consumer API is asserted.'
]
ids = ['ASTIS-RT-20261114-HuanjianMatrixBernsteinExponential',
       'ASTIS-RT-20261114-HuanjianMatrixBernsteinExponentialPrivateConsumer']
audits = []
for i, key in enumerate(['producer', 'actual_private_consumer']):
    x = seal[key]
    name = x['name'] if i == 0 else '_private.Tests.GaussianComplexityBernsteinMgf.0.' + x['name']
    statement = '∀ ' + x['signature'].replace(' :\n', ' ,\n', 1)
    a = {'id': ids[i], 'state': 'draft',
         'source': {'source_id': 'tropp2011-real-deterministic-exponential-quadratic' if i == 0 else 'gaussian-original-normalized-single-summand-mgf-authored-specialization',
                    'anchor': 'Tropp2011Lemma6.7p25-26; explicit real deterministic component and separately authored original-Gaussian single-summand specialization only',
                    'original_text': texts[i], 'text_sha256': rt.sha256_text(texts[i])},
         'lean': {'declaration': name, 'file': x['planned_file'], 'statement': statement,
                  'statement_sha256': rt.sha256_text(statement), 'compiled': True,
                  'formalizer': 'huanjian_20261114_matrix_bernstein_exponential',
                  'decoder_context': pcontext if i == 0 else tcontext},
         'repairs': [], 'source_review': {'state': 'pending'}, 'verdict': 'pending',
         'candidate_commit': '0ff1e2227b8e5a45a6a73906582ef042bd0d73ff'}
    assert not rt._core._decoder_context_violations(a)
    audits.append(a)
create(Path('research-wiki/semantic-roundtrip/audits/huanjian-matrix-bernstein-exponential.json'), audits[0])
create(W / 'private-consumer-audit.draft.json', audits[1])
create(W / 'private-consumer-registry.draft.json', {'schema_version': 1, 'audits': [audits[1]]})
print(json.dumps({'draft_audits': 2, 'statement_hashes': [a['lean']['statement_sha256'] for a in audits],
                  'new_semantic_verdicts': 0, 'private_scope': 'Authored actual original-Gaussian single-summand specialization only'}))
