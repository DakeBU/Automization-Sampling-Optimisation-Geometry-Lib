"""Statement elaboration and bounded source/API retrieval only, before sealing."""
import datetime
import hashlib
import json
import os
import subprocess
import time
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "header-elaboration90-v2"
OUT.mkdir(exist_ok=False)
HEADER = HERE / "header90.v2.proposed.lean"

def desc(p):
    b = p.read_bytes()
    return {"path": str(p), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

env = os.environ.copy()
env["PATH"] = str(ROOT / ".astis/toolchain/lean-4.33.0-windows/bin") + os.pathsep + env["PATH"]
env.pop("ELAN_TOOLCHAIN", None)
args = [str(ROOT / ".astis/toolchain/lean-4.33.0-windows/bin/lake.exe"), "env", "lean", str(HEADER)]
started = time.monotonic()
q = subprocess.run(args, cwd=ROOT, env=env, capture_output=True)
(OUT / "stdout.log").write_bytes(q.stdout)
(OUT / "stderr.log").write_bytes(q.stderr)
receipt = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "command": args, "exit_code": q.returncode, "terminal_closed": True,
           "seconds": time.monotonic()-started, "header": desc(HEADER),
           "proof_BODY_present": False, "statement_sealed": False}
(OUT / "receipt.json").write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
print(json.dumps(receipt))
print(q.stdout.decode(errors="replace")[:3000])
print(q.stderr.decode(errors="replace")[:1000])
