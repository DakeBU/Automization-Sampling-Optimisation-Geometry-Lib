from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

root = Path.cwd()
r = root / 'runs/20261007-companion-priority/pbps-actual-harmonic-flow73'
pre = root / 'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73'
label, command = sys.argv[1], sys.argv[2:]
assert (r / 'claim.json').is_file()
out = r / label
out.mkdir(parents=True, exist_ok=False)
def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), RAW_bytes=len(b), RAW_sha256=hashlib.sha256(b).hexdigest(), LF_sha256=hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest())
paths = [root / p for p in ['lean-toolchain', 'lake-manifest.json', 'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean', 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean', 'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json']]
paths += [pre / p for p in ['header73.proposed.lean', 'root.statement-seal73.json', 'root.header-math73.adoption.json', 'root.header-source73.adoption.json']]
inputs = [pin(p) for p in paths if p.is_file()]
snap = out / 'inputs'
snap.mkdir()
for i, z in enumerate(inputs):
    b = Path(z['path']).read_bytes()
    (snap / f'{i}.exactraw.snapshot').write_bytes(b)
    (snap / f'{i}.LF.snapshot').write_bytes(b.replace(b'\r\n', b'\n'))
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf8', ASTIS_FOREGROUND_OBSERVER_DIR=out.resolve().as_posix())
env.pop('ELAN_TOOLCHAIN', None)
with (out / 'stdout.log').open('wb') as stdout, (out / 'stderr.log').open('wb') as stderr:
    child = subprocess.Popen(command, cwd=root, env=env, stdout=stdout, stderr=stderr)
    print(json.dumps(dict(label=label, actual_foreground_PID=child.pid, status='RUNNING_INPUTS_PINNED')), flush=True)
    code = child.wait()
receipt = dict(command=command, checked_parent=head, started_utc=started, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), actual_foreground_PID=child.pid, exit_code=code, terminal_closed=True, inputs=inputs, stdout=pin(out / 'stdout.log'), stderr=pin(out / 'stderr.log'), Goal_complete=False)
(out / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print(json.dumps(dict(label=label, PID=child.pid, EXIT=code)))
lines = (out / 'stdout.log').read_text(encoding='utf8', errors='replace').splitlines() + (out / 'stderr.log').read_text(encoding='utf8', errors='replace').splitlines()
chosen = [s for s in lines if any(t in s for t in ['error:', 'error(', 'Build completed', 'PASS', 'FAIL', 'depends on axioms:'])]
print('\n'.join(chosen[-24:]))
if code:
    print('\n'.join(lines[-90:]))
sys.exit(code)
