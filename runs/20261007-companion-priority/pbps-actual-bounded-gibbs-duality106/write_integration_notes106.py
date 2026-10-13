from pathlib import Path
import datetime, hashlib, json, subprocess
root = Path.cwd().resolve()
r = Path(__file__).resolve().parent
out = r / 'integration106'
load = lambda p: json.loads(Path(p).read_bytes())
def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.resolve().relative_to(root).as_posix(), raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
labels = ['tests', 'astis', 'canonical', 'publication', 'contributor', 'semantic', 'frontier', 'process-memory', 'python-compile', 'site-build', 'site-check', 'graph-after-site', 'site-regressions', 'harness', 'diff-check']
checks = []
for label in labels:
    p = r / 'checks106' / ('integration-' + label)
    d = load(p / 'receipt.json')
    assert d['exit_code'] == 0 and d['terminal_closed'], label
    checks.append(dict(label=label, receipt=ref(p / 'receipt.json'), stdout=ref(p / 'stdout.log'), stderr=ref(p / 'stderr.log')))
gate = load('.astis/site-lean-gate.json')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
assert gate['passed'] and gate['commit'] == head
science = load(out / 'integration-scope.json')['science_commit']
assert subprocess.run(['git','merge-base','--is-ancestor',science,head]).returncode==0
saved = load(r / 'exact-commit-verification106/closed-RAW-manifest106.json')['preserved_collaborator_inputs']
for d in saved:
    assert hashlib.sha256(Path(d['path']).read_bytes()).hexdigest() == d['raw_sha256'], d['path']
note = dict(status='LOCAL_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), science_commit=science, integration_base_commit=head, registry_count=int(__import__('re').search(r'formalizedTechnicalLemmaCount = (\d+)', Path('Tests/Basic.lean').read_text(encoding='utf8')).group(1)), verification=ref(r / 'exact-commit-verification106/verified.json'), checks=checks, source_digest=gate['source_digest'], offline_reader=ref(out / 'offline-reader106.json'), static_svg=ref(out / 'static-svg/viewed106.json'), affected_branch_svg=ref(out / 'static-svg/branch-viewed106.json'), graph_delta='One bounded signed Gibbs duality and fixed-time invariance integration node consuming actual endpoint law105, normalization103 and UnitExponentialProduct. Internal Gaussian negation and signed Fubini close the marginal and integrability edges. Direct marginal and printed F=1 source routes are separately identified; conceptual relationships are not Lean edges.', preserved_collaborator_modified_files=len(saved), sole_lane='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity', state_distinctions=dict(proved_locally=True, independently_verified=True, local_aggregate_and_generated_site_gates=True, stabilized=False, merged=False, purified=False, live_verified=False, full_Exposition_Seal=False, main_theorem_complete=False), remaining=['Bounded signed bilinear duality and fixed-time marginal phase invariance are closed for the same actual process. L2 operator/domain identity, restart and Markovness, and separate kernel witness identification remain open.', 'Restart/Markovness, hypocoercivity, implementation errors, actual expected costs, main results, composition and all four full papers remain open.', 'Actual browser page/interactive acceptance, main merge and postmerge purification remain separate.'], resolved_focused_failures='Two compiler representation issues were closed by explicit integrands and unfolding the local operator. Exact sealed statement unchanged. The direct marginal source graph alternative was separately independently reviewed, preserving the printed F=1 route. Final source and exposition review required no repair. Upstream sphere Rayleigh work and both canonical ledger histories are preserved.', Goal_complete=False)
p = r / 'integration.notes.json'
assert not p.exists()
p.write_text(json.dumps(note, indent=2) + '\n', encoding='utf8', newline='\n')
print('Aggregate106 and generated-reader evidence recorded; full reader/main/purification/paper completion remains separate.')
