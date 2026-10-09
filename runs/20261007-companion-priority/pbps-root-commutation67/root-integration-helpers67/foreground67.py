from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

root = Path.cwd()
label, command = sys.argv[1], sys.argv[2:]
out = root / 'runs/20261007-companion-priority/pbps-root-commutation67' / label
out.mkdir(parents=True, exist_ok=False)

def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), bytes=len(b),
                raw_sha256=hashlib.sha256(b).hexdigest(),
                lf_sha256=hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest())

names = [
    'AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean',
    'AutoSamplingTheory/TechnicalLemmas/Measure/L2Expectation.lean',
    'AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean',
    'Tests/ProximalBPSAmbientAdjointCorrector.lean', 'lean-toolchain', 'lake-manifest.json',
    'AutoSamplingTheory/TechnicalLemmas/Registry.lean', 'AutoSamplingTheory/TechnicalLemmas.lean',
    'AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareOrder.lean',
    'research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-order.json',
    'website/content/publications/real-l2-positive-square-order.json',
    'website/content/declaration_lessons/real-l2-positive-square-order.json',
    'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-RealL2PositiveSquareOrder.json',
    'AutoSamplingTheory/ExampleCases.lean', 'Tests.lean', 'Tests/Basic.lean',
    'research-wiki/frontier-cells/ASTIS-SW-PBPS-ambient-adjoint-corrector.json',
    'website/content/publications/pbps-ambient-adjoint-corrector.json',
    'website/content/declaration_lessons/pbps-ambient-adjoint-corrector.json',
    'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSAmbientAdjointCorrector.json']
names += ['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareCommute.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean','Tests/ProximalBPSActualRootCommutation.lean','runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67/root.statement-seal67.json']
names += ['research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-commutation.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-root-inverse-commutation.json','website/content/publications/real-l2-positive-square-commutation.json','website/content/publications/pbps-actual-root-inverse-commutation.json','website/content/declaration_lessons/real-l2-positive-square-commutation.json','website/content/declaration_lessons/pbps-actual-root-inverse-commutation.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-RealL2PositiveSquareCommutation.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualRootInverseCommutation.json','runs/20261007-companion-priority/pbps-root-commutation67/math-freeze.json']
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
