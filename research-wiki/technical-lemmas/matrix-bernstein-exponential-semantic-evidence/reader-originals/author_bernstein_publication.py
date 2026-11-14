"""Author one real deterministic lemma and its fully scoped actual Gaussian use."""
from pathlib import Path
import hashlib, json, sys
sys.path.insert(0, 'tools')
import astis_publication as pub

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
P = Path('AutoSamplingTheory/TechnicalLemmas/Probability/MatrixBernsteinExponential.lean')
T = Path('Tests/GaussianComplexityBernsteinMgf.lean')
ident = 'huanjian-matrix-bernstein-exponential'
decl = 'AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential.bernstein_exponential_quadratic_bound'
cell = 'ASTIS-SHARED-MATRIX-BERNSTEIN-EXPONENTIAL-QUADRATIC'
A = Path('research-wiki/semantic-roundtrip/audits') / (ident + '.json')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)

source = {'url': 'https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf#page=25',
          'edition': 'Author preprint revised15June2011; pinned PDF SHA256 f4c3cff8661011395e793972a1f8d9a199fae4ca0fd098535d7a42166cf8fc86',
          'anchor': 'Lemma6.7 deterministic proof p25; expectation step p26; standing regularity and functional calculus §2.2-2.3 p7-8',
          'label': 'Tropp, bounded Bernstein MGF: real deterministic proof component',
          'wording_status': 'faithful paraphrase',
          'attribution': 'Joel A. Tropp, User-Friendly Tail Bounds for Sums of Random Matrices, author preprint revised15June2011.',
          'scope': 'Only the real finite-nonempty deterministic exponential-quadratic component. Tropp is independently matched external background, not a citation supplied by the Gaussian paper.'}
statement = 'A self-adjoint real matrix bounded above by the identity satisfies the exponential quadratic bound for every positive parameter.'
formula = r'A=A^\top,\quad A\preceq I,\quad s>0\quad\Longrightarrow\quad e^{sA}\preceq I+sA+(e^s-s-1)A^2.'
assumptions = [
    r'The public result concerns a real square matrix on any finite nonempty index set. The order \(U\preceq V\) means that \(V-U\) is positive semidefinite as a full quadratic form. The matrix exponential is the matrix-algebra power series.',
    r'The public mathematical hypotheses are precisely \(A=A^\top\), \(I-A\succeq0\), and \(s>0\). The cap is one-sided; negative eigenvalues are unrestricted. Finite enumeration and decidable equality supply the Lean matrix index structure.',
    r'Private actual-use scope: take \(d,q\in\mathbb N\), \(2q+1<d\), \(r=q+1\), \(\Omega=(\mathbb R^d)^r\), and the original unconditional measure \(\mu=\gamma_d^{\otimes r}\), where \(\gamma_j=N(0,I_j)\). The case \(q=0\) is included.',
    r'For source indices \(i=1,\ldots,d\), let \(\Phi_i=(\omega_b(i))_{b=0}^q\), \(\theta_i=(i-\tfrac12)\pi/d\), \(t_i=(1,\sqrt2\cos\theta_i,\ldots,\sqrt2\cos(q\theta_i))\), and \(L=2r+3\log(1000d)\). Lean uses source index \(i.val+1\).',
    r'Set \(Y_i=d^{-1}(\Phi_i\Phi_i^\top\otimes t_it_i^\top)\mathbf1_{\{\|\Phi_i\|^2\le L\}}\), \(M_i=\int Y_i\,d\mu\), \(Z_i=Y_i-M_i\), \(\rho=2r(L+1)/d\), and \(X_i=\rho^{-1}Z_i\). The paired matrix index lists the Gaussian coordinate first and the feature coordinate second. Norms use the real Euclidean operator norm with its standard Borel structure.',
    r'For this private consumer, the sole dimension hypothesis and these literal definitions determine every object. Positivity of \(\rho\), centering, Hermitian structure, measurability, integrability and the spectral cap are proved internally. All expectations use the same original \(\mu\); no all-row good event or conditional law is introduced.'
]
boundary = 'Public P is the real deterministic proof component of Tropp Lemma6.7. The final three steps give one complete private authored actual-Gaussian normalized single-summand MGF specialization, with no public consumer API or separate canonical node credit. The cosine-weighted application is still unimplemented. There is no sum-tail or event-probability conclusion, no Lieb/master-tail/full matrix Bernstein/FactC6/Lemma4.4/main lowerbound completion, and no oracle/TV/precision/dimension-condition-number/worst-query-cap/expected-cost adapter or serialized main/site/purification acceptance.'
pl = P.read_text().splitlines(keepends=True)
tl = T.read_text().splitlines(keepends=True)
def step(title, text, formula, lines, lo, hi):
    return {'title': title, 'text': text, 'formula': formula, 'lean': ''.join(lines[lo-1:hi])}
