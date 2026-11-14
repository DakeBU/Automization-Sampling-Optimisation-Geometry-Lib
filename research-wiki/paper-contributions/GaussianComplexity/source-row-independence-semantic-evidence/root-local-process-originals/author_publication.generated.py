"""Author the row-law statement, real consumer and anonymous decoder input."""
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
evidence = paper / 'source-row-independence-semantic-evidence'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-independence.json')
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
private_name = '_private.Tests.GaussianComplexityFixedSpectrumSourceRowIndependence.0.' + seal['actual_private_consumer']['name']
for key, text in [('producer', p_text), ('actual_private_consumer', t_text)]:
    short = seal[key]['name'].split('.')[-1]
    literal = text.split('theorem ' + short, 1)[1].split(' := by', 1)[0].lstrip() + '\n'
    assert literal == seal[key]['signature']
assert sha(P.read_bytes()) == 'f63b38ba191d22354f23cf7a518717f47be96728a72b2bb3c7fbd9292c47db86'
assert sha(T.read_bytes()) == '7f138451e328360e9dcf049f3de0b267693be622818781705fdf4c6521a33dd0'
build, _ = receipt('20261112T081502699476Z-source-row-independence-producer-and-real-consumer-firstbuild')
kernel, log = receipt('20261112T081659781193Z-source-row-independence-exact-literal-kernel-and-parents')
row_parent = seal['shared_floor_audit']['known_existing_node']
parents = {name: [row_parent], private_name: [name, row_parent]}
for target, required in parents.items():
    assert 'ACTUAL_SEALED_LITERAL_KERNEL_TYPE_APPLICATION_PASS ' + target in log
    start = log.index('ACTUAL_PUBLIC_ASTIS_PARENTS ' + target + ': [')
    stop = log.index(']', start)
    assert all(item in log[start:stop] for item in required)
assert 'ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED 2' in log

title = 'Independent Gaussian rows and their truncated matrix images'
statement = r'The coordinate-row vectors of the independent-column Gaussian experiment are jointly independent. Their actual truncated matrix images are measurable and jointly independent in that same experiment.'
formula = (
    r'\mu\!\left(\bigcap_{i\in S}\Phi_i^{-1}(A_i)\right)'
    r'=\prod_{i\in S}\mu\bigl(\Phi_i^{-1}(A_i)\bigr),'
    r'\qquad S\subseteq\{1,\ldots,d\},\quad A_i\text{ Borel}.'
)
image_formula = (
    r'Y_i(\omega)=\frac1d\bigl(\Phi_i(\omega)\Phi_i(\omega)^\top\otimes t_it_i^\top\bigr)'
    r'\mathbf1_{\{\|\Phi_i(\omega)\|^2\le L\}}.'
)
consumer_formula = r'\forall i,\ Y_i\text{ is measurable};\qquad (Y_i)_{i=1}^d\text{ is independent under }\mu.'
assumptions = [
    r'Let \(d,q\in\mathbb N\), \(2q+1<d\), and \(r=q+1\). In particular \(d\ge2\), \(r\ge1\), and \(q=0\) is included.',
    r'Write \(\gamma_n=N(0,I_n)\) on real Euclidean \(n\)-space. The outcome space is \(\Omega=(\mathbb R^d)^r\), with the literal column-product probability law \(\mu=\gamma_d^{\otimes r}\). Define \(\Phi_i(\omega)=(\omega_{1,i},\ldots,\omega_{r,i})\in\mathbb R^r\).',
    r'The public independence conclusion means factorization for every finite family of Borel row events. The canonical row-law declaration supplies row measurability and Gaussian marginal laws internally; neither law nor independence is a caller-supplied certificate.',
    r'For the actual matrix consumer, put \(\theta_i=(i-\tfrac12)\pi/d\), \(t_i[0]=1\), \(t_i[k]=\sqrt2\cos(k\theta_i)\) for \(1\le k\le q\), and \(L=2r+3\log(1000d)\). Lean uses source indices \(i.val+1\) and \(a.val+1\).',
    r'Each \(Y_i\) has the displayed literal formula with its own closed cutoff. At entry \(((a,j),(b,k))\), the value inside the cutoff is \(d^{-1}\Phi_i[a]\Phi_i[b]t_i[j]t_i[k]\). Gaussian coordinates come first in both paired indices.',
    r'Matrices use their finite real-entry product measurable structure. Both measurability of all \(Y_i\) and full-family independence are proved outputs. The deterministic features vary with \(i\), so no identical-distribution claim for the matrices is made. No Gram, norm, moment, integrability, tail, \(\tau\), or condition-number premise is added.',
]
boundary = (
    'This local result proves full row-family independence in the canonical independent-column realization '
    'and the complete private consumer proves measurability and independence of the actual source truncated matrices. '
    'The producer adds independence to the same existing canonical row-law node; it creates no second marginal-law proof. '
    'Arbitrary extended-ambient transfer, original matrix-expectation adapters, public aggregate canonicalization, '
    'centered variance, matrix concentration, full Lemma4.4, both main lower bounds and exact oracle/TV/precision/'
    'worst-query-cap/expected-cost adapters remain open. Serialized integration, actual desktop/mobile/'
    'source-index/globalgraph/copy/download/public delivery and purification remain open.'
)
source = {
    'url': 'https://arxiv.org/html/2610.20492v1#A3.SS2.p1',
    'edition': 'arXiv:2610.20492v1; pinned HTML SHA256 ' + seal['source']['raw_sha256'],
    'anchor': 'Appendix C.2 p1 full row independence, p12 first sentence and Ex107 independent truncated matrices; S4.E11 half-grid, p10 cutoff and standing2q+1<d',
    'wording_status': 'faithful paraphrase',
    'attribution': 'On Complexity of Gaussian Sampling, arXiv:2610.20492v1.',
    'scope': 'Joint independence in the concrete source column-product realization and actual measurable Ex107 images; no arbitrary ambient-space transfer.',
}
mathlib = [
    'ProbabilityTheory.map_pi_eq_stdGaussian', 'MeasureTheory.Measure.map_map',
    'MeasureTheory.Measure.map_id', 'MeasureTheory.measurePreserving_pi',
    'MeasureTheory.Measure.infinitePi_eq_pi', 'MeasureTheory.Measure.infinitePi_map_curry_symm',
    'MeasureTheory.measurePreserving_piCongrLeft', 'MeasureTheory.Measure.infinitePi_map_curry',
    'MeasureTheory.MeasurePreserving.comp', 'ProbabilityTheory.iIndepFun_iff_map_fun_eq_pi_map',
    'measurableSet_le', 'measurable_pi_lambda', 'Measurable.ite',
    'Measurable.comp', 'ProbabilityTheory.iIndepFun.comp',
]


