from pathlib import Path
import gzip, hashlib, io, json, re, subprocess, sys, tarfile
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
S = Path('.astis/semantic-neutral-20261111/kr_src_c47e12/phase5-normal-sourceV')
L = Path('runs/substantive_advances.jsonl')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json')
base = 'd4ff03bf3574da615cca39a812cd9b442dca47f0'
aid = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumKrylovRange'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == base
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only']).strip()
assert sha((S/'hash-manifest.json').read_bytes()) == '08b3a509384f614405baf1bdd5f35d30cb552fdbd3d99fd6de6f03041fa76162'
assert sha((S/'original-final-execution-receipt.json').read_bytes()) == '23f97704822d50420636e435b77835b5ed24e102deefa1ccd4e6ce0d11ab8660'
assert sha((S/'audit/0011-exactly-one-normal-VERIFIED.receipt.json').read_bytes()) == 'f8ccd12f26e79ecc516b7f3009a4c3af2d0da876a135a2e4957e9708a50d3783'
m = json.loads((S/'hash-manifest.json').read_bytes())
for row in m['files']:
    p = S/row['path']
    assert sha(p.read_bytes()) == row['sha256'] and p.stat().st_size == row['bytes'], p
    assert p.stat().st_mode & 0o777 == 0o444, p
files = sorted(p for p in S.rglob('*') if p.is_file())
assert len(files) == 98 and {str(p.relative_to(S)) for p in files} == {r['path'] for r in m['files']} | {'hash-manifest.json'}
assert not any(p.is_symlink() for p in S.rglob('*'))
before = subprocess.check_output(['git', 'show', base+':'+str(L)])
after = L.read_bytes()
assert after.startswith(before) and len(before) == 6015724
app = after[len(before):]
assert len(app.splitlines()) == 1 and sha(app) == '959a610cedf1d4f35528664abee862361c636ec1da3ec79f3a91565c29b3e9e9'
assert app == (S/'actual-normal-VERIFIED-append.exact.jsonl').read_bytes()
oldrows = [json.loads(z) for z in before.splitlines()]
newrows = [json.loads(z) for z in after.splitlines()]
oldstates, newstates = [adv._replay_advances(x) for x in [oldrows, newrows]]
assert {a:s for a,s in oldstates.items() if a != aid} == {a:s for a,s in newstates.items() if a != aid}
event = json.loads(app)
ev = event['evidence']
assert newstates[aid]['state'] == 'VERIFIED' and newstates[aid]['latest_evidence'] == ev
assert ev == json.loads((S/'actual-normal-VERIFIED-evidence.full.json').read_bytes())
assert ev['verifier_id'] == ev['normal_VERIFIED_API_actor'] == '/root/krylov_fresh_source_c47e12'
plocal = next(z for z in reversed(oldrows) if z.get('advance_id') == aid and z.get('to_state') == 'PROVED_LOCAL')
assert ev['original_PROVED_LOCAL_event_full'] == plocal
assert ev['original_PROVED_LOCAL_evidence_full'] == plocal['evidence']
assert ev['original_local_proof_capsule_full'] == json.loads((E/'local-proof-capsule.json').read_bytes())
oldcell = json.loads(subprocess.check_output(['git', 'show', base+':'+str(C)]))
newcell = json.loads(C.read_bytes())
assert oldcell['status'] == 'proved_locally' and newcell['status'] == 'independently_verified'
assert {k:v for k,v in oldcell.items() if k != 'status'} == {k:v for k,v in newcell.items() if k != 'status'}
assert newcell['owner_id'] == 'huanjian_gc_20261110_fixed_spectrum_krylov_range'
def nodes(x):
    return 1+sum(nodes(v) for v in x.values()) if isinstance(x,dict) else 1+sum(nodes(v) for v in x) if isinstance(x,list) else 1
