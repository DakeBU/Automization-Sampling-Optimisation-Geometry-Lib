"""Compile the owned, non-admitted Bench candidates with pinned Lake.

Build only the two declared predecessors into a fresh private directory.
The padded witness imports those checked candidates; no source is duplicated,
and no task packet, submission, model or network service is involved.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "benchmarks/samplingoptimisationgeometrybench/candidates"
STAGING = ROOT / ".astis/sog-bench-candidates"
DEPENDENCIES = ("averaged-budget-counterexample", "conditional-budget-transfer")


def compile_candidate(name: str, *flags: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(
        ["lake", "env", "lean", f"--root={SOURCES}", *flags, str(SOURCES / f"{name}.lean")],
        cwd=ROOT, env=env, check=True,
    )


def main() -> None:
    STAGING.mkdir(parents=True, exist_ok=True)
    if not STAGING.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Candidate staging must remain inside the repository")
    compile_candidate("coupling-mass")
    with tempfile.TemporaryDirectory(prefix="lean-", dir=STAGING) as tmp:
        for stem in DEPENDENCIES:
            compile_candidate(stem, "-o", str(Path(tmp) / f"{stem}.olean"))
        env = os.environ.copy()
        env["LEAN_PATH"] = os.pathsep.join(filter(None, (tmp, env.get("LEAN_PATH"))))
        compile_candidate("padded-budget-counterexample", env=env)
    print("Compiled four trusted Bench candidates; no catalogue or admission changes.")


if __name__ == "__main__":
    main()
