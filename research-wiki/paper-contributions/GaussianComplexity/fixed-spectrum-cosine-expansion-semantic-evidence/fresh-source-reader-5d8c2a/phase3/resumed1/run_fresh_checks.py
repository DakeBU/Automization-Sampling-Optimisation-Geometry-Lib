from pathlib import Path
import subprocess, json, hashlib, os, time
from datetime import datetime, timezone

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = ROOT / '.astis/semantic-neutral-20261109/src_cosine_5d8c2a/phase3/resumed1'
FRESH = OUT / 'fresholean'
LEAN = Path('/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean')
sha = lambda b: hashlib.sha256(b).hexdigest()

def run(label, args, env=None):
    started = datetime.now(timezone.utc).isoformat()
    before = time.monotonic()
    print('START', label, flush=True)
    result = subprocess.run(args, cwd=ROOT, env=env, capture_output=True)
    (OUT / (label + '.stdout')).write_bytes(result.stdout)
    (OUT / (label + '.stderr')).write_bytes(result.stderr)
    receipt = {'label': label, 'argv': [str(a) for a in args], 'cwd': str(ROOT),
               'started_utc': started, 'elapsed_seconds': time.monotonic()-before,
               'exit_code': result.returncode, 'stdout_sha256': sha(result.stdout),
               'stderr_sha256': sha(result.stderr),
               'LEAN_PATH': None if env is None else env.get('LEAN_PATH')}
    (OUT / (label + '.receipt.json')).write_text(json.dumps(receipt, indent=2)+'\n')
    print('END', label, result.returncode, flush=True)
    if result.returncode:
        print(result.stdout.decode(errors='replace'), result.stderr.decode(errors='replace'), flush=True)
        raise SystemExit(result.returncode)
    return result.stdout.decode()

if __name__ == '__main__':
    assert run('010-head', ['git','rev-parse','HEAD']).strip() == '37645c774481c4cad19fc29bcaa76799da64db7d'
    assert run('011-tracked-status', ['git','status','--short','--untracked-files=no']).strip() == ''
    version = run('012-lean-version', [str(LEAN), '--version'])
    assert 'version 4.33.0' in version and 'd8b18978322de05a8f3dba51ef03cf5461676c17' in version
    manifest_bytes = (ROOT/'lake-manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    assert len(manifest['packages']) == 9
    pins = []
    libs = []
    for i, pkg in enumerate(manifest['packages']):
        path = ROOT/'.lake/packages'/pkg['name']
        observed = run(f'020-pin-{i}-{pkg["name"]}', ['git','-C',str(path),'rev-parse','HEAD']).strip()
        status = run(f'021-clean-{i}-{pkg["name"]}', ['git','-C',str(path),'status','--porcelain','--untracked-files=no']).strip()
        assert observed == pkg['rev'], (pkg['name'], observed, pkg['rev'])
        assert status == '', (pkg['name'], status)
        lib = path/'.lake/build/lib/lean'
        assert lib.is_dir(), str(lib)
        libs.append(str(lib))
        pins.append({'name':pkg['name'],'url':pkg['url'],'expected_rev':pkg['rev'],'observed_rev':observed,'tracked_clean':True,'lib_path':str(lib)})
    FRESH.mkdir(exist_ok=False)
    env = dict(os.environ)
    env['LEAN_PATH'] = ':'.join([str(FRESH), str(ROOT/'.lake/build/lib/lean')] + libs)
    (OUT/'fresh-environment.json').write_text(json.dumps({'lean_executable':str(LEAN),'lean_executable_sha256':sha(LEAN.read_bytes()),'lean_version':version.strip(),'toolchain_file_sha256':sha((ROOT/'lean-toolchain').read_bytes()),'manifest_sha256':sha(manifest_bytes),'pins':pins,'LEAN_PATH':env['LEAN_PATH'],'fresholean_first':True,'fresholean_did_not_exist_before_run':True,'dependency_scope':'Reuse exact pinned existing dependency oleans; compile both candidate modules independently into this new first-path directory.'},indent=2)+'\n')
    for label, module in [('030-fresh-production','AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumCosineExpansion'),('031-fresh-test','Tests/GaussianComplexityFixedSpectrumCosineExpansion')]:
        dest = FRESH / (module + '.olean')
        dest.parent.mkdir(parents=True, exist_ok=True)
        run(label, [str(LEAN), '-o', str(dest), module+'.lean'], env)
    print('FRESH_CANDIDATE_MODULES_COMPILED', flush=True)
