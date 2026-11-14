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
evidence = paper / 'source-row-law-semantic-evidence'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-law.json')
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
private_name = '_private.Tests.GaussianComplexityFixedSpectrumSourceRowLaw.0.' + seal['actual_private_consumer']['name']
for key, text in [('producer', p_text), ('actual_private_consumer', t_text)]:
    short = seal[key]['name'].split('.')[-1]
    literal = text.split('theorem ' + short, 1)[1].split(' := by', 1)[0].lstrip() + '\n'
    assert literal == seal[key]['signature']
assert sha(P.read_bytes()) == 'c370caf377c5d56c97bdb1012d407049e63b04998011df327de79c46fb2b1201'
assert sha(T.read_bytes()) == 'ed2c97bd4d49c9ebcabc7ecf24ce3eba91a972e5e634fb3c694f6eff7a496715'
build, _ = receipt('20261112T060103893612Z-source-row-law-final-simp-clean-build')
kernel, log = receipt('20261112T060306835900Z-source-row-law-final-exact-kernel-and-parents')
moment_parent = seal['shared_floor_audit']['existing_canonical_consumer_parent']
parents = {name: [], private_name: [name, moment_parent]}
for target, required in parents.items():
    assert 'ACTUAL_SEALED_LITERAL_KERNEL_TYPE_APPLICATION_PASS ' + target in log
    start = log.index('ACTUAL_PUBLIC_ASTIS_PARENTS ' + target + ': [')
    stop = log.index(']', start)
    assert all(item in log[start:stop] for item in required)
assert 'ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED 4' in log

title = 'Gaussian row marginals and the simultaneous cutoff event'
statement = r'Every coordinate row of the independent-column Gaussian experiment has law \(N(0,I_r)\). In this same experiment, all row squared norms are at most \(2r+3\log(1000d)\) with probability at least \(999/1000\).'
formula = (
    r'\mu=\gamma_d^{\otimes r},\qquad \Phi_i(\omega)=(\omega_{1,i},\ldots,\omega_{r,i}),'
    r'\qquad(\Phi_i)_\#\mu=\gamma_r.'
)
moment_formula = r'\int_\Omega e^{\|\Phi_i(\omega)\|^2/3}\,d\mu(\omega)=3^{r/2}.'
good_formula = (
    r'\mu\{\omega:\ \forall i,\ \|\Phi_i(\omega)\|^2\le 2r+3\log(1000d)\}'
    r'\ge\frac{999}{1000}.'
)
assumptions = [
    r'Let \(d,q\in\mathbb N\), \(2q+1<d\), and \(r=q+1\). Hence \(d\ge2\) and \(r\ge1\); \(q=0\) is included.',
    r'Write \(\gamma_n=N(0,I_n)\) on real \(n\)-dimensional Euclidean space. The outcome space is \(\Omega=(\mathbb R^d)^r\), with the literal product probability measure \(\mu=\gamma_d^{\otimes r}\). Its \(r\) column vectors are independent by this fixed construction.',
    r'The \(i\)-th row map is \(\Phi_i(\omega)=(\omega_{1,i},\ldots,\omega_{r,i})\in\mathbb R^r\). Lean uses \(a.val+1\) and \(i.val+1\) for the source column and row indices, respectively; WithLp.toLp supplies the Euclidean row norm.',
    r'Put \(R_i(\omega)=\|\Phi_i(\omega)\|^2\) and \(L=2r+3\log(1000d)\). The good event is the simultaneous closed cutoff \(\{\forall i,\ R_i\le L\}\); each bad event uses the strict inequality \(L<R_i\).',
    r'The public conclusion MeasurePreserving includes both measurability of each row map and its exact Gaussian pushforward law. These are proved outputs. Exponential integrability, the exact exponential moment, the tail estimates and event measurability are also derived internally.',
    r'The private consumer measures the good event under this same \(\mu\), using the exact ENNReal threshold ofReal \((999/1000)\). No retained-law normalization, auxiliary law certificate, \(\tau\)-smallness or condition-number premise is added. No Gaussian assertion is made about a norm on the function carrier \(\Omega\).',
]
boundary = (
    'The public theorem proves each marginal row law in the canonical independent-column realization; '
    'the complete private consumer proves the printed simultaneous cutoff probability in that same experiment. '
    'Marginals alone do not establish joint-row independence. Transfer from an arbitrary extended ambient experiment, '
    'full joint-row independence, original matrix-expectation adapters, centered variance, concentration, Fact C.6 '
    'and full Lemma 4.4 remain open. Both main lower bounds, exact oracle/TV/precision/worst-case cap/expected-cost '
    'adapters, serialized integration, full desktop/mobile source-index/graph delivery and purification remain open.'
)
source = {
    'url': 'https://arxiv.org/html/2610.20492v1#A3.SS2.p1',
    'edition': 'arXiv:2610.20492v1; pinned HTML SHA256 ' + seal['source']['raw_sha256'],
    'anchor': 'Appendix C.2 p1 independent Gaussian columns and coordinate rows; p10 Ex104/Ex105 and the printed probability at least0.999; standing 2q+1<d',
    'wording_status': 'faithful paraphrase',
    'attribution': 'On Complexity of Gaussian Sampling, arXiv:2610.20492v1.',
    'scope': 'Each row marginal and the all-good cutoff in the canonical realization of the source independent-column experiment. Full joint-row independence is excluded.',
}
mathlib = [
    'ProbabilityTheory.map_pi_eq_stdGaussian', 'MeasureTheory.Measure.map_map',
    'MeasureTheory.measurePreserving_eval', 'MeasureTheory.measurePreserving_pi',
    'MeasureTheory.MeasurePreserving.comp',
    'MeasureTheory.MeasurePreserving.integrable_comp_of_integrable',
    'MeasureTheory.integral_map', 'MeasureTheory.meas_ge_le_lintegral_div',
    'MeasureTheory.ofReal_integral_eq_lintegral_ofReal',
    'MeasureTheory.measure_iUnion_fintype_le', 'MeasurableSet.iInter',
    'MeasureTheory.measure_compl', 'ENNReal.ofReal_sub',
]


