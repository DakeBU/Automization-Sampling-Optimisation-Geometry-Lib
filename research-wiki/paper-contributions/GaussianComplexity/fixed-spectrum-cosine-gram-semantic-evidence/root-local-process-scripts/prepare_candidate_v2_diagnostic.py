from pathlib import Path
import hashlib, json, gzip
W = Path(__file__).parent
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
sha = lambda b: hashlib.sha256(b).hexdigest()
old = (W/'create_mathematical_candidate.py').read_bytes()
for p in [W/'create_mathematical_candidate.attempt1.executed.py', E/'root-local-process-scripts/create_mathematical_candidate.attempt1.executed.py']:
    with p.open('xb') as f:
        f.write(old)
text = old.decode()
text = text.replace("with p.open('xb') as f:\n        f.write(data)", "if p.exists():\n        assert p.read_bytes() == data, p\n        return\n    with p.open('xb') as f:\n        f.write(data)")
text = text.replace("'export_requested_normalization_context.py', 'create_mathematical_candidate.py'", "'export_requested_normalization_context.py', 'create_mathematical_candidate_v2.py', 'prepare_candidate_v2_diagnostic.py'")
text = text.replace("'20261110T165007007580Z-cosine-gram-normal-PROVED-LOCAL-exact-types-and-foreign-preservation',", "'20261110T165007007580Z-cosine-gram-normal-PROVED-LOCAL-exact-types-and-foreign-preservation',")
text = text.replace("rb'wxid_|/Library/Containers/com\\.tencent\\.xinWeChat'", "rb'wxid_[A-Za-z0-9]{6,}|/Library/Containers/com[.]tencent[.]xinWeChat/Data/Documents/'")
assert text != old.decode() and "if p.exists():" in text
new = W/'create_mathematical_candidate_v2.py'
with new.open('xb') as f:
    f.write(text.encode())
stem = '20261110T165128071543Z-cosine-gram-immutable-mathematical-candidate-exact-selected-files'
rp = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
receipt = json.loads(rp.read_bytes())
log = Path(receipt['log']).read_bytes()
assert receipt['exit_code'] == 1 and sha(log) == receipt['log_sha256']
assert receipt['head_before'] == receipt['head_after'] == '75dcc0c9c7d9591384c6e0705e118b1ab440cd6c'
for p, b in [(E/(stem+'.receipt.json'), rp.read_bytes()), (E/(stem+'.log.gz'), gzip.compress(log, mtime=0))]:
    with p.open('xb') as f:
        f.write(b)
diag = {'kind': 'LOCAL_CANDIDATE_PROCESS_PREFLIGHT_FAILED',
        'reason': 'The privacy detector matched its own literal identifier prefix in its own staged-script input. No actual private identifier was observed. Failure occurred before git add/commit; normal PROVED_LOCAL had already succeeded and is not replayed.',
        'repair': 'The new detector requires an actual identifier suffix or concrete container document path; all original executed script bytes and real failure receipt/output are preserved. Existing exact scaffolding is checked byte-for-byte rather than rewritten.',
        'original_executed_script_sha256': sha(old), 'new_script_sha256': sha(text.encode()),
        'normal_API_replay': False}
(E/'candidate-preflight-self-match-diagnostic.json').write_text(json.dumps(diag, indent=2)+'\n')
print(json.dumps(diag))
