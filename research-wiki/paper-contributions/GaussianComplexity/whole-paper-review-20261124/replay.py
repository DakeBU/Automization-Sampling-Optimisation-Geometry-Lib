"""Compile the complete Gaussian sampling review and audit its printed axioms."""

from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory


def read_verified(path, digest):
    data = path.read_bytes()
    if sha256(data).hexdigest() != digest:
        raise SystemExit(f"Source hash differs for {path}")
    return data.decode()


def main():
    package = Path(__file__).resolve().parent
    root = package.parents[3]
    manifest = json.loads((package / "review.json").read_text())
    pin = manifest["toolchain"]
    lake = json.loads(read_verified(root / "lake-manifest.json", pin["lake_manifest_sha256"]))
    mathlib = next(p for p in lake["packages"] if p["name"] == "mathlib")
    if (root / "lean-toolchain").read_text().strip() != pin["lean_toolchain"] or mathlib["rev"] != pin["mathlib_revision"]:
        raise SystemExit("The Lean or Mathlib pin differs from the review")
    for record in manifest["production_sources"]:
        read_verified(root / record["file"], record["sha256"])

    sources = {}
    imports = {}
    for record in manifest["review_modules_in_dependency_order"]:
        path = package.parent / record["file"]
        data = read_verified(path, record["sha256"])
        sources[path.stem] = path
        imports[path.stem] = set(re.findall(r"^import ([\w.]+)$", data, re.MULTILINE))
    external = set.union(*imports.values()).difference(sources)
    subprocess.run(["lake", "build", *sorted(external)], cwd=root, check=True)
    lake_path = subprocess.check_output(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=root, text=True
    ).strip()

    allowed = set(manifest["verification"]["main_axioms"])
    expected = {"AutoSamplingTheory.ExampleCases.GaussianComplexity." + name for name in manifest["declarations"]}
    with TemporaryDirectory() as build:
        env = {**os.environ, "LEAN_PATH": os.pathsep.join([build, lake_path])}

        def compile_module(name):
            obj = Path(build) / (name + ".olean")
            result = subprocess.run(
                ["lean", "-DwarningAsError=true", "-o", str(obj), str(sources[name])],
                capture_output=True, text=True, cwd=root, env=env,
            )
            output = result.stdout + result.stderr
            if result.returncode:
                raise SystemExit(f"{name} failed\n{output}")
            audited = set()
            for decl, axioms in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output):
                unexpected = {s.strip() for s in axioms.split(",") if s.strip()} - allowed
                if unexpected:
                    raise SystemExit(f"{decl} uses additional axioms: {sorted(unexpected)}")
                audited.add(decl)
            audited.update(re.findall(r"'([^']+)' does not depend on any axioms", output))
            if name == "GCWholePaper" and audited != expected:
                raise SystemExit(f"Aggregate axiom report differs: {sorted(audited ^ expected)}")
            return name

        # Review modules reuse only dependencies compiled in this temporary directory.
        pending = {name: deps.intersection(sources) for name, deps in imports.items()}
        complete = set()
        active = {}
        worker_count = min(3, os.cpu_count() or 1)
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            while pending or active:
                ready = [name for name, deps in pending.items() if deps <= complete]
                for name in ready[:worker_count - len(active)]:
                    active[executor.submit(compile_module, name)] = name
                    del pending[name]
                if not active:
                    raise SystemExit(f"Unresolved imports: {sorted(pending)}")
                finished, _ = wait(active, return_when=FIRST_COMPLETED)
                for future in finished:
                    complete.add(future.result())
                    print(f"[{len(complete)}/{len(sources)}] {active.pop(future)}", flush=True)
    print(f"Verified {len(sources)} review modules and the axiom reports for {len(expected)} declarations.")


if __name__ == "__main__":
    main()
