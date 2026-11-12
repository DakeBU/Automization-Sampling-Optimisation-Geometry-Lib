"""Local plan, archive and human scoring for reviewed private Bench prose tasks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import sog_bench_prose as prose
import sog_bench_split_guard as guard


PROFILE = "private-prose-prompt-v1"
SPLIT = "private-test"
META_KEYS = {"run_id", "model", "model_version", "created_at", "track", "prompt_profile", "attempt_policy",
             "retrieval_profile", "tools", "seed", "decoding", "task_ids"}
PLAN_FIELDS = {"schema_version", "split", "run_metadata", "admission", "prompt_file_sha256", "task_bindings"}
ADMISSION_DIGESTS = {"public_history_sha256", "reservation_sha256", "family_packets_sha256"}


def sealed(obj: dict) -> bytes:
    raw = guard.canonical(obj) + b"\n"
    guard.require(len(raw) <= guard.MAX_BYTES, "private-run-file-limit")
    return raw


def file_digest(raw: bytes, expected: bytes) -> str:
    digest = guard.digest(raw)
    guard.require(expected in (digest.encode(), digest.encode() + b"\n"), "private-run-digest-mismatch")
    return digest


def admitted_tasks(repo: Path, tips: list[str], reservation: dict, packet: dict, reviews: list[bytes]) -> tuple[list[dict], dict]:
    exposed, report = guard.inventory(repo, tips)
    guard.require(guard.check_reservation(reservation, exposed)["no_known_conflict"], "private-run-reservation-rejected")
    bindings, _ = guard.private_prose_packet(reservation, packet)
    history = report["public_history_sha256"]
    review = guard.check_review_evidence(reservation, reviews, history, prose_bindings=bindings)
    guard.require(review["all_review_files_bound"], "private-run-review-rejected")
    return packet["tasks"], {"public_tips": sorted(set(tips)), "public_history_sha256": history,
                             "reservation_sha256": guard.digest(guard.canonical(reservation)),
                             "family_packets_sha256": guard.digest(guard.canonical(bindings))}


def plan_for(tasks: list[dict], admission: dict, metadata: dict) -> tuple[dict, bytes, list[dict]]:
    guard.exact_keys(admission, {"public_tips", *ADMISSION_DIGESTS}, "private-run-admission-schema")
    tips = guard.sequence(admission["public_tips"], "private-run-admission-schema", nonempty=True)
    guard.require(all(type(t) is str and guard.COMMIT.fullmatch(t) for t in tips) and tips == sorted(set(tips)),
                  "private-run-admission-schema")
    for key in ADMISSION_DIGESTS:
        guard.hash_id(admission[key])
    guard.exact_keys(metadata, META_KEYS, "private-run-metadata")
    ids = prose.validate_metadata(metadata, tasks, prompt_profile=PROFILE)
    # No JSON extensions such as NaN/Infinity in arbitrary provider decoding settings.
    json.dumps(metadata["decoding"], allow_nan=False)
    by_id = {row["id"]: row for row in tasks}
    selected = [by_id[i] for i in ids]
    guard.require(all(t["retrieval_profile"] == metadata["retrieval_profile"] and
                      t["allowed_tools"] == metadata["tools"] for t in selected), "private-run-policy-drift")
    prompts = b"".join(guard.canonical(guard.prose_prompt(t)) + b"\n" for t in selected)
    plan = {"schema_version": 1, "split": SPLIT, "run_metadata": metadata, "admission": admission,
            "prompt_file_sha256": guard.digest(prompts),
            "task_bindings": [{"id": t["id"], "sha256": guard.digest(guard.canonical(t))} for t in selected]}
    return plan, prompts, selected


def response_rows(raw: dict, selected: list[dict], plan_sha: str) -> list[dict]:
    guard.exact_keys(raw, {"schema_version", "plan_sha256", "responses"}, "private-run-responses-schema")
    guard.require(type(raw["schema_version"]) is int and raw["schema_version"] == 1 and
                  raw["plan_sha256"] == plan_sha, "private-run-responses-plan-binding")
    expected = {t["id"]: guard.prose_prompt(t)["prompt_sha256"] for t in selected}
    rows = {}
    for row in guard.sequence(raw["responses"], "private-run-responses-schema"):
        guard.exact_keys(row, {"id", "prompt_sha256", "track", "attempt", "response"}, "private-run-response-schema")
        identity = row["id"]
        guard.require(type(identity) is str and identity in expected and identity not in rows,
                      "private-run-unselected-or-duplicate-response")
        guard.require(row["prompt_sha256"] == expected[identity] and row["track"] == "natural-language" and
                      type(row["attempt"]) is int and row["attempt"] == 1 and type(row["response"]) is str,
                      "private-run-response-binding")
        rows[identity] = row
    return [rows[t["id"]] for t in selected if t["id"] in rows]


def archive_for(tasks: list[dict], admission: dict, plan_bytes: bytes, digest_bytes: bytes,
                observed_prompts: bytes, response_object: dict) -> dict:
    plan_sha = file_digest(plan_bytes, digest_bytes)
    given = guard.parse(plan_bytes)
    guard.exact_keys(given, PLAN_FIELDS, "private-run-plan-schema")
    plan, prompts, selected = plan_for(tasks, admission, given["run_metadata"])
    guard.require(sealed(plan) == plan_bytes and prompts == observed_prompts, "private-run-plan-or-prompt-drift")
    return {"schema_version": 1, "split": SPLIT, "plan": plan, "plan_sha256": plan_sha,
            "tasks": selected, "responses": response_rows(response_object, selected, plan_sha)}


def score_input(archive: dict, archive_sha: str) -> tuple[dict, dict, str]:
    guard.exact_keys(archive, {"schema_version", "split", "plan", "plan_sha256", "tasks", "responses"},
                     "private-run-archive-schema")
    guard.require(type(archive["schema_version"]) is int and archive["schema_version"] == 1 and
                  archive["split"] == SPLIT, "private-run-archive-schema")
    given = archive["plan"]
    guard.exact_keys(given, PLAN_FIELDS, "private-run-plan-schema")
    plan, _, selected = plan_for(archive["tasks"], given["admission"], given["run_metadata"])
    guard.require(sealed(plan) == sealed(given) and archive["tasks"] == selected and
                  guard.digest(sealed(plan)) == archive["plan_sha256"], "private-run-archive-plan-drift")
    responses = response_rows({"schema_version": 1, "plan_sha256": archive["plan_sha256"],
                               "responses": archive["responses"]}, selected, archive["plan_sha256"])
    guard.require(archive["responses"] == responses, "private-run-archive-response-order")
    cores = [{"id": t["id"], "family": t["family"], "track_levels": {"natural-language": t["level"]},
              "rubric": [{"criterion": c} for c in t["rubric"]], "binding_sha256": b["sha256"]}
             for t, b in zip(selected, plan["task_bindings"], strict=True)]
    manifest = {"files": {"rubric-packet.json": archive_sha}}
    packet = {"reference_cores": cores, "responses": responses, "run_metadata": plan["run_metadata"],
              "split": SPLIT, "catalog_version": PROFILE, "registered_plan_sha256": archive["plan_sha256"]}
    return manifest, packet, archive_sha


def output_directory(path: Path, repo: Path, files: dict[str, bytes]) -> None:
    guard.require(path.name not in ("", ".", "..") and ":" not in path.name, "invalid-private-output-name")
    directory = path.parent.resolve(strict=True) / path.name
    guard.require_private_path(directory, repo.resolve())
    # Reject even an empty existing directory; its contents/access are not ours.
    directory.mkdir(mode=0o700)
    for name, raw in files.items():
        guard.write_private_output(directory / name, repo, raw)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", help="Verify admission and freeze a private pre-response plan")
    archive = commands.add_parser("archive", help="Bind reported first responses to the separately pinned plan")
    score = commands.add_parser("score", help="Record human scores of the exact private archive")
    for command in (plan, archive):
        command.add_argument("--public-tip", action="append", required=True)
        command.add_argument("--review-file", action="append", type=Path, required=True)
        for name in ("reservation", "prose-packet", "output"):
            command.add_argument("--" + name, type=Path, required=True)
    plan.add_argument("--run-metadata", type=Path, required=True)
    for name in ("plan", "plan-digest", "prompts", "responses"):
        archive.add_argument("--" + name, type=Path, required=True)
    for name in ("archive", "archive-digest", "judgment", "output"):
        score.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args(argv)
    repo = guard.ROOT

    def raw(path: Path, limit: int = guard.MAX_BYTES) -> bytes:
        return guard.private_bytes(path, repo, limit)

    try:
        if args.command == "score":
            archive_bytes = raw(args.archive)
            archive_sha = file_digest(archive_bytes, raw(args.archive_digest, 65))
            report = prose.grade_snapshot(score_input(guard.parse(archive_bytes), archive_sha),
                                          guard.parse(raw(args.judgment)))
            del report["manifest_sha256"]  # The private archive itself is the sealed input.
            report["archive_sha256"] = archive_sha
            report["private_runner_sha256_lf"] = prose.bench.text_hash(Path(__file__))
            guard.write_private_output(args.output, repo, sealed(report))
        else:
            guard.require(len(args.review_file) <= guard.MAX_REVIEW_FILES, "private-review-input-limit")
            tasks, admission = admitted_tasks(repo, args.public_tip, guard.parse(raw(args.reservation)),
                                              guard.parse(raw(args.prose_packet)),
                                              [raw(path, guard.MAX_REVIEW_BYTES) for path in args.review_file])
            if args.command == "plan":
                record, prompts, _ = plan_for(tasks, admission, guard.parse(raw(args.run_metadata)))
                plan_bytes = sealed(record)
                output_directory(args.output, repo, {"plan.json": plan_bytes, "prompts.jsonl": prompts,
                                                     "plan.sha256": (guard.digest(plan_bytes) + "\n").encode()})
            else:
                record = archive_for(tasks, admission, raw(args.plan), raw(args.plan_digest, 65),
                                     raw(args.prompts), guard.parse(raw(args.responses)))
                archive_bytes = sealed(record)
                sha = guard.digest(archive_bytes)
                _, packet, _ = score_input(record, sha)
                worksheet = prose.judgment_template(packet["reference_cores"], packet["responses"], sha)
                output_directory(args.output, repo, {"archive.json": archive_bytes, "archive.sha256": (sha + "\n").encode(),
                                                     "adjudication-template.json": sealed(worksheet)})
    except guard.GuardError as exc:
        print(json.dumps({"status": "rejected", "reason": str(exc)}), file=sys.stderr)
        return 2
    except (ValueError, OSError, TypeError, KeyError, RuntimeError):
        # A parser/OS error may include private text or paths. Never echo it.
        print(json.dumps({"status": "rejected", "reason": "invalid-private-run-input-or-destination"}), file=sys.stderr)
        return 2
    print(json.dumps({"status": "written-locally", "operation": args.command,
                      "execution_verified": False, "unseen_generalization_claim": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
