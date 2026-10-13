from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
R = Path('E:/Samplinglib')
r = Path(__file__).parent
f = R / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean'
p = r / 'focused' / sys.argv[1]
p.mkdir(exist_ok=False, parents=True)
(p / 'module.exactraw.snapshot.lean').write_bytes(f.read_bytes())
env = os.environ.copy()
env['PATH'] = str(R / '.astis/toolchain/lean-4.33.0-windows/bin') + os.pathsep + env['PATH']
env.pop('ELAN_TOOLCHAIN', None)
args = [str(R / '.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'), 'env', 'lean', str(f)]
t = time.monotonic()
q = subprocess.run(args, cwd=R, capture_output=True, env=env)
(p / 'stdout.log').write_bytes(q.stdout)
(p / 'stderr.log').write_bytes(q.stderr)
receipt = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), command=args, exit_code=q.returncode, terminal_closed=True, seconds=time.monotonic()-t, module_raw_sha256=hashlib.sha256(f.read_bytes()).hexdigest(), statement_seal_raw_sha256=hashlib.sha256((r / 'root.statement-seal89.json').read_bytes()).hexdigest())
(p / 'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf8', newline='\n')
lines = q.stdout.decode(errors='replace').splitlines()
errors = [i for i,x in enumerate(lines) if ': error:' in x]
for k,i in enumerate(errors):
    part = lines[i:errors[k+1] if k+1<len(errors) else len(lines)]
    print('\n'.join(part[:8]))
    goals = [j for j,x in enumerate(part) if x.startswith('⊢')]
    if goals:
        print('FINAL GOAL:', '\n'.join(part[goals[-1]:goals[-1]+8]))
print(json.dumps(receipt), 'ERROR_COUNT', len(errors))
print(q.stderr.decode(errors='replace')[-1000:])
