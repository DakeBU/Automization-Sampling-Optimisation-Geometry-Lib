"""Replay one draft graph question and a separate private proof-occurrence trace."""
from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "website/scripts")]

import sog_bench as bench
import sog_bench_compiled_graph as compiler
import sog_bench_reader as reader
import sog_bench_review as review

SPEC = HERE / "selection.json"
SNAPSHOT = HERE / "compiled-public.json"
TRACE_SOURCE = HERE / "PrivateBalanceTrace.lean"
TRACE = HERE / "private-balance-trace.json"
PREFIX = "AutoSamplingTheory.TechnicalLemmas.Probability."
REV = PREFIX + "RandomScanHeatBath.randomScan_isReversible"
POINT = PREFIX + "RandomScanHeatBath.randomScan_apply_singleton"
BRIDGE = PREFIX + "RandomScanHeatBath.singleton_balance"
COND = PREFIX + "CoordinateHeatBath.heatBath_eq_cond"
KEEP = PREFIX + "CoordinateHeatBath.heatBath_ae_apply_eq"
INVARIANT = PREFIX + "CoordinateHeatBath.heatBath_invariant"
LAW = PREFIX + "HeatBath.heatBathSnd_apply"
MARKER = "SOG_RANDOM_SCAN_PRIVATE_V1 "


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def replay_private(snapshot: dict) -> dict:
    result = subprocess.run(["lake", "env", "lean", TRACE_SOURCE.relative_to(ROOT).as_posix()],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=120)
    require(result.returncode == 0, result.stdout + result.stderr)
    lines = [line.split(MARKER, 1)[1] for line in result.stdout.splitlines() if MARKER in line]
    require(len(lines) == 1, "Expected one structured private balance trace")
    observed = json.loads(lines[0])
    private = observed.get("private_bridge", "")
    require(observed == {"public_target": REV, "private_bridge": private, "bridge_source_name": BRIDGE,
                         "pointwise_law": POINT, "pointwise_occurs_directly_in_public_target": False}
            and private.startswith("_private.") and private.endswith("." + BRIDGE),
            "The observed private proof-term evidence does not match this candidate")
    return {"schema_version": 1, "scope": "operator-only selected proof-body occurrences; not complete closure",
            "probe_sha256_lf": bench.text_hash(TRACE_SOURCE),
            "public_snapshot_sha256": bench.sha(bench.encoded(snapshot)), "observed": observed}


def validate_question(item: dict, snapshot: dict, trace: dict) -> None:
    expected = {"nodes": sorted([POINT, KEEP]), "entails_mathematical_necessity": False}
    require(item["answer"] == expected and set(item["targets"]) == {REV, POINT, KEEP, INVARIANT},
            "Question must preserve the positive, negative and private-route cases")
    public_edges = {tuple(edge) for edge in snapshot["graph"]["edges"]}
    require({(POINT, COND), (COND, LAW), (KEEP, LAW)} <= public_edges
            and (REV, POINT) not in public_edges, "Public occurrence edges changed")
    require(REV not in expected["nodes"] and trace["observed"]["pointwise_law"] == POINT
            and trace["observed"]["private_bridge"] not in item["context"]["nodes"],
            "Do not export the private witness as a public graph node")
    prompt = bench.curriculum.graph_prompts([item])[0]
    prompt_bytes = bench.encoded(prompt)
    require("answer" not in prompt and "observed" not in prompt and "private_bridge" not in prompt
            and trace["observed"]["private_bridge"].encode() not in prompt_bytes,
            "Review-only proof path leaked into the agent question")
    for answer, score in (
        (expected, 1),
        ({"nodes": sorted([REV, POINT, KEEP]), "entails_mathematical_necessity": False}, 0),
        ({"nodes": [KEEP], "entails_mathematical_necessity": False}, 0),
        ({"nodes": expected["nodes"], "entails_mathematical_necessity": True}, 0),
    ):
        scored = bench.curriculum.grade_graph([item], [{"id": item["id"], "attempt": 1,
                    "binding_sha256": item["binding_sha256"], "answer": answer}])
        require(scored["points"] == score, "Existing structural scorer changed on a boundary case")


