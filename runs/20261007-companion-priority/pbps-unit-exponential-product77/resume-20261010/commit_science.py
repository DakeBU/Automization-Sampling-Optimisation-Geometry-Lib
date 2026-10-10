"""Commit a bounded, reviewed SAU77 snapshot, preserving all unrelated edits."""
from pathlib import Path
import hashlib
import json
import subprocess

root = Path.cwd()
run = Path("runs/20261007-companion-priority/pbps-unit-exponential-product77")
assert json.loads((run / "root.source77.adoption.json").read_bytes())["publication_binding_unchanged"]
assert not subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).strip()
paths = [
    "AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean",
    "research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json",
    "research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-UnitExponentialProduct.json",
    "website/content/declaration_lessons/unit-exponential-product.json",
    "website/content/publications/unit-exponential-product.json",
    "runs/substantive_advances.jsonl",
]
paths += [p.as_posix() for p in run.rglob("*") if p.is_file() and p.suffix not in {".pyc", ".html"}]
pre = Path("runs/20261007-companion-priority/pbps-iid-product-preproof77")
paths += [p.as_posix() for p in pre.rglob("*") if p.is_file() and p.suffix not in {".pyc", ".html"} and p.stat().st_size < 500000]
paths = list(dict.fromkeys(paths))
assert all(Path(p).exists() for p in paths)
assert all(not p.startswith(("agent-briefs/", "docs/", "research-wiki/technical-lemmas/")) for p in paths)
inventory = [{"path": p, "bytes": Path(p).stat().st_size,
              "RAW_sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in paths]
(run / "resume-20261010/science-staging.json").write_text(json.dumps({
    "files": inventory,
    "excluded": "Pre-existing collaborator edits, duplicate full primary HTML copies, and >500k raw historical transcript payloads remain local; fixed source digest/anchors and selected source-review artifacts are recorded. No deletion or alteration of excluded evidence.",
    "source_review": "accepted", "exact_commit_verification": "pending",
    "aggregate": "pending", "Goal_complete": False
}, indent=2) + "\n", encoding="utf-8")
paths.append((run / "resume-20261010/science-staging.json").as_posix())
subprocess.run(["git", "-c", "core.autocrlf=false", "add", "-f", "--pathspec-from-file=-", "--pathspec-file-nul"],
               input=("\0".join(paths) + "\0").encode(), check=True)
check = subprocess.run(["git", "-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check"], capture_output=True)
(run / "resume-20261010/staged-whitespace.log").write_bytes(check.stdout + check.stderr)
print("staged", len(paths), "whitespace_exit", check.returncode)
if check.returncode:
    print("\n".join(s for s in check.stdout.decode(errors="replace").splitlines()
                    if not s.startswith(("+", " ")) )[:10000])
    raise SystemExit(check.returncode)
subprocess.run(["git", "commit", "-q", "-m", "Prove and source-review actual countable unit-exponential inputs"], check=True)
print("SCIENCE_COMMIT", subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip())
