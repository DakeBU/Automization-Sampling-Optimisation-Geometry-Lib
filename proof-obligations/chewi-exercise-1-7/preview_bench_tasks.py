"""Preflight the two reviewed Exercise 1.7 drafts without editing the catalog."""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from unittest.mock import patch

from check_exercise_publication_packets import PACKET_DIR, ROOT, read, require

import sog_bench as bench
import sog_bench_exercises as exercises
import sog_bench_lean as runtime
import sog_bench_reader as reader


FAMILY = "chewi-lcs-2026-08-20-exercise-1-7"
PUBLICATION = ROOT / "website/content/publications/chewi-exercise-1-7-conclusions.json"
DRAFT_PINS = {
    "compact-pi": "7b9d1fcf1bb85ece5327ac22581bfb50c3489df4260c23f734d275f255c31c63",
    "actual-kl": "4869a923acf2e9acedaa2eb095bc448641e5e7a775c94da7c36cd0d0119515a1",
}
REVIEW_PIN = "c3fcd62d35a31e95ef80b0df6f7c1bd42e176abdaf33feccc141347f0db9b7bb"


def core(label: str, item: dict, lesson: dict) -> dict:
    is_pi = label == "compact-pi"
    path = PACKET_DIR / f"{label}-bench-draft-v2.md"
    require(bench.text_hash(path) == DRAFT_PINS[label], f"{label}: reviewed text has changed")
    draft = path.read_text(encoding="utf-8")
    heading = "Natural-language prompt" if is_pi else "Prompt only"
    question = draft.split(f"## {heading}\n\n", 1)[1].split("\n\nSuggested ", 1)[0]
    grading = draft.split("## Grader only: four binary criteria", 1)[1]
    rows = [row[2:-2].split(" | ", 1) for row in grading.splitlines()
            if row.startswith("| ") and row.endswith(" |")][2:]
    require(len(rows) == 4 and all(len(row) == 2 for row in rows), "Expected four reviewed slots")
    declaration = lesson["declaration"]
    module = declaration.rsplit(".", 1)[0]
    level = "L4" if is_pi else "L3"
    context = ("set_option autoImplicit false\nnoncomputable section\nopen MeasureTheory Filter\n"
               + ("open scoped Topology ContDiff RealInnerProductSpace\n"
                  "open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities\n"
                  "open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation\n"
                  "open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy\n"
                  "open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient "
                  "(continuous_gradient_of_contDiff_one)\n"
                  "open AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation\n"
                  "open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff"
                  if is_pi else
                  "open scoped Topology Asymptotics\n"
                  "open AutoSamplingTheory.TechnicalLemmas.InformationTheory."
                  "BoundedDensityPerturbation\n"
                  "open AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw"))
    return {
        "id": f"draft-exercise-1-7-{label}",
        "family": FAMILY, "textbook_exercise_id": FAMILY,
        "domain": "sampling", "library_domains": ["log-concave-sampling"],
        "skills": ["proof", "assumption-audit", "composition"],
        "track_levels": {"natural-language": level, "lean": level},
        "difficulty_reason": ("Legitimate square-root LSI domain and two distinct dominated limits."
                              if is_pi else "Actual-law normalization, finite KL and a two-sided remainder."),
        "title": item["title"], "question": question,
        # The reviewed question already states the complete premises. Do not
        # copy the publication assumptions: some explain how to solve the task.
        "assumptions": ["Use exactly the mathematical premises in the question or fixed Lean target."],
        "declaration": declaration, "source_file": module.replace(".", "/") + ".lean",
        "context": context, "lean_explanation": lesson["lean_proof"],
        "source_note": item["source"]["anchor"], "boundary": lesson["boundary"],
        "steps": [step["title"] + ": " + step["text"] + r" \[" + step["formula"] + r"\]"
                  for step in lesson["steps"]],
        "dependencies": {"astis": lesson["astis_dependencies"], "mathlib": lesson["mathlib_dependencies"]},
        "rubric": [{"points": 1, "criterion": f"{name}: {evidence}"} for name, evidence in rows],
    }


