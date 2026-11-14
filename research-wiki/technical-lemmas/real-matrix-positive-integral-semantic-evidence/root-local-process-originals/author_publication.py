"""Author separate background and concrete-source lessons/audits for the two compiled nodes."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_publication as publication
import astis_semantic_roundtrip as semantic

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
shared_evidence = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
route_evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
shared_cell = Path('research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json')
route_cell = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
runner = Path('.astis/huanjian-resume-20261103')
sha = lambda b: hashlib.sha256(b.encode() if isinstance(b, str) else b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(dump(value))

def receipt(stem):
    path = runner / (stem + '.receipt.json')
    raw = path.read_bytes()
    obj = json.loads(raw)
    log = Path(obj['log']).read_bytes()
    assert obj['exit_code'] == 0 and sha(log) == obj['log_sha256']
    return {'path': str(path), 'sha256': sha(raw), 'log_sha256': sha(log)}, log.decode()

seal = json.loads((workspace / 'statement-seal-v1.json').read_bytes())
S, P = [Path(seal[k]['planned_file']) for k in ('producer', 'actual_consumer')]
text_s, text_p = S.read_text(), P.read_text()
name_s, name_p = [seal[k]['name'] for k in ('producer', 'actual_consumer')]
for key, text in [('producer', text_s), ('actual_consumer', text_p)]:
    short = seal[key]['name'].split('.')[-1]
    assert text.split('theorem ' + short + '\n', 1)[1].split(':= by\n', 1)[0] == seal[key]['signature']
snapshots = json.loads(Path('.astis/semantic-neutral-20261112/mv_src_6e28/shared-code-only-inputs-v1/input-manifest.json').read_bytes())
for p in (S, P, Path('Tests/RealMatrixPositiveIntegral.lean')):
    entry = next(x for x in snapshots['entries'] if x['source'] == str(p))
    assert sha(p.read_bytes()) == entry['sha256']
build, _ = receipt('20261112T145727632793Z-real-matrix-positive-integral-focused-build')
producer_build, _ = receipt('20261112T145113476724Z-real-matrix-positive-integral-producer-real-star-import-v2')
consumer_build, _ = receipt('20261112T145435349586Z-real-matrix-positive-integral-actual-source-consumer-firstbuild')
kernel, log = receipt('20261112T145804292918Z-real-matrix-positive-integral-exact-literal-kernel-and-canonical-calls')
parents_p = [
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law',
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment.actual_radial_fourth_moment_matrix',
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound.actual_weighted_cosine_coefficient_bound',
    name_s,
]
parents = {name_s: [], name_p: parents_p}
for target, required in parents.items():
    assert 'ACTUAL_SEALED_LITERAL_KERNEL_TYPE_APPLICATION_PASS ' + target in log
    start = log.index('ACTUAL_PUBLIC_ASTIS_PARENTS ' + target + ': [')
    stop = log.index(']', start)
    assert all(p in log[start:stop] for p in required)
assert 'ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED 4' in log
assert 'ACTUAL_RAW_LITERAL_EXPR_EQUALITY ' + name_s + ': true' in log
assert 'ACTUAL_RAW_LITERAL_EXPR_EQUALITY ' + name_p + ': false' in log

def code(text, first, last):
    return ''.join(text.splitlines(keepends=True)[first - 1:last])

boundary_s = ('Explicit ASTIS-authored shared background, with probability/integrability/AE-PSD contracts on arbitrary f. '
    'The full PSD cone geometry is proved internally. Empty finite matrix indices are included. '
    'This is a specialization of the fixed upstream closed-convex integral theorem, not a printed arbitrary-f Gaussian-paper theorem or a source repair. '
    'The concrete original-experiment uncentered bound is an actual consumer with its own source binding. '
    'The later centered/weighted source variance, concentration, both main lower bounds and oracle/TV/precision/cap/cost adapters remain open. '
    'Serialized integration, actual desktop/mobile/MathJax/global source-index/graph/copy/download/public delivery and purification remain open.')
boundary_p = ('Only the actual original-column uncentered squared-moment integrability and PSD bound are proved here. '
    'The exact original R9 producer signature is unchanged, including q=0 and sole source inequality2q+1<d. '
    'The new shared positivity interface is materially called on an internally integrable pointwise PSD residual. '
    'The real centered and cosine-weighted centered variance operator-norm consumer is still unimplemented and the full R9 SAU remains EXPLORING. '
    'No Bernstein, full Lemma4.4, ambient transfer, main lower bound, exact oracle/TV/precision/cap/cost, serialized integration, actual public-reader delivery or purification credit is claimed.')
source_s = {
    'url': 'https://github.com/leanprover-community/mathlib4/blob/db584cd6d46c92f209a44c0f1c829460d327499d/Mathlib/Analysis/Convex/Integral.lean#L57',
    'edition': 'ASTIS-authored matrix specialization; external source Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d, source SHA1b3115887fabf0dccc2fed689d1f1ddc7a114b5de4594e752c02908a445aafb4',
    'anchor': 'Authored finite-real-matrix PSD-cone specialization of Convex.integral_mem lines46-83; arXiv2610.20492v1 C.2 p14 supplies concrete application need only',
    'wording_status': 'licensed original', 'attribution': 'ASTIS-authored reusable background; upstream closed-convex integral theorem is Mathlib.',
    'scope': 'Generic probability expectation positivity, with cone geometry proved, distinct from the concrete source calculation.',
}
source_p = {
    'url': 'https://arxiv.org/html/2610.20492v1#A3.SS2.p14',
    'edition': 'arXiv:2610.20492v1; pinned HTML SHA256 ' + seal['source']['raw_sha256'],
    'anchor': 'Appendix C.2 p14 Ex113-117, actual Ex107 local cutoff, original p1 product experiment and Fact C.5 unweighted frame',
    'wording_status': 'faithful paraphrase', 'attribution': 'On Complexity of Gaussian Sampling, arXiv:2610.20492v1.',
    'scope': 'Actual uncentered squared-moment sum only; p14 centered/weighted conclusions and p15 Bernstein remain separate.',
}
formula_s = r'f\in L^1(\mu),\quad f(\omega)\succeq0\ \mu\text{-a.e.}\quad\Longrightarrow\quad\int f\,d\mu\succeq0.'
formula_p = r'Y_i^2\in L^1(\mu)\quad(1\le i\le d),\qquad\sum_{i=1}^d\mathbb E_\mu[Y_i^2]\preceq\frac{2r(r+2)}d I_{r^2}.'
assumptions_s = [
    r'Let \(n\) be a finite index set, possibly empty, and let \((\Omega,\mu)\) be any measurable probability space. The function \(f\) takes values in real \(n\)-by-\(n\) matrices.',
    r'The explicit authored contracts are \(f\in L^1(\mu)\) and \(f(\omega)\succeq0\) almost everywhere. Integrability includes an a.e. strongly measurable representative and finite extended-norm integral.',
    r'Here \(A\succeq0\) means both \(A^\top=A\) and \(v^\top A v\ge0\) for every finite vector. Positivity is full matrix PSD, rather than entrywise positivity.',
    r'The matrix space uses its complete Euclidean operator norm and the integral is Bochner. No caller-supplied closed/convex cone, pointwise measurability, nonempty matrix index or representative certificate is required.',
    r'This arbitrary-function background statement is authored explicitly. Concrete Gaussian consumers prove its contracts internally; the original Gaussian Source Anchor gains no new premise.',
]
assumptions_p = [
    r'Let \(d,q\in\mathbb N\) satisfy \(2q+1<d\), and put \(r=q+1\). The case \(q=0\) is included. All denominator positivity follows internally.',
    r'Use exactly \(\Omega=(\mathbb R^d)^r\), \(\mu=\gamma_d^{\otimes r}\), and the actual physical row \(\Phi_i(\omega)=(\omega_{1,i},\ldots,\omega_{r,i})\), with \(\gamma_j=N(0,I_j)\). No replacement row experiment or caller law certificate is used.',
    r'Put \(\theta_i=(i-\tfrac12)\pi/d\), \(t_i=(1,\sqrt2\cos\theta_i,\ldots,\sqrt2\cos(q\theta_i))\), \(R_i=\|\Phi_i\|^2\) and \(L=2r+3\log(1000d)\). Source physical index \(i\) corresponds to \(i.val+1\).',
    r'The literal matrix is \(Y_i=d^{-1}(\Phi_i\Phi_i^\top\otimes t_it_i^\top)\mathbf1_{\{R_i\le L\}}\), with the Gaussian coordinate first in each paired Kronecker index. Each row keeps its own inclusive cutoff, under the same unconditional original law.',
    r'Squares use ordinary matrix multiplication, and expectations are actual Bochner integrals in the Euclidean operator norm. Every squared summand is proved integrable. Full Hermitian/quadratic PSD is used throughout.',
    r'The only source proposition input is \(2q+1<d\). Row law, fourth moment, frame, integrability, PSD and variance estimates are produced inside the proof. Joint independence, exact first-mean/a identities, \(\tau\), \(\kappa\), and Bernstein assumptions are not inputs.',
]
steps_s = [
    {'title': 'Fix the full PSD cone and the actual integral contract',
     'text': 'Use the literal finite real matrix space and the genuine integrable, a.e. PSD function. The full signature permits empty finite indices. Its standard operator-norm and completeness instances are synthesized internally.',
     'formula': r'\mathcal P=\{A:A^\top=A,\ v^\top A v\ge0\ \text{for every }v\}.', 'lean': code(text_s, 1, 26)},
    {'title': 'Prove the cone closed in the declared topology',
     'text': 'Hermitian matrices form the equalizer of continuous star and identity. For every fixed finite vector, its quadratic evaluation is continuous and the nonnegative half-line is closed. Intersect these closed conditions; no cone-geometry certificate is a public input.',
     'formula': r'\mathcal P=\{A:A^\top=A\}\cap\bigcap_v\{A:v^\top A v\ge0\}.', 'lean': code(text_s, 27, 38)},
    {'title': 'Use convexity and the canonical probability integral theorem',
     'text': 'Nonnegative scalar combinations of full PSD matrices remain PSD, proving convexity. Apply the existing closed-convex integral theorem to the actual a.e. membership and integrability hypotheses. The proof does not strengthen a.e. positivity to pointwise positivity.',
     'formula': r'a,b\ge0,\ a+b=1,\ A,B\in\mathcal P\Longrightarrow aA+bB\in\mathcal P,\qquad\int f\,d\mu\in\mathcal P.', 'lean': code(text_s, 39, 44)},
]
steps_p = [
    {'title': 'Transport the canonical fourth moment to the actual physical rows',
     'text': 'Keep the complete original source statement and experiment. Reuse the canonical actual-row law and the existing integrable radial fourth-moment matrix. The noninjective row pushforward transports that moment to the actual same product measure. A fixed continuous tensor map yields the untruncated majorants and their integrability; the actual row cutoff is measurable.',
     'formula': r'(\Phi_i)_\#\mu=\gamma_r,\qquad\mathbb E_{\gamma_r}[\|x\|^2xx^\top]=(r+2)I_r,\quad W_i=\frac{\|t_i\|^2}{d^2}(R_i\Phi_i\Phi_i^\top\otimes t_it_i^\top).', 'lean': code(text_p, 1, 107)},
    {'title': 'Compute both ordinary rank-one squares and prove squared integrability',
     'text': 'Use the Gaussian and feature rank-one square identities and Kronecker multiplication. The literal squared matrix is exactly its untruncated majorant retained on its own closed cutoff. Indicator integrability therefore follows from actual majorant integrability.',
     'formula': r'(xx^\top)^2=\|x\|^2xx^\top,\quad(t_it_i^\top)^2=\|t_i\|^2t_it_i^\top,\quad Y_i^2=W_i\mathbf1_{\{R_i\le L\}}.', 'lean': code(text_p, 108, 145)},
    {'title': 'Apply the shared node to the actual PSD residual',
     'text': 'The untruncated majorant is a nonnegative multiple of the actual tensor-vector outer product. Thus W_i minus Y_i squared is PSD pointwise. Prove both finite sums integrable and call the shared lemma on their actual difference. This does not assume pointwise PSD of the final C I minus the random square sum.',
     'formula': r'W_i-Y_i^2\succeq0,\qquad\int\!\left(\sum_iW_i-\sum_iY_i^2\right)d\mu\succeq0.', 'lean': code(text_p, 146, 179)},
    {'title': 'Evaluate the majorant mean and consume the canonical frame bound',
     'text': 'Commute the fixed continuous tensor maps and finite sums with the actual integrals. The transported fourth moment evaluates the majorant expectation. Normalize the algebraically equal midpoint-grid expressions and apply the existing weighted coefficient bound, then add the integrated PSD residual to obtain the stated uncentered bound.',
     'formula': r'\mathbb E_\mu W_i=\frac{(r+2)\|t_i\|^2}{d^2}(I_r\otimes t_it_i^\top),\qquad\sum_i\mathbb E_\mu W_i\preceq\frac{2r(r+2)}dI_{r^2}.', 'lean': code(text_p, 180, 216)},
]
mathlib_s = ['Convex.integral_mem', 'Matrix.posSemidef_iff_dotProduct_mulVec', 'Matrix.PosSemidef.smul', 'Matrix.PosSemidef.add']
mathlib_p = ['MeasureTheory.MeasurePreserving.integrable_comp_of_integrable', 'MeasureTheory.integral_map', 'ContinuousLinearMap.integrable_comp', 'ContinuousLinearMap.integral_comp_comm', 'Matrix.kroneckerBilinear', 'Matrix.vecMulVec_mul_vecMulVec', 'Matrix.mul_kronecker_mul', 'MeasureTheory.Integrable.indicator', 'MeasureTheory.integrable_finsetSum', 'MeasureTheory.integral_finsetSum', 'MeasureTheory.integral_sub']
definitions_s = [
    'A finite type has a finite set of indices and may be empty. DecidableEq is a decision procedure for equality on that finite index set.',
    'Matrix n n real is the finite real two-index matrix space, here with the complete Euclidean operator norm. Scalar multiplication multiplies each entry.',
    'Matrix.PosSemidef A means that A is Hermitian and its quadratic form is nonnegative for every finitely supported vector. For finite real matrices Hermitian means transpose A equals A and the quadratic test is the ordinary test on all finite vectors.',
    'The notation almost everywhere with respect to a measure permits an exceptional null set. MeasurableSpace is the chosen sigma algebra and IsProbabilityMeasure means the whole space has measure one.',
    'Integrable f mu means almost-everywhere strong measurability and finite integral of the extended norm. The integral notation is the Bochner integral, totalized to zero outside complete or integrable cases. The explicit integrability hypothesis is part of the contract.',
]
definitions_p = [
    'Fin n is the finite index set of natural numbers less than n. Natural numbers embed into real numbers in the usual way.',
    'EuclideanSpace real (Fin n) is real n-dimensional Euclidean space with its Euclidean norm and Borel structure. WithLp.toLp 2 wraps a coordinate function as that vector and WithLp.ofLp recovers the same coordinates.',
    'stdGaussian on finite-dimensional real Euclidean space is the centered Gaussian probability law with identity covariance. Measure.pi is the finite product measure with its product measurable structure.',
    'Real.log is the natural logarithm and Real.sqrt the nonnegative square root. An if-expression with a real inequality uses that exact condition, including equality in a less-than-or-equal condition.',
    'Matrix.vecMulVec u v has entry u_i times v_j. Matrix.kronecker A B has paired indices with entry A_(i,k) times B_(j,l) at ((i,j),(k,l)). Matrix multiplication is ordinary finite matrix multiplication, not entrywise multiplication. The symbol 1 is the identity matrix.',
    'Matrix.PosSemidef A includes both Hermitian symmetry and nonnegative quadratic form for all finitely supported vectors; on a finite real index set this is ordinary symmetric positive semidefiniteness.',
    'Matrix integrals use the complete Euclidean operator norm and the Bochner integral. Integrable means almost-everywhere strong measurability and finite extended-norm integral; it is an asserted output wherever displayed. The integral is totalized to zero when not integrable, so the explicit integrability outputs are substantive.',
]
source_text_s = ('ASTIS-authored background statement, specializing the fixed upstream closed-convex probability integral theorem to the full finite real PSD matrix cone. '
    'Let n be any finite index type, including the empty type, and let Omega be any measurable space with a probability measure mu. '
    'Let f map Omega to real n-by-n matrices equipped with the Euclidean operator norm. Assume f is Bochner integrable and is Hermitian positive semidefinite mu-almost everywhere. '
    'Then the actual Bochner integral of f is Hermitian positive semidefinite. Closedness and convexity of that concrete cone are proved internally. '
    'This arbitrary-function statement is authored background, not a printed general theorem in the Gaussian paper, and its hypotheses are not new hypotheses of the concrete Gaussian theorem.')
source_text_p = ('For natural d,q with 2q+1<d set r=q+1. Take exactly r independent standard d-dimensional Gaussian columns with their product probability measure mu. '
    'Let gamma_i be their actual physical row. Put theta_i=(i-1/2)pi/d, t_i=(1,sqrt(2)cos(theta_i),...,sqrt(2)cos(q theta_i)), R_i=norm(gamma_i)^2 and L=2r+3log(1000d). '
    'Define Y_i as inverse-d times gamma_i gamma_i-transpose tensor t_i t_i-transpose on the closed event R_i<=L, and zero outside. '
    'Every actual ordinary matrix square Y_i squared is Bochner integrable. The sum over physical rows of its actual expectations is bounded above in full PSD order by (2r(r+2)/d) times the identity matrix of size r squared. '
    'This binding stops at the uncentered bound of Ex115-117. Centered variance, weighted centered variance and matrix concentration are separate unfinished claims.')
configs = [
    {'slug': 'huanjian-real-matrix-positive-integral', 'audit_id': 'ASTIS-RT-20261112-HuanjianRealMatrixPositiveIntegral', 'name': name_s, 'file': S, 'cell': shared_cell, 'title': 'Probability expectations preserve full real matrix positivity', 'statement': 'An integrable, almost-everywhere positive semidefinite real matrix map has a positive semidefinite probability expectation.', 'formula': formula_s, 'assumptions': assumptions_s, 'steps': steps_s, 'source': source_s, 'boundary': boundary_s, 'astis': [], 'mathlib': mathlib_s, 'definition_context': definitions_s, 'source_text': source_text_s, 'seal_key': 'producer', 'formalizer': 'huanjian_20261112_real_matrix_positive_integral', 'evidence': shared_evidence, 'obligation': 'shared-real-matrix-positive-integral', 'delta': [
        {'source': 'The fixed upstream theorem accepts an integrable, AE-valued function into a closed convex set in a complete real normed space under a probability measure.', 'lean': 'Specialize the space to finite real matrices and the set to the full PSD cone, proving its closedness and convexity internally.', 'classification': 'same', 'reason': 'Explicit authored specialization of the cited general theorem; no cone geometry certificate becomes a public input.'},
        {'source': 'The paper p14 supplies concrete PSD expectation applications, not an arbitrary-function theorem.', 'lean': 'The reusable arbitrary-f theorem is separately authored, with probability, integrability and AE full PSD as genuine generic contracts.', 'classification': 'generalization', 'reason': 'This is disclosed authored background, not a source repair or a new printed primary result. Concrete Gaussian consumers establish all generic contracts inside their unchanged source proof.'},
    ]},
    {'slug': 'huanjian-gaussian-source-matrix-variance', 'audit_id': 'ASTIS-RT-20261112-HuanjianGaussianSourceMatrixVarianceUncentered', 'name': name_p, 'file': P, 'cell': route_cell, 'title': 'Actual Gaussian truncated matrix second moments', 'statement': 'Every actual squared truncated summand is integrable, and the sum of its expectations has the exact source PSD upper bound.', 'formula': formula_p, 'assumptions': assumptions_p, 'steps': steps_p, 'source': source_p, 'boundary': boundary_p, 'astis': parents_p, 'mathlib': mathlib_p, 'definition_context': definitions_p, 'source_text': source_text_p, 'seal_key': 'actual_consumer', 'formalizer': 'huanjian_gc_20261112_source_matrix_variance', 'evidence': route_evidence, 'obligation': 'c2-actual-source-uncentered-second-moments', 'delta': [
        {'source': 'Original independent standard Gaussian columns, natural q>=0 and2q+1<d, actual physical rows and exact source midpoint features/local cutoff.', 'lean': 'Literal canonical column-product realization, actual row projections and exact inclusive truncated matrices, including q=0.', 'classification': 'same', 'reason': 'No alternate law, extra query restriction, row-law/moment/frame/PSD certificate or ambient transfer is introduced.'},
        {'source': 'Ex115-117 integrate actual ordinary Y_i squared and derive the upper PSD coefficient2r(r+2)/d.', 'lean': 'All actual squared maps are Bochner integrable as explicit outputs, and the full Hermitian/quadratic PSD difference is proved.', 'classification': 'source-implicit', 'reason': 'Integrability and the full PSD integration bridge are proved internally for the fixed variables. Source proof ingredients are dependency edges, never new public assumptions.'},
    ]},
]
records = []
for idx, cfg in enumerate(configs):
    unit = {'kind': 'theorem', 'reading_layout': 'progressive', 'declaration': cfg['name'], 'title': cfg['title'], 'reader_note': 'Open assumptions and source-ordered proof steps for the full conditions and adjacent exact Lean.', 'statement': cfg['statement'], 'formula': cfg['formula'], 'assumptions': cfg['assumptions'], 'steps': cfg['steps'], 'astis_dependencies': cfg['astis'], 'mathlib_dependencies': cfg['mathlib'], 'dependency_notes': 'Exact common compiled declarations remain canonical once. The shared producer has no ASTIS parent; the concrete source consumer materially uses it and the existing row-law, fourth-moment and weighted-frame nodes. Planned centered use is not a current compiled call.', 'lean_statement': cfg['statement'], 'lean_proof': 'See the complete source-ordered formula steps and exact Lean folds.', 'boundary': cfg['boundary'], 'sources': [{**cfg['source'], 'label': cfg['source']['anchor']}, {'path': str(cfg['file']), 'line': 18 if idx == 0 else 19, 'label': 'Complete exact compiled declaration source', 'scope': cfg['boundary']}], 'tests': ['lake build Tests.RealMatrixPositiveIntegral']}
    if idx == 0:
        unit['sources'].append({'path': str(P), 'line': 19, 'label': 'Actual original-experiment uncentered consumer', 'scope': 'Its own source binding proves integrability and uncentered PSD domination; full centered R9 remains unfinished.'})
    lesson_path = Path('website/content/declaration_lessons') / (cfg['slug'] + '.json')
    pub_path = Path('website/content/publications') / (cfg['slug'] + '.json')
    audit_path = Path('research-wiki/semantic-roundtrip/audits') / (cfg['slug'] + '.json')
    write(lesson_path, {'schema_version': 1, 'units': [unit]})
    binding = {'declaration': cfg['name'], 'cell': cfg['cell'].stem, 'role': 'proof-edge', 'supports': [cfg['obligation']], 'boundary': cfg['boundary'], 'audit_id': cfg['audit_id'], 'assumption_deltas': cfg['delta']}
    item = {'id': cfg['slug'], 'library': 'samplewiki', 'chapter': 'gaussian-sampling-complexity', 'chapter_path': 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html', 'title': cfg['title'], 'source': cfg['source'], 'statement': cfg['statement'], 'formulae': [{'label': cfg['title'], 'tex': cfg['formula']}], 'assumptions': cfg['assumptions'], 'obligations': [{'id': cfg['obligation'], 'label': cfg['statement']}], 'bindings': [binding]}
    write(pub_path, {'schema_version': 1, 'items': [item]})
    binders, conclusion = seal[cfg['seal_key']]['signature'].split(' :\n', 1)
    literal = '∀ ' + binders + ',\n' + conclusion
    audit = {'id': cfg['audit_id'], 'state': 'draft', 'source': {'source_id': cfg['obligation'], 'url': cfg['source']['url'], 'anchor': cfg['source']['anchor'], 'original_text': cfg['source_text'], 'text_sha256': sha(cfg['source_text']), 'source_snapshot_sha256': '1b3115887fabf0dccc2fed689d1f1ddc7a114b5de4594e752c02908a445aafb4' if idx == 0 else seal['source']['raw_sha256']}, 'lean': {'declaration': cfg['name'], 'file': str(cfg['file']), 'statement': literal, 'statement_sha256': sha(literal), 'formalizer': cfg['formalizer'], 'compiled': True, 'decoder_context': cfg['definition_context']}, 'reconstruction': {}, 'semantic_slots': {}, 'deltas': [], 'verdict': 'pending', 'source_review': {'state': 'pending'}, 'repairs': []}
    publication.inputs.cache_clear()
    publication.load.cache_clear()
    audit['publication_binding_sha256'] = publication.binding_digest(item, binding)
    audit['publication_context'] = publication.review_context(item, binding)
    write(audit_path, audit)
    packet = semantic.decoder_packet(audit)
    neutral = Path('.astis/semantic-neutral-20261113/n_decode_mp_6a17') / ('a.json' if idx == 0 else 'b.json')
    write(neutral, packet)
    write(cfg['evidence'] / 'decoder-input.json', packet)
    record = {'declaration': cfg['name'], 'file': str(cfg['file']), 'file_sha256': sha(cfg['file'].read_bytes()), 'source_audit': cfg['audit_id'], 'publication_binding_sha256': audit['publication_binding_sha256'], 'neutral_input': str(neutral), 'neutral_input_raw_sha256': sha(neutral.read_bytes()), 'neutral_canonical_packet_sha256': packet['packet_sha256'], 'anonymous_statement_sha256': sha(literal), 'source_review': 'pending', 'step_code_sha256': [sha(x['lean']) for x in cfg['steps']], 'actual_ASTIS_parents': cfg['astis']}
    write(cfg['evidence'] / 'publication-draft-record.json', record)
    records.append(record)

# Shared cell current metadata; historical intake bytes/zero counts stay in originals.
cs = json.loads(shared_cell.read_bytes())
cs['evidence']['actual_compilation'] = producer_build
cs['evidence']['actual_material_consumer_compilation'] = consumer_build
cs['evidence']['actual_focused_build'] = build
cs['evidence']['actual_kernel'] = kernel
cs['evidence']['actual_public_ASTIS_parents'] = parents
cs['evidence'].pop('new_shared_target_proof_attempts', None)
cs['evidence'].pop('target_proof_calls', None)
cs['reuse_plan']['reused_declarations'] = mathlib_s
cs['reuse_plan']['known_consumers'] = [name_p]
cs['reuse_plan']['planned_consumers'] = [x for x in cs['consumers'] if x != name_p]
for key in ['source_ordered', 'source_statement_adjacent', 'natural_language_formula_proof', 'hidden_assumptions_visible', 'lean_collapsed', 'external_dependencies_visible']:
    cs['reader_contract'][key] = True
cs['reader_contract']['status'] = 'Three exact initially closed shared proof folds and separately bound four-fold actual source consumer. Independent decoding/source/native/reader acceptance pending.'
shared_cell.write_bytes(dump(cs))

# This active source consumer is owned by the same sole root worker. Record its
# partial producer progress honestly, while retaining every original baseline.
route_before = route_cell.read_bytes()
cp = json.loads(route_before)
assert cp['advance_id'] == 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
cp['evidence']['partial_public_producer_compilation'] = consumer_build
cp['evidence']['partial_public_producer_kernel'] = kernel
cp['evidence']['partial_public_producer_ASTIS_parents'] = parents_p
cp['evidence']['partial_public_producer_publication_binding_sha256'] = records[1]['publication_binding_sha256']
cp['evidence']['remaining_private_consumer_unimplemented'] = True
cp['evidence'].pop('new_target_proof_attempts', None)
cp['evidence'].pop('target_proof_calls', None)
cp['reader_contract']['status'] = 'Only the public uncentered producer has a four-fold lesson and compiled proof. Full centered/weighted private consumer, whole-SAU source/native acceptance and reader delivery remain pending.'
route_cell.write_bytes(dump(cp))
write(workspace / 'active-consumer-cell-before-publication-update.original.json', json.loads(route_before))
qualification = {'kind': 'Authorized metadata progress in ROOT own active Gaussian consumer cell; not another owner or completed frontier', 'path': str(route_cell), 'before_sha256': sha(route_before), 'after_sha256': sha(route_cell.read_bytes()), 'status_unchanged': cp['status'], 'source_statement_and_seal_unchanged': True, 'source_SAU_still_EXPLORING': True, 'private_centered_consumer_not_claimed': True, 'changes': 'Only partial public-producer compilation/kernel/publication pointers and an honest reader-scope note; preproof zero counts remain in original admission artifacts. No ledger transition or source binder changes.'}
write(shared_evidence / 'authorized-active-consumer-cell-metadata-update.json', qualification)
baseline_path = workspace / 'preproof-baseline.private.json'
baseline_raw = baseline_path.read_bytes()
baseline = json.loads(baseline_raw)
assert baseline['all_existing_frontier_hashes'][str(route_cell)] == sha(route_before)
for p, digest in baseline['all_existing_frontier_hashes'].items():
    if p != str(route_cell):
        assert sha(Path(p).read_bytes()) == digest
baseline['all_existing_frontier_hashes'][str(route_cell)] = sha(route_cell.read_bytes())
baseline['qualification'] = {'kind': 'Post-mathematics candidate boundary; NOT a rewritten preproof baseline', 'original_preproof_baseline': str(baseline_path), 'original_sha256': sha(baseline_raw), 'only_authorized_active_consumer_cell_delta': qualification, 'all_other_468_regular_frontiers_preserved': True, 'all_foreign_advance_and_discovery_states_unchanged': True}
write(workspace / 'candidate-boundary-v2.private.json', baseline)
publication.inputs.cache_clear()
publication.load.cache_clear()
publication.check_advance([name_s, name_p], reviewed=False)
write(shared_evidence / 'coupled-publication-draft-record.json', {'producer': records[0], 'actual_consumer': records[1], 'build': build, 'producer_build': producer_build, 'consumer_first_build': consumer_build, 'kernel': kernel, 'actual_public_ASTIS_parents': parents, 'owned_mathematics': {'handwritten': 2, 'generated': 2, 'all4_reachable': True, 'shared_module': '1 handwritten +1 generated', 'actual_consumer_module': '1 handwritten +1 generated'}, 'raw_Expr_equality': {name_s: True, name_p: False}, 'generic_empty_index_and_source_q0_kernel_applications': True, 'source_SAU_state': 'EXPLORING; full centered consumer unimplemented', 'normal_VERIFIED_calls_by_root': 0})
print(json.dumps({'publication_records': records, 'shared_lines': len(text_s.splitlines()), 'actual_consumer_lines': len(text_p.splitlines()), 'all_new_public_declarations_have_separate_source_bindings': True, 'normal_VERIFIED_calls': 0}))
