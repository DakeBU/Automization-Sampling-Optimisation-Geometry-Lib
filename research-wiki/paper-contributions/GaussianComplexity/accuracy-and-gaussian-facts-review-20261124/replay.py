"""Replay this proof package against the repository's pinned Lake environment."""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory


def main():
    package = Path(__file__).resolve().parent
    root = package.parents[3]
    manifest = json.loads((package / "review.json").read_text())
    sources = []
    imports = set()
    for record in manifest["review_modules_in_dependency_order"]:
        path = package.parent / record["file"]
        data = path.read_bytes()
        if sha256(data).hexdigest() != record["sha256"]:
            raise SystemExit(f"Source hash differs for {path}")
        sources.append(path)
        imports.update(re.findall(r"^import ([\w.]+)$", data.decode(), re.MULTILINE))

    local_modules = {path.stem for path in sources}
    subprocess.run(["lake", "build", *sorted(imports - local_modules)], cwd=root, check=True)
    lake_path = subprocess.check_output(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=root, text=True
    ).strip()
    with TemporaryDirectory() as build:
        env = {**os.environ, "LEAN_PATH": os.pathsep.join([build, lake_path])}
        for path in sources:
            print(f"Checking {path.stem}", flush=True)
            obj = Path(build) / (path.stem + ".olean")
            subprocess.run(
                ["lean", "-DwarningAsError=true", "-o", str(obj), str(path)],
                cwd=root, env=env, check=True,
            )


if __name__ == "__main__":
    main()
