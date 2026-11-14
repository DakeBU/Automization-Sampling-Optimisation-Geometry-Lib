"""Source restatements and minimal anonymous contexts; no semantic verdicts."""
from pathlib import Path
import json,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
seal=json.loads((W/'statement-seal-v1.unclaimed.json').read_bytes())
def create(p,o):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
context=[
 'Fin n is the finite set of natural numbers strictly less than n; i.val is the zero-based natural value of i. Natural numbers embed into the reals in the usual way.',
 'EuclideanSpace real (Fin n) is real n-dimensional Euclidean space with its Euclidean norm and Borel structure. WithLp.toLp 2 wraps a coordinate function as a Euclidean vector; WithLp.ofLp recovers its same coordinates.',
 'stdGaussian is the centered Gaussian probability law with identity covariance. Measure.pi is the displayed finite product measure on the corresponding function space.',
 'Real.log is the natural logarithm; Real.sqrt is the nonnegative square root. Set.indicator S f is f on S and zero off S. An if-condition written with less-than-or-equal includes equality.',
 'Matrix is the displayed finite real matrix space. Matrix.vecMulVec u v has entry u_i v_j. Matrix.kronecker A B has entry A_(i,k) B_(j,l) at row (i,j) and column (k,l). transpose interchanges matrix indices; multiplication is ordinary matrix multiplication.',
 'Matrix.diagonal w has diagonal entry w_i and every off-diagonal entry zero. The matrix 1 is the identity on its displayed finite index set. Scalar multiplication, subtraction and finite sums have their usual real matrix meanings.',
 'All matrix norms use the real Euclidean L2 operator norm of the displayed matrix action; they are not entrywise or coordinate sup norms. This norm has the standard finite-coordinate topology.',
 'The integral notation is the Bochner integral in the displayed space. It is totalized to zero when its integrand is not integrable. Reconstruct the literal assertions as displayed; do not add an integrability hypothesis or conclusion.',
 'A local function G from the sample space to Prop defines a condition on a sample. The arrow following G omega is logical implication, with all subsequent conjunctions under its scope.'
]
common='For natural d,q satisfying2q+1<d, put r=q+1, including q=0. Use Omega=(R^d)^r and the original product mu of r independent standard d-dimensional Gaussian column laws. Phi_i is the physical row with coordinates omega(b)_i. Put theta_i=(i-1/2)pi/d, t_i=(1,sqrt(2)cos(theta_i),...,sqrt(2)cos(q theta_i)), L=2r+3log(1000d), and w_i=cos((2q+1)theta_i). Define Yi=d^(-1)(Phi_i Phi_i^T tensor t_i t_i^T) on norm(Phi_i)^2<=L and zero otherwise; Mi is its actual Bochner integral under the same original unconditional mu, Zi=Yi-Mi. Put a=r^(-1) integral norm(x)^2 times the inclusive cutoff indicator under the standard r-dimensional Gaussian. Define the actual d by r^2 matrix B by B_(i,(b,k))=sqrt(d)^(-1) Phi_i(b)t_i(k), with Gaussian index first, and let G be the event that every actual row satisfies its inclusive cutoff. '
texts=[common+'For every original sample omega in G, sum_i Zi(omega)=B(omega)^T B(omega)-a I_(r^2), and sum_i wi Zi(omega)=B(omega)^T diag(w) B(omega). These are the two actual eventwise centered Gram identities of Ex125. No probability of G or concentration event is asserted.',
 common+'Authored private deterministic generalization of the Ex126 implication: for every real threshold Delta and every original sample omega, if omega belongs to G and both norm(sum_i Zi(omega))<=Delta and norm(sum_i wi Zi(omega))<=Delta, then norm(B(omega)^T B(omega)-I_(r^2))<=Delta+(1-a) and norm(B(omega)^T diag(w) B(omega))<=Delta. Norms are real Euclidean operator norms. The source numeric positive threshold is one instance; the private generalization quantifies over all real thresholds, with negative-threshold antecedents impossible. No event probability or new public API is claimed.']
ids=['ASTIS-RT-20261113-HuanjianGaussianSourceGramRealization','ASTIS-RT-20261113-HuanjianGaussianSourceGramRealizationPrivateConsumer']
audits=[]
for i,k in enumerate(['producer','actual_private_consumer']):
 x=seal[k];p=Path(x['planned_file']);sig=x['signature'];assert sig in p.read_text()
 name=x['name'] if i==0 else '_private.Tests.GaussianComplexityFixedSpectrumSourceGramRealization.0.'+x['name']
 statement='∀ '+sig.replace(' :\n',' ,\n',1)
 a={'id':ids[i],'state':'draft','source':{'source_id':'c2-actual-centered-gram-realization' if i==0 else 'c2-private-deterministic-gram-deviation-generalization','anchor':'AppendixC.2 p17 Ex125/126, with original p1/frame/cutoff/actualmean definitions; private all-real-threshold scope explicitly authored generalization','original_text':texts[i],'text_sha256':rt.sha256_text(texts[i])},'lean':{'declaration':name,'file':str(p),'statement':statement,'statement_sha256':rt.sha256_text(statement),'compiled':True,'formalizer':'huanjian_gc_20261113_source_gram_realization','decoder_context':context},'repairs':[],'source_review':{'state':'pending'},'verdict':'pending','candidate_commit':'60ec0e083261dfa71f009bdd5d8c9e63b1425bb7'}
 assert not rt._core._decoder_context_violations(a)
 audits.append(a)
create(Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-gram-realization.json'),audits[0])
create(W/'private-consumer-audit.draft.json',audits[1]);create(W/'private-consumer-registry.draft.json',{'schema_version':1,'audits':[audits[1]]})
print(json.dumps({'draft_audits':2,'statement_hashes':[a['lean']['statement_sha256'] for a in audits],'private_scope':'Explicit authored deterministic generalization, no public/probability credit','new_semantic_verdicts':0}))
