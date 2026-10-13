from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

root = Path.cwd()
label, command = sys.argv[1], sys.argv[2:]
r = root / 'runs/20261007-companion-priority/pbps-reflection-intertwining69'
assert r.is_dir(), 'Claim the sealed SAU before proof execution.'
out = r / label
out.mkdir(parents=True, exist_ok=False)

def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), bytes=len(b),
                raw_sha256=hashlib.sha256(b).hexdigest(),
                lf_sha256=hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest())

pre = root / 'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69'
names = [root/'lean-toolchain', root/'lake-manifest.json',
         root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean',
         root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean',
         root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean',
         root/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-reflection-intertwining.json',
         pre/'root.statement-seal69.json', pre/'root.header69.adoption.json',
         pre/'root.primary69.adoption.json', pre/'root.library-retrieval69.json',
         pre/'root.library-retrieval69.extension.json']
inputs = [pin(p) for p in names if p.is_file()]
snaps = out/'inputs'; snaps.mkdir()
for i, q in enumerate(inputs):
    b = Path(q['path']).read_bytes()
    (snaps/f'{i}.exactraw.snapshot').write_bytes(b)
    (snaps/f'{i}.LF.snapshot').write_bytes(b.replace(b'\r\n', b'\n'))
head = subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
           ASTIS_FOREGROUND_OBSERVER_DIR=out.resolve().as_posix())
env.pop('ELAN_TOOLCHAIN', None)
with (out/'stdout.log').open('wb') as o, (out/'stderr.log').open('wb') as e:
    child = subprocess.Popen(command, cwd=root, env=env, stdout=o, stderr=e)
    print(json.dumps(dict(label=label, actual_foreground_pid=child.pid,
                         status='RUNNING_INPUTS_PINNED')), flush=True)
    code = child.wait()
receipt = dict(command=command, cwd=root.as_posix(), checked_parent=head,
               started_utc=started, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               actual_foreground_pid=child.pid, exit_code=code, terminal_closed=True,
               inputs=inputs, stdout=pin(out/'stdout.log'), stderr=pin(out/'stderr.log'),
               observer_dir_exclusion='Active observer directory is not staged.',
               full_paper_completion=False)
(out/'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(label=label, pid=child.pid, exit_code=code)))
lines = (out/'stdout.log').read_text(encoding='utf-8', errors='replace').splitlines()
lines += (out/'stderr.log').read_text(encoding='utf-8', errors='replace').splitlines()
selected = [s for s in lines if any(t in s for t in ['error:', 'error(', 'Build completed', 'PASS', 'FAIL', 'checked'])]
print('\n'.join(selected[-20:]))
if code: print('\n'.join(lines[-45:]))
sys.exit(code)
