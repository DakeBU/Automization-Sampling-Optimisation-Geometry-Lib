#!/usr/bin/env python3
"""Prepared only. A future separate root authorization is mandatory.
No source verdict or PROVED_LOCAL->VERIFIED transition is created here.
"""
from pathlib import Path
import argparse, copy, datetime, gzip, hashlib, json, os, re, subprocess, sys

ROOT = Path("/Users/zhouhuanjian/ASTIS-GC")
BASE = ROOT / "research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-normalizer-semantic-evidence"
OWN = ROOT / ".astis/huanjian-fixed-spectrum-normalizer-20261108/fresh-source-640251"
PREP = BASE / "fresh-source-reader-640251/post-integration-normalpark-preparation"
PUB_EXEC = BASE / "fresh-source-reader-640251/post-integration-normalpark-execution"
PRIV_EXEC = OWN / "post-integration-normalpark-execution"
ACTOR = "/root/norm_fresh_source_640251"
READER = "/root/norm_integration_reader"
ADVANCE = "ASTIS-SA-20261108-GaussianComplexityFixedSpectrumNormalizer"
TARGET = "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumNormalizer.actual_normalizing_integral"
ORIGINAL_V_SHA = "630b6125401c93aec5588645373ab70a61ea2a098ca1f345a351b422d47c477c"
API_SHA = "6281ff332258ebc3603f5169baece7774882b1d931dfa108b97ca7ae75202c19"
AUDIT_SHA = "8fa833c84e0a39e2afef0a7c4236e8d624a1cab94ecfbaa6b47a820f4f2ca7d1"
BINDING_SHA = "b2f41e36a9d705ff68da71f72f0ec14f1cd2ff105bcf0ae5000ef1406a5d1f41"
SOURCE_INPUTS = {
    "AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumNormalizer.lean": "2a61f494afc9b6496527094edccefa39be9cd71a72b599e5fcd2ca5bc26cf4cf",
    "Tests/GaussianComplexityFixedSpectrumNormalizer.lean": "71040132321ec908370494d289571e7366b87658de6dd531829162dfc95c90d1",
    "website/content/declaration_lessons/huanjian-fixed-spectrum-normalizer.json": "c38b809c1f71d652037443e4c47a1d448d15c3983a27aa1133d5aec4c85055f5",
    "website/content/publications/huanjian-fixed-spectrum-normalizer.json": "68da4cb0de5380fea1796abfc6e193a35779009983dd3d9b10e03f1ca05bf0b0",
}
ORIGINAL_FIELDS = ("verifier_id", "verified_commit", "gate", "source_audit",
                   "fake_closure_scan", "lean_declarations", "publication_declarations")

class GuardError(RuntimeError):
    pass

def need(ok, message):
    if not ok:
        raise GuardError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()

def read_json(path):
    return json.loads(path.read_bytes())

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def public_artifact(descriptor):
    need(isinstance(descriptor, dict), "Artifact descriptor must be an object")
    name, expected = descriptor.get("path"), descriptor.get("sha256")
    need(isinstance(name, str) and re.fullmatch(r"[0-9a-f]{64}", str(expected)), "Exact public path/SHA256 required")
    path = (ROOT / name).resolve()
    need(path.is_relative_to(ROOT), "Artifact escapes repository")
    relative = path.relative_to(ROOT)
    need(relative.parts[0] in {"research-wiki", "runs"} and ".astis" not in relative.parts,
         "Other actors' private artifacts are forbidden; use a lossless public export")
    raw = path.read_bytes()
    need(sha(raw) == expected, "Artifact SHA mismatch: " + name)
    return raw

def artifact_json(descriptor):
    return json.loads(public_artifact(descriptor))

def bound(payload, auth):
    need(payload.get("checked_core_commit") == auth["checked_core_commit"], "Evidence core commit mismatch")
    need(payload.get("source_digest_sha256") == auth["source_digest_sha256"], "Evidence sourceDigest mismatch")

def states_from(raw):
    sys.path.insert(0, str(ROOT))
    from tools import astis_advance
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    return rows, astis_advance._replay_advances(rows)

