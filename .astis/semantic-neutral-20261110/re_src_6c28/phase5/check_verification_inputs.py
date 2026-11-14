"""Independently bind the current radial-exponential proof and gate evidence."""

import hashlib
import json
import re
import subprocess
import tarfile
from pathlib import Path


ROOT = Path("/Users/zhouhuanjian/ASTIS-GC")
PHASES = Path(".astis/semantic-neutral-20261110/re_src_6c28")
EVIDENCE = Path("research-wiki/paper-contributions/GaussianComplexity/radial-exponential-semantic-evidence")
RECEIPTS = Path(".astis/huanjian-resume-20261103")
HEAD = "aba7324fabec3de0889b079d7fbed86095661016"
MATH = "c0bb993e3674181e33813d4b25fe655865e5ad0b"
LESSON_COMMIT = "dfa1d8afb8c67d18b498f39b0dee04168451fe20"
BASE = "f5494dc9ba0f5c4abab0a6b2cd59f2a465e4b848"
OWNER = "huanjian_gc_20261110_std_gaussian_radial_exponential"
REVIEWER = "/root/radial_exp_fresh_source_6c28"
ADVANCE = "ASTIS-SA-20261110-StdGaussianRadialExponential"
PRODUCER = (
    "AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential"
    ".integrable_exp_norm_sq_div_three_and_integral_stdGaussian"
)
DENSITY = (
    "AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity"
    ".map_sqrt_smul_stdGaussian_eq_withDensity"
)
PRIVATE = (
    "_private.Tests.GaussianComplexityRadialExponential.0.AutoSamplingTheory.Tests"
    ".GaussianComplexityRadialExponential.actual_source_row_truncation_tail"
)
AUDIT = Path("research-wiki/semantic-roundtrip/audits/huanjian-std-gaussian-radial-exponential.json")
LESSON = Path("website/content/declaration_lessons/huanjian-std-gaussian-radial-exponential.json")
REVIEW = EVIDENCE / "independent-source-review-original.json"
BINDING_SHA = "73a244cdf93dd12673339c0345e56a4db555b6d0b11811642c66f224c15ee1fb"
REVIEW_SHA = "11da864aa276f68a551f97dad507ef8e3fc4d84ccb0e78215e9585223fa8b844"
REVIEW_PACKET_SHA = "493fe1dce4a3cdea9af2ca791c5a637036ae66f1611aa86f8fb0220809386148"
LESSON_SHA = "20629617e4dfecf97d42247e95d7c3adc967191b7ecba798bc4c15a055de68cb"
PROOF_EVENT_SHA = "91872f3e7fe76108d01049a2a6bbaf719b4e829a05952da1525265becfc58c5d"
PROOF_EVIDENCE_SHA = "e453f22aed3b63eedf4ebfd0c889de5233c8c3cc4e1f426aad8db0a52d9a1b15"
NATIVE_SHA = "8a2562f2891354f501e60551632afe94eeb869ec0e6a62f0e7df90db3f568ccd"
READER_SHA = "ca4823545566a89bab8d5d94255880472256f11612dea06de244c1bda6a5a70f"
PYTHON = "/opt/anaconda3/bin/python"

MODULES = {
    "AutoSamplingTheory/TechnicalLemmas/Measure/RadonNikodym.lean":
        "12146654d4036bf8601a48786572d11fe46b69a4d84ab5a61c1aa25cc0848317",
    "AutoSamplingTheory/TechnicalLemmas/Measure/IsotropicGaussianDensity.lean":
        "08eaba5759c1f514e80c58123f6a7c4c9f1ffc18c4d20df3a93b6e718fae25d7",
    "AutoSamplingTheory/TechnicalLemmas/Probability/StdGaussianRadialExponential.lean":
        "c44b2840eb91a3abf29434bdf2baa9859b503f7a30c24c10ed3296e7f41c88e4",
    "Tests/GaussianComplexityRadialExponential.lean":
        "d80698f914312d2953bb1ac1a8f0a92d43a752389f0e14f6abcfa01563345443",
}
ROOT_GATES = (
    ("20261110T231439082946Z-radial-exp-reviewed-publication-at-aba", "astis_publication.py",
     ["--base", BASE], "Publication PASS"),
    ("20261110T231439082940Z-radial-exp-reviewed-contributor-at-aba", "astis_contributor_contract.py",
     ["--base", BASE], "ASTIS contributor contract PASS"),
    ("20261110T231439082940Z-radial-exp-reviewed-semantic-at-aba", "astis_semantic_roundtrip.py",
     [], "semantic round-trip registry valid"),
    ("20261110T231439082968Z-radial-exp-reviewed-frontier-at-aba", "astis_frontier_cells.py",
     [], "ASTIS Frontier Cell protocol check passed"),
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def pinned(path, digest):
    raw = Path(path).read_bytes()
    require(sha(raw) == digest, f"SHA-256 mismatch for {path}")
    return raw


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True).stdout


