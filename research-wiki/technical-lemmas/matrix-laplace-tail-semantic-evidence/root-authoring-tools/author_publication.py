from pathlib import Path
import hashlib, json

r=Path.cwd(); w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
P='AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail.max_eigenvalue_tail_le_iInf_trace_exp'
T='AutoSamplingTheory.Tests.GaussianComplexityLaplaceTail.actual_source_four_sums_laplace_tail'
pf='AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean'
tf='Tests/GaussianComplexityLaplaceTail.lean'
commit='1d1103af694b9663a72b0d610004ed85c7c6b527'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(path,obj):
    p=r/path; p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),str(p)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
tropp={'url':'https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf#page=9',
 'edition':'Author preprint revised 15 June 2011; pinned PDF SHA256 f4c3cff8661011395e793972a1f8d9a199fae4ca0fd098535d7a42166cf8fc86',
 'anchor':'Proposition 3.1 statement p9 and proof pp9–10; §§2.1–2.4 pp7–8; §3.1 expectation-domain caveat p9',
 'label':'Tropp, matrix Laplace transform tail bound', 'wording_status':'faithful paraphrase',
 'attribution':'Joel A. Tropp, User-Friendly Tail Bounds for Sums of Random Matrices, author preprint revised 15 June 2011.',
 'scope':'Real finite-dimensional specialization with a disclosed nonnegative scalar extended-expectation domain completion. Independently matched background; no explicit Tropp citation is supplied by the Gaussian paper.'}
formula=r'\mu\{\lambda_{\max}(X)\ge t\}\le\inf_{s>0}e^{-st}\,\overline{\mathbb E}_{\mu}\operatorname{tr}e^{sX},\qquad t\in\mathbb R.'
assumptions=[
r'Let \((\Omega,\Sigma,\mu)\) be a probability space, let \(\mathcal I\) be finite and nonempty, and let \(X:\Omega\to\operatorname{Mat}_{\mathcal I}(\mathbb R)\) be almost-everywhere strongly measurable and self-adjoint almost everywhere. The threshold \(t\) is any real number.',
r'\(\lambda_{\max}\) denotes the algebraically largest real eigenvalue on the self-adjoint domain; it is not the operator norm. The trace is the ordinary unnormalized trace, and \(e^A\) is the matrix-algebra power-series exponential.',
r'The bar on \(\overline{\mathbb E}\) means a nonnegative scalar integral, permitted to be \(+\infty\). The real coefficient \(e^{-st}\) is finite and strictly positive for every \(s>0\). This is an explicit domain completion of the source inequality, not a claim that the source defines ENNReal or that every matrix MGF exists as a Bochner integral.',
r'Neither centering, independence, a norm cap nor a variance bound is a premise of the public theorem. Almost-everywhere event comparison handles the null exceptional self-adjoint set; no separate eigenbasis selector or general eigenvalue measurability theorem is claimed.',
r'For the private application let \(d,q\in\mathbb N\), \(2q+1<d\), \(r=q+1\), \(\Omega=(\mathbb R^d)^r\), and \(\mu=\gamma_d^{\otimes r}\), with \(\gamma_d=N(0,I_d)\). The case \(q=0\) remains included. Every mean and probability uses this original unconditional law.',
r'For physical rows \(i=1,\ldots,d\), set \(\alpha_i=(i-\tfrac12)\pi/d\), \(t_i=(1,\sqrt2\cos\alpha_i,\ldots,\sqrt2\cos(q\alpha_i))\), \(\Phi_i=(\omega_b(i))_{b=0}^q\), and \(L=2r+3\log(1000d)\). Lean represents physical row \(i\) by \(i.val+1\).',
r'Set \(Y_i=d^{-1}(\Phi_i\Phi_i^\top\otimes t_it_i^\top)\mathbf1_{\{\|\Phi_i\|^2\le L\}}\) and \(Z_i=Y_i-\mathbb E_\mu Y_i\). The cutoff includes equality and uses the same row; the paired index has Gaussian coordinate first, feature coordinate second. The matrices have size \(r^2\times r^2\).',
r'Choose either \(w_i=1\) or \(w_i=\cos((2q+1)\alpha_i)\), and either global sign \(\varepsilon\in\{-1,1\}\). The consumer handles all four matrices \(S=\varepsilon\sum_iw_iZ_i\), every \(s>0\) and every \(a\in\mathbb R\). Actual trace-exponential integrability and positivity are derived inside the proof. No equality of the laws or MGFs of \(S\) and \(-S\) is assumed.'
]
boundary='This packet proves the real extended-expectation Laplace-tail reduction and its private finite-Bochner-expectation application to all four literal signed Gaussian sums. It does not bound their trace MGF, prove Lieb/independent-sum master-tail or Bernstein, close C6/Lemma4.4 or either main lower bound, or supply the strict-norm union bridge, oracle/TV/precision/query-cap/expected-cost adapters. Main/site/global graph integration, purification and whole-Goal acceptance remain separate.'
def step(title,text,formula,path,lo,hi,source):
    b=(r/path).read_bytes(); txt=b.decode(); lines=txt.splitlines(keepends=True)
    start=sum(map(len,lines[:lo-1])); end=sum(map(len,lines[:hi]))
    s=txt[start:end]; bs=len(txt[:start].encode()); be=len(txt[:end].encode())
    src={'path':path,'commit':commit,'file_sha256':sha(b),'LF_lines_1based':[lo,hi],
      'decoded_char_span':[start,end],'raw_UTF8_byte_span':[bs,be],
      'span_convention':'Lines inclusive and 1-based; character/codepoint and UTF8-byte offsets 0-based half-open; newline bytes retained.',
      'start_line_column0':[lo,0],'end_exclusive_line_column0':[hi+1,0],
      'span_sha256':sha(s.encode()),'download_path':'downloads/lean/'+path,'download_filename':Path(path).name}
    return {'title':title,'text':text,'formula':formula,'lean':s,
      'lean_source_path':path,'lean_source':src,'lean_download_path':src['download_path'],
      'source_attribution':source,'scope':'public P' if path==pf else 'associated private T'}
