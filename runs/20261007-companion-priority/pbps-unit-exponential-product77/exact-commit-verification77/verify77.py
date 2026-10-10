"""Independent foreground exact-commit verifier; honest input/command receipts only."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/pbps-unit-exponential-product77/exact-commit-verification77'
COMMIT = '4f88383540a865aea304c63c40de5a699ea61611'
ORIGINAL_COMMIT = '24cacd367f9936a68fc709a02b3b051802033aa6'
BASE = '10ca06b04634e95ff67b461c7b37c9cee0931998'
MODULE = 'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
DECL = 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
AUDIT = 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-UnitExponentialProduct.json'
LAKE = str(ROOT / '.astis/toolchain/lean-4.33.0-windows/bin/lake.exe')
LEAN = str(ROOT / '.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
os.environ['PYTHONUTF8'] = '1'
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
OUT.mkdir(parents=True, exist_ok=True)

def sha(data): return hashlib.sha256(data).hexdigest()
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name, value):
    p = OUT / name
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return p
def info(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': str(p), 'RAW_bytes': len(b), 'RAW_sha256': sha(b)}
def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True).stdout
def run(name, args):
    if '--finish-only' in sys.argv:
        previous=json.loads((OUT/(name+'.receipt.json')).read_text(encoding='utf-8'))
        assert previous['exit_code']==0 and previous['terminal_closed'] and previous['command']==args
        assert info(previous['stdout']['path'])['RAW_sha256']==previous['stdout']['RAW_sha256']
        assert info(previous['stderr']['path'])['RAW_sha256']==previous['stderr']['RAW_sha256']
        print(name,'EXACT_TERMINAL_RECEIPT_REUSED',flush=True)
        return previous
    start = stamp()
    with (OUT / (name+'.stdout.log')).open('wb') as stdout, (OUT / (name+'.stderr.log')).open('wb') as stderr:
        child = subprocess.Popen(args, cwd=ROOT, stdout=stdout, stderr=stderr, env=os.environ.copy())
        code = child.wait()
    receipt = {'command': args, 'cwd': str(ROOT), 'started_utc': start,
        'finished_utc': stamp(), 'actual_foreground_PID': child.pid, 'exit_code': code,
        'terminal_closed': True, 'checked_commit': COMMIT, 'inputs': frozen,
        'stdout': info(OUT/(name+'.stdout.log')), 'stderr': info(OUT/(name+'.stderr.log')),
        'provenance': 'Real subprocess invocation and terminal result. No native reasoning trajectory claimed.'}
    save(name+'.receipt.json', receipt)
    print(name, 'EXIT', code, flush=True)
    if code: raise RuntimeError(name + ' failed; inspect retained stdout/stderr')
    return receipt

def freeze():
    assert git('rev-parse', COMMIT).decode().strip() == COMMIT
    science = [MODULE, 'lean-toolchain', 'lake-manifest.json',
       'website/content/declaration_lessons/unit-exponential-product.json',
       'website/content/publications/unit-exponential-product.json', AUDIT,
       'runs/20261007-companion-priority/pbps-unit-exponential-product77/source-review.packet.json',
       'runs/20261007-companion-priority/pbps-unit-exponential-product77/root.math77.adoption.json',
       'runs/20261007-companion-priority/pbps-unit-exponential-product77/root.decoder77.adoption.json',
       'runs/20261007-companion-priority/pbps-unit-exponential-product77/root.source77.adoption.json']
    matches = []
    for path in science:
        blob = git('show', COMMIT+':'+path)
        raw = (ROOT/path).read_bytes()
        same = blob == raw
        normalized = blob.replace(b'\r\n',b'\n') == raw.replace(b'\r\n',b'\n')
        assert same or (path in {'lean-toolchain','lake-manifest.json'} and normalized), 'Exact-commit mismatch: '+path
        matches.append({**info(ROOT/path), 'git_blob_raw_sha256': sha(blob), 'exact_equal': same,
            'LF_equal': normalized, 'newline_only_checkout_difference': not same})
    module = (ROOT/MODULE).read_bytes()
    assert sha(module) == 'c4a93999f287008d9ddb3f3624f52f302df122e5e007a54fd427a9985edc5ec0'
    (OUT/'module.exactraw.lean').write_bytes(module)
    lesson = json.loads((ROOT/science[3]).read_text(encoding='utf-8'))['units'][0]
    lines = module.splitlines(keepends=True)
    regions = []
    for step in lesson['steps']:
        region = step['lean_source_region']
        code = b''.join(lines[region['start_line']-1:region['end_line']])
        assert code == step['lean'].encode('utf-8')
        assert sha(code) == region['exact_code_raw_sha256']
        assert region['source_raw_sha256'] == sha(module)
        assert step['formula'] and step['text']
        regions.append({'title': step['title'], 'start': region['start_line'], 'end': region['end_line'], 'sha256':sha(code)})
    assert len(regions)==7
    assert ''.join(s['lean'] for s in lesson['steps']).encode('utf-8') == b''.join(lines[34:126])
    audit=json.loads((ROOT/AUDIT).read_text(encoding='utf-8'))
    assert audit['state']=='accepted'
    manifest=ROOT/'runs/20261007-companion-priority/pbps-unit-exponential-product77/resume-source-review77/review-run-manifest.json'
    review=json.loads(manifest.read_text(encoding='utf-8'))
    for entry in review['inputs']:
        assert sha((ROOT/entry['path']).read_bytes())==entry['raw_sha256'],entry['path']
    save('input-freeze.json', {'checked_commit':COMMIT,'head_at_freeze':git('rev-parse','HEAD').decode().strip(),
         'exact_commit_matches':matches,'source_review_manifest':info(manifest),'all_source_review_input_hashes_unchanged':True,
         'seven_contiguous_exact_BODY_regions':regions, 'full_public_BODY_covered':True,
         'audit_state':audit['state'], 'scope':'Actual Exp(1) input-law leaf only; direct author moment route and actual process Ex9 remain open.'})
    return matches

frozen=freeze()
if '--after-frontier' in sys.argv:
    changed=git('diff','--name-only',ORIGINAL_COMMIT,COMMIT).decode().splitlines()
    assert set(changed)=={'research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json',
        'runs/20261007-companion-priority/pbps-unit-exponential-product77/resume-20261010/adopt_and_checkpoint.py'}
    oldcell=json.loads(git('show',ORIGINAL_COMMIT+':research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json'))
    newcell=json.loads(git('show',COMMIT+':research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json'))
    assert oldcell['source_detail_audit']['detail_status']=='recovered'
    oldcell['source_detail_audit']['detail_status']='omitted'
    assert oldcell==newcell
    assert (ROOT/'research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json').read_bytes()==git('show',COMMIT+':research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json')
    save('successor-delta.json',{'original_commit':ORIGINAL_COMMIT,'successor_commit':COMMIT,
        'changed_files':changed,'cell_semantic_delta':'source_detail_audit.detail_status recovered -> omitted only',
        'unchanged_whole_module_sha256':sha((ROOT/MODULE).read_bytes()),
        'retained_original_failed_frontier_receipt':info(OUT/'frontier.receipt.json'),
        'reused_unchanged_fresh_whole_source_receipt':info(OUT/'fresh-whole-module-axioms.receipt.json'),
        'new_source_or_proof_review_needed':False})
if len(sys.argv)>1 and sys.argv[1]=='freeze':
    print('FREEZE PASS',flush=True)
    raise SystemExit(0)

probe=OUT/'FreshWholeModuleAxioms77.lean'
probe.write_bytes((ROOT/MODULE).read_bytes()+ ('\n/- Independent exact-commit fresh whole-module elaboration and axiom inspection. -/\n#print axioms '+DECL+'\n#check '+DECL+'\n').encode('utf-8'))
frozen.append(info(probe))
if '--after-fresh' not in sys.argv and '--after-frontier' not in sys.argv:
    run('lean-version',[LEAN,'--version'])
    run('fresh-whole-module-axioms',[LAKE,'env',LEAN,str(probe)])
else:
    previous=json.loads((OUT/'fresh-whole-module-axioms.receipt.json').read_text(encoding='utf-8'))
    assert previous['exit_code']==0 and previous['terminal_closed']
    assert previous['inputs'][-1]['RAW_sha256']==info(probe)['RAW_sha256']
    assert previous['stdout']['RAW_sha256']==info(OUT/'fresh-whole-module-axioms.stdout.log')['RAW_sha256']
output=(OUT/'fresh-whole-module-axioms.stdout.log').read_text(encoding='utf-8')
axioms=re.search(r'depends on axioms: \[([^\]]+)\]',output)
assert axioms and set(a.strip() for a in axioms.group(1).split(','))=={'propext','Classical.choice','Quot.sound'}
if '--after-frontier' not in sys.argv:
    run('focused-module',[LAKE,'build','AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct'])
    run('contributor',[sys.executable,'-X','utf8','tools/astis_contributor_contract.py','check','--base',BASE])
    run('publication',[sys.executable,'-X','utf8','tools/astis_publication.py','check','--base',BASE])
    run('semantic',[sys.executable,'-X','utf8','tools/astis_semantic_roundtrip.py','check'])
else:
    for name in ['focused-module','contributor','publication','semantic']:
        assert json.loads((OUT/(name+'.receipt.json')).read_text(encoding='utf-8'))['exit_code']==0
    run('contributor-successor',[sys.executable,'-X','utf8','tools/astis_contributor_contract.py','check','--base',BASE])
    run('publication-successor',[sys.executable,'-X','utf8','tools/astis_publication.py','check','--base',BASE])
    run('semantic-successor',[sys.executable,'-X','utf8','tools/astis_semantic_roundtrip.py','check'])
frozen.append(info(ROOT/'research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json'))
run('frontier-recheck' if '--after-frontier' in sys.argv else 'frontier',[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'])
run('packet',[sys.executable,'-X','utf8','tools/astis_publication.py','packet','--cell','ASTIS-SHARED-unit-exponential-product'])
packet=json.loads((OUT/'packet.stdout.log').read_text(encoding='utf-8'))
assert packet['targets'][0]['publication_binding_sha256']=='465fcece1be5adf9e62da6bad2639b3d4c65943b35b733b75e6f44227b6e09bf'
sys.path.insert(0,str(ROOT/'tools'))
from tools import astis
hits=astis.forbidden_pattern_hits()
save('fake-closure-scan.json',{'verifier_id':'/root/exact_verify77','checked_commit':COMMIT,
    'algorithm':'tools.astis.forbidden_pattern_hits (same production scan as astis.py check)',
    'scanned_files':len(astis.lean_source_files()),'hits':hits,'module_sha256':sha((ROOT/MODULE).read_bytes()),
    'scope':'Production closure scan only; full ASTIS aggregate Lake build is a later stabilization gate.'})
assert not hits
freeze()
save('checks-complete.json',{'status':'PASS','checked_commit':COMMIT,'verifier_id':'/root/exact_verify77',
    'fresh_full_source_elaboration':True,'axioms':['propext','Classical.choice','Quot.sound'],
    'checks':['focused-module','contributor','publication','semantic','frontier','packet','fake-closure-scan'],
    'publication_binding_sha256':packet['targets'][0]['publication_binding_sha256'],
    'aggregate_ASTIS_check':'Pending stabilization; not run by this bounded verifier.'})
print('ALL BOUNDED CHECKS PASS',flush=True)