def git_blob(commit, path):
    return git("show", f"{commit}:{path}")


def check_current(path, digest=None):
    raw = Path(path).read_bytes() if digest is None else pinned(path, digest)
    require(raw == git_blob(HEAD, path), f"Working bytes differ from checked HEAD for {path}")
    return raw


def check_receipt(path, expected_head, expected_sha=None):
    raw = Path(path).read_bytes() if expected_sha is None else pinned(path, expected_sha)
    receipt = json.loads(raw)
    require(receipt["cwd"] == str(ROOT) and receipt["exit_code"] == 0, f"Receipt failed for {path}")
    require(receipt["head_before"] == receipt["head_after"] == expected_head, f"Wrong receipt HEAD for {path}")
    log = pinned(receipt["log"], receipt["log_sha256"])
    return {
        "receipt": str(path), "sha256": sha(raw), "log_sha256": sha(log),
        "command": receipt["command"], "head": expected_head, "exit_code": 0,
    }, log


def check_native(module_bytes, lesson_bytes):
    native_path = EVIDENCE / "independent-native-original-verdict.json"
    reader_path = EVIDENCE / "independent-reader-corrected-verdict.json"
    native_bytes = check_current(native_path, NATIVE_SHA)
    reader_bytes = check_current(reader_path, READER_SHA)
    native = json.loads(native_bytes)
    reader = json.loads(reader_bytes)
    require(native["commit"] == MATH and native["native_verdict"] == "PASS", "Native proof verdict mismatch")
    require("version 4.33.0" in native["native_lean"] and native["dependency_heads_match"] == 9,
            "Native version or dependency scope mismatch")
    require(native["sealed_literal_kernel_def_eq"]["P"] is True and native["sealed_literal_kernel_def_eq"]["T"] is True
            and native["raw_ExprStructEq"] == {"P": False, "T": False}, "Kernel comparison mismatch")
    require(set(native["transitive_axioms"]) == {"Quot.sound", "Classical.choice", "propext"},
            "Unexpected transitive axiom")
    require(native["first_public_ASTIS_parents"] == {"P": [DENSITY], "T": [PRODUCER]}
            and native["T_direct_proof_value_uses_P"] is True, "Compiler-backed dependency edge mismatch")
    require(reader["commit"] == LESSON_COMMIT and reader["lesson_sha256"] == LESSON_SHA
            and reader["original_verdict_sha256"] == NATIVE_SHA
            and reader["bounded_render"] == "PASS" and reader["reader_controls"] == "HOLD",
            "Reader render result or HOLD boundary mismatch")
    observed = reader["observed"]
    require(observed["adjacent_byte_exact_Lean_step_folds"] == 4
            and observed["complete_private_T_module_in_step_4"] is True
            and observed["adjacent_copy_download_or_context_controls_per_step"] == [0] * 4
            and observed["private_citation_page_has_copy_download_or_context_controls"] is False
            and reader["browser_acceptance"].startswith("Not performed"), "Reader scope mismatch")

    native_manifest_path = EVIDENCE / "independent-native-original-manifest.json"
    reader_manifest_path = EVIDENCE / "independent-reader-corrected-manifest.json"
    native_manifest = json.loads(check_current(
        native_manifest_path, "942b29301d06f9e62e03aec07e0b62500ddbd56e569509b36161b20a46da0dde"))
    reader_manifest = json.loads(check_current(
        reader_manifest_path, "7ef22bfbd947115961cf409941c85b0e526c9fae598ca6c64b150c975d69a2a4"))
    archive_path = EVIDENCE / "independent-native-and-static-reader.original-files.tar.gz"
    archive_digest = "9c6fa9e6220de03bde18c04ec4294ab78c7b95afe370f69b4fe4367c09c5cdab"
    check_current(archive_path, archive_digest)
    with tarfile.open(archive_path, "r:gz") as archive:
        def member(name):
            with archive.extractfile(name) as handle:
                return handle.read()

        for entry in native_manifest["files"] + reader_manifest["files"]:
            raw = member(entry["path"])
            require(sha(raw) == entry["sha256"] and len(raw) == entry["bytes"],
                    f"Native archive manifest mismatch for {entry['path']}")
        require(member("verdict-original.json") == native_bytes
                and member("verdict-corrected.json") == reader_bytes
                and member("corrected-lesson.exact.json") == lesson_bytes,
                "Archived verdict or corrected lesson mismatch")
        for path, raw in module_bytes.items():
            require(member(f"snapshot/{path}") == raw, f"Native source bytes differ for {path}")
        environment = json.loads(member("environment.json"))
        require(environment["commit"] == MATH and environment["toolchain"] == "leanprover/lean4:v4.33.0"
                and len(environment["packages"]) == 9
                and all(item["head"] == item["pinned"] for item in environment["packages"]),
                "Archived environment pin mismatch")
        for path, digest in (
            ("lean-toolchain", "302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b"),
            ("lake-manifest.json", "b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37"),
        ):
            require(member(f"snapshot/{path}") == check_current(path, digest), f"Native pin mismatch for {path}")
        compilation = json.loads(member("native-compilation.json"))
        require([item["path"] for item in compilation] == list(MODULES), "Native compilation scope mismatch")
        for item in compilation:
            log = member(item["log"]).decode("utf-8")
            require(log.rstrip().endswith("exit_code=0") and item["path"] in log,
                    f"Missing zero-exit actual compile log for {item['path']}")
        probe = member("probe-attempt-2.log").decode("utf-8")
        require("exit_code=0" in probe and all(probe.count(line) == 2 for line in (
            "kernel_def_eq=true", "raw_ExprStructEq=false", "proof_value=present",
            "closed_type_value_and_seal=true", "missing=[]",
            "axioms=[Quot.sound, Classical.choice, propext]",
        )) and PRODUCER in probe and PRIVATE in probe and DENSITY in probe, "Actual native proof probe mismatch")
        rendered = json.loads(member("reader-corrected.json"))
        require(rendered["rendered"] is True and rendered["rendered_exact_adjacent_step_folds"] == 4
                and rendered["corrected_lesson_sha256"] == LESSON_SHA
                and rendered["step_4_has_its_own_copy_or_download"] is False, "Actual bounded renderer mismatch")
    return {
        "native_verdict": {"path": str(native_path), "sha256": NATIVE_SHA, "report": native},
        "reader_verdict": {"path": str(reader_path), "sha256": READER_SHA, "report": reader},
        "archive": {"path": str(archive_path), "sha256": archive_digest,
                    "verified_manifest_entries": len(native_manifest["files"]) + len(reader_manifest["files"])},
    }


