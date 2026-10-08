from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

root = Path.cwd()
label, command = sys.argv[1], sys.argv[2:]
out = root / 'runs/20261007-companion-priority/pbps-centered-defect59/integration59' / label
out.mkdir(parents=True, exist_ok=False)

def pin(path):
    p = Path(path)
    raw = p.read_bytes()
    return dict(path=str(p.resolve()), raw_sha256=hashlib.sha256(raw).hexdigest(),
                lf_sha256=hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest(),
                bytes=len(raw))

head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
with (out / 'stdout.log').open('wb') as stdout, (out / 'stderr.log').open('wb') as stderr:
    child = subprocess.Popen(command, cwd=root, env=env, stdout=stdout, stderr=stderr)
    code = child.wait()
receipt = dict(command=command, cwd=str(root), checked_science_parent=head,
               actual_foreground_pid=child.pid, exit_code=code, terminal_closed=True,
               started_utc=started, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               stdout=pin(out/'stdout.log'), stderr=pin(out/'stderr.log'),
               full_paper_completion=False)
(out/'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(label=label, actual_pid=child.pid, exit_code=code, receipt=str(out/'receipt.json'))))
lines = (out/'stdout.log').read_text(encoding='utf-8', errors='replace').splitlines() + (out/'stderr.log').read_text(encoding='utf-8', errors='replace').splitlines()
for line in lines:
    if any(word in line for word in ['error:', 'Build completed', 'PASS', 'FAIL', 'wrote:', 'checked']):
        print(line)
if code:
    print('\n'.join(lines[-70:]))
sys.exit(code)
