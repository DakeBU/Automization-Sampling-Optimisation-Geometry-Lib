"""Run only the sealed sogb-035 candidate fixtures; not an admission or submission API."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sog_bench_lean as runtime

BENCH = Path("benchmarks/samplingoptimisationgeometrybench")
REVIEW = BENCH / "reviews/candidate-sogb-035/reviewer-input.json"
REVIEW_SHA256 = "0ae63b7eac7280e317200a586025e02c528a7e0e58e200903d68cbe6efcb8410"
ID = "sogb-035"
NS = "SamplingOptimisationGeometryBench"
POSITIVE = f"{NS}.BinaryPrefixLikelihood.binary_stopped_work_transfer"
NEGATIVE = f"{NS}.PaddedCounterexample.binary_padded_averaged_budget_counterexample"
SOURCES = ("averaged-budget-counterexample.lean", "conditional-budget-transfer.lean",
           "padded-budget-counterexample.lean")
OPENS = """open MeasureTheory Set Filter ProbabilityTheory
open scoped BigOperators ENNReal Topology
"""
BINARY_DEFS = ("abbrev Path", "def readPrefix", "abbrev historyFiltration",
               "def cylinder", "def mass", "def Realizes", "def Supports", "def ratio",
               "def likelihood", "def chiSquare", "def conditionalBudget", "def budgetProcess")
AXIOM_GUARD = re.compile(
    r"(?m)^/--\ninfo: '[^\n]+' depends on axioms: \[propext, Classical.choice, Quot.sound\]\n-/\n"
    r"#guard_msgs \(whitespace := lax\) in\n#print axioms [\w.]+\n")
EXPECTED = {
    "reference": ("accepted", None),
    "positive-only": ("proof-rejected", "Challenge and solution theorem statement do not match"),
    "weakened-negative": ("proof-rejected", "Const does not match between challenge and target 'SogBenchCandidate.Negative'"),
    "proof-hole": ("proof-rejected", "Illegal axiom detected: 'sorryAx'"),
}


def load_sources(root: Path) -> tuple[str, str, str]:
    raw = (root / REVIEW).read_bytes()
    if runtime.bench.sha(raw) != REVIEW_SHA256:
        raise ValueError("Sealed candidate mathematical review drift")
    record = json.loads(raw)
    paths = [BENCH / "candidates" / name for name in SOURCES]
    # The full catalog may legitimately change; compare the exact reviewed item.
    core, = (item for item in json.loads((root / BENCH / "cores.json").read_bytes())["cores"]
             if item["id"] == ID)
    if (core.get("lean_enabled") is not False or
            any(core.get(key) != value for key, value in record["original_source"].items())):
        raise ValueError("Expected the reviewed, still-unpaired prose question")
    loaded = []
    for path in (*paths, Path("lean-toolchain"), Path("lake-manifest.json")):
        source = (root / path).read_text(encoding="utf-8")
        if runtime.bench.sha(source.encode()) != record["files_sha256_lf"][path.as_posix()]:
            raise ValueError(f"Sealed source/toolchain drift: {path}")
        loaded.append(source)
    return loaded[0], loaded[1], loaded[2]


def block(source: str, key: str) -> str:
    # These delimiters are for exact hash-checked source, not a general Lean parser.
    # Select the first command with the exact prefix (never a theorem name substring).
    match = re.search(r"(?m)^" + re.escape(key) + r"(?=[ (:\n])", source)
    if match is None:
        raise ValueError(f"Missing reviewed model command: {key}")
    return source[match.start():].split("\n\n", 1)[0]


def body(source: str, guards: int) -> str:
    source = source[source.index("/-!\n"):]
    clean, count = AXIOM_GUARD.subn("", source)
    if count != guards:
        raise ValueError("Unexpected trusted candidate axiom audit blocks")
    return clean.strip() + "\n\n"


def proposition(source: str, owner: str, alias: str) -> str:
    key = "theorem " + owner.rsplit(".", 1)[1] + " "
    params, separator, conclusion = source.split("\n" + key, 1)[1].partition(" :\n")
    # partition splits exactly at the binder/conclusion boundary. Inside the
    # statement let-bound terms use ':='; only the final ':= by' is the proof.
    if not separator or " := by\n" not in conclusion:
        raise ValueError("Cannot locate reviewed theorem signature")
    return (f"set_option linter.unusedVariables false in\ndef {alias} : Prop :=\n"
            f"  ∀ {params},\n{conclusion.split(' := by', 1)[0]}\n\n")


def namespace(name: str, contents: str) -> str:
    return f"namespace {name}\n{contents.rstrip()}\nend {name}\n\n"


def sources(root: Path) -> dict[str, str]:
    finite, conditional, padded = load_sources(root)
    policy = runtime.policy()
    target_name = policy["target_name"]
    reference_imports = list(dict.fromkeys(re.findall(
        r"(?m)^import Mathlib\.[\w.]+$", conditional + "\n" + finite)))
    solver_imports = (
        "Mathlib.Probability.Process.Stopping", "Mathlib.Probability.Moments.Variance",
        "Mathlib.MeasureTheory.Measure.Real", "Mathlib.Data.Fin.Tuple.Basic",
    )
    model = namespace(f"{NS}.ConditionalBudgetTransfer", block(conditional, "def historyFiltration"))
    # The binary abbreviation has the same short name; search after its namespace.
    binary = conditional.split(f"\nnamespace {NS}.BinaryPrefixLikelihood\n", 1)[1]
    model += namespace(f"{NS}.BinaryPrefixLikelihood", "\n\n".join(block(binary, k) for k in BINARY_DEFS))
    model += namespace(f"{NS}.AveragedBudget", block(finite, "def bitMass"))
    model += namespace(f"{NS}.PaddedCounterexample", "open BinaryPrefixLikelihood AveragedBudget\n\n"
                       + block(padded, "def paddedTable") + "\n\n" + block(padded, "def terminalCharge"))
    before = "".join(f"import {name}\n" for name in solver_imports) + "\n" + OPENS
    before += "\nnoncomputable section\n\n" + model
    props_start = (OPENS + f"\nopen {NS}.BinaryPrefixLikelihood {NS}.PaddedCounterexample\n\n"
                   + proposition(conditional, POSITIVE, "Positive"))
    negative = proposition(padded, NEGATIVE, "Negative")
    props_end = "def ProposedTarget : Prop := Positive ∧ Negative\n\n"
    baseline = before + namespace("SogBenchCandidate", props_start + negative + props_end)
    full = "\n".join(reference_imports) + "\n\n" + body(finite, 1) + body(conditional, 9) + body(padded, 3)
    seal = f"""open Lean Elab Command in
