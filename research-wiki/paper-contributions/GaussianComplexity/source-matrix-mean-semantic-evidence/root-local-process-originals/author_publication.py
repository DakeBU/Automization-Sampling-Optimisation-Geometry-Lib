"""Author exact actual-matrix means and their real finite-sum consumer once."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_publication as publication
import astis_semantic_roundtrip as semantic

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
paper = Path('research-wiki/paper-contributions/GaussianComplexity')
evidence = paper / 'source-matrix-mean-semantic-evidence'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json')
runner = Path('.astis/huanjian-resume-20261103')
sha = lambda b: hashlib.sha256(b.encode() if isinstance(b, str) else b).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as out:
        json.dump(value, out, ensure_ascii=False, indent=2)
        out.write('\n')

def receipt(stem):
    path = runner / (stem + '.receipt.json')
    obj = json.loads(path.read_bytes())
    log = Path(obj['log']).read_bytes()
    assert obj['exit_code'] == 0 and sha(log) == obj['log_sha256']
    return {'path': str(path), 'sha256': sha(path.read_bytes()), 'log_sha256': sha(log)}, log.decode()

seal = json.loads((workspace / 'statement-seal-v1.json').read_bytes())
P, T = [Path(seal[k]['planned_file']) for k in ('producer', 'actual_private_consumer')]
p_text, t_text = P.read_text(), T.read_text()
name = seal['producer']['name']
private_name = '_private.Tests.GaussianComplexityFixedSpectrumSourceMatrixMean.0.' + seal['actual_private_consumer']['name']
for key, text in [('producer', p_text), ('actual_private_consumer', t_text)]:
    short = seal[key]['name'].split('.')[-1]
    literal = text.split('theorem ' + short + '\n', 1)[1].split(':= by\n', 1)[0]
    assert literal == seal[key]['signature']
snapshots = json.loads(Path('.astis/semantic-neutral-20261112/mm_src_8c31/code-only-inputs-v1/input-manifest.json').read_bytes())
for path in (P, T):
    entry = next(x for x in snapshots['entries'] if x['source'] == str(path))
    assert sha(path.read_bytes()) == entry['sha256']
build, _ = receipt('20261112T125123575778Z-source-matrix-mean-real-consumer-implicit-sum-arguments-v3')
first_producer, _ = receipt('20261112T124717774428Z-source-matrix-mean-producer-firstbuild')
kernel, log = receipt('20261112T125208720803Z-source-matrix-mean-exact-literal-kernel-and-real-parents')
row_parent, moment_parent, frame_parent = seal['shared_floor_audit']['known_canonical_nodes']
parents = {name: [row_parent, moment_parent], private_name: [name, frame_parent]}
for target, required in parents.items():
    assert 'ACTUAL_SEALED_LITERAL_KERNEL_TYPE_APPLICATION_PASS ' + target in log
    start = log.index('ACTUAL_PUBLIC_ASTIS_PARENTS ' + target + ': [')
    stop = log.index(']', start)
    assert all(item in log[start:stop] for item in required)
assert 'ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED 3' in log

title = 'Actual truncated matrix means in the Gaussian column experiment'
statement = 'Every actual truncated matrix is integrable and has the exact common-coefficient mean. The private consumer proves the expectations of the actual unweighted and cosine-weighted sums.'
formula = r'Y_i\in L^1(\mu),\qquad \mathbb E_\mu Y_i=\frac ad\bigl(I_r\otimes t_it_i^\top\bigr).'
image_formula = r'Y_i(\omega)=\frac1d\bigl(\Phi_i(\omega)\Phi_i(\omega)^\top\otimes t_it_i^\top\bigr)\mathbf1_{\{\|\Phi_i(\omega)\|^2\le L\}}.'
consumer_formula = r'\mathbb E_\mu\!\left[\sum_{i=1}^dY_i\right]=aI_{r^2},\qquad \mathbb E_\mu\!\left[\sum_{i=1}^d\cos(n\theta_i)Y_i\right]=0,\quad n=2q+1.'
assumptions = [
    r'Let \(d,q\in\mathbb N\), \(2q+1<d\), and \(r=q+1\). Thus \(d\ge2\), \(r\ge1\), and \(q=0\) is retained.',
    r'The original outcome space is \(\Omega=(\mathbb R^d)^r\), with the literal product \(\mu=\gamma_d^{\otimes r}\), where \(\gamma_j=N(0,I_j)\). The actual row is \(\Phi_i(\omega)=(\omega_{1,i},\ldots,\omega_{r,i})\). No row law or mean is supplied by the caller.',
    r'Put \(L=2r+3\log(1000d)\), \(\theta_i=(i-\tfrac12)\pi/d\), \(t_i[0]=1\), and \(t_i[k]=\sqrt2\cos(k\theta_i)\) for \(1\le k\le q\). The source physical index is \(i.val+1\); feature indices remain \(k.val\).',
    r'The common scalar is fixed by \(a=r^{-1}\int_{\mathbb R^r}\|x\|^2\mathbf1_{\{\|x\|^2\le L\}}\,d\gamma_r(x)\). Its retained-radius integrability belongs to the reused canonical moment proof. The actual row law identifies this same scalar in every physical row; no free per-row coefficient is introduced.',
    r'The displayed \(Y_i\) uses its own inclusive local cutoff, inverse-\(d\) scaling, and Gaussian-first paired indices in the Kronecker product. It is an unconditional truncated matrix on the same original \(\mu\); the law is not conditioned on all rows passing.',
    r'Matrix expectations are complete Bochner integrals in the actual finite-dimensional Euclidean operator norm. Integrability of every \(Y_i\) and of both actual sums is proved. The source displays sums of expectations; finite integrability and integral exchange internally give the displayed actual-sum expectations. No independence, Gram, moment, integrability, mean, \(\tau\), or condition-number certificate is a premise.',
]
boundary = ('This local producer proves only actual original-experiment truncated matrix integrability and first moments. '
    'Its private consumer proves integrability and expectations of both actual finite sums. '
    'The same canonical row-law, truncated-row moment and cosine-frame nodes are reused; no second public radial/marginal lemma is created. '
    'The old private canonical-row matrix application remains immutable history and gains no duplicate public credit. '
    'Arbitrary extended-ambient transfer, scalar bias/range extensions, public aggregate canonicalization, centered variance, '
    'matrix concentration, full Lemma4.4, both main lower bounds and exact oracle/TV/precision/worst-query-cap/expected-cost adapters remain open. '
    'Serialized integration, actual desktop/mobile/MathJax/source-index/globalgraph/copy/download/public delivery and purification remain open.')
source = {
    'url': 'https://arxiv.org/html/2610.20492v1#A3.SS2.p12',
    'edition': 'arXiv:2610.20492v1; pinned HTML SHA256 ' + seal['source']['raw_sha256'],
    'anchor': 'Appendix C.2 p12.4 actual matrix means, Ex107/108 and Ex110 two mean sums; original p1 experiment, p10 cutoff and Fact C.5 feature sums',
    'wording_status': 'faithful paraphrase',
    'attribution': 'On Complexity of Gaussian Sampling, arXiv:2610.20492v1.',
    'scope': 'Concrete original column-product realization; actual integrable matrix and sum means. No ambient transfer or concentration result.',
}
mathlib = ['MeasureTheory.MeasurePreserving.integrable_comp_of_integrable', 'MeasureTheory.integral_map',
    'ContinuousLinearMap.integrable_comp', 'ContinuousLinearMap.integral_comp_comm',
    'Matrix.kroneckerBilinear', 'Matrix.sum_apply', 'Matrix.mul_diagonal', 'Matrix.one_kronecker_one',
    'MeasureTheory.integrable_finsetSum', 'MeasureTheory.integral_finsetSum',
    'MeasureTheory.Integrable.smul', 'MeasureTheory.integral_smul']

def code(text, first, last):
    return ''.join(text.splitlines(keepends=True)[first - 1:last])

steps = [
    {'title': 'Use the same canonical row law and retained radial moment',
     'text': 'Set up the literal source experiment and cutoff. Reuse the existing truncated-row theorem, whose proof establishes retained-radius and matrix integrability and identifies the coefficient by the radial trace. Reuse the existing actual-row Gaussian pushforward, with measurability and exact standard marginal law as its outputs.',
     'formula': r'(\Phi_i)_\#\mu=\gamma_r,\qquad G_L(x)=xx^\top\mathbf1_{\{\|x\|^2\le L\}},\quad G_L\in L^1(\gamma_r),\quad\int G_L\,d\gamma_r=aI_r.',
     'lean': code(p_text, 45, 78)},
    {'title': 'Transport the genuine row moment to the original experiment',
     'text': 'The measure-preserving row map pulls canonical integrability back to the actual row. Apply the general integral-map rule with the actual a.e. strong measurability furnished by integrability. No injectivity or measurable embedding of the row map is required. The same pushforward also identifies the retained scalar coefficient under each actual row law.',
     'formula': r'G_L\circ\Phi_i\in L^1(\mu),\qquad \int_\Omega G_L(\Phi_i(\omega))\,d\mu(\omega)=aI_r.',
     'lean': code(p_text, 79, 89)},
    {'title': 'Commute the fixed tensor map with expectation',
     'text': 'For each physical row, form the continuous linear map from r-by-r matrices to paired-index matrices, M maps to inverse-d times M tensor t_i t_i-transpose. Its image of the retained row matrix is exactly the actual Y_i, including the inclusive cutoff. Continuous linear maps preserve integrability and commute with these Bochner integrals, yielding the producer conclusion.',
     'formula': r'T_i(M)=d^{-1}(M\otimes t_it_i^\top),\qquad Y_i=T_i\circ G_L\circ\Phi_i,\qquad \mathbb E_\mu Y_i=T_i(aI_r).',
     'lean': code(p_text, 90, 118)},
    {'title': 'Match both source cosine-frame identities',
     'text': 'The complete private statement and setup use the exact same actual experiment and materially call the new producer. Normalize the two algebraically equal half-grid angle expressions, then apply the existing canonical cosine-frame theorem. Reading its ordinary and diagonal-weighted products entrywise gives both deterministic feature sums, including the constant-feature q=0 case.',
     'formula': r'\sum_i t_it_i^\top=dI_r,\qquad \sum_i\cos(n\theta_i)t_it_i^\top=0,\quad n=2q+1.',
     'lean': code(t_text, 1, 110)},
    {'title': 'Assemble the two sums of actual matrix means',
     'text': 'The fixed linear tensor map M maps to I_r tensor M carries the two feature sums to dI_(r squared) and zero. Substitute the actual individual means and use the internally derived nonzero physical dimension to cancel d. The result is the source Ex110 pair of sums of expectations, without a supplied Gram or mean certificate.',
     'formula': r'\sum_i\mathbb E_\mu Y_i=\frac ad\!\left(I_r\otimes\sum_it_it_i^\top\right)=aI_{r^2},\qquad \sum_i\cos(n\theta_i)\mathbb E_\mu Y_i=0.',
     'lean': code(t_text, 111, 143)},
    {'title': 'Integrate the actual finite random sums',
     'text': 'Individual actual Y integrability gives integrability of each deterministically weighted summand and both finite sums. Exchange the finite sums with the Bochner integral and pull out each fixed cosine scalar. This turns the source sums of expectations into the actual-sum expectations in the private target. Joint independence is not required for this calculation.',
     'formula': consumer_formula,
     'lean': code(t_text, 144, 158)},
]
unit = {
    'kind': 'theorem', 'reading_layout': 'progressive', 'declaration': name, 'title': title,
    'reader_note': 'Open assumptions and source-ordered steps for the exact experiment, coefficient and adjacent Lean.',
    'statement': statement, 'formula': formula, 'assumptions': assumptions, 'steps': steps,
    'astis_dependencies': [row_parent, moment_parent], 'mathlib_dependencies': mathlib,
    'dependency_notes': 'The producer materially uses the same canonical actual-row law and truncated-row moment. The private actual-sum consumer uses this producer and the same canonical cosine-frame theorem. Private consumers receive no independent public theorem credit; exact common declarations remain single canonical nodes.',
    'lean_statement': 'Every literal source-experiment Yi is Bochner integrable with mean (a/d) times I tensor ti ti-transpose.',
    'lean_proof': 'Transport the existing retained row moment under the genuine noninjective row pushforward, then apply the fixed continuous tensor map. The real consumer uses both exact frame identities and finite Bochner linearity.',
    'boundary': boundary,
    'sources': [{**source, 'label': 'Appendix C.2 actual truncated matrix means'},
                {'path': str(T), 'line': 17, 'label': 'Complete private actual-sum expectation consumer',
                 'scope': 'Both actual finite sums are integrable with expectations aI and zero.'}],
    'tests': ['lake build Tests.GaussianComplexityFixedSpectrumSourceMatrixMean'],
}
slug = 'huanjian-gaussian-source-matrix-mean'
audit_id = 'ASTIS-RT-20261112-HuanjianGaussianSourceMatrixMean'
lesson_path = Path('website/content/declaration_lessons') / (slug + '.json')
pub_path = Path('website/content/publications') / (slug + '.json')
audit_path = Path('research-wiki/semantic-roundtrip/audits') / (slug + '.json')
write(lesson_path, {'schema_version': 1, 'units': [unit]})
binding = {
    'declaration': name, 'cell': cell_path.stem, 'role': 'proof-edge',
    'supports': ['c2-actual-source-matrix-means'], 'boundary': boundary, 'audit_id': audit_id,
    'assumption_deltas': [
        {'source': 'Original r=q+1 independent standard d-Gaussian columns, q>=0 and2q+1<d.',
         'lean': 'Fixed canonical product experiment, actual row coordinates, q=0 and exact half-grid/cutoff retained.',
         'classification': 'same', 'reason': 'Concrete realization only; no ambient transfer, independence or row-law certificate input.'},
        {'source': 'The same a=(1/r)E[Ri indicator(Ri<=L)] occurs in every actual Yi mean.',
         'lean': 'a is defined by the canonical retained radial integral; actual row transport and the existing canonical radial moment derive all exact actual matrix means.',
         'classification': 'same', 'reason': 'The common law identifies the scalar internally. No free per-row mean or new public radial lemma is introduced.'},
        {'source': 'Ex110 displays both sums of expectations and p12.5 states the weighted sum has zero expectation.',
         'lean': 'The real private consumer proves integrability and Bochner integrals of both actual random sums.',
         'classification': 'source-implicit', 'reason': 'Finite integrability, matrix norm/completeness and finite integral/scalar exchange are proved internally; they are output obligations, not added hypotheses.'},
    ],
}
item = {
    'id': slug, 'library': 'samplewiki', 'chapter': 'gaussian-sampling-complexity',
    'chapter_path': 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html',
    'title': title, 'source': source, 'statement': statement,
    'formulae': [{'label': 'Actual individual matrix means', 'tex': formula},
                 {'label': 'Literal actual truncated matrices', 'tex': image_formula},
                 {'label': 'Expectations of both actual sums', 'tex': consumer_formula}],
    'assumptions': assumptions,
    'obligations': [{'id': 'c2-actual-source-matrix-means', 'label': 'Actual Yi integrability and means with a real two-sum expectation consumer.'}],
    'bindings': [binding],
}
write(pub_path, {'schema_version': 1, 'items': [item]})
binders, conclusion = seal['producer']['signature'].split(' :\n', 1)
literal = '∀ ' + binders + ',\n' + conclusion
source_text = ('For natural d and q with 2q+1<d put r=q+1. Realize r independent standard d-dimensional Gaussian columns on their column-product probability space. '
    'Let gamma_i collect their physical coordinate i. Put L=2r+3log(1000d), theta_i=(i-1/2)pi/d, and t_i=(1,sqrt(2)cos(theta_i),...,sqrt(2)cos(q theta_i)). '
    'Define Yi as inverse-d times the outer-product tensor gamma_i gamma_i-transpose tensor t_i t_i-transpose, retained on norm(gamma_i)^2<=L and zero outside. '
    'Let a be (1/r) times the retained squared-radius expectation under a standard r-dimensional Gaussian. '
    'Every actual Yi is integrable and its expectation is (a/d) times I_r tensor t_i t_i-transpose. '
    'This binding concerns the individual matrix means; the actual finite-sum expectations are checked separately as the material private consumer.')
audit = {
    'id': audit_id, 'state': 'draft',
    'source': {'source_id': 'arxiv2610.20492v1-c2-actual-source-matrix-means',
               'url': source['url'], 'anchor': source['anchor'], 'original_text': source_text,
               'text_sha256': sha(source_text), 'source_snapshot_sha256': seal['source']['raw_sha256']},
    'lean': {'declaration': name, 'file': str(P), 'statement': literal, 'statement_sha256': sha(literal),
             'formalizer': 'huanjian_gc_20261112_source_matrix_mean', 'compiled': True,
             'decoder_context': [
                 'Fin n is the finite index set of natural numbers less than n. Natural numbers embed into real numbers in the usual way.',
                 'EuclideanSpace real (Fin n) is real n-dimensional Euclidean space with its Euclidean norm and Borel structure. WithLp.toLp 2 wraps a real coordinate function as that vector; WithLp.ofLp recovers the same coordinates.',
                 'stdGaussian on a finite-dimensional real Euclidean space is the centered Gaussian probability measure with identity covariance. Measure.pi is the finite product measure with the product measurable structure.',
                 'Set.indicator s f equals f on s and zero outside s. Real.log is the natural logarithm and Real.sqrt is the nonnegative square root.',
                 'Matrix m n real is a finite real matrix. Matrix.vecMulVec u v has entries u_i times v_j. Matrix.kronecker A B has paired indices and entry A_(i,k) times B_(j,l) at ((i,j),(k,l)). The symbol 1 is the identity matrix and scalar action multiplies every entry.',
                 'Matrix integrals use the Euclidean operator norm on the finite complete real matrix space. Integrable f mu means almost-everywhere strong measurability and finite integral of the extended norm; it is an asserted conclusion wherever displayed.',
                 'The integral notation is the Bochner integral. It is totalized to zero outside complete or integrable cases; the explicit Integrable conclusions require genuine integrability. All local lets define fixed objects, rather than additional assumptions.',
             ]},
    'reconstruction': {}, 'semantic_slots': {}, 'deltas': [], 'verdict': 'pending',
    'source_review': {'state': 'pending'}, 'repairs': [],
}
publication.inputs.cache_clear()
publication.load.cache_clear()
audit['publication_binding_sha256'] = publication.binding_digest(item, binding)
audit['publication_context'] = publication.review_context(item, binding)
write(audit_path, audit)
cell = json.loads(cell_path.read_bytes())
cell['parents'] = [row_parent, moment_parent, frame_parent]
cell['evidence']['actual_compilation'] = build
cell['evidence']['actual_producer_first_compilation'] = first_producer
cell['evidence']['actual_kernel'] = kernel
cell['evidence']['actual_public_ASTIS_parents'] = parents
cell['evidence'].pop('target_proof_calls', None)
cell['evidence'].pop('new_target_proof_attempts', None)
cell['reuse_plan']['reused_declarations'] = [row_parent, moment_parent, frame_parent, *mathlib]
cell['reuse_plan']['known_consumers'] = [private_name]
for key in ['source_ordered', 'source_statement_adjacent', 'natural_language_formula_proof',
            'hidden_assumptions_visible', 'lean_collapsed', 'external_dependencies_visible']:
    cell['reader_contract'][key] = True
cell['reader_contract']['status'] = 'Six exact source-ordered formula/Lean folds and complete private158-line L17 source export. Independent code/source/decoder/native/static acceptance pending.'
cell_path.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n')
publication.check_advance([name], reviewed=False)
packet = semantic.decoder_packet(audit)
neutral = Path('.astis/semantic-neutral-20261112/n_decode_38df/input.json')
write(neutral, packet)
write(evidence / 'decoder-input.json', packet)
write(evidence / 'publication-draft-record.json', {
    'producer_sha256': sha(P.read_bytes()), 'private_consumer_sha256': sha(T.read_bytes()),
    'build': build, 'producer_first_build': first_producer, 'kernel': kernel,
    'actual_public_ASTIS_parents': parents,
    'both_exact_literal_types_kernel_applied': True, 'raw_Expr_structural_equality': False,
    'owned_theorems': 3, 'handwritten': 2, 'generated_internal': 1,
    'publication_binding_sha256': audit['publication_binding_sha256'],
    'neutral_input': str(neutral), 'neutral_input_raw_sha256': sha(neutral.read_bytes()),
    'neutral_canonical_packet_sha256': packet['packet_sha256'], 'anonymous_statement_sha256': sha(literal),
    'step_code_sha256': [sha(step['lean']) for step in steps], 'source_review': 'pending',
})
print(json.dumps({'publication_binding_sha256': audit['publication_binding_sha256'],
                  'neutral_input': str(neutral), 'neutral_canonical_packet_sha256': packet['packet_sha256'],
                  'public_producer_lines': len(p_text.splitlines()), 'private_consumer_lines': len(t_text.splitlines()),
                  'owned_theorems': 3, 'normal_VERIFIED_calls': 0}))