def check_inputs():
    require(Path.cwd() == ROOT, "Wrong explicit workspace")
    require(git("rev-parse", "HEAD").decode().strip() == HEAD, "Immutable HEAD mismatch")
    module_bytes = {}
    for path, digest in MODULES.items():
        raw = check_current(path, digest)
        require(raw == git_blob(MATH, path), f"Math commit bytes differ for {path}")
        require(re.search(rb"\b(?:sorry|sorryAx|admit|axiom|unsafe)\b", raw) is None,
                f"Placeholder or unauthorized declaration token in {path}")
        module_bytes[path] = raw
    lesson_bytes = check_current(LESSON, LESSON_SHA)
    require(lesson_bytes == git_blob(LESSON_COMMIT, LESSON), "Corrected lesson bytes differ from lesson commit")
    review_bytes = check_current(REVIEW, REVIEW_SHA)
    require(review_bytes == (PHASES / "phase4/independent-source-review-original.json").read_bytes(),
            "Attached original review differs from reviewer's raw original")
    review = json.loads(review_bytes)
    overlay_bytes = check_current(EVIDENCE / "independent-source-review-overlay.exact.json",
                                  "7fa7db8eb6a9bc2642cc7375919511e09907725f553638859ddbd54dd175c9d3")
    require(overlay_bytes == (PHASES / "phase4/source-review-overlay.json").read_bytes(), "Attached overlay changed")
    overlay = json.loads(overlay_bytes)
    audit_bytes = check_current(AUDIT)
    audit = json.loads(audit_bytes)
    require({key: audit[key] for key in overlay} == overlay and audit["state"] == "source-reviewed"
            and audit["publication_binding_sha256"] == BINDING_SHA
            and audit["source_review"]["state"] == "accepted"
            and audit["source_review"]["reviewer"] == REVIEWER
            and audit["source_review"]["review_run_sha256"] == REVIEW_SHA
            and audit["source_review"]["reviewer_packet_sha256"] == REVIEW_PACKET_SHA
            and audit["source_review"]["evidence"] == str(REVIEW)
            and review["verdict"] == "equivalent-after-elaboration", "Accepted source audit mismatch")
    source_audit = {
        "id": audit["id"], "path": str(AUDIT), "sha256": sha(audit_bytes), "verdict": audit["verdict"],
        "source_review": audit["source_review"], "publication_binding_sha256": BINDING_SHA,
    }

    gates = {}
    for basename, tool, args, log_text in ROOT_GATES:
        item, log = check_receipt(RECEIPTS / (basename + ".receipt.json"), HEAD)
        require(item["command"] == [PYTHON, "-B", "tools/" + tool, "check", *args]
                and log_text.encode() in log, f"Gate receipt/log mismatch for {tool}")
        gates[tool.removesuffix(".py")] = item
    local_path = EVIDENCE / "local-proof-gate-success.actual.receipt.json"
    local_gate, local_log = check_receipt(local_path, MATH)
    require(local_log == (EVIDENCE / "local-proof-gate-success.actual.log").read_bytes()
            and json.loads(local_log)["append_sha256"] == PROOF_EVENT_SHA, "Local proof gate log mismatch")
    gates["original_local_proof"] = local_gate
    proof_event_path = EVIDENCE / "actual-PROVED_LOCAL-append.exact.jsonl"
    proof_evidence_path = EVIDENCE / "actual-PROVED_LOCAL-evidence.full.json"
    proof_event_raw = check_current(proof_event_path, PROOF_EVENT_SHA)
    proof_event = json.loads(proof_event_raw)
    proof_evidence = json.loads(check_current(proof_evidence_path, PROOF_EVIDENCE_SHA))
    require(proof_event["evidence"] == proof_evidence
            and proof_event["event"] == "transition" and proof_event["advance_id"] == ADVANCE
            and proof_event["from_state"] == "EXPLORING" and proof_event["to_state"] == "PROVED_LOCAL"
            and proof_event["worker_id"] == OWNER and proof_evidence["mathematical_candidate"] == MATH
            and proof_evidence["publication_declarations"] == [PRODUCER]
            and proof_evidence["lean_declarations"] == [PRODUCER]
            and proof_evidence["publication_binding_sha256"] == BINDING_SHA, "Original local proof event mismatch")
    for index, entry in enumerate(proof_evidence["focused_checks"]):
        item, log = check_receipt(entry["path"], BASE, entry["sha256"])
        require(item["log_sha256"] == entry["log_sha256"], "Original focused log digest mismatch")
        if index == 0:
            require(item["command"] == ["lake", "build", "Tests.GaussianComplexityRadialExponential"],
                    "Original focused build command mismatch")
        else:
            require(b"ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED 3" in log
                    and log.count(b"ACTUAL_SEALED_LITERAL_KERNEL_TYPE_APPLICATION_PASS") == 2,
                    "Original actual kernel probe log mismatch")
        gates[f"original_focused_check_{index + 1}"] = item
    native_evidence = check_native(module_bytes, lesson_bytes)
    return {
        "verified_commit": MATH,
        "checked_metadata_commit": HEAD,
        "checked_corrected_lesson_commit": LESSON_COMMIT,
        "verifier_id": REVIEWER,
        "publication_declarations": [PRODUCER],
        "source_audit": source_audit,
        "gate": gates,
        "fake_closure_scan": {
            "lexical_scan": {"modules": MODULES, "placeholder_or_unauthorized_tokens": 0},
            "native_proof_values": "Both actual declarations have closed proof values and no missing constants.",
            "allowed_transitive_axioms": ["Quot.sound", "Classical.choice", "propext"],
            "native_verdict_sha256": NATIVE_SHA,
        },
        "independent_native_and_reader": native_evidence,
        "original_proved_local": {
            "append_path": str(proof_event_path), "append_sha256": PROOF_EVENT_SHA,
            "full_evidence_path": str(proof_evidence_path), "full_evidence_sha256": PROOF_EVIDENCE_SHA,
            "event": proof_event, "evidence": proof_evidence,
        },
        "truth_boundary": (
            "Independent local verification of the exact finite-dimensional standard Gaussian quadratic moment "
            "and the actual private strict single-row cutoff application. The public moment includes dimension zero. "
            "The arbitrary-threshold chain, simultaneous row event, shifted bias, matrix concentration, and full "
            "Lemma 4.4 are beyond the verified declarations. The corrected static render passed. Proof-step and "
            "private-source reader controls and desktop/mobile browser acceptance remain HOLD. "
            "Public integration and purification remain separate."
        ),
    }
