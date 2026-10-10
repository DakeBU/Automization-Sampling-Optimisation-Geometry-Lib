"""Foreground, terminal-receipted acceptance checks for serialized SAU80."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

run = Path("runs/20261007-companion-priority/pbps-actual-physical-time-measurability80")
out = run / "integration80"
assert out.exists()
env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf8", PYTHONUNBUFFERED="1")
env.pop("ELAN_TOOLCHAIN", None)
env["PATH"] = str(Path(".astis/toolchain/lean-4.33.0-windows/bin").resolve()) + os.pathsep + env["PATH"]
py = sys.executable
base = "bdc743c8022ef5e682f38ecac2f8e5a9815ff3de"

def gate(label, command):
    dest = out / label
    dest.mkdir(exist_ok=False)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (dest / "stdout.log").open("wb") as stdout, (dest / "stderr.log").open("wb") as stderr:
        process = subprocess.Popen(command, env=env, stdout=stdout, stderr=stderr)
        print(f"{label}: foreground PID {process.pid}", flush=True)
        code = process.wait()
    receipt = {"command": command, "actual_PID": process.pid, "exit_code": code,
               "terminal_closed": True, "started_utc": started,
               "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "checked_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()}
    for key in ("stdout", "stderr"):
        p = dest / (key + ".log")
        raw = p.read_bytes()
        receipt[key] = {"path": p.as_posix(), "RAW_sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    (dest / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"{label}: EXIT {code}", flush=True)
    if code:
        print((dest / "stdout.log").read_text(encoding="utf-8", errors="replace")[-11000:])
        print((dest / "stderr.log").read_text(encoding="utf-8", errors="replace")[-5000:])
        raise SystemExit(code)

if sys.argv[1] == "aggregate":
    gate("canonical-lean-gate", [py, "-X", "utf8", "website/scripts/lean_gate.py"])
    gate("python-compile", [py, "-m", "py_compile", "tools/astis.py"])
elif sys.argv[1] == "publication":
    for label, args in [
        ("contributor", ["tools/astis_contributor_contract.py", "check", "--base", base]),
        ("publication", ["tools/astis_publication.py", "check", "--base", base]),
        ("semantic", ["tools/astis_semantic_roundtrip.py", "check"]),
        ("frontier", ["tools/astis_frontier_cells.py", "check"]),
        ("site-build", ["website/scripts/build_site.py"]),
        ("underlying-graph", ["website/scripts/underlying_lean_graph.py"]),
        ("graph-check", ["tools/astis_publication.py", "graph-check", "--cell", "ASTIS-SW-PBPS-actual-physical-time-measurability"]),
        ("site-check", ["website/scripts/check_site.py"]),
    ]:
        gate(label, [py, "-X", "utf8", *args])
    gate("diff-check", ["git", "-c", "core.whitespace=cr-at-eol", "diff", "--check"])
elif sys.argv[1] == "ci-base":
    gate("ci-full-base-publication", [py, "-X", "utf8", "tools/astis_publication.py", "check", "--base", "c05de12e6a8ca7af8ce2df8608836f8d4e90f617"])
else:
    raise ValueError(sys.argv[1])