def source_guards(core):
    need(sha((ROOT / "tools/astis_advance.py").read_bytes()) == API_SHA, "Normal API changed; new review required")
    for name, expected in SOURCE_INPUTS.items():
        raw = (ROOT / name).read_bytes()
        need(sha(raw) == expected, "Mathematical packet changed: " + name)
        committed = subprocess.check_output(["git", "show", core + ":" + name], cwd=ROOT)
        need(committed == raw, "Mathematical input is not exact immutable core: " + name)
    audit = ROOT / "research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-normalizer.json"
    need(sha(audit.read_bytes()) == AUDIT_SHA, "Accepted source audit changed")
    need(read_json(audit)["publication_binding_sha256"] == BINDING_SHA, "Source publication binding changed")

def inspect_authorized(args):
    need(args.actor == ACTOR, "Only the original independent source-verifier actor may execute")
    auth_desc = {"path": args.authorization, "sha256": args.authorization_sha256}
    auth = artifact_json(auth_desc)
    need(auth.get("kind") == "ASTIS-normalpark-STABILIZING-to-VERIFIED-v1", "A NEW normalpark authorization is required")
    need(auth.get("authorization_state") == "authorized", "Template/observational metadata is not authorization")
    need(auth.get("authorized_by") == "/root" and auth.get("authorized_actor") == ACTOR, "Wrong authorization roles")
    need(auth.get("advance_id") == ADVANCE, "Wrong advance")
    need(auth.get("authorized_operation") == "STABILIZING_TO_VERIFIED_NORMALPARK_ONLY", "Wrong operation")
    need(auth.get("original_source_V_append_sha256") == ORIGINAL_V_SHA, "Original source V not bound")
    need(auth.get("helper_sha256") == sha(Path(__file__).read_bytes()), "Helper not exactly authorized")
    need(auth.get("source_publication_binding_sha256") == BINDING_SHA, "Wrong source binding")
    issued = datetime.datetime.fromisoformat(auth["authorized_utc"].replace("Z", "+00:00"))
    prepared = datetime.datetime.fromisoformat(read_json(PREP / "observed-preparation-baseline.json")["observed_utc"])
    need(issued > prepared, "Authorization predates this preparation; a new separate root authorization is mandatory")
    need(set(auth.get("allowed_output_roots", [])) ==
         {PUB_EXEC.relative_to(ROOT).as_posix(), PRIV_EXEC.relative_to(ROOT).as_posix()},
         "Future owned execution output roots not explicitly authorized")
    need(re.fullmatch(r"[0-9a-f]{40}", str(auth.get("checked_core_commit"))), "Full immutable core required")
    need(re.fullmatch(r"[0-9a-f]{64}", str(auth.get("source_digest_sha256"))), "Full sourceDigest required, no prefix")
    need(auth["source_digest_sha256"].startswith("92a908"), "Reported unchanged sourceDigest prefix differs")
    need(git("rev-parse", "HEAD") == auth["checked_core_commit"], "HEAD is not separately authorized future core")
    tracked_dirty = set(git("diff", "--name-only", auth["checked_core_commit"], "--").splitlines())
    need(tracked_dirty <= {"runs/substantive_advances.jsonl"},
         "Tracked worktree differs from immutable layout/core beyond the guarded advance ledger")
    need(not (PRIV_EXEC / "API-attempted.json").exists(), "Already attempted: never retry the API")
    source_guards(auth["checked_core_commit"])

    ledger = (ROOT / "runs/substantive_advances.jsonl").read_bytes()
    need(sha(ledger) == auth.get("ledger_before_sha256"), "Ledger guard mismatch")
    rows, states = states_from(ledger)
    own = states[ADVANCE]
    need(own["state"] == "STABILIZING", "Own state is not STABILIZING")
    need([k for k, v in states.items() if v["state"] == "STABILIZING"] == [ADVANCE], "STAB is not uniquely own")
    need(own["owner_id"] == "huanjian_gc_20261108_fixed_spectrum_normalizer", "Original proof owner changed")
    need(own["latest_evidence"].get("integration_owner") == auth.get("expected_integration_owner"),
         "Current sole integration owner not exactly authorized")
    need(own["owner_id"] != ACTOR and own["publication_declarations"] == [TARGET], "Actor/target drift")
    original = [line for line in ledger.splitlines(keepends=True) if line.strip()
                and json.loads(line).get("advance_id") == ADVANCE
                and json.loads(line).get("from_state") == "PROVED_LOCAL"
                and json.loads(line).get("to_state") == "VERIFIED"]
    need(len(original) == 1 and sha(original[0]) == ORIGINAL_V_SHA, "Original source V must be unique and byte exact")
    need(not any(r.get("advance_id") == ADVANCE and r.get("from_state") == "STABILIZING"
                 and r.get("to_state") == "VERIFIED" for r in rows), "A normalpark already completed: never repeat")
    source_v = json.loads(original[0])
    need(source_v["worker_id"] == ACTOR, "Original source verifier differs")
    need(source_v["evidence"]["verifier_id"] == ACTOR, "Original evidence verifier differs")
    need(source_v["evidence"]["verified_commit"] == "813268bc2683a82269364caffbc0c7490a884204",
         "Original verified mathematical commit differs")

    reader = artifact_json(auth["independent_reader_receipt"])
    eligibility = artifact_json(auth["eligibility_receipt"])
    images = artifact_json(auth["actual_46_image_review"])
    checks = artifact_json(auth["nine_actual_checks"])
    for payload in [reader, eligibility, images, checks]:
        bound(payload, auth)
    need(reader.get("reviewer") == READER and READER not in {ACTOR, "/root", own["owner_id"]}, "Reader is not independent")
    need(reader.get("decision") == "accepted" and reader.get("blocking") == [], "Independent reader has not accepted")
    need(eligibility.get("eligible_for_normalpark") is True and eligibility.get("blocking") == [], "Not eligible")
    need(reader.get("eligibility_receipt_sha256") == auth["eligibility_receipt"]["sha256"], "Reader/eligibility not joined")
    need(reader.get("actual_image_review_sha256") == auth["actual_46_image_review"]["sha256"], "Reader/image review not joined")
    need(reader.get("nine_actual_checks_sha256") == auth["nine_actual_checks"]["sha256"], "Reader/checks not joined")
    need(images.get("reviewer") == READER and images.get("decision") == "accepted" and images.get("blocking") == [],
         "46-image actual independent review not accepted")
    image_rows = images.get("images", [])
    need(len(image_rows) == 46 and len({r["id"] for r in image_rows}) == 46, "Need exactly 46 actual image reviews")
    for image in image_rows:
        need(image.get("actual_reviewed") is True and image.get("decision") == "accepted"
             and isinstance(image.get("notes"), str) and image["notes"].strip(), "Image is not actually reviewed/accepted")
        raw = public_artifact(image["image"])
        if image["image"].get("compression") == "gzip":
            raw = gzip.decompress(raw)
        need(raw.startswith(b"\x89PNG\r\n\x1a\n") or raw.startswith(b"\xff\xd8"), "Not an original image payload")
        need(sha(raw) == image.get("raw_image_sha256"), "Original image raw hash mismatch")

    check_rows = checks.get("checks", [])
    required_ids = auth.get("required_check_ids", [])
    need(len(check_rows) == len(required_ids) == 9 and len(set(required_ids)) == 9, "Nine exact checks required")
    need({r["id"] for r in check_rows} == set(required_ids), "Wrong nine-check identity set")
    for row in check_rows:
        receipt = artifact_json(row["receipt"])
        command = receipt.get("actual_command", receipt.get("command"))
        need(isinstance(command, list) and len(command) > 0, "Actual command missing")
        need(receipt.get("exit_code", receipt.get("returncode")) == 0, "Actual check did not pass")
        need(receipt.get("started_utc", receipt.get("start_utc")), "Actual check start time missing")
        need(receipt.get("completed_utc", receipt.get("end_utc")) or
             isinstance(receipt.get("elapsed_seconds", receipt.get("duration_seconds")), (int, float)),
             "Actual completion/duration missing")
        receipt_core = receipt.get("checked_core_commit", receipt.get("core_commit", receipt.get("head_after")))
        need(receipt_core == auth["checked_core_commit"], "Check not on future exact immutable core")
        if "head_before" in receipt:
            need(receipt["head_before"] == auth["checked_core_commit"], "Check crossed core commits")
        raw_log = public_artifact(row["log"])
        if row["log"].get("compression") == "gzip":
            raw_log = gzip.decompress(raw_log)
        need(sha(raw_log) == receipt.get("log_raw_sha256", receipt.get("log_sha256")), "Actual raw log/receipt hash mismatch")

    frontiers = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes())
                 for p in sorted((ROOT / "research-wiki/frontier-cells").rglob("*.json"))}
    need(len(frontiers) == 443, "Expected all 443 raw frontier JSONs")
    own_frontier = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-normalizer.json"
    need(own_frontier in frontiers, "Own frontier missing")
    foreign = {k: sha(canonical(v)) for k, v in states.items() if k != ADVANCE}
    need(len(foreign) == 283 and len(frontiers) - 1 == 442, "Foreign preservation counts differ")
    source_v_baseline_raw = (BASE / "fresh-source-reader-640251/verification-transition/preflight-baseline.json").read_bytes()
    need(sha(source_v_baseline_raw) == "e03b337aafd250c2f28b10a375caff5a9363a426203fd8a1df6517d87f4bca99",
         "Original source-V preservation baseline changed")
    source_v_baseline = json.loads(source_v_baseline_raw)
    need(foreign == source_v_baseline["foreign_state_hashes"], "A foreign advance changed since original source V")
    need(all(frontiers.get(p) == h for p, h in source_v_baseline["foreign_frontier_hashes"].items()),
         "A foreign frontier changed since original source V")
    need(sha((ROOT / "runs/substantive_discoveries.jsonl").read_bytes()) == source_v_baseline["discovery_ledger_sha256"],
         "Discovery ledger changed since original source V")
    tracked = git("ls-files").splitlines()
    protected = {"README.md", "AGENTS.md", "lean-toolchain", "lake-manifest.json"}
    protected.update(p for p in tracked if ".astis" not in Path(p).parts
                     and re.search(r"(^|[/_.-])models?([/_.-]|$)", p, re.I))
    protected = {p: sha((ROOT / p).read_bytes()) for p in sorted(protected) if (ROOT / p).is_file()}
    frozen = {}
    for prefix in [BASE / "fresh-source-reader-640251", OWN]:
        for folder in ["phase1", "phase2", "phase3", "verification-transition", "post-integration-normalpark-preparation"]:
            for path in sorted((prefix / folder).rglob("*")):
                if path.is_file():
                    frozen[path.relative_to(ROOT).as_posix()] = sha(path.read_bytes())
    evidence = copy.deepcopy(source_v["evidence"])
    evidence["post_integration_normalpark"] = {
        "operation": "mechanical STABILIZING->VERIFIED lane release; not a new source verdict",
        "checked_immutable_core": auth["checked_core_commit"],
        "source_digest_sha256": auth["source_digest_sha256"],
        "original_source_V_append_sha256": ORIGINAL_V_SHA,
        "original_source_verifier": ACTOR, "independent_reader": READER,
        "authorization": auth_desc,
        "independent_reader_receipt": auth["independent_reader_receipt"],
        "eligibility_receipt": auth["eligibility_receipt"],
        "actual_46_image_review": auth["actual_46_image_review"],
        "nine_actual_checks": auth["nine_actual_checks"],
        "actual_image_count": 46, "actual_check_count": 9,
        "no_new_source_verdict": True, "no_root_impersonation_authorized": True,
    }
    for key in ORIGINAL_FIELDS:
        need(evidence[key] == source_v["evidence"][key], "Original V field altered: " + key)
    context = {
        "actor": ACTOR, "advance_id": ADVANCE, "authorized_utc": auth["authorized_utc"],
        "core_commit": auth["checked_core_commit"], "ledger_before_sha256": sha(ledger),
        "own_before": own, "foreign_state_hashes": foreign, "all_raw_frontier_hashes": frontiers,
        "foreign_frontier_count": 442,
        "discovery_sha256": sha((ROOT / "runs/substantive_discoveries.jsonl").read_bytes()),
        "protected_README_model_config_hashes": protected, "frozen_file_hashes": frozen,
        "authorization": auth_desc, "evidence": evidence, "created_utc": utc(),
    }
    return auth, context, ledger

