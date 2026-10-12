from pathlib import Path
import datetime, hashlib, json, subprocess
root = Path.cwd().resolve()
r = Path(__file__).resolve().parent
out = r / 'integration109'
load = lambda p: json.loads(Path(p).read_bytes())
def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.resolve().relative_to(root).as_posix(), raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
labels = ['tests', 'astis', 'canonical', 'publication', 'contributor', 'semantic', 'frontier', 'process-memory', 'python-compile', 'site-build', 'site-check', 'graph-after-site', 'site-regressions', 'harness', 'diff-check']
checks = []
for label in labels:
    p = r / 'checks109' / ('integration-' + label)
    repair = r / 'checks109' / ('display-' + label)
    if (repair/'receipt.json').exists(): p=repair
    d = load(p / 'receipt.json')
    assert d['exit_code'] == 0 and d['terminal_closed'], label
    if label == 'graph-after-site': assert d['argv'][-1] == load(r/'claim.json')['frontier_cell'], 'Graph gate must target this exact cell'
    checks.append(dict(label=label, receipt=ref(p / 'receipt.json'), stdout=ref(p / 'stdout.log'), stderr=ref(p / 'stderr.log')))
gate = load('.astis/site-lean-gate.json')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
assert gate['passed'] and gate['commit'] == head
science = load(out / 'integration-scope.json')['science_commit']
assert subprocess.run(['git','merge-base','--is-ancestor',science,head]).returncode==0
saved = load(r / 'exact-commit-verification109/closed-RAW-manifest109.json')['preserved_collaborator_inputs']
for d in saved:
    assert hashlib.sha256(Path(d['path']).read_bytes()).hexdigest() == d['raw_sha256'], d['path']
note = dict(status='LOCAL_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), science_commit=science, integration_base_commit=head, registry_count=int(__import__('re').search(r'formalizedTechnicalLemmaCount = (\d+)', Path('Tests/Basic.lean').read_text(encoding='utf8')).group(1)), verification=ref(r / 'exact-commit-verification109/verified.json'), checks=checks, source_digest=gate['source_digest'], offline_reader=ref(out / 'offline-reader109.json'), static_svg=ref(out / 'static-svg/viewed109.json'), affected_branch_svg=ref(out / 'static-svg/branch-viewed109.json'), graph_delta='One actual position Gaussian averaging node consuming actual108 once. Canonical fst lift and its adjoint are identified with the literal Gaussian integral for arbitrary MemLp representatives. Fubini and indicator uniqueness give the L2 class; flip absorption yields a self-adjoint contraction and the inherited clock action gives its actual nested expectation. The original sealed graph is preserved with an independently reviewed namespace/L1-indicator adapter.', preserved_collaborator_modified_files=len(saved), sole_lane='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity', state_distinctions=dict(proved_locally=True, independently_verified=True, local_aggregate_and_generated_site_gates=True, stabilized=False, merged=False, purified=False, live_verified=False, full_Exposition_Seal=False, main_theorem_complete=False), remaining=['Markov positivity/constants, restart/semigroup, strong continuity, independent-reference averaging and separate kernel-witness identification remain open.', 'Hypocoercivity, implementation errors, actual expected costs, main results, composition and all four full papers remain open.', 'Actual browser page/interactive acceptance, main merge and postmerge purification remain separate.'], resolved_focused_failures='Exact sealed statement unchanged. Full1 needed explicit double-adjoint rewriting and the Measure namespace for the AE product slice. Full2 required explicit extensionality to align a let-expanded J; full3 passed. The source graph namespace and selected L1-indicator realization received separate independent admission before final source review.', display_repair='One explanatory B**=B token replaced with words after site-marker failure; separately reviewed, rebound and checked. Lean and statement unchanged.', Goal_complete=False)
p = r / 'integration.notes.json'
assert not p.exists()
p.write_text(json.dumps(note, indent=2) + '\n', encoding='utf8', newline='\n')
print('Aggregate109 and generated-reader evidence recorded; full reader/main/purification/paper completion remains separate.')
