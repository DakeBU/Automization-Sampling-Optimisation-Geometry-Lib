from pathlib import Path
import datetime, hashlib, json, subprocess
root = Path.cwd().resolve()
r = Path(__file__).resolve().parent
out = r / 'integration104'
load = lambda p: json.loads(Path(p).read_bytes())
def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.resolve().relative_to(root).as_posix(), raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
labels = ['tests', 'astis', 'canonical', 'publication', 'contributor', 'semantic', 'frontier', 'process-memory', 'python-compile', 'site-build', 'site-check', 'graph-after-site', 'site-regressions', 'harness', 'diff-check']
checks = []
for label in labels:
    p = r / 'checks104' / ('integration-' + label)
    d = load(p / 'receipt.json')
    assert d['exit_code'] == 0 and d['terminal_closed'], label
    checks.append(dict(label=label, receipt=ref(p / 'receipt.json'), stdout=ref(p / 'stdout.log'), stderr=ref(p / 'stderr.log')))
gate = load('.astis/site-lean-gate.json')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
assert gate['passed'] and gate['commit'] == head == load(out / 'integration-scope.json')['science_commit']
saved = load(r / 'exact-commit-verification104/closed-RAW-manifest104.json')['preserved_collaborator_inputs']
for d in saved:
    assert hashlib.sha256(Path(d['path']).read_bytes()).hexdigest() == d['raw_sha256'], d['path']
note = dict(status='LOCAL_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), science_commit=head, integration_base_commit=head, registry_count=555, verification=ref(r / 'exact-commit-verification104/verified.json'), checks=checks, source_digest=gate['source_digest'], offline_reader=ref(out / 'offline-reader104.json'), static_svg=ref(out / 'static-svg/viewed104.json'), affected_branch_svg=ref(out / 'static-svg/branch-viewed104.json'), graph_delta='One actual normalized endpoint-pair integration node consuming four reviewed public parents93/97/102/103. Normalization103 and weighted-sector102 are now joined. Exact call edges are reviewed, not conceptual transport claims.', preserved_collaborator_modified_files=len(saved), sole_lane='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity', state_distinctions=dict(proved_locally=True, independently_verified=True, local_aggregate_and_generated_site_gates=True, stabilized=False, merged=False, purified=False, live_verified=False, full_Exposition_Seal=False, main_theorem_complete=False), remaining=['Signed endpoint tests and countable sector assembly toward actual process invariance.', 'Restart/Markovness, hypocoercivity, implementation errors, actual expected costs, main results, composition and all four full papers remain open.', 'Actual browser page/interactive acceptance, main merge and postmerge purification remain separate.'], resolved_focused_failures='Diagnosed composition elaboration by inferring the measurable composition first; used explicit function arguments for density integrals and explicit Set.ofPred intersections for simplex measurability. Exact statement unchanged. One independent exposition repair added the zero-based time-coordinate convention, without changing Lean or decoder input.', Goal_complete=False)
p = r / 'integration.notes.json'
assert not p.exists()
p.write_text(json.dumps(note, indent=2) + '\n', encoding='utf8', newline='\n')
print('Aggregate104 and generated-reader evidence recorded; full reader/main/purification/paper completion remains separate.')