steps = [
    step('Expand the scalar remainder without dividing at zero',
         'The source leaves monotonicity of the removable scalar remainder as a calculus exercise. Apply the fundamental theorem of calculus and integration by parts to the exponential. The resulting integral identity holds for every real k, including zero.',
         r'e^k-1-k=k^2K(k),\qquad K(k)=\int_0^1(1-t)e^{kt}\,dt.', pl, 1, 56),
    step('Prove monotonicity on the whole real line',
         'On the interval of integration, both t and1−t are nonnegative. The exponential integrand therefore increases with k. Also K(0)=1/2. The source remainder equals s²K(sx) at every real x, including its specified value at zero. Since s>0, it is increasing across negative, zero and positive x.',
         r'f_s(x)=\begin{cases}(e^{sx}-sx-1)/x^2,&x\ne0,\\s^2/2,&x=0,\end{cases}\qquad f_s(x)=s^2K(sx),\quad f_s(x)x^2=e^{sx}-sx-1.', pl, 57, 104),
    step('Use only the upper scalar cap',
         'For every x≤1, multiply f_s(x)≤f_s(1) by the nonnegative x² and rearrange. This requires no lower bound on x. The same inequality holds at x=0 with the removable value already proved.',
         r'x\le1\Longrightarrow e^{sx}\le1+sx+(e^s-s-1)x^2.', pl, 105, 112),
    step('Transfer the scalar comparison to the same self-adjoint matrix',
         'The matrix cap places its real spectrum below1. Continuous functional calculus transfers the scalar inequality on that spectrum. Expand the polynomial side and identify the exponential functional calculus with the convergent matrix-algebra exponential. This is a scalar comparison on one matrix; operator monotonicity of the exponential is not used.',
         r'\sigma(A)\subset(-\infty,1]\quad\Longrightarrow\quad e^{sA}\preceq I+sA+(e^s-s-1)A^2.', pl, 113, 148),
    step('Normalize the actual original Gaussian summand',
         'The complete private module first proves three spectral adapters: a Hermitian matrix of norm at most1 has upper cap1; that cap bounds the norm of exp(sA) by exp(s); and I+C≼exp(C) holds for every Hermitian C. Then retain the literal Gaussian experiment and actual Bochner means. The canonical radius and centered-structure results give the two source norm bounds and centering. Derive the positive source radius and the normalized cap internally.',
         r'\|Y_i\|\le\frac{2rL}{d},\quad\|M_i\|\le\frac{2r}{d}\quad\Longrightarrow\quad\|Z_i\|\le\rho=\frac{2r(L+1)}d>0,\quad\|X_i\|\le1,\quad X_i=X_i^\top,\quad X_i\preceq I.', tl, 1, 167),
    step('Discharge the expectations and second-moment meaning',
         'The canonical centered structure yields measurable, integrable, zero-mean X_i. Measurability and the uniform bounds make X_i² and exp(sX_i) Bochner integrable. Each square is positive semidefinite, so the canonical positive-integral theorem gives the same property for its actual expectation. Thus C is positive semidefinite and hence Hermitian. This is an internal fact; the preceding generic inequality I+C≼exp(C) needs only Hermitian C.',
         r'\mathbb E_\mu X_i=0,\quad\|X_i^2\|\le1,\quad\|e^{sX_i}\|\le e^s,\qquad g=e^s-s-1\ge0,\quad C=g\,\mathbb E_\mu X_i^2\succeq0.', tl, 168, 199),
    step('Integrate the quadratic bound and close the individual MGF comparison',
         'Apply the public bound pointwise to the same actual X_i. The difference is positive semidefinite and integrable, so its actual expectation is positive semidefinite. Finite linearity and the derived zero mean remove the linear term. Finally add the two positive semidefinite differences for the expectation bound and I+C≼exp(C). This proves the private individual comparison for every s>0 and each i under the original measure.',
         r'\mathbb E_\mu e^{sX_i}\preceq I+g\,\mathbb E_\mu X_i^2\preceq e^{g\mathbb E_\mu X_i^2},\qquad e^C-\mathbb E_\mu e^{sX_i}=(e^C-I-C)+(I+C-\mathbb E_\mu e^{sX_i})\succeq0.', tl, 200, 240)
]
assert ''.join(x['lean'] for x in steps[:4]) == P.read_text()
assert ''.join(x['lean'] for x in steps[4:]) == T.read_text()
private_parents = [decl,
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds',
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure',
    'AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef']
