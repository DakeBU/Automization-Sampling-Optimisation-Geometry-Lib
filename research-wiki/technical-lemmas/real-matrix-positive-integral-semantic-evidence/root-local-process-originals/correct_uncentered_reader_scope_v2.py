"""Correct the independent reader's precise scope finding; preserve all v1 inputs."""
from pathlib import Path
import hashlib
import json
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_publication as publication
import astis_semantic_roundtrip as semantic

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
ES = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
slug = 'huanjian-gaussian-source-matrix-variance'
lesson = Path('website/content/declaration_lessons') / (slug + '.json')
pub = Path('website/content/publications') / (slug + '.json')
audit_path = Path('research-wiki/semantic-roundtrip/audits') / (slug + '.json')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

paths = [lesson, pub, audit_path, E/'anti-anchored-reviewer-packet.json', E/'decoder-original-custody.json', E/'publication-draft-record.json', ES/'coupled-publication-draft-record.json', C]
originals = {}
for i, p in enumerate(paths):
    raw = p.read_bytes()
    dest = E / 'reader-scope-v1-originals' / (str(i) + '-' + p.name)
    create(dest, raw)
    originals[str(p)] = {'preserved_as': str(dest), 'sha256': sha(raw)}
old = 'Row law, fourth moment, frame, integrability, PSD and variance estimates are produced inside the proof.'
new = 'Row law, fourth moment, frame, integrability, and the uncentered squared-moment PSD estimate are proved internally.'
for p in (lesson, pub):
    text = p.read_text()
    assert text.count(old) == 1
    p.write_text(text.replace(old, new))
audit = json.loads(audit_path.read_bytes())
old_decoder = semantic.decoder_packet(audit)
old_source = audit['source']
old_lean = audit['lean']
old_binding = audit['publication_binding_sha256']
item = json.loads(pub.read_bytes())['items'][0]
binding = item['bindings'][0]
publication.inputs.cache_clear()
publication.load.cache_clear()
audit['publication_binding_sha256'] = publication.binding_digest(item, binding)
audit['publication_context'] = publication.review_context(item, binding)
assert audit['source'] == old_source and audit['lean'] == old_lean
assert semantic.decoder_packet(audit) == old_decoder
assert audit['publication_binding_sha256'] != old_binding
audit_path.write_bytes(dump(audit))
packet = semantic.semantic_reviewer_packet(audit)
new_packet = E / 'anti-anchored-reviewer-packet.v2.json'
create(new_packet, dump(packet))
record = {
    'kind': 'Independent final-reader finding and exact prose-only correction',
    'independent_actor': '/root/mv_fresh_source_6e28',
    'finding': 'Unqualified variance estimates in P assumptions overstates its actual uncentered-only source boundary.',
    'old': old, 'new': new, 'originals': originals,
    'old_publication_binding_sha256': old_binding,
    'publication_binding_sha256': audit['publication_binding_sha256'],
    'anti_anchored_packet': str(new_packet), 'anti_anchored_raw_sha256': sha(new_packet.read_bytes()),
    'anti_anchored_packet_sha256': packet['packet_sha256'],
    'same_anonymous_decoder_packet': True, 'same_source_and_Lean': True,
    'independent_source_acceptance': 'pending-v2', 'root_VERIFIED_calls': 0,
}
create(E / 'reader-scope-correction-v2.json', dump(record))
for path, key in [(E/'publication-draft-record.json', None), (ES/'coupled-publication-draft-record.json', 'actual_consumer')]:
    obj = json.loads(path.read_bytes())
    target = obj if key is None else obj[key]
    target['publication_binding_sha256'] = audit['publication_binding_sha256']
    target['reader_scope_correction'] = str(E/'reader-scope-correction-v2.json')
    path.write_bytes(dump(obj))
before = C.read_bytes()
cell = json.loads(before)
cell['evidence']['partial_public_producer_publication_binding_sha256'] = audit['publication_binding_sha256']
cell['evidence']['partial_public_producer_reader_scope_correction'] = str(E/'reader-scope-correction-v2.json')
C.write_bytes(dump(cell))
baseline_path = W/'candidate-boundary-v2.private.json'
b = json.loads(baseline_path.read_bytes())
assert b['all_existing_frontier_hashes'][str(C)] == sha(before)
b['all_existing_frontier_hashes'][str(C)] = sha(C.read_bytes())
q = b['qualification']['only_authorized_active_consumer_cell_delta']
q['after_sha256'] = sha(C.read_bytes())
q['changes'] += ' Successor prose-only independent reader correction updates the current P publication binding pointer; all v1 author/audit/anti inputs remain preserved byte-exact.'
b['qualification']['v2_boundary_preserved_sha256'] = sha(baseline_path.read_bytes())
b['qualification']['current_scope_correction'] = str(E/'reader-scope-correction-v2.json')
create(W/'candidate-boundary-v3.private.json', dump(b))
publication.check_advance([audit['lean']['declaration']], reviewed=False)
print(json.dumps(record))