def write_owned(out, name, raw):
    need(out.is_relative_to(PUB_EXEC) or out.is_relative_to(PRIV_EXEC), "Output is outside authorized owned runtime")
    out.mkdir(parents=True, exist_ok=True)
    path = out / name
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())

def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()

def runtime_guard(context):
    need(git("rev-parse", "HEAD") == context["core_commit"], "Core changed before API")
    need(sha((ROOT / "runs/substantive_advances.jsonl").read_bytes()) == context["ledger_before_sha256"], "Ledger changed before API")
    for key in ["all_raw_frontier_hashes", "protected_README_model_config_hashes", "frozen_file_hashes"]:
        need(all(sha((ROOT / p).read_bytes()) == h for p, h in context[key].items()), "Preservation guard changed: " + key)
    need(sha((ROOT / "runs/substantive_discoveries.jsonl").read_bytes()) == context["discovery_sha256"], "Discovery changed")
    source_guards(context["core_commit"])

def api_child(context_path, expected_sha):
    path = Path(context_path).resolve()
    need(path.is_relative_to(PRIV_EXEC), "Internal context is not own private runtime")
    raw = path.read_bytes()
    need(sha(raw) == expected_sha, "Internal context hash mismatch")
    context = json.loads(raw)
    need(context["actor"] == ACTOR, "Internal actor differs")
    auth = artifact_json(context["authorization"])
    need(auth.get("kind") == "ASTIS-normalpark-STABILIZING-to-VERIFIED-v1"
         and auth.get("authorized_by") == "/root" and auth.get("authorized_actor") == ACTOR,
         "Separate future authorization missing in child")
    need(auth["helper_sha256"] == sha(Path(__file__).read_bytes()), "Child helper differs")
    fresh_args = argparse.Namespace(authorization=context["authorization"]["path"],
                                   authorization_sha256=context["authorization"]["sha256"], actor=ACTOR)
    _, freshly_checked, _ = inspect_authorized(fresh_args)
    for key, value in context.items():
        if key != "created_utc":
            need(freshly_checked[key] == value, "Authorized preflight/context differs immediately before API: " + key)
    runtime_guard(context)
    need(not (PRIV_EXEC / "API-attempted.json").exists(), "Already attempted; no API retry")
    marker = json_bytes({"actor": ACTOR, "attempted_utc": utc(), "context_sha256": expected_sha, "call_count": 1})
    for out in [PRIV_EXEC, PUB_EXEC]:
        write_owned(out, "API-attempted.json", marker)
    sys.path.insert(0, str(ROOT))
    from tools import astis_advance
    print("NORMALPARK_API_BEGIN " + utc(), flush=True)
    astis_advance.transition_advance(ADVANCE, "VERIFIED", worker_id=ACTOR,
        modes=context["own_before"].get("modes", []), evidence=context["evidence"])
    success = json_bytes({"normal_API_returned_success": True, "completed_utc": utc(),
                          "actor": ACTOR, "context_sha256": expected_sha, "call_count": 1})
    for out in [PRIV_EXEC, PUB_EXEC]:
        write_owned(out, "API-success.json", success)
    print("NORMALPARK_API_RETURNED_SUCCESS " + utc(), flush=True)

