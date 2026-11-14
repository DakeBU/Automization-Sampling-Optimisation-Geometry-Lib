from pathlib import Path
import gzip, hashlib, json, subprocess
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
O = E/'actual-source-V'
L = Path('runs/substantive_advances.jsonl')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json')
carrier = '7359f552e3b9bdf27c2253703d879783f331c4e9'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
def put(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == carrier
assert not (W/'complete-actual-sourceV-carry-commit.json').exists()
record = json.loads((E/'root-actual-source-V-exact-byte-carry.json').read_bytes())
assert record['all_original_top_level_evidence_keys_count'] == 19
assert record['all94_selected_original_files_exact']
selected = {x['destination']: x for x in record['selected_original_files']}
assert len(selected) == 94
staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()
assert len(staged) == 100 and set(selected) <= set(staged)
raws = {n: Path(n).read_bytes() for n in staged}
for n, b in raws.items():
    assert subprocess.check_output(['git', 'show', ':'+n]) == b, n
for n, x in selected.items():
    assert sha(raws[n]) == x['sha256'] and len(raws[n]) == x['bytes'], n
app = (O/'phase5/normal-VERIFIED-append.exact.jsonl').read_bytes()
assert sha(app) == record['raw_event_sha256'] == '90cc9126e265bd0e401e7bddf7593dc4505ea89c4091d80810c963d72e34bac9'
assert L.read_bytes() == subprocess.check_output(['git', 'show', carrier+':'+str(L)]) + app
assert json.loads(app)['evidence'] == json.loads((O/'phase5/actual-normal-VERIFIED-event.json').read_bytes())['evidence']
exceptions = [str(O/'phase5/inspect-carrier.stdout'), str(O/'phase5/private-intake-process-schema.stdout')]
stem = '20261110T175629009774Z-cosine-gram-complete-original-sourceV-all-fields-and-exact-Git-carry'
rp = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
failure = json.loads(rp.read_bytes())
log = Path(failure['log']).read_bytes()
assert failure['exit_code'] == 1 and sha(log) == '2e8671adf36c1dd6ab5a86ea499e6bb1fe28ba7a2fce0407f00643a8d343bf30'
assert failure['head_before'] == failure['head_after'] == carrier
messages = [line for line in log.decode().splitlines() if line.startswith(str(O))]
assert len(messages) == 2
assert all(any(line.startswith(n+':') and line.endswith('new blank line at EOF.') for line in messages) for n in exceptions)
for n in exceptions:
    assert raws[n].endswith(b'\n\n')
diag = {'kind': 'EXACT_RAW_EVIDENCE_STYLE_EXCEPTION',
        'actual_failure_log_sha256': sha(log), 'exact_original_stdout_paths': exceptions,
        'reason': 'The complete original source-verifier stdout files contain terminal blank lines. The default Git whitespace check rejected these two raw evidence files after all original bytes had been verified and staged; it did not find a proof, source, ledger or preservation failure.',
        'repair': 'Preserve every original byte. Run the normal whitespace check on every other staged path, and disable only blank-at-eof for these two exact stdout paths using command-local git -c. No tracked Git configuration is changed, no original output is normalized, and no normal API is repeated.',
        'normal_SourceV_replay': False, 'mathematics_or_original_V_values_changed': False}
new = {
    E/'sourceV-raw-stdout-whitespace-preservation-diagnostic.json': dump(diag),
    E/'root-local-process-scripts/finalize_sourceV_carry_preserving_raw_stdout.py': Path(__file__).read_bytes(),
    E/(stem+'.receipt.json'): rp.read_bytes(),
    E/(stem+'.log.gz'): gzip.compress(log, mtime=0),
}
for p, b in new.items():
    put(p, b)
    raws[str(p)] = b
subprocess.run(['git', 'add', '-f', '--']+[str(p) for p in new], check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()) == set(raws)
normal_paths = sorted(set(raws)-set(exceptions))
subprocess.run(['git', 'diff', '--cached', '--check', '--']+normal_paths, check=True)
subprocess.run(['git', '-c', 'core.whitespace=-blank-at-eof', 'diff', '--cached', '--check', '--']+exceptions, check=True)
for n, b in raws.items():
    assert subprocess.check_output(['git', 'show', ':'+n]) == b, n
subprocess.run(['git', 'commit', '-m', 'Carry all original cosine-Gram verification bytes and preserve reader HOLD'], check=True)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert subprocess.check_output(['git', 'rev-parse', commit+'^'], text=True).strip() == carrier
for n, b in raws.items():
    assert subprocess.check_output(['git', 'show', commit+':'+n]) == b, n
out = {'complete_actual_sourceV_carry_commit': commit, 'parent_metadata_carrier': carrier,
       'native_mathematical_commit': record['native_mathematical_commit'],
       'all94_selected_original_files_exact_in_Git_tree': True,
       'all_original_evidence_keys': record['all_original_top_level_evidence_keys_count'],
       'all_recursive_JSON_nodes': record['all_recursive_JSON_nodes'],
       'raw_event_sha256': record['raw_event_sha256'], 'root_sourceV_API_calls': 0,
       'two_exact_raw_stdout_EOF_exceptions_only': exceptions,
       'all_other_staged_whitespace_checks_passed': True,
       'reader_HOLD_global_purification_Goal_boundaries_preserved': True}
put(W/'complete-actual-sourceV-carry-commit.json', dump(out))
print(json.dumps(out))
