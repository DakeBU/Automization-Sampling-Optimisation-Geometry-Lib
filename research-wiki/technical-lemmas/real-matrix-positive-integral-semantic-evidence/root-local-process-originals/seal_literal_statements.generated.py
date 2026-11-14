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
import subprocess

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
seal_path = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-statement-seal.json')
runner = Path('.astis/huanjian-resume-20261103')
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + chr(10)).encode()

def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

formation_path = runner / '20261112T141642155267Z-real-matrix-positive-integral-literal-Prop-formation.receipt.json'
formation_raw = formation_path.read_bytes()
formation = json.loads(formation_raw)
formation_log = Path(formation['log']).read_bytes()
assert formation['exit_code'] == 0 and sha(formation_log) == formation['log_sha256']
for token in [b'Matrix.instL2OpNormedRing', b'Matrix.instL2OpNormedSpace', b'Matrix.instCompleteSpace']:
    assert token in formation_log
producer = (workspace / 'producer-signature.original.txt').read_bytes()
source_seal_path = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json')
source_seal_raw = source_seal_path.read_bytes()
assert sha(source_seal_raw) == '5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14'
source_seal = json.loads(source_seal_raw)
consumer = source_seal['producer']
context_path = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/minimal-definition-context.json')
context = json.loads(context_path.read_bytes())
assert sha(context_path.read_bytes()) == source_seal['minimal_definition_context_sha256']
context['shared_bridge_meaning'] = {
    'classification': 'ASTIS-authored reusable background; NOT a verbatim or equivalent general theorem printed in the paper.',
    'n_Omega_mu_f': 'Arbitrary finite real square-matrix index set (empty allowed), arbitrary measurable sample space, arbitrary probability measure and actual matrix-valued function under the L2Operator norm.',
    'hf': 'Genuine analytic hypothesis for the arbitrary-function background theorem: Integrable f mu expands to AE strongly measurable representative and finite extended norm integral. Every concrete Gaussian consumer must prove it internally.',
    'hpos': 'Genuine arbitrary-function background hypothesis: AE full PosSemidef(f omega), recursively Hermitian plus nonnegative finite quadratic form. AE means the exceptional set is mu-null. It is never added to the sealed concrete Gaussian theorem.',
    'conclusion': 'The actual Bochner integral is full Hermitian positive semidefinite, not just entrywise nonnegative. Integrability prevents a default-zero proof for a nonintegrable function.',
    'consumer': 'The exact already-sealed actual original-experiment squared-moment target is unchanged. Its pointwise PSD residual and integrability are internal evidence to supply at this shared lemma application. The later actual centered and weighted square integrals are a second real consumer family, without any newly added source binder.',
}
process_path = Path('research-wiki/process-memory.json')
process_raw = process_path.read_bytes()
process = json.loads(process_raw)
memory = {'source': str(process_path), 'source_sha256': sha(process_raw),
          'entries_read': [x['id'] for x in process['entries']],
          'applicable_standing_or_negative_entry_ids': [], 'control_plane_math_authority': False,
          'decision': 'No current process/negative entry decides this arbitrary finite real-matrix positivity theorem. Actual measure roles remain explicit.'}
