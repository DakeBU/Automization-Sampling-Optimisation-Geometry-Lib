from pathlib import Path
import copy, hashlib, json, os, subprocess, sys

root = Path.cwd()
r = root / 'runs/20261007-companion-priority/pbps-macro-root63'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.relative_to(root).as_posix(), bytes=len(b), raw_sha256=sha(b),
                lf_sha256=sha(b.replace(b'\r\n', b'\n')))

def write(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n',
                       encoding='utf-8', newline='\n')

lease = load(r / 'exact-science-verification/lease.json')
assert lease['status'] == 'CLOSED_LAST'
assert lease['actual_foreground_candidate_readback']['exit_code'] == 0
assert lease['actual_foreground_candidate_readback']['status'] == 'FOREGROUND_TERMINAL_CLOSED'
assert lease['verifier_id'] == '/root/exact_science63'
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == '4d02622332d02d0bd6c977d3cee48fd535ebf203'
sys.path.insert(0, str(root / 'tools'))
import astis_publication as pub

plan = load(r / 'publication-plan.json')
cid = plan['active_cells'][0]
p = root / 'research-wiki/frontier-cells' / (cid + '.json')
old_raw = p.read_bytes()
assert old_raw == subprocess.check_output(['git', 'show', 'HEAD:' + p.relative_to(root).as_posix()]), 'Preserve exact SCI63 cell before repair.'
old = load(p)
assert old['learning_contract']['failure_class'] == 'API_INSTANCE_ALIGNMENT'
assert old['learning_contract']['salvage']['required'] is False
assert old['learning_contract']['salvage']['status'] == 'not-applicable'
pub.inputs.cache_clear(); pub.load.cache_clear()
before_packet = pub.packet(cid)
data = pub.inputs()
item = next(i for i in pub.load() if i['id'] == plan['slugs'][0])
binding = item['bindings'][0]
before_context = pub.review_context(item, binding, data)
before_binding = pub.binding_digest(item, binding, data)
protected = [root / name for name in [
    'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean',
    'Tests/ProximalBPSMacroscopicDefectRoot.lean',
    'website/content/publications/' + plan['slugs'][0] + '.json',
    'website/content/declaration_lessons/' + plan['slugs'][0] + '.json',
    'research-wiki/semantic-roundtrip/audits/' + plan['audit_ids'][0] + '.json',
    'lean-toolchain', 'lake-manifest.json']]
protected_before = [pin(q) for q in protected]
out = r / 'frontier-process-repair63'
out.mkdir(exist_ok=False)
(out / 'cell.science63.exactraw.snapshot.json').write_bytes(old_raw)
new = copy.deepcopy(old)
new['learning_contract']['failure_class'] = 'IMPLEMENTATION_FAILED'
new['learning_contract']['salvage']['required'] = True
new['learning_contract']['salvage']['status'] = 'completed'
write(p, new)
pub.inputs.cache_clear(); pub.load.cache_clear()
after_packet = pub.packet(cid)
data = pub.inputs()
item = next(i for i in pub.load() if i['id'] == plan['slugs'][0])
binding = item['bindings'][0]
assert after_packet == before_packet
assert pub.review_context(item, binding, data) == before_context
assert pub.binding_digest(item, binding, data) == before_binding
assert [pin(q) for q in protected] == protected_before
write(out / 'repair.json', dict(
    status='PROCESS_METADATA_REPAIRED_GATES_PENDING', actual_adopter_pid=os.getpid(),
    exact_science_commit=head, verifier_closed_lease=pin(r / 'exact-science-verification/lease.json'),
    before=pin(out / 'cell.science63.exactraw.snapshot.json'), after=pin(p),
    exact_changed_fields=[
        'learning_contract.failure_class: API_INSTANCE_ALIGNMENT -> IMPLEMENTATION_FAILED',
        'learning_contract.salvage.required: false -> true',
        'learning_contract.salvage.status: not-applicable -> completed'],
    salvage_reason_and_fragment_lists_preserved=True,
    original_failures=[pin(r / 'remote-science63-site-failure-log/stdout.log'),
                       pin(r / 'remote-formal63-failure-log/stdout.log')],
    protected_inputs=protected_before, publication_binding_sha256=before_binding,
    publication_packet_and_review_context_unchanged=True,
    mathematical_source_repair=False, repository_acceptance=False,
    full_paper_completion=False))
print('PASS three process fields repaired after native exact-review closure; mathematical bytes and publication binding/context unchanged. Frontier/site/aggregate gates pending.')
