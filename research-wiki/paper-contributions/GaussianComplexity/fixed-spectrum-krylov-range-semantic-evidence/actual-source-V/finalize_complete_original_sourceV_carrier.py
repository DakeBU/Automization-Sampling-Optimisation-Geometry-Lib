from pathlib import Path
import hashlib, json, re, subprocess

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
D = E/'actual-source-V'
S = Path('.astis/semantic-neutral-20261111/kr_src_c47e12/phase5-normal-sourceV')
base = 'd4ff03bf3574da615cca39a812cd9b442dca47f0'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == base
manifest = json.loads((S/'hash-manifest.json').read_bytes())
for row in manifest['files']:
    assert sha((S/row['path']).read_bytes()) == row['sha256']
allowed = {'runs/substantive_advances.jsonl','research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json'}
allowed |= {str(p) for p in S.rglob('*') if p.is_file()}
allowed |= {str(p) for p in D.rglob('*') if p.is_file()}
for row in json.loads((W/'exact-normal-sourceV-request.json').read_bytes())['actual_metadata_gate_receipts']:
    allowed |= {row['receipt'],str(Path(row['log']).relative_to(Path.cwd()))}
staged = subprocess.check_output(['git','diff','--cached','--name-only','-z']).decode().rstrip('\0').split('\0')
assert staged and set(staged) <= allowed
hashes = {n:sha(Path(n).read_bytes()) for n in staged}
for n,h in hashes.items():
    assert sha(subprocess.check_output(['git','show',':'+n])) == h
result = subprocess.run(['git','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
assert result.returncode == 2 and not result.stderr
exceptions = {}
expect_context = False
for line in result.stdout.decode().splitlines():
    match = re.fullmatch(r'(.+):\d+: (new blank line at EOF|trailing whitespace)\.',line)
    if match:
        n,kind = match.groups()
        assert n in hashes and n.startswith(str(S)+'/'),n
        if kind == 'trailing whitespace':
            assert n.endswith('.stdout'),n
        exceptions.setdefault(n,set()).add('blank-at-eof' if kind.startswith('new blank') else 'blank-at-eol')
        expect_context = kind == 'trailing whitespace'
    else:
        assert expect_context and line.startswith('+'),line
        expect_context = False
note = D/'exact-original-whitespace-exceptions.json'
assert not note.exists()
note.write_bytes(dump({'original_git_check_exit':2,'original_stdout_utf8':result.stdout.decode(),'exceptions':{n:{'sha256':hashes[n],'disabled_flags':sorted(flags)} for n,flags in exceptions.items()},'reason':'Exact independent original API-source-window stdout includes numbered blank lines ending in space, and original scripts/tool-envelope JSON include terminal blank lines. No original is normalized. Command-local exceptions apply only to these exact byte-hashed raw artifacts; every other staged file uses default whitespace checks.','root_normal_V_API_calls':0}))
sc = D/Path(__file__).name
sc.write_bytes(Path(__file__).read_bytes())
failure = Path('.astis/huanjian-resume-20261103/20261110T211953884229Z-krylov-range-complete-original-29-key-1407-node-sourceV-carrier-no-replay.receipt.json')
fr = json.loads(failure.read_bytes())
assert fr['exit_code'] == 1 and sha(Path(fr['log']).read_bytes()) == fr['log_sha256']
extra = [note,sc,failure,Path(fr['log']).relative_to(Path.cwd())]
for p in extra:
    hashes[str(p)] = sha(p.read_bytes())
subprocess.run(['git','add','-f','--',*[str(p) for p in extra]],check=True)
subprocess.run(['git','diff','--cached','--check','--','.',*[':(exclude)'+n for n in exceptions]],check=True)
groups = {}
for n,flags in exceptions.items():
    groups.setdefault(tuple(sorted(flags)),[]).append(n)
for flags,names in groups.items():
    subprocess.run(['git','-c','core.whitespace='+','.join('-'+f for f in flags),'diff','--cached','--check','--',*names],check=True)
subprocess.run(['git','commit','-m','docs(gaussian): preserve complete original Krylov source verification'],check=True)
commit = subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for n,h in hashes.items():
    assert sha(subprocess.check_output(['git','show',commit+':'+n])) == h,n
record = json.loads((D/'root-exact-readback.json').read_bytes())
out = {**record,'complete_original_V_carrier_commit':commit,'all_selected_original_bytes_exact_in_Git':True,'exact_original_whitespace_exception_files':len(exceptions),'original_portable_files':98,'carrier_attempt_failure_preserved_without_any_normal_API_replay':True}
(W/'actual-complete-original-V-carrier.json').write_bytes(dump(out))
print(json.dumps(out))
