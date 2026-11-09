"""Replay the scoped Exercise 1.7 publication evidence without registering it."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


PACKET_DIR = Path(__file__).resolve().parent
ROOT = PACKET_DIR.parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "website/scripts")]

import astis_publication as publication
import astis_semantic_roundtrip as roundtrip
import declaration_lessons as reader


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_superseded_cutoff(evidence: Path) -> None:
    for label, was_blocked in (("superseded-extension", True),
                               ("superseded-extension-v2", True),
                               ("superseded-cutoff-limits", False)):
        prior_packet = read(evidence / f"{label}.reviewer_packet.json")
        prior_review = read(evidence / f"{label}.review_result.json")
        prior_packet_hash = prior_packet.pop("packet_sha256")
        prior_review_hash = prior_review.pop("review_run_sha256")
        require(roundtrip.sha256_json(prior_packet) == prior_packet_hash
                and roundtrip.sha256_json(prior_review) == prior_review_hash
                and prior_review["reviewer_packet_sha256"] == prior_packet_hash
                and any(row["blocking"] for row in prior_review["deltas"]) == was_blocked,
                f"{label}: the preserved older review is missing or changed")


def check_bundle(batch: str, data: dict) -> None:
    if batch == "cutoff":
        evidence = PACKET_DIR / "cutoff-publication-evidence-v1"
        check_superseded_cutoff(evidence)
        candidates = [read(PACKET_DIR / "cutoff-publication-candidate-v3.json"),
                      read(evidence / "gaussian-successor-publication.json")]
        expected = 3
    else:
        evidence = PACKET_DIR / "exercise-conclusions-publication-evidence-v1"
        candidates = [read(PACKET_DIR / "exercise-conclusions-publication-candidate-v1.json")]
        expected = 2
    items = [item for candidate in candidates for item in candidate["items"]]
    units = [unit for candidate in candidates for unit in candidate["units"]]
    bindings = {b["audit_id"]: (i, b) for i in items for b in i["bindings"]}
    audits = []
    for path in sorted(evidence.glob("*.audit.json")):
        fragment = read(path)
        audit = roundtrip._artifact_backed_audit(fragment, path)
        ident = audit["id"]
        require(audit["state"] == "source-reviewed" and audit["verdict"] in
                {"exact", "equivalent-after-elaboration"}
                and not any(row["severity"] == "blocking" for row in audit["deltas"]),
                f"{ident}: no acceptance for this bounded candidate")
        for field, hash_field in (("decoder_result", "decoder_run_sha256"),
                                  ("review_result", "review_run_sha256")):
            result = read(ROOT / fragment[field])
            pin = result.pop(hash_field)
            require(roundtrip.sha256_json(result) == pin, f"{ident}: invalid {field} pin")
        require(read(ROOT / fragment["decoder_packet"]) == roundtrip.decoder_packet(audit),
                f"{ident}: decoder packet changed")
        require(read(ROOT / fragment["reviewer_packet"]) == roundtrip.semantic_reviewer_packet(audit),
                f"{ident}: reviewer packet changed")
        audits.append(audit)
    require(len(audits) == len(units) == expected
            and {a["id"] for a in audits} == set(bindings),
            f"{batch}: expected {expected} distinct candidate bindings and their exact reviews")
    registry = {"schema_version": 1, "protocol": roundtrip.load_registry()["protocol"],
                "audits": audits}
    errors = roundtrip.validate_registry(registry)
    require(not errors, "\n".join(errors))

    data = {**data, "lessons": {**data["lessons"], **{u["declaration"]: u for u in units}},
            "audits": {**data["audits"], **{a["id"]: a for a in audits}}}
    for audit in audits:
        item, binding = bindings[audit["id"]]
        require(audit["publication_binding_sha256"] == publication.binding_digest(item, binding, data),
                f"{audit['id']}: code, source, or lesson has drifted")
        require(audit["publication_context"] == publication.review_context(item, binding, data),
                f"{audit['id']}: independent reviewer context is stale")
    for unit in units:
        html = reader.render_unit(unit, reader.lesson_path(unit["declaration"]))
        require("reader-progressive" in html and "Corresponding Lean step" in html
                and html.count("proof-reader-equation") >= 3,
                f"{unit['declaration']}: progressive lesson fragment is incomplete")
    print(f"{batch}: {expected} exact source reviews and lesson fragments validated.")


def replay_trusted_references() -> None:
    """Compile exact, previously reviewed proof bodies, not model submissions."""
    scratch = ROOT / ".astis" / "sog-bench"
    scratch.mkdir(parents=True, exist_ok=True)
    version = subprocess.check_output(["lake", "env", "lean", "--version"], cwd=ROOT,
                                      encoding="utf-8")
    require(re.search(r"\bversion 4\.33\.0(?:,|\s|$)", version) is not None,
            f"Expected Lean 4.33.0, got {version.strip()}")
    for name, seal in [
        ("AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare.variance_le_of_compact_logSobolev",
         "compact-pi-statement-v1.lean.txt"),
        ("AutoSamplingTheory.TechnicalLemmas.InformationTheory.AffinePerturbationKL.klDiv_affine_perturbation_second_order",
         "actual-kl-statement-v1.lean.txt"),
    ]:
        module, original = name.rsplit(".", 1)
        source = (ROOT / (module.replace(".", "/") + ".lean")).read_text(encoding="utf-8")
        frozen = (PACKET_DIR / seal).read_text(encoding="utf-8").strip()
        marker = f"theorem {original}\n"
        require(source.count(marker) == 1 and frozen + " := by" in source,
                f"{name}: the trusted statement changed")
        doc_at = source.rfind("/--", 0, source.index(marker))
        require(doc_at >= 0, f"{name}: missing declaration docstring")
        guard = (f"open Lean Elab Command in\nrun_cmd do\n"
                 f"  if ((← getEnv).find? `{name}).isSome then\n"
                 f"    throwError \"Answer is already in the trusted task imports\"\n\n")
        reference = "exercise_bench_trusted_reference"
        ref_marker = f"theorem {reference}\n"
        body = source[:doc_at] + guard + source[doc_at:].replace(marker, ref_marker, 1)
        require(frozen.replace(marker, ref_marker, 1) + " := by" in body,
                f"{name}: replay does not match the frozen mathematical target")
        with tempfile.TemporaryDirectory(prefix="exercise-bench-reference-", dir=scratch) as directory:
            path = Path(directory) / "TrustedReference.lean"
            path.write_text(body + f"\n#print axioms {module}.{reference}\n", encoding="utf-8", newline="\n")
            run = subprocess.run(["lake", "env", "lean", str(path)], cwd=ROOT,
                                 capture_output=True, encoding="utf-8")
            require(run.returncode == 0, run.stdout + run.stderr)
            axiom_report = re.search(r"depends on axioms:\s*\[([^\]]*)\]", run.stdout)
            require(axiom_report is not None, f"{name}: missing transitive axiom report")
            axioms = {a.strip() for a in axiom_report[1].split(",") if a.strip()}
            require(axioms <= {"propext", "Classical.choice", "Quot.sound"},
                    f"{name}: unexpected axiom set {sorted(axioms)}")
        print(f"{original}: trusted reference built with the finished answer absent from imports")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", choices=("cutoff", "conclusions", "all"), default="all")
    parser.add_argument("--replay-trusted-references", action="store_true",
                        help="Also compile the exact reviewed PI/KL references with answer imports excluded")
    args = parser.parse_args()
    if args.replay_trusted_references and args.batch == "cutoff":
        parser.error("trusted reference replay requires the conclusions packet check")
    data = publication.inputs()
    for batch in ("cutoff", "conclusions") if args.batch == "all" else (args.batch,):
        check_bundle(batch, data)
    if args.replay_trusted_references:
        replay_trusted_references()
    print("No Cell or publication status changed.")


if __name__ == "__main__":
    main()