def pdf(page,region):
    return {'origin':'INDEPENDENTLY_MATCHED_EXTERNAL_PRIMARY','file':'.astis/semantic-neutral-20261113/bernstein_raw_intake_74ab/Tro11-User-Friendly-preprint.pdf',
      'file_sha256':'f4c3cff8661011395e793972a1f8d9a199fae4ca0fd098535d7a42166cf8fc86','printed_page':page,'region':region,
      'qualification':'Printed-page locator, not a claim about a PDF byte span.'}
def gc(anchor,region):
    return {'origin':'PRIMARY','file':'.astis/huanjian-handoff-20261019/2610.20492v1.html',
      'file_sha256':'6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915',
      'url':'https://arxiv.org/html/2610.20492v1#'+anchor,'anchor':anchor,'region':region}
steps=[
step('One positive eigenvalue term is bounded by the trace',
'Diagonalize a fixed real self-adjoint matrix. Functional calculus and cyclicity of the unnormalized trace identify the trace exponential with the sum of scalar exponentials. The finite nonempty real spectrum attains its largest element, and its positive exponential is one summand. This pointwise comparison holds for every real s; positivity of s is used later to compare threshold events.',
r'\operatorname{tr}e^{sA}=\sum_{j\in\mathcal I}e^{s\lambda_j(A)}\ge e^{s\lambda_{\max}(A)}.',pf,1,52,[pdf(7,'§§2.1–2.3 spectrum, trace and scalar functional calculus'),pdf(10,'Prop3.1 proof: spectral mapping and largest eigenvalue versus trace')]),
step('Use the positive trace observable on the almost-sure domain',
'Fix s>0. Continuity of the matrix exponential and trace makes their scalar composition almost-everywhere measurable. Outside the null exceptional set, λmax(X)≥t implies exp(st)≤tr exp(sX). Compare the event measures almost everywhere. This avoids assuming a measurable eigenbasis or replacing λmax by the norm.',
r'\{\lambda_{\max}(X)\ge t\}\subseteq_{\mu\text{-a.e.}}\{e^{st}\le\operatorname{tr}e^{sX}\}.',pf,53,85,[pdf(9,'Prop3.1 fixed positive parameter and Markov reduction'),pdf(10,'Prop3.1 trace domination')]),
step('Apply scalar Markov and take the positive-parameter infimum',
'Apply nonnegative Markov to ofReal(tr exp(sX)) at the finite positive threshold exp(st). Divide by that threshold and rewrite its reciprocal as exp(−st). This combines the two elementary source comparisons by applying Markov directly to the trace exponential. Every s>0 gives a bound, so take their infimum. Infinite expectations remain valid terms and do not create a zero-times-infinity case.',
r'\mu\{\lambda_{\max}(X)\ge t\}\le e^{-st}\overline{\mathbb E}_\mu\operatorname{tr}e^{sX}\quad(s>0).',pf,86,96,[pdf(9,'Prop3.1 Markov bound and parameter optimization; §3.1 expectation caveat'),pdf(10,'Completion of Prop3.1 proof')]),
step('Keep the literal four Gaussian sums and their finite-dimensional semantics',
'The application uses the original product Gaussian experiment, inclusive own-row truncation, actual unconditional means, both deterministic weights and both global signs. Its two private analytic helpers prove an exponential norm bound from a Hermitian norm bound and nonnegativity of the trace exponential by functional calculus. Their estimates are internal proof ingredients.',
r'S=\varepsilon\sum_{i=1}^dw_iZ_i,\quad w_i\in\{1,\cos((2q+1)\alpha_i)\},\quad\varepsilon\in\{-1,1\}.',tf,1,76,[gc('A3.Ex85','Feature vectors and physical Gaussian rows'),gc('A3.Ex107','Literal truncated rank-one Kronecker matrices'),gc('A3.SS2.p13.1','Actual centering'),gc('A3.SS2.p15.2','Cosine-weighted concentration context'),pdf(7,'Scalar spectral functional calculus')]),
step('Reuse genuine source structure and radius to bound all four sums',
'The canonical source-structure parent supplies measurability and Hermiticity under the original experiment; its own mean-integrability prerequisites are already proved in its dependency closure. The source-radius parent supplies the truncated matrix and actual mean bounds. Triangle and scalar norm inequalities give a finite uniform bound for each weighted signed sum. Independence and centering from the structure package are not used by this probability reduction.',
r'\rho=\frac{2r(L+1)}d,\qquad\|Z_i\|\le\rho,\qquad\|S\|\le d\rho.',tf,77,164,[gc('A3.Ex112','Truncated radius and actual-mean norm bound'),gc('A3.SS2.p13.1','Centered matrices'),gc('A3.SS2.p15.2','Bounded cosine weighting')]),
step('Prove the actual trace expectation finite and apply the public theorem',
'For each fixed positive s, functional calculus and the uniform bound yield ||exp(sS)||≤exp(sdρ). Hence the matrix exponential is Bochner integrable, and the continuous linear trace map gives scalar trace integrability. Its nonnegativity then converts the nonnegative integral to ofReal of the actual Bochner expectation. Specialize the public infimum at this s to obtain the four-family conclusion with no integrability premise added.',
r'\|e^{sS}\|\le e^{sd\rho},\quad\operatorname{tr}e^{sS}\ge0,\quad\mu\{\lambda_{\max}(S)\ge a\}\le e^{-sa}\mathbb E_\mu\operatorname{tr}e^{sS}.',tf,165,193,[pdf(9,'Prop3.1 fixed-parameter tail reduction'),gc('A3.Ex121','Source ordinary centered-sum strict norm tail context; complete strict-norm union bound remains outside this packet'),gc('A3.SS2.p15.2','Weighted centered-sum tail context')])]
sources=[tropp,{'path':pf,'line':55,'label':'Exact public matrix Laplace-tail theorem'},
 {'path':tf,'line':44,'label':'Complete private four-family original-Gaussian application'}]