def materialize() -> list[dict]:
    require(bench.text_hash(PACKET_DIR / "exercise-bench-rubric-review-v2.md") == REVIEW_PIN,
            "Independent review has changed")
    publication = read(PACKET_DIR / "exercise-conclusions-publication-candidate-v1.json")
    items = {item["id"]: item for item in publication["items"]}
    lessons = {unit["declaration"]: unit for unit in publication["units"]}
    pairs = [("compact-pi", "compact-poincare"), ("actual-kl", "actual-kl-expansion")]
    candidates = []
    for label, suffix in pairs:
        item = items["chewi-lcs-exercise-1-7-" + suffix]
        candidate = core(label, item, lessons[item["bindings"][0]["declaration"]])
        bench.curriculum.classify(candidate, bench.curriculum.curriculum())
        candidates.append(candidate)
    data = read(exercises.DATA)
    source = publication["items"][0]["source"]
    book = "chewi-lcs-2026-08-20"
    require(FAMILY not in {r["id"] for r in data["exercises"]},
            "This preview is superseded by a canonical exercise record")
    data["books"].setdefault(book, {
        "title": "Log-Concave Sampling", "authors": ["Sinho Chewi"],
        "edition": source["edition"], "pdf_url": source["url"].split("#", 1)[0],
        "pdf_sha256": source["pdf_sha256"], "pdf_pages": 333,
        "rights_boundary": "Only original exposition and bibliographic metadata; no PDF or source prose in exports.",
    })
    data["exercises"].append({
        "id": FAMILY, "book_id": book, "number": "1.7", "chapter": "1",
        "book_page": 43, "pdf_page": 55,
        "publication_components": [
            {"publication_file": PUBLICATION.relative_to(ROOT).as_posix(), "item_id": i} for i in items],
        "context_notes": ["Compact Euclidean PI and actual-law KL have different premises and targets."],
        "unformalized_context": ["No identification with the abstract Chapter 1 form domain, "
                                 "and no compiled transport consumer corresponding to Corollary 2.1.2."],
    })
    # Exact-path in-process projection only. The admission validator still
    # rejects these draft IDs, and no canonical source is changed on disk.
    existing = Path.read_text
    if PUBLICATION.is_file():
        require(read(PUBLICATION)["items"] == publication["items"],
                "Do not shadow a different canonical publication")
    overlay = {exercises.DATA: data, PUBLICATION: publication}

    def projected(path, *args, **kwargs):
        return json.dumps(overlay[path]) if path in overlay else existing(path, *args, **kwargs)

    with patch.object(Path, "read_text", projected):
        return bench.materialize({"split": "public-dev", "cores": candidates})


def check_agent_inputs(prompts: list[dict], packets: list[dict], cores: list[dict]) -> None:
    allowed = {"id", "family", "domain", "library_domains", "skills", "title", "split",
               "assumptions", "binding_sha256", "exercise_source", "track", "level", "question"}
    expected = {(c["id"], track) for c in cores for track in bench.TRACKS}
    require(len(prompts) == 4 and {(p["id"], p["track"]) for p in prompts} == expected,
            "Expected two distinct tasks with exactly two views each")
    source = exercises.source_prompt(cores[0]["textbook_exercise"])
    for row in prompts:
        require(set(row) == allowed and row["family"] == FAMILY and row["exercise_source"] == source,
                "The agent prompt may contain only approved fields and bibliography")
        for c in cores:
            forbidden = (c["declaration"], c["source_file"], c["lean_reference"],
                         *[r["criterion"] for r in c["rubric"]])
            require(not any(s in row["question"] for s in forbidden), "Reference material leaked into prompt")
    for packet, c in zip(packets, cores, strict=True):
        row = json.loads(packet["agent/prompt.json"])
        require(row in prompts and row["id"] == c["id"] and row["track"] == "lean",
                "The operator and public Lean prompts disagree")
        task = packet["agent/Solution.lean.txt"].decode()
        require(task.endswith(" := by\n  -- Replace this comment with your proof.\n")
                and not re.search(r"\b(sorry|admit|axiom|unsafe)\b",
                                  bench.astis_site.sanitize_lean(task)),
                "Agent-facing Lean must be an unproved fixed target, not a trusted answer")


