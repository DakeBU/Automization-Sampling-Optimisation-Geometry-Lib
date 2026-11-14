"""Author the stable R10 candidate mathematics and draft audits, without review verdicts."""
from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixRadius.lean')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixRadius.lean')
decl='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds'
tdecl='_private.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius.0.AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius.actual_source_centered_summand_radius'
cell='ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius'
ident='huanjian-gaussian-source-matrix-radius'
auditid='ASTIS-RT-20261113-HuanjianGaussianSourceMatrixRadius'
tauditid='ASTIS-RT-20261113-HuanjianGaussianSourceMatrixRadiusPrivateConsumer'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def create(p,o):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(dump(o))
anchor='Appendix C.2 p13 Ex111-112; literal p1 product experiment, Ex107 cutoff, p12 actual mean, Fact C.5 frame'
source={'url':'https://arxiv.org/html/2610.20492v1#A3.SS2.p13','edition':'arXiv:2610.20492v1; pinned HTML SHA256 6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915','anchor':anchor,'wording_status':'faithful paraphrase','attribution':'On Complexity of Gaussian Sampling, arXiv:2610.20492v1.','scope':'Public uncentered summand and actual mean operator norms; centered and cosine-weighted radius is a separately labelled private consumer.'}
assumptions=[
 r'Let \(d,q\in\mathbb N\) satisfy \(2q+1<d\), and put \(r=q+1\). This includes \(q=0\). Positivity of \(d,r,L\) is derived internally.',
 r'Use the original space \(\Omega=(\mathbb R^d)^r\) with \(\mu=\gamma_d^{\otimes r}\), where \(\gamma_j=N(0,I_j)\). The physical row is \(\Phi_i(\omega)=(\omega_{1,i},\ldots,\omega_{r,i})\).',
 r'Put \(\theta_i=(i-\tfrac12)\pi/d\), \(t_i=(1,\sqrt2\cos\theta_i,\ldots,\sqrt2\cos(q\theta_i))\), and \(L=2r+3\log(1000d)\). Source index \(i\) is Lean index \(i.val+1\).',
 r'Define \(Y_i=d^{-1}(\Phi_i\Phi_i^\top\otimes t_it_i^\top)\mathbf1_{\{\|\Phi_i\|^2\le L\}}\). The cutoff is inclusive and row-specific. The Gaussian coordinate comes first in the paired matrix index.',
 r'Norms are the real Euclidean operator norm of the \(r^2\times r^2\) matrices. Expectations are actual Bochner integrals on the same original \(\mu\); the existing actual-mean theorem proves integrability internally.',
 r'The only proposition input is \(2q+1<d\). The feature bound, retained-moment coefficient \(0\le a\le1\), rank-one norm identities and actual mean estimate are proved inside the proof, with no certificate assumptions.'
]
boundary='Public P proves the actual pointwise truncated-summand norm and actual-mean norm only. Its private Tests consumer proves centered and cosine-weighted centered radius 2r(L+1)/d in the same literal experiment, including q=0. The private theorem is not a public API or separate canonical node. Matrix concentration, full Lemma4.4, both main lower bounds, exact oracle/precision/TV/dimension-condition-number/worst-query-cap/expected-cost adapters, serialized main/site/source-index/globalgraph integration and purification are separate obligations.'
formula=r'\|Y_i(\omega)\|_{\rm op}\le\frac{2rL}{d},\qquad\|\mathbb E_\mu Y_i\|_{\rm op}\le\frac{2r}{d}\quad(1\le i\le d,\ \omega\in\Omega).'
statement='Every actual truncated Gaussian summand and its actual mean satisfy the two operator-norm bounds.'
pl=P.read_text().splitlines(keepends=True);tl=T.read_text().splitlines(keepends=True)
def step(title,text,formula,lines,a,b):return {'title':title,'text':text,'formula':formula,'lean':''.join(lines[a-1:b])}
steps=[
 step('Identify the actual Euclidean operator norms', 'Identify a real outer-product matrix with its canonical Euclidean rank-one continuous map. Flatten the tensor of two outer products to the outer product of the paired vector. For an identity tensor feature outer product, use its symmetric square identity and a nonzero diagonal witness; the zero feature is handled separately. Nonemptiness needed by this generic identity holds automatically for the actual positive size r.',r'\|uu^\top\|=\|u\|^2,\quad\|uu^\top\otimes vv^\top\|=\|u\|^2\|v\|^2,\quad\|I_r\otimes tt^\top\|=\|t\|^2.',pl,1,100),
 step('Retain the literal experiment and derive the coefficient range', 'Use the canonical cosine frame to bound the squared feature norm. The actual first-moment theorem gives integrability and the precise radial mean. The retained scalar squared radius lies pointwise between zero and the full Gaussian squared radius; integrating and using the canonical second moment yields 0≤a≤1. These are internal deductions under the original source condition.',r'S_i=\|t_i\|^2\le2r,\quad a=\frac1r\int\|x\|^2\mathbf1_{\{\|x\|^2\le L\}}d\gamma_r\in[0,1],\quad\mathbb E_\mu Y_i=\frac ad(I_r\otimes t_it_i^\top).',pl,101,196),
 step('Bound the truncated summand on both cutoff branches', 'On the retained event apply the exact paired rank-one norm and the feature bound. Outside the closed retained event the actual summand is zero. Derived positivity makes the same upper bound valid on both branches.',r'\|Y_i\|=\frac{\|\Phi_i\|^2S_i}{d}\mathbf1_{\{\|\Phi_i\|^2\le L\}}\le\frac{2rL}{d}.',pl,197,216),
 step('Evaluate and bound the actual mean norm', 'Apply the identity-tensor rank-one norm to the evaluated actual Bochner mean. Use the internally derived coefficient range and feature bound.',r'\|\mathbb E_\mu Y_i\|=\frac{aS_i}{d}\le\frac{2r}{d}.',pl,217,226),
 step('Consume both estimates in the actual centered radius', 'The complete private consumer defines Mi as the actual integral of Yi and Zi=Yi−Mi on the same original product measure. Triangle inequality and both public estimates give the exact source Rstar. No arbitrary mean, replacement law or norm certificate is supplied.',r'M_i=\mathbb E_\mu Y_i,\quad Z_i=Y_i-M_i,\qquad\|Z_i\|\le\frac{2rL}{d}+\frac{2r}{d}=R_*:=\frac{2r(L+1)}d.',tl,1,84),
 step('Retain the radius after the deterministic cosine weight', 'In the same private theorem use the deterministic source frequency n=2q+1 and |cos(nθi)|≤1. The weighted and unweighted assertions hold for every sample, including samples outside the row cutoff.',r'w_i=\cos((2q+1)\theta_i),\qquad\|w_iZ_i\|=|w_i|\|Z_i\|\le R_*.',tl,85,95)
]
assert ''.join(x['lean'] for x in steps[:4])==P.read_text()
assert ''.join(x['lean'] for x in steps[4:])==T.read_text()
parents=['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram','AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian']
mathlib=['Matrix.cstar_norm_def','InnerProductSpace.norm_rankOne','InnerProductSpace.symm_toEuclideanLin_rankOne','Matrix.l2_opNorm_conjTranspose_mul_self','Matrix.conjTranspose_kronecker','Matrix.mul_kronecker_mul','EuclideanSpace.norm_sq_eq','MeasureTheory.Integrable.indicator','MeasureTheory.integral_mono','MeasureTheory.integral_nonneg']
unit={'kind':'theorem','reading_layout':'progressive','declaration':decl,'title':'Actual Gaussian summand and mean operator norms','reader_note':'The main statement is the public summand/mean producer. The final two proof steps contain its complete private centered and cosine-weighted radius consumer, under the same source condition.','statement':statement,'formula':formula,'assumptions':assumptions,'steps':steps,'astis_dependencies':parents,'mathlib_dependencies':mathlib,'dependency_notes':'P materially calls exactly the three listed canonical ASTIS parents. Its three private representation/algebra helpers share the public module review and create no extra public node. Private T calls P only; triangle inequality, norm_smul and Real.abs_cos_le_one discharge its remaining estimates. These are not additional P parents.','lean_statement':statement,'lean_proof':'Four source-ordered steps reproduce the entire public module, followed by two steps reproducing the entire private consumer.','boundary':boundary,'sources':[source,{'path':str(P),'line':101,'label':'Complete exact public summand/mean theorem','scope':boundary},{'url':'https://arxiv.org/html/2610.20492v1#A3.Ex112','label':'Exact centered radius and following cosine-weighted bound','scope':'Private consumer only.'},{'path':str(T),'line':17,'label':'Complete exact private centered/weighted consumer','scope':'Private real consumer; no separate public declaration credit.'}],'tests':['lake build Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius']}
create(Path('website/content/declaration_lessons')/(ident+'.json'),{'schema_version':1,'units':[unit]})
binding={'declaration':decl,'cell':cell,'role':'proof-edge','supports':['c2-actual-summand-mean-operator-norms'],'boundary':boundary,'audit_id':auditid,'assumption_deltas':[{'source':'Original independent standard Gaussian columns, natural q≥0 and2q+1<d, actual rows, exact midpoint features and inclusive local cutoff.','lean':'Literal original product experiment and exact same row matrices, including q=0; sole hq proposition input.','classification':'same','reason':'No alternate experiment, extra query restriction, norm/moment/mean/frame certificate or source assumption is introduced.'},{'source':'Ex111 uses the actual radial mean and 0≤a≤1, the feature estimate, and exact real operator norms.','lean':'Canonical mean and second-moment results are consumed internally; all needed signs, nonemptiness, coefficient range and norm identities are proved internally.','classification':'source-implicit','reason':'Proof ingredients are discharged inside the proof, not added as caller hypotheses. The actual mean provider establishes integrability, avoiding any use of a totalized nonintegrable integral.'}]}
item={'id':ident,'library':'samplewiki','chapter':'gaussian-sampling-complexity','chapter_path':'example-cases/samplewiki/companions/gaussian-sampling-complexity.html','title':unit['title'],'source':source,'statement':statement,'formulae':[{'label':unit['title'],'tex':formula}],'assumptions':assumptions,'obligations':[{'id':'c2-actual-summand-mean-operator-norms','label':statement}],'bindings':[binding]}
create(Path('website/content/publications')/(ident+'.json'),{'schema_version':1,'items':[item]})
context=[
 'Fin n is the finite index set of natural numbers less than n. Natural numbers embed into real numbers in the usual way.',
 'EuclideanSpace real (Fin n) is real n-dimensional Euclidean space with its Euclidean norm and Borel structure. WithLp.toLp 2 wraps a coordinate function as that vector and WithLp.ofLp recovers its same coordinates.',
 'stdGaussian on finite-dimensional real Euclidean space is the centered Gaussian probability law with identity covariance. Measure.pi is the finite product measure with its product measurable structure.',
 'Real.log is the natural logarithm and Real.sqrt the nonnegative square root. The displayed less-than-or-equal branch includes equality.',
 'Matrix.vecMulVec u v has entry u_i times v_j. Matrix.kronecker A B at row (i,j) and column (k,l) has entry A_(i,k) times B_(j,l). Scalar multiplication and subtraction have their ordinary real matrix meaning.',
 'Every displayed matrix norm is the real Euclidean operator norm, namely the norm of its action between the Euclidean spaces on the displayed paired index set, not an entrywise or supremum norm.',
 'Matrix expectations are Bochner integrals. This integral is totalized to zero when its integrand is not integrable; the displayed proposition must be reconstructed as written, without adding an integrability premise or assertion.'
]
common='For all natural d,q with 2q+1<d put r=q+1. On the original r independent standard d-dimensional Gaussian columns with product probability mu, let Phi_i be their actual physical row. Put theta_i=(i-1/2)pi/d, t_i=(1,sqrt(2)cos(theta_i),...,sqrt(2)cos(q theta_i)), and L=2r+3log(1000d). Define Yi=d^(-1)(Phi_i Phi_i-transpose tensor t_i t_i-transpose) on the inclusive event norm(Phi_i)^2<=L and zero otherwise. All matrix norms are real Euclidean operator norms and means are actual Bochner integrals under mu. The case q=0 is included. '
ptext=common+'For every i and every sample omega, norm(Yi(omega))<=2rL/d. For every i, norm(integral Yi dmu)<=2r/d. This is the public Ex111 bound only.'
ttext=common+'Let Mi be the actual integral of Yi under mu, Zi=Yi-Mi, wi=cos((2q+1)theta_i), and Rstar=2r(L+1)/d. For every i and sample omega, both norm(Zi(omega))<=Rstar and norm(wi Zi(omega))<=Rstar. This is the exact Ex112 and following weighted centered-radius consequence.'
def audit(ident,name,file,sig,text):
    statement='∀ '+sig.replace(' :\n',' ,\n',1)
    return {'id':ident,'state':'draft','source':{'source_id':'c2-actual-summand-mean-operator-norms' if name==decl else 'c2-private-centered-summand-radius','anchor':anchor,'original_text':text,'text_sha256':rt.sha256_text(text)},'lean':{'declaration':name,'file':str(file),'statement':statement,'statement_sha256':rt.sha256_text(statement),'compiled':True,'formalizer':'huanjian_gc_20261113_source_matrix_radius','decoder_context':context},'repairs':[],'candidate_commit':'4c3251454100a4591113b16ed119fdf758c876b7'}
pa=audit(auditid,decl,P,(W/'producer-signature.unclaimed.txt').read_text(),ptext)
ta=audit(tauditid,tdecl,T,(W/'consumer-signature.unclaimed.txt').read_text(),ttext)
for a in [pa,ta]:
    assert not rt._core._decoder_context_violations(a)
create(Path('research-wiki/semantic-roundtrip/audits')/(ident+'.json'),pa)
create(W/'private-consumer-audit.draft.json',ta)
create(W/'private-consumer-registry.draft.json',{'schema_version':1,'audits':[ta]})
print(json.dumps({'authored_P_lines':len(pl),'authored_private_T_lines':len(tl),'all_exact_source_lines_preserved':True,'semantic_verdicts_written':0,'P_statement_sha256':pa['lean']['statement_sha256'],'T_statement_sha256':ta['lean']['statement_sha256']}))