assert len(ev) == 29 and nodes(ev) == 1407
dest = E/'actual-source-V'
assert not dest.exists()
dest.mkdir()
target = dest/'phase5-normal-sourceV-all98-original-files.tar.gz'
entries = {}
with target.open('xb') as out:
    with gzip.GzipFile(filename='', fileobj=out, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tf:
            for p in files:
                data = p.read_bytes()
                assert (b'/xwechat'+b'_files/') not in data and not re.search(rb'wx'+rb'id_[a-z0-9]{5,}', data), p
                info = tarfile.TarInfo(str(p.relative_to(S)))
                info.size = len(data);info.mode = 0o444
                tf.addfile(info, io.BytesIO(data))
                entries[info.name] = {'sha256':sha(data),'bytes':len(data),'original_mode':'0444'}
with tarfile.open(target,'r:gz') as tf:
    assert set(tf.getnames()) == set(entries)
    for member in tf:
        assert sha(tf.extractfile(member).read()) == entries[member.name]['sha256']
(dest/'all98-original-files.archive-manifest.json').write_bytes(dump({'archive':str(target),'sha256':sha(target.read_bytes()),'files':entries,'private_foreign_baselines_included':False,'scope':'Exactly98 original portable phase5 files. Private sibling never enumerated, copied or exported.'}))
for name in ['actual-normal-VERIFIED-append.exact.jsonl','actual-normal-VERIFIED-event.full.json','actual-normal-VERIFIED-evidence.full.json','normal-VERIFIED-postguards.full-bounded-result.json','original-final-execution-receipt.json','hash-manifest.json']:
    (dest/name).write_bytes((S/name).read_bytes())
record = {'actual_actor':ev['verifier_id'],'exact_append_sha256':sha(app),'raw_old_ledger_prefix_bytes':len(before),'complete_original_V_top_keys':list(ev),'complete_original_V_recursive_JSON_nodes':nodes(ev),'old316_VERIFIED_objects_raw_prefix_preserved':True,'all299_foreign_states_and_latest_evidence_exact':True,'own_latest_evidence_equals_entire_original_V':True,'full_original_PLOCAL_event_evidence_and_capsule_exact':True,'frontier_only_status_changed_original_owner_preserved':True,'all98_portable_originals_and_original_API_receipt_preserved':True,'private_foreign_baseline_exported':False,'math_commit':ev['mathematical_candidate'],'metadata_checked_commit':ev['metadata_checked_commit'],'root_sourceV_API_calls':0,'reader_global_publication_purification_Goal_complete':False}
(dest/'root-exact-readback.json').write_bytes(dump(record))
scriptcopy = dest/Path(__file__).name
scriptcopy.write_bytes(Path(__file__).read_bytes())
paths = [L,C]+files+sorted(p for p in dest.rglob('*') if p.is_file())
# Retain the four immutable metadata-gate originals at the paths named by V.
for row in json.loads((W/'exact-normal-sourceV-request.json').read_bytes())['actual_metadata_gate_receipts']:
    paths += [Path(row['receipt']),Path(row['log']).relative_to(Path.cwd())]
hashes = {str(p):sha(p.read_bytes()) for p in paths}
subprocess.run(['git','add','-f','--',*hashes],check=True)
staged = subprocess.check_output(['git','diff','--cached','--name-only','-z']).decode().rstrip('\0').split('\0')
assert set(staged) <= set(hashes) and staged
for name in staged:
    assert sha(subprocess.check_output(['git','show',':'+name])) == hashes[name]
check = subprocess.run(['git','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
exceptions = []
if check.returncode:
    assert check.returncode == 2 and not check.stderr
    for line in check.stdout.decode().splitlines():
        mt = re.fullmatch(r'(.+):\d+: new blank line at EOF\.',line)
        assert mt,line
        name = mt.group(1)
        assert name in hashes and (name.startswith(str(S)+'/') or name.startswith(str(dest)+'/')),name
        exceptions.append(name)
    exceptions = sorted(set(exceptions))
    note = dest/'exact-original-EOF-check-scope.json'
    note.write_bytes(dump({'original_git_check_exit':check.returncode,'original_stdout_utf8':check.stdout.decode(),'exceptions':{n:hashes[n] for n in exceptions},'scope':'Only command-local blank-at-eof relaxation for these exact independent original artifacts. All remaining files and all other diagnostics use default checks; no original data normalized.'}))
    hashes[str(note)] = sha(note.read_bytes())
    subprocess.run(['git','add','-f','--',str(note)],check=True)
    subprocess.run(['git','diff','--cached','--check','--','.',*[':(exclude)'+n for n in exceptions]],check=True)
    subprocess.run(['git','-c','core.whitespace=-blank-at-eof','diff','--cached','--check','--',*exceptions],check=True)
subprocess.run(['git','commit','-m','docs(gaussian): preserve complete original Krylov source verification'],check=True)
commit = subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for name,h in hashes.items():
    assert sha(subprocess.check_output(['git','show',commit+':'+name])) == h,name
out = {**record,'complete_original_V_carrier_commit':commit,'all_selected_original_bytes_exact_in_Git':True,'exact_EOF_exceptions':exceptions,'original_portable_files':98}
(W/'actual-complete-original-V-carrier.json').write_bytes(dump(out))
print(json.dumps(out))