for a,lab in [('A3.Ex85','Feature and Gaussian row coordinates'),('A3.SS2.p1.2','Original Gaussian law'),('A3.SS2.p4.1','Midpoint angles'),('A3.SS2.p10.1','Truncation threshold'),('A3.Ex107','Inclusive own-row truncation'),('A3.SS2.p13.1','Actual centering'),('A3.Ex112','Radius inputs'),('A3.Ex121','Ordinary strict norm tail context'),('A3.SS2.p15.2','Weighted concentration context')]:
    sources.append({'url':'https://arxiv.org/html/2610.20492v1#'+a,'label':lab})
unit={'kind':'theorem','reading_layout':'progressive','declaration':P,'title':'Real matrix Laplace tail',
 'statement':'The largest-eigenvalue tail is bounded by the optimized expected trace exponential.',
 'formula':formula,'assumptions':assumptions,'reader_note':'The first three steps prove the public tail reduction. The last three apply it to all four literal signed Gaussian sums, deriving their finite trace expectations internally.',
 'steps':steps,'dependencies':[],
 'mathlib_dependencies':['Matrix.IsHermitian.cfc_eq','Matrix.IsHermitian.spectrum_real_eq_range_eigenvalues','Matrix.trace_mul_cycle','Matrix.trace_diagonal','Set.Nonempty.csSup_mem','Finset.single_le_sum','NormedSpace.exp_analytic','MeasureTheory.measure_mono_ae','MeasureTheory.meas_ge_le_lintegral_div','ENNReal.ofReal_inv_of_pos','Real.exp_neg'],
 'dependency_notes':'Public P has no ASTIS mathematical parent; its two private spectral helpers depend only on Mathlib. Private T directly calls P and the canonical actual_source_truncated_matrix_norm_bounds and actual_source_centered_matrix_structure. Its internal exponential bound is used only for integrability, not as a variance or Bernstein estimate. Its proof uses the actual finite Bochner expectation; no independent-sum MGF multiplication, Lieb theorem, operator monotonicity, or symmetry of signed laws is invoked.',
 'lean_statement':'Exact finite nonempty real random-matrix signature, all real thresholds and every positive Laplace parameter; the literal private four-family signature is in step4.',
 'lean_proof':'The six exact spans partition all96 public-module lines and all193 private-module lines, with imports, parameters and complete bodies retained from the frozen mathematical commit.',
 'boundary':boundary,'sources':sources,
 'tests':['lake env lean '+pf,'lake build AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail Tests.GaussianComplexityLaplaceTail']}