def replay(c: dict, packet: dict, absent: set[str], scratch: Path) -> None:
    module = c["declaration"].rsplit(".", 1)[0]
    closure = set(runtime.local_imports(c["imports"]))
    require(not closure.intersection(n.rsplit(".", 1)[0] for n in absent), "Answer module in task imports")
    label = c["id"].removeprefix("draft-exercise-1-7-")
    frozen = (PACKET_DIR / f"{label}-statement-v1.lean.txt").read_text(encoding="utf-8").strip()
    name = runtime.policy()["target_name"]
    target = frozen.replace("theorem " + c["declaration"].rsplit(".", 1)[1], "theorem " + name, 1)
    oracle = packet["oracle/Solution.lean.txt"].decode()
    task = packet["agent/Solution.lean.txt"].decode()
    marker = "\n" + target + " := by\n"
    require(oracle.count(marker) == task.count(marker) == 1, f"{module}: exact frozen target changed")
    guard = "open Lean Elab Command in\nrun_cmd do\n" + "".join(
        f"  if ((← getEnv).find? `{n}).isSome then\n"
        f'    throwError "Exercise answer already available in the task imports"\n' for n in sorted(absent))
    checked = oracle.replace(marker, "\n" + guard + marker, 1) + f"\n#print axioms {name}\n"
    with tempfile.TemporaryDirectory(prefix="exercise17-oracle-", dir=scratch) as tmp:
        path = Path(tmp) / "TrustedReference.lean"
        path.write_text(checked, encoding="utf-8", newline="\n")
        result = subprocess.run(["lake", "env", "lean", str(path)], cwd=ROOT,
                                capture_output=True, encoding="utf-8", timeout=90)
        require(result.returncode == 0, result.stdout + result.stderr)
        exercises.checked_axioms(result.stdout, [name])


def main() -> None:
    scratch = ROOT / ".astis/sog-bench"
    scratch.mkdir(parents=True, exist_ok=True)
    version = subprocess.check_output(["lake", "env", "lean", "--version"], cwd=ROOT,
                                      encoding="utf-8", timeout=30)
    require(re.search(r"\bversion 4\.33\.0(?:,|\s|$)", version) is not None, "Expected Lean 4.33.0")
    cores = materialize()
    prompts = bench.prompts(cores)
    packets = [runtime.packet(c) for c in cores]
    check_agent_inputs(prompts, packets, cores)
    absent = {c["declaration"] for c in cores}
    for c, packet in zip(cores, packets, strict=True):
        replay(c, packet, absent, scratch)
        print(c["id"] + ": actual exported oracle replays with both finished answers absent from imports")
    pages = {}
    for c in cores:
        path = reader.HUB + c["id"] + ".html"
        body = reader.core_page(c, checked=False, structural=[], review_row={"editorial": "pending"})
        require("Separate mathematical results and their assumptions" in body
                and "Reference mathematical proof" in body and "Reference Lean and explanation" in body,
                "The actual Bench renderer lost a required proof or source disclosure")
        banner = '<p>Local draft preview. Not admitted; download links are not published.</p>'
        pages[path] = reader.with_styles(
            bench.astis_site.page(c["title"], path, banner + body, active="benchmarks"), path)
    dest = Path(tempfile.mkdtemp(prefix="exercise17-bench-draft-", dir=scratch))
    (dest / "DRAFT.txt").write_text(
        "Local preflight only. Not admitted, not a holdout, not a sandbox or model result.\n"
        "Send only the intended task inputs from agent/; do not share the operator directory.\n",
        encoding="utf-8", newline="\n")
    (dest / "agent").mkdir()
    (dest / "operator").mkdir()
    (dest / "agent/prompts.jsonl").write_bytes(b"".join(
        (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode() for row in prompts))
    (dest / "operator/references.json").write_bytes(bench.encoded(cores))
    for path, page in pages.items():
        target = dest / "operator/reader" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8", newline="\n")
    assets = dest / "operator/reader/assets"
    assets.mkdir()
    shutil.copyfile(reader.STYLESHEET, assets / "sog-bench.css")
    for c, packet in zip(cores, packets, strict=True):
        for name, data in packet.items():
            # Do not write the verifier-only placeholder or claim runtime export.
            if not name.startswith(("agent/", "oracle/")):
                continue
            lane, filename = name.split("/", 1)
            target = dest / ("agent" if lane == "agent" else "operator") / c["id"] / filename
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(data)
    print(f"Prepared four draft views; output: {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