unit = {'kind': 'theorem', 'reading_layout': 'progressive', 'declaration': decl,
        'title': 'Real matrix exponential quadratic bound',
        'reader_note': 'The first four steps prove the public deterministic inequality. The last three give its complete private actual-Gaussian individual MGF consumer; they do not assert a Bernstein sum tail.',
        'statement': statement, 'formula': formula, 'assumptions': assumptions, 'steps': steps,
        'astis_dependencies': [],
        'mathlib_dependencies': ['intervalIntegral.integral_eq_sub_of_hasDerivAt', 'intervalIntegral.integral_mul_deriv_eq_deriv_mul_of_hasDerivAt', 'intervalIntegral.integral_mono_on', 'CFC.le_one_iff', 'cfc_mono', 'cfc_comp_const_mul', 'CFC.real_exp_eq_normedSpace_exp', 'cfc_add', 'cfc_mul', 'Matrix.le_iff'],
        'dependency_notes': 'P calls no pre-existing ASTIS declaration; its seven private lemmas and two private scalar definitions are internal implementation support. The actual private consumer materially calls exactly P, actualSourceRadius, actualCenteredStructure and the canonical PSD Bochner-integral theorem. Its additional Mathlib adapters include norm_cfc_le, NormedSpace.exp_analytic, Integrable.of_bound, integral_smul/integral_add/integral_sub, and Real.add_one_le_exp. Source-derived and future-use edges remain distinct from those actual compiled parents.',
        'lean_statement': 'Exact generic real finite-nonempty Hermitian/upper-cap/positive-s bound, with the complete private actual-use statement retained in step5.',
        'lean_proof': 'Four folds preserve all148 public-file lines; three further folds preserve all240 private-file lines exactly once.',
        'boundary': boundary,
        'sources': [source,
            {'path': str(P), 'line': 116, 'label': 'Exact public deterministic matrix theorem', 'scope': 'Public real deterministic component only.'},
            {'url': 'https://arxiv.org/html/2610.20492v1#A3.Ex112', 'label': 'Original Gaussian source radius and normalization', 'scope': 'Literal Gaussian definitions and R_*; source Ex121 invokes Bernstein without supplying the Tropp citation.'},
            {'path': str(T), 'line': 54, 'label': 'Complete private actual-Gaussian individual MGF consumer', 'scope': 'Authored original-experiment specialization; no probability or separate public-node credit.'}],
        'tests': ['lake build Tests.GaussianComplexityBernsteinMgf']}