run_cmd
  for name in ["{POSITIVE}", "{NEGATIVE}"] do
    if (← getEnv).contains name.toName then
      throwError "Exact answer declaration unexpectedly visible: {{name}}"

"""
    target = f"theorem {target_name} : SogBenchCandidate."
    fixed = target + "ProposedTarget :=\n"
    reference = full + namespace("SogBenchCandidate", props_start + negative + props_end)
    axiom_check = (f"\n/--\ninfo: '{target_name}' depends on axioms: "
                   "[propext, Classical.choice, Quot.sound]\n-/\n"
                   f"#guard_msgs (whitespace := lax) in\n#print axioms {target_name}\n")
    result = {
        "model": baseline + seal + "#check SogBenchCandidate.ProposedTarget\n\nend\n",
        "starter": baseline + target + "ProposedTarget := by\n  -- Supply both proofs.\n\nend\n",
        "challenge": baseline + seal + fixed + "  by sorry\n\nend\n",
        "reference": reference + fixed + f"  ⟨@{POSITIVE}, {NEGATIVE}⟩\n" + axiom_check,
        "positive-only": reference + target + f"Positive := @{POSITIVE}\n",
        "weakened-negative": full + namespace("SogBenchCandidate", props_start +
                              "def Negative : Prop := True\n\n" + props_end)
                              + fixed + f"  ⟨@{POSITIVE}, True.intro⟩\n",
        "proof-hole": reference + fixed + f"  ⟨@{POSITIVE}, by sorry⟩\n",
    }
    if any(len(result[key].encode()) > policy["limits"]["submission_bytes"] for key in EXPECTED):
        raise ValueError("Controlled candidate fixture exceeds current submission limit")
    return result


def freeze(output: Path) -> dict:
    generated = sources(runtime.ROOT)
    policy = runtime.policy()
    stage = output / "stage"
    output.mkdir(parents=True)
    (stage / "project").mkdir(parents=True)
    (stage / "owned-build").mkdir()
    files = {
        "Model.lean": generated["model"].encode(),
        "Solver.lean.txt": generated["starter"].encode(),
        "stage/Challenge.lean": generated["challenge"].encode(),
        "stage/config.json": runtime.bench.encoded({
            "challenge_module": "Challenge", "solution_module": "Solution",
            "theorem_names": [policy["target_name"]], "definition_names": [],
            "permitted_axioms": policy["permitted_axioms"], "enable_nanoda": False,
        }),
        "stage/project/lakefile.lean": runtime.offline_lakefile().encode(),
        "stage/project/lake-manifest.json": runtime.bench.encoded(runtime.offline_manifest()),
        "stage/project/lean-toolchain": (runtime.ROOT / "lean-toolchain").read_text().encode(),
        **{name: (runtime.ROOT / name).read_bytes() for name in ("LICENSE", "NOTICE", "LICENSE_SCOPE.md")},
        **{f"fixtures/{name}.lean.txt": generated[name].encode() for name in EXPECTED},
    }
    for name, data in files.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    record = {
        "schema_version": 1, "id": ID, "kind": "fixed-candidate-software-fixtures",
        "admitted": False, "model_measurement": False, "reference_in_stage": False,
        "review_input_sha256": REVIEW_SHA256,
        "policy_sha256": runtime.bench.sha(runtime.bench.encoded(policy)),
        "generator_sha256_lf": runtime.bench.text_hash(Path(__file__)),
        "files": {name: runtime.bench.sha(data) for name, data in files.items()},
    }
    (output / "packet.json").write_bytes(runtime.bench.encoded(record))
    return record


def check_local(output: Path, *, build_imports: bool = False) -> None:
    """Elaborate only owned generated inputs, in separate Lean environments."""
    freeze(output)
    output = output.resolve()
    modules = (("Challenge", "stage/Challenge.lean"), ("Solution", "fixtures/reference.lean.txt"))
    if build_imports:
        # Direct lean does not materialize Lake's dependency traces. Finish
        # trusted imports (including ProofWidgets) before the readonly snapshot.
        imports = sorted({module for _, source in modules for module in re.findall(
            r"(?m)^import (Mathlib\.[\w.]+)$", (output / source).read_text(encoding="utf-8"))})
        if not imports:
            raise ValueError("Missing trusted Mathlib imports")
        subprocess.run(["lake", "build", *imports], cwd=runtime.ROOT, check=True)
    env = dict(os.environ)
    # Supply the two fresh oleans in addition to Lake's package search path.
    paths = subprocess.check_output(["lake", "env", sys.executable, "-c",
                                    "import os; print(os.environ['LEAN_PATH'])"],
                                   cwd=runtime.ROOT, text=True)
    env["LEAN_PATH"] = os.pathsep.join((str(output), paths.strip()))
    for name, source in modules:
        subprocess.run(["lake", "env", "lean", "-o", str(output / f"{name}.olean"),
                        str(output / source)], cwd=runtime.ROOT, check=True)
    # Use Lean's environment API, not printing/reparsing types. The two modules
    # declare the same names and therefore must not be loaded into one environment.
    lean = subprocess.check_output(["lake", "env", "lean", "--print-prefix"],
                                   cwd=runtime.ROOT, text=True).strip()
    argv = [str(Path(lean) / "bin" / ("lean.exe" if sys.platform == "win32" else "lean")),
            "--run", str(runtime.ROOT / "tools/bench/CheckStoppedWorkCandidate.lean")]
    subprocess.run(argv, cwd=runtime.ROOT, env=env, check=True)


def verify(prepared: Path, output: Path) -> bool:
    # No path accepting a caller-controlled challenge, stage or submission:
    # build all input files afresh here and invoke only the fixed controls.
    runtime.check_runtime(prepared)
    record = freeze(output)
    binding = runtime.bench.sha(runtime.bench.encoded(record))
    results = []
    for name, (expected, reason) in EXPECTED.items():
        for path, digest in record["files"].items():
            if runtime.bench.sha((output / path).read_bytes()) != digest:
                raise ValueError(f"Generated candidate input changed: {path}")
        run = output / "runs" / name
        report = runtime._run_bound_submission(
            identity=ID, binding_sha256=binding, packet_sha256=binding,
            stage_dir=output / "stage", submission=output / "fixtures" / (name + ".lean.txt"),
            runtime=prepared, output=run)
        diagnostic = run / "compiler-diagnostic.bin"
        matches = (reason is None or (diagnostic.is_file() and reason in
                   diagnostic.read_bytes().decode("utf-8", errors="replace")))
        row = {"fixture": name, "expected": expected, "actual": report["kind"],
               "expected_reason_seen": matches, "wall_seconds": report.get("wall_seconds"),
               "receipt_sha256": runtime.bench.sha((run / "result.json").read_bytes())}
        results.append(row)
        print(json.dumps(row), flush=True)
    passed = all(row["expected"] == row["actual"] and row["expected_reason_seen"] for row in results)
    (output / "summary.json").write_bytes(runtime.bench.encoded({
        "schema_version": 1, "id": ID, "kind": record["kind"], "admitted": False,
        "model_measurement": False, "packet_sha256": binding, "results": results, "passed": passed,
    }))
    return passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("freeze", "check-local", "verify"):
        command = sub.add_parser(name)
        command.add_argument("--output", required=True, type=Path)
        if name == "check-local":
            command.add_argument("--build-imports", action="store_true",
                                 help="Materialize trusted Lake dependency traces before native snapshot")
        if name == "verify":
            command.add_argument("--runtime", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "freeze":
        print(json.dumps(freeze(args.output), sort_keys=True))
        return 0
    if args.command == "check-local":
        check_local(args.output, build_imports=args.build_imports)
        return 0
    return 0 if verify(args.runtime, args.output) else 1


if __name__ == "__main__":
    raise SystemExit(main())