def code(text, first, last):
    return ''.join(text.splitlines(keepends=True)[first - 1:last])


steps = [
    {'title': 'Expose the full scalar-coordinate product',
     'text': 'Set up the same actual column experiment and reuse the existing canonical row-law theorem. The Mathlib equality identifying the Euclidean image of a scalar Gaussian product with stdGaussian supplies the full physical-coordinate joint law of each column. Unwrap each Euclidean column and apply the finite product-map theorem across columns.',
     'formula': r'\omega\longmapsto(\omega_{a,i})_{a,i}\quad\text{pushes }\mu\text{ to }\nu=\bigotimes_{a=1}^r\bigotimes_{i=1}^d N(0,1).',
     'lean': code(p_text, 21, 57)},
    {'title': 'Regroup the same coordinate array into physical rows',
     'text': 'Flatten the finite scalar array, exchange its two index factors, and curry it back with the physical-row index outside. The general product-measure curry rules are specialized using the exact equality of finite and infinite product constructions. Each step is a measurable measure-preserving map on the same sampled array.',
     'formula': r'\tau(x)_{i,a}=x_{a,i},\qquad\tau_\#\nu=\rho=\bigotimes_{i=1}^d\bigotimes_{a=1}^rN(0,1).',
     'lean': code(p_text, 59, 77)},
    {'title': 'Wrap rows and identify their joint law',
     'text': 'Wrap each scalar row in Euclidean r-space using the same canonical Gaussian product-image equality. Compose column unwrapping, coordinate regrouping and row wrapping. This gives a measurable exact joint pushforward for the actual row maps. The joint transport is an internal proof step.',
     'formula': r'(\omega\mapsto(\Phi_i(\omega))_{i=1}^d)_\#\mu=\gamma_r^{\otimes d}.',
     'lean': code(p_text, 78, 86)},
    {'title': 'Read full independence from the joint product law',
     'text': 'The reused row-law theorem supplies measurability and the exact marginal map equalities. Apply the finite-family independence characterization by joint product pushforward. Combining the genuine joint law with those canonical marginal equalities yields full event factorization for every finite family.',
     'formula': formula,
     'lean': code(p_text, 88, 96)},
    {'title': 'Keep the actual truncated matrices as separate row images',
     'text': 'Define the literal source features and cutoff. For each fixed i, let F_i map one Euclidean row to its inverse-d scaled, locally truncated outer-product tensor. The actual Y_i equals F_i composed with the actual row map on Omega. Reuse both the new independence producer and the same canonical row-law declaration. This fold contains the complete private statement and setup.',
     'formula': image_formula + r'\qquad Y_i=F_i\circ\Phi_i.',
     'lean': code(t_text, 1, 59)},
    {'title': 'Prove measurable images and preserve independence',
     'text': 'The squared-norm cutoff is a measurable closed event. Inside it, each matrix entry is a polynomial in two row coordinates with fixed scalar coefficients; outside it, the entry is zero. Thus each F_i is measurable into the finite real-entry product space. Compose with row measurability, then apply full-family independence preservation under the separate measurable F_i. The rule requires no injectivity, and the F_i may differ.',
     'formula': r'F_i(x)_{(a,j),(b,k)}=\frac{x_ax_b\,t_i[j]t_i[k]}d\mathbf1_{\{\|x\|^2\le L\}},\qquad' + consumer_formula,
     'lean': code(t_text, 61, 81)},
]
unit = {
    'kind': 'theorem', 'reading_layout': 'progressive', 'declaration': name, 'title': title,
    'reader_note': 'Open the assumptions and source steps for the exact experiment, matrix maps and adjacent Lean.',
    'statement': statement, 'formula': formula, 'assumptions': assumptions, 'steps': steps,
    'astis_dependencies': [row_parent], 'mathlib_dependencies': mathlib,
    'dependency_notes': 'The producer materially reuses the same existing compiled row-law node. The actual private consumer uses this new independence producer and that same row-law node. Canonical Gaussian/product/map facts remain shared Mathlib calls; no duplicate row-law theorem or separate public matrix-consumer credit is introduced.',
    'lean_statement': 'The literal physical coordinate-row family is iIndepFun under the fixed independent-column Gaussian product law.',
    'lean_proof': 'Unwrap the full joint Gaussian coordinate law, flatten/swap/regroup the finite array, wrap rows, and use the joint-product characterization of independence. The actual consumer proves each local truncated matrix image measurable and transports full independence through it.',
    'boundary': boundary,
    'sources': [{**source, 'label': 'Appendix C.2 row and actual truncated-matrix independence'},
                {'path': str(T), 'line': 11, 'label': 'Complete private actual matrix-independence consumer',
                 'scope': 'All actual Yi are measurable and jointly independent under the identical product measure.'}],
    'tests': ['lake build Tests.GaussianComplexityFixedSpectrumSourceRowIndependence'],
}
slug = 'huanjian-gaussian-source-row-independence'
audit_id = 'ASTIS-RT-20261112-HuanjianGaussianSourceRowIndependence'
lesson_path = Path('website/content/declaration_lessons') / (slug + '.json')
pub_path = Path('website/content/publications') / (slug + '.json')
audit_path = Path('research-wiki/semantic-roundtrip/audits') / (slug + '.json')
write(lesson_path, {'schema_version': 1, 'units': [unit]})
binding = {
    'declaration': name, 'cell': cell_path.stem, 'role': 'proof-edge',
    'supports': ['c2-original-row-joint-independence'], 'boundary': boundary, 'audit_id': audit_id,
    'assumption_deltas': [
        {'source': 'r=q+1 independent standard d-Gaussian columns, natural q and2q+1<d.',
         'lean': 'Literal finite column product mu on Omega; source Fin index shifts; q=0 retained.',
         'classification': 'same', 'reason': 'This is the concrete canonical realization. No caller supplies a column-law or independence certificate and no arbitrary extended-ambient adapter is claimed.'},
        {'source': 'p1 asserts the coordinate row vectors are independent N(0,I_r).',
         'lean': 'This producer proves full iIndepFun of the actual row family; the same existing canonical row-law node supplies its measurable Gaussian marginals.',
         'classification': 'same', 'reason': 'The binding covers the joint-independence subclaim. The genuine joint product transport is proved internally; independence is not inferred from marginal laws alone. No second marginal-law credit is created.'},
        {'source': 'p12 defines independent actual truncated matrices by Ex107.',
         'lean': 'The private consumer proves all actual Yi measurable and their full independence, with closed cutoff and Gaussian-first entry pairs.',
         'classification': 'source-implicit', 'reason': 'Measurability elaborates the random-matrix meaning and is an output, not an added premise. Canonical finite-entry product measurability is explicit; varying deterministic features do not imply iid matrices.'},
    ],
}
item = {
    'id': slug, 'library': 'samplewiki', 'chapter': 'gaussian-sampling-complexity',
    'chapter_path': 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html',
    'title': title, 'source': source, 'statement': statement,
    'formulae': [{'label': 'Full row-family independence', 'tex': formula},
                 {'label': 'Actual truncated matrix images', 'tex': image_formula},
                 {'label': 'Actual measurable independent matrix family', 'tex': consumer_formula}],
    'assumptions': assumptions,
    'obligations': [{'id': 'c2-original-row-joint-independence', 'label': 'Full coordinate-row independence with a real measurable independent Ex107 consumer.'}],
    'bindings': [binding],
}
write(pub_path, {'schema_version': 1, 'items': [item]})
binders, conclusion = seal['producer']['signature'].split(' :\n', 1)
literal = '∀ ' + binders + ',\n' + conclusion
source_text = (
    'For natural d and q with 2q+1<d, put r=q+1. Let g_1,...,g_r be independent '
    'standard Gaussian vectors in real d-dimensional Euclidean space, realized on their column-product probability space. '
    'For each physical coordinate i=1,...,d, form the row vector gamma_i=(g_1i,...,g_ri) in real r-dimensional Euclidean space. '
    'The full family gamma_1,...,gamma_d is independent. This independence subclaim means factorization of '
    'probabilities of finite intersections of measurable row events. The Gaussian marginal-law subclaim is kept in its existing canonical declaration.'
)
audit = {
    'id': audit_id, 'state': 'draft',
    'source': {'source_id': 'arxiv2610.20492v1-c2-original-row-joint-independence',
               'url': source['url'], 'anchor': source['anchor'], 'original_text': source_text,
               'text_sha256': sha(source_text), 'source_snapshot_sha256': seal['source']['raw_sha256']},
    'lean': {'declaration': name, 'file': str(P), 'statement': literal, 'statement_sha256': sha(literal),
             'formalizer': 'huanjian_gc_20261112_source_row_independence', 'compiled': True,
             'decoder_context': [
                 'Fin n is the finite index set of natural numbers less than n. Natural numbers embed into real numbers in the usual way.',
                 'EuclideanSpace real (Fin n) is real n-dimensional Euclidean space with its Euclidean and Borel structures. WithLp.toLp 2 wraps a real coordinate function as that Euclidean vector without changing coordinates.',
                 'stdGaussian on a finite-dimensional real Euclidean space is the centered Gaussian probability measure with identity covariance.',
                 'Measure.pi of a finite family of probability measures is the finite product measure. Its points are functions choosing one vector in each factor, with the product measurable structure.',
                 'iIndepFun f mu means that the sigma-algebras generated by the inverse images of each f_i are mutually independent: for every finite index set S and measurable target events A_i, mu of the intersection of f_i inverse A_i over S equals the product of the individual probabilities. This is full finite-family independence, not only pairwise independence. The predicate alone does not assert measurability of arbitrary f_i or equality of their distributions.',
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
cell['parents'] = [row_parent]
cell['evidence']['actual_compilation'] = build
cell['evidence']['actual_kernel'] = kernel
cell['evidence']['actual_public_ASTIS_parents'] = parents
cell['evidence'].pop('target_proof_calls', None)
cell['evidence'].pop('new_target_proof_attempts', None)
cell['reuse_plan']['reused_declarations'] = [row_parent, *mathlib]
cell['reuse_plan']['known_consumers'] = [private_name]
for key in ['source_ordered', 'source_statement_adjacent', 'natural_language_formula_proof',
            'hidden_assumptions_visible', 'lean_collapsed', 'external_dependencies_visible']:
    cell['reader_contract'][key] = True
cell['reader_contract']['status'] = 'Six adjacent source-ordered formula/Lean folds, including the complete private81-line actual matrix consumer. Independent source/native/static acceptance pending.'
cell_path.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n')
publication.check_advance([name], reviewed=False)
packet = semantic.decoder_packet(audit)
neutral = Path('.astis/semantic-neutral-20261112/n_decode_9e31/input.json')
write(neutral, packet)
write(evidence / 'decoder-input.json', packet)
record = {
    'producer_sha256': sha(P.read_bytes()), 'private_consumer_sha256': sha(T.read_bytes()),
    'build': build, 'kernel': kernel, 'actual_public_ASTIS_parents': parents,
    'both_exact_literal_types_kernel_applied': True, 'raw_Expr_structural_equality': False,
    'owned_theorems': 2, 'handwritten': 2, 'generated_internal': 0,
    'publication_binding_sha256': audit['publication_binding_sha256'],
    'neutral_input': str(neutral), 'neutral_input_raw_sha256': sha(neutral.read_bytes()),
    'neutral_canonical_packet_sha256': packet['packet_sha256'], 'anonymous_statement_sha256': sha(literal),
    'step_code_sha256': [sha(step['lean']) for step in steps], 'source_review': 'pending',
}
write(evidence / 'publication-draft-record.json', record)
print(json.dumps(record))