exposure = {
    'formalizer_API_pristine': False,
    'known_context': ['Prior compiled R4/R5 private consumers already contain local closed/convex PSD-set applications of Convex.integral_mem; their complete proofs and APIs were known before this shared target selection.', 'Post-seal/admission R9 API search inspected the same local proofs and pinned Mathlib CFC/Matrix order/integrability APIs; real Matrix lacks the complex CStarAlgebra hypotheses of the direct norm shortcut. Generic real CFC norm APIs exist and remain separate from this positivity bridge.', 'Exact ASTIS/Mathlib/frontier name searches did not identify a public integral_posSemidef provider; no preseal pristine or independent rediscovery claim.'],
    'new_shared_target_proof_implementation_attempts': 0,
    'selection': 'Multiple real consumers require one shared canonical positivity-integral node, rather than another private duplicate of the cone application. Existing historical private code remains untouched.',
    'R9_newtarget_API_search_chunks_before_shared_selection': ['d75a9e', '8da081', '9f06b5', 'd88481', '92ed31', 'd7822c', 'fc8763', '26065b', 'b663b0', '8ab0b6', '357313', '91d02b', '2b3e45', '2777c9', '326d48', '1d0bc1'],
    'honest_search_qualification': 'The first R9 technical-library rg was overbroad and output-truncated; several guessed source paths did not exist. No missing full stdout/hash is invented and no API or environment failure is a mathematical refutation.',
}
seal = {
    'schema_version': 1, 'seal_id': 'SHARED-REAL-MATRIX-POSITIVE-INTEGRAL-20261112-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'state': 'EXACT_LITERAL_PROPS_FORMED;UNPROVED;INDEPENDENT_BACKGROUND_TYPE_TOPOLOGY_PENDING',
    'current_HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    'classification': 'ASTIS-authored shared background bridge, not a new printed primary-paper theorem, source repair or extra Gaussian premise.',
    'source': {'version': 'arXiv2610.20492v1', 'raw': '.astis/huanjian-resume-20261103/2610.20492v1.html',
               'raw_sha256': sha(raw), 'anchors': [source_span(x) for x in ['A3.SS2.p14', 'A3.Ex115.m1', 'A3.Ex118.m1', 'A3.Ex120.m1']],
               'scope': 'Omitted integration-of-PSD residual/square step in the source calculation; arbitrary-function probability lemma is an explicitly authored general background expansion.'},
    'producer': {'name': 'AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef',
                 'planned_file': 'AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveIntegral.lean',
                 'signature': producer.decode(), 'signature_sha256': sha(producer)},
    'actual_consumer': consumer,
    'consumer_existing_exact_seal': {'file': str(source_seal_path), 'sha256': sha(source_seal_raw), 'unchanged': True},
    'binder_audit': [
        {'binder': 'n,Omega:Type*,Fintype n,DecidableEq n,MeasurableSpace Omega', 'class': 'TYPING', 'meaning': 'Finite real square matrices and measurable sample carrier; no dimension positivity or nonempty restriction.'},
        {'binder': 'mu:Measure Omega, IsProbabilityMeasure mu', 'class': 'AUTHORED_BACKGROUND_HYPOTHESIS', 'meaning': 'Arbitrary probability law for this generic background theorem, exactly available internally for both actual product-Gaussian consumers.'},
        {'binder': 'f:Omega->Matrix n n Real', 'class': 'TYPING', 'meaning': 'Arbitrary actual matrix random variable, no placeholder expected matrix.'},
        {'binder': 'hf:Integrable f mu', 'class': 'AUTHORED_BACKGROUND_HYPOTHESIS', 'meaning': 'Genuine integrability contract on arbitrary f. Not an input of the sealed Gaussian theorem; its proof derives this for each concrete application.'},
        {'binder': 'hpos:AE PosSemidef(f omega)', 'class': 'AUTHORED_BACKGROUND_HYPOTHESIS', 'meaning': 'AE full Hermitian/quadratic positivity of arbitrary f. No project-owned bundle remains unexpanded; each concrete Gaussian consumer proves it internally.'},
    ],
    'EXCESS_public_binders': [],
    'output_bundle_audit': {'input_project_bundle': False, 'output': 'Full PosSemidef of the actual integrable Bochner expectation.'},
    'shared_floor_audit': {'decision': 'new_canonical_shared',
        'canonical_shared_cell': 'ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL',
        'searched': ['Samplinglib/ASTIS exact public theorem searches found no integral_posSemidef provider; existing R4/R5 historical private cone applications are not public providers.', 'Pinned Mathlib Analysis.Matrix.Order, Matrix.PosDef and CFC sources provide matrix positivity/order primitives; Convex.integral_mem is the existing canonical general integral provider. A public real-matrix PSD specialization with proved cone applicability is absent from the actual searched floor.'],
        'actual_consumers': [consumer['name'], source_seal['actual_private_consumer']['name']],
        'decision_reason': 'One public canonical finite-real-matrix positivity integration interface supplies actual uncentered residual and actual centered/weighted-square expectations; old private application histories stay intact. No algorithmic implication or PBPS/SPHMC dependency is asserted.'},
    'scope_boundary': 'Shared mathematical background only. No concrete Gaussian moment identity, source variance bound, complex-matrix generality, concentration, main lower bound, integration/publication/purification or Goal completion follows from this generic lemma alone. Actual consumer is sealed but not yet implemented.',
    'actual_statement_formation': {'receipt': str(formation_path), 'sha256': sha(formation_raw), 'log_sha256': sha(formation_log)},
    'actual_definition_meaning_reused_exactly': source_seal['actual_definition_meaning'],
    'actual_environment': json.loads((workspace / 'actual-environment-before-seal.json').read_bytes()),
    'process_memory_readback': memory, 'preseal_exposure': exposure,
    'formalizer_API_pristine': False, 'new_shared_target_proof_implementation_attempts': 0,
    'minimal_definition_context_sha256': sha(dump(context)),
    'chronology': 'The actors already froze original p14 source independently for R9. The new generic background statement is selected explicitly by ROOT after actual floor search; no claim that the source independently printed this arbitrary-f theorem. Exact new type/topology review follows this seal, before a new shared-target proof implementation.',
}
assert not evidence.exists() and not Path(seal['producer']['planned_file']).exists()
create(evidence / 'minimal-definition-context.json', dump(context))
create(evidence / 'StatementFormation.lean.raw.txt', (workspace / 'StatementFormation.lean').read_bytes())
seal_raw = dump(seal)
for p in [seal_path, workspace / 'statement-seal-v1.json']:
    create(p, seal_raw)
    p.chmod(0o444)
create(workspace / 'process-memory-readback.json', dump(memory))
create(workspace / 'preseal-exposure.original.json', dump(exposure))
packet = {key: seal[key] for key in ['classification', 'source', 'producer', 'actual_consumer', 'consumer_existing_exact_seal', 'binder_audit', 'EXCESS_public_binders', 'output_bundle_audit', 'scope_boundary']}
packet.update({'roles': 'Exact background and unchanged concrete consumer types/definitions only; no new-target implementation or previous reviewer verdict.', 'minimal_definition_context': context, 'statement_seal_sha256': sha(seal_raw), 'minimal_definition_context_sha256': sha(dump(context)), 'formalizer_API_pristine': False})
packet_raw = dump(packet)
create(workspace / 'selective-type-definition-packet.json', packet_raw)
print(json.dumps({'seal': str(seal_path), 'seal_sha256': sha(seal_raw), 'producer_signature_sha256': sha(producer), 'context_sha256': sha(dump(context)), 'packet_sha256': sha(packet_raw), 'new_shared_target_proof_implementation_attempts': 0}))
