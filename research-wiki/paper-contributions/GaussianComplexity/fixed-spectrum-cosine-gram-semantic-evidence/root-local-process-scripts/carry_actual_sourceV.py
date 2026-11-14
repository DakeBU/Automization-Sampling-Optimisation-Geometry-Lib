"""Lossless readback/carry of the original independent event; no normal API."""
from pathlib import Path
import copy, gzip, hashlib, json, re, subprocess, sys, tarfile
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
S = Path('.astis/semantic-neutral-20261110/cg_src_7e41d9')
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
O = E/'actual-source-V'
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json')
L = Path('runs/substantive_advances.jsonl')
ADV = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumCosineGram'
OWNER = 'huanjian_gc_20261110_fixed_spectrum_cosine_gram'
ACTOR = '/root/cosine_gram_fresh_source_7e41d9'
carrier = '7359f552e3b9bdf27c2253703d879783f331c4e9'
native = '72e5d1405284f729f4eb600c5ae5dd556365b7e2'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
def put(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
def nodes(x):
    return 1 + sum(nodes(v) for v in x.values()) if isinstance(x, dict) else 1 + sum(nodes(v) for v in x) if isinstance(x, list) else 1
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == carrier
assert not O.exists() and not (W/'complete-actual-sourceV-carry-commit.json').exists()
archive = S/'phase5-normal-sourceV-all-portable-original-files.lossless-file-bytes.tar.gz'
manifest = S/'phase5-normal-sourceV-archive-manifest.json'
assert sha(archive.read_bytes()) == 'cca5d1af691f6fe97b6e19684ce84a470a63e9065b67e8ec8c5b4b3281df93a9'
assert sha(manifest.read_bytes()) == '5ca24a2abeb308eef999e20775b9071e6643725ef30cf386fa48a1957763b239'
m = json.loads(manifest.read_bytes())
assert m['file_count'] == 89 and m['normal_API_calls'] == 1
assert m['full_private_foreign_snapshots_included'] is False
expected = {x['archive_path']: x for x in m['files']}
assert len(expected) == 89
files = {}
with tarfile.open(archive) as tar:
    members = tar.getmembers()
    assert len(members) == len(expected)
    for member in members:
        assert member.isfile() and member.name in expected
        p = Path(member.name)
        assert not p.is_absolute() and '..' not in p.parts
        assert 'private-phase5-preservation' not in member.name
        row = expected[member.name]
        b = tar.extractfile(member).read()
        assert len(b) == row['bytes'] and sha(b) == row['sha256']
        original = Path(row['original_repo_path'])
        assert original.is_file() and not original.is_symlink()
        assert original.read_bytes() == b and original.stat().st_mode & 0o777 == 0o444
        files[member.name] = b
extra_originals = {
    'phase5_package_execution.json': '89595f76b9b72fc4808ad6eb9eb2ec96798760a7187e51c525d321e1548196db',
    'phase5_package_execution.stdout': 'abc9245234a2743f0f2d61460cceda0c8eabff7e339a1b98c6e1d98ac203c927',
    'phase5_package_execution.stderr': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
}
for n, h in extra_originals.items():
    p = S/n
    assert p.stat().st_mode & 0o777 == 0o444 and sha(p.read_bytes()) == h
    files[n] = p.read_bytes()
assert len(files) == 92
files[archive.name] = archive.read_bytes()
files[manifest.name] = manifest.read_bytes()
assert len(files) == 94
for n, b in files.items():
    assert not re.search(rb'wxid_[a-z0-9]{8,}|/Library/Containers/com\.tencent', b, re.I), n
assert sha(files['phase5/manifest.json']) == 'ba4054bb145c389863ce58cfe93d1f50f4a2a610867fd19c4fcd7aacd4d26ebe'
assert sha(files['phase5/freeze_receipt.json']) == '0532d22c6d3396499c7385e14f5663d56c88f3c87944e07f1952d8b3ef31daf1'
r = json.loads(files['phase5/freeze_receipt.json'])
assert r['normal_API_calls'] == 1 and r['source_actor'] == ACTOR
assert r['metadata_checked_carrier'] == carrier and r['mathematical_native_checked_commit'] == native
assert r['private_full_foreign_data_not_included'] is True
assert r['all_six_reader_HOLD_remote_STABILIZING_lease_and_global_boundaries_retained']
app = files['phase5/normal-VERIFIED-append.exact.jsonl']
assert len(app) == 19774 and sha(app) == '90cc9126e265bd0e401e7bddf7593dc4505ea89c4091d80810c963d72e34bac9'
old = subprocess.check_output(['git', 'show', carrier+':'+str(L)])
now = L.read_bytes()
assert len(old) == 5983401 and now == old + app and len(app.splitlines()) == 1
assert now.splitlines().count(app.rstrip(b'\n')) == 1
event = json.loads(app)
e = event['evidence']
assert event == json.loads(files['phase5/actual-normal-VERIFIED-event.json'])
assert event['advance_id'] == ADV and event['worker_id'] == ACTOR
assert event['from_state'] == 'PROVED_LOCAL' and event['to_state'] == 'VERIFIED'
assert e['verifier_id'] == ACTOR and e['verified_commit'] == native and e['metadata_checked_commit'] == carrier
assert len(e) == 19 and e == json.loads(files['phase5/normal-V-evidence.proposed.json'])
before = adv._replay_advances([json.loads(z) for z in old.splitlines()])
after = adv._replay_advances([json.loads(z) for z in now.splitlines()])
assert after[ADV]['state'] == 'VERIFIED' and after[ADV]['owner_id'] == OWNER
assert after[ADV]['latest_evidence'] == e
assert {k: v for k, v in before.items() if k != ADV} == {k: v for k, v in after.items() if k != ADV}
assert e['original_proved_local_evidence'] == before[ADV]['latest_evidence']
plocal_raw = (E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()
assert e['original_proved_local_event'] == json.loads(plocal_raw)
assert e['original_proved_local_event_sha256'] == sha(plocal_raw)
assert e['original_local_proof_capsule'] == json.loads((E/'local-proof-capsule.json').read_bytes())
prior_v = [z for z in old.splitlines() if json.loads(z).get('to_state') == 'VERIFIED']
assert len(prior_v) == 315
cb_raw = files['phase5/own-frontier-before.raw.json']
ca_raw = files['phase5/own-frontier-after.raw.json']
assert cb_raw == subprocess.check_output(['git', 'show', carrier+':'+str(C)])
assert ca_raw == C.read_bytes()
cb, ca = json.loads(cb_raw), json.loads(ca_raw)
assert cb['status'] == 'proved_locally' and ca['status'] == 'independently_verified'
rest = copy.deepcopy(ca)
rest['status'] = cb['status']
assert 'integration_boundary' not in cb['evidence']
del rest['evidence']['integration_boundary']
assert rest == cb
post = json.loads(files['phase5/normal-V-preservation-verification.json'])
assert post['all_foreign_current_states_and_latest_evidence_preserved'] == 298
assert post['all_foreign_controls_preserved'] == 832
assert post['all_tracked_except_own_ledger_frontier_preserved'] == 128717
assert post['all_prior_VERIFIED_events_preserved'] == 315
assert post['whole_ledger_prior_prefix_bytes_preserved'] == len(old)
assert post['actual_own_appended_event_count'] == 1 and post['ledger_after_sha256'] == sha(now)
assert post['restricted_metadata_exceptions_preserved']
for n in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumCosineGram.lean',
          'Tests/GaussianComplexityFixedSpectrumCosineGram.lean',
          'website/content/declaration_lessons/huanjian-fixed-spectrum-cosine-gram.json',
          'website/content/publications/huanjian-fixed-spectrum-cosine-gram.json',
          'lake-manifest.json', 'lean-toolchain']:
    assert Path(n).read_bytes() == subprocess.check_output(['git', 'show', native+':'+n]) == subprocess.check_output(['git', 'show', carrier+':'+n]), n
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
assert set(subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()) == {str(L), str(C)}
for n, b in files.items():
    put(O/n, b)
    (O/n).chmod(0o444)
record = {'scope': 'Root exact original-byte carry/readback only; no new source verdict or normal API.',
          'original_source_actor': ACTOR, 'actual_normal_source_API_calls': 1, 'root_source_API_calls': 0,
          'native_mathematical_commit': native, 'metadata_checked_carrier': carrier,
          'raw_event_sha256': sha(app), 'all_original_evidence_keys': list(e),
          'all_original_top_level_evidence_keys_count': len(e), 'all_recursive_JSON_nodes': nodes(e),
          'all_original_nested_values_exact_in_actual_event_and_latest_evidence': True,
          'complete_original_PLOCAL_event_evidence_capsule_retained_nested': True,
          'portable_originals': 92, 'archive_and_archive_manifest_additionally_preserved': 2,
          'all94_selected_original_files_exact': True,
          'original_preservation': post, 'original_freeze': r,
          'selected_original_files': [{'path': n, 'destination': str(O/n), 'bytes': len(b), 'sha256': sha(b)} for n, b in sorted(files.items())],
          'private_full_foreign_snapshots_excluded': True,
          'all_six_reader_HOLDs_preserved': True,
          'only_same_original_source_actor_may_later_add_post_integration_preserving_ALL_values': ACTOR,
          'global_site_browser_publication_purification_Goal_acceptance': False}
q = E/'root-actual-source-V-exact-byte-carry.json'
put(q, dump(record))
sp = E/'root-local-process-scripts/carry_actual_sourceV.py'
put(sp, Path(__file__).read_bytes())
stem = '20261110T173428993429Z-cosine-gram-immutable-independent-review-metadata-carrier'
rp = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
x = json.loads(rp.read_bytes())
raw = Path(x['log']).read_bytes()
assert x['exit_code'] == 0 and sha(raw) == x['log_sha256']
extras = []
for dest, b in [(E/'actual-review-layer-checks'/rp.name, rp.read_bytes()),
                (E/'actual-review-layer-checks'/(stem+'.log.gz'), gzip.compress(raw, mtime=0))]:
    put(dest, b)
    extras.append(dest)
paths = [L, C, q, sp] + extras + [O/n for n in files]
raws = {str(p): p.read_bytes() for p in paths}
subprocess.run(['git', 'add', '-f', '--']+list(raws), check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert staged == set(raws), staged ^ set(raws)
for n, b in raws.items():
    assert subprocess.check_output(['git', 'show', ':'+n]) == b, n
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', 'commit', '-m', 'Carry complete original cosine-Gram verification with reader HOLD'], check=True)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert subprocess.check_output(['git', 'rev-parse', commit+'^'], text=True).strip() == carrier
for n, b in raws.items():
    assert subprocess.check_output(['git', 'show', commit+':'+n]) == b, n
out = {'complete_actual_sourceV_carry_commit': commit, 'parent_metadata_carrier': carrier,
       'native_mathematical_commit': native, 'all94_selected_original_files_exact_in_Git_tree': True,
       'all_original_evidence_keys': len(e), 'all_recursive_JSON_nodes': nodes(e),
       'raw_event_sha256': sha(app), 'root_sourceV_API_calls': 0,
       'reader_HOLD_global_purification_Goal_boundaries_preserved': True}
put(W/'complete-actual-sourceV-carry-commit.json', dump(out))
print(json.dumps(out))
