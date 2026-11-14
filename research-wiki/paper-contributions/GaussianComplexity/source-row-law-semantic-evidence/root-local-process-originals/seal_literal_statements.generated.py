"""Locate source formulas and the exact compiled proof and statement spans."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json

evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence')
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

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
paper = Path('research-wiki/paper-contributions/GaussianComplexity')
runner = Path('.astis/huanjian-resume-20261103')
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + chr(10)).encode()


def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)


def checked_run(stem):
    p = runner / (stem + '.receipt.json')
    b = p.read_bytes()
    r = json.loads(b)
    log = Path(r['log']).read_bytes()
    assert r['exit_code'] == 0 and sha(log) == r['log_sha256']
    return {'receipt': str(p), 'sha256': sha(b), 'log_sha256': sha(log)}, log


formation, formation_log = checked_run('20261112T050618966992Z-source-row-law-literal-Prop-formation')
meaning, meaning_log = checked_run('20261112T050850849746Z-source-row-law-complete-definition-meaning-v2')
environment_receipt, _ = checked_run('20261112T050703267089Z-source-row-law-exact-environment')
assert b'ProducerStatement : Prop' in formation_log and b'ConsumerStatement : Prop' in formation_log
for token in (b'MeasurePreserving.measurable', b'MeasurePreserving.map_eq',
              b'MeasureTheory.Measure.pi', b'isProbabilityMeasure_stdGaussian',
              b'Measure.pi.instIsProbabilityMeasure'):
    assert token in meaning_log, token
freezes = [
    (Path('.astis/semantic-neutral-20261112/rl_sg_6a90/freeze_manifest.json'),
     '236c0cd4dfeb3bd1c0a56ffd86e3b665b1bf333bb312c8df501cbc6848662439'),
    (Path('.astis/semantic-neutral-20261112/rl_tc_b7e1/raw-freeze-v1.json'),
     'f3177059c29c68676885a0a16201ab2d1a70ecc56417e82d666873cdcfe6aef7'),
]
raw_originals = {}
for p, digest in freezes:
    b = p.read_bytes()
    assert sha(b) == digest
    raw_originals[str(p)] = {'path': str(p), 'bytes': len(b), 'sha256': sha(b)}
    for item in json.loads(b)['artifacts']:
        original = Path(item['path'])
        content = original.read_bytes()
        assert len(content) == item['bytes'] and sha(content) == item['sha256'], str(original)
        relative = original.resolve().relative_to(Path.cwd().resolve())
        raw_originals[str(relative)] = {'path': str(relative), 'bytes': len(content), 'sha256': sha(content)}
create(workspace / 'actual-raw-freezes-rehashed.json', dump({
    'raw_originals': list(raw_originals.values()),
    'no_proposed_types_supplied_to_roles_yet': True,
}))
pi_source = Path('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean')
pi_raw = pi_source.read_bytes()
pi_lines = pi_raw.splitlines(keepends=True)
definition_excerpts = []
for first, last in [(99, 106), (208, 212)]:
    data = b''.join(pi_lines[first-1:last])
    definition_excerpts.append({
        'file': str(pi_source), 'file_sha256': sha(pi_raw), 'lines_1based': [first, last],
        'literal_source': data.decode(), 'literal_source_sha256': sha(data),
    })
context = {
    'allowed_only': 'Canonical definition semantics, actual current prints and standard source probability-space interpretation. No new target implementation or proof certificate.',
    'imports': ['import Mathlib', 'open MeasureTheory ProbabilityTheory'],
    'mathlib_pin': 'db584cd6d46c92f209a44c0f1c829460d327499d',
    'literal_current_prints_and_instances': meaning_log.decode(),
    'literal_current_prints_sha256': sha(meaning_log),
    'actual_current_print_receipt': meaning,
    'product_measure_literal_definition_excerpts': definition_excerpts,
    'definition_kinds': [
        {'object': 'D, E', 'kind': 'literal canonical Euclidean carriers', 'meaning': 'D has d real coordinates; E has q+1 real coordinates. Row squared norm is the Euclidean sum of coordinate squares.'},
        {'object': 'Omega', 'kind': 'literal finite function carrier', 'meaning': 'An outcome is a tuple of q+1 column vectors in D. It is not a single canonical row variable. No Gaussian law on the function carrier Omega is asserted.'},
        {'object': 'mu', 'kind': 'canonical finite product measure', 'meaning': 'Measure.pi of the actual standard Gaussian measures on D. Thus the q+1 columns follow the source independent standard d-Gaussian experiment. The actual product-probability and factor sigma-finiteness instances were synthesized, not taken as new inputs.'},
        {'object': 'row i', 'kind': 'literal source coordinates', 'meaning': 'The a-th coordinate is column a at physical coordinate i, rewrapped by WithLp.toLp2 into Euclidean row space. Source indices are i.val+1 and a.val+1.'},
        {'object': 'MeasurePreserving output', 'kind': 'standard output structure expanded', 'meaning': 'Both fields are conclusions: Measurable(row i) and Measure.map(row i)mu=stdGaussian E. This structure is not an assumption bundle.'},
        {'object': 'L and good', 'kind': 'literal source cutoff/event', 'meaning': 'L=2(q+1)+3log(1000d). All rows use the same outcome omega and the closed condition norm(row i omega)^2<=L. The complement is the strict any-bad event with norm squared>L.'},
        {'object': 'ENNReal.ofReal(999/1000)', 'kind': 'literal probability threshold', 'meaning': 'The positive real rational999/1000 is embedded into nonnegative extended reals. It is exactly the source0.999, with no change of normalization.'},
    ],
    'scope': 'Concrete original-column product experiment, marginal-law transport and global all-good event. No inference of full joint-row independence from marginal laws.',
}
producer = (workspace / 'producer-signature.draft.txt').read_bytes()
consumer = (workspace / 'consumer-signature.draft.txt').read_bytes()
assert not any(s in producer+consumer for s in (b':= by', b'sorry', b'axiom', b'admit'))
environment = json.loads((workspace / 'actual-environment-before-seal.json').read_bytes())
exposure = json.loads((workspace / 'preseal-exposure.json').read_bytes())
assert exposure['formalizer_API_pristine'] is False and exposure['new_target_proof_implementation_attempts'] == 0
anchors = [source_span(n) for n in [
    'S4.Thmtheorem3.p1', 'S4.Thmtheorem4.p1', 'A3.SS2.p1',
    'A3.SS2.p10', 'A3.Ex104.m1', 'A3.Ex105.m1',
]]
seal = {
    'schema_version': 1, 'seal_id': 'GAUSSIAN-COMPLEXITY-SOURCE-ROW-LAW-20261112-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'state': 'EXACT_LITERAL_PROPS_FORMED;UNPROVED;INDEPENDENT_TYPE_TOPOLOGY_PENDING',
    'source': {'version': 'arXiv2610.20492v1', 'raw': '.astis/huanjian-resume-20261103/2610.20492v1.html',
               'raw_sha256': sha(raw), 'anchors': anchors,
               'scope': 'C.2 p1 source rows and p10 printed all-good cutoff event, with standing integer query range.'},
    'producer': {
        'name': 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law',
        'planned_file': 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowLaw.lean',
        'signature': producer.decode(), 'signature_sha256': sha(producer),
        'outcome': 'Each actual coordinate-row map from the source independent-column experiment is measurable and transports its law to the canonical standard row Gaussian.',
    },
    'actual_private_consumer': {
        'name': 'AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceRowLaw.actual_original_all_good_cutoff_probability',
        'planned_file': 'Tests/GaussianComplexityFixedSpectrumSourceRowLaw.lean',
        'signature': consumer.decode(), 'signature_sha256': sha(consumer),
        'outcome': 'In that same original-column experiment, every row simultaneously lies below the source cutoff with probability at least999/1000.',
        'consumer_edge': 'Materially use the row-law producer and the existing canonical Gaussian exponential moment with integrability. Derive strict row tails, the finite bad-row union estimate and the closed-event complement internally.',
    },
    'binder_audit': [
        {'binder': 'd q : Nat', 'class': 'TYPING', 'meaning': 'Natural physical dimension and nonnegative integer query count, including q=0.'},
        {'binder': 'hq : 2*q+1<d', 'class': 'STANDING', 'meaning': 'Exact source range; positive d and positive row cardinality follow internally.'},
        {'binder': 'i : Fin d', 'class': 'TYPING', 'meaning': 'Every actual source row, with source index i.val+1.'},
        {'binder': 'all local lets', 'class': 'DEFINITION', 'meaning': 'Canonical column product law, literal coordinate row, radius/cutoff and global event, not additional inputs.'},
    ],
    'output_bundle_audit': {
        'name': 'MeasurePreserving',
        'fields': {'measurable': 'TARGET_CONCLUSION', 'map_eq': 'TARGET_CONCLUSION'},
        'extra_input_bundle': False,
    },
    'EXCESS_public_binders': [],
    'proof_components_forbidden_as_extra_binders': [
        'Row measurability or Gaussian pushforward certificate',
        'Column or row law/independence certificate for the fixed literal experiment',
        'Gaussian exponential moment, its integrability, Markov/tail bound or union-bound certificate',
        'Threshold positivity, tau-smallness, kappa bounds or q>0',
        'Measurable good-event or probability-normalization certificate',
    ],
    'shared_floor_audit': {
        'existing_canonical_consumer_parent': exposure['canonical_reuse_before_seal']['declaration'],
        'decision': 'Route-local source-experiment marginal adapter with actual global probability consumer. Reuse canonical Gaussian/product/measure-map substrate, not another exponential-moment theorem.',
        'actual_compiled_parent_edges': 'Pending new proof and kernel extraction.',
    },
    'scope_boundary': 'Marginal row-law transport for the concrete original independent-column experiment and the printed global truncation probability. Full joint-row independence, original matrix expectation adapters, public aggregate canonicalization, centered variance/concentration, both main bounds and exact oracle/precision/TV/cap/cost adapters, serialized reader/site integration and purification remain open.',
    'actual_statement_formation': formation, 'actual_definition_meaning': meaning,
    'actual_environment': environment, 'actual_environment_receipt': environment_receipt,
    'preseal_exposure': exposure, 'formalizer_API_pristine': False,
    'new_target_proof_implementation_attempts': 0,
    'preseal_corrections': [
        'The first private exposure-description draft incorrectly described an unsuccessful filename search as identifying the exponential module. It was corrected before the first seal, and the original draft plus actual subsequent signature lookup are retained.',
        'The first standard-definition print hid Measure.pi behind its irreducible implementation wrapper. Canonical construction excerpts and actual probability/sigma-finite instances supplement the complete version2 meaning context.',
    ],
    'minimal_definition_context_sha256': sha(dump(context)),
    'raw_source_freezes_rehashed_before_type_handoff': [str(p) for p,_ in freezes],
}
evidence.mkdir(exist_ok=False)
create(evidence / 'minimal-definition-context.json', dump(context))
create(evidence / 'actual-definition-meaning.log', meaning_log)
create(evidence / 'StatementFormation.lean.raw.txt', (workspace / 'StatementFormation.lean').read_bytes())
create(evidence / 'DefinitionMeaning.lean.raw.txt', (workspace / 'DefinitionMeaning.lean').read_bytes())
seal_raw = dump(seal)
seal_path = paper / 'source-row-law-statement-seal.json'
create(seal_path, seal_raw)
create(workspace / 'statement-seal-v1.json', seal_raw)
seal_path.chmod(0o444)
(workspace / 'statement-seal-v1.json').chmod(0o444)
packet = {
    'roles': 'Selective exact types and canonical meanings after separate independent raw-source freezes.',
    'producer': seal['producer'], 'actual_private_consumer': seal['actual_private_consumer'],
    'source': {'raw': seal['source']['raw'], 'sha256': sha(raw)},
    'minimal_definition_context': context,
    'statement_seal_sha256': sha(seal_raw),
    'minimal_definition_context_sha256': sha(dump(context)),
}
create(workspace / 'selective-type-definition-packet.json', dump(packet))
print(json.dumps({
    'seal': str(seal_path), 'seal_sha256': sha(seal_raw),
    'producer_signature_sha256': sha(producer), 'consumer_signature_sha256': sha(consumer),
    'context_sha256': sha(dump(context)), 'selective_packet_sha256': sha(dump(packet)),
    'raw_originals_rehashed': len(raw_originals),
}))