write('website/content/declaration_lessons/huanjian-matrix-laplace-tail.json',{'schema_version':1,'units':[unit]})
source_statement='Let X be a self-adjoint random matrix on a probability space. For every real threshold t, its largest-eigenvalue upper-tail probability is bounded by infimum over positive s of exp(−st) times the expected unnormalized trace of exp(sX). The selected formal version restricts to finite nonempty real matrices, makes almost-sure measurability/self-adjointness explicit, and permits a nonnegative scalar extended expectation as a disclosed domain completion. Tropp §3.1 notes that the matrix MGF need not exist for every parameter; the completion does not claim that all matrix MGFs are finite.'
binding={'declaration':P,'cell':'ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL','role':'proof-edge','supports':['real-spectral-laplace-tail'],
 'boundary':boundary,'audit_id':'ASTIS-RT-20261114-HuanjianMatrixLaplaceTail','assumption_deltas':[
 {'source':'A self-adjoint random matrix; ordinary trace and largest algebraic eigenvalue.',
  'lean':'Finite nonempty real matrices; AE Hermitian; sSup of the real spectrum; ordinary Matrix.trace and matrix-algebra exponential.',
  'classification':'same','reason':'Explicit real specialization. The largest eigenvalue is not replaced by the operator norm and no dimension factor is silently normalized away.'},
 {'source':'Probability and §2.2 standing regularity, with random-matrix relations understood almost surely.',
  'lean':'IsProbabilityMeasure μ, AEStronglyMeasurable X μ and AE Hermiticity.',
  'classification':'source-implicit','reason':'Continuity supplies measurable trace exponentials, and measure_mono_ae transfers the source-domain event comparison. No eigenbasis selector premise is added.'},
 {'source':'Prop3.1 expectation bound; §3.1 warns that some positive parameters can lack a matrix MGF.',
  'lean':'A nonnegative scalar lintegral valued in ENNReal; no generic Bochner-integrability premise.',
  'classification':'generalization','reason':'Disclosed extended-expectation domain completion, proved by nonnegative Markov. Infinite scalar expectations remain legitimate terms. This is not extended matrix-valued expectation or a statement that every source MGF exists.'},
 {'source':'Every real t and infimum over positive real parameters.',
  'lean':'t : ℝ and an iInf over {s : ℝ // 0<s}.',
  'classification':'same','reason':'No positivity condition on the threshold, no negative-parameter or lower-tail identification, and no minimizer-existence requirement.'}]}
item={'id':'huanjian-matrix-laplace-tail','library':'samplewiki','chapter':'gaussian-sampling-complexity',
 'chapter_path':'example-cases/samplewiki/companions/gaussian-sampling-complexity.html','title':unit['title'],'source':tropp,
 'statement':source_statement,'formulae':[{'label':'Real extended-expectation Laplace tail','tex':formula}],
 'assumptions':assumptions[:4],'obligations':[{'id':'real-spectral-laplace-tail','label':'The real largest-eigenvalue trace-exponential tail reduction, with the disclosed scalar extended-expectation completion.'}],
 'bindings':[binding]}
