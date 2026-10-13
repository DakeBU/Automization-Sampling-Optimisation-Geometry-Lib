from pathlib import Path
import datetime, hashlib, json, subprocess
root = Path.cwd().resolve()
r = Path(__file__).resolve().parent
out = r / 'integration107'
load = lambda p: json.loads(Path(p).read_bytes())
def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.resolve().relative_to(root).as_posix(), raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
labels = ['tests', 'astis', 'canonical', 'publication', 'contributor', 'semantic', 'frontier', 'process-memory', 'python-compile', 'site-build', 'site-check', 'graph-after-site', 'site-regressions', 'harness', 'diff-check']
checks = []
for label in labels:
    p = r / 'checks107' / ('integration-' + label)
    d = load(p / 'receipt.json')
    assert d['exit_code'] == 0 and d['terminal_closed'], label
    checks.append(dict(label=label, receipt=ref(p / 'receipt.json'), stdout=ref(p / 'stdout.log'), stderr=ref(p / 'stderr.log')))
gate = load('.astis/site-lean-gate.json')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
assert gate['passed'] and gate['commit'] == head
science = load(out / 'integration-scope.json')['science_commit']
assert subprocess.run(['git','merge-base','--is-ancestor',science,head]).returncode==0
saved = load(r / 'exact-commit-verification107/closed-RAW-manifest107.json')['preserved_collaborator_inputs']
for d in saved:
    assert hashlib.sha256(Path(d['path']).read_bytes()).hexdigest() == d['raw_sha256'], d['path']
note = dict(status='LOCAL_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), science_commit=science, integration_base_commit=head, registry_count=int(__import__('re').search(r'formalizedTechnicalLemmaCount = (\d+)', Path('Tests/Basic.lean').read_text(encoding='utf8')).group(1)), verification=ref(r / 'exact-commit-verification107/verified.json'), checks=checks, source_digest=gate['source_digest'], offline_reader=ref(out / 'offline-reader107.json'), static_svg=ref(out / 'static-svg/viewed107.json'), affected_branch_svg=ref(out / 'static-svg/branch-viewed107.json'), graph_delta='One actual L2 expectation contraction node consuming actual bounded Gibbs duality106, normalization103 and UnitExponentialProduct. Pullback isometries, adjoint averaging, product L1 and signed Fubini identify the literal expectation by indicator-test uniqueness. Universal quotient identification implies representative independence; the retained direct-AE source route is explicitly unselected. No extra public source premise.', preserved_collaborator_modified_files=len(saved), sole_lane='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity', state_distinctions=dict(proved_locally=True, independently_verified=True, local_aggregate_and_generated_site_gates=True, stabilized=False, merged=False, purified=False, live_verified=False, full_Exposition_Seal=False, main_theorem_complete=False), remaining=['Full L2 momentum-flip identity Eq A.3, restart/Markov/semigroup, strong continuity and separate kernel-witness identification remain open.', 'Hypocoercivity, implementation errors, actual expected costs, main results, composition and all four full papers remain open.', 'Actual browser page/interactive acceptance, main merge and postmerge purification remain separate.'], resolved_focused_failures='Exact sealed statement unchanged. Retained probes diagnose typed embeddings, integral-uniqueness import, indicator AE rewriting, proof-local universe specialization and zero-time filter annotation. The universal-quotient route was independently admitted as an alternative to the planned direct-AE proof. Final source review and exposition admission are bound separately.', Goal_complete=False)
p = r / 'integration.notes.json'
assert not p.exists()
p.write_text(json.dumps(note, indent=2) + '\n', encoding='utf8', newline='\n')
print('Aggregate107 and generated-reader evidence recorded; full reader/main/purification/paper completion remains separate.')
