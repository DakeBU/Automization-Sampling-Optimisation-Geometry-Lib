"""Author source restatements and source-blind definition context; no verdicts."""
from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
sha=lambda b:hashlib.sha256(b).hexdigest()
def create(p,o):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixStructure.lean')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixStructure.lean')
seal=json.loads((W/'statement-seal-v2.json').read_bytes())
context=[
 'Fin n is the finite set of natural numbers less than n. Natural numbers are embedded into the real numbers by the usual coercion.',
 'EuclideanSpace real (Fin n) is real n-dimensional Euclidean space, with Euclidean norm and its Borel sigma algebra. WithLp.toLp 2 wraps a coordinate function as a Euclidean vector, and WithLp.ofLp recovers the same coordinates.',
 'stdGaussian is the centered Gaussian probability measure with identity covariance. Measure.pi is the finite product measure on the displayed function space.',
 'Real.log denotes the natural logarithm and Real.sqrt the nonnegative square root. An if-condition using less-than-or-equal includes equality.',
 'Matrix.vecMulVec u v has entry u_i times v_j. Matrix.kronecker A B has entry A_(i,k) times B_(j,l) at row (i,j) and column (k,l). Scalar multiplication and subtraction are ordinary real matrix operations.',
 'The local letI fixes the measurable space of the finite real matrices to borel of their topology. Their topology is the ordinary finite coordinate topology. The opened L2 operator norm convention gives the norm of the matrix action between real Euclidean spaces and preserves that topology.',
 'Measurable means measurable for the displayed domain and codomain sigma algebras. iIndepFun f mu means the entire displayed indexed family of random functions is jointly independent under mu, not only pairwise independent.',
 'Integrable f mu means Bochner integrable, including almost-everywhere strong measurability and finite integral of the norm. The integral notation is the Bochner integral; it is totalized to zero for nonintegrable functions. Reconstruct each asserted integrability and integral equality exactly as displayed.',
 'For real matrices, A.IsHermitian means A equals its transpose (equivalently its conjugate transpose, since real conjugation is trivial). This is a symmetry condition.'
]
common='For all natural d,q with 2q+1<d, put r=q+1, including q=0. On Omega=(R^d)^r with mu the product of r independent standard d-dimensional Gaussian column laws, let Phi_i be the actual physical row. Put theta_i=(i-1/2)pi/d, t_i=(1,sqrt(2)cos(theta_i),...,sqrt(2)cos(q theta_i)), and L=2r+3log(1000d). Define Yi=d^(-1)(Phi_i Phi_i-transpose tensor t_i t_i-transpose) when norm(Phi_i)^2<=L and zero otherwise. The cutoff is inclusive and local to row i. Let Mi be the actual Bochner integral of Yi under this same original unconditional mu, and Zi=Yi-Mi. Matrix measurability uses the standard finite-coordinate Borel structure; norms use real Euclidean operator norms. '
texts=[common+'Each Zi is measurable. The entire family (Zi) indexed by i is jointly independent under mu. Each Zi is Bochner integrable, its actual integral under mu is zero, and Zi(omega) is Hermitian for every i and every omega. These are the structural prerequisites used for the unweighted matrix Bernstein step in Appendix C.2; no concentration tail is asserted here.',
 common+'Put wi=cos((2q+1)theta_i) and Xi=wi Zi. Each Xi is measurable. The entire family (Xi) indexed by i is jointly independent under mu. Each Xi is Bochner integrable, its actual integral under mu is zero, and Xi(omega) is Hermitian for every i and every omega. Weights may be zero or negative. These are the corresponding prerequisites for the weighted matrix Bernstein step, without any combined-family independence or concentration conclusion.']
ids=['ASTIS-RT-20261113-HuanjianGaussianSourceMatrixStructure','ASTIS-RT-20261113-HuanjianGaussianSourceMatrixStructurePrivateConsumer']
names=[seal['producer']['name'],'_private.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure.0.AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure.actual_source_weighted_centered_matrix_structure']
audits=[]
for i,(k,p,text) in enumerate(zip(['producer','actual_private_consumer'],[P,T],texts)):
    sig=seal[k]['signature'];assert sig in p.read_text()
    statement='∀ '+sig.replace(' :\n',' ,\n',1)
    a={'id':ids[i],'state':'draft','source':{'source_id':'c2-actual-centered-matrix-structure' if i==0 else 'c2-private-weighted-centered-matrix-structure','anchor':'Appendix C.2 p13-p14, Ex113 and weighted Ex115; original Gaussian experiment p1, cutoff Ex107, actual mean p12; Lemma4.4 regime','original_text':text,'text_sha256':rt.sha256_text(text)},'lean':{'declaration':names[i],'file':str(p),'statement':statement,'statement_sha256':rt.sha256_text(statement),'compiled':True,'formalizer':'huanjian_gc_20261113_source_matrix_structure','decoder_context':context},'repairs':[],'candidate_commit':'9ed997b7fda8631deb5bc1397d021495d53c4d41'}
    assert not rt._core._decoder_context_violations(a)
    audits.append(a)
create(Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-structure.json'),audits[0])
create(W/'private-consumer-audit.draft.json',audits[1])
create(W/'private-consumer-registry.draft.json',{'schema_version':1,'audits':[audits[1]]})
print(json.dumps({'draft_audits':2,'statement_hashes':[a['lean']['statement_sha256'] for a in audits],'semantic_verdicts':0}))
