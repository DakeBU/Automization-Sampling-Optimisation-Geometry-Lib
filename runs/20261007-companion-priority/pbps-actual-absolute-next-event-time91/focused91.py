from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time

root = Path.cwd()
run = Path(__file__).parent
f = root / "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean"
p = run / "focused" / sys.argv[1]
p.mkdir(exist_ok=False, parents=True)
snapshot = f.read_bytes()
(p / "module.exactraw.snapshot.lean").write_bytes(snapshot)
env = os.environ.copy()
env["PATH"] = str(root / ".astis/toolchain/lean-4.33.0-windows/bin") + os.pathsep + env["PATH"]
env.pop("ELAN_TOOLCHAIN", None)
argv = [str(root / ".astis/toolchain/lean-4.33.0-windows/bin/lake.exe"), "env", "lean", str(f)]
t = time.monotonic()
q = subprocess.run(argv, cwd=root, env=env, capture_output=True)
(p / "stdout.log").write_bytes(q.stdout)
(p / "stderr.log").write_bytes(q.stderr)
assert f.read_bytes() == snapshot
receipt = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "command": argv,
    "exit_code": q.returncode, "terminal_closed": True, "seconds": time.monotonic() - t,
    "module_raw_sha256": hashlib.sha256(snapshot).hexdigest(),
    "statement_seal_raw_sha256": hashlib.sha256((run / "root.statement-seal91.json").read_bytes()).hexdigest(),
}
(p / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
lines = q.stdout.decode(errors="replace").splitlines()
errors = [i for i, line in enumerate(lines) if ": error:" in line]
for k, i in enumerate(errors):
    chunk = lines[i:errors[k + 1] if k + 1 < len(errors) else len(lines)]
    print("\n".join(chunk[:8]))
    goals = [j for j, line in enumerate(chunk) if line.startswith("⊢")]
    if goals:
        print("FINAL GOAL:", "\n".join(chunk[goals[-1]:goals[-1] + 8]))
print(json.dumps(receipt), "ERROR_COUNT", len(errors))
print(q.stderr.decode(errors="replace")[-1000:])