create(Path('website/content/declaration_lessons') / (ident + '.json'), dump({'schema_version': 1, 'units': [unit]}))
binding = {'declaration': decl, 'cell': cell, 'role': 'proof-edge',
           'supports': ['real-deterministic-exponential-quadratic'], 'boundary': boundary,
           'audit_id': 'ASTIS-RT-20261114-HuanjianMatrixBernsteinExponential',
           'assumption_deltas': [
               {'source': 'The proof of Lemma6.7 uses the deterministic cap X≼I for self-adjoint matrices in a complex finite-dimensional setting.',
                'lean': 'A is real Hermitian on any finite nonempty index set, with full PSD(I-A) and s>0.',
                'classification': 'API-limitation', 'reason': 'The explicit real restriction is sufficient for the actual Gaussian matrices. This binding covers the deterministic component, not the full complex random theorem.'},
               {'source': 'The scalar remainder has value s²/2 at zero and is increasing on the real line.',
                'lean': 'The integral representation proves this across all real arguments, including negative eigenvalues and zero.',
                'classification': 'same', 'reason': 'No two-sided norm cap or PSD(A) assumption replaces the one-sided source cap.'},
               {'source': 'Gaussian source summands are actually centered, bounded by R_*, and live under their original law.',
                'lean': 'The private consumer keeps sole hq and the literal original definitions, derives rho positivity and all regularity/cap/centering/PSD adapters inside its proof.',
                'classification': 'source-implicit', 'reason': 'The auxiliary MGF specialization is explicitly authored and private. Proof ingredients are not new Gaussian theorem premises.'}]}
item = {'id': ident, 'library': 'samplewiki', 'chapter': 'gaussian-sampling-complexity',
        'chapter_path': 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html',
        'title': unit['title'], 'source': source, 'statement': statement,
        'formulae': [{'label': 'One-sided real matrix exponential quadratic bound', 'tex': formula}],
        'assumptions': assumptions,
        'obligations': [{'id': 'real-deterministic-exponential-quadratic', 'label': 'Real deterministic component used in the individual matrix MGF proof.'}],
        'bindings': [binding]}
create(Path('website/content/publications') / (ident + '.json'), dump({'schema_version': 1, 'items': [item]}))

hp = Path('.astis/huanjian-gc-source-matrix-structure-20261113/source_span_helpers.exact-prefix.original.py')
ns = {}
exec(compile(hp.read_bytes(), str(hp), 'exec'), ns)
create(W / 'source_span_helpers.reused.original.py', hp.read_bytes())
primary, mapping = ns['primary'], ns['mapping']
pdf = Path('.astis/semantic-neutral-20261113/bernstein_raw_intake_74ab/Tro11-User-Friendly-preprint.pdf')
def pdfpage(page, region):
    p = W / ('Tropp-pdf-page-' + str(page) + '.text.txt')
    return {'origin': 'INDEPENDENTLY_MATCHED_EXTERNAL_PRIMARY', 'file': str(pdf),
            'file_sha256': sha(pdf.read_bytes()), 'printed_page': page, 'region': region,
            'derived_page_text': str(p), 'derived_page_text_sha256': sha(p.read_bytes()),
            'qualification': 'Extracted page text is a derivative locator, not a PDF byte range; the pinned visual PDF page remains primary.'}
maps = [
    mapping([pdfpage(25, 'Lemma6.7 remainder definition and calculus sentence')], [(P, 1, 56)], 'FTC and integration by parts discharge the omitted scalar calculus step through an all-real integral identity.', 'INTERNAL_EXPANSION_OF_SOURCE_CALCULUS'),
    mapping([pdfpage(25, 'f(0), f increasing, f(x)<=f(1) for x<=1')], [(P, 57, 104)], 'Exact removable value and global monotonicity, including negative and zero arguments.', 'SOURCE_SCALAR_REMAINDER'),
    mapping([pdfpage(25, 'final deterministic exponential bound')], [(P, 105, 112)], 'One-sided scalar quadratic comparison for all x<=1.', 'SOURCE_DETERMINISTIC_SCALAR_COMPONENT'),
    mapping([pdfpage(25, 'spectral transfer and deterministic exponential bound')], [(P, 113, 148)], 'Real continuous functional calculus and matrix-series exponential bridge implement the source deterministic comparison.', 'EXPLICIT_REAL_RESTRICTION_OF_SOURCE_COMPONENT'),
    mapping([primary('A3.Ex107'), primary('A3.SS2.p13.1'), primary('A3.Ex112'), pdfpage(26, 'expectation and I+C<=exp(C) step')], [(T, 1, 167)], 'Generic spectral support and literal actual Gaussian experiment; existing canonical parents supply original radius and structure, normalization derived internally.', 'AUTHORED_ACTUAL_GAUSSIAN_NORMALIZATION'),
    mapping([primary('A3.Ex107'), primary('A3.Ex112'), pdfpage(7, 'standing expectation/regularity conventions'), pdfpage(26, 'expectation of the semidefinite bound')], [(T, 168, 199)], 'Derive actual measurability, integrability, zero mean, square PSD and covariance PSD under original mu.', 'AUTHORED_INTERNAL_ANALYTIC_APPLICABILITY'),
    mapping([pdfpage(26, 'completion of Lemma6.7'), primary('A3.Ex121')], [(T, 200, 240)], 'Pointwise P and canonical PSD expectation prove individual MGF specialization; Ex121 is a downstream use context, not an assertion that its sum tail is proved.', 'PRIVATE_INDIVIDUAL_MGF_SPECIALIZATION_ONLY')
]
record = {'kind': 'Authored source-to-code map, not an independent source verdict',
          'pinned_primary_pdf_sha256': sha(pdf.read_bytes()), 'pinned_Gaussian_HTML_sha256': sha(ns['raw']),
          'mappings': maps, 'code_files': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in [P, T]],
          'canonical_P_parents': [], 'private_T_parents': private_parents,
          'source_graph_boundary': 'Independent raw source graph plus distinct topology challenge preserved separately. Source and conceptual topology are not compiled implications.',
          'external_attribution': 'Tropp is independently matched external primary background, never falsely supplied as a Gaussian-paper citation.',
          'remaining_boundary': boundary}
