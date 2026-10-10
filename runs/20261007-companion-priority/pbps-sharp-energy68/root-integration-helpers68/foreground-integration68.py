from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

root = Path.cwd()
label, command = sys.argv[1], sys.argv[2:]
out = root / 'runs/20261007-companion-priority/pbps-sharp-energy68' / label
out.mkdir(parents=True, exist_ok=False)

def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), bytes=len(b),
                raw_sha256=hashlib.sha256(b).hexdigest(),
                lf_sha256=hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest())

names = ['lean-toolchain', 'lake-manifest.json', 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean', 'Tests/ProximalBPSActualRootCommutation.lean', 'runs/20261007-companion-priority/pbps-root-commutation67/root.exact-verification67.adoption.json', 'runs/20261007-companion-priority/pbps-sharp-energy-preproof68/root.statement-seal68.json', 'AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean', 'AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean', 'Tests/ProximalBPSSharpCorrectorEnergy.lean', 'research-wiki/frontier-cells/ASTIS-SHARED-hilbert-corrector-square-bound.json', 'research-wiki/frontier-cells/ASTIS-SW-PBPS-sharp-corrector-energy.json']
names += ['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','website/content/publications/hilbert-sharp-quadratic-corrector-bound.json','website/content/publications/pbps-sharp-corrector-energy.json','website/content/declaration_lessons/hilbert-sharp-quadratic-corrector-bound.json','website/content/declaration_lessons/pbps-sharp-corrector-energy.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSSharpCorrectorEnergy.json','runs/20261007-companion-priority/pbps-sharp-energy68/verified.json','runs/20261007-companion-priority/pbps-sharp-energy68/root.exact-verification68.adoption.json']
inputs = [pin(root / name) for name in names if (root / name).is_file()]
snaps = out / 'inputs'; snaps.mkdir(); input_snapshots = []
for i, q in enumerate(inputs):
    b = Path(q['path']).read_bytes()
    rp, lp = snaps / (str(i) + '.exactraw.snapshot'), snaps / (str(i) + '.LF.snapshot')
    rp.write_bytes(b); lp.write_bytes(b.replace(b'\r\n', b'\n'))
    input_snapshots.append(dict(original=q, exact_raw_snapshot=pin(rp), LF_snapshot=pin(lp)))
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
           ASTIS_FOREGROUND_OBSERVER_DIR=out.resolve().as_posix())
env.pop('ELAN_TOOLCHAIN', None)
with (out / 'stdout.log').open('wb') as o, (out / 'stderr.log').open('wb') as e:
    child = subprocess.Popen(command, cwd=root, env=env, stdout=o, stderr=e)
    print(json.dumps(dict(label=label, actual_foreground_pid=child.pid,
                         status='RUNNING_INPUTS_PINNED')), flush=True)
    code = child.wait()
receipt = dict(command=command, cwd=root.as_posix(), checked_science_parent=head,
               started_utc=started, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               actual_foreground_pid=child.pid, exit_code=code, terminal_closed=True,
               inputs=inputs, input_snapshots=input_snapshots,
               stdout=pin(out / 'stdout.log'), stderr=pin(out / 'stderr.log'),
               observer_dir_exclusion='Active observer directory must never be staged.',
               full_paper_completion=False)
(out / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n',
                                  encoding='utf-8', newline='\n')
print(json.dumps(dict(label=label, pid=child.pid, exit_code=code)))
lines = (out / 'stdout.log').read_text(encoding='utf-8', errors='replace').splitlines()
lines += (out / 'stderr.log').read_text(encoding='utf-8', errors='replace').splitlines()
selected = [s for s in lines if any(t in s for t in ['error:', 'error(', 'Build completed', 'PASS', 'FAIL', 'wrote:', 'checked'])]
print('\n'.join(selected[-20:]))
if code: print('\n'.join(lines[-45:]))
sys.exit(code)
