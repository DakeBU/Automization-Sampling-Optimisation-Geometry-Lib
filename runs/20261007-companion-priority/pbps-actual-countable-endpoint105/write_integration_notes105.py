from pathlib import Path
import datetime, hashlib, json, subprocess
root = Path.cwd().resolve()
r = Path(__file__).resolve().parent
out = r / 'integration105'
load = lambda p: json.loads(Path(p).read_bytes())
def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.resolve().relative_to(root).as_posix(), raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
labels = ['tests', 'astis', 'canonical', 'publication', 'contributor', 'semantic', 'frontier', 'process-memory', 'python-compile', 'site-build', 'site-check', 'graph-after-site', 'site-regressions', 'harness', 'diff-check']
checks = []
for label in labels:
    p = r / 'checks105' / ('integration-' + label)
    d = load(p / 'receipt.json')
    assert d['exit_code'] == 0 and d['terminal_closed'], label
    checks.append(dict(label=label, receipt=ref(p / 'receipt.json'), stdout=ref(p / 'stdout.log'), stderr=ref(p / 'stderr.log')))
gate = load('.astis/site-lean-gate.json')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
assert gate['passed'] and gate['commit'] == head
science = load(out / 'integration-scope.json')['science_commit']
assert subprocess.run(['git','merge-base','--is-ancestor',science,head]).returncode==0
saved = load(r / 'exact-commit-verification105/closed-RAW-manifest105.json')['preserved_collaborator_inputs']
for d in saved:
    assert hashlib.sha256(Path(d['path']).read_bytes()).hexdigest() == d['raw_sha256'], d['path']
note = dict(status='LOCAL_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), science_commit=science, integration_base_commit=head, registry_count=557, verification=ref(r / 'exact-commit-verification105/verified.json'), checks=checks, source_digest=gate['source_digest'], offline_reader=ref(out / 'offline-reader105.json'), static_svg=ref(out / 'static-svg/viewed105.json'), affected_branch_svg=ref(out / 'static-svg/branch-viewed105.json'), graph_delta='One actual countable endpoint-law integration node consuming four reviewed producers93/103/UnitExponentialProduct/104. All finite-count sectors are assembled into the same actual global process endpoint probability. Exact call edges are reviewed, not conceptual transport claims.', preserved_collaborator_modified_files=len(saved), sole_lane='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity', state_distinctions=dict(proved_locally=True, independently_verified=True, local_aggregate_and_generated_site_gates=True, stabilized=False, merged=False, purified=False, live_verified=False, full_Exposition_Seal=False, main_theorem_complete=False), remaining=['Bounded signed bilinear duality and fixed-time marginal phase invariance remain open; countable actual endpoint assembly, probability and flipped-swap reversal are closed.', 'Restart/Markovness, hypocoercivity, implementation errors, actual expected costs, main results, composition and all four full papers remain open.', 'Actual browser page/interactive acceptance, main merge and postmerge purification remain separate.'], resolved_focused_failures='Compiler failures were representation/API issues closed with explicit probability transport, integrands and function multiplication. Exact sealed statement unchanged. An independently reviewed exposition-only repair defined H, pi_y and gamma. Upstream merge preserves sphere work and both append-only ledgers; ledger delivery omission repaired and independently reviewed.', Goal_complete=False)
p = r / 'integration.notes.json'
assert not p.exists()
p.write_text(json.dumps(note, indent=2) + '\n', encoding='utf8', newline='\n')
print('Aggregate105 and generated-reader evidence recorded; full reader/main/purification/paper completion remains separate.')
