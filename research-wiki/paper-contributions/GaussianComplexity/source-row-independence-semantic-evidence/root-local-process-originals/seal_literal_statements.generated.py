"""Locate source formulas and the exact compiled proof and statement spans."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json

evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence')
raw = Path('.astis/huanjian-resume-20261103/2610.20492v1.html').read_bytes()
text = raw.decode()
sha = lambda data: hashlib.sha256(data).hexdigest()
assert sha(raw) == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
offsets = [0] + [i + 1 for i, char in enumerate(text) if char == '\n']


class SourceElements(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.elements = {}

    def source_offset(self):
        line, col = self.getpos()
        return offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, dict(attrs).get('id'), self.source_offset()))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, identifier, start = self.stack[i]
                if identifier:
                    self.elements[identifier] = (start, text.index('>', self.source_offset()) + 1)
                del self.stack[i:]
                return


parser = SourceElements()
parser.feed(text)


def source_span(identifier):
    first, last = parser.elements[identifier]
    data = text[first:last].encode()
    a, b = len(text[:first].encode()), len(text[:last].encode())
    assert raw[a:b] == data and f'id="{identifier}"'.encode() in data
    return {
        'source_id': identifier, 'char_start': first, 'char_end': last,
        'raw_utf8_start': a, 'raw_utf8_end': b,
        'lf_line_start': text.count('\n', 0, first) + 1,
        'lf_column0_start': first - text.rfind('\n', 0, first) - 1,
        'lf_line_end': text.count('\n', 0, last) + 1, 'span_sha256': sha(data),
    }




from datetime import datetime, timezone
import subprocess

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
paper = Path('research-wiki/paper-contributions/GaussianComplexity')
runner = Path('.astis/huanjian-resume-20261103')
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + chr(10)).encode()


def create(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(data)


def checked_run(stem):
    path = runner / (stem + '.receipt.json')
    data = path.read_bytes()
    receipt = json.loads(data)
    log = Path(receipt['log']).read_bytes()
    assert receipt['exit_code'] == 0 and sha(log) == receipt['log_sha256']
    return {'receipt': str(path), 'sha256': sha(data), 'log_sha256': sha(log)}, log


formation, formation_log = checked_run('20261112T074709253066Z-source-row-independence-final-literal-Prop-formation-v4')
meaning, meaning_log = checked_run('20261112T074709253067Z-source-row-independence-complete-definition-meaning-v2')
environment_receipt, _ = checked_run('20261112T074338227880Z-source-row-independence-exact-environment-before-seal')
assert b'proposedIndependentRows : Prop' in formation_log
assert b'proposedIndependentTruncatedMatrices : Prop' in formation_log
for token in (b'ProbabilityTheory.Kernel.iIndepSets', b'MeasurableSpace.comap',
              b'MeasurableSpace.pi', b'Matrix.kronecker', b'Measure.pi.instIsProbabilityMeasure'):
    assert token in meaning_log
body = (workspace / 'StatementFormation.lean').read_text()
sections = []
for name in ['proposedIndependentRows', 'proposedIndependentTruncatedMatrices']:
    section = body.split('def ' + name + ' : Prop :=\n', 1)[1]
    section = section.split('\ndef ', 1)[0].split('\n#check ', 1)[0].rstrip() + '\n'
    assert section.startswith('  ∀ {d q : ℕ} (hq : 2 * q + 1 < d),\n')
    signature = section.replace('  ∀ {d q : ℕ} (hq : 2 * q + 1 < d),\n',
                                '{d q : ℕ} (hq : 2 * q + 1 < d) :\n', 1)
    sections.append(signature)
producer, consumer = [s.encode() for s in sections]
assert not any(token in producer + consumer for token in (b':= by', b'sorry', b'axiom', b'admit'))
assert '(∀ i : Fin d, Measurable (Y i)) ∧ iIndepFun Y μ' in sections[1]

sg = Path('.astis/semantic-neutral-20261112/ri_sg_78c2/raw-freeze-v1/frozen-manifest.json')
tc = Path('.astis/semantic-neutral-20261112/ri_tc_24a6/raw-freeze.json')
assert sha(sg.read_bytes()) == '2bdc92ca14e919b33ec81f8480e8782bf0fe16e94fca4442e2f1e15ad040b351'
assert sha(tc.read_bytes()) == 'dc5f3b9278a7fe8d3eac246c794f0832ca157f4d9cf3b9c52443c28444e70ee9'
raw_originals = []
for path in [sg, tc]:
    raw_originals.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())})
for item in json.loads(sg.read_bytes())['files']:
    path = sg.parent / item['path']
    data = path.read_bytes()
    assert len(data) == item['bytes'] and sha(data) == item['sha256']
    raw_originals.append({'path': str(path), 'bytes': len(data), 'sha256': sha(data)})
for item in json.loads(tc.read_bytes())['local_records']:
    path = Path(item['path'])
    data = path.read_bytes()
    assert len(data) == item['bytes'] and sha(data) == item['sha256']
    raw_originals.append({'path': str(path), 'bytes': len(data), 'sha256': sha(data)})
create(workspace / 'actual-raw-preparations-rehashed.json', dump({
    'independent_originals': raw_originals, 'new_types_not_yet_supplied': True,
    'topology_accepted': False,
}))
excerpts = []
for filename, windows in [
    ('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean', [(99, 106), (208, 212)]),
    ('.lake/packages/mathlib/Mathlib/Probability/Independence/Basic.lean', [(92, 100), (104, 114), (131, 139)]),
]:
    path = Path(filename)
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    for first, last in windows:
        span = b''.join(lines[first-1:last])
        excerpts.append({'file': str(path), 'file_sha256': sha(data), 'lines_1based': [first, last],
                         'literal_source': span.decode(), 'literal_source_sha256': sha(span)})
context = {
    'allowed_only': 'Literal standard definition semantics and actual current prints/instances. No new target proof or theorem certificate.',
    'mathlib_pin': 'db584cd6d46c92f209a44c0f1c829460d327499d',
    'literal_current_prints_and_instances': meaning_log.decode(),
    'literal_current_prints_sha256': sha(meaning_log), 'actual_print_receipt': meaning,
    'literal_definition_excerpts': excerpts,
    'definition_kinds': [
        {'object': 'D,E,Omega,mu,row', 'kind': 'literal', 'meaning': 'd-dimensional standard Gaussian columns on their finite product; coordinate row in Euclidean(q+1)-space, source indices a.val+1 and i.val+1. No Gaussian law on an Omega function norm is asserted.'},
        {'object': 'iIndepFun', 'kind': 'canonical standard predicate expanded', 'meaning': 'Independence of the inverse-image sigma-algebras, hence factorization for every finite intersection of measurable row events. The implementation expands through Kernel.iIndepFun/iIndep/iIndepSets and a constant kernel on Unit under dirac(). It is not pairwise independence only, does not assert injectivity or identical distribution, and by itself does not assert measurability of arbitrary maps.'},
        {'object': 'L,theta,t', 'kind': 'literal', 'meaning': 'L=2(q+1)+3log(1000d), theta_i=(i.val+1-1/2)pi/d, feature0=1 and featurek=sqrt2cos(k theta_i). No Gram or norm bound is an input.'},
        {'object': 'Y matrix carrier', 'kind': 'literal finite entry array', 'meaning': 'A real matrix is definitionally a function of two finite paired indices. The explicit function carrier exposes its canonical product measurable structure without an opaque local type alias or additional typeclass hypothesis. The Gaussian coordinate precedes the feature coordinate in both paired indices. No matrix operator-norm assertion is made by this independence statement.'},
        {'object': 'Y entries', 'kind': 'literal', 'meaning': 'The closed cutoff selects inverse-d times the Kronecker product of actual Gaussian-row and deterministic-feature outer products; outside the event it is zero, exactly the source indicator. This is not an existence/default definition.'},
        {'object': 'private consumer conjunction', 'kind': 'two target conclusions', 'meaning': 'All actual Y maps are measurable AND the entire family is iIndepFun under that same mu. Neither measurability nor independence is a new input certificate. The matrices need not be identically distributed because features vary with i.'},
    ],
}
exposure = {
    'formalizer_API_pristine': False, 'new_target_proof_implementation_attempts': 0,
    'known_before_first_seal': [
        'The formalizer proved/inspected prior canonical Gaussian, cosine, fourth-moment, weighted-frame and original-row-law packets; their whole code/proof API context is known.',
        'The same exact compiled original-row marginal theorem and its measurable output are known; joint independence is not inferred from those marginals.',
        'Preseal source-only reading covered C.2p1,p10,p12,p13,p14 and Ex107. Existing row-template formulas are known from prior packets.',
        'Only this new target literal Prop formation and standard definition expansion were attempted. No target proof API/implementation search or target proof was started.',
        'Definition lookup Independence.Basic92-143 included the adjacent Indep/IndepSet standard definitions. Kernel wrappers and finite product construction meanings were printed/read. No independence proof body was opened in this lookup.',
    ],
    'preseal_formation_history': [
        'Attempt1: local Matrix alias had no synthesized family MeasurableSpace; rejected.',
        'Attempt2: adding a local inferred product measurable-space let caused an auxiliary kernel declaration type mismatch; rejected.',
        'Attempt3: explicit finite real-entry function carrier formed both Props successfully. Before the first seal, the real private consumer was strengthened to include its source-implicit measurability output.',
        'Final attempt4: both final Props formed successfully, with unchanged producer and measurable-and-independent private consumer. All prior formation sources and actual receipts retained; no proof result is claimed from these definitions.',
        'First definition print exposed standard independence kernel wrappers; version2 fully expands them, with product-measure constructor excerpts supplementing irreducible Measure.pi.',
    ],
}
seal = {
    'schema_version': 1, 'seal_id': 'GAUSSIAN-COMPLEXITY-SOURCE-ROW-INDEPENDENCE-20261112-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'state': 'EXACT_LITERAL_PROPS_FORMED;UNPROVED;INDEPENDENT_GRAPH_TYPE_TOPOLOGY_PENDING',
    'current_HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    'source': {'version': 'arXiv2610.20492v1', 'raw': '.astis/huanjian-resume-20261103/2610.20492v1.html',
               'raw_sha256': sha(raw), 'anchors': [source_span(i) for i in [
                   'S4.Thmtheorem4.p1', 'S4.E11.m1', 'A3.SS2.p1', 'A3.SS2.p10',
                   'A3.SS2.p12.1', 'A3.Ex107.m1']],
               'scope': 'Full physical-row joint independence in the canonical column experiment and actual Ex107 truncated-matrix independence.'},
    'producer': {
        'name': 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence.actual_source_rows_independent',
        'planned_file': 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowIndependence.lean',
        'signature': producer.decode(), 'signature_sha256': sha(producer),
    },
    'actual_private_consumer': {
        'name': 'AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceRowIndependence.actual_truncated_matrices_measurable_and_independent',
        'planned_file': 'Tests/GaussianComplexityFixedSpectrumSourceRowIndependence.lean',
        'signature': consumer.decode(), 'signature_sha256': sha(consumer),
        'consumer_edge': 'Material use of the new joint-independence producer for actual Ex107 Yi. Derive measurable matrix maps internally; reuse the existing canonical row-law node for row measurability if needed, with no premise certificate.',
    },
    'binder_audit': [
        {'binder': 'd q : Nat', 'class': 'TYPING', 'meaning': 'Physical dimension and nonnegative integer query count; q=0 included.'},
        {'binder': 'hq : 2*q+1<d', 'class': 'STANDING', 'meaning': 'Exact source range. Positive d and row cardinality follow internally.'},
        {'binder': 'all local lets', 'class': 'DEFINITION', 'meaning': 'Literal canonical probability space, rows, threshold, grid/features and matrix maps, not additional data or hypotheses.'},
    ],
    'output_bundle_audit': {'input_bundle': False, 'producer': 'iIndepFun is the target finite-family independence predicate.',
                            'consumer_fields': {'all_Y_measurable': 'TARGET_CONCLUSION', 'iIndepFun_Y': 'TARGET_CONCLUSION'}},
    'EXCESS_public_binders': [],
    'proof_components_forbidden_as_extra_binders': [
        'Row or coordinate independence certificate', 'Joint-law or column-law certificate for the fixed literal product experiment',
        'Row or matrix-map measurability certificate', 'Feature Gram/norm, threshold positivity or concentration certificate',
        'Tau-smallness, kappa bound, q>0 or additional regularity',
    ],
    'shared_floor_audit': {
        'known_existing_node': 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law',
        'decision': 'Complement the existing marginal law with genuinely new joint independence; use it on literal Yi rather than a wrapper assumption bundle.',
        'actual_compiled_parent_edges': 'Unproved; extract only after actual new kernel bodies exist.',
    },
    'scope_boundary': 'Same canonical independent-column experiment only. No arbitrary extended-ambient transfer, matrix expectation/centered variance/concentration, full Lemma4.4, main lower bounds or oracle/TV/precision/cap/cost result. Serialized integration, actual rendered public reader and purification remain open.',
    'actual_statement_formation': formation, 'actual_definition_meaning': meaning,
    'actual_environment': json.loads((workspace / 'actual-environment-before-seal.json').read_bytes()),
    'actual_environment_receipt': environment_receipt,
    'preseal_exposure': exposure, 'formalizer_API_pristine': False,
    'new_target_proof_implementation_attempts': 0,
    'minimal_definition_context_sha256': sha(dump(context)),
    'source_preparation_chronology': 'Raw reading/inventory and a clearly unaccepted preliminary draft precede this seal; formal graph/type/topology admission starts only after this seal. No raw preparation is recertified as admitted topology.',
}
assert not evidence.exists()
evidence.mkdir()
create(evidence / 'minimal-definition-context.json', dump(context))
create(evidence / 'actual-definition-meaning.log', meaning_log)
create(evidence / 'StatementFormation.lean.raw.txt', (workspace / 'StatementFormation.lean').read_bytes())
create(evidence / 'DefinitionMeaning.lean.raw.txt', (workspace / 'DefinitionMeaning.lean').read_bytes())
seal_raw = dump(seal)
seal_path = paper / 'source-row-independence-statement-seal.json'
create(seal_path, seal_raw)
create(workspace / 'statement-seal-v1.json', seal_raw)
create(workspace / 'preseal-exposure.json', dump(exposure))
for path in [seal_path, workspace / 'statement-seal-v1.json']:
    path.chmod(0o444)
packet = {
    'roles': 'Exact sealed types and canonical definition semantics; no implementation/proof/audit verdict.',
    'producer': seal['producer'], 'actual_private_consumer': seal['actual_private_consumer'],
    'binder_audit': seal['binder_audit'], 'output_bundle_audit': seal['output_bundle_audit'],
    'EXCESS_public_binders': [], 'minimal_definition_context': context,
    'source': seal['source'], 'statement_seal_sha256': sha(seal_raw),
    'minimal_definition_context_sha256': sha(dump(context)), 'formalizer_API_pristine': False,
}
create(workspace / 'selective-type-definition-packet.json', dump(packet))
print(json.dumps({'seal': str(seal_path), 'seal_sha256': sha(seal_raw),
                  'producer_signature_sha256': sha(producer), 'consumer_signature_sha256': sha(consumer),
                  'context_sha256': sha(dump(context)), 'selective_packet_sha256': sha(dump(packet)),
                  'raw_originals_rehashed': len(raw_originals), 'topology_accepted': False,
                  'new_target_proof_implementation_attempts': 0}))