def code(text, first, last):
    return ''.join(text.splitlines(keepends=True)[first - 1:last])


steps = [
    {'title': 'Identify a coordinate of one Gaussian column',
     'text': 'Express the canonical d-dimensional Gaussian as the Euclidean image of the product of scalar standard Gaussians. A physical-coordinate evaluation is measurable and pushes this product onto one scalar standard Gaussian. Composition of measure maps gives the coordinate law under the actual column Gaussian.',
     'formula': r'(x\mapsto x_i)_\#\gamma_d=N(0,1).',
     'lean': code(p_text, 22, 42)},
    {'title': 'Collect the coordinates across independent columns',
     'text': 'The finite product-map theorem collects the same physical coordinate across all r independent columns. Wrap the resulting coordinate tuple in Euclidean space. This proves both row measurability and the exact row Gaussian law, rather than assuming either. The public result asserts each marginal only.',
     'formula': formula,
     'lean': code(p_text, 43, 52)},
    {'title': 'Transport exponential integrability and its exact mean',
     'text': 'Use the existing canonical Gaussian exponential-moment theorem, including its genuine integrability conclusion. The row-law producer transports integrability to the actual outcome space. The general measurable-map integral theorem transports the exact mean; it requires no injectivity of the row projection. This fold includes the complete private statement and setup.',
     'formula': moment_formula,
     'lean': code(t_text, 1, 65)},
    {'title': 'Calibrate the cutoff',
     'text': 'The source exponential estimate is bounded by the reciprocal error scale. Split log3 into two elementary logarithms to prove log3<4/3, then use r>=0. With L=2r+3log(1000d), the exponential-moment-to-threshold ratio is at most1/(1000d).',
     'formula': r'\frac{3^{r/2}}{e^{L/3}}=\exp\!\left(\frac r2\log3-\frac{2r}3-\log(1000d)\right)\le\frac1{1000d}.',
     'lean': code(t_text, 67, 85)},
    {'title': 'Apply exponential Markov on the actual outcome space',
     'text': 'The strict bad-row event is contained in the weak exponential threshold event. Apply nonnegative Markov, then use the transported Bochner integrability and exact mean to evaluate the nonnegative integral. This proves the strict tail bound under the original column-product measure.',
     'formula': r'\mu\{L<R_i\}\le\frac{\int_\Omega e^{R_i/3}\,d\mu}{e^{L/3}}\le\frac1{1000d}.',
     'lean': code(t_text, 87, 109)},
    {'title': 'Exclude every bad row simultaneously',
     'text': 'The complement of the closed good event is the finite union of strict bad-row events. Finite subadditivity gives total bad probability at most1/1000 without a joint-independence premise. Prove the good event measurable and subtract from the probability of the whole space to obtain the exact rational lower bound. The union-bound expansion is a source-supported derivation of the printed probability.',
     'formula': r'\mu(\mathrm{good}^{c})\le\sum_{i=1}^{d}\mu\{L<R_i\}\le\frac1{1000},\qquad\mu(\mathrm{good})\ge\frac{999}{1000}.',
     'lean': code(t_text, 111, 145)},
]
unit = {
    'kind': 'theorem', 'reading_layout': 'progressive', 'declaration': name, 'title': title,
    'reader_note': 'Open the assumptions and source steps for the exact experiment and adjacent Lean.',
    'statement': statement, 'formula': formula, 'assumptions': assumptions, 'steps': steps,
    'astis_dependencies': [], 'mathlib_dependencies': mathlib,
    'dependency_notes': 'The public row-law producer has no ASTIS theorem parent. The actual private cutoff consumer materially uses this producer and the existing canonical StdGaussianRadialExponential.integrable_exp_norm_sq_div_three_and_integral_stdGaussian node. The generic moment is reused, with no new public moment or tail wrapper.',
    'lean_statement': 'Each literal coordinate-row map pushes the fixed independent-column Gaussian product onto the row standard Gaussian and is measurable.',
    'lean_proof': 'Project Gaussian column coordinates, collect them under the finite product law, and wrap in Euclidean space. The private consumer transports the canonical exponential moment, applies Markov and finite subadditivity, then takes the measurable complement.',
    'boundary': boundary,
    'sources': [{**source, 'label': 'Appendix C.2 original row construction and cutoff event'},
                {'path': str(T), 'line': 14, 'label': 'Complete private same-experiment cutoff proof',
                 'scope': 'The exact simultaneous closed cutoff has probability at least999/1000 under the same column-product measure.'}],
    'tests': ['lake build Tests.GaussianComplexityFixedSpectrumSourceRowLaw'],
}
slug = 'huanjian-gaussian-source-row-law'
audit_id = 'ASTIS-RT-20261112-HuanjianGaussianSourceRowLaw'
lesson_path = Path('website/content/declaration_lessons') / (slug + '.json')
pub_path = Path('website/content/publications') / (slug + '.json')
audit_path = Path('research-wiki/semantic-roundtrip/audits') / (slug + '.json')
write(lesson_path, {'schema_version': 1, 'units': [unit]})
binding = {
    'declaration': name, 'cell': cell_path.stem, 'role': 'proof-edge',
    'supports': ['c2-original-coordinate-row-marginals'], 'boundary': boundary, 'audit_id': audit_id,
    'assumption_deltas': [
        {'source': 'Independent N(0,I_d) columns g_1,...,g_r with r=q+1 and standing 2q+1<d.',
         'lean': 'The literal finite product of r canonical standard d-dimensional Gaussian measures; natural q includes0.',
         'classification': 'same', 'reason': 'This is the canonical realization of the specified independent-column experiment. No transfer to every possible extended ambient probability space is claimed.'},
        {'source': 'The coordinate rows gamma_i=(g_1i,...,g_ri) have N(0,I_r) law; p1 also asserts their joint independence.',
         'lean': 'Every literal coordinate-row map is MeasurePreserving to the canonical row Gaussian.',
         'classification': 'same', 'reason': 'This binding covers the marginal-law subclaim only. Both measurability and map_eq are outputs. The stronger source joint-row independence claim remains outside this local obligation.'},
        {'source': 'p10 states probability at least0.999 for the all-row closed cutoff L=2r+3log(1000d).',
         'lean': 'The complete private consumer proves ofReal(999/1000)<=mu good in that same fixed product experiment.',
         'classification': 'source-implicit', 'reason': 'Exponential integrability, exact moment transport, strict tails, finite union and good-event measurability are proved internally. The union-bound expansion is explicitly an inference supporting the printed source probability.'},
    ],
}
item = {
    'id': slug, 'library': 'samplewiki', 'chapter': 'gaussian-sampling-complexity',
    'chapter_path': 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html',
    'title': title, 'source': source, 'statement': statement,
    'formulae': [{'label': 'Original experiment and row law', 'tex': formula},
                 {'label': 'Transported exponential moment', 'tex': moment_formula},
                 {'label': 'Same-experiment simultaneous cutoff', 'tex': good_formula}],
    'assumptions': assumptions,
    'obligations': [{'id': 'c2-original-coordinate-row-marginals', 'label': 'Each marginal row law in the source column-product realization, with a real same-experiment cutoff consumer.'}],
    'bindings': [binding],
}
write(pub_path, {'schema_version': 1, 'items': [item]})
binders, conclusion = seal['producer']['signature'].split(' :\n', 1)
literal = '∀ ' + binders + ',\n' + conclusion
source_text = (
    'For natural d and q with 2q+1<d, put r=q+1. Let g_1,...,g_r be independent '
    'standard Gaussian vectors in real d-dimensional Euclidean space, realized on their product probability space. '
    'For each i=1,...,d, the coordinate row (g_1i,...,g_ri) has the standard Gaussian law '
    'N(0,I_r) on real r-dimensional Euclidean space. This marginal-law subclaim includes the measurability '
    'needed for its pushforward interpretation and does not assert full joint-row independence.'
)
audit = {
    'id': audit_id, 'state': 'draft',
    'source': {'source_id': 'arxiv2610.20492v1-c2-source-coordinate-row-law',
               'url': source['url'], 'anchor': source['anchor'], 'original_text': source_text,
               'text_sha256': sha(source_text), 'source_snapshot_sha256': seal['source']['raw_sha256']},
    'lean': {'declaration': name, 'file': str(P), 'statement': literal, 'statement_sha256': sha(literal),
             'formalizer': 'huanjian_gc_20261112_source_row_law', 'compiled': True,
             'decoder_context': [
                 'Fin n has exactly the natural-number indices with value less than n. The natural-number coercion to real numbers is the usual one.',
                 'EuclideanSpace real (Fin n) is real n-dimensional Euclidean space. Its coordinates are indexed by Fin n. WithLp.toLp 2 converts a real coordinate function into this Euclidean vector, without changing any coordinate.',
                 'stdGaussian on a finite-dimensional real Euclidean space is its centered Gaussian probability measure with identity covariance.',
                 'Measure.pi assigns the finite product measure to the indicated family of probability measures. Its points are functions selecting one point of each factor, with the product measurable space.',
                 'MeasurePreserving f mu nu means that f is measurable and that the pushforward Measure.map f mu equals nu. It does not state that f is injective. Application omega a i takes coordinate i of the vector in factor a.',
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
cell['parents'] = [moment_parent]
cell['evidence']['actual_compilation'] = build
cell['evidence']['actual_kernel'] = kernel
cell['evidence']['actual_public_ASTIS_parents'] = parents
cell['evidence'].pop('target_proof_calls', None)
cell['evidence'].pop('new_target_proof_attempts', None)
cell['reuse_plan']['reused_declarations'] = [moment_parent, *mathlib]
cell['reuse_plan']['known_consumers'] = [private_name]
for key in ['source_ordered', 'source_statement_adjacent', 'natural_language_formula_proof',
            'hidden_assumptions_visible', 'lean_collapsed', 'external_dependencies_visible']:
    cell['reader_contract'][key] = True
cell['reader_contract']['status'] = 'Six adjacent source-ordered Lean folds, including the complete private same-experiment proof. Independent semantic and native/static reader acceptance pending.'
cell_path.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n')
publication.check_advance([name], reviewed=False)
packet = semantic.decoder_packet(audit)
neutral = Path('.astis/semantic-neutral-20261112/rl_decode_74bf/input.json')
write(neutral, packet)
write(evidence / 'decoder-input.json', packet)
record = {
    'producer_sha256': sha(P.read_bytes()), 'private_consumer_sha256': sha(T.read_bytes()),
    'build': build, 'kernel': kernel, 'actual_public_ASTIS_parents': parents,
    'both_exact_literal_types_kernel_applied': True, 'raw_Expr_structural_equality': False,
    'owned_theorems': 4, 'handwritten': 2, 'generated_internal': 2,
    'publication_binding_sha256': audit['publication_binding_sha256'],
    'neutral_input': str(neutral), 'neutral_input_raw_sha256': sha(neutral.read_bytes()),
    'neutral_canonical_packet_sha256': packet['packet_sha256'], 'anonymous_statement_sha256': sha(literal),
    'step_code_sha256': [sha(step['lean']) for step in steps], 'source_review': 'pending',
}
write(evidence / 'publication-draft-record.json', record)
print(json.dumps(record))