def package(out_key):
    outs = [PUB_EXEC / out_key, PRIV_EXEC / out_key]
    context = read_json(outs[1] / "runtime-context.json")
    receipt = read_json(outs[1] / "actual-API.receipt.json")
    need(receipt["returncode"] == 0 and (PRIV_EXEC / "API-success.json").is_file(), "No completed successful API receipt; never re-call")
    before = gzip.decompress((outs[1] / "before-ledger.lossless.jsonl.gz").read_bytes())
    after = (ROOT / "runs/substantive_advances.jsonl").read_bytes()
    need(after.startswith(before), "Old ledger prefix changed")
    append = after[len(before):]
    need(len(append.splitlines()) == 1, "Expected exactly one normalpark append")
    event = json.loads(append)
    need(event["advance_id"] == ADVANCE and event["from_state"] == "STABILIZING"
         and event["to_state"] == "VERIFIED" and event["worker_id"] == ACTOR, "Wrong normal transition event")
    for key in ORIGINAL_FIELDS:
        need(event["evidence"][key] == context["evidence"][key], "Original V field not retained: " + key)
    _, states = states_from(after)
    need(states[ADVANCE]["state"] == "VERIFIED" and states[ADVANCE]["owner_id"] == context["own_before"]["owner_id"],
         "State/proof owner mismatch")
    need({k: sha(canonical(v)) for k, v in states.items() if k != ADVANCE} == context["foreign_state_hashes"], "Foreign state changed")
    need(not any(v["state"] == "STABILIZING" for v in states.values()), "STAB not empty after release")
    for key in ["all_raw_frontier_hashes", "protected_README_model_config_hashes", "frozen_file_hashes"]:
        need(all(sha((ROOT / p).read_bytes()) == h for p, h in context[key].items()), "Post-API preservation mismatch: " + key)
    need(sha((ROOT / "runs/substantive_discoveries.jsonl").read_bytes()) == context["discovery_sha256"], "Discovery changed")
    summary = {"status": "NORMALPARK_COMPLETED_ONCE", "actor": ACTOR, "source_verdict_repeated": False,
        "core_commit": context["core_commit"], "normal_API_calls": 1, "original_source_V_sha256": ORIGINAL_V_SHA,
        "ledger_before_sha256": sha(before), "ledger_after_sha256": sha(after), "append_sha256": sha(append),
        "foreign_states_preserved": 283, "raw_frontiers_preserved": 443, "foreign_frontiers_preserved": 442,
        "README_models_discovery_frozen_files_preserved": True, "own_frontier_not_edited": True,
        "root_may_project_own_frontier_only_after_this_receipt": True, "STAB": [], "API_returncode": 0}
    for out in outs:
        for name, raw in {"after-ledger.lossless.jsonl.gz": gzip.compress(after, mtime=0),
                          "normalpark-append.exact.jsonl": append,
                          "transition-summary.json": json_bytes(summary)}.items():
            if not (out / name).exists():
                write_owned(out, name, raw)
            else:
                need((out / name).read_bytes() == raw, "Packaging file differs; preserve and diagnose, never repeat API")
        files = sorted(p for p in out.rglob("*") if p.is_file() and p.name != "preservation-manifest.json")
        manifest = {"status": "FROZEN", "summary": summary,
            "files": [{"path": p.relative_to(out).as_posix(), "bytes": p.stat().st_size,
                       "sha256": sha(p.read_bytes())} for p in files]}
        raw = json_bytes(manifest)
        if not (out / "preservation-manifest.json").exists():
            write_owned(out, "preservation-manifest.json", raw)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--authorization")
    parser.add_argument("--authorization-sha256")
    parser.add_argument("--actor")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--package-only", metavar="AUTH_HASH_PREFIX")
    parser.add_argument("--internal-api-child", nargs=2, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.internal_api_child:
        api_child(*args.internal_api_child)
        return
    if args.package_only:
        need(args.actor == ACTOR, "Packaging must retain the actual independent actor")
        need(re.fullmatch(r"[0-9a-f]{16}", args.package_only) is not None, "Invalid recovery key")
        package(args.package_only)
        return
    need(args.authorization and args.authorization_sha256, "A separate future normalpark authorization path+raw SHA is mandatory")
    auth, context, before = inspect_authorized(args)
    if not args.execute:
        print(json.dumps({"status": "AUTHORIZED_PREFLIGHT_ONLY_NO_API", "actor": ACTOR,
                          "checked_core_commit": auth["checked_core_commit"], "API_calls": 0}, indent=2))
        return
    key = args.authorization_sha256[:16]
    outs = [PUB_EXEC / key, PRIV_EXEC / key]
    runtime = json_bytes(context)
    for out in outs:
        write_owned(out, "runtime-context.json", runtime)
        write_owned(out, "before-ledger.lossless.jsonl.gz", gzip.compress(before, mtime=0))
    command = [sys.executable, str(Path(__file__).resolve()), "--internal-api-child",
               str(outs[1] / "runtime-context.json"), sha(runtime)]
    started = utc()
    completed = subprocess.run(command, cwd=ROOT, capture_output=True)
    log = completed.stdout + b"\n[STDERR]\n" + completed.stderr
    receipt = {"actual_command": command, "started_utc": started, "completed_utc": utc(),
               "returncode": completed.returncode, "exit_code": completed.returncode,
               "raw_log_sha256": sha(log), "actual_subprocess_completed": True, "actor": ACTOR}
    for out in outs:
        write_owned(out, "actual-API.log", log)
        write_owned(out, "actual-API.receipt.json", json_bytes(receipt))
    need(completed.returncode == 0, "API attempt returned nonzero. Do not retry; inspect ledger/success marker and preserve exact failure")
    package(key)

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(type(error).__name__ + ": " + str(error), file=sys.stderr)
        raise
