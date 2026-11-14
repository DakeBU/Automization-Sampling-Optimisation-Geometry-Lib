from pathlib import Path
import hashlib, json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
sha = lambda b: hashlib.sha256(b.encode() if isinstance(b, str) else b).hexdigest()
def put(p, x):
    p = Path(p)
    assert not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n')
lp = Path('website/content/declaration_lessons/huanjian-fixed-spectrum-krylov-range.json')
pp = Path('website/content/publications/huanjian-fixed-spectrum-krylov-range.json')
ap = Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json')
old = E/'publication-attempt1-invalid-wording-enum-exact-hierarchy'
assert not old.exists()
old.mkdir()
for p in [lp, pp, ap, W/'author_publication.py']:
    q = old/p
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(p.read_bytes())
    q.chmod(0o444)
lesson, publication, audit = [json.loads(p.read_bytes()) for p in [lp, pp, ap]]
for source in [lesson['units'][0]['sources'][0], publication['items'][0]['source']]:
    assert source['wording_status'] == 'faithful paraphrase with explicit pointwise deterministic-start generalization'
    source['wording_status'] = 'faithful paraphrase'
    source['pointwise_generalization_disclosure'] = 'The extracted range identity is proved for arbitrary deterministic starts, as supported by the source polynomial proof; source Gaussian context and downstream stochastic estimates remain separate. See the assumption ledger and remaining boundary.'
for p, x in [(lp, lesson), (pp, publication)]:
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n')
item = publication['items'][0]
binding = item['bindings'][0]
pub.inputs.cache_clear()
pub.load.cache_clear()
audit['publication_binding_sha256'] = pub.binding_digest(item, binding)
audit['publication_context'] = pub.review_context(item, binding)
ap.write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
pub.check_advance([binding['declaration']], reviewed=False)
packet = rt.decoder_packet(audit)
neutral = Path('.astis/semantic-neutral-20261111/p_kr_91de5a')
put(neutral/'input.json', packet)
put(E/'decoder-input.json', packet)
k = json.loads((E/'actual-kernel-owned-inventory.json').read_bytes())
s = json.loads((W/'statement-seal-v1.json').read_bytes())
records = []
for step in lesson['units'][0]['steps']:
    code = step['lean']
    candidates = []
    for key in ['producer', 'actual_private_consumer']:
        p = Path(s[key]['planned_file'])
        text = p.read_text()
        if code in text:
            candidates.append({'file': str(p), 'line': text[:text.index(code)].count('\n')+1, 'code_sha256': sha(code), 'exact_contiguous_source': True})
    assert len(candidates) == 1
    records.extend(candidates)
record = {'producer_raw_sha256': k['actual_producer_sha256'], 'Test_raw_sha256': k['actual_Test_sha256'], 'producer_signature_sha256': s['producer']['signature_sha256'], 'private_consumer_signature_sha256': s['actual_private_consumer']['signature_sha256'], 'publication_binding_sha256': audit['publication_binding_sha256'], 'anonymous_statement_sha256': audit['lean']['statement_sha256'], 'anonymous_packet_canonical_sha256': packet['packet_sha256'], 'neutral_input': str(neutral/'input.json'), 'neutral_input_raw_sha256': sha((neutral/'input.json').read_bytes()), 'exact_step_code_records': records, 'actual_first_public_ASTIS_parents': k['actual_first_public_ASTIS_parents'], 'actual_owned_declarations': 4, 'handwritten': 2, 'generated_auxiliaries': 2, 'all_owned_reachable': True, 'source_review': 'pending', 'decoder': 'pending', 'sourceV_global_Goal_complete': False, 'archive_attempt2_failure': 'The first archive attempt used colliding basenames for lesson/publication/audit; it stopped at the second read-only destination before any source metadata mutation. Original failed script, receipt and first copied lesson retained. Corrected archive preserves exact directory hierarchy.', 'attempt1_failure': 'Invalid non-enum source.wording_status. Original three metadata files and script retained byte-exact; qualification remains explicit in source metadata, assumption deltas, proof and boundary. No Lean or sealed signature changed.'}
put(E/'publication-draft-record.json', record)
print(json.dumps(record))
