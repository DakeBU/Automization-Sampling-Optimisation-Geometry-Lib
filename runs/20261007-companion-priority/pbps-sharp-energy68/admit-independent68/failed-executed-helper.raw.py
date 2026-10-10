from pathlib import Path
import copy, hashlib, json, os, sys
root = Path.cwd()
sys.path.insert(0, 'tools')
import astis_publication as pub, astis_semantic_roundtrip as rt, astis_advance as adv
r = root / 'runs/20261007-companion-priority/pbps-sharp-energy68'
d = r / 'independent-source-delta-schema68'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def replace(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
def new(p, value):
    assert not p.exists(), p
    replace(p, value)
def check(b, row):
    assert len(b) == row['RAW_bytes'] and sha(b) == row['RAW_sha256']
    assert sha(b.replace(b'\r\n', b'\n')) == row['LF_sha256']
source = load(r / 'root.source68.adoption.json')
assert source['status'] == 'INDEPENDENT_SOURCE68_ACCEPTED_SELECTED_BOUNDARIES'
assert load(r / 'root.math68.adoption.json')['native_owned_files'] == 275
assert load(r / 'root.decoder68.adoption.json')['native_owned_files'] == 31
assert load(r / 'root.consumer-decoder68.adoption.json')['native_owned_files'] == 25
assert load(r / 'root.prose-span-overlay68.adoption.json')['status'] == 'INDEPENDENTLY_APPROVED_V2_OVERLAY_APPLIED'
lease = load(d / 'lease.final.json')
assert sha((d / 'lease.final.json').read_bytes()) == '3a6254f1334127de61473688605872877e9caef3c109975864c852f0d9f7f828'
assert lease['status'] == 'CLOSED_LAST' and lease['total_owned_file_count_including_manifest_and_final_lease'] == 24
assert lease['actual_closing_pid'] == 19204 and lease['terminal_receipt']['actual_child_pid'] == 19820 and lease['terminal_receipt']['actual_exit_code'] == 0
for key in ['complete_named_RAW_review','complete_named_RAW_decision','complete_named_RAW_input_payload','owned_manifest']:
    check((d / lease[key]['path']).read_bytes(), lease[key])
manifest = load(d / 'owned-manifest.json')
files = {p.relative_to(d).as_posix(): p for p in d.rglob('*') if p.is_file()}
assert len(files) == 24 and len(manifest['rows']) == 22
assert set(files) == {row['path'] for row in manifest['rows']} | {'owned-manifest.json','lease.final.json'}
for row in manifest['rows']:
    check(files[row['path']].read_bytes(), row)
assert (d / 'lease.final.json').stat().st_mtime_ns >= max(p.stat().st_mtime_ns for p in files.values())
run = load(d / 'review-run.json')
assert sha(can({k:v for k,v in run.items() if k != 'run_sha256'})) == run['run_sha256'] == lease['whole_logical_run_sha256'] == '64e6cd51162d5671fcc2ff24882db8f40bbd9f896aff13183e2eb0d142bb0fc4'
payload = load(d / 'complete-RAW-input-payload.json')
assert payload['entry_count'] == len(payload['entries']) == 4
for row in payload['entries']:
    b = (root / row['source_path']).read_bytes()
    check(b, row)
    assert (d / row['raw_snapshot']).read_bytes() == b
    assert (d / row['lf_snapshot']).read_bytes() == b.replace(b'\r\n', b'\n')
mapping = load(d / 'complete-RAW-decision.json')
assert mapping['decision'] == lease['decision'] == 'APPROVED_EXACT_FINITE_SCHEMA_ADAPTER'
assert not mapping['repairs'] and not mapping['source_mathematical_repair'] and not mapping['native_decisions_modified']
proposal_path = r / 'source-delta-schema-adapter68/proposal.json'
assert sha(proposal_path.read_bytes()) == mapping['proposal_RAW_sha256'] == '5c935327f649dcfe8ce5329f027c7206849fa4989f22db227ca72b7af8a924fd'
proposal = load(proposal_path)
assert len(mapping['entries']) == len(proposal['entries']) == 3
for proposed, reviewed in zip(proposal['entries'], mapping['entries']):
    assert proposed['native_decision'] == reviewed['native_decision']
    assert sha((root / proposed['native_decision']).read_bytes()) == proposed['native_RAW_sha256'] == reviewed['native_RAW_sha256']
    assert reviewed['all_five_native_records_and_fields_preserved'] and not reviewed['verdict_changed'] and not reviewed['source_Lean_statement_packet_binding_changed']
    for original, normalized in zip(proposed['native_deltas'], proposed['canonical_deltas']):
        assert {key:value for key,value in normalized.items() if key not in ['slot','severity','description','evidence']} == original
        assert normalized['severity'] == 'informational' and normalized['blocking'] is False
new(r / 'root.source-delta-schema68.adoption.json', dict(
    status='EXACT_INDEPENDENTLY_APPROVED_SOURCE_DELTA_SCHEMA_ADAPTER_ACCEPTED',
    actual_read_only_adopter_pid=os.getpid(), native_owned_files=24,
    native_whole_logical_run_sha256=run['run_sha256'],
    native_complete_RAW_decision_sha256=lease['complete_named_RAW_decision']['RAW_sha256'],
    native_complete_RAW_input_sha256=lease['complete_named_RAW_input_payload']['RAW_sha256'],
    finite_slot_map=proposal['slot_map'], all15_native_records_preserved=True,
    native_CLOSED363_unmodified=True, source_mathematical_repair=False,
    closing_pid_external_EXIT0=19204, postclose_read_only_pid_external_EXIT0=49320,
    full_Exposition=False, PURIFIED=False, Goal_complete=False))
plan, claim, registry = load(r / 'publication-plan.json'), load(r / 'claim.json'), rt.load_registry()
pub.inputs.cache_clear()
pub.load.cache_clear()
data = pub.inputs()
accepted_records = []
for i, key in enumerate(['0','1','consumer']):
    decision = load(r / 'independent-source68' / f'source.{key}.decision.json')
    packet = load(r / f'source.{key}.reviewer-packet.json')
    ap = root / 'research-wiki/semantic-roundtrip/audits' / (plan['audit_ids'][i] + '.json') if i < 2 else r / 'consumer.semantic-audit68.blind.json'
    audit = load(ap)
    assert audit['state'] == 'blind-reconstructed' and rt.semantic_reviewer_packet(audit) == packet
    assert packet['packet_sha256'] == decision['reviewer_packet_sha256']
    if i < 2:
        item = next(item for item in pub.load() if item['id'] == plan['slugs'][i])
        assert pub.binding_digest(item,item['bindings'][0],data) == audit['publication_binding_sha256'] == decision['publication_binding_sha256']
    else:
        assert sha(can(audit['publication_context'])) == audit['publication_binding_sha256'] == decision['publication_binding_sha256']
    adapter = copy.deepcopy(decision)
    adapter['deltas'] = copy.deepcopy(proposal['entries'][i]['canonical_deltas'])
    adapter.update(exact_delta_schema_map='root.source-delta-schema68.adoption.json; preserve complete native fields and independently approved finite mapping',
        native_complete_RAW_review_sha256=source['native_complete_RAW_review_sha256'],
        native_review_bytes_preserved=True, external_whole_run_binding='root.source68.adoption.json; delete only top-level run_sha256')
    target = r / f'source.{key}.review.root-adapter.json'
    new(target, adapter)
    accepted = copy.deepcopy(audit)
    accepted.update(state='accepted', semantic_slots=decision['semantic_slots'], deltas=adapter['deltas'],
                    verdict=decision['verdict'], repairs=[])
    accepted['source_review'] = dict(state='accepted', reviewer=decision['reviewer'],
        independent_from_formalizer=True, independent_from_decoder=True,
        evidence=decision['review_evidence'], review_run_sha256=decision['review_run_sha256'],
        reviewer_packet_sha256=decision['reviewer_packet_sha256'], run_artifact=target.relative_to(root).as_posix())
    if i < 2:
        registry['audits'] = [accepted if item['id'] == plan['audit_ids'][i] else item for item in registry['audits']]
    accepted_records.append((i,key,ap,accepted))
errors = rt.validate_registry(registry)
assert not errors, errors
for i,key,ap,accepted in accepted_records:
    before = r / f'audit.{key}.before-source-admission.exactraw.snapshot.json'
    assert not before.exists()
    before.write_bytes(ap.read_bytes())
    if i < 2:
        replace(ap, accepted)
    else:
        new(r / 'consumer.semantic-audit68.accepted.json', accepted)
pub.inputs.cache_clear()
pub.load.cache_clear()
pub.check_advance(plan['mathematical_declarations'], reviewed=True)
mirror = load(r / 'conceptual-mirror-audit68.json')
mirror = {key:mirror[key] for key in ['status','discovery_ids','reason']}
boundary = claim['truth_boundary'] + ' Independent precommit math, two blind native bundles and primary-first full-module source review accepted, including the complete original-input Test. Exact V2 prose/span overlay and independent schema adapter preserve all mathematical bytes. Exact SCI68 verification and serialized aggregate/reader admission remain pending. Generic S,T reader aliases need a separately reviewed prose overlay; full Exposition/PURIFIED unearned.'
cells = [(root / 'research-wiki/frontier-cells' / (cid + '.json'), cid) for cid in plan['active_cells']]
evidence = dict(result_kind='integration-node', theorem_delta=claim['theorem_delta'],
    lean_declarations=claim['target_declarations'], publication_declarations=plan['mathematical_declarations'],
    lean_files=claim['proposed_files'], focused_checks=[dict(command='lake build Tests.ProximalBPSSharpCorrectorEnergy',
      result='Root38372 EXIT0/3950; clean actual21404 EXIT0. Independent fresh leaf41164/main18400/Test42008 EXIT0; all3 declarations standard3 only.'),
      dict(command='Independent math, two source-blind bundles, primary-first full-module source review',
      result='CLOSED math275/source363/decoder31+25;344 selected source nodes/11 literal BODY steps;3 packets/21 slots equivalent-after-elaboration. Separate V2 and schema24 reviewed. No source mathematical repair.')],
    truth_boundary=boundary, conceptual_mirror_audit=mirror, useful_discoveries=[], active_cells=plan['active_cells'],
    reader_lesson=['website/content/declaration_lessons/' + slug + '.json' for slug in plan['slugs']],
    integration_notes='Reusable sharp Hilbert estimate, SAME actual PBPS sharp corrector and genuine original-input LemmaB3 Test. Rank0/alphaeta1 preserved; no onto V or new caller ingredient. Next actual B21 intertwining/rotation has source-only419-node preflight, not a proof. Sole stabilization lane; no main/errors/cost/composition/full Exposition/PURIFIED/Goal completion.')
for key in ['statement_seal','source_proof_coverage','proof_digestion','purification']:
    evidence[key] = [dict(declaration=decl, declaration_level=load(p)['declaration_level'], report=load(p)[key])
                     for (p,cid),decl in zip(cells,plan['mathematical_declarations'])]
adv.transition_advance(claim['advance_id'], 'PROVED_LOCAL', worker_id=claim['created_by'], evidence=evidence)
for i,(p,cid) in enumerate(cells):
    cell = load(p)
    assert cell['status'] == 'claimed'
    (r / f'cell.{i}.before-proved.exactraw.snapshot.json').write_bytes(p.read_bytes())
    cell['status'] = 'proved_locally'
    cell['conceptual_mirror_audit'] = mirror
    cell['evidence'].update(proof_review=(r / 'independent-math68/named-mathematical-review.payload.json').relative_to(root).as_posix(),
        source_review=(r / f'source.{i}.review.root-adapter.json').relative_to(root).as_posix(), execution_boundary=boundary)
    replace(p, cell)
new(r / 'proved-local.json', evidence)
print('PASS68 PROVED_LOCAL: math/decoder/source/independently approved schema and real publication admission; exact SCI68 and aggregate remain pending.')