def export(item: dict, trace: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=False)
    (output / "agent").mkdir()
    (output / "review").mkdir()
    (output / "assets").mkdir()
    shutil.copyfile(ROOT / "website/static/sog-bench.css", output / "assets/sog-bench.css")
    prompt = bench.curriculum.graph_prompts([item])[0]
    (output / "agent/prompt.json").write_bytes(bench.encoded(prompt))
    packet = {"status": "draft; independent editorial review not yet recorded",
              "item": item, "private_witness": trace,
              "review_checks": ["Verify the actual graph edges and private witness by replay.",
                                "Check the selected positive and negative targets, graph-only scoring and L2 difficulty.",
                                "Do not infer proof necessity, full dependency independence, or an equivalent Lean task.",
                                "Check public-dev family, original material scope and absence of answer data from agent input."]}
    (output / "review/packet.json").write_bytes(bench.encoded(packet))
    context = item["context"]
    # Display aliases only: the exact question labels, IDs, edges and binding
    # remain those of the frozen compiler-backed prompt.
    labels = {**context["node_labels"],
              PREFIX + "KernelReversibility.isReversible_of_singleton_balance": "Balance ⇒ reversibility",
              KEEP: "Unselected site stays fixed",
              POINT: "Scan singleton formula"}
    display = {**context, "node_labels": labels}
    body = ('<article class="sog-reader sog-graph-draft"><h1>' + escape(item["title"]) + '</h1>'
            '<p>Local graph QA draft · not admitted · provisional L2</p>'
            + reader.prose(item["question"])
            + reader.prose("Targets: " + "; ".join(labels[n] for n in item["targets"]) + ".")
            + reader.prose("Queried interface: " + labels[item["remove"]] + ".")
            + reader.import_figure(display)
            + reader.fold("Review only: answer and why this slice omits a real use",
                reader.prose("Reachable in this slice: " + "; ".join(labels[n] for n in item["answer"]["nodes"]) + ".")
                + reader.prose("The compiled reversibility proof instead reaches the pointwise law through "
                               "its private singleton-balance theorem, which is not a vertex here. This records "
                               "proof-term occurrences, not necessity or independence."))
            + '</article>')
    html = bench.astis_site.page(item["title"], "review/preview.html", body)
    html = html.replace('</head>', '<link rel="stylesheet" href="../assets/sog-bench.css">'
                        '<style>.sog-graph-draft {max-width: 68rem;} '
                        '.sog-graph-draft .sog-graph svg {width:100%;min-width:850px;height:auto;}</style></head>')
    (output / "review/preview.html").write_text(html, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true", help="Create this candidate's two snapshots once")
    parser.add_argument("--export-review", type=Path, help="Write separated prompt and review files to a new path")
    args = parser.parse_args()
    if args.freeze:
        require(not SNAPSHOT.exists() and not TRACE.exists(), "Never overwrite a frozen draft or an audit")
    _, core, _ = compiler.inputs(SPEC)
    require(core["id"] == "sogb-021" and core["family"] == "conditional-resampling-invariance"
            and core["split"] == "public-dev"
            and review.accepted(bench.editorial_review([core])["items"][core["id"]]),
            "Use the exact, independently accepted mathematical source core")
    fresh = compiler.replay(SPEC)
    local_closure = fresh["provenance"]["local_import_closure_sha256_lf"]
    for relative in local_closure:
        require(relative.startswith("AutoSamplingTheory/TechnicalLemmas/")
                and "atlas" not in (ROOT / relative).read_text(encoding="utf-8").lower(),
                "Only eligible original local technical sources belong in this evidence")
    trace = replay_private(fresh)
    if args.freeze:
        with tempfile.TemporaryDirectory(prefix="random-scan-draft-", dir=ROOT / ".astis/sog-bench") as tmp:
            provisional = Path(tmp) / "snapshot.json"
            provisional.write_bytes(bench.encoded(fresh))
            item, = compiler.items(SPEC, provisional)
            validate_question(item, fresh, trace)
        for path, value in ((SNAPSHOT, fresh), (TRACE, trace)):
            with path.open("xb") as f:
                f.write(bench.encoded(value))
    else:
        require(fresh == json.loads(SNAPSHOT.read_bytes()), "Public proof-body slice changed")
        require(trace == json.loads(TRACE.read_bytes()), "Private balance witness changed")
        item, = compiler.items(SPEC, SNAPSHOT)
        validate_question(item, fresh, trace)
    if args.export_review:
        export(item, trace, args.export_review)
    print(f"Replayed {len(fresh['rows'])} public declarations and {len(fresh['graph']['edges'])} selected edges.")
    print("Separate private balance witness and four structural scoring cases passed; no new admission.")


if __name__ == "__main__":
    main()
