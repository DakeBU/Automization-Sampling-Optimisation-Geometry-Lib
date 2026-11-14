from pathlib import Path
import gzip, hashlib, json, sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json')
sha = lambda b: hashlib.sha256(b.encode() if isinstance(b, str) else b).hexdigest()

def put(p, x):
    p = Path(p)
    assert not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')

s = json.loads((W/'statement-seal-v1.json').read_bytes())
k = json.loads((E/'actual-kernel-owned-inventory.json').read_bytes())
P, T = [Path(s[a]['planned_file']) for a in ['producer', 'actual_private_consumer']]
pr, tr = P.read_text(), T.read_text()
name = s['producer']['name']
assert sha(P.read_bytes()) == k['actual_producer_sha256']
assert sha(T.read_bytes()) == k['actual_Test_sha256']
for text, key, marker in [(pr, 'producer', 'theorem actual_cosine_feature_krylov_range '), (tr, 'actual_private_consumer', 'private theorem actual_krylov_quadratic_coordinates ')]:
    a = text.index(marker) + len(marker)
    assert text[a:text.index(' := by', a)] + '\n' == s[key]['signature']
assert k['actual_first_public_ASTIS_parents'][name] == []
assert k['both_exact_sealed_types_kernel_applied'] and k['all_owned_reachable']

title = 'The actual cosine feature matrix spans the block Krylov space'
statement = 'For the literal affine cosine spectrum, the image of the normalized feature matrix is exactly the block Krylov space. Every Krylov vector therefore has one coefficient representation giving both Euclidean quadratic identities.'
formula = r'\operatorname{range}(B)=K_q=\operatorname{span}\{\Lambda^j g_a:0\le a,j\le q\}.'
assumptions = [
    r'\(d,q\in\mathbb N\), \(2q+1<d\), and \(\kappa\ge2\). The case \(q=0\) is included; the dimension condition implies \(d\ge2\).',
    r'Put \(r=q+1\), \(\theta_i=(i+1/2)\pi/d\), \(\lambda_i=(\kappa+1)/2+(\kappa-1)\cos\theta_i/2\), and \(\Lambda=\operatorname{diag}(\lambda_i)\), with zero-based indices.',
    r'The starts \(g_a\in\mathbb R^d\) are arbitrary deterministic vectors, encoded by \(x\in\mathbb R^{d\times r}\). They are unscaled. Define \(t_{i0}=1\), \(t_{ij}=\sqrt2\cos(j\theta_i)\) for \(j>0\), and \(B_{i,(a,j)}=d^{-1/2}(g_a)_i t_{ij}\).',
    r'The space \(K_q\) is defined independently as the span of ordinary matrix powers \(\Lambda^j g_a\). No full-rank, vector-independence, Gaussian, polynomial-basis or normalization certificate is assumed.',
    r'For the private application, \(D=\operatorname{diag}(\cos((2q+1)\theta_i))\). Norm and inner product are the real Euclidean ones, explicitly realized by \(\mathrm{WithLp.toLp}\ 2\).'
]
boundary = 'Pointwise range component of Appendix C.2 Fact C.5, and a private same-witness Euclidean quadratic-coordinate application underlying the proof of Lemma4.4. Arbitrary deterministic starts are a source-proof-supported strengthening of the Gaussian-context assertion; no Gaussian law or coefficient measurability is asserted. The signed bilinear identity is proved directly, not inferred by reversing an absolute-value equality. The separate cosine-frame Gram/mean results are not formal parents of range. Fact C.6 concentration, a source-valid absolute constant, full uniform Lemma4.4, deferred Haar/joint/adaptive/private-seed/transcript/output-law constructions, exact matvec/finite precision/TV and dimension-condition-number adapters, deterministic worst-query caps and explicit expected-cost comparisons, both main lower bounds, public integration, desktop/mobile delivery and postmerge purification/Exposition Seal remain open.'
steps = [
    {'title': 'Undo the affine spectrum and keep all normalizations nonzero', 'text': 'Write the eigenvalue as alpha plus beta times the cosine. Kappa at least2 makes beta nonzero. The source dimension gives a nonzero square-root scale, while the constant and positive-frequency columns have nonzero factors1 and sqrt2. These facts are proved inside the theorem.', 'formula': r'\alpha=(\kappa+1)/2,\quad\beta=(\kappa-1)/2\ne0,\quad z(X)=\beta^{-1}(X-\alpha),\quad z(\lambda_i)=\cos\theta_i.'},
    {'title': 'Use the same truncated polynomial space', 'text': 'The monomials U_j=X^j and transformed Chebyshev polynomials Q_j=T_j composed with z each have degree j. Over the real field their leading coefficients are units. The canonical polynomial-sequence theorem shows that their first q+1 elements span precisely the same polynomial space. This is the triangular change of polynomial coordinates; it requires no independence of sampled vectors.', 'formula': r'U_j=X^j,\quad Q_j=T_j\circ z,\quad\deg U_j=\deg Q_j=j,\qquad\operatorname{span}_{j\le q}U_j=\mathbb R[X]_{<q+1}=\operatorname{span}_{j\le q}Q_j.'},
    {'title': 'Evaluate polynomials against each actual start', 'text': 'For each start, weighted evaluation is a linear map. Diagonal matrix powers act coordinatewise, including power0. The Chebyshev cosine identity sends Q_j to the cosine-weighted start. Thus the polynomial comparison applies to the actual Krylov columns and the literal feature columns.', 'formula': r'F_a(p)_i=p(\lambda_i)(g_a)_i,\qquad F_a(U_j)=\Lambda^j g_a,\qquad F_a(Q_j)_i=\cos(j\theta_i)(g_a)_i.'},
    {'title': 'Compare both column spans', 'text': 'Each feature column is a nonzero scalar multiple of its evaluated Chebyshev polynomial. Map the two polynomial spans through weighted evaluation to obtain both inclusions. Finally use the canonical equality between a finite matrix image and its column span. Neither inclusion needs B to be injective.', 'formula': r'B_{\bullet,(a,j)}=d^{-1/2}w_jF_a(Q_j),\quad w_0=1,\ w_j=\sqrt2\ (j>0),\qquad\operatorname{range}(B)=K_q.'},
    {'title': 'Choose one coefficient vector for each Krylov vector', 'text': 'Invoke the compiled range theorem. Membership in K_q becomes actual membership in the image of B, providing one c with Bc=v. This is pointwise existence; no measurable selection or expectation involving a random coefficient is claimed.', 'formula': r'v\in K_q\ \Longrightarrow\ \exists c\in\mathbb R^{r^2},\ Bc=v.'},
    {'title': 'Use that same coefficient in both Euclidean identities', 'text': 'The real Euclidean inner product agrees with the finite dot product. Transposing B in this bilinear form gives the norm identity and the signed D-weighted identity for the same c. The complete private application is folded below; concentration events are needed only for later inequalities.', 'formula': r'\|v\|_2^2=c^\top B^\top Bc,\qquad\langle v,Dv\rangle=c^\top B^\top DBc.'}
]
ranges = [
    (P, pr.index('  have hβ'), pr.index('  let U :')),
    (P, pr.index('  let U :'), pr.index('  let F :')),
    (P, pr.index('  let F :'), pr.index('  have hcol')),
    (P, pr.index('  have hcol'), pr.index('\nend AutoSamplingTheory')),
    (T, tr.index('  have hr :='), tr.index('  have hcoord')),
    (T, 0, len(tr))
]
records = []
for step, (p, a, b) in zip(steps, ranges):
    text = p.read_text()
    code = text[a:b].rstrip() + '\n'
    assert code in text
    step['lean'] = code
    records.append({'file': str(p), 'line': text[:a].count('\n')+1, 'code_sha256': sha(code), 'exact_contiguous_source': True})