create(E / 'source-lean-map.authored-v1.json', dump(record))
data = pub.inputs()
live = next(x for x in pub.load() if x['id'] == ident)
b = live['bindings'][0]
ctx = pub.review_context(live, b, data)
bh = pub.binding_digest(live, b, data)
a = json.loads(A.read_bytes())
a['publication_binding_sha256'] = bh
a['publication_context'] = ctx
A.write_bytes(dump(a))
create(W / 'candidate-publication-context.v1.json', dump({'publication_binding_sha256': bh, 'publication_context': ctx}))
ta = json.loads((W / 'private-consumer-audit.draft.json').read_bytes())
tctx = {'canonical_public_producer_context': ctx,
        'private_consumer': {'file': str(T), 'file_sha256': sha(T.read_bytes()), 'whole_module_text': T.read_text(),
                             'statement_sha256': ta['lean']['statement_sha256'],
                             'placement': 'Private authored actual-Gaussian individual MGF specialization only'},
        'source_lean_correspondence': record}
ta['publication_context'] = tctx
ta['publication_binding_sha256'] = sha(json.dumps(tctx, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
create(W / 'private-consumer-audit.bound.v1.json', dump(ta))
create(W / 'private-consumer-registry.bound.v1.json', dump({'schema_version': 1, 'audits': [ta]}))
mirror = {'status': 'none-found', 'discovery_ids': [],
          'checked_sources': ['Libraries/conceptual-mirror-protocol.json', 'website/content/graph_memory_index.json', 'website/content/functor_hypergraph.json', 'Libraries/frontloaded-shared-spine.json', 'runs/substantive_discoveries.jsonl'],
          'checked_mechanism': 'All-real scalar exponential remainder, same-matrix spectral transfer, positive Bochner expectation and actual Gaussian radius normalization.',
          'finding': 'This packet directly instantiates existing scalar/CFC/PSD-integral mechanisms in one matrix algebra and one literal probability experiment. No new independently sourced cross-domain hypothesis/estimate/conclusion transport was found; the future weighted application is planned reuse of the SAME compiled P node.',
          'failure_boundaries': ['Self-adjointness is needed by the spectral comparison.', 'The one-sided upper cap and s>0 are retained.', 'Scalar monotonicity on one spectrum is not exponential operator monotonicity.', 'The actual MGF consumer needs its actual original law and internally proved integrability/centering/radius; a changed mean or conditional law changes the proposition.', 'An individual MGF does not itself give the sum-tail/master bound.'],
          'independent_review': 'Pending independent source/reader review; no self-validation.'}
create(E / 'conceptual-mirror-audit.authored-v1.json', dump(mirror))
print(json.dumps({'public_lines': len(pl), 'private_lines': len(tl), 'exact_full_source_folds': len(steps),
                  'P_binding_sha256': bh, 'T_binding_sha256': ta['publication_binding_sha256'], 'new_semantic_verdicts': 0}))