write('website/content/publications/huanjian-matrix-laplace-tail.json',{'schema_version':1,'items':[item]})
context=[
'The universes specify carrier levels only. The displayed measure and sigma-algebra form a probability experiment. The finite nonempty index type has a finite enumeration and decidable equality.',
'Matrix is the real finite square-matrix algebra. Multiplication and the power-series exponential NormedSpace.exp use ordinary matrix multiplication; Real.exp is scalar exponential. Matrix.trace is the unnormalized sum of diagonal entries. The topology is the Euclidean operator-norm topology.',
'For a real matrix IsHermitian means transpose equals itself. The real spectrum is the set of real scalars for which scalar identity minus the matrix is not invertible. sSup is the real conditional supremum; on the finite nonempty Hermitian spectrum it is the largest algebraic eigenvalue, with no absolute value.',
'AEStronglyMeasurable means equal almost everywhere to a strongly measurable function under the displayed measure. The AE filter and the set measure refer to that same measure, including possible null exceptional points.',
'ENNReal is the extended nonnegative reals, with top equal to positive infinity. ofReal maps a real value to its nonnegative part. The symbol lintegral is the nonnegative Lebesgue integral, allowed to be infinity. The indexed infimum runs over every positive real parameter, without asserting existence of an optimizer.'
]
ps=(w/'P.proposition.sealed.v1.txt').read_text(); ts=(w/'T.proposition.sealed.v1.txt').read_text()
def audit(ident,decl,file,stmt,source,ctx):
    return {'id':ident,'state':'draft','base_commit':'2da2ccccfd1429aab18007e06895a1eb7cc58066','candidate_commit':commit,
      'source':{'source_id':source[0],'anchor':source[1],'original_text':source[2],'text_sha256':sha(source[2].encode())},
      'lean':{'declaration':decl,'file':file,'statement':stmt,'statement_sha256':sha(stmt.encode()),
        'compiled':True,'formalizer':'huanjian_20261114_matrix_laplace_tail','decoder_context':ctx,
        'compiler_evidence':'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/local-mathematics-checkpoint.v1.json'},
      'reconstruction':{},'source_review':{'state':'pending'},'semantic_slots':{},'deltas':[],
      'verdict':'pending','repairs':[],'scope_boundary':boundary}
a=audit('ASTIS-RT-20261114-HuanjianMatrixLaplaceTail',P,pf,ps,
 ('tropp2011-real-extended-spectral-laplace-tail',tropp['anchor'],source_statement),context)
write('research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json',a)
t_context=context+[
'EuclideanSpace with Fin n is the real Euclidean space of dimension n. WithLp.toLp 2 and WithLp.ofLp change representation between Euclidean coordinates and coordinate functions, without changing those coordinates.',
'stdGaussian on a real finite-dimensional Euclidean space is the centered Gaussian probability measure with identity covariance. Measure.pi over a finite index forms its product law. Every displayed mean is a Bochner integral under that displayed unconditional product measure.',
'Matrix.vecMulVec is the outer product of the two displayed coordinate vectors. Matrix.kronecker uses ordered pairs: the first coordinate comes from its first matrix factor. The cutoff if branches use the inclusive displayed inequality and the actual zero matrix otherwise.',
'The two Boolean values are universally quantified choices. The displayed conditionals choose the deterministic weights and global scalar sign. Fin d indices range from zero through d−1 and the displayed angle includes the explicit offset.'
]
ta=audit('ASTIS-RT-20261114-HuanjianMatrixLaplaceTailPrivate',T,tf,ts,
 ('gaussian2610-literal-four-sum-laplace-intermediate','AppendixC2 Ex85/Ex107/Ex112/Ex121 and p15.2; authored Laplace intermediate',
  'For the original r=q+1 independent standard Gaussian vectors in dimension d with 2q+1<d, form the displayed inclusive own-row truncated Kronecker matrices and subtract their actual unconditional expectations. Both ordinary and cosine-weighted centered sums and both global signs have, for every positive s and every real a, largest-eigenvalue upper-tail bounded by exp(−sa) times their actual finite expected trace exponential. This is an authored intermediate for the source concentration proof, not a literal printed full Bernstein theorem.'),t_context)
ta['private_consumer']=True;ta['owner_public_declaration']=P;ta['separate_public_node']=False
write('.astis/huanjian-gc-matrix-laplace-20261114/private-consumer-audit.registry.json',{'schema_version':1,'audits':[ta]})
print(json.dumps({'lesson':sha(json.dumps(unit,ensure_ascii=False).encode()),'P_audit':'draft','T_audit':'private-draft','no_independent_verdict':True}))