assert steps[-1]['lean'] == tr
deps = ['Polynomial.Sequence.span_degreeLT', 'Polynomial.Sequence.degree_eq', 'Polynomial.Sequence.ne_zero', 'Polynomial.degree_comp', 'Polynomial.degree_C_mul', 'Polynomial.degree_X_sub_C', 'Polynomial.Chebyshev.degree_T', 'Polynomial.Chebyshev.T_real_cos', 'Polynomial.eval_smul', 'Polynomial.eval_comp', 'Matrix.diagonal_pow', 'Matrix.mulVec_diagonal', 'Matrix.range_mulVecLin', 'Submodule.smul_mem_iff', 'Submodule.span_le', 'Submodule.subset_span', 'EuclideanSpace.inner_toLp_toLp', 'real_inner_self_eq_norm_sq', 'Matrix.dotProduct_transpose_mulVec', 'Matrix.mulVec_mulVec']
source = {'url': 'https://arxiv.org/html/2610.20492v1#A3.Thmtheorem5', 'edition': 'arXiv2610.20492v1; pinned raw SHA256 '+s['source']['raw_sha256'], 'anchor': 'Section4.2 block Krylov definition S4.SS2.SSS0.Px1.p2; AppendixC.2 FactC.5 range, A3.SS2.2 proof and A3.SS2.p19/inline Ex130–131 quadratic use', 'wording_status': 'faithful paraphrase with explicit pointwise deterministic-start generalization', 'attribution': 'On Complexity of Gaussian Sampling, arXiv2610.20492v1.', 'scope': 'Range component and a private exact Euclidean quadratic-coordinate application; not complete C5/C6/Lemma4.4 or either lower bound.'}
unit = {'kind': 'theorem', 'reading_layout': 'progressive', 'declaration': name, 'title': title, 'reader_note': 'Open conditions and proof steps for the details. Each formula has exact folded Lean; step6 includes the full private Euclidean application.', 'statement': statement, 'formula': formula, 'assumptions': assumptions, 'steps': steps, 'astis_dependencies': [], 'mathlib_dependencies': deps, 'dependency_notes': 'The producer has no public ASTIS proof parents: it directly reuses canonical Mathlib polynomial and span facts. Its private application genuinely invokes this producer as its only public ASTIS parent. The two reachable generated proof certificates are internal providers, not additional source results. No separate cosine-Gram or Gaussian-moment node is required for this range statement.', 'lean_statement': 'The exact sealed natural d,q range includes q0 and preserves kappa>=2, the literal diagonal spectrum, unscaled starts, normalized feature matrix, independently defined Krylov span and actual set image.', 'lean_proof': 'Transport the equal truncated monomial and transformed Chebyshev spans through weighted polynomial evaluation, remove the internally proved nonzero column scalars and identify image with column span. The private application uses that image equality to obtain one c and then applies canonical Euclidean bilinear identities.', 'boundary': boundary, 'sources': [{**source, 'label': 'FactC.5 range and Lemma4.4 representation use'}, {'path': str(T), 'line': tr[:tr.index('private theorem')].count('\n')+1, 'label': 'Complete same-witness Euclidean application', 'scope': 'Private implementation consumer; no extra public or Registry node.'}], 'tests': ['lake build Tests.GaussianComplexityFixedSpectrumKrylovRange']}
put('website/content/declaration_lessons/huanjian-fixed-spectrum-krylov-range.json', {'schema_version': 1, 'units': [unit]})
aid = 'ASTIS-RT-20261110-HuanjianFixedSpectrumKrylovRange'
deltas = [
    {'source': 'FactC.5 appears with independent Gaussian starting vectors in the Lemma4.4 setup.', 'lean': 'The exact range identity is pointwise for every deterministic starting array x; no law, rank or independence binder is added.', 'classification': 'generalization', 'reason': 'The source polynomial change-of-coordinates proof is deterministic and works for any starts, even dependent or zero starts. The stochastic Lemma4.4 remains separate.'},
    {'source': 'K_q is the span of ordinary powers of the actual diagonal spectrum applied to unscaled g_a; B alone has row scale d^(-1/2) and normalized cosine columns.', 'lean': 'Exactly these literal matrix powers, starts, column weights and nonzero row factor at kappa>=2 and2q+1<d, including q0.', 'classification': 'same', 'reason': 'No span equality, basis, invertibility, normalization or concentration result is made a premise.'},
    {'source': 'The Lemma4.4 proof uses u=Bc, the Euclidean norm and an absolute weighted quadratic equality.', 'lean': 'A private theorem obtains one existential c from the producer and proves the actual Euclidean norm square and signed weighted-inner identity simultaneously.', 'classification': 'source-implicit', 'reason': 'The signed identity follows directly from bilinear matrix algebra and implies the displayed absolute identity; no converse inference from absolute values or measurable/random-coefficient selection is used.'}
]
binding = {'declaration': name, 'cell': 'ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range', 'role': 'prerequisite', 'supports': ['actual-krylov-range'], 'boundary': boundary, 'audit_id': aid, 'assumption_deltas': deltas}
original = ' '.join([statement, formula, *assumptions])
item = {'id': 'huanjian-fixed-spectrum-krylov-range', 'library': 'samplewiki', 'chapter': 'gaussian-sampling-complexity', 'chapter_path': 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html', 'title': title, 'source': source, 'statement': original, 'formulae': [{'label': 'The actual cosine feature image equals the Krylov span', 'tex': formula}], 'assumptions': assumptions, 'obligations': [{'id': 'actual-krylov-range', 'label': 'Actual image=Krylov equality, with a private same-witness Euclidean norm and weighted-inner application.'}], 'bindings': [binding]}
put('website/content/publications/huanjian-fixed-spectrum-krylov-range.json', {'schema_version': 1, 'items': [item]})
head, body = s['producer']['signature'].split(' :\n', 1)
literal = '∀ '+head+',\n'+body
context = ['Fin n denotes the finite set of integers0,...,n-1. A real Matrix m n is an m-by-n array; mulVec uses ordinary finite-sum real matrix-vector multiplication, and a matrix raised to a natural power uses ordinary matrix multiplication with power0 equal to the identity.', 'Submodule.span Real S is the real linear span of S. Set.range f is the actual set of values of f. The local lets in the statement define all objects literally and independently.', 'EuclideanSpace Real I is the real Euclidean space on the finite coordinates I. WithLp.ofLp forgets the Euclidean wrapper without changing coordinates; a product index (i,a) denotes the corresponding coordinate of the arbitrary input array. No distribution or independence is implicit.', 'Cosine and pi have their usual real meanings. Real.sqrt is the nonnegative real square root. Matrix.diagonal puts its supplied vector on the diagonal with zero off the diagonal; inverse on a real number is real field inverse. Universal quantifiers, natural inequalities, finite products and real arithmetic have their usual meanings.']
audit = {'id': aid, 'state': 'draft', 'source': {'source_id': 'arxiv2610.20492v1-actual-krylov-range-component', 'url': source['url'], 'anchor': source['anchor'], 'original_text': original, 'text_sha256': sha(original), 'source_snapshot_sha256': s['source']['raw_sha256']}, 'lean': {'declaration': name, 'file': str(P), 'statement': literal, 'statement_sha256': sha(literal), 'formalizer': 'huanjian_gc_20261110_fixed_spectrum_krylov_range', 'compiled': True, 'decoder_context': context}, 'reconstruction': {}, 'semantic_slots': {}, 'deltas': [], 'verdict': 'pending', 'source_review': {'state': 'pending'}, 'repairs': []}
pub.inputs.cache_clear()
pub.load.cache_clear()
audit['publication_binding_sha256'] = pub.binding_digest(item, binding)
audit['publication_context'] = pub.review_context(item, binding)
put('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json', audit)
raw = C.read_bytes()
c = json.loads(raw)
(E/'frontier-before-compiled-publication-authoring.raw.json.gz').write_bytes(gzip.compress(raw, mtime=0))
c['shared_floor_audit']['canonical_declaration'] = name
c['shared_floor_audit']['searched'].append('After actual prospective admission: Mathlib Polynomial.Sequence and Chebyshev degree/trigonometric identities, Matrix.ToLin range and diagonal powers; local Gaussian/TechnicalLemmas search found no existing actual range theorem.')
c['reuse_plan']['searched_existing'] = c['shared_floor_audit']['searched'][:]
c['reuse_plan']['reused_declarations'] = deps
c['reuse_plan']['known_consumers'] = [k['actual_consumer_private_FQName']+' genuinely obtains one c and proves both exact Euclidean quadratic formulas.']
c['evidence']['actual_compiled_first_public_ASTIS_parents'] = k['actual_first_public_ASTIS_parents']
for field in ['source_ordered', 'source_statement_adjacent', 'natural_language_formula_proof', 'hidden_assumptions_visible', 'lean_collapsed', 'external_dependencies_visible']:
    c['reader_contract'][field] = True
c['reader_contract']['status'] = 'Authored progressive six-step lesson with exact contiguous code and full private consumer. Independent static/rendered desktop/mobile/site acceptance remains pending; these flags do not certify live delivery.'
c['graph_contribution']['functor_view'] = 'none-found'
C.write_text(json.dumps(c, ensure_ascii=False, indent=2)+'\n')
pub.check_advance([name], reviewed=False)
packet = rt.decoder_packet(audit)
neutral = Path('.astis/semantic-neutral-20261111/p_kr_91de5a')
put(neutral/'input.json', packet)
put(E/'decoder-input.json', packet)
record = {'producer_raw_sha256': sha(P.read_bytes()), 'Test_raw_sha256': sha(T.read_bytes()), 'producer_signature_sha256': s['producer']['signature_sha256'], 'private_consumer_signature_sha256': s['actual_private_consumer']['signature_sha256'], 'publication_binding_sha256': audit['publication_binding_sha256'], 'anonymous_statement_sha256': sha(literal), 'anonymous_packet_canonical_sha256': packet['packet_sha256'], 'neutral_input': str(neutral/'input.json'), 'neutral_input_raw_sha256': sha((neutral/'input.json').read_bytes()), 'exact_step_code_records': records, 'actual_first_public_ASTIS_parents': k['actual_first_public_ASTIS_parents'], 'actual_owned_declarations': 4, 'handwritten': 2, 'generated_auxiliaries': 2, 'all_owned_reachable': True, 'source_review': 'pending', 'decoder': 'pending', 'sourceV_global_Goal_complete': False}
put(E/'publication-draft-record.json', record)
print(json.dumps(record))
