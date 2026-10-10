from pathlib import Path
import copy, hashlib, json, os, sys

root = Path.cwd()
sys.path.insert(0, str(root / 'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
import astis_advance as adv

r = Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72')
o = r / 'independent-source72'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def check(b, z):
    assert len(b) == z['raw_bytes'] and sha(b) == z['raw_sha256'], z['path']
    lf = b.replace(b'\r\n', b'\n')
    assert len(lf) == z['lf_bytes'] and sha(lf) == z['lf_sha256'], z['path']

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b), LF_sha256=sha(b.replace(b'\r\n', b'\n')))

def write(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

def new(p, x):
    assert not Path(p).exists(), p
    write(p, x)

lease = load(o / 'lease.final.json')
assert sha((o / 'lease.final.json').read_bytes()) == '3beaf636af477be8cf53add22555f5a228d9f68e0c530d1e5baf191c734c8580'
assert lease['status'] == 'CLOSED_LAST' and lease['terminal_exit_code'] == 0
assert lease['closed_file_count'] == 258 and not lease['old_CLOSED_and_canonical_writes']
manifest = load(o / 'native.manifest.json')
assert sha((o / 'native.manifest.json').read_bytes()) == lease['manifest_RAW_sha256']
assert sha(can(manifest['entries'])) == manifest['logical_manifest_sha256'] == lease['manifest_logical_entries_sha256']
files = {p.relative_to(o).as_posix(): p for p in o.rglob('*') if p.is_file()}
assert len(files) == 258 and set(files) == {z['path'] for z in manifest['entries']} | {'native.manifest.json', 'lease.final.json'}
for z in manifest['entries']:
    check(files[z['path']].read_bytes(), z)
    assert files[z['path']].stat().st_mtime_ns <= files['lease.final.json'].stat().st_mtime_ns
run = load(o / 'source72.run.json')
h = sha(can({k: v for k, v in run.items() if k != 'run_sha256'}))
assert h == run['run_sha256'] == lease['run_sha256'] == '9db1799a86b5da0b17347fc961698c4117991d97f49c03e3458910801d46fda0'
assert run['reviewer'] == 'independent_primary69' and not run['canonical_or_old_closed_writes']
assert run['coverage'] == dict(source_items=361, NODE=239, EXCLUDED=122, source_nodes=24, source_edges=53, source_formulas=20, source_obligations=27, module_lines=494, BODY_spans=[6, 4], blocking_deltas=[0, 0])
payload_path = o / 'complete-named-review-decision-input-payload.json'
assert sha(payload_path.read_bytes()) == lease['complete_named_payload_RAW_sha256'] == '032eabcc5a75557227bf7a09e82c2dc6828624af33c3d86906940f9f0e844a41'
payload = load(payload_path)
assert payload['native_whole_logical_run_sha256'] == h
for name, z in payload['named_files'].items():
    b = (o / name).read_bytes()
    assert z['RAW_utf8'].encode() == b and z['RAW_sha256'] == sha(b) and z['RAW_bytes'] == len(b), name
for z in payload['manifest']['files'] + payload['finite_coverage_pins'] + run['input_manifests'] + run['coverage_artifacts']:
    check(Path(z['path']).read_bytes(), z)

overlay = load(r / 'root.reader-status-overlay72.adoption.json')
approved_current = {z['path']: z['RAW_sha256'] for z in overlay['exact_current'] + overlay['audits']}
for z in overlay['exact_current'] + overlay['audits']:
    assert sha(Path(z['path']).read_bytes()) == z['RAW_sha256']
versions = []
for name in ['preparation.inputs.json', 'StageB.current-inputs.manifest.json', 'StageB.final-current-inputs.manifest.json', 'StageB.overlay-history.inputs.json']:
    data = load(o / name)
    for z in data['inputs']:
        current = Path(z['path']).read_bytes()
        if 'raw_snapshot' in z:
            check((o / z['raw_snapshot']).read_bytes(), z)
            lf = (o / z['lf_snapshot']).read_bytes()
            assert len(lf) == z['lf_bytes'] and sha(lf) == z['lf_sha256'] and b'\r\n' not in lf
        if sha(current) != z['raw_sha256']:
            assert name == 'StageB.current-inputs.manifest.json' and approved_current.get(z['path']) == sha(current), z['path']
            versions.append(dict(path=z['path'], historical_RAW_sha256=z['raw_sha256'], approved_current_RAW_sha256=sha(current), historical_manifest=name))
        else:
            check(current, z)
    if 'primary_reference_only' in data:
        check(Path(data['primary_reference_only']['path']).read_bytes(), data['primary_reference_only'])
assert len(versions) == 8
plan = load(r / 'publication-plan.json')
claim = load(r / 'claim.json')
assert adv.current_advances()[claim['advance_id']]['state'] == 'EXPLORING'
assert load(r / 'root.math72.adoption.json')['native_files'] == 82
assert load(r / 'root.decoder72.adoption.json')['native_owned_files'] == 5
accepted_audits = []
canonical = []
for i, (slug, aid, cid) in enumerate(zip(plan['slugs'], plan['audit_ids'], plan['active_cells'])):
    ap = Path('research-wiki/semantic-roundtrip/audits') / (aid + '.json')
    cp = Path('research-wiki/frontier-cells') / (cid + '.json')
    pp = Path('website/content/publications') / (slug + '.json')
    audit, cell, publication = load(ap), load(cp), load(pp)
    packet = load(r / f'source-review.packet.{i+2}.json')
    decision = load(o / f'source.{i}.decision.json')
    admission = load(o / f'source.{i}.admission-fields.json')
    assert audit['state'] == 'blind-reconstructed' and rt.semantic_reviewer_packet(audit) == packet
    assert decision['verdict'] == 'equivalent-after-elaboration' and decision['blocking_deltas'] == 0 and not decision['repairs']
    assert decision['independent_from_formalizer'] and decision['independent_from_decoder'] and decision['review_run_sha256'] == h
    assert len(decision['deltas']) == [5, 11][i] and all(z['severity'] == 'informational' for z in decision['deltas'])
    assert set(decision['semantic_slots']) == set(rt.SEMANTIC_SLOTS)
    assert all(z['relation'] != 'not-audited' and z['evidence'] for z in decision['semantic_slots'].values())
    assert packet['packet_sha256'] == admission['official_packet_sha256'] == decision['reviewer_packet_sha256']
    assert sha((r / f'source-review.packet.{i+2}.json').read_bytes()) == admission['official_packet_RAW_sha256']
    assert audit['publication_binding_sha256'] == admission['publication_binding_sha256'] == decision['publication_binding_sha256']
    accepted = copy.deepcopy(audit)
    accepted.update(admission['audit_fields'])
    assert rt.semantic_reviewer_packet(accepted) == packet
    cell['source_proof_coverage'] = admission['cell_source_proof_coverage']
    publication['items'][0]['source_proof_coverage'] = admission['publication_source_proof_coverage']
    accepted_audits.append(accepted)
    canonical.append((ap, cp, pp, accepted, cell, publication))
registry = rt.load_registry()
byid = {a['id']: a for a in accepted_audits}
registry['audits'] = [byid.get(x['id'], x) for x in registry['audits']]
errors = rt.validate_registry(registry)
assert not errors, errors
for i, (ap, cp, pp, accepted, cell, publication) in enumerate(canonical):
    for p, kind in [(ap, 'audit'), (cp, 'cell'), (pp, 'publication')]:
        snapshot = r / f'{kind}.{i}.before-source-admission72.exactraw.json'
        assert not snapshot.exists()
        snapshot.write_bytes(p.read_bytes())
    write(ap, accepted)
    write(cp, cell)
    write(pp, publication)
pub.inputs.cache_clear()
pub.load.cache_clear()
pub.check_advance(plan['mathematical_declarations'], reviewed=True)
for i, (slug, accepted) in enumerate(zip(plan['slugs'], accepted_audits)):
    item = next(x for x in pub.load() if x['id'] == slug)
    assert pub.binding_digest(item, item['bindings'][0], pub.inputs()) == accepted['publication_binding_sha256']
    assert pub.review_context(item, item['bindings'][0], pub.inputs()) == accepted['publication_context']
mirror = load(r / 'conceptual-mirror-audit72.json')
mirror = {k: mirror[k] for k in ['status', 'discovery_ids', 'reason']}
boundary = 'Two connected perturbation identities focused-compiled, independently mathematically reviewed, blindly reconstructed and source-reviewed. Exact SCI72, serialized shared integration and reader validation remain pending. Arbitrary r is not actual r_rho; real H/K/B27/B28/fullB4/H1, invariance/nonexplosion, full papers, errors, expected-query costs and actual-input composition remain open. No whole-paper/Exposition Seal/PURIFIED/main/live/Goal credit.'
e = dict(result_kind='theorem-edge', theorem_delta=claim['theorem_delta'], lean_declarations=plan['mathematical_declarations'], publication_declarations=plan['mathematical_declarations'], lean_files=claim['proposed_files'], focused_checks=[dict(command=c, result=['Root9564 EXIT0/2392; independent22524 EXIT0; first coercion failure13416 retained.', 'Root37484 EXIT0/3952; independent41536 EXIT0.'][i]) for i, c in enumerate(claim['focused_checks'])], truth_boundary=boundary, conceptual_mirror_audit=mirror, useful_discoveries=[], active_cells=plan['active_cells'], reader_lesson=['website/content/declaration_lessons/' + s + '.json' for s in plan['slugs']], integration_notes='One SAU, two connected publication cells: generic real-Hilbert algebra is actually consumed by original-six-input/twelve-witness actual PBPS theorem. Same C and exact +1/2 term. Sole stabilization lane; no actual residual/kernel/main/cost/composition credit.')
for key in ['statement_seal', 'source_proof_coverage', 'proof_digestion', 'purification']:
    e[key] = [dict(declaration=d, declaration_level=entry[4]['declaration_level'], report=entry[4][key]) for d, entry in zip(plan['mathematical_declarations'], canonical)]
adv.transition_advance(claim['advance_id'], 'PROVED_LOCAL', worker_id=claim['created_by'], evidence=e)
for i, (ap, cp, pp, accepted, cell, publication) in enumerate(canonical):
    cell['status'] = 'proved_locally'
    cell['conceptual_mirror_audit'] = mirror
    cell['evidence'].update(proof_review=(r / 'independent-math72/mathematical-verdict.json').as_posix(), source_review=(o / f'source.{i}.decision.json').as_posix(), execution_boundary=boundary)
    write(cp, cell)
new(r / 'proved-local.json', e)
new(r / 'root.source72.adoption.json', dict(status='ACCEPTED_INDEPENDENT_SOURCE72_TWO_CONNECTED_PERTURBATION_IDENTITIES_ONLY', actual_root_PID=os.getpid(), native_owned_files=258, native_whole_logical_run_sha256=h, native_complete_named_RAW=pin(payload_path), native_lease=pin(o / 'lease.final.json'), finite_current_input_maps=versions, coverage=run['coverage'], no_mathematical_repair=True, official_reviewer_packets_unchanged=True, publication_bindings_unchanged=True, VERIFIED=False, full_paper=False, Goal_complete=False))
print('PASS72 PROVED_LOCAL once: CLOSED82 math/5blind/258source; two connected perturbation identities only. Exact SCI/aggregate/reader pending.')
