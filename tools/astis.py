#!/usr/bin/env python3
"""ASTIS local workflow helper.

This is the stable command surface for Auto-Sampling-Theory-In-Sleep.  It is
adapted from the plain-file workflow used by the Quantum block-encoding
automation project, but the domain is SDE/Sampling proof formalization.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import astis_harness as harness


ROOT = Path(__file__).resolve().parents[1]
LEAN_TOOLCHAIN_FILE = ROOT / "lean-toolchain"
STATE_DIR = ROOT / ".astis"
STATE_FILE = STATE_DIR / "state.json"
TRIAL_LOG = ROOT / "runs" / "trials.jsonl"
TRIAL_SUMMARY = ROOT / "runs" / "trials_summary.csv"
MANIFEST = ROOT / "MANIFEST.md"
EFFICIENCY_DIR = ROOT / "runs" / "efficiency"
CONTEXT_PACK_DIR = ROOT / "runs" / "context-packs"
PROOF_BLUEPRINT_DIR = ROOT / "proof-blueprints"
LEGACY_BLUEPRINT_DIR = ROOT / "research-wiki" / "blueprints"
BLUEPRINT_DIR = PROOF_BLUEPRINT_DIR
VERIFIER_FEEDBACK_DIR = ROOT / "verifier-feedback"
AGENT_BRIEFS_DIR = ROOT / "agent-briefs"
RETRIEVAL_INDEX_DIR = ROOT / "research-wiki" / "retrieval-index"
TECHNICAL_LEMMAS_DIR = ROOT / "research-wiki" / "technical-lemmas"
LEGACY_TECHNICAL_LEMMA_MEMORY_DIR = ROOT / "research-wiki" / "technical-lemma-memory"
TECHNICAL_LEMMA_MEMORY_DIR = LEGACY_TECHNICAL_LEMMA_MEMORY_DIR
LEMMA_DAG_DIR = ROOT / "research-wiki" / "lemma-dags"
SAMPLING_LIBRARY_DIR = ROOT / "research-wiki" / "sampling-sde-library"
LOG_CONCAVE_OVERVIEW_MD = SAMPLING_LIBRARY_DIR / "log_concave_sampling_overview.md"
LOG_CONCAVE_FOUNDATION_DAG_MD = LEMMA_DAG_DIR / "log_concave_sampling_foundation.md"
LOG_CONCAVE_EXECUTION_PACK_MD = AGENT_BRIEFS_DIR / "log_concave_sampling_6h_execution_pack.md"
LOG_CONCAVE_FOUNDATION_MMD = ROOT / "docs" / "assets" / "log_concave_sampling_foundation.mmd"
LOG_CONCAVE_FOUNDATION_SVG = ROOT / "docs" / "assets" / "log_concave_sampling_foundation.svg"
LOG_CONCAVE_FOUNDATION_PNG = ROOT / "docs" / "assets" / "log_concave_sampling_foundation.png"
LOG_CONCAVE_STATUS_MMD = ROOT / "docs" / "assets" / "log_concave_sampling_status.mmd"
LOG_CONCAVE_STATUS_SVG = ROOT / "docs" / "assets" / "log_concave_sampling_status.svg"
LOG_CONCAVE_STATUS_PNG = ROOT / "docs" / "assets" / "log_concave_sampling_status.png"
EXTERNAL_LEAN_LIBRARY_DIR = ROOT / "research-wiki" / "external-lean-libraries"
PAPER_CONTRIBUTION_DIR = ROOT / "research-wiki" / "paper-contributions"
SALD_CONTRIBUTION_DIR = PAPER_CONTRIBUTION_DIR / "SALD"
PAPER_MEMORY_DIR = ROOT / "research-wiki" / "paper-memory"
LEGACY_SALD_PAPER_MEMORY_DIR = PAPER_MEMORY_DIR / "ASTIS-SALD-001"
SALD_PAPER_MEMORY_DIR = SALD_CONTRIBUTION_DIR
SALD_UNFINISHED_SOURCE_MAP = SALD_PAPER_MEMORY_DIR / "unfinished_source_map.md"
SALD_UNFINISHED_SOURCE_JSONL = SALD_PAPER_MEMORY_DIR / "unfinished_source_map.jsonl"
LEGACY_SALD_UNFINISHED_SOURCE_MAP = LEGACY_SALD_PAPER_MEMORY_DIR / "unfinished_source_map.md"
LEGACY_SALD_UNFINISHED_SOURCE_JSONL = LEGACY_SALD_PAPER_MEMORY_DIR / "unfinished_source_map.jsonl"
PROJECT_ARTICLE_UPDATE_DIR = ROOT / "paper-notes" / "project-paper" / "cycle-updates"
PRO_PROMPT_DIR = ROOT / "runs" / "pro-prompts"
SALD_CYCLE_SUMMARY_DIR = ROOT / "paper-notes" / "SALD" / "markdown" / "cycle-summaries"

OUTER_REPOS_ROOT = Path("/home/nitanda_sub/mark/repos/outer_repos")
OUTER_PAPERS_ROOT = Path("/home/nitanda_sub/mark/repos/outer_papers")
OUTER_REPOS_AUTOMATION_ROOT = OUTER_REPOS_ROOT / "automation_systems"
OUTER_REPOS_SAMPLING_ROOT = OUTER_REPOS_ROOT / "sampling_theory_sde"
OUTER_PAPERS_SAMPLING_ROOT = OUTER_PAPERS_ROOT / "sampling_theory_sde"
OUTER_PAPERS_AUTOMATION_ROOT = OUTER_PAPERS_ROOT / "automation_systems"

SALD_ROOT = Path("/home/nitanda_sub/mark/repos/sald/paper")
RMFLD_ROOT = Path("/home/nitanda_sub/mark/repos/RMFLD/RMFLD_paper")
SLT_ROOT = OUTER_REPOS_SAMPLING_ROOT / "lean-stat-learning-theory"
SLT_ARTICLE_ROOT = OUTER_PAPERS_SAMPLING_ROOT / "Statistical Learning Theory in Lean 4 Empirical Processes from Scratch"
CHEWI_LOG_CONCAVE_PDF = OUTER_PAPERS_SAMPLING_ROOT / "Chewi-Log-Concave-Sampling" / "main.pdf"
CHEWI_LEGACY_PDF = OUTER_REPOS_SAMPLING_ROOT / "chewisinho-stochastic-processes-main.pdf"
LEAN_ASYMPTOTIC_STATISTICS_ROOT = OUTER_REPOS_SAMPLING_ROOT / "Lean-Asymptotic-Statistical-Theory"
LEAN_ASYMPTOTIC_STATISTICS_PDF = (
    OUTER_PAPERS_SAMPLING_ROOT
    / "Hypothesis-Disciplined-Asymptotic-Statistical-Theory"
    / "2606.20642.pdf"
)
LEANMARATHON_ROOT = OUTER_REPOS_AUTOMATION_ROOT / "LeanMarathon"
LEANMARATHON_PDF = OUTER_PAPERS_AUTOMATION_ROOT / "LeanMarathon-2606.05400.pdf"
TECH_REPORT_ROOT = Path(os.environ.get("ASTIS_TECH_REPORT_ROOT", str(ROOT.parent / "Auto_Proof_Papers" / "ASTIS")))

QUANTUM_AUTOPROOF_URL = "https://github.com/DakeBU/Quantum-Computing-Block-Encoding/tree/wip/ghl2025-faithful-20260518-0201"
MATHLIB_URL = "https://mathlib-initiative.org/"
SLT_URL = "https://github.com/YuanheZ/lean-stat-learning-theory"
SLT_ARXIV_URL = "https://arxiv.org/abs/2602.02285"
CHEWI_LOG_CONCAVE_URL = "https://chewisinho.github.io/main.pdf"
LEAN_ASYMPTOTIC_STATISTICS_URL = "https://github.com/junwei-lu/Lean-Asymptotic-Statistical-Theory"
LEAN_ASYMPTOTIC_STATISTICS_ARXIV_URL = "https://arxiv.org/abs/2606.20642"
LEANMARATHON_URL = "https://github.com/YuanheZ/LeanMarathon"
LEANMARATHON_ARXIV_URL = "https://arxiv.org/abs/2606.05400"
MATHCODE_URL = "https://github.com/math-ai-org/mathcode"
MATHCODE_LOCAL_REFERENCE = OUTER_REPOS_AUTOMATION_ROOT / "mathcode"
ARIS_URL = "https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep"
LBG_URL = "https://github.com/Trinkle23897/learning-beyond-gradients"
EOH_URL = "https://github.com/FeiLiu36/EoH"

BASE_AGENT_ROLES = ("upper", "middle", "lower", "reviewer")
UPPER_DIRECTOR_ROLE = "upper_director"
UPPER_PANEL_ROLES = ("upper_source_math", "upper_proof_dag", "upper_process_memory")
MIDDLE_COORDINATOR_ROLE = "middle_formalizer"
MIDDLE_PANEL_ROLES = ("middle_source_correspondence", "middle_technical_lemma", "middle_report_export")
DEFAULT_REVIEWER_AGENT_ROLES = ("reviewer_gate",)
FINAL_AUDIT_REVIEWER_ROLES = ("reviewer_gate", "reviewer_waste")
AGENT_ROLES = (
    *BASE_AGENT_ROLES,
    UPPER_DIRECTOR_ROLE,
    *UPPER_PANEL_ROLES,
    "upper_critic",
    "upper_planner",
    MIDDLE_COORDINATOR_ROLE,
    *MIDDLE_PANEL_ROLES,
    "middle_architect",
    "middle_librarian",
    *DEFAULT_REVIEWER_AGENT_ROLES,
    "reviewer_waste",
    *(f"lower_{i}" for i in range(1, 17)),
)
TRIAL_KINDS = ("plan", "attempt", "build", "review", "proposal", "compression", "handoff", "source-index")
TRIAL_STATUSES = ("queued", "running", "blocked", "failed", "compiled", "accepted", "rejected", "indexed")
PACKET_CLASSIFICATIONS = (
    "discharges-supplied-hypothesis",
    "narrows-source-cited-boundary",
    "rejected-wrapper-churn",
)
SALD_COMPACT_CONTEXT_START_CYCLE = 85
FORBIDDEN_REGEX = re.compile(
    r"\bsorry\b|\badmit\b|"
    r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|local|unsafe|partial)\s+)*"
    r"(?:axiom|constant|postulate)\b|"
    r"Prop\s*:=\s*True|:=\s*trivial"
)
LEAN_DECL_REGEX = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|local|unsafe|partial)\s+)*"
    r"(theorem|lemma|def|instance|structure|class|inductive)\b",
    re.MULTILINE,
)
LEAN_DECL_NAME_REGEX = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|local|unsafe|partial)\s+)*"
    r"(theorem|lemma|def|instance|structure|class|inductive)\s+([A-Za-z0-9_.'-]+)",
)

WORK_DIRS = [
    "tasks",
    "conversion-windows",
    "paper-notes",
    "agent-briefs",
    "proof-obligations",
    "proof-attempts",
    "proof-blueprints",
    "verifier-feedback",
    "candidate-populations",
    "open-problem-proposals",
    "reviews",
    "runs",
    "runs/efficiency",
    "runs/context-packs",
    "runs/pro-prompts",
    "research-wiki/cited-results",
    "research-wiki/source-index",
    "research-wiki/blueprints",
    "research-wiki/retrieval-index",
    "research-wiki/technical-lemmas",
    "research-wiki/technical-lemma-memory",
    "research-wiki/lemma-dags",
    "research-wiki/sampling-sde-library",
    "research-wiki/sampling-sde-library/cards",
    "research-wiki/external-lean-libraries",
    "research-wiki/paper-contributions",
    "research-wiki/paper-contributions/SALD",
    "research-wiki/paper-memory",
    "research-wiki/paper-memory/ASTIS-SALD-001",
    "research-wiki/todo",
    "research-wiki/papers",
    "research-wiki/claims",
    "research-wiki/ideas",
    "research-wiki/experiments",
    "paper-notes/SALD/markdown/cycle-summaries",
    "paper-notes/project-paper/cycle-updates",
]


def now_stamp() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def file_stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    return value or "untitled"


def public_article_text(value: str) -> str:
    """Convert internal run notes into public-facing report prose."""

    replacements = {
        "sald_version_2.tex": "unrelated draft routes",
        "•": " dot ",
        "→": " -> ",
        "↦": " |-> ",
        "–": "-",
        "—": "--",
        "“": '"',
        "”": '"',
        "’": "'",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"/home/nitanda_sub/mark/repos/[^\s`]+", "[local source path]", value)
    value = re.sub(r"\bappendix\.tex:\d+(?:-\d+)?", "the relevant SALD appendix passage", value)
    value = re.sub(r"\bmain_body\.tex:\d+(?:-\d+)?", "the corresponding SALD main-text passage", value)
    value = re.sub(r"\b[A-Za-z0-9_.-]+\.tex:\d+(?:-\d+)?", "the source LaTeX passage", value)
    value = re.sub(r"\b[1-9]\d{2,3}-\d{3,4}\b", "the relevant SALD source passage", value)
    value = re.sub(r"lower_\d+ recorded as lower because astis\.py rejects lower_\d+\.\s*", "", value)
    return value


def run(cmd: list[str]) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT).returncode


def run_capture(cmd: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.returncode, completed.stdout


def strip_lean_comments_and_strings(text: str) -> str:
    """Remove Lean comments and string literals for policy scans.

    The forbidden-proof gate should reject executable proof closures, not the
    documentation that explains the policy or the string-valued policy table in
    `Core.lean`.
    """

    result: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    in_line_comment = False
    while index < len(text):
        char = text[index]
        nxt = text[index + 1] if index + 1 < len(text) else ""

        if in_line_comment:
            if char == "\n":
                in_line_comment = False
                result.append("\n")
            else:
                result.append(" ")
            index += 1
            continue

        if block_depth > 0:
            if char == "/" and nxt == "-":
                block_depth += 1
                result.extend("  ")
                index += 2
                continue
            if char == "-" and nxt == "/":
                block_depth -= 1
                result.extend("  ")
                index += 2
                continue
            result.append("\n" if char == "\n" else " ")
            index += 1
            continue

        if in_string:
            if char == "\\" and nxt:
                result.extend("  ")
                index += 2
                continue
            if char == '"':
                in_string = False
            result.append("\n" if char == "\n" else " ")
            index += 1
            continue

        if char == "-" and nxt == "-":
            in_line_comment = True
            result.extend("  ")
            index += 2
            continue
        if char == "/" and nxt == "-":
            block_depth = 1
            result.extend("  ")
            index += 2
            continue
        if char == '"':
            in_string = True
            result.append(" ")
            index += 1
            continue

        result.append(char)
        index += 1

    return "".join(result)


def forbidden_pattern_hits() -> list[str]:
    hits = []
    for path in lean_source_files():
        if not path.exists():
            continue
        stripped = strip_lean_comments_and_strings(read_text(path))
        for lineno, line in enumerate(stripped.splitlines(), start=1):
            if FORBIDDEN_REGEX.search(line):
                hits.append(f"{rel(path)}:{lineno}:{line.strip()}")
    return hits


def lean_source_files() -> list[Path]:
    files = [
        *ROOT.glob("AutoSamplingTheory/**/*.lean"),
        *ROOT.glob("Tests/**/*.lean"),
        ROOT / "AutoSamplingTheory.lean",
        ROOT / "Tests.lean",
    ]
    return sorted({path for path in files if path.exists()})


def lean_diagnostics() -> dict:
    """Report lightweight Lean proof diagnostics for reviewer handoffs."""

    per_file = []
    totals: dict[str, int] = {
        "files": 0,
        "theorem": 0,
        "lemma": 0,
        "def": 0,
        "instance": 0,
        "structure": 0,
        "class": 0,
        "inductive": 0,
        "forbidden_hits": 0,
    }
    for path in lean_source_files():
        stripped = strip_lean_comments_and_strings(read_text(path))
        counts = {key: 0 for key in totals if key not in {"files", "forbidden_hits"}}
        for match in LEAN_DECL_REGEX.finditer(stripped):
            counts[match.group(1)] += 1
        forbidden = []
        for lineno, line in enumerate(stripped.splitlines(), start=1):
            if FORBIDDEN_REGEX.search(line):
                forbidden.append({"line": lineno, "text": line.strip()})
        totals["files"] += 1
        totals["forbidden_hits"] += len(forbidden)
        for key, value in counts.items():
            totals[key] += value
        per_file.append({"file": rel(path), "declarations": counts, "forbidden": forbidden})
    return {
        "mathcode_reference": MATHCODE_URL,
        "mathcode_local_reference": str(MATHCODE_LOCAL_REFERENCE),
        "mathcode_local_reference_exists": MATHCODE_LOCAL_REFERENCE.exists(),
        "policy": "diagnostics are advisory; lake build and forbidden-pattern gate remain mandatory",
        "totals": totals,
        "files": per_file,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_if_missing(path: Path, text: str) -> bool:
    if path.exists():
        return False
    harness.atomic_write_text(path, text)
    print(f"initialized {rel(path)}")
    return True


def write_new(path: Path, text: str) -> None:
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing file: {rel(path)}")
    harness.atomic_write_text(path, text)
    print(f"wrote {rel(path)}")


def write_text(path: Path, text: str) -> None:
    harness.atomic_write_text(path, text)
    print(f"wrote {rel(path)}")


def write_text_mirror(primary: Path, text: str, mirrors: list[Path] | None = None) -> None:
    write_text(primary, text)
    for mirror in mirrors or []:
        if mirror == primary:
            continue
        write_text(mirror, text)


def copy_text_if_exists(source: Path, destination: Path) -> bool:
    if not source.exists():
        return False
    write_text(destination, source.read_text(encoding="utf-8"))
    return True


def append_line(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with harness.file_lock(path.resolve()):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()
            os.fsync(handle.fileno())


def append_jsonl(path: Path, record: dict) -> None:
    harness.append_jsonl(path, record)


def load_jsonl(path: Path) -> list[dict]:
    return harness.load_jsonl(path)


def load_feedback_payload(args: argparse.Namespace) -> dict:
    feedback: dict = {}
    if getattr(args, "feedback_json", ""):
        source = args.feedback_json.strip()
        try:
            if source.startswith("{") or source.startswith("["):
                parsed = json.loads(source)
            else:
                maybe_path = Path(source)
                parsed = json.loads(maybe_path.read_text(encoding="utf-8")) if maybe_path.exists() else json.loads(source)
            if isinstance(parsed, dict):
                feedback.update(parsed)
            else:
                raise ValueError("feedback payload must be a JSON object")
        except Exception as exc:
            raise SystemExit(f"invalid --feedback-json payload: {exc}") from exc
    for item in getattr(args, "feedback_field", []) or []:
        if "=" not in item:
            raise SystemExit(f"--feedback-field must be key=value, got: {item}")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        lowered = value.lower()
        if lowered == "true":
            parsed_value: object = True
        elif lowered == "false":
            parsed_value = False
        elif lowered in {"null", "none", ""}:
            parsed_value = None
        else:
            parsed_value = value
        feedback[key] = parsed_value
    return feedback


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"version": 2, "active_task": "ASTIS-CHEWI-001", "last_check": None}
    return json.loads(read_text(STATE_FILE))


def save_state(state: dict) -> None:
    harness.atomic_write_text(STATE_FILE, json.dumps(state, indent=2, sort_keys=True) + "\n")


def ensure_manifest() -> None:
    write_if_missing(
        MANIFEST,
        """# ASTIS Output Manifest

| Timestamp | Tool | File | Stage | Description |
|---|---|---|---|---|
""",
    )


def add_manifest(tool: str, file: Path, stage: str, description: str) -> None:
    ensure_manifest()
    append_line(MANIFEST, f"| {now_stamp()} | {tool} | `{rel(file)}` | {stage} | {description} |")


def init_texts() -> dict[Path, str]:
    return {
        ROOT / "research-wiki" / "index.md": "# ASTIS Research Wiki\n",
        ROOT / "research-wiki" / "query_pack.md": (
            "# Query Pack\n\n"
            "- Active task: ASTIS-SALD-001\n"
            "- Gate: `python3 tools/astis.py check`\n"
            f"- SLT reference: `{SLT_ROOT}`\n"
            f"- LeanMarathon reference: `{LEANMARATHON_ROOT}`\n"
            f"- MathCode workflow reference: `{MATHCODE_URL}`\n"
        ),
        ROOT / "paper-notes" / "README.md": (
            "# Paper Notes\n\n"
            "Human-readable proof exports and source-to-Lean notes.\n"
        ),
        PROOF_BLUEPRINT_DIR / "README.md": (
            "# Proof Blueprints\n\n"
            "Canonical ABEIS-style compact system-of-record snapshots for ASTIS tasks.\n"
            "Legacy mirrors may also exist under `research-wiki/blueprints/`.\n"
        ),
        VERIFIER_FEEDBACK_DIR / "README.md": (
            "# Verifier Feedback\n\n"
            "Typed feedback packets for Sampling/SDE proof attempts.  These are\n"
            "diagnostics for choosing the next Lean target, not theorem closure.\n"
        ),
        AGENT_BRIEFS_DIR / "README.md": (
            "# Agent Briefs\n\n"
            "Generated context packets for upper/middle/lower/reviewer agents.\n"
        ),
        RETRIEVAL_INDEX_DIR / "README.md": (
            "# Retrieval Index\n\n"
            "Compact JSON memory packets for upper and middle agents.  Read these\n"
            "before replaying long run logs.\n"
        ),
        TECHNICAL_LEMMAS_DIR / "README.md": (
            "# Technical Lemmas\n\n"
            "Canonical memory for reusable Sampling/SDE background facts: KL/FI/LSI,\n"
            "weak Fokker--Planck, Ito/Taylor, Gaussian moments, measurability,\n"
            "integrability, and integration-by-parts tools.  Legacy mirrors may\n"
            "exist under `research-wiki/technical-lemma-memory/`.\n"
        ),
        LEMMA_DAG_DIR / "README.md": (
            "# Lemma DAGs\n\n"
            "Mathlib-ready dependency graphs for reusable SDE/Sampling leaf lemmas.\n"
            "Run `python3 tools/astis.py lemma-dag-refresh` to regenerate the\n"
            "standard skill tree and current SALD weak-Fokker--Planck leaf DAG.\n"
        ),
        SAMPLING_LIBRARY_DIR / "README.md": (
            "# Sampling/SDE Lean Library\n\n"
            "This directory is the atlas for the Lean leaves used to formalize\n"
            "`Log-Concave Sampling`.  It is organized by reusable mathematical roots, not\n"
            "by temporary proof attempts.  Chapter subtrees should point into these roots\n"
            "and only create new leaves when no shared Mathlib-shaped fact exists.\n\n"
            "## Navigation Graph\n\n"
            "```mermaid\n"
            "flowchart LR\n"
            "  Readme[this atlas]:::node\n"
            "  Roadmap[roadmap<br/>chapter to root map]:::node\n"
            "  DAG[foundation DAG<br/>blue/red theorem tree]:::node\n"
            "  Modules[module graph<br/>Lean owners]:::node\n"
            "  Cards[cards<br/>one file per module]:::node\n"
            "  Registry[registry<br/>compiled facts only]:::node\n\n"
            "  Readme --> Roadmap --> DAG --> Modules --> Cards --> Registry\n\n"
            "  classDef node fill:#e0f2fe,stroke:#0284c7,color:#0f172a,stroke-width:2px;\n"
            "```\n\n"
            "| Need | File |\n"
            "|---|---|\n"
            "| chapter-to-Lean roadmap | `roadmap/log_concave_sampling_to_lean_tree.md` |\n"
            "| master theorem DAG | `../lemma-dags/log_concave_sampling_foundation.md` |\n"
            "| generated Lean module graph | `lean-leaf-module-graph.md` |\n"
            "| module cards | `cards/` |\n"
            "| compiled declaration registry | `../../AutoSamplingTheory/TechnicalLemmas/Registry.lean` |\n\n"
            "## Ch.1 Active Subtree\n\n"
            "```mermaid\n"
            "flowchart LR\n"
            "  A[pointwise generator<br/>Lf = Delta f - grad V . grad f]:::blue\n"
            "  B[weighted coordinate sum<br/>exp(-V)Lf]:::blue\n"
            "  C[coordinateDivergence<br/>ASTIS convention]:::blue\n"
            "  D[Mathlib fderiv<br/>summand bridge]:::blue\n"
            "  AE[WithLp/Pi a.e.<br/>trace bridge]:::blue\n"
            "  P[explicit Pi trace<br/>= exp(-V)Lf]:::blue\n"
            "  R[scalar display ContinuousOn<br/>from components]:::blue\n"
            "  Q[trace IntegrableOn<br/>under global C1/C2<br/>with canonical fderiv]:::blue\n"
            "  T[trace-to-coordinate<br/>IntegrableOn transfer]:::blue\n"
            "  E[box divergence theorem<br/>face terms]:::blue\n"
            "  X[global C1/C2 components<br/>and Pi field fderiv]:::blue\n"
            "  F[weighted IBP<br/>no boundary]:::blue\n"
            "  DOM[generator and semigroup<br/>domain contracts]:::red\n"
            "  G[invariant Gibbs law]:::red\n\n"
            "  A --> B --> C --> D --> AE --> T --> E --> F --> G\n"
            "  DOM --> G\n"
            "  D --> P --> Q --> T\n"
            "  R --> Q\n"
            "  X --> P\n"
            "  X --> R\n"
            "  X --> Q\n\n"
            "  classDef blue fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;\n"
            "  classDef red fill:#fee2e2,stroke:#dc2626,color:#450a0a,stroke-width:2px;\n"
            "```\n\n"
            "Run `python3 tools/astis.py module-graph-refresh` to regenerate the SVG graph,\n"
            "module ledger, cards, and retrieval index.  Blue status is reserved for\n"
            "compiled ASTIS-owned declarations; external references and unproved analytic\n"
            "backends stay red or orange.\n"
        ),
        EXTERNAL_LEAN_LIBRARY_DIR / "README.md": (
            "# External Lean And Textbook Reference Cards\n\n"
            "Memory cards for Mathlib, external Lean projects, and textbooks used as\n"
            "references or port sources.  These are not local proof certificates;\n"
            "a theorem becomes callable only after ASTIS owns a compiled Lean\n"
            "declaration for it.\n"
        ),
        PAPER_CONTRIBUTION_DIR / "README.md": (
            "# Paper Contributions\n\n"
            "Canonical memory for paper-owned proof contributions.  Keep these\n"
            "separate from reusable technical lemmas.\n"
        ),
        SALD_CONTRIBUTION_DIR / "README.md": (
            "# SALD Paper Contributions\n\n"
            "Task-local memory for the VA-SALD faithful reproduction: source lines,\n"
            "proof-DAG leaves, and unfinished theorem boundaries.\n"
        ),
    }


def cmd_init(_: argparse.Namespace) -> int:
    for dirname in WORK_DIRS:
        (ROOT / dirname).mkdir(parents=True, exist_ok=True)
    for path, text in init_texts().items():
        write_if_missing(path, text)
    ensure_manifest()
    state = load_state()
    state["version"] = 2
    if state.get("active_task") in {None, "", "ASTIS-SALD-001"}:
        state["active_task"] = "ASTIS-CHEWI-001"
    state["task_relationship"] = {
        "primary_foundation": "ASTIS-CHEWI-001",
        "downstream_consumers": ["ASTIS-SALD-001", "ASTIS-RMFLD-001"],
    }
    state["initialized_at"] = state.get("initialized_at") or now_stamp()
    save_state(state)
    add_manifest("astis.py init", ROOT / "ASTIS.md", "init", "Initialized ASTIS workflow state")
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    if not (ROOT / "lake-manifest.json").exists():
        code = run(["lake", "update"])
        if code != 0:
            return code
    code = run(["lake", "exe", "cache", "get"])
    if code != 0:
        return code
    code = run(["lake", "build"])
    if code != 0:
        return code
    code = run(["lake", "build", "Tests"])
    if code != 0:
        return code
    code = run([sys.executable, "tools/atlas_memory.py", "check"])
    if code != 0:
        return code
    hits = forbidden_pattern_hits()
    if hits:
        print("\n".join(hits))
        return 1
    state = load_state()
    state["last_check"] = {"timestamp": now_stamp(), "exit_code": 0}
    save_state(state)
    print("ASTIS check passed")
    return 0


def parse_literature() -> list[dict[str, str]]:
    source = read_text(ROOT / "AutoSamplingTheory" / "Literature.lean")
    blocks = re.findall(r"\{\s*key := .*?\n\s*\}", source, flags=re.S)
    entries = []
    for block in blocks:
        item: dict[str, str] = {}
        for field in ["key", "title", "authors", "targetFile", "urlOrPath", "note"]:
            match = re.search(field + r' := "([^"]*)"', block)
            if match:
                item[field] = match.group(1)
        status_match = re.search(r"status := ImplementationStatus\.([A-Za-z]+)", block)
        mode_match = re.search(r"mode := PaperMode\.([A-Za-z]+)", block)
        if status_match:
            item["status"] = status_match.group(1)
        if mode_match:
            item["mode"] = mode_match.group(1)
        if "key" in item:
            entries.append(item)
    return entries


def cmd_list_literature(_: argparse.Namespace) -> int:
    for item in parse_literature():
        print(
            f"{item.get('status','unknown'):14s} "
            f"{item.get('mode','unknown'):18s} "
            f"{item.get('key')} :: {item.get('title')}"
        )
    return 0


def task_files() -> list[Path]:
    return sorted((ROOT / "tasks").glob("*.md"))


def read_task_status(path: Path) -> str:
    text = read_text(path)
    match = re.search(r"^Status:\s*`?([^`\n]+)`?", text, flags=re.M)
    return match.group(1).strip() if match else "unknown"


def task_context(task_id: str) -> tuple[str, str]:
    path = ROOT / "tasks" / f"{slugify(task_id)}.md"
    if path.exists():
        text = read_text(path)
        return text.splitlines()[0].lstrip("# ").strip(), text
    raise SystemExit(f"task not found: {task_id}")


def cmd_next_task(_: argparse.Namespace) -> int:
    candidates = []
    for path in task_files():
        if path.name == "README.md":
            continue
        status = read_task_status(path)
        if status in {"active", "planned"}:
            priority = 0 if status == "active" else 1
            candidates.append((priority, path))
    if not candidates:
        print("no active or planned tasks")
        return 0
    path = sorted(candidates, key=lambda item: (item[0], item[1].name))[0][1]
    print(f"{path.stem}: {read_text(path).splitlines()[0].lstrip('# ').strip()}")
    print(f"path: {rel(path)}")
    return 0


def cmd_list_tasks(_: argparse.Namespace) -> int:
    priority = {"active": 0, "planned": 1, "indexed": 2, "blocked": 3}
    paths = [path for path in task_files() if path.name != "README.md"]
    for path in sorted(paths, key=lambda item: (priority.get(read_task_status(item), 9), item.name)):
        print(f"{read_task_status(path):12s} {path.stem:18s} {read_text(path).splitlines()[0].lstrip('# ').strip()}")
    return 0


def source_roots_for_task(task_id: str) -> tuple[Path, list[str], Path]:
    if task_id == "ASTIS-SALD-001":
        return SALD_ROOT, ["sald_version_2.tex"], ROOT / "research-wiki" / "source-index" / "SALD_original.jsonl"
    if task_id == "ASTIS-RMFLD-001":
        return RMFLD_ROOT, [], ROOT / "research-wiki" / "source-index" / "RMFLD_paper.jsonl"
    raise SystemExit(f"no source-index configuration for task: {task_id}")


ENV_RE = re.compile(
    r"\\begin\{(?P<kind>theorem|lemma|proposition|prop|corollary|definition|defn|assumption|ass|thm|equation\*?|align\*?|alignat\*?|gather\*?|multline\*?)\}"
    r"(?:\[(?P<title>[^\]]*)\])?"
)
LABEL_RE = re.compile(r"\\label\{(?P<label>[^}]+)\}")


def index_tex_file(path: Path, root: Path) -> list[dict]:
    records = []
    current: dict | None = None
    current_env: str | None = None
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        if line.lstrip().startswith("%"):
            continue
        if current is not None:
            current.setdefault("body_lines", []).append(line.strip())
            label = LABEL_RE.search(line)
            if label and not current.get("label"):
                current["label"] = label.group("label")
            if current_env and re.search(rf"\\end\{{{re.escape(current_env)}\}}", line):
                current["line_end"] = lineno
                body = "\n".join(current.pop("body_lines", []))
                current["body_excerpt"] = compact_inline_text(body, 900)
                if current.get("label"):
                    records.append(current)
                current = None
                current_env = None
            continue
        env = ENV_RE.search(line)
        if env:
            current_env = env.group("kind")
            current = {
                "kind": current_env,
                "title": env.group("title") or "",
                "file": str(path.relative_to(root)),
                "line": lineno,
                "line_start": lineno,
                "line_end": lineno,
                "label": "",
                "snippet": line.strip()[:240],
                "body_lines": [line.strip()],
            }
            label = LABEL_RE.search(line)
            if label:
                current["label"] = label.group("label")
            if re.search(rf"\\end\{{{re.escape(current_env)}\}}", line):
                body = "\n".join(current.pop("body_lines", []))
                current["body_excerpt"] = compact_inline_text(body, 900)
                if current.get("label"):
                    records.append(current)
                current = None
                current_env = None
            continue
    return records


def cmd_source_index(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    source_root, excluded, output = source_roots_for_task(args.task)
    if not source_root.exists():
        raise SystemExit(f"source root not found: {source_root}")
    records = []
    for path in sorted(source_root.glob("*.tex")):
        if path.name in excluded:
            continue
        records.extend(index_tex_file(path, source_root))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
    add_manifest("astis.py source-index", output, "source-index", f"Indexed {len(records)} source declarations for {args.task}")
    print(f"indexed {len(records)} declarations -> {rel(output)}")
    if args.task == "ASTIS-SALD-001" and any(record["file"] == "sald_version_2.tex" for record in records):
        raise SystemExit("sald_version_2.tex was indexed despite exclusion")
    return 0


def compact_inline_text(value: str, max_chars: int = 420) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3].rstrip() + "..."


def trial_records_for_task(task_id: str) -> list[dict]:
    records = []
    for record in load_jsonl(TRIAL_LOG):
        if record.get("task_id") != task_id:
            continue
        artifact = record.get("artifact", "")
        artifact_path = ROOT / artifact if artifact else None
        if artifact.startswith("runs/") and "cycle" in artifact and artifact_path and not artifact_path.exists():
            continue
        records.append(record)
    return records


def recent_trial_text(task_id: str, limit: int = 4, max_note_chars: int = 420) -> str:
    records = trial_records_for_task(task_id)
    if not records:
        return "no trial records yet"
    lines = []
    for record in records[-limit:]:
        lines.append(
            "{timestamp} {role}/{kind} {status} gate={lean_gate} :: {notes}".format(
                timestamp=record.get("timestamp", ""),
                role=record.get("role", ""),
                kind=record.get("kind", ""),
                status=record.get("status", ""),
                lean_gate=record.get("lean_gate", ""),
                notes=compact_inline_text(record.get("notes", ""), max_note_chars),
            )
        )
    return "\n".join(lines)


def latest_handoff_notes(task_id: str, limit: int = 6) -> list[str]:
    notes = []
    for record in reversed(trial_records_for_task(task_id)):
        if record.get("kind") != "handoff":
            continue
        note = compact_inline_text(record.get("notes", ""), 520)
        if note:
            notes.append(note)
        if len(notes) >= limit:
            break
    return list(reversed(notes))


def classification_counts_in_text(text: str) -> dict[str, int]:
    return {name: len(re.findall(re.escape(name), text)) for name in PACKET_CLASSIFICATIONS}


def classification_counts_in_trials(task_id: str, cycles: list[int] | None = None) -> dict[str, int]:
    allowed_cycles = set(cycles or [])
    counts = {name: 0 for name in PACKET_CLASSIFICATIONS}
    for record in trial_records_for_task(task_id):
        note = record.get("notes", "")
        cycle = cycle_number_from_record(record)
        if allowed_cycles and (cycle is None or cycle not in allowed_cycles):
            continue
        for name in PACKET_CLASSIFICATIONS:
            if name in note:
                counts[name] += 1
    return counts


def extract_remaining_boundary(note: str) -> str:
    note = compact_inline_text(note, 1100)
    marker = re.search(
        r"((?:Remaining exact blocker|Remaining exact boundary|Remaining blockers?|Remaining boundary).*?)(?:\. No fake|; no |$)",
        note,
        flags=re.I,
    )
    return marker.group(1).strip() if marker else note


def cycle_number_from_record(record: dict) -> int | None:
    fields = [
        record.get("trial_id", ""),
        record.get("artifact", ""),
        record.get("notes", ""),
    ]
    for value in fields:
        match = re.search(r"(?:cycle|Cycle)\s*-?(\d+)", value)
        if match:
            return int(match.group(1))
    return None


def latest_trial_cycle(task_id: str) -> int:
    latest = 0
    for record in trial_records_for_task(task_id):
        cycle = cycle_number_from_record(record)
        if cycle is not None:
            latest = max(latest, cycle)
    return latest


def proof_status_counts() -> dict[str, int]:
    counts = {status: 0 for status in ["planned", "sourceCited", "contractOnly", "obligation", "formalized", "blocked"]}
    for path in lean_source_files():
        text = strip_lean_comments_and_strings(read_text(path))
        for match in re.finditer(r"ProofStatus\.([A-Za-z]+)", text):
            status = match.group(1)
            counts[status] = counts.get(status, 0) + 1
    return counts


def latest_matching_note(task_id: str, patterns: list[str]) -> str:
    compiled = [re.compile(pattern, flags=re.I) for pattern in patterns]
    for record in reversed(trial_records_for_task(task_id)):
        note = record.get("notes", "")
        if any(pattern.search(note) for pattern in compiled):
            return extract_remaining_boundary(note)
    return ""


def latest_reviewer_blocker(task_id: str) -> str:
    decision_patterns = [
        "Exact boundary narrowed",
        "next best leaf",
        "leaf=",
        "error_class=",
        "source-contract gap",
    ]
    for record in reversed(trial_records_for_task(task_id)):
        if base_agent_role(record.get("role", "")) != "reviewer" or record.get("kind") != "handoff":
            continue
        note = compact_inline_text(record.get("notes", ""), 1100)
        remaining = extract_remaining_boundary(note)
        if remaining != note:
            return remaining
        if any(pattern in note for pattern in decision_patterns):
            return note
        if "Remaining" in note:
            return note
    if task_id == "ASTIS-SALD-001":
        return (
            "Remaining exact boundary: prove the concrete contraction bound, "
            "align `weakGradPairing`/`driftDiv` with the `hatRhoS` law integral, "
            "and prove the no-boundary IBP theorem for `hatRhoS * barB`."
        )
    return "No reviewer blocker recorded yet; use source index and proof-obligation ledger."


def blueprint_control_state(task_id: str) -> dict:
    latest_cycle = latest_trial_cycle(task_id)
    recent_cycles = list(range(max(1, latest_cycle - 5), latest_cycle + 1)) if latest_cycle else []
    latest_blocker = latest_reviewer_blocker(task_id)
    dynamic_leaf = latest_blocker or latest_matching_note(task_id, [
        r"next non-wrapper blocker",
        r"first non-wrapper blocker",
        r"Remaining exact blocker",
        r"remaining .* blocker",
        r"hbarBStateSetIntegral",
        r"dynamic leaf",
    ])
    illness_area = latest_matching_note(task_id, [
        r"illness area",
        r"affected region",
        r"state-event",
        r"box-trace",
        r"appendix\.tex:1368-1377",
        r"appendix\.tex:1379-1387",
        r"appendix\.tex:1358-1366",
    ]) or dynamic_leaf
    if task_id == "ASTIS-CHEWI-001":
        frontier = harness.reconcile_frontier(ROOT)
        selected = frontier.get("selected_ready_leaf")
        if selected:
            dynamic_leaf = (
                f"{selected['node_id']}: {selected['label']}; missing declarations: "
                + ", ".join(selected["missing_declarations"])
            )
            illness_area = dynamic_leaf
    if task_id == "ASTIS-SALD-001":
        system_of_record = [
            "AutoSamplingTheory/SALD.lean",
            "conversion-windows/ASTIS-SALD-001.md",
            "proof-obligations/ASTIS-SALD-001.md",
            "research-wiki/source-index/SALD_original.jsonl",
            "proof-blueprints/ASTIS-SALD-001.md",
            "research-wiki/paper-contributions/SALD/unfinished_source_map.md",
            "research-wiki/technical-lemmas/technical_lemma_registry.jsonl",
            "research-wiki/retrieval-index/ASTIS-SALD-001.json",
            "research-wiki/cited-results/SLT_reuse_audit.md",
            "runs/trials.jsonl",
        ]
        stage = "LeanMarathon Stage-2 analogue: DAG-guided proof discharge after faithful source transcript stabilization"
    elif task_id == "ASTIS-CHEWI-001":
        system_of_record = [
            "tasks/ASTIS-CHEWI-001.md",
            "proof-blueprints/ASTIS-CHEWI-001.md",
            "research-wiki/sampling-sde-library/log_concave_sampling_overview.md",
            "research-wiki/lemma-dags/log_concave_sampling_foundation.md",
            "research-wiki/sampling-sde-library/roadmap/log_concave_sampling_to_lean_tree.md",
            "research-wiki/sampling-sde-library/lean-leaf-module-graph.md",
            "research-wiki/retrieval-index/ASTIS-CHEWI-001.json",
            "research-wiki/external-lean-libraries/log-concave-sampling-notes.md",
            "research-wiki/external-lean-libraries/lean-asymptotic-statistical-theory.md",
            "agent-briefs/log_concave_sampling_6h_execution_pack.md",
            "AutoSamplingTheory/TechnicalLemmas/Registry.lean",
            "runs/trials.jsonl",
        ]
        stage = "Log-concave sampling foundation Stage-1: chapter map, shared-root DAG, and Mathlib-ready leaf growth"
    else:
        system_of_record = [
            "AutoSamplingTheory/RMFLD.lean",
            "research-wiki/source-index/RMFLD_paper.jsonl",
            "runs/trials.jsonl",
        ]
        stage = "exploratoryProof blueprint construction"
    return {
        "task_id": task_id,
        "generated": now_stamp(),
        "latest_cycle": latest_cycle,
        "recent_cycles": recent_cycles,
        "system_of_record": system_of_record,
        "stage": stage,
        "dynamic_leaf_candidate": dynamic_leaf,
        "illness_area_candidate": illness_area,
        "latest_blocker": latest_blocker,
        "trial_classifications_recent": classification_counts_in_trials(task_id, recent_cycles),
        "proof_status_counts": proof_status_counts(),
        "leanmarathon_controls_absorbed": [
            "blueprint/system-of-record control state",
            "target-review no-more/no-less discipline",
            "dynamic-leaf proof discharge instead of broad route replay",
            "illness-area refiner rule for connected blocker regions",
            "deterministic CI gate as the only progress authority",
            "local refinement region before asking for upstream changes",
        ],
        "astis_kept_advantages": [
            "EoH-style candidate populations for exploratoryProof mode after a Lean-checkable target is fixed",
            "Learning-beyond-gradients style trial memory through logs, summaries, rejected directions, and negative cache",
            "upper/middle/lower/reviewer agent stack inherited from the ARIS/LBG/QBE automation lineage",
            "auto-research-in-sleep long-window self-loop with graceful final-cycle completion",
            "plain-file reproducibility without requiring GitHub PR or Slurm for local research iteration",
            "sampling/SDE-specific source anchors, proof obligations, technical lemma memory, and SLT port audit",
        ],
        "references": {
            "EoH": EOH_URL,
            "Learning beyond gradients": LBG_URL,
            "Auto-research-in-sleep": ARIS_URL,
            "LeanMarathon": LEANMARATHON_URL,
            "LeanMarathon paper": LEANMARATHON_ARXIV_URL,
            "local LeanMarathon repo": str(LEANMARATHON_ROOT),
            "local LeanMarathon pdf": str(LEANMARATHON_PDF),
        },
    }


def blueprint_status_text(state: dict) -> str:
    controls = "\n".join(f"- {item}" for item in state["leanmarathon_controls_absorbed"])
    kept = "\n".join(f"- {item}" for item in state["astis_kept_advantages"])
    record = "\n".join(f"- `{item}`" for item in state["system_of_record"])
    class_lines = "\n".join(
        f"- `{key}`: {value}" for key, value in state["trial_classifications_recent"].items()
    )
    status_lines = "\n".join(
        f"- `{key}`: {value}" for key, value in sorted(state["proof_status_counts"].items())
    )
    refs = "\n".join(f"- {key}: {value}" for key, value in state["references"].items())
    return "\n".join([
        "# ASTIS Blueprint Control State",
        "",
        f"- Task: `{state['task_id']}`",
        f"- Generated: `{state['generated']}`",
        f"- Latest cycle: `{state['latest_cycle']}`",
        f"- Stage: {state['stage']}",
        "",
        "## System Of Record",
        "",
        record,
        "",
        "## Dynamic Leaf Candidate",
        "",
        state["dynamic_leaf_candidate"],
        "",
        "## Illness Area Candidate",
        "",
        state["illness_area_candidate"],
        "",
        "## Latest Blocker",
        "",
        state["latest_blocker"],
        "",
        "## Recent Packet Classifications",
        "",
        class_lines,
        "",
        "## Proof Status Counts",
        "",
        status_lines,
        "",
        "## LeanMarathon Controls Absorbed",
        "",
        controls,
        "",
        "## ASTIS Advantages Preserved",
        "",
        kept,
        "",
        "## References",
        "",
        refs,
        "",
        "## Next-Cycle Discipline",
        "",
        "- Upper must select either the dynamic leaf candidate or a named refiner illness area.",
        "- Middle must translate only that local region into lower-ready Lean declarations.",
        "- Lower must work inside that local target/refinement region before asking for upstream changes.",
        "- Reviewer treats `python3 tools/astis.py check` as the deterministic merge/progress gate and rejects broad replay.",
    ]) + "\n"


def write_blueprint_status(task_id: str, output: Path | None = None) -> tuple[Path, Path]:
    state = blueprint_control_state(task_id)
    base = output or BLUEPRINT_DIR / f"{slugify(task_id)}-blueprint-status.md"
    md_path = base if base.suffix == ".md" else base.with_suffix(".md")
    json_path = md_path.with_suffix(".json")
    legacy_md = LEGACY_BLUEPRINT_DIR / md_path.name if md_path.parent == BLUEPRINT_DIR else None
    legacy_json = LEGACY_BLUEPRINT_DIR / json_path.name if json_path.parent == BLUEPRINT_DIR else None
    write_text_mirror(md_path, blueprint_status_text(state), [legacy_md] if legacy_md else [])
    write_text_mirror(
        json_path,
        json.dumps(state, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        [legacy_json] if legacy_json else [],
    )
    add_manifest("astis.py blueprint-status", md_path, "blueprint", f"Wrote blueprint control state for {task_id}")
    return md_path, json_path


def compact_file_lines(path: Path, patterns: list[str], limit: int = 24) -> list[str]:
    if not path.exists():
        return []
    regexes = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    rows = []
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if stripped and any(regex.search(stripped) for regex in regexes):
            rows.append(compact_inline_text(stripped, max_chars=360))
    return rows[-limit:]


def task_relevant_lean_declarations(task_id: str, limit: int = 60) -> list[dict]:
    if task_id == "ASTIS-SALD-001":
        files = [
            ROOT / "AutoSamplingTheory" / "SALD.lean",
            ROOT / "AutoSamplingTheory" / "SDE.lean",
            ROOT / "AutoSamplingTheory" / "Probability.lean",
            ROOT / "AutoSamplingTheory" / "Core.lean",
        ]
    elif task_id == "ASTIS-RMFLD-001":
        files = [
            ROOT / "AutoSamplingTheory" / "RMFLD.lean",
            ROOT / "AutoSamplingTheory" / "SDE.lean",
            ROOT / "AutoSamplingTheory" / "Probability.lean",
            ROOT / "AutoSamplingTheory" / "Core.lean",
        ]
    else:
        files = lean_source_files()
    rows = []
    for path in files:
        if not path.exists():
            continue
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            match = LEAN_DECL_NAME_REGEX.match(line)
            if not match:
                continue
            rows.append({
                "kind": match.group(1),
                "name": match.group(2),
                "file": f"{rel(path)}:{lineno}",
            })
    return rows[-limit:]


def blueprint_refresh_text(task_id: str) -> str:
    title, task_text = task_context(task_id)
    state = blueprint_control_state(task_id)
    status_md = BLUEPRINT_DIR / f"{slugify(task_id)}-blueprint-status.md"
    obligation_path = ROOT / "proof-obligations" / f"{task_id}.md"
    conversion_path = ROOT / "conversion-windows" / f"{task_id}.md"
    if task_id == "ASTIS-SALD-001":
        source_index_path = ROOT / "research-wiki" / "source-index" / "SALD_original.jsonl"
    elif task_id == "ASTIS-CHEWI-001":
        source_index_path = ROOT / "research-wiki" / "retrieval-index" / "ASTIS-CHEWI-001.json"
    else:
        source_index_path = ROOT / "research-wiki" / "source-index" / "RMFLD_paper.jsonl"
    if task_id == "ASTIS-CHEWI-001":
        gate_policy = "\n".join([
            "- Textbook mode may not silently strengthen a mathematical statement to close Lean.",
            "- Chapter summaries, shared-root DAGs, module cards, and retrieval indexes must stay synchronized.",
            "- Algorithm chapters are consumers until their shared analytic roots compile locally.",
            "- Lower workers compile one Mathlib-ready ASTIS-owned leaf or return one strictly smaller source-cited blocker.",
            "- Reviewer accepts progress only through `python3 tools/astis.py check`, a precise proof obligation, a concrete port plan, or explicit rejection of an unsupported statement.",
        ])
        extra_sections = f"""
## Library And Run Entry Points

- Library overview: `{rel(LOG_CONCAVE_OVERVIEW_MD)}`
- Master chapter/theorem DAG: `{rel(LOG_CONCAVE_FOUNDATION_DAG_MD)}`
- Blue/red status tree: `{rel(LOG_CONCAVE_STATUS_SVG)}`
- Six-hour execution pack: `{rel(LOG_CONCAVE_EXECUTION_PACK_MD)}`
- Launcher: `python3 tools/astis.py launch-log-concave-6h --hours 6 --wall-hours 24 --lower-count 3`
"""
    else:
        gate_policy = "\n".join([
            "- Faithful paper mode may not weaken the SALD statement to close a Lean goal.",
            "- Stage 1 target/source review remains active when notation or hypotheses move.",
            "- Stage 2 proof discharge assigns lower workers to dynamic leaves only.",
            "- Refiner work should repair one connected illness area instead of stacking unrelated wrapper lemmas.",
            "- Lean plus explicit source correspondence is the gate; agent self-assessment is not proof progress.",
        ])
        extra_sections = ""
    directive = "\n".join([
        f"Mode: `{task_id}` follows `{state['stage']}`.",
        f"Current dynamic leaf: {state['dynamic_leaf_candidate']}",
        f"Current illness area: {state['illness_area_candidate']}",
        "Upper/middle must retire stale leaves before assigning lower work.",
        "Lower work should be one local Lean declaration/proof boundary at a time.",
        "Reviewer accepts progress only through `python3 tools/astis.py check` plus source correspondence.",
    ])
    handoffs = latest_handoff_notes(task_id, limit=8)
    leaves = [
        state["dynamic_leaf_candidate"],
        state["illness_area_candidate"],
        *handoffs,
    ]
    seen_leaves = []
    for leaf in leaves:
        clean = compact_inline_text(str(leaf), max_chars=520)
        if clean and clean not in seen_leaves:
            seen_leaves.append(clean)
    obligation_rows = compact_file_lines(
        obligation_path,
        [
            r"obligation",
            r"unproved",
            r"source",
            r"conditional",
            r"Bochner",
            r"set-integral",
            r"hbarB",
            r"barB",
        ],
        limit=28,
    )
    artifact_candidates = [
        ROOT / item for item in state["system_of_record"]
    ] + [
        status_md,
        conversion_path,
        obligation_path,
        source_index_path,
        ROOT / "paper-notes" / "AutoLeanInSleepSampling" / "markdown" / "status.md",
        ROOT / "paper-notes" / "AutoLeanInSleepSampling" / "latex" / "sections" / "00_overview.tex",
        ROOT / "docs" / "leanmarathon_reference_notes.md",
        ROOT / "docs" / "self_reflection_and_efficiency.md",
    ]
    artifacts = []
    for path in artifact_candidates:
        if path.exists() and path not in artifacts:
            artifacts.append(path)
    class_lines = "\n".join(
        f"- `{key}`: {value}" for key, value in state["trial_classifications_recent"].items()
    )
    status_lines = "\n".join(
        f"- `{key}`: {value}" for key, value in sorted(state["proof_status_counts"].items())
    )
    leaf_rows = "\n".join(f"| {leaf.replace('|', '/')} | candidate |" for leaf in seen_leaves)
    if not leaf_rows:
        leaf_rows = "| none detected | upper must refresh the task directive |"
    obligation_text = "\n".join(obligation_rows) if obligation_rows else "no compact obligation signals found"
    declaration_rows = "\n".join(
        f"| {row['kind']} | `{row['name']}` | `{row['file']}` |"
        for row in task_relevant_lean_declarations(task_id)
    )
    if not declaration_rows:
        declaration_rows = "| none | no task-relevant declaration found | n/a |"
    artifact_rows = "\n".join(f"| `{rel(path)}` | correspondence/system-of-record |" for path in artifacts)
    source_excerpt = compact_inline_text(task_text, max_chars=1200)
    return f"""# ASTIS Proof Blueprint: {task_id}

Task id: `{task_id}`
Title: {title}
Updated: `{now_stamp()}`
Blueprint stage: `{state['stage']}`

This is ASTIS's compact system-of-record snapshot for long-horizon Lean proof
automation.  It follows the LeanMarathon/QBE blueprint lesson, but the
correspondence surface is SDE/Sampling-specific: Lean declarations,
source-paper labels, proof obligations, ASTIS technical lemma memory,
SLT/SDE cited-result port audits, and
Lean-Markdown-LaTeX exports must stay synchronized.

## Current Directive

```text
{directive}
```

## Dynamic Leaf Queue

Lower agents should work on one item at a time.  If a leaf is stale, upper or
middle must retire it before spending more proof-search tokens.

| Leaf | Status |
|---|---|
{leaf_rows}

## Open Obligation Signals

```text
{obligation_text}
```

## Recent Packet Classifications

{class_lines}

## Proof Status Counts

{status_lines}

## Lean Declaration Index

| Kind | Lean name | File |
|---|---|---|
{declaration_rows}

## Correspondence Artifacts

| Artifact | Role |
|---|---|
{artifact_rows}

## Source Contract Excerpt

```text
{source_excerpt}
```

## Gate Policy

{gate_policy}

{extra_sections}

## External References

- LeanMarathon: {LEANMARATHON_URL}
- LeanMarathon article: {LEANMARATHON_ARXIV_URL}
- Shared local LeanMarathon repo: `{LEANMARATHON_ROOT}`
- Shared local LeanMarathon PDF: `{LEANMARATHON_PDF}`
"""


def write_blueprint_refresh(task_id: str, output: Path | None = None) -> Path:
    write_blueprint_status(task_id)
    path = output or BLUEPRINT_DIR / f"{slugify(task_id)}.md"
    legacy_path = LEGACY_BLUEPRINT_DIR / path.name if path.parent == BLUEPRINT_DIR else None
    write_text_mirror(path, blueprint_refresh_text(task_id), [legacy_path] if legacy_path else [])
    add_manifest("astis.py blueprint-refresh", path, "blueprint", f"Refreshed proof blueprint for {task_id}")
    return path


def blueprint_context_snippet(task_id: str) -> str:
    state = blueprint_control_state(task_id)
    return "\n".join([
        f"- Stage: {state['stage']}",
        f"- Latest cycle: {state['latest_cycle']}",
        f"- Dynamic leaf candidate: {state['dynamic_leaf_candidate']}",
        f"- Illness area candidate: {state['illness_area_candidate']}",
        f"- Task blueprint: `proof-blueprints/{slugify(task_id)}.md` (legacy mirror: `research-wiki/blueprints/{slugify(task_id)}.md`).",
        "- Borrowed LeanMarathon controls: blueprint system-of-record, target review, dynamic leaves, illness-area refiner, deterministic gate.",
        "- Preserved ASTIS controls: EoH candidate populations for exploratoryProof, LBG-style trial memory, ARIS/QBE upper-middle-lower-reviewer loops, auto-research-in-sleep long run, SDE/Sampling source anchors.",
    ])


def slt_reference_pack() -> str:
    exists_note = "exists" if SLT_ROOT.exists() else "missing"
    article_note = "exists" if SLT_ARTICLE_ROOT.exists() else "missing"
    return "\n".join([
        f"- External SLT clone for audited porting only ({exists_note}): `{SLT_ROOT}`.",
        f"- External SLT paper source for exposition/provenance only ({article_note}): `{SLT_ARTICLE_ROOT}`.",
        "- Do not use the SLT clone as a runtime dependency and do not tell agents to call upstream declarations directly.",
        "- Any useful SLT theorem must become an ASTIS-owned compiled declaration under `AutoSamplingTheory/TechnicalLemmas` before it is callable.",
        "- Port status/provenance remains recorded in `research-wiki/cited-results/SLT_reuse_audit.md`.",
    ])


def technical_lemma_registry_rows() -> list[dict]:
    path = TECHNICAL_LEMMAS_DIR / "technical_lemma_registry.jsonl"
    if not path.exists():
        path = LEGACY_TECHNICAL_LEMMA_MEMORY_DIR / "technical_lemma_registry.jsonl"
    rows: list[dict] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def technical_lemma_port_queue_rows() -> list[dict]:
    path = TECHNICAL_LEMMAS_DIR / "SLT_port_queue.jsonl"
    if not path.exists():
        path = LEGACY_TECHNICAL_LEMMA_MEMORY_DIR / "SLT_port_queue.jsonl"
    rows: list[dict] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def ensure_source_index(task_id: str) -> Path:
    _, _, output = source_roots_for_task(task_id)
    records = load_jsonl(output)
    needs_refresh = not output.exists() or any(
        "line_start" not in record or "line_end" not in record or "body_excerpt" not in record
        for record in records[:10]
    )
    if needs_refresh:
        cmd_source_index(argparse.Namespace(task=task_id))
    return output


def source_index_records(task_id: str) -> list[dict]:
    return load_jsonl(ensure_source_index(task_id))


def source_record_by_label(task_id: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for record in source_index_records(task_id):
        label = record.get("label", "")
        if label:
            rows[label] = record
    return rows


def source_ref_text(row: dict) -> str:
    source_file = row.get("source_file") or row.get("file") or "unknown"
    start = row.get("line_start") or row.get("line")
    end = row.get("line_end") or start
    if start is None:
        return f"{source_file}:line-range-missing"
    if end and int(end) != int(start):
        return f"{source_file}:{start}-{end}"
    return f"{source_file}:{start}"


def sald_source_anchor(
    labels: dict[str, dict],
    label: str = "",
    source_file: str = "",
    line_start: int | None = None,
    line_end: int | None = None,
) -> dict:
    if label and label in labels:
        record = labels[label]
        start = record.get("line_start", record.get("line"))
        end = record.get("line_end", start)
        return {
            "source_label": label,
            "source_file": record.get("file", source_file),
            "line_start": start,
            "line_end": end,
            "body_excerpt": record.get("body_excerpt", record.get("snippet", "")),
            "line_range_status": "precise",
        }
    status = "precise" if source_file and line_start is not None else "line-range-missing"
    return {
        "source_label": label,
        "source_file": source_file or "line-range-missing",
        "line_start": line_start,
        "line_end": line_end if line_end is not None else line_start,
        "body_excerpt": "",
        "line_range_status": status,
    }


def sald_unfinished_source_items() -> list[dict]:
    labels = source_record_by_label("ASTIS-SALD-001")
    specs = [
        {
            "id": "discrete-forward-kl-main",
            "kind": "paper-contribution",
            "label": "thm:forward-KL-discrete",
            "lean_boundary": "SALD.discreteForwardKlProofDag / thm:forward-KL-discrete contract",
            "human_meaning": "Discrete VA-SALD Euler--Maruyama forward-KL theorem statement and proof route.",
            "status": "source-indexed; analytic backend open",
            "next_action": "Keep theorem contract fixed; discharge the EM weak-FP and Brownian/Ito generator leaves below.",
        },
        {
            "id": "unified-forward-kl-main",
            "kind": "paper-contribution",
            "label": "thm:unified-forward-KL",
            "lean_boundary": "SALD.unifiedForwardKlContract",
            "human_meaning": "Unified guided VA-SALD theorem that depends on the general moving-target theorem.",
            "status": "source-indexed; depends on general theorem closure",
            "next_action": "Do not mutate the statement; backfill shared KL/FI/LSI and moving-target interfaces.",
        },
        {
            "id": "frozen-em-interpolation",
            "kind": "paper-contribution",
            "label": "eq:general_moving_target_SALD_frozen_interp",
            "lean_boundary": "hBrownianCoordinateGeneratorTaylorIntegralDef; hRemainderGeneratorLimitDef",
            "human_meaning": "Frozen EM interpolation used to identify the Brownian/Ito scalar generator and Taylor remainder.",
            "status": "active unfinished leaf",
            "next_action": "Prove one coordinate generator equality or narrow it to a single Taylor/Ito source obligation.",
        },
        {
            "id": "conditional-drift-definition",
            "kind": "paper-contribution",
            "source_file": "appendix.tex",
            "line_start": 1368,
            "line_end": 1377,
            "lean_boundary": "conditional drift representative and law integral fields",
            "human_meaning": "The conditional drift \\bar b_{k,s} and conditional-law representative used by the weak FP equation.",
            "status": "source-line mapped; representative/measurability leaves open",
            "next_action": "Close or strictly narrow conditional expectation representative and integrability hypotheses.",
        },
        {
            "id": "weak-fokker-planck-line",
            "kind": "paper-contribution",
            "source_file": "appendix.tex",
            "line_start": 1379,
            "line_end": 1387,
            "lean_boundary": "sald.general_moving_target_discrete.em_interpolation_fp",
            "human_meaning": "Weak Fokker--Planck equation for the EM interpolation law.",
            "status": "core unfinished analytic backend",
            "next_action": "Prove/narrow generator-to-law weak action with the selected test function and Brownian term.",
        },
        {
            "id": "kl-derivative-start",
            "kind": "paper-contribution",
            "label": "eq:general_KL_derivative_0_discrete",
            "lean_boundary": "KL derivative handoff for hat rho_s versus pi_s",
            "human_meaning": "First derivative of the KL along the discrete moving-target law.",
            "status": "source-indexed; depends on weak-FP and admissible log-ratio test",
            "next_action": "Connect the weak-FP identity to the KL derivative only after the law-level backend is stable.",
        },
        {
            "id": "divergence-fi-ibp",
            "kind": "paper-contribution",
            "label": "eq:general_KL_derivative_1_discrete",
            "lean_boundary": "divergence rewrite, FI term, and no-boundary IBP",
            "human_meaning": "Divergence/Laplacian rewrite producing the Fisher-information term and residual pairing.",
            "status": "source-indexed; Green/trace and integration-by-parts leaves open",
            "next_action": "Use local measure/variational technical lemmas first; queue missing Green/trace facts explicitly.",
        },
        {
            "id": "selected-source-hessian-fields",
            "kind": "paper-contribution",
            "source_file": "appendix.tex",
            "line_start": 982,
            "line_end": 995,
            "lean_boundary": "hSourceHasHessian; hSourceHessianBound",
            "human_meaning": "Selected weak-test Hessian regularity required by the Brownian/Ito Taylor expansion.",
            "status": "source-contract gap; do not fake via wrapper assumptions",
            "next_action": "Either locate the exact source regularity assumption or leave a precise ProofObligation.",
        },
        {
            "id": "taylor-dct-technical-backend",
            "kind": "technical-lemma",
            "source_file": "appendix.tex",
            "line_start": 982,
            "line_end": 995,
            "lean_boundary": "hRemainderMeas; hRemainderBound; hRemainderBoundInt",
            "human_meaning": "Taylor remainder measurability, domination, integrability, and Gaussian moment/limit facts.",
            "status": "technical lemma port/proof queue",
            "next_action": "Port or prove ASTIS-owned local lemmas before calling them from SALD proof code.",
        },
    ]
    items = []
    for spec in specs:
        anchor = sald_source_anchor(
            labels,
            label=spec.get("label", ""),
            source_file=spec.get("source_file", ""),
            line_start=spec.get("line_start"),
            line_end=spec.get("line_end"),
        )
        item = {**spec, **anchor}
        item["source_ref"] = source_ref_text(item)
        if item.get("line_range_status") != "precise":
            item["status"] = f"{item.get('status', '')}; line-range-missing".strip("; ")
        items.append(item)
    return items


def unfinished_source_markdown_table(items: list[dict] | None = None) -> str:
    rows = items or sald_unfinished_source_items()
    body = "\n".join(
        "| `{id}` | {kind} | `{source_ref}` | `{lean_boundary}` | {status} | {next_action} |".format(
            id=row.get("id", ""),
            kind=row.get("kind", ""),
            source_ref=row.get("source_ref", "line-range-missing"),
            lean_boundary=row.get("lean_boundary", ""),
            status=row.get("status", ""),
            next_action=row.get("next_action", ""),
        )
        for row in rows
    )
    return body or "| none | none | none | none | none | none |"


def technical_lemma_status_markdown() -> str:
    registry_rows = technical_lemma_registry_rows()
    formalized_rows = [row for row in registry_rows if row.get("status") == "formalized-local"]
    port_rows = [row for row in registry_rows if row.get("status") != "formalized-local"]
    port_rows.extend(technical_lemma_port_queue_rows())
    formalized_table = "\n".join(
        f"| `{row.get('local_decl', '')}` | {', '.join(row.get('tags', []))} | {row.get('sald_use', '')} | `{row.get('local_file', '')}` |"
        for row in formalized_rows
    ) or "| none | none | none | none |"
    port_table = "\n".join(
        f"| `{row.get('upstream_file', '')}` | {format_decl_list(row.get('upstream_declarations', row.get('upstream_decl', '')))} | {row.get('astis_target', row.get('sald_use', row.get('target_local_module', '')))} | {row.get('status', '')} |"
        for row in port_rows
    ) or "| none | none | none | none |"
    return f"""## Formalized Local Technical Lemmas

| Local declaration | Tags | SALD use | File |
|---|---|---|---|
{formalized_table}

## Technical Lemma Port Queue

| Source / upstream | Declarations | ASTIS target | Status |
|---|---|---|---|
{port_table}
"""


def mathlib_ready_leaf_protocol_text() -> str:
    return f"""# Mathlib-Ready Leaf Lemma Protocol

ASTIS treats every reusable SDE/Sampling background result as a possible future
Mathlib contribution.  The immediate rule is more modest: before a lemma is
called by a SALD or RMFLD proof, it must be an ASTIS-owned Lean declaration
that builds locally, or it must be recorded as an explicit proof obligation.

Reference target: {MATHLIB_URL}

## Core Rule

One lower-agent packet should target one small theorem.  The packet must fit in
one agent context window and must include more than the theorem statement:

- proposed declaration name and namespace;
- existing local APIs and Mathlib declarations to try first;
- minimal imports;
- hidden regularity contracts;
- intended proof route in at most seven steps;
- source anchor or upstream theorem reference;
- failure policy.

The lower agent should not repeatedly redesign the statement.  If the same
target fails two or three times for the same reason, treat that as a
mathematical signal: look for a missing assumption, a false statement, a
wrong representative, a typeclass mismatch, or a counterexample.

## Mathlib-Ready Shape

A leaf is Mathlib-ready when it has these properties.

| Check | Required behavior |
|---|---|
| Generality | State the reusable mathematical fact, not a SALD-specific wrapper. |
| Minimal assumptions | Expose only the regularity actually used by the proof. |
| Local API | Reuse existing Mathlib names before inventing ASTIS names. |
| Naming | Prefer descriptive names that would still make sense outside SALD. |
| Proof route | Keep one stable proof route unless reviewer identifies a real statement issue. |
| Import discipline | Use the smallest reasonable imports and avoid hidden project dependencies. |
| Callability | Status becomes callable only after `lake build` covers the declaration. |

SALD-specific theorem boundaries still belong in paper-contribution memory.
Only reusable facts such as law-map integrals, dominated derivative transfer,
conditional-kernel pairings, KL/FI algebra, weak Fokker--Planck statements,
Gaussian moments, Ito/Taylor remainders, and integration-by-parts identities
belong in technical lemma memory.

## Hidden Regularity Contracts

Paper prose often hides assumptions behind phrases such as "standard",
"smooth", "by Fokker--Planck", or "by integration by parts".  In Lean these
must be explicit contracts.  Common contracts include:

- measurability or `AEStronglyMeasurable`;
- integrability or domination for exchanging limits and integrals;
- finite measure, probability measure, sigma-finiteness, or nonempty space;
- continuity, differentiability, `ContDiff`, bounded Hessian, or compact
  support;
- positivity or nonzero density hypotheses for logarithms and KL terms;
- no-boundary, compact-support, or decay assumptions for integration by parts;
- a fixed conditional-distribution representative when conditional laws are
  used.

When a hidden regularity fact is needed in more than one proof, promote it to
`AutoSamplingTheory/TechnicalLemmas/*` and register it under
`research-wiki/technical-lemmas/`.

## Local Mathlib Search Discipline

Before writing a new technical lemma, middle and lower agents should search
the local Mathlib checkout and ASTIS memory:

```bash
rg -n "condDistrib|map.*integral|HasDerivAt|Kullback|Fisher|Gaussian" .lake/packages/mathlib/Mathlib AutoSamplingTheory
rg -n "theorem|lemma" AutoSamplingTheory/TechnicalLemmas research-wiki/technical-lemmas
```

If Mathlib already has the theorem, the ASTIS leaf should be a thin usage
proof or notation bridge.  If Mathlib has only nearby infrastructure, the
ASTIS leaf should be written in a way that could later be upstreamed.
"""


def technical_lemmas_readme_text() -> str:
    return """# Technical Lemmas

Canonical memory for reusable Sampling/SDE background facts: KL/FI/LSI, weak
Fokker--Planck, Ito/Taylor, Gaussian moments, measurability, integrability,
conditional laws, law-map rewrites, and integration-by-parts tools.

This folder is the skill memory for lower agents.  A lemma is callable only
when it is ASTIS-owned Lean code and the local gate covers it.  External Lean
projects such as lean-stat-learning-theory, lean-rademacher, MathCode, and
LeanMarathon are references or port sources; they are not silently treated as
local proofs.

## Memory Split

| Layer | What goes here | What does not go here |
|---|---|---|
| Technical lemma memory | General SDE/Sampling facts that can be reused across papers. | SALD-specific theorem statements or paper-only constants. |
| Paper contribution memory | A paper's own theorem leaves, source lines, and exact proof route. | Generic measure-theory, probability, or analysis facts. |
| Port queue | External declarations that look useful but are not yet ASTIS-owned. | Claims marked callable before they compile locally. |

## Required Leaf Packet

Every new reusable lemma should be accompanied by the template in
`mathlib_ready_leaf_template.md`.  The packet must name local APIs, intended
proof route, hidden regularity contracts, and failure policy.

## DAG Entry Points

- `research-wiki/lemma-dags/SDE_Sampling_skill_tree.md` gives the reusable
  skill tree.
- `research-wiki/lemma-dags/SALD_weak_fp_leaf_dag.md` gives the current SALD
  weak-Fokker--Planck leaf DAG and next lower-agent priorities.
- `hidden_regularities.md` lists reusable regularity contracts that should be
  pulled out of paper prose and made explicit.
"""


def mathlib_ready_leaf_template_text() -> str:
    return """# Mathlib-Ready Leaf Template

Copy this template for every reusable technical lemma target.  Keep it short:
the goal is a packet that one lower agent can execute without rereading the
whole paper or long run history.

## Leaf

- Leaf id:
- Proposed Lean name:
- Proposed namespace:
- Target file:
- Status: `candidate`, `in-progress`, `formalized-local`, `port-queue`, or
  `blocked-by-statement`.

## Mathematical Statement

Write the statement in ordinary mathematics in one paragraph.  State whether
it is domain-general enough to become a Mathlib contribution or should remain
ASTIS-local.

## Local APIs To Try First

- ASTIS declarations:
- Mathlib files/declarations:
- External reference projects:

## Hidden Regularity Contracts

List the exact assumptions required by the proof:

- measurability:
- integrability/domination:
- differentiability/smoothness:
- boundedness/compact support/decay:
- measure assumptions:
- conditional-distribution representative:
- positivity/nonzero assumptions:

## Intended Proof Route

1. 
2. 
3. 

Stop at seven steps.  If more steps are needed, decompose the target.

## Failure Policy

If the same proof route fails two or three times, do not keep editing the
proof script.  Record the failure as one of:

- missing assumption;
- false statement or counterexample risk;
- wrong representative or definitional mismatch;
- Mathlib API mismatch;
- target too large and must be split.

## Reviewer Checklist

- Builds locally.
- No fake proof closure.
- Statement is smaller than the parent theorem.
- No broad same-shape wrapper.
- Hidden regularity is explicit.
- Source/upstream reference is recorded.
"""


def mathlib_leaf_reviewer_checklist_text() -> str:
    return """# Mathlib-Ready Leaf Reviewer Checklist

Reviewer agents use this checklist before marking a reusable SDE/Sampling leaf
as `formalized-local` or a plausible future Mathlib contribution.  The goal is
not only to make the current paper compile; the goal is a small, stable,
searchable theorem that later papers can call.

## Gate 1: Stable Statement

- The theorem is one leaf, not a bundled paper proof.
- The statement is domain-general unless a local ASTIS namespace is explicitly
  justified.
- All hidden regularity assumptions are explicit: measurability, integrability,
  domination, differentiability, boundedness, nonemptiness, positivity,
  compact support or boundary decay, and conditional representatives.
- Constants and conventions are named rather than buried in prose.
- The statement has not been repeatedly rewritten just to satisfy the current
  proof script.  Persistent failure triggers a statement audit.

## Gate 2: API And File Placement

- The file path matches the mathematical family: `Probability`,
  `ProbabilityDistributions`, `Analysis/Calculus`, `InformationTheory`, or
  `FunctionalInequalities`.
- Existing Mathlib declarations were searched first.
- External projects such as `lean-stat-learning-theory` or `lean-rademacher`
  are cited as port/reference memory, not treated as local proof certificates.
- Imports are the smallest reasonable imports for the family.
- The theorem name would still make sense outside SALD/RMFLD.

## Gate 3: Proof Quality

- The proof route is stable and described in the leaf packet.
- No `axiom`, `sorry`, `admit`, fake `Prop := True`, or fake `trivial` closure.
- No broad wrapper that merely repackages the parent theorem.
- If the proof depends on a large theorem, that theorem is either a compiled
  local declaration or a named proof obligation.
- The declaration is covered by `lake build` and `lake build Tests`.

## Gate 4: Retrieval And Memory

- The leaf is recorded in `AutoSamplingTheory/TechnicalLemmas/Registry.lean`
  if it is meant to be callable memory.
- The technical-lemma registry, retrieval index, module graph, and card are
  refreshed.
- The external source is recorded under `research-wiki/external-lean-libraries/`
  or the port queue.

Reviewer outcome should be one of:

- `accept-mathlib-ready-local`: compiled, small, reusable, and correctly placed;
- `accept-astis-local`: compiled but intentionally project-local;
- `split-required`: target too large for one lower agent;
- `regularity-gap`: hidden assumptions missing;
- `api-search-required`: likely already in Mathlib or nearby ASTIS memory;
- `statement-risk`: possible false statement, counterexample, or wrong version.
"""


def hidden_regularities_text() -> str:
    return """# Hidden Regularity Contracts

This file turns paper prose such as "standard", "smooth", or "by dominated
convergence" into reusable theorem-contract categories.  These are not
annoying bookkeeping details; they are the assumptions that decide whether a
Lean statement is true.

| Contract | Why it matters | Typical ASTIS location |
|---|---|---|
| Measurability | Needed before integrals, kernels, conditional expectations, and laws are well-typed. | `AutoSamplingTheory/TechnicalLemmas/Measure.lean` |
| Integrability | Needed before Bochner integrals, KL/FI terms, and limits under integrals are legal. | `Measure.lean`, `Variational.lean` |
| Domination | Needed for dominated convergence and parametric integral differentiation. | `Measure.lean` |
| Smoothness | Needed for Ito/Taylor generator and Hessian remainder statements. | `Analysis/Calculus/Taylor.lean`, SDE leaf files |
| Bounded Hessian | Needed for one-step Taylor remainders and EM weak-error bounds. | `Analysis/Calculus/Taylor.lean` |
| Compact support or decay | Needed to erase boundary terms in integration by parts. | future `IBP.lean` |
| Probability/finite measure | Needed for law-map, conditional law, and entropy statements. | `Measure.lean` |
| Conditional representative | Needed because conditional laws are only defined up to a.e. equality. | `Measure.lean`, `SDE.lean` |
| Positivity/nonzero density | Needed for log, KL, score, and Fisher-information algebra. | `Variational.lean` |
| Time regularity | Needed for differentiating time-indexed laws and weak-test integrals. | future `WeakFP.lean` |

Reviewer rule: if a lower proof succeeds only by assuming one of these
contracts informally, the result is not complete.  Either add the contract to
the statement, prove it from existing hypotheses, or record a source-cited
proof obligation.
"""


def sde_sampling_skill_tree_text() -> str:
    return """# SDE/Sampling Technical Lemma Skill Tree

This is the reusable lemma network ASTIS should grow beyond SALD.  The aim is
not only to reproduce one paper, but to build a Mathlib-ready path for common
Sampling/SDE proof blocks.

```mermaid
flowchart LR
  M[Mathlib foundations]
  Search[Mathlib search and API scout]
  Measure[Measure and law-map rewrites]
  Kernel[Conditional laws and kernels]
  Deriv[Parametric integral and law derivatives]
  Ito[Ito generator and weak FP]
  Taylor[Ito/Taylor local error]
  Gaussian[Gaussian and Brownian moments]
  KL[KL/FI/log-density algebra]
  LSI[LSI/DV/Gronwall chains]
  IBP[Integration by parts and boundary contracts]
  SALD[SALD faithful proof DAG]
  RMFLD[RMFLD exploratory DAG]

  M --> Search
  Search --> Measure
  Search --> Kernel
  Search --> Gaussian
  Measure --> Deriv
  Kernel --> Ito
  Deriv --> Ito
  Gaussian --> Taylor
  Taylor --> Ito
  KL --> LSI
  IBP --> KL
  Ito --> SALD
  LSI --> SALD
  Ito --> RMFLD
  KL --> RMFLD
```

## Skill Blocks

| Block | Typical leaf size | Mathlib-ready target |
|---|---|---|
| Mathlib search | One API packet. | Find existing lemma before porting. |
| Measure/law map | One rewrite theorem. | Integral of a test function under a map/law. |
| Conditional laws | One pairing identity. | `condDistrib` kernel pairing, then optional conditional-mean form. |
| Parametric integral | One derivative transfer. | Move sample-space derivative to law-level weak-test derivative under domination. |
| Ito/weak FP | One weak-test identity. | Derive law-level weak FP from a source-cited Ito generator theorem plus law rewrites. |
| Ito/Taylor | One local expansion or bound. | Backup Gaussian one-step generator, covariance trace, or Taylor remainder bound. |
| KL/FI | One algebraic derivative/integrability fact. | KL pointwise derivative, mass-term removal, or Fisher-information rewrite. |
| LSI/DV/Gronwall | One inequality handoff. | Donsker--Varadhan, LSI-to-KL/FI, or scalar Gronwall block. |
| IBP | One boundary contract plus identity. | Integration-by-parts identity with explicit decay/compact support. |

## Current Pro-Assimilated Leaf Families

These are the concrete leaf families extracted from the external proof-engineering
advice packet.

| Family | First leaf | Keep source-cited? | Why |
|---|---|---|---|
| Conditional pairing/versioning | `condDistribIntegralNamedFieldIntegral` | formalized-local | Directly proved from `condDistrib`, named-law integral, and `integral_congr_ae`. |
| Conditional mean | `condDrift_pairing_of_condMean` | no | Use Bochner integral and continuous linear maps after the kernel form. |
| Weak-generator bridge | `weakGeneratorFromSampleDerivative` | formalized-local | Small rewriting theorem once Ito derivative, law identity, and generator pairings are supplied. |
| Frozen Ito generator | `frozen_interpolation_ito_generator_derivative` | yes, initially | This is the analytic Ito theorem; isolate and cite until a local SDE library exists. |
| KL density derivative | `hasDerivAt_KLDens` | yes/local structure | Requires local dominated derivative structure; prove pointwise algebra separately. |
| KL algebra | `klPointwiseDerivSimplify`, `klDerivativeRemoveMassTerm` | formalized-local | Small real algebra and derivative-target leaves. |
| IBP theorem | `integral_div_smul_eq_neg_integral_inner_grad` | yes, initially | Whole-space boundary conditions are substantial; use explicit compact-support/decay contract. |
| Fisher/FP algebra | `fpRewriteScalarAlgebra`, `fisherIbpAlgebra` | formalized-local | Small algebra once analytic FP/IBP identities are supplied. |
| Gaussian fallback | `covariance_contracts_bilinear_form`, `frozen_gaussian_one_step_generator` | maybe | Backup route if Ito generator source theorem is not usable. |

## Agent Routing

- `upper_proof_dag` chooses which skill block is the true bottleneck.
- `middle_technical_lemma` searches Mathlib and ASTIS memory before assigning
  lower work.
- `lower_1` writes the natural-language proof and hidden regularity list.
- `lower_2` implements the smallest Lean theorem.
- `lower_3` searches APIs and external reference projects.
- `reviewer_gate` rejects broad wrappers and missing regularity.
"""


def sald_weak_fp_leaf_dag_text() -> str:
    return """# SALD Weak-Fokker--Planck Leaf DAG

This graph records the current reusable technical-lemma route for the SALD
Euler--Maruyama interpolation / conditional weak Fokker--Planck backend.  It
is deliberately smaller than the whole SALD proof.  The purpose is to stop
lower agents from replaying broad SALD routes when one weak-test bridge is the
real blocker.

```mermaid
flowchart TD
  Root[emInterpolationConditionalWeakFp]
  Bridge[weakGeneratorFromSampleDerivative compiled]
  ItoGen[frozen_interpolation_ito_generator_derivative]
  LawDeriv[law-level weak-test derivative rewrite]
  PairKernel[condDistribIntegralNamedFieldIntegral compiled]
  PairMean[condDrift_pairing_of_condMean]
  LapLaw[laplacian law-map rewrite]
  Reg[hidden regularity contracts]
  KL[KL/FI downstream handoff]
  KLPt[klPointwiseDerivSimplify compiled]
  KLMass[klDerivativeRemoveMassTerm compiled]
  IBP[integral_div_smul_eq_neg_integral_inner_grad]
  Fisher[fisherIbpAlgebra compiled]
  SALD[SALD discrete moving-target theorem]
  Fallback[Brownian Taylor/DCT fallback]
  Cov[covariance_contracts_bilinear_form]
  GaussGen[frozen_gaussian_one_step_generator]

  SALD --> Root
  Root --> Bridge
  Bridge --> ItoGen
  Bridge --> LawDeriv
  Bridge --> PairKernel
  PairKernel --> PairMean
  Bridge --> LapLaw
  Bridge --> Reg
  Root --> KL
  KL --> KLPt
  KL --> KLMass
  KL --> IBP
  IBP --> Fisher
  Fallback -. use only if Ito route is false .-> Cov
  Cov --> GaussGen
  GaussGen -. backup generator .-> ItoGen
```

## Current Leaf Priorities

| Priority | Leaf | Status | Route |
|---|---|---|---|
| 1 | `condDistribIntegralNamedFieldIntegral` | formalized-local | Use named-law conditional integral and a.e. versioning; avoid vector conditional mean unless needed. |
| 2 | `weakGeneratorFromSampleDerivative` | formalized-local | Rewrite sample-space Ito derivative into law-level weak-generator form using law identity and supplied pairings. |
| 3 | `condDrift_pairing_of_condMean` | technical lemma after priority 1 | Pull inner product through Bochner integral with a continuous linear map. |
| 4 | `lawIntegralHasDerivAtOfMeasureMapEqAndSample` | formalized-local backend | Existing law-map derivative rewrite consumed by `weakGeneratorFromSampleDerivative`. |
| 5 | `laplacianLawMapIntegral` | technical lemma | Rewrite law integral of Laplacian/test function under endpoint map. |
| 6 | `klPointwiseDerivSimplify` and `klDerivativeRemoveMassTerm` | formalized-local | KL analytic domination remains a separate contract; algebra leaves are compiled. |
| 7 | `fpRewriteScalarAlgebra` and `fisherIbpAlgebra` | formalized-local | Use after FP/IBP analytic identities are supplied. |

## Non-Goals For The Next Lower Packet

- Do not reprove the whole SALD theorem.
- Do not redo leaves now marked `formalized-local`.
- Do not add same-shape theorem wrappers.
- Do not switch back to Brownian Taylor/DCT unless the Ito-generator bridge is
  shown false or missing a necessary assumption.
- Do not mark external SLT or Mathlib-inspired facts as callable until they
  are ASTIS-owned compiled declarations.

## Source-Cited Analytic Contracts

These are intentionally isolated.  They can become future local SDE library
theorems, but they should not block the directly provable measure-rewrite and
algebra leaves.

| Contract | Why source-cited first |
|---|---|
| `frozen_interpolation_ito_generator_derivative` | Finite-dimensional Ito formula plus martingale expectation zero is real stochastic-analysis infrastructure. |
| `hasDerivAt_KLDens` | Requires dominated differentiation under the KL-density integral.  Pointwise algebra is small, domination is not. |
| `integral_div_smul_eq_neg_integral_inner_grad` | Whole-space no-boundary IBP needs compact-support, periodic, or decay hypotheses. |
| `taylor_second_order_remainder_bound` | High-order Frechet Taylor theorem with explicit remainder is a separate calculus block. |

## Human Reading Guide

The remaining issue is not that the VA-SALD idea is unclear.  The paper uses
standard stochastic-analysis language.  Lean needs the exact bridge from a
sample-path generator statement to a law-level weak equation, including the
conditional-law representative and regularity assumptions.  That bridge is a
reusable SDE/Sampling technical lemma, so ASTIS should grow it in technical
lemma memory and not hide it inside a SALD-specific proof block.
"""


def pro_assimilated_leaf_targets_text() -> str:
    return """# Pro-Assimilated SDE/Sampling Leaf Targets

This file compresses the external proof-engineering advice packet into ASTIS
leaf targets.  It is meant for upper and middle agents before the next 6h run.
Do not paste the long advice packet into every prompt; retrieve this compact
DAG instead.

## Main Route

```mermaid
flowchart TD
  A0[condDistribIntegralNamedLawIntegral compiled]
  A1[condDistribIntegralNamedFieldIntegral compiled]
  A2[condDrift_pairing_of_condMean future]
  B1[weakGeneratorFromSampleDerivative compiled]
  Ito[frozen_interpolation_ito_generator_derivative source-cited]
  Law[lawIntegralHasDerivAtOfMeasureMapEqAndSample compiled]
  Lap[laplacian law-map integral supplied]
  KL0[hasDerivAt_KLDens source-cited]
  KL1[klPointwiseDerivSimplify compiled]
  KL2[klDerivativeRemoveMassTerm compiled]
  IBP[integral_div_smul_eq_neg_integral_inner_grad source-cited]
  ALG1[fpRewriteScalarAlgebra compiled]
  ALG2[fisherIbpAlgebra compiled]

  A0 --> A1
  A1 --> A2
  Ito --> B1
  A1 --> B1
  Law --> B1
  Lap --> B1
  B1 --> KL0
  KL0 --> KL1
  KL1 --> KL2
  B1 --> IBP
  IBP --> ALG1
  ALG1 --> ALG2
```

## Directly Provable Lean Leaves

| Leaf | Intended shape | First search area |
|---|---|---|
| `condDistribIntegralNamedFieldIntegral` | Named conditional-integral version integrates to the original joint-law integral. | ASTIS conditional-kernel module, `integral_congr_ae`. |
| `condDrift_pairing_of_condMean` | Conditional mean version using Bochner integral and continuous linear maps. | Bochner integral continuous-linear-map APIs. |
| `weakGeneratorFromSampleDerivative` | HasDerivAt law-level weak-generator form from supplied Ito/sample derivative and pairings. | ASTIS law-map derivative rewrite. |
| `klPointwiseDerivSimplify` | Real algebra for derivative of `q * log (q / p)`. | `field_simp`, `ring`. |
| `klDerivativeRemoveMassTerm` | Remove the mass-conservation derivative term. | `simpa`, commutative additive rewrites. |
| `fpRewriteScalarAlgebra` | Rewrite `-div(q b) + a lap q` into `a div(q A) + div(q V)`. | `ring`. |
| `fisherIbpAlgebra` | Combine two IBP identities into the Fisher/cross term. | `ring`. |
| `covariance_contracts_bilinear_form` | Covariance contracts a bilinear form to the coordinate trace. | Finite sums over `Fin d`, coordinate moments. |

## Source-Cited Or Isolated Analytic Contracts

| Contract | Why it is isolated |
|---|---|
| `frozen_interpolation_ito_generator_derivative` | Requires finite-dimensional Ito formula and martingale expectation zero. |
| `hasDerivAt_KLDens` | Requires local dominated derivative structure for a parameter integral. |
| `integral_div_smul_eq_neg_integral_inner_grad` | Requires compact-support, torus, or decay/no-boundary assumptions. |
| `taylor_second_order_remainder_bound` | Requires high-order finite-dimensional Taylor theorem with explicit remainder. |
| `frozen_gaussian_one_step_generator` | Backup Markov-kernel route; useful only if the Ito route is unusable. |

## Hidden Contracts To Expose

- `State d = EuclideanSpace R (Fin d)` or an explicitly equivalent state
  type.
- Probability or finite measure assumptions on the sample space.
- Measurability/a.e. measurability of `hatX`, frozen drift `B`, tests, gradient,
  and Laplacian fields.
- Integrability of `B`, pairings, Laplacian test, and KL/FI quantities.
- Eventual law identity `hatRho s = mu.map (hatX s)` near the derivative point.
- Conditional drift representative
  `barB = ae[mu.map (hatX s0)] condMean (hatX s0) B`.
- Positivity and domination assumptions for KL density derivatives.
- Compact support, periodicity, or decay/no-boundary assumptions for IBP.

## Next-Run Directive

The next lower batch should not redo `condDistribIntegralNamedFieldIntegral`,
`weakGeneratorFromSampleDerivative`, `klPointwiseDerivSimplify`,
`klDerivativeRemoveMassTerm`, `fpRewriteScalarAlgebra`, or `fisherIbpAlgebra`;
these leaves now compile locally.  The next real targets are the conditional
mean form if it is still needed, the dominated KL-density derivative contract,
the no-boundary IBP contract, and the covariance-to-trace Gaussian fallback.
Do not send lower agents back to the whole SALD theorem, and do not ask them
to formalize the full Ito formula unless the compiled weak-generator bridge is
shown insufficient.
"""


def sampling_lemma_dag_mmd_text() -> str:
    return """flowchart LR
  M[Mathlib]
  A[ASTIS Technical Lemmas]
  P[Paper Contributions]
  R[Reviewer Gate]
  S[Source Lines]
  L[One Leaf Lemma]
  H[Hidden Regularity Contracts]
  D[Dependency DAG]
  E[Compiled Lean Declaration]

  S --> D
  D --> L
  A --> L
  M --> L
  H --> L
  L --> E
  E --> R
  R --> P
"""


def render_svg_preview(svg_path: Path, png_path: Path) -> bool:
    converter = shutil.which("convert") or shutil.which("magick")
    if not converter:
        return False
    convert_cmd = [converter, str(svg_path), str(png_path)]
    if Path(converter).name == "magick":
        convert_cmd = [converter, "convert", str(svg_path), str(png_path)]
    completed = subprocess.run(convert_cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if completed.returncode != 0:
        print(f"warning: could not render PNG preview with {converter}: {completed.stdout.strip()}")
        return False
    print(f"wrote {rel(png_path)}")
    return True


def leaf_network_style(kind: str) -> tuple[str, str, str]:
    styles = {
        "input": ("#eef4ff", "#2d5fb3", "#17335f"),
        "memory": ("#e6f4ea", "#2e7d59", "#214f3b"),
        "contract": ("#fff4d8", "#b7791f", "#6b4a13"),
        "leaf": ("#f1f7ff", "#3973b7", "#1f4e7a"),
        "analytic": ("#fdecea", "#c24135", "#7f1d1d"),
        "consumer": ("#efe7f7", "#6d4aa2", "#442465"),
        "gate": ("#f8fafc", "#64748b", "#334155"),
    }
    return styles.get(kind, ("#ffffff", "#94a3b8", "#334155"))


def leaf_network_node(node_id: str, x: int, y: int, w: int, h: int, title: str, subtitle: str, kind: str) -> str:
    fill, stroke, text = leaf_network_style(kind)
    title = html.escape(title)
    subtitle = html.escape(subtitle)
    return f"""
<g id="{html.escape(node_id)}">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" ry="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>
  <text x="{x + w / 2:.1f}" y="{y + 26}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="14" font-weight="700" fill="{text}">{title}</text>
  <text x="{x + w / 2:.1f}" y="{y + 49}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="#334155">{subtitle}</text>
</g>"""


def leaf_network_edge(
    src: tuple[int, int, int, int],
    dst: tuple[int, int, int, int],
    label: str = "",
    dashed: bool = False,
) -> str:
    sx = src[0] + src[2] / 2
    sy = src[1] + src[3]
    dx = dst[0] + dst[2] / 2
    dy = dst[1]
    mid = (sy + dy) / 2
    dash = ' stroke-dasharray="7 5"' if dashed else ""
    label_svg = ""
    if label:
        label_svg = (
            f'<text x="{(sx + dx) / 2:.1f}" y="{mid - 5:.1f}" text-anchor="middle" '
            'font-family="Helvetica,Arial,sans-serif" font-size="10" fill="#475569">'
            f"{html.escape(label)}</text>"
        )
    return (
        f'<path d="M {sx:.1f} {sy:.1f} C {sx:.1f} {mid:.1f}, {dx:.1f} {mid:.1f}, {dx:.1f} {dy:.1f}" '
        f'fill="none" stroke="#7f8da3" stroke-width="1.5"{dash} marker-end="url(#arrowLeaf)"/>'
        + label_svg
    )


def sampling_sde_leaf_network_svg() -> str:
    boxes = {
        "mathlib": (55, 90, 220, 64, "Mathlib search", "reuse before porting", "input"),
        "refs": (55, 200, 220, 64, "Reference projects", "SLT, stochastic notes, local Lean", "input"),
        "memory": (365, 90, 245, 64, "Technical lemma memory", "ASTIS-owned compiled surface", "memory"),
        "regularity": (365, 200, 245, 64, "Hidden regularity contracts", "measurable, integrable, bounded", "contract"),
        "measure": (710, 55, 245, 64, "Measure and law map", "integral_map, laws, domination", "leaf"),
        "kernel": (1010, 55, 245, 64, "Conditional laws", "condDistrib pairing leaves", "leaf"),
        "gaussian": (710, 165, 245, 64, "Gaussian/Taylor", "moments, trace, local error", "leaf"),
        "ito": (1010, 165, 245, 64, "Weak FP bridge", "Ito generator to law identity", "leaf"),
        "kl": (710, 300, 245, 64, "KL/FI algebra", "log-density and mass terms", "leaf"),
        "ibp": (1010, 300, 245, 64, "IBP/boundary", "compact support or decay contract", "analytic"),
        "lsi": (710, 430, 245, 64, "LSI/DV/Gronwall", "inequality handoff blocks", "leaf"),
        "analytic": (1010, 430, 245, 64, "Source-cited analysis", "Ito, KL derivative, no-boundary IBP", "analytic"),
        "sald": (710, 605, 245, 68, "SALD case study", "paper contribution consumer", "consumer"),
        "rmfld": (1010, 605, 245, 68, "Exploratory SDE tasks", "RMFLD and future papers", "consumer"),
        "reviewer": (365, 605, 245, 68, "Reviewer gate", "build, source, regularity, no churn", "gate"),
    }
    edges = [
        ("mathlib", "memory", "API scout", False),
        ("refs", "memory", "port queue", False),
        ("refs", "regularity", "assumptions", True),
        ("memory", "measure", "", False),
        ("memory", "kernel", "", False),
        ("memory", "gaussian", "", False),
        ("regularity", "measure", "", True),
        ("regularity", "kernel", "", True),
        ("regularity", "ito", "", True),
        ("measure", "ito", "law rewrite", False),
        ("kernel", "ito", "conditional drift", False),
        ("gaussian", "ito", "backup generator", False),
        ("ito", "kl", "weak equation", False),
        ("ibp", "kl", "Fisher term", False),
        ("kl", "lsi", "entropy chain", False),
        ("analytic", "ito", "source contract", True),
        ("analytic", "ibp", "source contract", True),
        ("lsi", "sald", "", False),
        ("ito", "sald", "", False),
        ("kl", "rmfld", "", False),
        ("ito", "rmfld", "", False),
        ("sald", "reviewer", "", False),
        ("rmfld", "reviewer", "", False),
    ]
    node_parts = [
        leaf_network_node(node_id, x, y, w, h, title, subtitle, kind)
        for node_id, (x, y, w, h, title, subtitle, kind) in boxes.items()
    ]
    edge_parts = [
        leaf_network_edge(boxes[src][:4], boxes[dst][:4], label, dashed)
        for src, dst, label, dashed in edges
    ]
    generated = html.escape(now_stamp())
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="1320" height="750" viewBox="0 0 1320 750" xmlns="http://www.w3.org/2000/svg">
<defs>
  <marker id="arrowLeaf" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
    <polygon points="0 0, 9 3.5, 0 7" fill="#7f8da3"/>
  </marker>
</defs>
<rect width="1320" height="750" fill="white"/>
<text x="660" y="34" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="24" font-weight="700" fill="#1f2933">ASTIS SDE/Sampling Leaf Lemma Network</text>
<text x="660" y="58" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#475569">Reusable technical lemmas are the library center.  SALD and RMFLD consume this arsenal instead of owning background analysis facts.</text>
<rect x="690" y="35" width="585" height="480" rx="16" ry="16" fill="none" stroke="#2e7d59" stroke-width="2" stroke-dasharray="8 5"/>
<text x="982" y="525" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="13" font-weight="700" fill="#2e7d59">Mathlib-ready leaf families</text>
<g id="edges">
{chr(10).join(edge_parts)}
</g>
<g id="nodes">
{chr(10).join(node_parts)}
</g>
<g id="legend">
  <rect x="55" y="675" width="560" height="50" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="75" y="697" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="700">Reviewer principle</text>
  <text x="75" y="717" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="#475569">One leaf lemma per packet; expose regularity; repeated failure means recheck the statement, not churn the proof.</text>
  <text x="970" y="869" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="#64748b">Generated {generated} by tools/astis.py lemma-dag-refresh</text>
</g>
</svg>
"""


def chewi_shared_root_rows() -> list[dict[str, str]]:
    return [
        {
            "label": "MEAS",
            "root": "measure-space and law transport",
            "module": "TechnicalLemmas/Probability/LawMap.lean",
            "role": "push forward laws, weak-test integrals, map/withDensity/RN bridges",
            "status": "partial-compiled-local",
        },
        {
            "label": "KERN",
            "root": "conditional kernels and representatives",
            "module": "TechnicalLemmas/Probability/ConditionalKernel.lean",
            "role": "condDistrib pairings, conditional drifts, a.e. representative discipline",
            "status": "partial-compiled-local",
        },
        {
            "label": "DENS",
            "root": "densities, RN derivative, KL/Renyi integrands",
            "module": "TechnicalLemmas/Geometry/LogConcavity.lean; Measure/{Gibbs,RadonNikodym}.lean; InformationTheory/*",
            "role": "positive density APIs, density-to-potential extraction, log-concavity algebra/tensorization, level-set quasiconcavity/restriction, linear/affine precomposition, centered/shifted/two-point quadratic and one-dimensional Laplace Gibbs log-concavity, Gibbs ENNReal density, finite-measure, exact quadratic, and exact one-dimensional Laplace Lebesgue normalization, absolute continuity, withDensity, pointwise entropy algebra",
            "status": "partial-compiled-local",
        },
        {
            "label": "GAUSS",
            "root": "Gaussian and product Gaussian infrastructure",
            "module": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "role": "standard Gaussian laws, moments, MGF, finite-dimensional tilts, shifted and two-point quadratic density geometry",
            "status": "partial-compiled-local",
        },
        {
            "label": "CONV",
            "root": "convex and log-concave geometry",
            "module": "TechnicalLemmas/Geometry/{Convex,LogConcavity,PrekopaLeindler}.lean",
            "role": "convex functions/sets, negative-log potentials, log-concave superlevels, quadratic norm potentials, log-concavity products/powers and linear/affine pullbacks, Prekopa-Leindler, Brunn-Minkowski",
            "status": "partial-compiled-local",
        },
        {
            "label": "FI",
            "root": "functional inequalities",
            "module": "TechnicalLemmas/FunctionalInequalities/*",
            "role": "PI, LSI, transport, concentration, isoperimetry, preservation",
            "status": "planned-plus-LSI-bookkeeping-compiled",
        },
        {
            "label": "SDE",
            "root": "semigroup, generator, weak-FP, Langevin",
            "module": "TechnicalLemmas/StochasticProcesses/*",
            "role": "Markov semigroups, invariant Gibbs law, generator/KL dissipation",
            "status": "partial-compiled-local",
        },
        {
            "label": "PATH",
            "root": "path-space change of measure",
            "module": "TechnicalLemmas/StochasticProcesses/{Girsanov,DoobTransform,FollmerDrift}.lean",
            "role": "Girsanov, Doob transform, Follmer drift, Schrodinger bridge",
            "status": "planned",
        },
        {
            "label": "DISC",
            "root": "algorithm discretization layer",
            "module": "SamplingAlgorithms/*",
            "role": "LMC, randomized midpoint, HMC, underdamped, MALA, proximal sampler",
            "status": "planned-consumer",
        },
        {
            "label": "REG",
            "root": "hidden regularity contracts",
            "module": "research-wiki/technical-lemmas/hidden_regularities.md",
            "role": "measurability, integrability, domination, smoothness, boundary, positivity",
            "status": "protocol",
        },
    ]


def chewi_chapter_rows() -> list[dict[str, str]]:
    return [
        {
            "chapter": "1.1 stochastic calculus",
            "shared": "MEAS, GAUSS, REG",
            "dag": "Ito/quadratic-variation/Taylor local-error subtree",
            "first_leaf": "quadratic variation normalization and finite-dimensional Ito test identity",
            "status": "partial-local-compiled",
        },
        {
            "chapter": "1.2 Markov semigroups",
            "shared": "MEAS, SDE, REG",
            "dag": "semigroup -> generator-domain -> weak-test derivative subtree",
            "first_leaf": "semigroup test-function pairing under generator-domain hypotheses",
            "status": "planned",
        },
        {
            "chapter": "1.3 optimal transport geometry",
            "shared": "MEAS, CONV, REG",
            "dag": "couplings -> Wasserstein distance -> geodesic convexity subtree",
            "first_leaf": "law-map/coupling measurable pushforward interface",
            "status": "planned",
        },
        {
            "chapter": "1.4 Langevin as gradient flow",
            "shared": "DENS, FI, SDE, REG",
            "dag": "Gibbs density -> generator -> KL/FI dissipation -> WGF contract",
            "first_leaf": "Whole-space IBP, the C_c^2 core-domain contract, normalized-Gibbs core annihilation, and the abstract semigroup/domain-to-invariance bridge compile; concrete Langevin semigroup instantiation and domain extension remain",
            "status": "abstract-semigroup-invariance-bridge-compiled",
        },
        {
            "chapter": "2 functional inequalities",
            "shared": "CONV, DENS, FI, REG",
            "dag": "PI/LSI/TI/isoperimetry plus preservation-operation subtrees",
            "first_leaf": "log-concavity products, nonnegative powers, product-domain tensorization, linear/affine precomposition, negative-log potential convexity, superlevel convexity, plus Prekopa-Leindler preservation audit",
            "status": "partial-local-compiled",
        },
        {
            "chapter": "3 stochastic analysis topics",
            "shared": "PATH, DENS, SDE, REG",
            "dag": "Girsanov -> Doob transform -> Follmer drift -> Schrodinger bridge",
            "first_leaf": "finite-dimensional Gaussian Esscher density, stdGaussian inner-product form, cylindrical Girsanov integral, and RN/withDensity identity compiled; full Brownian path packaging remains",
            "status": "finite-girsanov-rn-cylinder-compiled",
        },
        {
            "chapter": "4 Langevin Monte Carlo",
            "shared": "MEAS, KERN, SDE, DENS, REG, DISC",
            "dag": "coupling/interpolation/convex-optimization/Girsanov proof subtrees",
            "first_leaf": "LMC interpolation weak-test law derivative under domination; two-point Gaussian transition-kernel geometry compiled",
            "status": "partial-local-compiled",
        },
        {
            "chapter": "5 faster low-accuracy samplers",
            "shared": "GAUSS, SDE, DISC, REG",
            "dag": "randomized midpoint, HMC, underdamped generator subtrees",
            "first_leaf": "Hamiltonian/underdamped transition-kernel regularity contract",
            "status": "planned",
        },
        {
            "chapter": "6 Renyi divergence",
            "shared": "DENS, FI, SDE, REG",
            "dag": "Renyi density algebra -> interpolation/Girsanov derivative subtrees",
            "first_leaf": "Renyi density algebra with positivity and finite-integral contracts",
            "status": "first algebra leaves compiled",
        },
        {
            "chapter": "7 high-accuracy samplers",
            "shared": "KERN, DENS, DISC, REG",
            "dag": "rejection/MH/MALA kernels, detailed balance, warm-start subtrees",
            "first_leaf": "proposal/acceptance Markov-kernel mass and reversibility contract",
            "status": "planned",
        },
        {
            "chapter": "8 proximal sampler",
            "shared": "CONV, GAUSS, KERN, DISC, REG",
            "dag": "restricted Gaussian oracle -> conditional laws -> proximal transition subtree",
            "first_leaf": "two-point Gaussian/proximal kernel log-concavity and log-concave superlevel restriction compiled; restricted Gaussian conditional law remains",
            "status": "kernel-geometry-compiled",
        },
        {
            "chapter": "9-12 lower bounds, structure, non-log-concave, diffusion models",
            "shared": "MEAS, DENS, SDE, PATH, DISC, REG",
            "dag": "consumer subtrees after core log-concave foundation stabilizes",
            "first_leaf": "source-specific leaf only after shared roots are compiled",
            "status": "deferred-consumer",
        },
    ]


def log_concave_chapter_map_rows() -> list[dict[str, str]]:
    return [
        {
            "part": "Part I",
            "chapter": "1. Langevin diffusion in continuous time",
            "reader_summary": "The continuous-time backbone: stochastic calculus, Markov semigroups, optimal-transport geometry, Langevin dynamics, and convergence viewpoints.",
            "lean_plan": "Build Gaussian increments and generator algebra, then close the explicit cutoff -> tail -> weighted-IBP -> generator-domain -> invariant-Gibbs chain before KL/FI and Wasserstein-gradient-flow consumers.",
            "shared": "MEAS, GAUSS, DENS, FI, SDE, REG",
            "status": "partial-local-compiled",
        },
        {
            "part": "Part I",
            "chapter": "2. Functional inequalities",
            "reader_summary": "The inequality toolkit that turns geometry of the target into convergence rates: PI, LSI, transport, concentration, isoperimetry, and preservation operations.",
            "lean_plan": "Separate definitions and bookkeeping from preservation theorems; reuse log-concavity, Prekopa-Leindler/Brunn-Minkowski, and LSI/KL/FI leaves.",
            "shared": "CONV, DENS, FI, REG",
            "status": "partial-local-compiled",
        },
        {
            "part": "Part I",
            "chapter": "3. Stochastic analysis topics",
            "reader_summary": "Path-space tools used repeatedly later: quadratic variation, Girsanov change of measure, Doob transforms, Follmer drift, and Schrodinger bridges.",
            "lean_plan": "Keep finite-dimensional Gaussian change of measure as the compiled base; only then lift to Brownian/path-space RN derivatives and bridge transforms.",
            "shared": "GAUSS, PATH, DENS, SDE, REG",
            "status": "finite-girsanov-rn-cylinder-compiled",
        },
        {
            "part": "Part II",
            "chapter": "4. Analysis of Langevin Monte Carlo",
            "reader_summary": "The first algorithmic convergence chapter, presenting coupling, interpolation, convex-optimization, and Girsanov proof routes for LMC.",
            "lean_plan": "Treat LMC as a consumer of law-map, conditional-kernel, weak-FP, KL/FI, Girsanov, and Gaussian-transition geometry leaves.",
            "shared": "MEAS, KERN, SDE, DENS, PATH, DISC, REG",
            "status": "partial-local-compiled",
        },
        {
            "part": "Part II",
            "chapter": "5. Faster low-accuracy samplers",
            "reader_summary": "Randomized midpoint, Hamiltonian Monte Carlo, and underdamped Langevin methods, organized around better discretizations and dynamics.",
            "lean_plan": "Delay algorithm theorems until transition kernels, Hamiltonian/underdamped generators, and Gaussian-noise update contracts are local.",
            "shared": "GAUSS, SDE, DISC, REG",
            "status": "planned",
        },
        {
            "part": "Part II",
            "chapter": "6. Convergence in Renyi divergence",
            "reader_summary": "Stronger divergence control for LMC and underdamped methods, using interpolation and Girsanov routes.",
            "lean_plan": "Extend compiled Renyi integrand algebra toward full divergence, log-normalizer, and path-derivative contracts.",
            "shared": "DENS, FI, SDE, PATH, REG",
            "status": "first algebra leaves compiled",
        },
        {
            "part": "Part II",
            "chapter": "7. High-accuracy samplers",
            "reader_summary": "Rejection sampling, Metropolis-Hastings filters, discrete-time Markov chains, and MALA cold/warm start analyses.",
            "lean_plan": "Formalize proposal kernels, acceptance probabilities, reversibility/detailed balance, and warm-start density comparisons after kernel infrastructure is stable.",
            "shared": "KERN, DENS, GAUSS, DISC, REG",
            "status": "planned",
        },
        {
            "part": "Part II",
            "chapter": "8. Proximal sampler",
            "reader_summary": "Restricted Gaussian oracles and proximal transitions, with convergence under strong log-concavity, log-concavity, and functional inequalities.",
            "lean_plan": "Use two-point Gaussian/proximal kernel log-concavity as the compiled start; add restricted Gaussian conditional laws and time-reversal flow interfaces.",
            "shared": "CONV, GAUSS, KERN, FI, DISC, REG",
            "status": "kernel-geometry-compiled",
        },
        {
            "part": "Part II",
            "chapter": "9. Lower bounds for sampling",
            "reader_summary": "Oracle/query lower bounds in one dimension, constant dimension, and Gaussian families.",
            "lean_plan": "Treat as a consumer of oracle models, information lower bounds, Gaussian comparison, and dimension-specific construction lemmas.",
            "shared": "MEAS, GAUSS, DENS, DISC, REG",
            "status": "deferred-consumer",
        },
        {
            "part": "Part II",
            "chapter": "10. Structured sampling",
            "reader_summary": "Sampling with stochastic gradients, coordinate methods, and mirror Langevin geometry.",
            "lean_plan": "Introduce oracle/noisy-gradient and coordinate-update interfaces only after base kernels and mirror-geometry assumptions are explicit.",
            "shared": "MEAS, CONV, SDE, DISC, REG",
            "status": "deferred-consumer",
        },
        {
            "part": "Part II",
            "chapter": "11. Non-log-concave sampling",
            "reader_summary": "Approximate stationarity and nonconvex behavior controlled through Fisher information bounds and applications.",
            "lean_plan": "Reuse FI, KL, weak-FP, and score/Fisher algebra; do not assume convexity roots unless the theorem explicitly requires them.",
            "shared": "DENS, FI, SDE, DISC, REG",
            "status": "deferred-consumer",
        },
        {
            "part": "Part II",
            "chapter": "12. Diffusion generative models",
            "reader_summary": "Score matching and discretization analysis for diffusion generative modeling.",
            "lean_plan": "Use path-space change of measure, score-drift regularity, weak-FP, and discretization leaves after the SDE/PATH foundation is mature.",
            "shared": "MEAS, DENS, SDE, PATH, DISC, REG",
            "status": "deferred-consumer",
        },
    ]


def chewi_open_leaf_rows() -> list[dict[str, str]]:
    return [
        {
            "leaf": "logConcaveOn_density_def",
            "label": "CONV/DENS",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "borrow": "Mathlib `ConcaveOn`, `ConcaveOn.subset`, `strictConcaveOn_log_Ioi`; AST Prekopa files for next statement style",
            "status": "core API, negative-log potential extraction, quasiconcavity/superlevel convexity and restriction, linear/affine precomposition, product/power/product-domain tensorization, norm-square convexity, centered/shifted/two-point quadratic Gibbs log-concavity, and Gibbs positive-rescale leaves compiled; next Prekopa/RN integration",
        },
        {
            "leaf": "prekopaLeindler_finiteDimensional",
            "label": "CONV/MEAS",
            "target": "TechnicalLemmas/Geometry/PrekopaLeindler.lean",
            "borrow": "external `AsymptoticStatistics/ForMathlib/PrekopaLeindler.lean`; Mathlib lacks direct PL package",
            "status": "external-port-audit",
        },
        {
            "leaf": "brunnMinkowski_oneDim_outerMeasure",
            "label": "CONV/MEAS",
            "target": "TechnicalLemmas/Geometry/BrunnMinkowski.lean",
            "borrow": "external `Brunn1D.lean`; Mathlib convex/volume APIs",
            "status": "external-port-audit",
        },
        {
            "leaf": "gibbsDensity_withDensity_normalized",
            "label": "DENS/CONV",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean; then TechnicalLemmas/Measure/{Gibbs,RadonNikodym}.lean",
            "borrow": "compiled `logConcaveOn_const_mul_exp_neg_of_convexOn`, log-concavity linear/affine precomposition and product/rpow/tensorization leaves, centered/shifted/two-point quadratic and one-dimensional Laplace normalized-density log-concavity, `gibbsDensityENNReal`, nonzero/finite envelope leaves, finite-measure lower-bound normalization, and `Analysis.Integrability` exact quadratic plus exact one-dimensional Laplace Lebesgue Gibbs normalizers; next generalize beyond finite-dimensional quadratic and one-dimensional Laplace tails",
            "status": "convex shape plus map pullbacks, product/power tensorization, centered/shifted/two-point quadratic and one-dimensional Laplace Gibbs log-concavity, Gibbs density, measurability, nonzero integral, finite-by-envelope, finite-measure lower-bound envelope, exact quadratic and exact one-dimensional Laplace Lebesgue normalizers, and normalized withDensity probability bridges compiled; general coercivity envelopes remain",
        },
        {
            "leaf": "langevinGenerator_invariant_gibbs_weak",
            "label": "SDE/DENS/FI",
            "target": "TechnicalLemmas/StochasticProcesses/Langevin.lean",
            "borrow": "compiled Langevin algebra and IBP, explicit C_c^2 core/domain agreement, normalized-Gibbs core annihilation, and the abstract integrated-semigroup-generator invariance bridge; ASTIS WeakGenerator, LangevinGenerator, and GibbsIntegral supply the interfaces",
            "status": "analytic core, core-domain contract, normalized core mean-zero, and abstract semigroup bridge compile; concrete Langevin semigroup construction plus extension to a semigroup-stable domain remain red before invariant Gibbs law",
        },
        {
            "leaf": "lsi_tensorization_or_preservation_contract",
            "label": "FI/CONV",
            "target": "TechnicalLemmas/FunctionalInequalities/Preservation.lean",
            "borrow": "Mathlib convex/Jensen APIs; SLT/AST reference style for functional inequality statements",
            "status": "planned",
        },
        {
            "leaf": "gaussianEsscher_shift_density",
            "label": "GAUSS/PATH",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "borrow": "external `GaussianMGF.lean`, `PiWithDensity.lean`, `GaussianShift.lean`",
            "status": "formalized-local-density-half",
        },
        {
            "leaf": "gaussianShift_change_of_measure",
            "label": "GAUSS/PATH",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "borrow": "external `GaussianShift.lean`; local `stdGaussianPi_withDensity_exp_shift`",
            "status": "formalized-local-product-measure",
        },
        {
            "leaf": "gaussianShift_euclidean_pushforward",
            "label": "GAUSS/PATH",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "borrow": "Mathlib `EuclideanSpace`/`WithLp.toLp`; local `stdGaussianPi_shift_integral`",
            "status": "formalized-local-euclidean-pushforward",
        },
        {
            "leaf": "gaussianShift_stdGaussian_inner",
            "label": "GAUSS/PATH",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "borrow": "Mathlib `map_pi_eq_stdGaussian`, `PiLp.inner_apply`, `EuclideanSpace.real_norm_sq_eq`",
            "status": "formalized-local-stdGaussian-inner",
        },
        {
            "leaf": "finiteGaussianGirsanov_cylinder",
            "label": "PATH/GAUSS",
            "target": "TechnicalLemmas/StochasticProcesses/Girsanov.lean",
            "borrow": "compiled `stdGaussian_shift_integral_map_toLp`; finite-dimensional cylindrical path-coordinate packaging",
            "status": "formalized-local-cylinder",
        },
        {
            "leaf": "finiteGaussianGirsanov_rn_density",
            "label": "PATH/MEAS/GAUSS",
            "target": "TechnicalLemmas/StochasticProcesses/Girsanov.lean",
            "borrow": "compiled `measurableEquiv_map_withDensity`, product Gaussian withDensity shift, and `map_pi_eq_stdGaussian`",
            "status": "formalized-local-rn-density",
        },
        {
            "leaf": "lmcInterpolation_weakGenerator",
            "label": "DISC/SDE/KERN",
            "target": "SamplingAlgorithms/LangevinMonteCarlo.lean",
            "borrow": "ASTIS LawMap/ConditionalKernel/WeakGenerator; textbook LMC interpolation as the consumer route",
            "status": "planned-generalization",
        },
        {
            "leaf": "renyiDensity_pointwiseDerivative",
            "label": "DENS/FI",
            "target": "TechnicalLemmas/InformationTheory/Renyi.lean",
            "borrow": "compiled `renyiIntegrand`, positivity, measurability, finite-envelope, and `HasDerivAt` rpow-product leaves; next add full divergence/log-normalization and path derivative contracts",
            "status": "first-leaves-compiled",
        },
        {
            "leaf": "mhKernel_detailedBalance",
            "label": "DISC/KERN",
            "target": "SamplingAlgorithms/MetropolisAdjustedLangevin.lean",
            "borrow": "Mathlib probability kernels/Markov-chain APIs if present; otherwise local kernel contracts",
            "status": "mathlib-search-required",
        },
    ]


def chewi_api_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "area": "convex/log-concave base",
            "mathlib": "`Analysis/Convex/*`, `ConvexOn`, `ConcaveOn`, log convexity examples",
            "external": "`ForMathlib/PrekopaLeindler.lean`, `Brunn1D.lean`, `Anderson.lean`",
            "gap": "No direct Mathlib Prekopa-Leindler/Brunn-Minkowski package observed.",
        },
        {
            "area": "density/RN/withDensity",
            "mathlib": "`Probability/Density.lean`, `Measure/Decomposition/*`, `withDensity`, `rnDeriv`",
            "external": "`RnDerivSqrt.lean`, `HellingerProduct.lean`, `L2.lean`",
            "gap": "Gibbs nonzero, finite-by-envelope, finite-measure bounded-below, exact quadratic Lebesgue, and exact one-dimensional Laplace normalization contracts are compiled; need general coercivity/growth leaves proving tail-integrable envelopes.",
        },
        {
            "area": "Gaussian/product Gaussian",
            "mathlib": "`Probability.Distributions.Gaussian.Real`, CLT/charFun support",
            "external": "`PiGaussian.lean`, `GaussianMGF.lean`, `GaussianShift.lean`, `PiWithDensity.lean`",
            "gap": "Product Gaussian MGF, normalizer, shifted withDensity identity, product integral change-of-measure, EuclideanSpace pushforward bridge, and stdGaussian inner-product form are compiled; Brownian/path packaging remains.",
        },
        {
            "area": "conditional kernels",
            "mathlib": "`Probability.Kernel.CondDistrib`, conditional expectation APIs",
            "external": "`CondExpL2.lean`, Markov-kernel/selection files",
            "gap": "Need fixed representative policy for conditional drifts in algorithm proofs.",
        },
        {
            "area": "SDE/semigroup/Langevin",
            "mathlib": "general topology/calculus/integration; no full finite-dimensional Ito/SDE library observed",
            "external": "ASTIS WeakGenerator/FokkerPlanckAlgebra, source-cited textbook route",
            "gap": "Finite-dimensional cylindrical Girsanov integral and RN/withDensity identity are compiled; Ito, generator domains, invariant Gibbs proof, and full Brownian path-space change of measure remain real analytic leaves.",
        },
        {
            "area": "information theory",
            "mathlib": "`InformationTheory/KullbackLeibler/KLFun.lean`, convexity of KL integrand",
            "external": "ASTIS `KLDensity`, `DonskerVaradhan`, external Hellinger/RN files",
            "gap": "Renyi divergence and derivative identities need new local leaves.",
        },
        {
            "area": "algorithms",
            "mathlib": "kernel/measure infrastructure; search per algorithm before local coding",
            "external": "AST Gaussian/conditional references and textbook algorithm proof routes",
            "gap": "LMC/HMC/MALA/proximal trees should be consumers until shared roots compile.",
        },
    ]


def chewi_foundation_mmd_text() -> str:
    return """flowchart LR
  Source[Log-Concave Sampling textbook]
  Mathlib[Mathlib API search]
  ASTRef[External Lean references]
  REG[REG hidden regularity contracts]
  MEAS[MEAS law map and measures]
  KERN[KERN conditional kernels]
  DENS[DENS densities RN KL Renyi]
  GAUSS[GAUSS Gaussian products]
  CONV[CONV convex log-concave PL BM]
  FI[FI PI LSI transport concentration]
  SDE[SDE semigroup generator Langevin weak-FP]
  PATH[PATH Girsanov Doob Follmer bridge]
  DISC[DISC LMC HMC MALA proximal]
  Consumers[textbook theorem and algorithm consumers]

  Source --> MEAS
  Source --> CONV
  Source --> FI
  Source --> SDE
  Source --> PATH
  Source --> DISC
  Mathlib --> MEAS
  Mathlib --> DENS
  Mathlib --> CONV
  Mathlib --> FI
  ASTRef --> CONV
  ASTRef --> GAUSS
  ASTRef --> DENS
  ASTRef --> PATH
  REG -. required by every leaf .-> MEAS
  REG -. required by every leaf .-> CONV
  REG -. required by every leaf .-> SDE
  MEAS --> KERN
  MEAS --> DENS
  DENS --> FI
  GAUSS --> PATH
  CONV --> FI
  FI --> SDE
  SDE --> DISC
  PATH --> DISC
  DISC --> Consumers
"""


def chewi_foundation_svg() -> str:
    boxes = {
        "source": (45, 105, 240, 70, "Textbook roadmap", "chapter/theorem source DAG", "input"),
        "mathlib": (45, 245, 240, 70, "Mathlib scout", "search before porting", "input"),
        "refs": (45, 385, 240, 70, "Reference repos", "AST, SLT, Rademacher", "input"),
        "reg": (365, 80, 260, 74, "REG contracts", "measurable, integrable, smooth, boundary", "contract"),
        "meas": (360, 205, 245, 70, "MEAS law maps", "map, withDensity, RN", "leaf"),
        "kern": (665, 205, 245, 70, "KERN conditional", "condDistrib representatives", "leaf"),
        "dens": (970, 205, 245, 70, "DENS entropy", "KL, Renyi, FI algebra", "leaf"),
        "gauss": (360, 350, 245, 70, "GAUSS products", "moments, MGF, tilts", "leaf"),
        "conv": (665, 350, 245, 70, "CONV geometry", "log-concavity, PL, BM", "leaf"),
        "fi": (970, 350, 245, 70, "FI inequalities", "PI, LSI, TI, concentration", "leaf"),
        "sde": (665, 500, 245, 74, "SDE Langevin", "semigroup, generator, weak-FP", "leaf"),
        "path": (970, 500, 245, 74, "PATH transforms", "Girsanov, Doob, Follmer", "analytic"),
        "disc": (665, 650, 245, 74, "DISC algorithms", "LMC, HMC, MALA, proximal", "consumer"),
        "gate": (970, 650, 245, 74, "Reviewer gate", "Mathlib-ready, no hidden assumptions", "gate"),
    }
    edges = [
        ("source", "reg", "extract", False),
        ("mathlib", "meas", "reuse", False),
        ("mathlib", "conv", "reuse", False),
        ("refs", "gauss", "port plan", False),
        ("refs", "conv", "port plan", False),
        ("refs", "path", "port plan", True),
        ("reg", "meas", "", True),
        ("reg", "conv", "", True),
        ("reg", "sde", "", True),
        ("meas", "kern", "", False),
        ("meas", "dens", "", False),
        ("gauss", "path", "tilt", False),
        ("conv", "fi", "preserve", False),
        ("dens", "fi", "entropy", False),
        ("fi", "sde", "dissipation", False),
        ("kern", "sde", "drift", False),
        ("sde", "disc", "interpolation", False),
        ("path", "disc", "change measure", False),
        ("disc", "gate", "gate", False),
    ]
    node_parts = [
        leaf_network_node(node_id, x, y, w, h, title, subtitle, kind)
        for node_id, (x, y, w, h, title, subtitle, kind) in boxes.items()
    ]
    edge_parts = [
        leaf_network_edge(boxes[src][:4], boxes[dst][:4], label, dashed)
        for src, dst, label, dashed in edges
    ]
    generated = html.escape(now_stamp())
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="1280" height="790" viewBox="0 0 1280 790" xmlns="http://www.w3.org/2000/svg">
<defs>
  <marker id="arrowLeaf" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
    <polygon points="0 0, 9 3.5, 0 7" fill="#7f8da3"/>
  </marker>
</defs>
<rect width="1280" height="790" fill="white"/>
<text x="640" y="34" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="24" font-weight="700" fill="#1f2933">Log-Concave Sampling Formalization Spine</text>
<text x="640" y="58" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#475569">Shared root nodes are reused across chapter/theorem DAGs; chapter proofs become consumers of the same Mathlib-ready leaves.</text>
<g id="edges">
{chr(10).join(edge_parts)}
</g>
<g id="nodes">
{chr(10).join(node_parts)}
</g>
<text x="830" y="760" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="#64748b">Generated {generated} by tools/astis.py lemma-dag-refresh</text>
</svg>
"""


def log_concave_lean_tree_status_rows() -> list[dict[str, str]]:
    return [
        {
            "family": "MEAS/KERN",
            "node": "Probability.LawMap",
            "target": "TechnicalLemmas/Probability/LawMap.lean",
            "status": "compiled-blue",
            "role": "law-map and weak-test integral rewrites",
        },
        {
            "family": "MEAS/KERN",
            "node": "Probability.ConditionalKernel",
            "target": "TechnicalLemmas/Probability/ConditionalKernel.lean",
            "status": "compiled-blue",
            "role": "condDistrib and conditional-integral representatives",
        },
        {
            "family": "MEAS/KERN",
            "node": "Measure.Transport",
            "target": "TechnicalLemmas/Measure/Transport.lean",
            "status": "todo-red",
            "role": "transport/coupling/Wasserstein interfaces",
        },
        {
            "family": "DENS/CONV",
            "node": "Geometry.LogConcavity",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "positive log-concavity, norm-square and absolute-value convexity, and convex-potential Gibbs shape",
        },
        {
            "family": "DENS/CONV",
            "node": "Log-concavity algebra/tensorization",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "pointwise products, nonnegative real powers, and Cartesian-product density factors preserve log-concavity",
        },
        {
            "family": "DENS/CONV",
            "node": "Log-concavity under maps",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "linear and affine precomposition preserve log-concavity on preimage domains",
        },
        {
            "family": "DENS/CONV",
            "node": "Log-concavity level sets",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "positive log-concave functions are quasiconcave; convex superlevel restrictions remain log-concave",
        },
        {
            "family": "GEOM/GAUSS/SDE",
            "node": "EuclideanSpace coordinate inner products",
            "target": "TechnicalLemmas/Geometry/EuclideanSpaceCoordinates.lean",
            "status": "compiled-blue",
            "role": "finite-dimensional coordinate formulas for `inner ℝ u v`, including direct `EuclideanSpace` vectors and `WithLp.toLp 2` coordinate functions",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Laplacian standard-basis formula",
            "target": "TechnicalLemmas/Analysis/Calculus/Laplacian.lean",
            "status": "compiled-blue",
            "role": "Mathlib `Laplacian.laplacian` equals the finite standard-orthonormal-basis second-derivative sum; no IBP or invariant-law proof",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Gradient coordinate-unit line derivative",
            "target": "TechnicalLemmas/Analysis/Calculus/Gradient.lean",
            "status": "compiled-blue",
            "role": "a supplied Mathlib gradient gives the coordinate-unit line derivative equal to the corresponding gradient coordinate; no divergence or IBP proof",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Gibbs-weight gradient chain rule",
            "target": "TechnicalLemmas/Analysis/Calculus/Gradient.lean",
            "status": "compiled-blue",
            "role": "a supplied `HasGradientAt V gradV x` or `DifferentiableAt ℝ V x` gives Mathlib `gradient (exp(-V))` and coordinate chain-rule displays; no weighted divergence, coordinate product-rule, or IBP proof",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Line-derivative product rule",
            "target": "TechnicalLemmas/Analysis/Calculus/LineDeriv.lean",
            "status": "compiled-blue",
            "role": "Mathlib `HasDerivAt.mul` exposed as real-valued `HasLineDerivAt` and `lineDeriv` product rules, explicit coordinate `lineDeriv (exp(-V) * g)` leaves, and `fderiv`-to-`iteratedFDeriv` coordinate wiring; no divergence or IBP proof",
        },
        {
            "family": "DENS/CONV/SDE",
            "node": "Negative-log potential geometry",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "positive log-concave densities have convex negative-log potentials and convex energy sublevels",
        },
        {
            "family": "DENS/CONV",
            "node": "Quadratic Gibbs log-concavity",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "nonnegative quadratic norm potentials and explicit normalized quadratic Gibbs densities are log-concave",
        },
        {
            "family": "DENS/CONV",
            "node": "Absolute-linear Laplace geometry",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "one-dimensional potentials `a|x|+b` and positive rescaled Laplace shapes are log-concave",
        },
        {
            "family": "DENS/CONV/GAUSS",
            "node": "Shifted quadratic Gibbs geometry",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "shifted potentials `a‖x-m‖^2+b` and explicit shifted quadratic densities are log-concave",
        },
        {
            "family": "DENS/CONV/GAUSS/DISC",
            "node": "Two-point Gaussian/proximal kernel geometry",
            "target": "TechnicalLemmas/Geometry/LogConcavity.lean",
            "status": "compiled-blue",
            "role": "two-point potentials `a‖x-y‖^2+b` and Gaussian-kernel shapes are log-concave on product space",
        },
        {
            "family": "DENS/CONV",
            "node": "Measure.RadonNikodym",
            "target": "TechnicalLemmas/Measure/RadonNikodym.lean",
            "status": "compiled-blue",
            "role": "withDensity, reciprocal-lintegral normalization, RN wrappers",
        },
        {
            "family": "DENS/MEAS",
            "node": "Measure.pi withDensity product",
            "target": "TechnicalLemmas/Measure/RadonNikodym.lean",
            "status": "compiled-blue",
            "role": "finite-product ENNReal Fubini and coordinatewise density-tilt decomposition",
        },
        {
            "family": "MEAS/FI/SDE",
            "node": "Measure.Product coordinate update",
            "target": "TechnicalLemmas/Measure/Product.lean",
            "status": "compiled-blue",
            "role": "finite product-law coordinate replacement map, measure-preserving wrapper, Bochner integral rewrite, and a.e. slice integrability",
        },
        {
            "family": "DENS/CONV",
            "node": "Measure.Gibbs",
            "target": "TechnicalLemmas/Measure/Gibbs.lean",
            "status": "compiled-blue",
            "role": "Gibbs ENNReal density, measurability, envelope comparison, and normalization",
        },
        {
            "family": "DENS/MEAS/SDE",
            "node": "Gibbs withDensity Bochner integral rewrite",
            "target": "TechnicalLemmas/Measure/GibbsIntegral.lean",
            "status": "compiled-blue",
            "role": "Bochner integrals under `Z⁻¹ exp(-V)` withDensity rewrite to density-weighted base-measure integrals",
        },
        {
            "family": "DENS/CONV",
            "node": "Normalized Gibbs real-density bridge",
            "target": "TechnicalLemmas/Measure/GibbsLogConcavity.lean",
            "status": "compiled-blue",
            "role": "finite nonzero ENNReal normalizer plus convex or strongly convex potential gives a real-valued normalized Gibbs density shape that is log-concave",
        },
        {
            "family": "DENS/CONV",
            "node": "Potential lower-bound envelope",
            "target": "TechnicalLemmas/Measure/Gibbs.lean",
            "status": "compiled-blue",
            "role": "`W ≤ V` a.e. and finite `∫ exp(-W)` imply finite `∫ exp(-V)` and normalized Gibbs law",
        },
        {
            "family": "DENS/CONV",
            "node": "Finite-measure Gibbs envelope",
            "target": "TechnicalLemmas/Measure/Gibbs.lean",
            "status": "compiled-blue",
            "role": "finite base measure plus a.e. constant lower bound on `V` gives finite Gibbs normalizer and normalized target law",
        },
        {
            "family": "DENS/CONV/ANALYSIS",
            "node": "Quadratic Lebesgue Gibbs envelope",
            "target": "TechnicalLemmas/Analysis/Integrability.lean",
            "status": "compiled-blue",
            "role": "finite-dimensional Lebesgue quadratic tails have exact ENNReal normalizers, and quadratic lower bounds give normalized Gibbs target laws",
        },
        {
            "family": "DENS/CONV/ANALYSIS",
            "node": "One-dimensional Laplace normalizer",
            "target": "TechnicalLemmas/Analysis/Integrability.lean",
            "status": "compiled-blue",
            "role": "exact `∫ exp (-(a|x|+b)) = 2 exp(-b)/a`, exact ENNReal normalizer, and explicit normalized Laplace law on `ℝ`",
        },
        {
            "family": "DENS/CONV",
            "node": "InformationTheory.KLDensity/DV",
            "target": "TechnicalLemmas/InformationTheory/{KLDensity,DonskerVaradhan}.lean",
            "status": "compiled-blue",
            "role": "KL pointwise algebra and DV energy leaves",
        },
        {
            "family": "DENS/CONV",
            "node": "Prekopa/Brunn/Convex",
            "target": "TechnicalLemmas/Geometry/{Convex,PrekopaLeindler,BrunnMinkowski}.lean",
            "status": "todo-red",
            "role": "finite-dimensional PL/BM and convex-measure preservation",
        },
        {
            "family": "DENS/CONV",
            "node": "Concrete Gibbs envelope",
            "target": "TechnicalLemmas/Measure/Gibbs.lean or Analysis/Integrability.lean",
            "status": "todo-red",
            "role": "general nonquadratic Lebesgue coercivity/growth assumptions beyond finite-dimensional quadratic and one-dimensional Laplace envelopes",
        },
        {
            "family": "DENS/CONV",
            "node": "Renyi density calculus",
            "target": "TechnicalLemmas/InformationTheory/Renyi.lean",
            "status": "compiled-blue",
            "role": "Renyi integrand positivity, measurability, finite-envelope, and pointwise derivative leaves",
        },
        {
            "family": "GAUSS",
            "node": "ProbabilityDistributions.Gaussian",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "compiled-blue",
            "role": "Gaussian moments, coordinate laws, finite linear forms, MGF normalizers, shifted densities, and variance packaging",
        },
        {
            "family": "GAUSS",
            "node": "Product Gaussian linear forms",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "compiled-blue",
            "role": "finite product-Gaussian linear-form integrability and zero mean",
        },
        {
            "family": "GAUSS",
            "node": "Product Gaussian MGF / normalizer",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "compiled-blue",
            "role": "finite product-Gaussian linear-form MGF and centered Esscher mass-one normalizer",
        },
        {
            "family": "GAUSS",
            "node": "Scalar Gaussian Esscher shift",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "compiled-blue",
            "role": "one-dimensional Gaussian exponential tilt shifts the mean",
        },
        {
            "family": "GAUSS",
            "node": "Product Gaussian shifted density",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "compiled-blue",
            "role": "finite product standard Gaussian withDensity tilt equals shifted product Gaussian",
        },
        {
            "family": "GAUSS",
            "node": "Product Gaussian change of measure",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "compiled-blue",
            "role": "finite shifted product-Gaussian integrals rewrite as centered weighted integrals",
        },
        {
            "family": "GAUSS",
            "node": "EuclideanSpace Gaussian pushforward",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "compiled-blue",
            "role": "transport finite product-Gaussian Esscher change-of-measure through `WithLp.toLp 2`",
        },
        {
            "family": "GAUSS",
            "node": "stdGaussian inner-product change of measure",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "compiled-blue",
            "role": "rewrite the Euclidean change-of-measure against Mathlib `stdGaussian` with inner-product/norm exponent",
        },
        {
            "family": "GAUSS",
            "node": "Full path-space Gaussian / Girsanov",
            "target": "TechnicalLemmas/ProbabilityDistributions/Gaussian.lean",
            "status": "todo-red",
            "role": "Brownian/path-space RN derivative beyond finite-dimensional cylinders",
        },
        {
            "family": "FI",
            "node": "FunctionalInequalities.LogSobolev",
            "target": "TechnicalLemmas/FunctionalInequalities/LogSobolev.lean",
            "status": "compiled-blue",
            "role": "LSI to KL/FI bookkeeping and sqrt-density handoffs",
        },
        {
            "family": "FI",
            "node": "PI/TI/Isoperimetry",
            "target": "TechnicalLemmas/FunctionalInequalities/{Poincare,Transport,Isoperimetry}.lean",
            "status": "todo-red",
            "role": "Poincare, transport inequalities, concentration, isoperimetry",
        },
        {
            "family": "FI",
            "node": "Preservation/tensorization",
            "target": "TechnicalLemmas/FunctionalInequalities/Preservation.lean",
            "status": "todo-red",
            "role": "tensorization and preservation under log-concavity operations",
        },
        {
            "family": "SDE/PATH",
            "node": "StochasticProcesses.WeakGenerator",
            "target": "TechnicalLemmas/StochasticProcesses/WeakGenerator.lean",
            "status": "compiled-blue",
            "role": "sample-to-law weak-generator rewrite",
        },
        {
            "family": "SDE/PATH",
            "node": "StochasticProcesses.FokkerPlanckAlgebra",
            "target": "TechnicalLemmas/StochasticProcesses/FokkerPlanckAlgebra.lean",
            "status": "compiled-blue",
            "role": "weak-FP and Fisher/IBP scalar algebra",
        },
        {
            "family": "SDE/PATH",
            "node": "StochasticProcesses.Langevin",
            "target": "TechnicalLemmas/StochasticProcesses/Langevin.lean",
            "status": "compiled-blue",
            "role": "Finite Euclidean pointwise display and supplied-hypothesis Langevin algebra: basis/coordinate display for the formal expression `Δ f - <∇V, ∇f>`, supplied coordinate-to-Mathlib weighted-divergence handoffs, `exp(-V)` handoffs discharging only the Gibbs-weight gradient premise, pointwise coordinateDivergence display, finite-box signed face-term wrapper with explicit assumptions, 1D pointwise derivative, finite-coordinate aggregation, and EuclideanSpace inner-product notation wrappers; no box-integrability discharge, semigroup-generator, IBP, stationarity, or invariant-law proof",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Reusable smooth cutoffs and plateaus",
            "target": "TechnicalLemmas/Analysis/Calculus/{Cutoff,Divergence}.lean",
            "status": "compiled-blue",
            "role": "unit and radial smooth cutoffs, support/tsupport and compact-support bounds, pointwise exhaustion, compact-in-open plateau, and finite Pi-box plateau",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Scale-uniform cutoff first derivative",
            "target": "TechnicalLemmas/Analysis/Calculus/{Cutoff,Divergence}.lean",
            "status": "compiled-blue",
            "role": "one unit-cutoff constant controls every positive-scale radial fderiv by C/R; the totalized fderiv vanishes on the closed outer region; PiLp chain-rule and standard-basis trace bridges expose the cutoff cross term",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Generic L1 cutoff-gradient limit",
            "target": "TechnicalLemmas/Analysis/Calculus/Divergence.lean",
            "status": "compiled-blue",
            "role": "for every Integrable finite-Pi vector field, the norm integral of the PiLp-wrapped radial cutoff derivative applied to the field tends to zero",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Generic cutoff main-term dominated convergence",
            "target": "TechnicalLemmas/Analysis/Calculus/Divergence.lean",
            "status": "compiled-blue",
            "role": "for every Integrable normed-space-valued field, multiplication by the PiLp-wrapped radial cutoff converges under the integral to the original field",
        },
        {
            "family": "ANALYSIS/SDE",
            "node": "Gibbs source and generator-display integrability",
            "target": "TechnicalLemmas/StochasticProcesses/Langevin.lean plus on-demand cutoff leaves",
            "status": "compiled-blue",
            "role": "finite Gibbs mass plus bounded genuine first derivative gives Integrable exp(-V)-weighted coordinate fields; compact C_c^2 tests give both the concrete Integrable generator display and the compiled whole-space identity integral exp(-V) Lf = 0",
        },
        {
            "family": "SDE/PATH",
            "node": "StochasticProcesses.Girsanov finite cylinder",
            "target": "TechnicalLemmas/StochasticProcesses/Girsanov.lean",
            "status": "compiled-blue",
            "role": "finite-dimensional cylindrical Gaussian Girsanov weight, RN density, and integral change-of-measure",
        },
        {
            "family": "SDE/PATH",
            "node": "Semigroup/Ito/invariant Gibbs law",
            "target": "TechnicalLemmas/StochasticProcesses/{MarkovSemigroup,Ito}.lean plus stronger Langevin analytic leaves",
            "status": "todo-red",
            "role": "semigroup domains, invariant Gibbs law, Ito interfaces",
        },
        {
            "family": "SDE/PATH",
            "node": "Girsanov/Doob/Follmer",
            "target": "TechnicalLemmas/StochasticProcesses/{Girsanov,DoobTransform,FollmerDrift}.lean",
            "status": "todo-red",
            "role": "path-space RN derivatives and bridge transforms",
        },
        {
            "family": "DISC",
            "node": "LMC interpolation",
            "target": "SamplingAlgorithms/LangevinMonteCarlo.lean",
            "status": "todo-red",
            "role": "LMC interpolation, coupling, KL/FI derivative consumers",
        },
        {
            "family": "DISC",
            "node": "HMC/underdamped/RM",
            "target": "SamplingAlgorithms/{HamiltonianMonteCarlo,UnderdampedLangevin,RandomizedMidpoint}.lean",
            "status": "todo-red",
            "role": "faster low-accuracy sampler transition/generator contracts",
        },
        {
            "family": "DISC",
            "node": "MALA/proximal/high-accuracy",
            "target": "SamplingAlgorithms/{MetropolisAdjustedLangevin,ProximalSampler}.lean",
            "status": "todo-red",
            "role": "acceptance kernels, detailed balance, restricted Gaussian oracles",
        },
    ]


def log_concave_lean_tree_status_mmd_text() -> str:
    return """flowchart TD
  Root[ASTIS-CHEWI-001<br/>Log-concave sampling Lean tree]
  MEAS[MEAS/KERN<br/>measure and kernels]
  DENS[DENS/CONV<br/>densities and convexity]
  GAUSS[GAUSS<br/>Gaussian infrastructure]
  FI[FI<br/>functional inequalities]
  SDE[SDE/PATH<br/>continuous-time and transforms]
  DISC[DISC<br/>sampling algorithms]

  Root --> MEAS
  Root --> DENS
  Root --> GAUSS
  Root --> FI
  Root --> SDE
  Root --> DISC

  MEAS --> LawMap[Probability.LawMap]
  MEAS --> CondKernel[Probability.ConditionalKernel]
  MEAS --> PiUpdate[Measure.Product coordinate update]
  MEAS --> Transport[Measure.Transport]

  DENS --> LogConcavity[Geometry.LogConcavity]
  DENS --> LogConcavityTensor[Log-concavity algebra/tensorization]
  DENS --> LogConcavityMaps[Log-concavity under maps]
  DENS --> LogConcavityLevels[Log-concavity level sets]
  DENS --> NegLogPotential[Negative-log potential geometry]
  DENS --> GibbsQuadLogConcavity[Quadratic Gibbs log-concavity]
  DENS --> ShiftedGibbsQuad[Shifted quadratic Gibbs geometry]
  DENS --> PairKernelGeometry[Two-point Gaussian/proximal kernel geometry]
  DENS --> RN[Measure.RadonNikodym]
  DENS --> PiDensity[Measure.pi withDensity product]
  DENS --> Gibbs[Measure.Gibbs]
  DENS --> GibbsIntegral[Gibbs withDensity Bochner integral rewrite]
  DENS --> GibbsPotentialEnv[Potential lower-bound envelope]
  DENS --> GibbsFiniteEnv[Finite-measure Gibbs envelope]
  DENS --> GibbsQuadEnv[Quadratic Lebesgue Gibbs envelope]
  DENS --> KLDV[InformationTheory.KLDensity/DV]
  DENS --> PLBM[Prekopa/Brunn/Convex]
  DENS --> GibbsEnv[General coercivity Gibbs envelope]
  DENS --> Renyi[Renyi density calculus]

  GAUSS --> Gaussian[ProbabilityDistributions.Gaussian]
  GAUSS --> GaussianLinear[Product Gaussian linear forms]
  GAUSS --> GaussianMGF[Product Gaussian MGF / normalizer]
  GAUSS --> GaussianScalarShift[Scalar Gaussian Esscher shift]
  GAUSS --> GaussianProductShift[Product Gaussian shifted density]
  GAUSS --> GaussianCOM[Product Gaussian change of measure]
  GAUSS --> GaussianEuclidean[EuclideanSpace Gaussian pushforward]
  GAUSS --> GaussianStd[stdGaussian inner-product change of measure]
  GAUSS --> GaussianPath[Full path-space Gaussian / Girsanov]

  FI --> LSI[FunctionalInequalities.LogSobolev]
  FI --> PITI[PI/TI/Isoperimetry]
  FI --> Preserve[Preservation/tensorization]

  SDE --> WeakGen[StochasticProcesses.WeakGenerator]
  SDE --> FP[StochasticProcesses.FokkerPlanckAlgebra]
  SDE --> Langevin1D[StochasticProcesses.Langevin expression display/algebra]
  SDE --> BoxDiv[Analysis.Calculus.Divergence box face-term wrapper]
  SDE --> AEBridge[Analysis.Calculus.Divergence a.e. trace bridge]
  SDE --> IntTransfer[Analysis.Calculus.Divergence trace-to-coordinate IntegrableOn]
  SDE --> ExplicitTrace[StochasticProcesses.Langevin explicit trace display]
  SDE --> DisplayContinuity[Scalar display ContinuousOn from components]
  SDE --> TraceIntegrability[Trace IntegrableOn under global C1/C2]
  SDE --> TestRegularity[Global C1/C2 components and Pi field fderiv]
  SDE --> CutoffBase[Reusable smooth cutoffs and plateaus]
  SDE --> CutoffFirst[Scale-uniform cutoff first derivative]
  SDE --> CutoffL1[Generic L1 cutoff-gradient limit]
  SDE --> CutoffMain[Generic cutoff main-term DCT]
  SDE --> CutoffSecond[Second-order cutoff on demand]
  SDE --> GirsanovFinite[StochasticProcesses.Girsanov finite cylinder]
  SDE --> Langevin[Semigroup/Ito/invariant Gibbs law]
  SDE --> Path[Girsanov/Doob/Follmer]

  DISC --> LMC[LMC interpolation]
  DISC --> HMC[HMC/underdamped/RM]
  DISC --> MALA[MALA/proximal/high-accuracy]

  classDef root fill:#f8fafc,stroke:#475569,color:#0f172a,stroke-width:2px;
  classDef compiled fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef todo fill:#fee2e2,stroke:#dc2626,color:#450a0a,stroke-width:2px;
  class Root,MEAS,DENS,GAUSS,FI,SDE,DISC root;
  class LawMap,CondKernel,PiUpdate,LogConcavity,LogConcavityTensor,LogConcavityMaps,LogConcavityLevels,NegLogPotential,GibbsQuadLogConcavity,ShiftedGibbsQuad,PairKernelGeometry,RN,PiDensity,Gibbs,GibbsIntegral,GibbsPotentialEnv,GibbsFiniteEnv,GibbsQuadEnv,KLDV,Renyi,Gaussian,GaussianLinear,GaussianMGF,GaussianScalarShift,GaussianProductShift,GaussianCOM,GaussianEuclidean,GaussianStd,LSI,WeakGen,FP,Langevin1D,BoxDiv,AEBridge,IntTransfer,ExplicitTrace,DisplayContinuity,TraceIntegrability,TestRegularity,CutoffBase,CutoffFirst,CutoffL1,GirsanovFinite compiled;
  class Transport,PLBM,GibbsEnv,GaussianPath,PITI,Preserve,CutoffSecond,Langevin,Path,LMC,HMC,MALA todo;
"""


def chewi_status_color(status: str) -> tuple[str, str, str]:
    if status == "compiled-blue":
        return "#dbeafe", "#2563eb", "#0f172a"
    if status == "todo-red":
        return "#fee2e2", "#dc2626", "#450a0a"
    return "#f8fafc", "#475569", "#0f172a"


def chewi_status_svg_node(
    node_id: str,
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    subtitle: str,
    status: str,
) -> str:
    fill, stroke, text_color = chewi_status_color(status)
    title = html.escape(title)
    subtitle = html.escape(subtitle)
    return f"""<g id="{html.escape(node_id)}">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>
  <text x="{x + w / 2:.1f}" y="{y + 20}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="{text_color}">{title}</text>
  <text x="{x + w / 2:.1f}" y="{y + 38}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="{text_color}">{subtitle}</text>
</g>"""


def chewi_status_svg_edge(src: tuple[int, int, int, int], dst: tuple[int, int, int, int]) -> str:
    x1 = src[0] + src[2] / 2
    y1 = src[1] + src[3]
    x2 = dst[0] + dst[2] / 2
    y2 = dst[1]
    mid = (y1 + y2) / 2
    return (
        f'<path d="M {x1:.1f} {y1:.1f} C {x1:.1f} {mid:.1f}, {x2:.1f} {mid:.1f}, {x2:.1f} {y2:.1f}" '
        'fill="none" stroke="#94a3b8" stroke-width="1.1" marker-end="url(#arrowStatus)"/>'
    )


def log_concave_lean_tree_status_svg() -> str:
    columns = [
        ("MEAS/KERN", 30, [
            ("Probability.LawMap", "compiled", "compiled-blue"),
            ("Probability.ConditionalKernel", "compiled", "compiled-blue"),
            ("Measure.Product", "compiled", "compiled-blue"),
            ("Measure.Transport", "todo", "todo-red"),
        ]),
        ("DENS/CONV", 275, [
            ("Geometry.LogConcavity", "compiled", "compiled-blue"),
            ("Measure.RadonNikodym", "compiled", "compiled-blue"),
            ("Pi withDensity", "compiled", "compiled-blue"),
            ("Measure.Gibbs", "compiled", "compiled-blue"),
            ("Gibbs integral rewrite", "compiled", "compiled-blue"),
            ("Potential envelope", "compiled", "compiled-blue"),
            ("KLDensity / DV", "compiled", "compiled-blue"),
            ("Renyi density", "compiled", "compiled-blue"),
            ("Prekopa / Brunn", "todo", "todo-red"),
            ("Coercivity envelope", "todo", "todo-red"),
        ]),
        ("GAUSS", 520, [
            ("Gaussian coordinates", "compiled", "compiled-blue"),
            ("Linear forms", "compiled", "compiled-blue"),
            ("MGF normalizer", "compiled", "compiled-blue"),
            ("Scalar shift", "compiled", "compiled-blue"),
            ("Product shift", "compiled", "compiled-blue"),
            ("Change of measure", "compiled", "compiled-blue"),
            ("Euclidean pushforward", "compiled", "compiled-blue"),
            ("stdGaussian inner form", "compiled", "compiled-blue"),
            ("Path-space packaging", "todo", "todo-red"),
        ]),
        ("FI", 765, [
            ("LogSobolev bookkeeping", "compiled", "compiled-blue"),
            ("PI / TI / Isoperimetry", "todo", "todo-red"),
            ("Preservation", "todo", "todo-red"),
        ]),
        ("SDE/PATH", 1010, [
            ("WeakGenerator", "compiled", "compiled-blue"),
            ("FokkerPlanck algebra", "compiled", "compiled-blue"),
            ("Langevin expression/algebra", "compiled", "compiled-blue"),
            ("Smooth cutoff/plateau base", "compiled", "compiled-blue"),
            ("Cutoff fderiv O(R^-1) + Pi trace", "compiled", "compiled-blue"),
            ("L1 cutoff-gradient limit", "compiled", "compiled-blue"),
            ("Cutoff main-term DCT", "compiled", "compiled-blue"),
            ("2nd-order cutoff (on demand)", "todo", "todo-red"),
            ("Finite Girsanov RN cylinder", "compiled", "compiled-blue"),
            ("Semigroup/Ito/invariant law", "todo", "todo-red"),
            ("Girsanov/Doob/Follmer", "todo", "todo-red"),
        ]),
        ("DISC", 1255, [
            ("LMC interpolation", "todo", "todo-red"),
            ("HMC / underdamped / RM", "todo", "todo-red"),
            ("MALA / proximal", "todo", "todo-red"),
        ]),
    ]
    root = (555, 52, 420, 58)
    nodes = [
        chewi_status_svg_node("root", *root, "ASTIS-CHEWI-001 Lean tree", "blue = compiled locally; red = todo", "root")
    ]
    edges = []
    family_boxes: dict[str, tuple[int, int, int, int]] = {}
    for family, x, children in columns:
        family_box = (x, 140, 210, 52)
        family_boxes[family] = family_box
        nodes.append(chewi_status_svg_node(slugify(family), *family_box, family, "shared root", "root"))
        edges.append(chewi_status_svg_edge(root, family_box))
        for i, (title, subtitle, status) in enumerate(children):
            child_box = (x, 220 + 56 * i, 210, 46)
            nodes.append(chewi_status_svg_node(slugify(f"{family}-{title}"), *child_box, title, subtitle, status))
            edges.append(chewi_status_svg_edge(family_box, child_box))
    generated = html.escape(now_stamp())
    legend_y = 810
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="1500" height="880" viewBox="0 0 1500 880" xmlns="http://www.w3.org/2000/svg">
<defs>
  <marker id="arrowStatus" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#94a3b8"/>
  </marker>
</defs>
<rect width="1500" height="880" fill="white"/>
<text x="750" y="30" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="24" font-weight="700" fill="#1f2933">Log-Concave Sampling Mathlib-Ready Lean Tree Status</text>
<g id="edges">
{chr(10).join(edges)}
</g>
<g id="nodes">
{chr(10).join(nodes)}
</g>
<rect x="30" y="{legend_y}" width="22" height="16" fill="#dbeafe" stroke="#2563eb"/>
<text x="60" y="{legend_y + 13}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#0f172a">compiled local ASTIS/Mathlib-ready leaf or module</text>
<rect x="350" y="{legend_y}" width="22" height="16" fill="#fee2e2" stroke="#dc2626"/>
<text x="380" y="{legend_y + 13}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#450a0a">todo branch/leaf with explicit target module and reviewer contract</text>
<text x="970" y="855" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="#64748b">Generated {generated} by tools/astis.py lemma-dag-refresh</text>
</svg>
"""


def chewi_additional_chapter_subtrees_text() -> str:
    return """## Chapter 3 Path-Space Stochastic Analysis Subtree

```mermaid
flowchart TD
  C3[Ch.3 stochastic analysis topics]
  QV[quadratic variation]
  COM[change of measure in path space]
  DOOB[Doob transform]
  FOLL[Follmer drift]
  SB[Schrodinger bridge]
  GAUSS[GAUSS finite Gaussian shifts]
  CYL[finite-dimensional Girsanov cylinder]
  RN[PATH RN derivative]
  BRIDGE[bridge drift transform]
  REG[REG path regularity]

  C3 --> QV
  C3 --> COM
  C3 --> DOOB
  C3 --> FOLL
  C3 --> SB
  GAUSS --> CYL --> RN
  COM --> RN
  DOOB --> BRIDGE
  FOLL --> BRIDGE
  SB --> BRIDGE
  REG -.-> QV
  REG -.-> RN
  REG -.-> BRIDGE
```

## Chapter 5 Faster Low-Accuracy Samplers Subtree

```mermaid
flowchart TD
  C5[Ch.5 faster low-accuracy samplers]
  RMD[randomized midpoint]
  HMC[Hamiltonian Monte Carlo]
  ULD[underdamped Langevin]
  GAUSS[GAUSS update noise]
  GEN[SDE generator contracts]
  KERN[DISC transition kernels]
  RATE[low-accuracy rate theorem]
  REG[REG smoothness and moments]

  C5 --> RMD
  C5 --> HMC
  C5 --> ULD
  GAUSS --> KERN
  RMD --> KERN
  HMC --> GEN
  ULD --> GEN
  GEN --> RATE
  KERN --> RATE
  REG -.-> GEN
  REG -.-> KERN
```

## Chapter 6 Renyi Divergence Subtree

```mermaid
flowchart TD
  C6[Ch.6 Renyi divergence]
  LMCINT[LMC interpolation route]
  LMCGIR[LMC Girsanov route]
  ULMC[ULMC Girsanov route]
  RENYI[DENS Renyi density calculus]
  FI[FI differential inequality]
  PATH[PATH change of measure]
  DISC[DISC algorithm theorem]
  REG[REG integrability and positivity]

  C6 --> LMCINT
  C6 --> LMCGIR
  C6 --> ULMC
  RENYI --> FI --> DISC
  PATH --> RENYI
  LMCINT --> FI
  LMCGIR --> PATH
  ULMC --> PATH
  REG -.-> RENYI
  REG -.-> FI
```

## Chapter 7 High-Accuracy Samplers Subtree

```mermaid
flowchart TD
  C7[Ch.7 high-accuracy samplers]
  RS[rejection sampling]
  MH[Metropolis-Hastings filter]
  MC[discrete-time Markov chains]
  COLD[MALA cold start]
  WARM[MALA warm start]
  KERN[KERN Markov kernels]
  BAL[detailed balance and reversibility]
  DENS[DENS warm-start densities]
  DISC[DISC high-accuracy theorem]
  REG[REG acceptance and support]

  C7 --> RS
  C7 --> MH
  C7 --> MC
  C7 --> COLD
  C7 --> WARM
  KERN --> BAL --> DISC
  DENS --> WARM --> DISC
  MH --> BAL
  MC --> KERN
  REG -.-> KERN
  REG -.-> BAL
```

## Chapter 8 Proximal Sampler Subtree

```mermaid
flowchart TD
  C8[Ch.8 proximal sampler]
  RGO[restricted Gaussian oracle]
  SLC[strong log-concavity]
  STR[simultaneous flow and time reversal]
  LC[log-concavity]
  FI[functional inequalities]
  IMPL[RGO implementations]
  CONV[CONV proximal geometry]
  GAUSS[GAUSS two-point kernels]
  KERN[KERN conditional law]
  DISC[DISC proximal transition]
  REG[REG oracle and support]

  C8 --> RGO
  C8 --> SLC
  C8 --> STR
  C8 --> LC
  C8 --> FI
  C8 --> IMPL
  CONV --> GAUSS --> KERN --> DISC
  RGO --> KERN
  LC --> CONV
  FI --> DISC
  REG -.-> KERN
```

## Chapter 9 Lower-Bound Subtree

```mermaid
flowchart TD
  C9[Ch.9 lower bounds]
  QUERY[query complexity model]
  ONE[one-dimensional constructions]
  CONST[constant-dimensional constructions]
  GAUSS[Gaussian lower bounds]
  ORACLE[DISC oracle interface]
  INFO[DENS information comparison]
  GROOT[GAUSS comparison lemmas]
  REG[REG model assumptions]

  C9 --> QUERY
  C9 --> ONE
  C9 --> CONST
  C9 --> GAUSS
  QUERY --> ORACLE
  ONE --> INFO
  CONST --> INFO
  GAUSS --> GROOT --> INFO
  REG -.-> ORACLE
```

## Chapter 10 Structured-Sampling Subtree

```mermaid
flowchart TD
  C10[Ch.10 structured sampling]
  SG[stochastic gradients]
  COORD[coordinate methods]
  MIRROR[mirror Langevin]
  ORACLE[MEAS noisy oracle laws]
  GEOM[CONV mirror geometry]
  GEN[SDE generator]
  DISC[DISC structured updates]
  REG[REG unbiasedness and smoothness]

  C10 --> SG
  C10 --> COORD
  C10 --> MIRROR
  SG --> ORACLE --> DISC
  COORD --> DISC
  MIRROR --> GEOM --> GEN --> DISC
  REG -.-> ORACLE
  REG -.-> GEOM
```

## Chapter 11 Non-Log-Concave Sampling Subtree

```mermaid
flowchart TD
  C11[Ch.11 non-log-concave sampling]
  STAT[approximate stationarity via FI]
  FIB[Fisher information bounds]
  APP[applications]
  LB[lower bounds]
  FI[FI score and Fisher algebra]
  SDE[SDE weak-FP]
  DISC[DISC algorithm consumers]
  REG[REG nonconvex regularity]

  C11 --> STAT
  C11 --> FIB
  C11 --> APP
  C11 --> LB
  STAT --> FI
  FIB --> FI --> SDE --> DISC
  APP --> DISC
  REG -.-> FI
  REG -.-> SDE
```

## Chapter 12 Diffusion-Generative-Models Subtree

```mermaid
flowchart TD
  C12[Ch.12 diffusion generative models]
  INTRO[introduction]
  SCORE[score matching and variants]
  DISCANA[discretization analysis]
  DENS[DENS score density]
  PATH[PATH reverse-time change of measure]
  SDE[SDE forward/reverse dynamics]
  DISC[DISC discretization theorem]
  REG[REG score and time regularity]

  C12 --> INTRO
  C12 --> SCORE
  C12 --> DISCANA
  SCORE --> DENS
  DENS --> PATH --> SDE
  SDE --> DISC
  DISCANA --> DISC
  REG -.-> DENS
  REG -.-> SDE
```
"""


def log_concave_sampling_overview_text() -> str:
    chapter_table = markdown_table(log_concave_chapter_map_rows(), [
        ("Part", "part"),
        ("Chapter", "chapter"),
        ("Summary", "reader_summary"),
        ("Lean organization plan", "lean_plan"),
        ("Shared roots", "shared"),
        ("Status", "status"),
    ])
    return f"""# Log-Concave Sampling Lean Organization

Generated: `{now_stamp()}`

Primary source: `{CHEWI_LOG_CONCAVE_URL}`

Local source: `{CHEWI_LOG_CONCAVE_PDF}`

The repository is a faithful reconstruction of the textbook mathematics.  A
textbook sentence is not stored as one monolithic Lean theorem: it is decomposed
into reusable leaves, and the cited or implicit background steps are made
explicit when Lean needs them.

## How To Read The Library

- Blue nodes in the status tree are compiled local Lean leaves or modules.
- Red nodes are missing mathematical infrastructure with a named target file.
- Shared roots (`MEAS`, `KERN`, `DENS`, `GAUSS`, `CONV`, `FI`, `SDE`, `PATH`,
  `DISC`, `REG`) are reused across chapters so the library does not duplicate
  the same measure-theory, convexity, Gaussian, or SDE lemmas for each sampler.
- Algorithm chapters should be consumers.  They should call the shared roots
  after those roots compile locally.

Main visual ledger:
`{rel(LOG_CONCAVE_FOUNDATION_DAG_MD)}`

Rendered status tree:
`{rel(LOG_CONCAVE_STATUS_SVG)}`

## Visual Index

```mermaid
flowchart LR
  PDF[textbook statement]:::source
  Hidden[cited or implicit<br/>background fact]:::source
  Root[shared root<br/>MEAS DENS CONV CALC SDE]:::root
  Leaf[small Lean leaf<br/>blue/red]:::leaf
  Module[owning Lean module]:::module
  Chapter[chapter theorem<br/>consumer]:::consumer

  PDF --> Hidden --> Root --> Leaf --> Module --> Chapter

  classDef source fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-width:1.5px;
  classDef root fill:#e0f2fe,stroke:#0284c7,color:#0f172a,stroke-width:2px;
  classDef leaf fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef module fill:#fef3c7,stroke:#d97706,color:#422006,stroke-width:2px;
  classDef consumer fill:#dcfce7,stroke:#16a34a,color:#052e16,stroke-width:2px;
```

## Chapter-By-Chapter Map

{chapter_table}

## Current Ch.1 Ladder

```mermaid
flowchart TD
  A[generator display<br/>Lf = Delta f - gradV dot gradf]:::blue
  B[weighted display<br/>exp(-V)Lf]:::blue
  C[coordinate divergence<br/>and trace bridge]:::blue
  D[global C1/C2 regularity<br/>gradient, Laplacian, Pi fderiv]:::blue
  E[finite-box trace<br/>IntegrableOn]:::blue
  F[finite-box face terms]:::blue
  G[local and exact-support<br/>smooth cutoffs]:::blue
  H[compact-in-open and Pi-box<br/>plateau = 1]:::blue
  I[radial cutoff family<br/>compact support + tends to 1]:::blue
  J1[scale-uniform cutoff fderiv<br/>O(R^-1)]:::blue
  J1S[closed outer region<br/>totalized fderiv = 0]:::blue
  JP[PiLp cutoff derivative<br/>chain-rule bridge]:::blue
  JT[smulRight basis trace<br/>equals derivative on field]:::blue
  J2[Hessian/Laplacian cutoff<br/>O(R^-2)]:::blue
  K[generic L1 cutoff-gradient limit<br/>from Integrable field]:::blue
  KS[Gibbs source-field<br/>integrability]:::blue
  KM[generic main-term<br/>dominated convergence]:::blue
  KMI[concrete generator-display<br/>integrability for C_c^2 tests]:::blue
  KGT[Gibbs-tail passage]:::blue
  L[weighted whole-space IBP<br/>integral Lf d pi = 0]:::blue
  M[generator and semigroup<br/>domain contract]:::red
  N[invariant Gibbs law]:::red
  O[reversibility<br/>KL/FI dissipation]:::red

  A --> B --> C --> E --> F --> L --> N --> O
  D --> B
  D --> E
  G --> F
  G --> H
  I --> J1 --> JP --> JT --> K --> L
  KS --> L
  KM --> KMI --> L
  KGT --> L
  I --> J1S
  I --> J2
  M --> N

  classDef blue fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef red fill:#fee2e2,stroke:#dc2626,color:#450a0a,stroke-width:2px;
```

| Layer | Current blue result | Remaining red edge |
| --- | --- | --- |
| display algebra | pointwise generator, weighted display, coordinate sum conventions | none for finite-dimensional pointwise algebra |
| regularity | global `C¹/C²` gives gradient continuity, Laplacian continuity, scalar `ContinuousOn`, and Pi-field `HasFDerivAt` with Mathlib `fderiv` | closed-box/local regularity variants if later needed |
| finite boxes | trace `IntegrableOn`, a.e. trace bridge, trace-to-coordinate transfer, signed face-term wrapper | none for the compact-support whole-space route |
| cutoffs | local/exact support, compact-in-open and Pi-box plateaus, radial compact support, pointwise exhaustion, `O(R⁻¹)` first-derivative control, and `O(R⁻²)` second-derivative/Laplacian control | no cutoff estimate is a semigroup-domain theorem |
| whole-space passage | compact-support whole-space divergence and Gibbs-weighted `integral exp(-V) Lf = 0` for `C_c^2` tests, plus generic cutoff/tail infrastructure | stronger noncompact test classes when a consumer requires them |
| operator bridge | C_c^2 core/domain agreement, normalized-Gibbs core annihilation, and abstract semigroup/domain-to-invariance theorem compile | instantiate the contract for the Langevin evolution and extend mean-zero to its stable domain |
| invariant law | abstract implication is compiled | concrete Langevin semigroup contract or an equivalent uniqueness theorem |

## Current Compiled Foundation

- Positive log-concavity, products, powers, pullbacks, superlevel geometry,
  absolute-linear Laplace geometry, and negative-log potential convexity live in
  `AutoSamplingTheory/TechnicalLemmas/Geometry/LogConcavity.lean`.
- Gibbs density, the ENNReal-to-real log-concavity bridge for finite nonzero
  normalizers, finite-measure lower-bound envelopes, exact finite-dimensional
  quadratic normalizers, exact one-dimensional Laplace normalizers, and
  normalized withDensity probability bridges under those explicit envelope
  hypotheses live in `AutoSamplingTheory/TechnicalLemmas/Measure/Gibbs.lean` and
  `AutoSamplingTheory/TechnicalLemmas/Analysis/Integrability.lean`.
- Product Gaussian linear forms, moment-generating normalizers, Esscher shifts,
  finite-dimensional change of measure, and Euclidean `stdGaussian` bridges
  live in `AutoSamplingTheory/TechnicalLemmas/ProbabilityDistributions/Gaussian.lean`.
- KL/DV/Renyi algebra, LSI bookkeeping, weak generator, weak-FP algebra, and
  finite-dimensional Girsanov cylinders are compiled as reusable support.
- `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean` contains
  the reusable smooth unit cutoff, positive-scale radial family, closed-ball
  support and topological-support bounds, compact support, pointwise convergence
  to one, a general compact-in-open smooth plateau theorem, a bounded unit-cutoff
  derivative, the totalized `fderiv` bound for `x -> ||x|| / R`, a single
  constant controlling every radial first derivative by `C / R`, and zero
  totalized derivative throughout the closed outer region `2R <= ||x||`, and
  a single constant controlling every radial second iterated derivative by
  `C / R^2`.  The finite-dimensional Laplacian trace bound is compiled in
  `Analysis/Calculus/Laplacian.lean`.
- `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Divergence.lean`
  contains the finite coordinate-divergence convention, Euclidean/Pi `WithLp`
  trace bridge, the radial-cutoff `toLp` derivative producer, the standard-basis
  `smulRight` trace identity, the generic `L¹` cutoff-gradient limit for every
  `Integrable` finite-Pi vector field, the generic expanding-ball `L¹` tail
  limit, generic cutoff main-term dominated convergence,
  open-box/off-countable to closed-box a.e. transfer,
  trace-to-coordinate `IntegrableOn` transfer, and the finite-box signed
  face-term wrapper with trace-integrability input, and the reusable theorem
  that a compactly supported `C¹` finite-dimensional vector field has zero
  whole-space divergence integral. It also specializes the plateau theorem to
  an inner closed Pi-box inside a larger open Pi-box. It contains no
  generator-domain, semigroup, invariant-law, reversibility, or KL/FI semantics.
- `AutoSamplingTheory/TechnicalLemmas/StochasticProcesses/Langevin.lean`
  contains Langevin-specific blue leaves: finite Euclidean basis/coordinate
  displays of the formal expression `Delta f - <grad V, grad f>`, supplied
  coordinate-to-Mathlib weighted-divergence handoffs, the `exp(-V)` handoffs
  that discharge only the Gibbs-weight gradient premise, the one-dimensional
  Gibbs-weighted generator pointwise identity, the multidimensional
  inner-product supplied-hypothesis weighted-divergence algebra handoff,
  finite-coordinate aggregation handoff, the explicit Pi trace display, and
  the closed-box trace `IntegrableOn` handoff under global `C¹/C²` regularity
  for the canonical Mathlib `fderiv` trace, and whole-space integrability of
  the concrete Gibbs-weighted first-derivative coordinate field from finite
  Gibbs mass and a uniform `fderiv` bound, concrete compact-test generator
  integrability, expanding-ball Gibbs-tail convergence, and whole-space
  Gibbs-weighted integration by parts for `C_c^2` tests. It also assembles the scalar
  display `ContinuousOn` fact from global `C¹/C²` and proves the explicit
  Pi-field `HasFDerivAt` needed by the trace handoff. It is not a closed
  semigroup-generator, invariant-law, reversibility, or semigroup-domain theorem.
- `AutoSamplingTheory/TechnicalLemmas/StochasticProcesses/LangevinGenerator.lean`
  names the `C_c^2` test core, the displayed operator, an explicit candidate
  generator core/domain agreement contract, and normalized-Gibbs generator
  mean-zero on that core. `WeakGenerator.lean` contains the separate abstract
  integrated-semigroup-generator contract and its invariance theorem.

## Immediate Library Boundary

The next high-value roots, ordered by the active textbook dependency, are:

1. `SDE/REG`: instantiate the integrated semigroup-generator contract for the
   actual Langevin evolution, including the right derivative of Gibbs pairings.
2. `SDE/DENS/FI`: extend normalized-Gibbs generator mean-zero from the
   `C_c^2` core to the semigroup-stable domain, or supply an equivalent
   martingale-problem/Fokker-Planck uniqueness theorem.
3. `CONV/MEAS`: finite-dimensional Prekopa-Leindler and Brunn-Minkowski
   interfaces, using `Lean-Asymptotic-Statistical-Theory/ForMathlib` as a
   reference but porting only small local leaves.
4. `DENS/CONV`: nonquadratic coercive Gibbs envelopes for Lebesgue targets.
5. `PATH/GAUSS`: Brownian/path-space change of measure beyond finite
   cylinders.
6. `DISC`: LMC/MALA/HMC/proximal samplers only after the above roots are local.

## Rigor Contract

Whenever the textbook uses a standard analytic phrase such as Fokker-Planck,
Girsanov, integration by parts, regularity assumptions, or invariant measure,
the Lean plan must expose the hidden assumptions: measurability,
integrability, domination, differentiability, boundary decay, positivity, and
representative choices.  Unsupported assumptions are recorded as red proof
obligations rather than being silently added to close a theorem.
"""


def chewi_agent_execution_pack_text() -> str:
    role_rows = [
        {
            "role": "upper_director",
            "job": "Choose the one chapter/root/leaf that gives the most reusable progress; reject wrapper churn that does not serve the textbook tree.",
            "output": "One cycle packet with source anchor, shared roots, lower split, and reviewer gate.",
        },
        {
            "role": "upper_source_math",
            "job": "Audit the source statement and hidden regularity before proof search starts.",
            "output": "Source-faithfulness decision: supported, standard background, regularity gap, or statement drift.",
        },
        {
            "role": "upper_proof_dag",
            "job": "Pick the shortest dependency path through the shared-root DAG.",
            "output": "A small active leaf and stale-leaf retirements.",
        },
        {
            "role": "upper_process_memory",
            "job": "Check whether the run is repeating old work or ignoring existing compiled roots.",
            "output": "One process correction if needed.",
        },
        {
            "role": "middle_formalizer",
            "job": "Translate the upper packet into lower-ready Lean theorem shapes.",
            "output": "One lower_1 math route, one lower_2 Lean implementation task, optional lower_3 API scout task.",
        },
        {
            "role": "middle_source_correspondence",
            "job": "Map textbook prose to exact Lean-facing objects and assumptions.",
            "output": "Source line/range, informal statement, Lean statement skeleton, hidden regularity list.",
        },
        {
            "role": "middle_technical_lemma",
            "job": "Search Mathlib, local ASTIS registry, and external reference repos as provenance only.",
            "output": "Compiled-local, needs-small-port, or proof-obligation classification.",
        },
        {
            "role": "middle_report_export",
            "job": "Keep library summaries and run summaries synchronized after proof progress.",
            "output": "Plain-language update, not proof search.",
        },
        {
            "role": "lower_1",
            "job": "Natural-language proof scout for exactly one leaf.",
            "output": "Math route, required hypotheses, expected Lean theorem shape, lower_2 handoff.",
        },
        {
            "role": "lower_2",
            "job": "Lean implementer for exactly one theorem or smaller source-cited boundary.",
            "output": "Compiled declaration or precise typed blocker.",
        },
        {
            "role": "lower_3",
            "job": "API/technical-lemma scout for missing reusable facts.",
            "output": "One tiny local port or proof-obligation packet.",
        },
        {
            "role": "reviewer_gate",
            "job": "Deterministic correctness gate.",
            "output": "`python3 tools/astis.py check` status, no fake closure, source/API consistency.",
        },
        {
            "role": "reviewer_waste",
            "job": "Progress-economics review for the 6h batch.",
            "output": "What improved, what wasted effort, and the best next leaf.",
        },
    ]
    return f"""# Log-Concave Sampling Six-Hour Execution Pack

Generated: `{now_stamp()}`

This pack is the control-console entry point for running the hierarchical
multi-agent system on the log-concave sampling foundation.  The run must keep
the textbook as the source roadmap and Mathlib-ready reusable leaves as the output.

## One-Command Launch

```bash
python3 tools/astis.py launch-log-concave-6h --hours 6 --wall-hours 24 --lower-count 3
```

This creates a long-window `sleep-run-window` job in the background.  It uses
an active-agent budget of 6 hours, keeps a larger wall-clock safety window, runs
lower workers in parallel, and executes `python3 tools/astis.py check` after
each cycle.

## Equivalent Direct Command

```bash
python3 tools/astis.py sleep-run-window ASTIS-CHEWI-001 \\
  --hours 24 \\
  --agent-hours-budget 6 \\
  --max-cycles 64 \\
  --lower-count 3 \\
  --parallel-lower \\
  --upper-panel-final \\
  --middle-panel-final \\
  --reviewer-waste-final \\
  --agent-cmd "bash tools/astis_codex_faithful.sh {{root}} {{prompt}}" \\
  --execute \\
  --check-each-cycle
```

## GNU Screen Mode

Use this when you want the long run to live in a named terminal session:

```bash
screen -dmS astis_log_concave_6h bash -lc 'cd /home/nitanda_sub/mark/repos/Auto-Sampling-Theory-In-Sleep; python3 tools/astis.py sleep-run-window ASTIS-CHEWI-001 --hours 24 --agent-hours-budget 6 --max-cycles 64 --lower-count 3 --parallel-lower --upper-panel-final --middle-panel-final --reviewer-waste-final --agent-cmd "bash tools/astis_codex_faithful.sh {{root}} {{prompt}}" --execute --check-each-cycle'
```

Attach/detach:

```bash
screen -r astis_log_concave_6h
```

Inside screen, detach with `Ctrl-a d`.  The run itself writes per-agent logs
under `runs/<cycle>/agent-logs/` and the global trial ledger under
`runs/trials.jsonl`.

## Role Split

{markdown_table(role_rows, [
    ("Role", "role"),
    ("Job", "job"),
    ("Required output", "output"),
])}

## Cycle Discipline

1. Upper picks one reusable shared-root leaf, not an algorithm theorem unless
   all analytic roots are already local.
2. Middle translates the leaf into a stable theorem statement, source anchor,
   hidden regularity list, and Mathlib/API search target.
3. Lower workers either compile one small ASTIS-owned theorem or return a
   strictly smaller blocker.
4. Reviewer accepts only compiled local Lean, source-indexed proof obligations,
   concrete port plans, or explicit rejection of a false/unsupported statement.
5. After a successful cycle, regenerate DAGs, module cards, and retrieval
   indexes so the next screen cycle starts from the updated plan.

## First Three Recommended Cycles

| Cycle | Objective | Reason |
|---|---|---|
| 1 | Chapter map plus shared-root lock | Prevent the system from drifting into wrappers that do not close textbook leaves. |
| 2 | `CONV/MEAS` Prekopa-Leindler audit and smallest port candidate | This is the missing preservation root for functional inequalities. |
| 3 | `DENS/CONV` nonquadratic coercive Gibbs envelope | This connects textbook target densities to normalized probability laws beyond quadratic examples. |

## Hard Stops

- Do not treat external Lean repos as callable dependencies.
- Do not add assumptions just to make Lean close.
- Do not mark a red node blue without a local compiled declaration covered by
  `lake build` and `lake build Tests`.
- Do not let lower workers edit the same theorem block in parallel unless
  middle explicitly assigned disjoint files.
"""


def chewi_chapter_dag_text() -> str:
    root_table = markdown_table(chewi_shared_root_rows(), [
        ("Label", "label"),
        ("Shared root", "root"),
        ("Target module/root", "module"),
        ("Role", "role"),
        ("Status", "status"),
    ])
    chapter_table = markdown_table(chewi_chapter_rows(), [
        ("Chapter/topic", "chapter"),
        ("Shared labels", "shared"),
        ("Subtree to draw/formalize", "dag"),
        ("First lower-agent leaf", "first_leaf"),
        ("Status", "status"),
    ])
    leaf_table = markdown_table(chewi_open_leaf_rows(), [
        ("Open leaf", "leaf"),
        ("Label", "label"),
        ("Target file", "target"),
        ("Mathlib/external borrow plan", "borrow"),
        ("Status", "status"),
    ])
    status_table = markdown_table(log_concave_lean_tree_status_rows(), [
        ("Family", "family"),
        ("Branch/leaf", "node"),
        ("Target", "target"),
        ("Color status", "status"),
        ("Role", "role"),
    ])
    api_table = markdown_table(chewi_api_audit_rows(), [
        ("Area", "area"),
        ("Mathlib surface", "mathlib"),
        ("External reference", "external"),
        ("Gap / next action", "gap"),
    ])
    return f"""# Log-Concave Sampling Foundation DAG

Generated: `{now_stamp()}`

Primary source: `{CHEWI_LOG_CONCAVE_URL}`

Local source: `{CHEWI_LOG_CONCAVE_PDF}`

This is the master visualization ledger for `ASTIS-CHEWI-001`.  The goal is
to avoid one oversized graph: every chapter or major theorem should point
to shared root nodes and then have its own smaller subtree.  Shared labels make
common Lean leaves reusable across chapters and later theorem subtrees.

## Global Spine

```mermaid
{chewi_foundation_mmd_text()}```

## Blue/Red Lean Tree Status

Blue nodes are compiled local ASTIS declarations or modules covered by
`lake build`.  Red nodes are the todo branches I can keep driving with
Mathlib-first leaves and explicit source/regularity contracts.

Rendered status tree:
`{rel(LOG_CONCAVE_STATUS_SVG)}`

```mermaid
{log_concave_lean_tree_status_mmd_text()}```

{status_table}

## Shared Root Nodes

{root_table}

## Chapter And Theorem Subtree Registry

{chapter_table}

## Chapter 1 Langevin Continuous-Time Subtree

```mermaid
flowchart TD
  C1[Ch.1 Langevin diffusion]
  SC[1.1 stochastic calculus]
  MS[1.2 Markov semigroup]
  OT[1.3 optimal transport]
  WGF[1.4 Wasserstein gradient flow]
  GAUSS[GAUSS Gaussian increments]
  TAY[Taylor/Ito local error]
  SEM[Markov semigroup operator]
  GEN[generator-domain contract]:::blue
  GENALG[Gibbs-weight generator algebra]:::blue
  BOX[finite-box divergence<br/>and zero-face handoffs]:::blue
  LOCAL[local/exact-support<br/>cutoff leaves]:::blue
  PLATEAU[compact-in-open and Pi-box<br/>plateau cutoffs]:::blue
  RADIAL[radial cutoff family<br/>compact support + pointwise limit]:::blue
  DERIV1[scale-uniform fderiv<br/>O(R^-1)]:::blue
  DSUP[closed outer region<br/>totalized fderiv = 0]:::blue
  PIB[PiLp derivative and<br/>smulRight trace bridges]:::blue
  DERIV2[Hessian/Laplacian<br/>O(R^-2)]:::blue
  TAIL[generic L1 cutoff-gradient limit<br/>from Integrable field]:::blue
  SOURCEINT[Gibbs source-field<br/>integrability]:::blue
  MAINCONV[generic main-term<br/>dominated convergence]:::blue
  MAININT[concrete generator-display<br/>integrability for C_c^2 tests]:::blue
  GIBBSTAIL[Gibbs-tail passage]:::blue
  IBP[whole-space weighted IBP]:::blue
  BRIDGE[abstract semigroup/domain<br/>to invariance]:::blue
  CONCRETE[concrete Langevin semigroup<br/>and stable domain]:::red
  INV[invariant Gibbs law]:::red
  KL[KL/FI dissipation]
  W2[Wasserstein gradient-flow contract]
  REG[REG hidden regularity]

  C1 --> SC
  C1 --> MS
  C1 --> OT
  C1 --> WGF
  SC --> GAUSS --> TAY
  MS --> SEM --> GEN --> BRIDGE
  GEN --> GENALG --> BOX --> IBP --> BRIDGE --> CONCRETE --> INV
  LOCAL --> BOX
  LOCAL --> PLATEAU
  PLATEAU --> BOX
  RADIAL --> DERIV1 --> PIB --> TAIL --> IBP
  SOURCEINT --> IBP
  MAINCONV --> MAININT --> IBP
  GIBBSTAIL --> IBP
  RADIAL --> DSUP
  RADIAL --> DERIV2
  WGF --> INV --> KL --> W2
  REG -.-> TAY
  REG -.-> GEN
  REG -.-> GENALG
  REG -.-> BOX
  REG -.-> DERIV1
  REG -.-> DSUP
  REG -.-> PIB
  REG -.-> DERIV2
  REG -.-> TAIL
  REG -.-> SOURCEINT
  REG -.-> MAINCONV
  REG -.-> IBP
  REG -.-> INV

  classDef blue fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef red fill:#fee2e2,stroke:#dc2626,color:#450a0a,stroke-width:2px;
```

## Chapter 2 Functional-Inequality Subtree

```mermaid
flowchart TD
  C2[Ch.2 functional inequalities]
  DEF[PI LSI TI definitions]
  SEM[semigroup proof route]
  PRES[preservation operations]
  CONC[concentration and isoperimetry]
  DISC[discrete space/time]
  CONV[CONV log-concavity]
  PL[Prekopa-Leindler]
  LSI[LSI to KL/FI compiled bookkeeping]
  REG[REG hidden regularity]

  C2 --> DEF
  C2 --> SEM
  C2 --> PRES
  C2 --> CONC
  C2 --> DISC
  CONV --> PL --> PRES
  DEF --> LSI
  SEM --> LSI
  REG -.-> PL
  REG -.-> LSI
```

## Chapter 4 LMC Interpolation Subtree

```mermaid
flowchart TD
  C4[Ch.4 Langevin Monte Carlo]
  COUP[Wasserstein coupling proof]
  INT[interpolation proof]
  OPT[convex optimization proof]
  GIR[Girsanov proof]
  LAW[MEAS law-map derivative]
  KERN[KERN conditional drift]
  WFP[SDE weak-FP bridge]
  KL[DENS KL/FI derivative]
  PATH[PATH change of measure]
  DISC[DISC LMC theorem]
  REG[REG hidden regularity]

  C4 --> COUP
  C4 --> INT
  C4 --> OPT
  C4 --> GIR
  INT --> LAW --> WFP
  KERN --> WFP
  WFP --> KL --> DISC
  GIR --> PATH --> DISC
  REG -.-> LAW
  REG -.-> WFP
  REG -.-> KL
```

{chewi_additional_chapter_subtrees_text()}

## Open Leaf Queue

{leaf_table}

## Mathlib And External API Audit

{api_table}

## Review Rule

Every subtree edge must eventually be one of:

- a compiled ASTIS-owned Lean declaration;
- a Mathlib theorem/API name used directly;
- an external reference theorem with a local port plan;
- a source-cited `ProofObligation` whose hidden regularity is explicit.

Do not add a chapter theorem node unless it reuses the shared roots above or
creates a new shared root with a label and reviewer contract.
"""


def write_chewi_foundation_docs() -> list[Path]:
    outputs: list[Path] = []
    path_texts = [
        (LOG_CONCAVE_FOUNDATION_DAG_MD, chewi_chapter_dag_text()),
        (LOG_CONCAVE_FOUNDATION_MMD, chewi_foundation_mmd_text()),
        (LOG_CONCAVE_FOUNDATION_SVG, chewi_foundation_svg()),
        (LOG_CONCAVE_STATUS_MMD, log_concave_lean_tree_status_mmd_text()),
        (LOG_CONCAVE_STATUS_SVG, log_concave_lean_tree_status_svg()),
        (LOG_CONCAVE_OVERVIEW_MD, log_concave_sampling_overview_text()),
        (LOG_CONCAVE_EXECUTION_PACK_MD, chewi_agent_execution_pack_text()),
    ]
    for path, text in path_texts:
        write_text(path, text)
        outputs.append(path)
    png_path = LOG_CONCAVE_FOUNDATION_PNG
    if render_svg_preview(LOG_CONCAVE_FOUNDATION_SVG, png_path):
        outputs.append(png_path)
    status_png_path = LOG_CONCAVE_STATUS_PNG
    if render_svg_preview(LOG_CONCAVE_STATUS_SVG, status_png_path):
        outputs.append(status_png_path)

    md_path, json_path = log_concave_sampling_to_lean_roadmap()
    outputs.extend([md_path, json_path])
    retrieval = {
        "generated": now_stamp(),
        "task": "ASTIS-CHEWI-001",
        "source_pdf": str(CHEWI_LOG_CONCAVE_PDF),
        "public_pdf": CHEWI_LOG_CONCAVE_URL,
        "foundation_dag": rel(LOG_CONCAVE_FOUNDATION_DAG_MD),
        "foundation_svg": rel(LOG_CONCAVE_FOUNDATION_SVG),
        "foundation_mmd": rel(LOG_CONCAVE_FOUNDATION_MMD),
        "status_tree_svg": rel(LOG_CONCAVE_STATUS_SVG),
        "status_tree_mmd": rel(LOG_CONCAVE_STATUS_MMD),
        "roadmap": rel(SAMPLING_LIBRARY_DIR / "roadmap" / "log_concave_sampling_to_lean_tree.md"),
        "library_overview": rel(LOG_CONCAVE_OVERVIEW_MD),
        "agent_execution_pack": rel(LOG_CONCAVE_EXECUTION_PACK_MD),
        "shared_roots": chewi_shared_root_rows(),
        "blue_red_lean_tree": log_concave_lean_tree_status_rows(),
        "chapter_map": log_concave_chapter_map_rows(),
        "chapter_subtrees": chewi_chapter_rows(),
        "open_leaf_queue": chewi_open_leaf_rows(),
        "api_audit": chewi_api_audit_rows(),
    }
    retrieval_path = RETRIEVAL_INDEX_DIR / "ASTIS-CHEWI-001.json"
    write_text(retrieval_path, json.dumps(retrieval, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    outputs.append(retrieval_path)
    return outputs


def leaf_packet_brief_text() -> str:
    return """# Lower-Agent Mathlib-Ready Leaf Packet

Use this brief when assigning lower agents to reusable SDE/Sampling lemmas.

## Assignment Rule

One packet, one theorem.  Do not change the theorem statement unless the
reviewer or upper director has identified a mathematical issue.

## Required Output

- final theorem name and file;
- proof route actually tried;
- exact Mathlib or ASTIS declarations reused;
- hidden regularity contracts consumed;
- whether the target compiled;
- if blocked, the mathematical signal: missing assumption, false statement,
  API mismatch, representative mismatch, or too-large target.

## Anti-Churn Rule

After repeated failure, stop editing the proof script.  Return a smaller leaf
or a statement diagnosis.  This is especially important for measure theory,
conditional laws, weak Fokker--Planck identities, and KL/FI algebra.
"""


def write_mathlib_ready_leaf_docs() -> list[Path]:
    outputs: list[Path] = []
    path_texts = [
        (ROOT / "docs" / "mathlib_ready_leaf_protocol.md", mathlib_ready_leaf_protocol_text()),
        (LEMMA_DAG_DIR / "README.md", "# Lemma DAGs\n\nThis folder stores Mathlib-ready dependency graphs for reusable SDE/Sampling leaf lemmas.\n\nKey ledgers:\n\n- `log_concave_sampling_foundation.md` is the active log-concave sampling chapter/theorem DAG and shared-root taxonomy.\n- `SDE_Sampling_skill_tree.md` is the generic reusable proof-skill tree.\n- `SALD_weak_fp_leaf_dag.md` is a downstream consumer pressure-test DAG.\n\nRun:\n\n```bash\npython3 tools/astis.py lemma-dag-refresh\n```\n\n"),
        (LEMMA_DAG_DIR / "SDE_Sampling_skill_tree.md", sde_sampling_skill_tree_text()),
        (LEMMA_DAG_DIR / "SALD_weak_fp_leaf_dag.md", sald_weak_fp_leaf_dag_text()),
        (LEMMA_DAG_DIR / "Pro_assimilated_leaf_targets.md", pro_assimilated_leaf_targets_text()),
        (ROOT / "docs" / "assets" / "sampling_lemma_dag.mmd", sampling_lemma_dag_mmd_text()),
        (ROOT / "docs" / "assets" / "sampling_sde_leaf_network.svg", sampling_sde_leaf_network_svg()),
        (AGENT_BRIEFS_DIR / "mathlib_ready_leaf_packet.md", leaf_packet_brief_text()),
        (ROOT / "docs" / "mathlib_ready_leaf_reviewer_checklist.md", mathlib_leaf_reviewer_checklist_text()),
        (AGENT_BRIEFS_DIR / "mathlib_ready_leaf_reviewer_checklist.md", mathlib_leaf_reviewer_checklist_text()),
    ]
    for path, text in path_texts:
        write_text(path, text)
        outputs.append(path)

    outputs.extend(write_chewi_foundation_docs())

    leaf_png = ROOT / "docs" / "assets" / "sampling_sde_leaf_network.png"
    if render_svg_preview(ROOT / "docs" / "assets" / "sampling_sde_leaf_network.svg", leaf_png):
        outputs.append(leaf_png)

    mirror_path_texts = [
        (TECHNICAL_LEMMAS_DIR / "README.md", technical_lemmas_readme_text(), LEGACY_TECHNICAL_LEMMA_MEMORY_DIR / "README.md"),
        (TECHNICAL_LEMMAS_DIR / "mathlib_ready_leaf_template.md", mathlib_ready_leaf_template_text(), LEGACY_TECHNICAL_LEMMA_MEMORY_DIR / "mathlib_ready_leaf_template.md"),
        (TECHNICAL_LEMMAS_DIR / "hidden_regularities.md", hidden_regularities_text(), LEGACY_TECHNICAL_LEMMA_MEMORY_DIR / "hidden_regularities.md"),
    ]
    for primary, text, mirror in mirror_path_texts:
        write_text_mirror(primary, text, [mirror])
        outputs.extend([primary, mirror])

    retrieval = {
        "generated": now_stamp(),
        "protocol": "mathlib-ready-leaf",
        "mathlib_url": MATHLIB_URL,
        "canonical_docs": [rel(path) for path in outputs if "technical-lemma-memory" not in rel(path)],
        "leaf_network_svg": "docs/assets/sampling_sde_leaf_network.svg",
        "rules": [
            "decompose aggressively",
            "specify theorem plus APIs plus proof route",
            "treat persistent failure as mathematical signal",
            "make hidden regularity reusable",
            "do not frequently change the proof",
            "search Mathlib before inventing local lemmas",
            "review every callable leaf against the Mathlib-ready checklist",
        ],
        "next_sald_dag": rel(LEMMA_DAG_DIR / "SALD_weak_fp_leaf_dag.md"),
        "pro_assimilated_leaf_targets": rel(LEMMA_DAG_DIR / "Pro_assimilated_leaf_targets.md"),
    }
    retrieval_path = RETRIEVAL_INDEX_DIR / "mathlib-ready-leaf-protocol.json"
    write_text(retrieval_path, json.dumps(retrieval, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    outputs.append(retrieval_path)
    return outputs


def cmd_lemma_dag_refresh(_: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    outputs = write_mathlib_ready_leaf_docs()
    for path in outputs:
        add_manifest("astis.py lemma-dag-refresh", path, "memory", "Refreshed Mathlib-ready SDE/Sampling leaf lemma memory")
    print("lemma-dag-refresh wrote:")
    for path in outputs:
        print(f"- {rel(path)}")
    return 0


ARSENAL_MODULE_SUMMARIES: dict[str, dict[str, str]] = {
    "AutoSamplingTheory.Core": {
        "layer": "foundation",
        "summary": "source anchors, proof obligations, theorem contracts, DAG records",
        "status": "ASTIS infrastructure; not Mathlib material",
    },
    "AutoSamplingTheory.Probability": {
        "layer": "generic technical core",
        "summary": "law-map rewrites, dominated law derivatives, conditional-law bridges, KL/DV/LSI bookkeeping",
        "status": "main Mathlib-ready adapter surface after naming/generalization cleanup",
    },
    "AutoSamplingTheory.SDE": {
        "layer": "contract layer",
        "summary": "Ito diffusion, Fokker--Planck, Euler--Maruyama, discretization contracts",
        "status": "ASTIS contract surface; future executable SDE theorem layer",
    },
    "AutoSamplingTheory.TechnicalLemmas.Gaussian": {
        "layer": "compatibility source",
        "summary": "source file for ASTIS-owned Gaussian coordinate and moment leaves",
        "status": "legacy import surface; prefer TechnicalLemmas.ProbabilityDistributions.Gaussian",
    },
    "AutoSamplingTheory.TechnicalLemmas.Measure": {
        "layer": "compatibility source",
        "summary": "compatibility aggregator for measure, Gibbs, law-map, conditional-kernel, and RN/withDensity lemmas",
        "status": "legacy search surface; prefer TechnicalLemmas.Measure.* and TechnicalLemmas.Probability.* for new work",
    },
    "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "ENNReal Gibbs density, positivity/finite-value, measurability, nonzero/finite-by-envelope, potential-envelope, and finite-measure lower-bound integral contracts, plus normalized withDensity probability bridges",
        "status": "preferred Mathlib-style location for Gibbs target-measure wrappers",
    },
    "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "Bochner integral rewrites for Gibbs withDensity measures, turning `Z⁻¹ * gibbsDensityENNReal V` integrals into real `Z.toReal⁻¹ * exp(-V)` weighted base-measure integrals",
        "status": "preferred bridge from Gibbs target-measure wrappers to weak-generator, invariant-law, and KL/FI test-function algebra; does not prove normalization",
    },
    "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "finite nonzero ENNReal normalizer bridge from normalized Gibbs densities to real-valued LogConcaveOn shapes for convex and strongly convex potentials",
        "status": "preferred bridge between measure-facing Gibbs density wrappers and real-valued log-concavity geometry; does not prove normalizer finiteness",
    },
    "AutoSamplingTheory.TechnicalLemmas.Measure.Product": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "finite product-measure coordinate replacement map, measure-preserving wrapper, Bochner integral rewrite, and a.e. slice integrability for `Function.update` coordinate refreshes",
        "status": "preferred Mathlib-style location for product-measure coordinate update and slice/Fubini leaves; does not prove kernels, entropy, LSI, or invariance",
    },
    "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "withDensity mass, reciprocal-lintegral normalization, finite-pi product density decomposition, measurable-equivalence density transport, absolute-continuity, and RN reconstruction wrappers",
        "status": "preferred Mathlib-style location for density normalization and RN derivative leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.Probability": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for probability technical lemmas",
        "status": "preferred parent module for law-map and conditional-kernel leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.Probability.LawMap": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "pushforward law, weak-test integral, and dominated derivative transport leaves",
        "status": "preferred Mathlib-style location for law-map leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "condDistrib/condExpKernel bridges and conditional-integral regularity leaves",
        "status": "preferred Mathlib-style location for conditional-kernel leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for distribution-specific reusable leaves",
        "status": "preferred parent module for Gaussian and future Gamma/Ornstein--Uhlenbeck distribution leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "Gaussian coordinate laws, finite linear-form integrability/mean-zero, product MGF normalizers, Esscher shifted densities/change-of-measure, EuclideanSpace/stdGaussian change-of-measure bridges, and variance-one packaging",
        "status": "preferred Mathlib-style location for Gaussian/Brownian increment leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.Geometry": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for convex-geometric and log-concavity leaves",
        "status": "preferred parent module for CONV/DENS roots",
    },
    "AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "finite-dimensional EuclideanSpace coordinate bridges, including inner-product coordinate-sum identities for direct vectors and `WithLp.toLp 2` coordinate functions",
        "status": "preferred shared GEOM/GAUSS/SDE notation bridge; does not define gradients, divergence, Laplacian, or analytic regularity",
    },
    "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "positive-function log-concavity API over Mathlib ConcaveOn; negative-log potential convexity and energy sublevels; quasiconcavity, convex superlevel sets, and restricted superlevel log-concavity; linear/affine precomposition; products, nonnegative powers, product-domain tensorization; norm-square, absolute-linear, and centered/shifted/two-point quadratic-potential convexity; explicit normalized quadratic, Laplace, and Gaussian-kernel log-concavity",
        "status": "compiled CONV/DENS leaf with density-to-potential extraction, level-set/restriction geometry, map-stability, algebra, one-dimensional Laplace geometry, and centered/shifted/two-point quadratic Gibbs geometry; extend toward Prekopa-Leindler interfaces",
    },
    "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "strong-convexity to convex-potential/log-concave Gibbs-shape bridges and the midpoint `k/4` centered quadratic lower envelope from a supplied global minimizer",
        "status": "compiled CONV/DENS bridge; sharp `k/2` first-order envelope and minimizer-existence theory remain separate red branches",
    },
    "AutoSamplingTheory.TechnicalLemmas.Taylor": {
        "layer": "compatibility source",
        "summary": "source file for ASTIS-owned Taylor/Hessian and quadratic-normalization leaves",
        "status": "legacy import surface; prefer TechnicalLemmas.Analysis.Calculus.Taylor",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for reusable analysis and integrability leaves",
        "status": "preferred parent module for calculus, integrability, regularity, and future IBP leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for smooth cutoffs, gradient, line-derivative, Laplacian, Taylor/Hessian, pointwise coordinate-divergence, WithLp/Pi a.e. trace bridge, trace-to-coordinate `IntegrableOn` transfer, and finite-box face-term wrapper leaves used by SDE/Sampling proofs",
        "status": "preferred parent module for calculus leaves before explicit trace-integrability, IBP, and domain contracts",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "smooth unit and radial cutoffs, range bounds, support control, compact support, pointwise exhaustion, compact-in-open plateaus, and scale-uniform first- and second-derivative control",
        "status": "compiled ANALYSIS/REG/SDE base through O(R^-1) fderiv and O(R^-2) second iterated derivative; the finite-dimensional Laplacian trace consumer is compiled in Laplacian",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "Mathlib gradient bridges for Langevin calculus: Gibbs-weight chain rule `∇ exp(-V) = -exp(-V) • ∇V` from `HasGradientAt` or `DifferentiableAt`, coordinate displays, finite-dimensional coordinate-unit line derivatives, and pointwise `fderiv`-to-`gradient` inner-product/coordinate bridges",
        "status": "preferred ANALYSIS/SDE bridge from Mathlib gradient API to finite-coordinate Langevin algebra; pointwise only, with no divergence, IBP, or invariant-law claims",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "finite-dimensional pointwise coordinate-divergence convention, fderiv trace bridges, radial-cutoff PiLp derivative producer, smulRight basis-trace identity, the generic L1 cutoff-gradient limit and generic cutoff main-term dominated convergence for Integrable fields, a.e. trace transfer, finite-box signed face-term wrappers, and the inner-closed-Pi-box/outer-open-Pi-box plateau specialization",
        "status": "preferred ANALYSIS/SDE bridge for finite-box cancellation and the compiled generic cutoff cross-term/main-term/tail limits; concrete compact-test generator-display integrability and Gibbs-tail convergence are compiled in Langevin, while whole-space IBP, no-boundary passage, and invariant law remain separate",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "line-derivative product-rule and second-derivative wiring bridges for finite-coordinate weighted-product calculations, including equality-form `lineDeriv`, explicit `exp(-V) * g` coordinate leaves, and `fderiv`-to-`iteratedFDeriv` coordinate leaves",
        "status": "preferred ANALYSIS/SDE bridge for the product-rule and Hessian-coordinate components before divergence, IBP, or invariant-law contracts",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "finite-dimensional real inner-product-space Laplacian coordinate bridges: Mathlib Laplacian equals the standard orthonormal-basis second-derivative sum, plus source-functional handoff",
        "status": "preferred ANALYSIS/SDE bridge for Langevin generator displays; does not prove IBP, boundary decay, stationarity, or invariant laws",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Taylor": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "Hessian/operator norm bridges, orthonormal-basis units, quadratic normalization",
        "status": "preferred Mathlib-style location for Ito/Taylor local-error leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "ofReal lintegral/Integrable bridge, finite-dimensional Gaussian quadratic-tail integrability, exact quadratic normalizers, exact one-dimensional Laplace normalizers, and quadratic/Laplace lower-bound Gibbs normalization leaves",
        "status": "preferred Mathlib-style location for Lebesgue tail and coercive-envelope leaves; general coercive envelopes remain red",
    },
    "AutoSamplingTheory.TechnicalLemmas.InformationTheory": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for KL/DV/Renyi/entropy technical lemmas",
        "status": "preferred parent module for information-theoretic leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.InformationTheory.DonskerVaradhan": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "Donsker--Varadhan one-sided and scaled-test energy leaves",
        "status": "preferred Mathlib-style location for DV/KL energy leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.InformationTheory.KLDensity": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "KL-density pointwise derivative and mass-conservation algebra leaves",
        "status": "preferred Mathlib-style location for KL density algebra after analytic domination is supplied",
    },
    "AutoSamplingTheory.TechnicalLemmas.InformationTheory.Renyi": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "Renyi density integrand positivity, measurability, finite-envelope, and pointwise derivative algebra leaves",
        "status": "preferred Mathlib-style location for Renyi density algebra before integral/path regularity contracts",
    },
    "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for LSI/FI/PI-style technical lemmas",
        "status": "preferred parent module for functional-inequality leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolev": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "log-Sobolev to KL/FI bookkeeping leaves",
        "status": "preferred Mathlib-style location for LSI/FI bookkeeping leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for weak-generator, Fokker--Planck algebra, Langevin generator, and finite-dimensional Girsanov cylinder leaves",
        "status": "preferred parent module for SDE/Sampling stochastic-process leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "sample-space generator derivative to named law weak-generator rewrite",
        "status": "preferred Mathlib-style location for weak FP generator bridge leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "Fokker--Planck split and Fisher/IBP scalar algebra leaves",
        "status": "preferred Mathlib-style location for weak FP and Fisher algebra handoffs",
    },
    "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "finite-dimensional pointwise display for the formal differential expression `Δ f - <∇V, ∇f>`, supplied coordinate-to-Mathlib weighted-divergence handoffs, `exp(-V)` handoffs, coordinate-sum and coordinateDivergence displays, finite-box trace regularity, whole-space Gibbs-weighted source-field and compact-test generator-display integrability, and Gibbs-tail convergence",
        "status": "preferred Mathlib-style location for Langevin expression algebra and the compiled source-field, compact-test generator-display, and Gibbs-tail leaves before IBP, invariant-law, Ito-generator, and semigroup-domain contracts",
    },
    "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Girsanov": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "finite-dimensional cylindrical Gaussian Girsanov weight, RN/withDensity identity, change-of-measure, and normalization leaves",
        "status": "preferred Mathlib-style location for PATH change-of-measure bridge leaves",
    },
    "AutoSamplingTheory.TechnicalLemmas.Variational": {
        "layer": "compatibility source",
        "summary": "compatibility aggregator for DV and LSI/FI leaves",
        "status": "legacy search surface; prefer InformationTheory and FunctionalInequalities modules",
    },
    "AutoSamplingTheory.TechnicalLemmas.Registry": {
        "layer": "memory index",
        "summary": "compiled lemma-memory metadata and external port queue",
        "status": "agent retrieval registry, not theorem content",
    },
    "AutoSamplingTheory.TechnicalLemmas": {
        "layer": "Mathlib-ready technical lemma",
        "summary": "parent import surface for reusable ASTIS-owned technical lemmas",
        "status": "public import surface for the Mathlib-ready arsenal; excludes SALDExtracted quarantine",
    },
    "AutoSamplingTheory.TechnicalLemmas.SALDExtracted": {
        "layer": "paper-extracted technical lemma",
        "summary": "compiled SALD-derived Brownian/Ito/Gronwall bridges exposed for search",
        "status": "compiled and useful; must be generalized before Mathlib submission",
    },
    "AutoSamplingTheory.SALD": {
        "layer": "paper consumer",
        "summary": "SALD case-study theorem contracts, compiled sublemmas, obligations",
        "status": "consumer of arsenal; no longer the center of the public library map",
    },
    "AutoSamplingTheory.RMFLD": {
        "layer": "exploratory consumer",
        "summary": "exploratory sampling-theory proof targets",
        "status": "consumer of arsenal",
    },
    "AutoSamplingTheory.Automation": {
        "layer": "harness",
        "summary": "compiled process contracts, role contracts, acceptance gates",
        "status": "automation metadata",
    },
    "AutoSamplingTheory.Literature": {
        "layer": "reference registry",
        "summary": "paper/source registry",
        "status": "metadata",
    },
    "AutoSamplingTheory.OpenProblems": {
        "layer": "exploration registry",
        "summary": "open problem registry",
        "status": "metadata",
    },
    "AutoSamplingTheory": {
        "layer": "root",
        "summary": "public root import surface",
        "status": "module root",
    },
}


def module_name_from_lean_path(path: Path) -> str:
    if path == ROOT / "AutoSamplingTheory.lean":
        return "AutoSamplingTheory"
    relative = path.relative_to(ROOT).with_suffix("")
    return ".".join(relative.parts)


def lean_module_records() -> list[dict]:
    files = [*sorted((ROOT / "AutoSamplingTheory").rglob("*.lean")), ROOT / "AutoSamplingTheory.lean"]
    records: list[dict] = []
    for path in files:
        if not path.exists():
            continue
        text = read_text(path)
        module = module_name_from_lean_path(path)
        imports = re.findall(r"^import\s+([A-Za-z0-9_.'/-]+)$", text, flags=re.M)
        decls = [
            {"kind": match.group(1), "name": match.group(2)}
            for match in re.finditer(
                LEAN_DECL_NAME_REGEX.pattern,
                strip_lean_comments_and_strings(text),
                flags=re.M,
            )
        ]
        exported: list[str] = []
        for block in re.findall(r"export\s+[A-Za-z0-9_.']+\s*\((.*?)\)", text, flags=re.S):
            exported.extend(re.findall(r"[A-Za-z][A-Za-z0-9_'.]*", block))
        records.append({
            "module": module,
            "path": rel(path),
            "imports": imports,
            "local_imports": [item for item in imports if item.startswith("AutoSamplingTheory")],
            "declarations": decls,
            "exports": sorted(set(exported)),
            "summary": ARSENAL_MODULE_SUMMARIES.get(module, {}).get("summary", ""),
            "layer": ARSENAL_MODULE_SUMMARIES.get(module, {}).get("layer", "uncategorized"),
            "status": ARSENAL_MODULE_SUMMARIES.get(module, {}).get("status", ""),
        })
    return records


def module_record_map(records: list[dict]) -> dict[str, dict]:
    return {record["module"]: record for record in records}


def local_lean_module_names() -> list[str]:
    files = [*sorted((ROOT / "AutoSamplingTheory").rglob("*.lean")), ROOT / "AutoSamplingTheory.lean"]
    return sorted(
        {module_name_from_lean_path(path) for path in files if path.exists()},
        key=len,
        reverse=True,
    )


def module_for_local_decl(decl: str, module_names: list[str]) -> str:
    for module in module_names:
        if decl == module or decl.startswith(module + "."):
            return module
    return decl.rsplit(".", 1)[0]


def module_decl_names(record: dict, limit: int = 8) -> list[str]:
    names = [decl["name"] for decl in record.get("declarations", [])]
    names.extend(record.get("exports", []))
    deduped: list[str] = []
    for name in names:
        if name not in deduped:
            deduped.append(name)
    return deduped[:limit]


def formalized_memory_entries_by_module() -> dict[str, list[dict[str, str]]]:
    registry = ROOT / "AutoSamplingTheory" / "TechnicalLemmas" / "Registry.lean"
    if not registry.exists():
        return {}
    text = read_text(registry)
    module_names = local_lean_module_names()
    entries: dict[str, list[dict[str, str]]] = {}
    for block in re.findall(r"\{\s*key := .*?\n\s*\}", text, flags=re.S):
        status = re.search(r"status\s*:=\s*LemmaMemoryStatus\.([A-Za-z0-9_]+)", block)
        local_decl = re.search(r'localDecl\s*:=\s*"([^"]*)"', block)
        key = re.search(r'key\s*:=\s*"([^"]*)"', block)
        upstream = re.search(r'upstreamFile\s*:=\s*"([^"]*)"', block)
        if not status or status.group(1) != "formalizedLocal":
            continue
        if not local_decl or not local_decl.group(1):
            continue
        decl = local_decl.group(1)
        module = module_for_local_decl(decl, module_names)
        entries.setdefault(module, []).append({
            "key": key.group(1) if key else decl.rsplit(".", 1)[-1],
            "decl": decl,
            "upstream": upstream.group(1) if upstream else "",
        })
    return entries


def canonical_arsenal_modules() -> set[str]:
    return {
        module
        for module in arsenal_module_coords()
        if module not in {"AutoSamplingTheory", "AutoSamplingTheory.TechnicalLemmas"}
    }


def mathlib_readiness_tier(record: dict, memory_count: int) -> tuple[str, str, str]:
    module = record["module"]
    decl_count = len(record.get("declarations", [])) + len(record.get("exports", []))
    if module == "AutoSamplingTheory.Probability":
        return (
            "adapter-surface",
            "compiled local adapter surface; too broad for direct upstreaming as one unit",
            "split reusable declarations into family modules before proposing upstream",
        )
    if memory_count > 0:
        return (
            "compiled-local-candidate",
            "locally compiled and registered as callable technical lemma memory",
            "review names, imports, assumptions, and theorem generality against Mathlib conventions",
        )
    if decl_count == 0:
        return (
            "parent-import-surface",
            "compiled parent file with no direct mathematical declarations",
            "keep as project organization; upstream individual child leaves instead",
        )
    return (
        "compiled-local-unreviewed",
        "compiled declarations exist but are not yet curated as formalized memory entries",
        "add reviewer audit rows or move non-upstream declarations out of the canonical arsenal",
    )


def mathlib_readiness_audit(records: list[dict]) -> tuple[Path, Path]:
    memory_entries = formalized_memory_entries_by_module()
    by_module = module_record_map(records)
    rows: list[dict[str, str]] = []
    for module in sorted(canonical_arsenal_modules()):
        record = by_module.get(module)
        if not record:
            continue
        memory_count = len(memory_entries.get(module, []))
        tier, reviewer_status, next_action = mathlib_readiness_tier(record, memory_count)
        decls = module_decl_names(record, limit=12)
        rows.append({
            "module": f"`{module}`",
            "file": f"`{record['path']}`",
            "tier": tier,
            "compiled_items": str(len(record.get("declarations", [])) + len(record.get("exports", []))),
            "memory_entries": str(memory_count),
            "representative_items": ", ".join(f"`{name}`" for name in decls) or "none",
            "reviewer_status": reviewer_status,
            "next_action": next_action,
        })
    table = markdown_table(rows, [
        ("Module", "module"),
        ("File", "file"),
        ("Tier", "tier"),
        ("Compiled items", "compiled_items"),
        ("Memory entries", "memory_entries"),
        ("Representative items", "representative_items"),
        ("Reviewer status", "reviewer_status"),
        ("Next action", "next_action"),
    ])
    md_path = SAMPLING_LIBRARY_DIR / "mathlib-readiness-audit.md"
    json_path = RETRIEVAL_INDEX_DIR / "mathlib-readiness-audit.json"
    text = f"""# Mathlib Readiness Audit For The ASTIS SDE/Sampling Arsenal

Generated: `{now_stamp()}`

This audit is deliberately stricter than "the file builds".  A declaration is
callable inside ASTIS after it compiles and appears in technical lemma memory.
It becomes a Mathlib-upstream candidate only after reviewer agents check its
generality, naming, imports, hidden regularity assumptions, and proof route.

The main module graph shows the canonical local arsenal.  This audit explains
what still separates those compiled leaves from an actual Mathlib contribution.

## Reviewer Rules

- Decompose aggressively: one candidate row should lead to one small theorem or
  one small file-cleanup packet.
- Specify more than the theorem: include local APIs, minimal imports, hidden
  assumptions, and intended proof route.
- Treat persistent failure as mathematical signal: recheck the statement for
  missing assumptions or counterexamples.
- Make hidden regularity reusable: measurability, integrability, continuity,
  nonemptiness, boundedness, and domination hypotheses belong in theorem
  contracts.
- Do not frequently change the proof route unless the reviewer identifies a
  real statement problem.

## Current Canonical Arsenal

{table}

## Interpretation

`compiled-local-candidate` means ASTIS has a local proof and the declaration is
registered as callable technical lemma memory.  It does not mean the theorem is
already formatted for a Mathlib pull request.  `parent-import-surface` files are
useful project organization, but their child declarations are the upstreamable
objects.  `adapter-surface` files contain useful glue and should be split before
upstream review.
"""
    write_text(md_path, text)
    payload = {
        "generated": now_stamp(),
        "rows": rows,
        "rules": [
            "decompose aggressively",
            "specify theorem plus APIs and proof route",
            "treat repeated failure as statement signal",
            "make hidden regularity reusable",
            "do not frequently change the proof",
        ],
    }
    write_text(json_path, json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    return md_path, json_path


def log_concave_sampling_to_lean_roadmap() -> tuple[Path, Path]:
    md_path = SAMPLING_LIBRARY_DIR / "roadmap" / "log_concave_sampling_to_lean_tree.md"
    json_path = RETRIEVAL_INDEX_DIR / "log-concave-sampling-to-lean-tree.json"
    rows = [
        {
            "source": row["chapter"],
            "lean_family": row["dag"],
            "first_leaf": row["first_leaf"],
            "status": row["status"],
            "review": f"reuse shared roots {row['shared']}; create a separate subtree when the theorem becomes active",
        }
        for row in chewi_chapter_rows()
    ]
    table = markdown_table(rows, [
        ("Textbook source", "source"),
        ("Target Lean family", "lean_family"),
        ("First small leaf", "first_leaf"),
        ("Status", "status"),
        ("Reviewer warning", "review"),
    ])
    text = f"""# Log-Concave Sampling To Lean Foundation Roadmap

Generated: `{now_stamp()}`

Reference PDF: `{CHEWI_LOG_CONCAVE_URL}`

Local primary copy: `{CHEWI_LOG_CONCAVE_PDF}`

Local legacy mirror: `{CHEWI_LEGACY_PDF}`

This roadmap is not a theorem dependency.  It is a textbook-to-Lean planning
map.  Textbook statements are often intentionally informal; ASTIS agents must
turn them into small theorem contracts with hidden regularity assumptions before
assigning lower Lean work.  The matching visual ledger is
`{rel(LOG_CONCAVE_FOUNDATION_DAG_MD)}`.

## Roadmap

{table}

## Agent Protocol

1. Start with Mathlib search and the current ASTIS arsenal.
2. If a textbook claim is useful, decompose it into one local theorem packet.
3. State measurability, integrability, continuity, nonemptiness, boundedness,
   domination, and boundary assumptions explicitly.
4. Use external Lean projects such as `lean-stat-learning-theory` and
   `lean-rademacher` as reference memory only; callable lemmas must be
   ASTIS-owned declarations that build locally.
5. If a packet fails repeatedly, audit the mathematical statement instead of
   changing the proof script.

## Current Priority

Do not attempt to formalize the whole textbook in one pass.  The next reusable
growth path is:

- lock the shared-root taxonomy (`MEAS`, `KERN`, `DENS`, `GAUSS`, `CONV`,
  `FI`, `SDE`, `PATH`, `DISC`, `REG`);
- the Ch.1 Langevin cutoff branch now includes the compiled local,
  compact-in-open, Pi-box, radial, scale-uniform `O(R⁻¹)` first-derivative,
  closed-outer derivative-zero, Pi derivative/trace bases, the generic
  `L¹` cutoff-gradient integral limit from `Integrable G`, the concrete
  Gibbs/source-field `Integrable` premise, and generic cutoff main-term dominated convergence;
- the compact-support whole-space divergence theorem and Gibbs-weighted identity
  `integral exp(-V) Lf = 0` for `C_c^2` tests are compiled;
- reuse the compiled `O(R⁻²)` radial Hessian/Laplacian bounds when a
  second-order consumer reaches the frontier;
- the explicit core-domain contract and abstract semigroup pairing derivative
  bridge compile; next instantiate them for the actual Langevin evolution and
  prove the domain extension before stating the invariant Gibbs law;
- in parallel, extend from the compiled log-concavity density-to-potential
  extraction, level-set geometry, algebra, and centered/shifted/two-point
  quadratic Gibbs geometry toward Prekopa-Leindler and nonquadratic coercive
  Gibbs envelopes;
- generalize existing law-map, conditional-kernel, Gaussian, KL, weak-generator,
  and LSI bookkeeping leaves away from paper-specific naming;
- add one subtree per chapter/theorem only when it reuses shared roots;
- keep algorithm theorems as consumers until their root leaves compile locally.
"""
    write_text(md_path, text)
    write_text(json_path, json.dumps({
        "generated": now_stamp(),
        "pdf": str(CHEWI_LOG_CONCAVE_PDF),
        "legacy_pdf": str(CHEWI_LEGACY_PDF),
        "public_pdf": CHEWI_LOG_CONCAVE_URL,
        "rows": rows,
        "shared_roots": chewi_shared_root_rows(),
        "open_leaf_queue": chewi_open_leaf_rows(),
    }, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    return md_path, json_path


def arsenal_module_coords() -> dict[str, tuple[int, int, int, int]]:
    return {
        "AutoSamplingTheory.Probability": (675, 75, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.Probability.LawMap": (70, 190, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel": (400, 190, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian": (730, 190, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Taylor": (1060, 190, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.InformationTheory.KLDensity": (1390, 190, 330, 56),
        "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff": (70, 255, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence": (400, 255, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient": (730, 255, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian": (1060, 255, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability": (1390, 255, 330, 56),
        "AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity": (70, 320, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator": (400, 320, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra": (730, 320, 330, 56),
        "AutoSamplingTheory.TechnicalLemmas.InformationTheory.DonskerVaradhan": (1060, 320, 300, 56),
        "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolev": (1390, 320, 330, 56),
        "AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates": (70, 390, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Girsanov": (400, 390, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin": (730, 390, 330, 54),
        "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym": (70, 455, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs": (400, 455, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral": (70, 520, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.Probability": (730, 455, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions": (1060, 455, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus": (1390, 455, 330, 54),
        "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity": (400, 520, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity": (730, 520, 330, 54),
        "AutoSamplingTheory.TechnicalLemmas.Measure.Product": (1060, 520, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.InformationTheory.Renyi": (1390, 520, 330, 54),
        "AutoSamplingTheory.TechnicalLemmas.Geometry": (70, 580, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses": (400, 580, 330, 54),
        "AutoSamplingTheory.TechnicalLemmas.InformationTheory": (730, 580, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.Analysis": (1060, 580, 300, 54),
        "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities": (1390, 580, 330, 54),
        "AutoSamplingTheory.TechnicalLemmas": (765, 705, 330, 58),
        "AutoSamplingTheory": (765, 805, 330, 54),
    }


def arsenal_node_style(layer: str) -> tuple[str, str]:
    if layer == "root":
        return "#eaf2ff", "#2563eb"
    if "Mathlib-ready" in layer or layer == "generic technical core":
        return "#dff0e4", "#2e7d59"
    if layer == "compatibility source":
        return "#f1f5f9", "#64748b"
    if layer == "paper-extracted technical lemma":
        return "#f8e5d0", "#d97924"
    if layer.endswith("consumer"):
        return "#f4f1f8", "#8d7aa8"
    if layer in {"foundation", "contract layer"}:
        return "#d8eef6", "#214e8a"
    if layer in {"memory index"}:
        return "#f8fafc", "#2e7d59"
    return "#f8fafc", "#7f8da3"


def module_title_lines(module: str) -> list[str]:
    if module == "AutoSamplingTheory":
        return ["AutoSamplingTheory"]
    for family in [
        "Probability",
        "ProbabilityDistributions",
        "Measure",
        "Analysis",
        "Geometry",
        "InformationTheory",
        "FunctionalInequalities",
        "StochasticProcesses",
    ]:
        prefix = f"AutoSamplingTheory.TechnicalLemmas.{family}."
        if module.startswith(prefix):
            display_family = {
                "ProbabilityDistributions": "ProbDistributions",
                "FunctionalInequalities": "FuncInequalities",
                "InformationTheory": "InformationTheory",
                "StochasticProcesses": "StochasticProcesses",
            }.get(family, family)
            return [f"TechnicalLemmas.{display_family}", "." + module.removeprefix(prefix)]
    prefix = "AutoSamplingTheory.TechnicalLemmas."
    if module.startswith(prefix):
        tail = module.removeprefix(prefix)
        display_tail = {
            "ProbabilityDistributions": "ProbDistributions",
            "FunctionalInequalities": "FuncInequalities",
        }.get(tail, tail)
        return ["TechnicalLemmas", "." + display_tail]
    if module.startswith("AutoSamplingTheory."):
        return ["AutoSamplingTheory", "." + module.removeprefix("AutoSamplingTheory.")]
    return [module]


def svg_rect_node(record: dict, x: int, y: int, w: int, h: int, memory_entries: dict[str, list[dict[str, str]]]) -> str:
    fill, stroke = arsenal_node_style(record.get("layer", ""))
    title_lines = [html.escape(line) for line in module_title_lines(record["module"])]
    decl_count = len(record.get("declarations", [])) + len(record.get("exports", []))
    curated_count = len(memory_entries.get(record["module"], []))
    file_label = Path(record.get("path", "")).name if record.get("path", "") else ""
    if record["module"] == "AutoSamplingTheory.TechnicalLemmas":
        subtitle = "parent import surface for reusable lemmas"
    elif record["module"] == "AutoSamplingTheory":
        subtitle = "root public import surface"
    elif curated_count:
        subtitle = html.escape(f"{file_label}; compiled {decl_count}; memory {curated_count}")
    else:
        subtitle = html.escape(f"{file_label}; compiled {decl_count}")
    return f"""
<g id="{html.escape(record['module'])}">
  <path fill="{fill}" stroke="{stroke}" stroke-width="1.8" d="M{x + 12},{y} L{x + w - 12},{y} Q{x + w},{y} {x + w},{y + 12} L{x + w},{y + h - 12} Q{x + w},{y + h} {x + w - 12},{y + h} L{x + 12},{y + h} Q{x},{y + h} {x},{y + h - 12} L{x},{y + 12} Q{x},{y} {x + 12},{y} Z"/>
  <text x="{x + w / 2:.1f}" y="{y + 16}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="700">{title_lines[0]}</text>
  {f'<text x="{x + w / 2:.1f}" y="{y + 31}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="12" font-weight="700">{title_lines[1]}</text>' if len(title_lines) > 1 else ''}
  <text x="{x + w / 2:.1f}" y="{y + 48}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="9" fill="#334155">{subtitle}</text>
</g>"""


def svg_edge(src_box: tuple[int, int, int, int], dst_box: tuple[int, int, int, int]) -> str:
    sx = src_box[0] + src_box[2] / 2
    sy = src_box[1] + src_box[3]
    dx = dst_box[0] + dst_box[2] / 2
    dy = dst_box[1]
    mid = (sy + dy) / 2
    return (
        f'<path d="M {sx:.1f} {sy:.1f} C {sx:.1f} {mid:.1f}, {dx:.1f} {mid:.1f}, {dx:.1f} {dy:.1f}" '
        'fill="none" stroke="#8a97aa" stroke-width="1.2" marker-end="url(#arrow)"/>'
    )


def arsenal_module_graph_svg(records: list[dict]) -> str:
    coords = arsenal_module_coords()
    by_module = module_record_map(records)
    memory_entries = formalized_memory_entries_by_module()
    curated_edges = [
        ("AutoSamplingTheory.Probability", "AutoSamplingTheory.TechnicalLemmas.Probability.LawMap"),
        ("AutoSamplingTheory.Probability", "AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel"),
        ("AutoSamplingTheory.Probability", "AutoSamplingTheory.TechnicalLemmas.InformationTheory.DonskerVaradhan"),
        ("AutoSamplingTheory.Probability", "AutoSamplingTheory.TechnicalLemmas.InformationTheory.KLDensity"),
        ("AutoSamplingTheory.Probability", "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolev"),
        ("AutoSamplingTheory.Probability", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator"),
        ("AutoSamplingTheory.TechnicalLemmas.Probability.LawMap", "AutoSamplingTheory.TechnicalLemmas.Probability"),
        ("AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel", "AutoSamplingTheory.TechnicalLemmas.Probability"),
        ("AutoSamplingTheory.TechnicalLemmas.Probability.LawMap", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator"),
        ("AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalKernel", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator"),
        ("AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Girsanov"),
        ("AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions.Gaussian", "AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions"),
        ("AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs", "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral"),
        ("AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs", "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity"),
        ("AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral", "AutoSamplingTheory.TechnicalLemmas.Measure"),
        ("AutoSamplingTheory.TechnicalLemmas.Measure.Product", "AutoSamplingTheory.TechnicalLemmas.Measure"),
        ("AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity", "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity"),
        ("AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity", "AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity"),
        ("AutoSamplingTheory.TechnicalLemmas.Measure.GibbsLogConcavity", "AutoSamplingTheory.TechnicalLemmas.Measure"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Taylor", "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence", "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient", "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv", "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian", "AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus", "AutoSamplingTheory.TechnicalLemmas.Analysis"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability", "AutoSamplingTheory.TechnicalLemmas.Analysis"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability", "AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs"),
        ("AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity", "AutoSamplingTheory.TechnicalLemmas.Geometry"),
        ("AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity", "AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity"),
        ("AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity", "AutoSamplingTheory.TechnicalLemmas.Geometry"),
        ("AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates", "AutoSamplingTheory.TechnicalLemmas.Geometry"),
        ("AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin"),
        ("AutoSamplingTheory.TechnicalLemmas.InformationTheory.DonskerVaradhan", "AutoSamplingTheory.TechnicalLemmas.InformationTheory"),
        ("AutoSamplingTheory.TechnicalLemmas.InformationTheory.KLDensity", "AutoSamplingTheory.TechnicalLemmas.InformationTheory"),
        ("AutoSamplingTheory.TechnicalLemmas.InformationTheory.Renyi", "AutoSamplingTheory.TechnicalLemmas.InformationTheory"),
        ("AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakGenerator", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses"),
        ("AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FokkerPlanckAlgebra", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses"),
        ("AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses"),
        ("AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Girsanov", "AutoSamplingTheory.TechnicalLemmas.StochasticProcesses"),
        ("AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolev", "AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities"),
        ("AutoSamplingTheory.TechnicalLemmas.ProbabilityDistributions", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas.Probability", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas.Analysis", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas.Geometry", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas.InformationTheory", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas.StochasticProcesses", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities", "AutoSamplingTheory.TechnicalLemmas"),
        ("AutoSamplingTheory.TechnicalLemmas", "AutoSamplingTheory"),
        ("AutoSamplingTheory.Probability", "AutoSamplingTheory"),
    ]
    edges = [
        svg_edge(coords[src], coords[dst])
        for src, dst in curated_edges
        if src in coords and dst in coords
    ]
    node_parts = []
    for module, box in coords.items():
        record = by_module.get(module, {
            "module": module,
            "layer": ARSENAL_MODULE_SUMMARIES.get(module, {}).get("layer", ""),
            "declarations": [],
            "exports": [],
            "path": "",
        })
        node_parts.append(svg_rect_node(record, *box, memory_entries))
    generated = html.escape(now_stamp())
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="1780" height="980" viewBox="0 0 1780 980" xmlns="http://www.w3.org/2000/svg">
<defs>
  <marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
    <polygon points="0 0, 9 3.5, 0 7" fill="#8a97aa"/>
  </marker>
</defs>
<rect width="1780" height="980" fill="white"/>
<text x="890" y="34" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="24" font-weight="700" fill="#1f2933">ASTIS Mathlib-Ready SDE/Sampling Lean Arsenal</text>
<text x="890" y="60" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#475569">Canonical local modules only: compiled ASTIS-owned technical leaves and their parent import surfaces.  Paper consumers and external projects are documented in ledgers, not shown as arsenal nodes.</text>
<g id="edges">
{chr(10).join(edges)}
</g>
<g id="nodes">
{chr(10).join(node_parts)}
</g>
<g id="legend">
  <rect x="60" y="845" width="520" height="105" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="78" y="869" font-family="Helvetica,Arial,sans-serif" font-size="13" font-weight="700">Legend</text>
  <rect x="78" y="883" width="18" height="12" fill="#dff0e4" stroke="#2e7d59"/><text x="104" y="894" font-family="Helvetica,Arial,sans-serif" font-size="11">Canonical Mathlib-ready candidate module: compiled local reusable leaves</text>
  <rect x="78" y="905" width="18" height="12" fill="#eaf2ff" stroke="#2563eb"/><text x="104" y="916" font-family="Helvetica,Arial,sans-serif" font-size="11">Root public import surface</text>
  <text x="78" y="938" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="#475569">Omitted from the main graph: SALD/RMFLD consumers, SALDExtracted quarantine, compatibility files, registry metadata, and external references.</text>
  <text x="1260" y="955" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="#64748b">Generated {generated} by tools/astis.py module-graph-refresh</text>
</g>
</svg>
"""


def module_file_tree_text() -> str:
    return """Main graph tree:

AutoSamplingTheory
|-- Probability.lean                  shared probability adapter surface
|-- TechnicalLemmas.lean              parent import surface for reusable lemmas
`-- TechnicalLemmas/
    |-- Analysis.lean                 parent for reusable analysis leaves
    |-- Analysis/
    |   |-- Calculus.lean             parent for calculus leaves
    |   `-- Calculus/
    |       |-- Divergence.lean       Mathlib-style pointwise coordinate-divergence bridge
    |       |-- Gradient.lean         Mathlib-style gradient coordinate bridges
    |       |-- Laplacian.lean        Mathlib-style Laplacian coordinate bridges
    |       `-- Taylor.lean           Mathlib-style Taylor/Hessian leaves
    |-- Probability.lean              parent for probability technical lemmas
    |-- Probability/
    |   |-- LawMap.lean               pushforward-law and weak-test rewrites
    |   `-- ConditionalKernel.lean    condDistrib and conditional-integral leaves
    |-- ProbabilityDistributions.lean parent for distribution-specific leaves
    |-- ProbabilityDistributions/
    |   `-- Gaussian.lean             Mathlib-style Gaussian coordinate leaves
    |-- Measure/
    |   |-- Gibbs.lean                ENNReal Gibbs density and normalization bridge
    |   |-- GibbsIntegral.lean        Gibbs withDensity Bochner integral rewrites
    |   |-- GibbsLogConcavity.lean    normalized Gibbs real-density log-concavity bridge
    |   |-- Product.lean              product-measure coordinate update and Fubini leaves
    |   `-- RadonNikodym.lean         withDensity, density transport, and RN normalization leaves
    |-- Geometry.lean                 parent for convex-geometric leaves
    |-- Geometry/
    |   |-- EuclideanSpaceCoordinates.lean finite-dimensional inner-product coordinate bridges
    |   |-- LogConcavity.lean         positive log-concavity, negative-log potential, level-set, and centered/shifted/two-point quadratic Gibbs geometry leaves
    |   `-- StrongConvexity.lean      strong-convexity to log-concavity and quadratic-envelope bridges
    |-- StochasticProcesses.lean      parent for SDE/weak-generator leaves
    |-- StochasticProcesses/
    |   |-- WeakGenerator.lean        sample-to-law weak-generator rewrites
    |   |-- FokkerPlanckAlgebra.lean  FP split and Fisher/IBP algebra leaves
    |   |-- Langevin.lean             finite Langevin expression display and Gibbs-weighted algebra leaves
    |   `-- Girsanov.lean             finite-dimensional cylindrical change-of-measure leaves
    |-- InformationTheory.lean        parent for KL/DV/Renyi/entropy leaves
    |-- InformationTheory/
    |   |-- DonskerVaradhan.lean      one-sided DV and energy bounds
    |   |-- KLDensity.lean            KL density derivative algebra leaves
    |   `-- Renyi.lean                Renyi integrand and derivative leaves
    |-- FunctionalInequalities.lean   parent for LSI/FI/PI-style leaves
    `-- FunctionalInequalities/
        `-- LogSobolev.lean           LSI-to-KL/FI bookkeeping leaves

Compatibility surfaces not shown in the main graph:
|-- TechnicalLemmas/Gaussian.lean
|-- TechnicalLemmas/Taylor.lean
|-- TechnicalLemmas/Measure.lean
`-- TechnicalLemmas/Variational.lean

Non-arsenal files documented separately:
|-- Core.lean, SDE.lean, Automation.lean, Literature.lean, OpenProblems.lean
|-- TechnicalLemmas/Registry.lean
|-- TechnicalLemmas/SALDExtracted.lean
|-- SALD.lean
`-- RMFLD.lean
"""


def arsenal_module_graph_markdown(records: list[dict]) -> str:
    memory_entries = formalized_memory_entries_by_module()
    rows = []
    for record in records:
        module = record["module"]
        if module == "AutoSamplingTheory" or module not in arsenal_module_coords():
            continue
        leaves = ", ".join(f"`{name}`" for name in module_decl_names(record, limit=8)) or "exports/metadata only"
        if len(module_decl_names(record, limit=99)) > 8:
            leaves += ", ..."
        memory_count = len(memory_entries.get(module, []))
        rows.append({
            "module": f"`{module}`",
            "file": f"`{record['path']}`",
            "layer": record.get("layer", ""),
            "summary": record.get("summary", ""),
            "leaves": leaves,
            "memory_count": str(memory_count),
            "status": record.get("status", ""),
        })
    memory_rows = []
    extracted_memory_rows = []
    for module, entries in sorted(memory_entries.items()):
        for entry in entries:
            row = {
                "module": f"`{module}`",
                "key": f"`{entry['key']}`",
                "decl": f"`{entry['decl'].rsplit('.', 1)[-1]}`",
                "upstream": entry["upstream"] or "local",
            }
            if module.endswith(".SALDExtracted"):
                extracted_memory_rows.append(row)
            else:
                memory_rows.append(row)
    return f"""# ASTIS Lean Leaf Module Graph

This is the textual ledger behind `docs/module-graph.svg`.  The graph itself
shows only canonical ASTIS-owned Lean modules that are currently treated as the
Mathlib-ready SDE/Sampling proof-weapon library: compiled reusable leaves and
their parent import surfaces.

The graph is intentionally organized like a Lean module map, following the
style of the public QuantumComputing module graph.  Paper consumers, registry
metadata, compatibility files, and external references are not main graph
nodes.  They are documented below so the reusable arsenal stays visible at a
glance.

![ASTIS module graph](../../docs/module-graph.svg)

## Public Module Tree

```text
{module_file_tree_text()}```

## Log-Concave Sampling Planned Extension

`ASTIS-CHEWI-001` sets the library goal to a log-concave sampling foundation.
`Geometry.LogConcavity` now has
compiled core, density-to-potential extraction, level-set/restriction geometry, map-stability, tensorization algebra, and centered/shifted/two-point quadratic Gibbs geometry leaves; the
remaining planned modules are not callable until they contain ASTIS-owned compiled declarations, but they define the
intended scientific organization for new leaves:

```text
Planned log-concave sampling extension:

AutoSamplingTheory
`-- TechnicalLemmas/
    |-- Measure/
    |   |-- Transport.lean
    |   |-- Gibbs.lean
    |   `-- RadonNikodym.lean
    |-- Geometry/
    |   |-- Convex.lean
    |   |-- LogConcavity.lean  compiled core/potential/level-set/map/tensorization API plus centered/shifted/two-point quadratic Gibbs geometry
    |   `-- PrekopaLeindler.lean
    |-- FunctionalInequalities/
    |   |-- Poincare.lean
    |   |-- Transport.lean
    |   `-- Isoperimetry.lean
    |-- StochasticProcesses/
    |   |-- MarkovSemigroup.lean
    |   |-- Ito.lean
    |   |-- Langevin.lean
    |   |-- Girsanov.lean
    |   |-- DoobTransform.lean
    |   `-- FollmerDrift.lean
    `-- SamplingAlgorithms/
        |-- LangevinMonteCarlo.lean
        |-- RandomizedMidpoint.lean
        |-- HamiltonianMonteCarlo.lean
        |-- UnderdampedLangevin.lean
        |-- MetropolisAdjustedLangevin.lean
        `-- ProximalSampler.lean
```

New modules should be added only when a small, source-anchored leaf is ready.
The next expected expansion is Prekopa-Leindler support and nonquadratic
coercive Gibbs envelopes, with Mathlib searched first and
`Lean-Asymptotic-Statistical-Theory` used as an external reference project.

## Canonical Compiled Module And Leaf Families

{markdown_table(rows, [
    ("Module", "module"),
    ("File", "file"),
    ("Layer", "layer"),
    ("Purpose", "summary"),
    ("Representative compiled leaves/exports", "leaves"),
    ("Curated memory entries", "memory_count"),
    ("Mathlib-quality status", "status"),
])}

## Mathlib-Ready Callable Arsenal

The table below is generated from
`AutoSamplingTheory/TechnicalLemmas/Registry.lean`.  These are the currently
compiled local entries that agents may retrieve as proven technical lemma
memory for future Mathlib-style cleanup.  External Lean projects may motivate
a row, but the callable proof is the ASTIS-owned declaration listed here.

{markdown_table(memory_rows, [
    ("Module", "module"),
    ("Memory key", "key"),
    ("Local declaration", "decl"),
    ("Upstream or source orientation", "upstream"),
])}

## Paper-Extracted Quarantine

These declarations also compile, but they are not counted as the Mathlib-ready
arsenal until the paper-specific names and assumptions are generalized.  The
main graph omits `SALDExtracted.lean` for this reason.

{markdown_table(extracted_memory_rows, [
    ("Module", "module"),
    ("Memory key", "key"),
    ("Local declaration", "decl"),
    ("Source orientation", "upstream"),
])}

## Current Library Boundary

| Layer | Rule |
|---|---|
| Main graph surface | `Probability.lean`, `TechnicalLemmas/Probability/*`, `TechnicalLemmas/ProbabilityDistributions/Gaussian.lean`, `TechnicalLemmas/Analysis/Calculus/Taylor.lean`, `TechnicalLemmas/Analysis/Integrability.lean`, `TechnicalLemmas/StochasticProcesses/*`, `TechnicalLemmas/InformationTheory/*`, and `TechnicalLemmas/FunctionalInequalities/*`. |
| Compatibility surfaces | `TechnicalLemmas/Gaussian.lean`, `TechnicalLemmas/Taylor.lean`, `TechnicalLemmas/Measure.lean`, and `TechnicalLemmas/Variational.lean` remain stable imports but are omitted from the main graph. |
| Contract and automation surfaces | `Core.lean`, `SDE.lean`, `Automation.lean`, `Literature.lean`, and `OpenProblems.lean` are system interfaces, not Mathlib-ready leaf families. |
| Paper-extracted compiled leaves | `TechnicalLemmas/SALDExtracted.lean` exposes useful local theorems, but they remain paper-derived until generalized. |
| Consumers | `SALD.lean` and `RMFLD.lean` are downstream users of the arsenal; they are not the public foundation. |

## External Reference Memory

External Lean code and textbooks are preserved as reference cards under
`research-wiki/external-lean-libraries/`.  They are port sources and proof-style
memory, not local proof certificates.

| Reference | Card |
|---|---|
| Mathlib | `research-wiki/external-lean-libraries/mathlib.md` |
| `YuanheZ/lean-stat-learning-theory` | `research-wiki/external-lean-libraries/lean-stat-learning-theory.md` |
| `auto-res/lean-rademacher` | `research-wiki/external-lean-libraries/lean-rademacher.md` |
| Log-concave sampling notes | `research-wiki/external-lean-libraries/log-concave-sampling-notes.md` |
| `junwei-lu/Lean-Asymptotic-Statistical-Theory` | `research-wiki/external-lean-libraries/lean-asymptotic-statistical-theory.md` |
| ATLAS v1 | `research-wiki/external-lean-libraries/atlas-v1.md` |

## Agent Rule

Upper agents use this graph to choose the likely proof family.  Middle agents
turn the selected family into one or two Mathlib-ready leaves and must search
Mathlib plus this arsenal before assigning generic infrastructure.  Lower Lean
workers prove one stable leaf at a time.  Persistent failure means the
statement probably needs a hidden regularity contract, a missing assumption, or
a counterexample audit.
"""


def arsenal_module_card_text(record: dict) -> str:
    memory_entries = formalized_memory_entries_by_module().get(record["module"], [])
    decls = module_decl_names(record, limit=40)
    decl_lines = "\n".join(f"- `{name}`" for name in decls) or "- no direct declarations or exports"
    memory_lines = "\n".join(
        f"- `{entry['key']}` -> `{entry['decl'].rsplit('.', 1)[-1]}` ({entry['upstream'] or 'local'})"
        for entry in memory_entries
    ) or "- no curated formalized memory entries for this module"
    imports = "\n".join(f"- `{item}`" for item in record.get("imports", [])) or "- none"
    return f"""# {record['module']}

- File: `{record['path']}`
- Layer: {record.get('layer', 'uncategorized')}
- Purpose: {record.get('summary', '')}
- Mathlib-quality status: {record.get('status', '')}

## Imports

{imports}

## Representative Declarations And Exports

{decl_lines}

## Curated Formalized Memory Entries

{memory_lines}

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
"""


def external_reference_cards() -> dict[Path, str]:
    return {
        EXTERNAL_LEAN_LIBRARY_DIR / "mathlib.md": f"""# Mathlib

- Public site: {MATHLIB_URL}
- Local checkout searched by ASTIS: `.lake/packages/mathlib/Mathlib`
- Role: upstream target and first search surface for reusable SDE/Sampling
  technical lemmas.

ASTIS agents must search Mathlib before creating a generic local theorem.  If
Mathlib already has the result, ASTIS should prove only the narrow adapter
needed by the current project.  If ASTIS proves a clean generic theorem, the
leaf should be written so it can later be proposed upstream.
""",
        EXTERNAL_LEAN_LIBRARY_DIR / "lean-stat-learning-theory.md": f"""# YuanheZ/lean-stat-learning-theory

- Public repository: {SLT_URL}
- Paper: {SLT_ARXIV_URL}
- Local checkout: `{SLT_ROOT}`
- Current audited checkout: `d0f506f0a695018265dccb33bcb05e2f5ca1c876`
  on `main`, tagged `v4.32.0`.
- Latest verification: `git fetch --prune origin` and fast-forward on 2026-07-16
  left local `HEAD` equal to `origin/main`.  The checkout has only untracked
  `.lake/` cache files, not source edits.  The focused target
  `lake build SLT.GaussianSobolevDense.Cutoff` passed at this commit under Lean
  `v4.32.0` (3115 jobs, including rebuilt dependencies).
- Role: audited port/reference source for probability, Gaussian,
  concentration, entropy duality, log-Sobolev/Poincare, product-measure
  slicing, matrix concentration, and discretization proof style.

ASTIS keeps this project as audited port/reference memory rather than a Lake
dependency because toolchains differ.  Useful theorems become callable only
after they are copied as ASTIS-owned Lean declarations and pass the local build,
or they remain recorded in the port queue.

## Current Useful Surfaces

| SLT file/family | ASTIS use |
|---|---|
| `SLT/EfronStein.lean` | coordinate replacement under product laws, especially `map_update_prod_pi` and integral rewrites for `Function.update` |
| `SLT/GaussianLSI/SubAddEnt/Basic.lean` | product-coordinate slice integrability and AE nonnegativity patterns such as `integrable_update_slice` |
| `SLT/GaussianLSI/SubAddEnt/Subadditivity.lean` | coordinate selection maps, tower properties, and entropy subadditivity staging |
| `SLT/GaussianLSI/SubAddEnt/Decomposition.lean` | entropy telescoping/decomposition patterns for product laws |
| `SLT/GaussianLSI/Entropy.lean` and `SLT/GaussianLSI/DualEntApp.lean` | entropy, Jensen, and Gibbs-duality proof patterns |
| `SLT/GaussianMeasure.lean` | `stdGaussianPi`, coordinate laws, independence, linear MGFs, and Gaussian tail/mean identities |
| `SLT/GaussianLSI/TensorizedGLSI.lean` | `partialDeriv`, `sliceFunction`, derivative of slices, and tensorized Gaussian LSI proof architecture |
| `SLT/GaussianPoincare/*` | Rademacher/Efron-Stein/limit architecture for Gaussian Poincare |
| `SLT/GaussianSobolevDense/Defs.lean` | radial smooth cutoff definitions: the support, compact-support, smoothness, range, and pointwise-exhaustion base has been ported as ASTIS-owned declarations in `Analysis/Calculus/Cutoff.lean` |
| `SLT/GaussianSobolevDense/Cutoff.lean` | the scalar derivative bound, norm-scaling bound, strengthened one-constant-for-all-R radial first-derivative theorem, and closed outer derivative-zero leaf have been ported as ASTIS-owned declarations; ASTIS also supplies the finite-Pi derivative/trace consumer bridge; dominated cutoff limits remain reference targets before IBP |
| `SLT/GaussianPoincare/TaylorBound.lean` | compact-support derivative support/boundedness patterns: `deriv_hasCompactSupport`, `deriv2_hasCompactSupport`, `deriv_bounded_of_compactlySupported`; closest SLT staging pattern for no-boundary/IBP prerequisites |
| `SLT/MeasureInfrastructure.lean` | Chernoff, layer-cake, Jensen, finite sup/union, and integrability proof patterns |
| `SLT/HansonWright.lean`, `SLT/MatrixInfra/*`, `SLT/RMT/*`, `SLT/TDudley.lean` | later matrix concentration, empirical-process, and random-matrix proof patterns |

Immediate port candidates for the log-concave sampling tree:

- `Measure.pi` coordinate replacement: port an ASTIS-owned version of
  `map_update_prod_pi` into a focused product-measure module.
- coordinate slices: reuse the `partialDeriv`/`sliceFunction` pattern when
  formalizing product/tensorization arguments and coordinate Langevin leaves.
- Gaussian product law surface: mirror the `stdGaussianPi` and coordinate-law
  interface when strengthening ASTIS Gaussian transition kernels and LMC noise.
- entropy/Jensen surface: reuse the proof staging around `entropy_nonneg`,
  conditional entropy, and subadditivity for FI/LSI chapters.
- cutoff/no-boundary surface: the radial support/exhaustion, scale-uniform
  first-derivative, closed outer derivative-zero, finite-Pi consumer bases,
  generic `L¹` cutoff-gradient limit, and generic cutoff main-term dominated
  convergence from `Integrable` fields are now ported;
  continue using `GaussianSobolevDense/Cutoff.lean` and
  `GaussianPoincare/TaylorBound.lean` as proof-pattern memory for ASTIS-owned
  dominated-limit leaves, and for Hessian/Laplacian leaves only when a named
  second-order consumer requires them.
- Gaussian tensorization: use the LSI/Poincare files as proof architecture
  references only; no theorem is callable until ported locally.

Recommended migration order for ASTIS roots:

1. `MEAS/KERN`: product update, Fubini, and slice-integrability facts.
2. `GAUSS/MEAS`: product Gaussian law and coordinate/linear functional facts.
3. `GAUSS/FI/DENS/REG`: coordinate derivative slicing and tensorized Gaussian
   LSI proof architecture.
4. `REG/CALC/SDE`: use the compiled generic `L¹` cutoff-gradient and main-term
   dominated-convergence limits plus the concrete Gibbs/source-field integrability
   leaf, separately prove concrete Langevin generator-display integrability, and add Hessian/Laplacian facts only
   for named second-order consumers.
5. `FI/DENS/MEAS`: entropy/Jensen and Gibbs-duality infrastructure.
6. `FI/MEAS`: entropy chain rule and product subadditivity.
""",
        EXTERNAL_LEAN_LIBRARY_DIR / "lean-rademacher.md": """# auto-res/lean-rademacher

- Public repository: https://github.com/auto-res/lean-rademacher
- Local checkout: `../outer_repos/automation_systems/lean-rademacher`
- Role: nearby reference for concentration, symmetrization, separability,
  Dudley-style entropy, and large-proof staging.

ASTIS treats it as proof-architecture memory.  Any theorem needed by ASTIS
must be ported into an ASTIS-owned module or recorded as a proof obligation.
""",
        EXTERNAL_LEAN_LIBRARY_DIR / "log-concave-sampling-notes.md": f"""# Log-Concave Sampling Notes

- Public PDF: {CHEWI_LOG_CONCAVE_URL}
- Local primary PDF: `{CHEWI_LOG_CONCAVE_PDF}`
- Role: primary roadmap for `ASTIS-CHEWI-001`, the log-concave sampling
  foundation program.

The textbook is the organizing source for ASTIS's reusable Sampling/SDE Lean
arsenal.  Local technical lemmas should be justified by the textbook tree or by
background sources cited by that tree.

## Chapter-To-Lean Families

| Textbook part | ASTIS Lean family |
|---|---|
| Stochastic calculus primer | `TechnicalLemmas/StochasticProcesses/Ito`, quadratic variation, martingale and weak-generator leaves |
| Markov semigroups | `TechnicalLemmas/StochasticProcesses/MarkovSemigroup`, invariant-measure and generator interfaces |
| Optimal transport geometry | `TechnicalLemmas/Measure/Transport` and Wasserstein gradient-flow contracts |
| Langevin as Wasserstein gradient flow | `TechnicalLemmas/StochasticProcesses/Langevin` plus KL/FI dissipation leaves |
| Functional inequalities | `TechnicalLemmas/FunctionalInequalities/*` for PI, LSI, transport, concentration, isoperimetry, and preservation operations |
| Change of measure, Doob transform, Follmer drift, Schrodinger bridge | `TechnicalLemmas/StochasticProcesses/Girsanov`, `DoobTransform`, `FollmerDrift`, and path-space RN derivative leaves |
| LMC and interpolation arguments | `SamplingAlgorithms/LangevinMonteCarlo` plus weak-FP, interpolation, and discretization-error leaves |
| HMC, underdamped, MALA, proximal sampler | `SamplingAlgorithms/*` consumers built only after the analytic foundation is local |
| Diffusion generative models | future consumer layer after path-space and score-drift leaves exist |

## Rigor Policy

The notes are a roadmap, not a Lean certificate.  Every extracted statement
must become one of:

- an ASTIS-owned compiled Lean declaration;
- an explicit `ProofObligation` with source anchor and hidden regularity
  contract;
- a cited-result memory card tied to a primary source;
- a rejected statement if the Lean assumptions would silently strengthen or
  change the textbook claim.

Do not import informal textbook shortcuts as assumptions.  For phrases such as
"standard", "by Fokker--Planck", "by Girsanov", "by integration by parts", or
"under regularity assumptions", agents must expose the exact measurability,
integrability, differentiability, boundary/decay, positivity, and
representative-choice hypotheses before lower proof work starts.
""",
        EXTERNAL_LEAN_LIBRARY_DIR / "lean-asymptotic-statistical-theory.md": f"""# Lean-Asymptotic-Statistical-Theory

- Public repo: {LEAN_ASYMPTOTIC_STATISTICS_URL}
- Local checkout: `{LEAN_ASYMPTOTIC_STATISTICS_ROOT}`
- Related paper: `Hypothesis-Disciplined Multi-Agent Automated Formalization of Asymptotic Statistical Theory`, {LEAN_ASYMPTOTIC_STATISTICS_ARXIV_URL}
- Local paper: `{LEAN_ASYMPTOTIC_STATISTICS_PDF}`
- Toolchain observed in repo: Lean 4.29.1 / Mathlib 4.29.1.
- Observed local commit: `8e7f22c88cc3280e898005b6445d94c581dd8b4d`
  (`2026-06-09 15:57:20 -0400`).
- Role: external reference project and process model.  It is not an ASTIS Lake
  dependency and none of its theorems are callable until ported or reproved
  locally.

## Useful Code For Log-Concave Sampling

The repository contains a broad `AsymptoticStatistics/ForMathlib` layer.  The
following files are especially relevant to log-concave sampling
infrastructure:

- `AsymptoticStatistics/ForMathlib/PrekopaLeindler.lean` for
  Prekopa-Leindler and Brunn-Minkowski style convex-measure infrastructure.
- `AsymptoticStatistics/ForMathlib/Brunn1D.lean` for the one-dimensional
  Brunn-Minkowski boundary used by the Prekopa-Leindler development.
- `AsymptoticStatistics/ForMathlib/GaussianMGF.lean`,
  `PiGaussian.lean`, `PiWithDensity.lean`, `GaussianRealTV.lean`, and
  `GaussianShift.lean` for Gaussian density, product Gaussian, MGF, and
  finite-dimensional change-of-measure patterns.
- `AsymptoticStatistics/ForMathlib/RnDerivSqrt.lean`,
  `HellingerProduct.lean`, and `L2.lean` for RN derivative, square-root
  density, Hellinger, and L2-style proof patterns.
- `AsymptoticStatistics/ForMathlib/Contiguity.lean`,
  `Prohorov.lean`, `PortmanteauLscBridge.lean`, and weak-convergence files for
  probability-limit infrastructure.
- `AsymptoticStatistics/ForMathlib/MeasurableSelection*.lean`,
  `MarkovKernelProhorov.lean`, and kernel files for measurable-selection,
  tightness, and Markov-kernel proof style.

The first audit of these log-concave-sampling-relevant `ForMathlib` files found no `sorry`,
`axiom`, or `unsafe` hits in the selected port candidates.  ASTIS should still
reprove or port only the minimal Mathlib-ready leaves needed by the log-concave sampling tree.

## Process Lessons To Reuse

The associated paper proposes a hypothesis-disciplined multi-agent pipeline.
ASTIS should reuse the discipline, not the exact domain:

- every theorem hypothesis must be source-anchored, a Lean encoding adapter,
  source-implied, or explicitly rejected;
- concept-layer fields must not drift from the informal theorem;
- dependency graphs and side-by-side informal/Lean statements are useful
  review artifacts for long proof runs;
- "hypothesis laundering" is a failure mode: do not close a proof by adding
  assumptions that the source does not justify.

For `ASTIS-CHEWI-001`, this reference should guide the audit protocol for
textbook chapter extraction and Mathlib-ready leaf acceptance.
""",
        EXTERNAL_LEAN_LIBRARY_DIR / "atlas-v1.md": """# ATLAS v1 external declaration memory

- Website: https://rammalahmad.github.io/atlas/
- Repository: https://github.com/facebookresearch/atlas-lean
- Paper: https://arxiv.org/abs/2605.29955
- Pinned commit: `e8b31c5cb0bec89b487ce33fe525a2c0b0f8b9c6`
- Default external checkout: `../outer_repos/atlas-lean/v1` (override with `ASTIS_ATLAS_ROOT`)
- Upstream toolchain: Lean 4.29.0 / Mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- ASTIS toolchain: Lean 4.33.0 / Mathlib v4.33.0
- License: CC BY-NC 4.0 for academic/research use; commercial use and ML model training, fine-tuning, distillation, evaluation, or development are prohibited; see pinned `v1/LICENSE`.

## Audited inventory

ASTIS deterministically indexes 26 books, 2,653 Lean files, and 36,469 named
source declarations: 17,098 theorems, 6,204 lemmas, and the remaining named
definitions and interfaces. It records 3,502 declarations with a direct
`sorry`, `admit`, or `axiom` marker. ATLAS reports 2,855 of 4,007 selected
textbook targets as passed; that evaluation is metadata, not ASTIS proof ownership.

The compact records live in `research-wiki/retrieval-index/atlas-v1/`. Search:

```bash
python3 tools/atlas_memory.py search markov --route samplewiki-route --clean-only
python3 tools/atlas_memory.py search riemannian --route riemannian-optimization
python3 tools/atlas_memory.py search convex --route optimisation
```

## Route relevance

- SampleWiki and sampling shared floor: 6,573 candidates in probability,
  conditional expectation, martingale, Markov, Brownian, concentration,
  information, semigroup, and PDE material.
- Riemannian Optimization: 1,674 candidates led by GeometryOfManifolds,
  DifferentialGeometry, and DifferentialAnalysis.
- Optimisation: 369 candidates led by CombinatorialOptimization and
  AnAlgorithmistsToolkit.

Every declaration remains searchable. Material outside these controlled book/topic
rules is intentionally unassigned rather than forced into an unrelated route.

## Call policy

Every record is `external-reference`, including records without a direct
placeholder. It becomes callable only after the minimal theorem is ported or
reproved as an ASTIS-owned declaration, tested under Lean 4.33.0, entered in
the Registry, source-mapped, and independently reviewed.
""",
    }


def write_arsenal_module_graph_docs() -> list[Path]:
    records = lean_module_records()
    outputs: list[Path] = []
    path_texts = [
        (ROOT / "docs" / "module-graph.svg", arsenal_module_graph_svg(records)),
        (ROOT / "docs" / "assets" / "astis_lean_arsenal_module_graph.svg", arsenal_module_graph_svg(records)),
        (SAMPLING_LIBRARY_DIR / "lean-leaf-module-graph.md", arsenal_module_graph_markdown(records)),
        (SAMPLING_LIBRARY_DIR / "index.md", "# ASTIS Sampling/SDE Lean Library\n\nStart with [`lean-leaf-module-graph.md`](lean-leaf-module-graph.md).\n"),
    ]
    json_payload = {
        "generated": now_stamp(),
        "module_graph_svg": "docs/module-graph.svg",
        "ledger": rel(SAMPLING_LIBRARY_DIR / "lean-leaf-module-graph.md"),
        "modules": records,
    }
    path_texts.append((RETRIEVAL_INDEX_DIR / "astis-lean-arsenal-module-graph.json",
                       json.dumps(json_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"))
    for path, text in path_texts:
        write_text(path, text)
        outputs.append(path)

    converter = shutil.which("convert") or shutil.which("magick")
    if converter:
        png_path = ROOT / "docs" / "assets" / "astis_lean_arsenal_module_graph.png"
        convert_cmd = [converter, str(ROOT / "docs" / "module-graph.svg"), str(png_path)]
        if Path(converter).name == "magick":
            convert_cmd = [converter, "convert", str(ROOT / "docs" / "module-graph.svg"), str(png_path)]
        completed = subprocess.run(convert_cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if completed.returncode == 0:
            print(f"wrote {rel(png_path)}")
            outputs.append(png_path)
        else:
            print(f"warning: could not render PNG preview with {converter}: {completed.stdout.strip()}")

    for record in records:
        if record["module"] == "AutoSamplingTheory":
            continue
        card_path = SAMPLING_LIBRARY_DIR / "cards" / f"{slugify(record['module'])}.md"
        write_text(card_path, arsenal_module_card_text(record))
        outputs.append(card_path)

    for path, text in external_reference_cards().items():
        write_text(path, text)
        outputs.append(path)

    external_index = {
        "generated": now_stamp(),
        "references": [
            {"id": path.stem, "path": rel(path)}
            for path in sorted(external_reference_cards())
        ],
    }
    external_index_path = RETRIEVAL_INDEX_DIR / "external-lean-reference-cards.json"
    write_text(external_index_path, json.dumps(external_index, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    outputs.append(external_index_path)
    return outputs


def cmd_module_graph_refresh(_: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    outputs = write_arsenal_module_graph_docs()
    outputs.extend(write_mathlib_ready_leaf_docs())
    for path in outputs:
        add_manifest("astis.py module-graph-refresh", path, "memory", "Refreshed ASTIS SDE/Sampling Lean arsenal module graph")
    print("module-graph-refresh wrote:")
    for path in outputs:
        print(f"- {rel(path)}")
    return 0


def write_sald_unfinished_source_map(cycle: int | None = None) -> Path:
    SALD_PAPER_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    items = sald_unfinished_source_items()
    missing = [row for row in items if row.get("line_range_status") != "precise"]
    missing_lines = "\n".join(
        f"- `{row.get('id')}` -> `{row.get('source_ref')}`"
        for row in missing
    ) or "- none"
    active_leaf = items[2] if len(items) > 2 else (items[0] if items else {})
    text = f"""# ASTIS-SALD-001 Paper Memory: Unfinished Source Map

Generated: `{now_stamp()}`

Cycle considered: `{cycle if cycle is not None else max(latest_cycle_number("ASTIS-SALD-001"), latest_trial_cycle("ASTIS-SALD-001"))}`.

This file is task-local paper contribution memory.  It records the VA-SALD
paper-specific source lines and Lean proof boundaries that remain unfinished.
Reusable background facts belong in canonical `research-wiki/technical-lemmas/`
and ASTIS-owned Lean modules under `AutoSamplingTheory/TechnicalLemmas/`.
The legacy mirror is `research-wiki/paper-memory/ASTIS-SALD-001/`.

## Unfinished Source-Line Map

| Boundary id | Type | Source lines | Lean boundary | Status | Next action |
|---|---|---|---|---|---|
{unfinished_source_markdown_table(items)}

## Line Range Audit

Reviewer must reject a cycle's "complete" claim if any active paper
contribution leaf is missing concrete source lines.

{missing_lines}

## Next Smallest Leaf

- Boundary: `{active_leaf.get("id", "unknown")}`
- Source: `{active_leaf.get("source_ref", "line-range-missing")}`
- Lean boundary: `{active_leaf.get("lean_boundary", "")}`
- Next action: {active_leaf.get("next_action", "")}

## Technical Lemma Status Snapshot

{technical_lemma_status_markdown()}
"""
    write_text_mirror(SALD_UNFINISHED_SOURCE_MAP, text, [LEGACY_SALD_UNFINISHED_SOURCE_MAP])
    for path in [SALD_UNFINISHED_SOURCE_JSONL, LEGACY_SALD_UNFINISHED_SOURCE_JSONL]:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            for row in items:
                handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    add_manifest(
        "astis.py update-sald-paper-memory",
        SALD_UNFINISHED_SOURCE_MAP,
        "paper-contributions",
        "Updated SALD unfinished source-line map",
    )
    return SALD_UNFINISHED_SOURCE_MAP


def paper_memory_pack(task_id: str) -> str:
    if task_id != "ASTIS-SALD-001":
        return "- No task-local paper memory pack selected."
    return "\n".join([
        "- Canonical task-local paper contribution memory: `research-wiki/paper-contributions/SALD/`.",
        "- Legacy mirror: `research-wiki/paper-memory/ASTIS-SALD-001/`.",
        "- Unfinished source-line map: `research-wiki/paper-contributions/SALD/unfinished_source_map.md`.",
        "- Paper memory stores VA-SALD-specific theorem/proof leaves, source line correspondence, and source-cited obligations.",
        "- It must not store generic prior facts; those belong in `research-wiki/technical-lemmas/` and `AutoSamplingTheory/TechnicalLemmas/`.",
        "- Upper reads compact context, blueprint, TODO, and unfinished map only; it must not replay long historical logs.",
        "- Middle checks task-local paper memory plus TechnicalLemmas before assigning lower agents.",
        "- Lower proves one compiled theorem or narrows one source-cited boundary.",
        "- Reviewer checks Lean gate, concrete source-line coverage, and whether any called technical lemma is ASTIS-owned and compiled.",
    ])


def latest_lean_gate_status(task_id: str) -> str:
    for record in reversed(trial_records_for_task(task_id)):
        lean_gate = record.get("lean_gate", "")
        if lean_gate in {"pass", "fail"}:
            cycle = cycle_number_from_record(record)
            cycle_text = f"cycle {cycle}, " if cycle is not None else ""
            return f"{cycle_text}{lean_gate} at {record.get('timestamp', 'unknown')}"
        if record.get("kind") == "build":
            status = "pass" if record.get("status") == "compiled" else record.get("status", "unknown")
            cycle = cycle_number_from_record(record)
            cycle_text = f"cycle {cycle}, " if cycle is not None else ""
            return f"{cycle_text}{status} at {record.get('timestamp', 'unknown')}"
    state = load_state()
    last_check = state.get("last_check")
    if isinstance(last_check, dict):
        return f"manual check exit_code={last_check.get('exit_code')} at {last_check.get('timestamp', 'unknown')}"
    return "not recorded"


def format_decl_list(value) -> str:
    if isinstance(value, list):
        return ", ".join(f"`{item}`" for item in value)
    if isinstance(value, str):
        return f"`{value}`" if value else ""
    return str(value)


def write_sald_reproduction_todo(cycle: int | None = None) -> Path:
    todo_dir = ROOT / "research-wiki" / "todo"
    todo_dir.mkdir(parents=True, exist_ok=True)
    path = todo_dir / "SALD_REPRODUCTION_TODO.md"
    cycle_note = cycle if cycle is not None else max(
        latest_cycle_number("ASTIS-SALD-001"),
        latest_trial_cycle("ASTIS-SALD-001"),
    )
    source_map_path = write_sald_unfinished_source_map(cycle_note)
    unfinished_table = unfinished_source_markdown_table()
    registry_rows = technical_lemma_registry_rows()
    formalized_rows = [row for row in registry_rows if row.get("status") == "formalized-local"]
    port_rows = [row for row in registry_rows if row.get("status") != "formalized-local"]
    port_rows.extend(technical_lemma_port_queue_rows())
    formalized_table = "\n".join(
        f"| `{row.get('local_decl', '')}` | {', '.join(row.get('tags', []))} | {row.get('sald_use', '')} | `{row.get('local_file', '')}` |"
        for row in formalized_rows[:24]
    ) or "| none | none | none | none |"
    port_table = "\n".join(
        f"| `{row.get('upstream_file', '')}` | {format_decl_list(row.get('upstream_declarations', row.get('upstream_decl', '')))} | {row.get('astis_target', row.get('sald_use', row.get('target_local_module', '')))} | {row.get('status', '')} |"
        for row in port_rows[:16]
    ) or "| none | none | none | none |"
    blocker = latest_reviewer_blocker("ASTIS-SALD-001")
    text = f"""# SALD Reproduction TODO

Generated: `{now_stamp()}`

Task: faithful Lean reproduction of the original VA-SALD paper
([arXiv:2605.07950](https://arxiv.org/abs/2605.07950)).

Latest cycle considered: `{cycle_note}`.

Gate to trust this dashboard:

```bash
python3 tools/astis.py check
```

## Human Reading Guide

- SALD-contribution rows are proof content specific to the VA-SALD paper.
- Technical-lemma rows are background or reusable infrastructure used by the
  SALD reproduction and later SDE/Sampling papers.
- `formalized-local` means the declaration is ASTIS-owned and compiled by the
  gate.  Port candidates are not callable by agents until they become local
  declarations.
- Compiled sublemma inventory:
  `research-wiki/technical-lemmas/compiled_sublemma_inventory.md`.

## SALD Paper Contribution Status

| SALD proof region | Source anchor | Lean location | Status for humans | Current action |
|---|---|---|---|---|
| Continuous SALD forward-KL theorem | `main_body.tex:thm:forward-KL`, `appendix.tex:proof:thm:forward-KL` | `AutoSamplingTheory/SALD.lean`, `forwardKlProofDag` | skeleton and many scalar/DV/Gronwall sublemmas represented; analytic FP/KL interfaces still source-cited | keep theorem status below `formalized` until KL derivative and cited analytic interfaces are closed |
| Discrete SALD forward-KL theorem | `main_body.tex:thm:forward-KL-discrete`, `appendix.tex:proof:thm:forward-KL-discrete` | `AutoSamplingTheory/SALD.lean`, `discreteForwardKlProofDag` | major source-to-Lean DAG and many EM endpoint/accumulation lemmas compiled | continue active EM weak-FP/Brownian backend |
| Guided residual proposition | `appendix.tex:prop:guided_path_residual` | `AutoSamplingTheory/SALD.lean`, `guidedResidualContract` | source-indexed and contracted | backfill residual normalizer/divergence only after active EM backend |
| General moving-target VA-SALD | `appendix.tex:thm:general-moving-target-SALD` | `AutoSamplingTheory/SALD.lean`, `generalVaSaldProofDag` | skeleton with LSI/DV/Gronwall route represented | keep cited analytic theorem interfaces explicit |
| Unified forward-KL VA-SALD | `main_body.tex:thm:unified-forward-KL` | `AutoSamplingTheory/SALD.lean`, `unifiedForwardKlContract` | specialization route represented | depends on general moving-target theorem closure |
| Discrete general moving-target VA-SALD | `appendix.tex:thm:general-moving-target-SALD-discrete` | `AutoSamplingTheory/SALD.lean`, `generalVaSaldDiscreteProofDag` | current main frontier | close/narrow Brownian/Ito scalar generator and EM weak-FP leaves |

## Unfinished Source-Line Map

Task-local paper memory:
`{rel(source_map_path)}`.

Every unfinished SALD contribution leaf must have concrete source lines.  If a
line range is missing, reviewer rejects any cycle that claims completion.

| Boundary id | Type | Source lines | Lean boundary | Status | Next action |
|---|---|---|---|---|---|
{unfinished_table}

Latest reviewer blocker:

```text
{blocker}
```

## Formalized Technical Lemma Memory

| Local declaration | Tags | SALD use | File |
|---|---|---|---|
{formalized_table}

## Technical Lemma Port Queue

| Source / upstream | Declarations | ASTIS target | Status |
|---|---|---|---|
{port_table}

## Per-Round Rule

Every cycle must update this file before producing a context pack or launch.
Reviewer should reject a cycle that changes SALD proof state without updating
the SALD contribution rows, active unfinished leaves, or technical lemma memory
when relevant.
"""
    write_text(path, text)
    add_manifest("astis.py update-sald-todo", path, "todo", "Updated human-readable SALD reproduction TODO")
    return path


def technical_lemma_memory_pack(task_id: str) -> str:
    if task_id != "ASTIS-SALD-001":
        return "- No task-specific technical lemma memory pack selected."
    return "\n".join([
        "- Technical lemma entry point: `research-wiki/technical-lemmas/README.md` (legacy mirror: `research-wiki/technical-lemma-memory/README.md`).",
        "- Compiled local Lean modules: `AutoSamplingTheory/TechnicalLemmas/Probability/*`, `AutoSamplingTheory/TechnicalLemmas/ProbabilityDistributions/Gaussian.lean`, `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Taylor.lean`, `AutoSamplingTheory/TechnicalLemmas/Analysis/Integrability.lean`, `AutoSamplingTheory/TechnicalLemmas/InformationTheory/*`, `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/*`, `AutoSamplingTheory/TechnicalLemmas/SALDExtracted.lean`, and `AutoSamplingTheory/TechnicalLemmas/Registry.lean`.",
        "- Local registry: `research-wiki/technical-lemmas/technical_lemma_registry.jsonl` (mirrored from legacy when needed).",
        "- SALD map: `research-wiki/technical-lemmas/SALD_remaining_map.md`.",
        "- Human TODO dashboard: `research-wiki/todo/SALD_REPRODUCTION_TODO.md`.",
        "- Task-local SALD paper memory: `research-wiki/paper-contributions/SALD/unfinished_source_map.md` (legacy mirror: `research-wiki/paper-memory/ASTIS-SALD-001/unfinished_source_map.md`).",
        "- Retrieval index: `research-wiki/retrieval-index/ASTIS-SALD-001.json`.",
        "- Port queue: `research-wiki/technical-lemmas/SLT_port_queue.jsonl`; queue entries are not callable until ported locally.",
        "- Separation rule: common prior knowledge lives here; SALD-specific theorem leaves and source line coverage live in paper memory.",
        "- Current SALD priority: use ASTIS technical lemmas for the EM Brownian/Ito scalar generator backend before broad LSI/DV backfill.",
        "- First local candidates: `TechnicalLemmas.ProbabilityDistributions.Gaussian.map_eval_stdGaussianPi`, `TechnicalLemmas.ProbabilityDistributions.Gaussian.nnrealVarianceOneOfGaussianRealUnitLaw`, and `TechnicalLemmas.ProbabilityDistributions.Gaussian.realVarianceOneOfNNRealVarianceOne`.",
        "- Second local candidates: `TechnicalLemmas.Analysis.Calculus.Taylor.hessianOpNormOfSourceHessianField`, `TechnicalLemmas.Analysis.Calculus.Taylor.iteratedFDerivTwoOpNormOfFDerivFDerivOpNorm`, and `TechnicalLemmas.Analysis.Calculus.Taylor.quadraticVariationNormalizationOfCoeffDefAndVarianceOne`.",
        "- Compatibility source files `TechnicalLemmas/Gaussian.lean` and `TechnicalLemmas/Taylor.lean` remain stable, but new lower packets should use the family-specific paths.",
        "- Current active leaves after cycle 181: `hBrownianCoordinateGeneratorTaylorIntegralDef`, `hRemainderGeneratorLimitDef`, concrete remainder measurability/domination, and coordinate-law/variance side leaves.",
        "- Known source-contract gap: `hSourceHasHessian` and `hSourceHessianBound`; do not fake it via technical lemmas unless the original source supplies the fields.",
        "- Deferred backends: `entropy_duality` for DV and `gaussian_logSobolev_W12_pi` for LSI are high-value port candidates, but only after they are implemented as local ASTIS declarations.",
    ])


def external_lookup_discipline() -> str:
    return (
        "External lookup discipline: upper and middle may use network search when "
        "local context is insufficient for Mathlib names, Lean API examples, or "
        "standard SDE/measure-theory statements such as weak Fokker-Planck, "
        "Green identities, trace theorems, or divergence theorems. Prefer primary "
        "sources: Mathlib docs/source, Lean project repositories, arXiv papers, "
        "or official project documentation. Any external result must be converted "
        "into a local ASTIS compiled declaration or a precise source-cited "
        "ProofObligation; do not mark it formalized just because it was found "
        "online."
    )


def compact_task_context(task_id: str, title: str, task_text: str, cycle: int) -> str:
    if task_id != "ASTIS-SALD-001" or cycle < SALD_COMPACT_CONTEXT_START_CYCLE:
        return task_text.strip()
    return "\n".join([
        f"# {title}",
        "",
        "Status: active faithfulPaper reproduction of the original VA-SALD paper.",
        "Source: `/home/nitanda_sub/mark/repos/sald/paper`; exclude `sald_version_2.tex`.",
        "Current phase: Phase 1 faithful transcript and proof backfill; Phase 2 API reorganization is deferred.",
        "",
        "Current post-cycle-84 rule: do not add broad wrappers or broad theorem-route audits. Each cycle must either discharge one supplied hypothesis, strictly narrow one source-cited theorem boundary, or explicitly reject wrapper churn.",
        "",
        "Active blocker:",
        latest_reviewer_blocker(task_id),
        "",
        "Allowed packet classifications:",
        "- `discharges-supplied-hypothesis`: compiled local theorem removes an older supplied hypothesis.",
        "- `narrows-source-cited-boundary`: exact missing theorem is smaller and source-cited with imports/hypotheses.",
        "- `rejected-wrapper-churn`: proposed work only restates a supplied hypothesis or broad ledger.",
    ])


def build_context_pack(task_id: str, title: str, task_text: str, cycle: int) -> str:
    trial_memory = "\n".join(f"- {note}" for note in latest_handoff_notes(task_id, limit=6))
    if not trial_memory:
        trial_memory = "- no handoff memory yet"
    return "\n".join([
        "# ASTIS Compact Context Pack",
        "",
        f"- Task: `{task_id}`",
        f"- Cycle: `{cycle}`",
        f"- Generated: `{now_stamp()}`",
        "",
        "## Compact Task Contract",
        "",
        compact_task_context(task_id, title, task_text, cycle),
        "",
        "## Cycle Focus",
        "",
        task_cycle_focus(task_id, cycle),
        "",
        "## Recent High-Signal Handoffs",
        "",
        trial_memory,
        "",
        "## External SLT Provenance And Port Discipline",
        "",
        slt_reference_pack(),
        "",
        "## ASTIS Technical Lemma Memory For This Task",
        "",
        technical_lemma_memory_pack(task_id),
        "",
        "## Task-Local Paper Contribution Memory",
        "",
        paper_memory_pack(task_id),
        "",
        "## Human TODO Dashboard",
        "",
        task_human_dashboard(task_id),
        "",
        "## Blueprint Control State",
        "",
        blueprint_context_snippet(task_id),
        "",
        "## Self-Reflection Guard",
        "",
        "- Start the handoff with one packet classification from the allowed list.",
        "- Name the exact supplied hypothesis discharged or the exact missing theorem boundary narrowed.",
        "- State whether the packet is a dynamic-leaf worker packet or an illness-area refiner packet.",
        "- State which local ASTIS technical lemmas/Mathlib files were used, or which external theorem was only queued for local porting.",
        "- Reject broad source-index, route-audit, wrapper, or project-article work unless it directly closes the active blocker.",
        "- Keep `python3 tools/astis.py check` as the mandatory gate.",
    ])


def write_context_pack(task_id: str, cycle: int, output: Path | None = None) -> Path:
    title, task_text = task_context(task_id)
    if task_id == "ASTIS-SALD-001":
        write_sald_reproduction_todo(cycle)
    path = output or CONTEXT_PACK_DIR / f"{slugify(task_id)}-cycle{cycle:03d}.md"
    write_text(path, build_context_pack(task_id, title, task_text, cycle))
    add_manifest("astis.py write-context-pack", path, "context", f"Wrote compact context pack for {task_id} cycle {cycle}")
    return path


def sald_cycle_focus(cycle: int) -> str:
    if cycle >= 183:
        return (
            "Cycle-183+ closure sprint: freeze `hSourceHasHessian` and "
            "`hSourceHessianBound` as an explicit source-contract gap unless "
            "the original SALD source is found to state the selected weak-test "
            "Hessian regularity verbatim. Do not spend the cycle on wrapper "
            "projections, `testRegular` repackaging, VP score-Hessian "
            "substitution, or source-Hessian re-audits. The active proof work "
            "is the connected Brownian/Ito frozen-interpolation backend: "
            "first close or strictly narrow `hBrownianCoordinateGeneratorTaylorIntegralDef` "
            "and `hRemainderGeneratorLimitDef`; then connect the same local "
            "backend to the conditional-drift weak-Fokker--Planck line "
            "`appendix.tex:1379-1387`, the KL derivative handoff "
            "`appendix.tex:1358-1365`, and the divergence/FI/IBP rewrite "
            "`appendix.tex:1422-1434`. Lower_1 should write the natural-language "
            "classical proof route for exactly one ticket, and lower_2 should "
            "implement one compiled ASTIS-owned theorem or record one strictly "
            "smaller source-cited obligation with typed verifier feedback."
        )
    if cycle >= 174:
        return (
            "Post-cycle-173 source-Hessian leaf: stay on "
            "`sald.general_moving_target_discrete.em_interpolation_fp` and discharge or strictly narrow the two "
            "source-facing selected weak-test Hessian fields left by "
            "`SALD.selectedWeakTestHessianOpNormOfSourceHessianField`: "
            "`hSourceHasHessian : forall z, HasFDerivAt (fderiv Real sourceTest) (sourceHessian z) z` and "
            "`hSourceHessianBound : forall z, norm (sourceHessian z) <= C1`. "
            "Upper/middle must first decide whether these fields are genuine source assumptions or derivable from "
            "the selected-test regularity used by the EM Brownian/Ito weak action. "
            "If derivable, lower_1 writes the natural-language Mathlib route and lower_2 implements exactly one "
            "compiled theorem. If not derivable from the paper source, record the gap honestly and move to the next "
            "real leaf in the same Brownian/Ito chain: selected-line Taylor domination, Gaussian DCT integrability, "
            "quadratic-variation normalization, or per-coordinate Hessian generator identity. "
            "Do not return to older `htraceFieldEqLaplacian`/consumer-wrapper targets unless this Hessian leaf is "
            "closed or reviewer records a strict dependency."
        )
    if cycle >= 114:
        return (
            "Blueprint-guided dynamic leaf: use `python3 tools/astis.py blueprint-refresh ASTIS-SALD-001` "
            "and target the refreshed dynamic leaf / illness area rather than the old rotating focus. "
            f"Current blocker: {latest_reviewer_blocker('ASTIS-SALD-001')}. "
            "For the current SALD state this means stay on the EM conditional-drift/state-event set-integral boundary "
            "unless reviewer records a named Mathlib/theory gap; do not take a non-EM fallback merely because the old cycle schedule rotates there."
        )
    backend_proof_closure_start_cycle = 85
    if cycle >= backend_proof_closure_start_cycle:
        focus = [
            (
                "Post-84 closure 1: conditional-kernel theorem boundary",
                "Stop adding supplied-hypothesis wrappers.  Target the smallest real backend behind `appendix.tex:1368-1377`: Mathlib `condDistrib`/`condExpKernel` orientation for `X_k^eta | hat X_s`, named `hat rho_s` marginal, and component conditional-integral fields.  Lower must either prove/port one local theorem from Mathlib-style ingredients or record one exact missing theorem with its imports and hypotheses.",
            ),
            (
                "Post-84 closure 2: generator-to-law weak-FP boundary",
                "Target `appendix.tex:1379-1387`: turn sample-path derivative plus `Measure.map`/Bochner integral transport into the weak generator-to-law Fokker--Planck statement.  Use existing cycle-79 `lawMapIntegral` helpers and Mathlib parametric-integral APIs; do not create another wrapper unless it removes a supplied hypothesis.",
            ),
            (
                "Post-84 closure 3: KL/log-ratio analytic boundary",
                "Target `appendix.tex:1358-1366`: formalize or precisely isolate KL differentiability at the admissible log-ratio weak test, including log-ratio measurability/integrability and the handoff from weak-FP action to `dK`.  Keep theorem statements unchanged.",
            ),
            (
                "Post-84 closure 4: discharge one supplied EM hypothesis",
                "Choose exactly one supplied hypothesis used by cycles 80-84 and replace it with a compiled local theorem or a narrower source-cited boundary.  The acceptable targets are conditional-kernel existence, conditional integral regularity, generator-to-law weak FP, or log-ratio admissibility.",
            ),
            (
                "Post-84 closure 5: discrete theorem closure pressure test",
                "Attempt to route `thm:forward-KL-discrete` through the currently compiled EM wrappers and existing LSI/DV/Gronwall interfaces.  The goal is not to mark the theorem formalized, but to identify the next non-wrapper blocker with a source line and exact Lean declaration.",
            ),
            (
                "Post-84 closure 6: one slow non-EM backend if EM is blocked",
                "Only if the active EM boundary is blocked by a named Mathlib gap, spend one cycle on the smallest non-EM blocker needed by theorem closure: LSI-to-KL/FI, DV finite-log-mgf/common-space, or endpoint-safe Gronwall.  Search ASTIS `TechnicalLemmas` first; use local `lean-stat-learning-theory` only as source material for an ASTIS-owned port, not as a Lake dependency.",
            ),
        ]
        title, labels = focus[(cycle - backend_proof_closure_start_cycle) % len(focus)]
        return f"{title}: {labels}"
    backend_backfill_start_cycle = 70
    if cycle >= backend_backfill_start_cycle:
        focus = [
            (
                "Backend backfill 1: EM conditional-law interface",
                "Focus only on `sald.general_moving_target_discrete.em_interpolation_fp` over `appendix.tex:1358-1387`: conditional-law/measurability and named conditional drift interfaces. Use ASTIS `TechnicalLemmas` before creating new interfaces; external SLT files are port references only.",
            ),
            (
                "Backend backfill 2: endpoint-to-conditional compatibility",
                "Continue the same EM backend: connect endpoint-law `Measure.map` bookkeeping to the conditional-law interface needed by the weak Fokker--Planck statement. Avoid unrelated theorem-route audits or display algebra.",
            ),
            (
                "Backend backfill 3: weak Fokker--Planck source signs",
                "Continue the same EM backend: sharpen or prove the weak conditional Fokker--Planck source-sign statement with `-div` drift and `+(sigma_eta^2/2) Delta` diffusion terms under explicit hypotheses.",
            ),
            (
                "Backend backfill 4: KL derivative handoff from weak FP",
                "Continue the same EM backend: connect the weak FP identity to the discrete KL-derivative handoff while keeping LSI, DV, Gronwall, and theorem statuses below formalized.",
            ),
            (
                "Backend backfill 5: minimal cited measure interface if blocked",
                "Only if proof-producing work is blocked, introduce one narrow Mathlib/measure-theory source-cited interface for the missing conditional-law or weak-FP fact; otherwise keep proving the active EM backend.",
            ),
        ]
        title, labels = focus[(cycle - backend_backfill_start_cycle) % len(focus)]
        return f"{title}: {labels}"
    main_skeleton_start_cycle = 44
    focus = [
        (
            "Main skeleton sprint 1: analytic interface ledger",
            "Create or sharpen the five source-cited analytic interfaces needed by the SALD proof route: Gronwall, DV, LSI-to-KL/FI, continuous forward-KL Fokker--Planck/KL derivative, and EM interpolation Fokker--Planck. Keep every unproved backend below formalized status.",
        ),
        (
            "Main skeleton sprint 2: continuous forward-KL",
            "Wire the source-cited analytic interfaces into the faithful proof skeleton for `thm:forward-KL`, matching `main_body.tex:238-247` and `appendix.tex:164-252` without changing constants, statements, or source labels.",
        ),
        (
            "Main skeleton sprint 3: discrete forward-KL",
            "Wire the theorem-level interfaces into `thm:forward-KL-discrete`, matching `main_body.tex:299-323` and `appendix.tex:260-592`; use source-cited EM/Fokker--Planck interfaces explicitly instead of proving them from scratch in this cycle.",
        ),
        (
            "Main skeleton sprint 4: guided residual and general moving-target",
            "Wire `prop:guided_path_residual` and `thm:general-moving-target-SALD` to the already named interfaces, matching `appendix.tex:619-951`; preserve the paper theorem statements and expose any missing analytic fact as a source-cited interface.",
        ),
        (
            "Main skeleton sprint 5: unified and discrete general theorem",
            "Wire `thm:unified-forward-KL` and `thm:general-moving-target-SALD-discrete` through the continuous/general skeletons and explicit source-cited interfaces; only after that, backfill one narrow measure-theory detail guided by ASTIS technical lemma memory or a local port candidate.",
        ),
    ]
    title, labels = focus[(max(cycle, main_skeleton_start_cycle) - main_skeleton_start_cycle) % len(focus)]
    return f"{title}: {labels}"


def chewi_cycle_focus(cycle: int) -> str:
    frontier = harness.reconcile_frontier(ROOT)
    selected = frontier.get("selected_ready_leaf")
    if not selected:
        return (
            "Log-concave sampling foundation: no dependency-ready red leaf was found. "
            "Reviewer must reconcile the current Lean inventory before assigning proof search."
        )
    dependencies = ", ".join(selected["dependencies"]) or "none"
    missing = ", ".join(selected["missing_declarations"])
    return (
        f"Log-concave sampling source-derived frontier for cycle {cycle}: "
        f"`{selected['node_id']}` ({selected['label']}). Dependencies already compiled: "
        f"{dependencies}. Missing local declaration(s): {missing}. Upper must provide the exact "
        "mathematical/source contract; middle must map it to current ASTIS/Mathlib APIs; lower may "
        "attempt only one smaller dependency-ready declaration; reviewer must reject a contract-only "
        "or external result presented as a local proof. Independent optional leaves may run only when "
        "they cannot edit the same module and are explicitly marked non-blocking."
    )


def task_cycle_focus(task_id: str, cycle: int) -> str:
    if task_id == "ASTIS-SALD-001":
        return sald_cycle_focus(cycle)
    if task_id == "ASTIS-CHEWI-001":
        return chewi_cycle_focus(cycle)
    return "Follow the task contract and current conversion window."


def task_human_dashboard(task_id: str) -> str:
    if task_id == "ASTIS-CHEWI-001":
        return "\n".join([
            f"- Library overview: `{rel(LOG_CONCAVE_OVERVIEW_MD)}`.",
            f"- Master chapter/theorem DAG: `{rel(LOG_CONCAVE_FOUNDATION_DAG_MD)}`.",
            f"- Blue/red status tree: `{rel(LOG_CONCAVE_STATUS_SVG)}`.",
            f"- Six-hour execution pack: `{rel(LOG_CONCAVE_EXECUTION_PACK_MD)}`.",
            "- Compact retrieval index: `research-wiki/retrieval-index/ASTIS-CHEWI-001.json`.",
        ])
    if task_id == "ASTIS-SALD-001":
        return "\n".join([
            "- Current human-readable SALD reproduction TODO: `research-wiki/todo/SALD_REPRODUCTION_TODO.md`.",
            "- Current unfinished source-line map: `research-wiki/paper-contributions/SALD/unfinished_source_map.md`.",
            "- Compact retrieval index for upper/middle: `research-wiki/retrieval-index/ASTIS-SALD-001.json`.",
        ])
    return f"- Compact retrieval index: `research-wiki/retrieval-index/{task_id}.json` if present."


def chewi_role_instructions(role: str, role_name: str, lower_count: int) -> str:
    role_specific = {
        "upper": (
            "Choose exactly one log-concave sampling objective for this cycle. Start from the library overview, chapter DAG, module graph, and retrieval index. "
            "Prefer shared roots over chapter-specific theorem work: MEAS, KERN, DENS, GAUSS, CONV, FI, SDE, PATH, DISC, REG. "
            "Do not assign SALD/RMFLD wrapper work unless it extracts a reusable ASTIS-owned lemma for the log-concave sampling foundation. "
            "The upper packet must name the chapter/topic, the shared roots reused, the target module, one lower-ready leaf, and reviewer criteria."
        ),
        "middle": (
            "Translate the upper packet into Lean-facing declarations and proof obligations. "
            "For every textbook phrase such as standard Fokker-Planck, Girsanov, invariant measure, integration by parts, or regularity assumptions, list the exact hidden assumptions: measurability, integrability, domination, differentiability, boundary decay, positivity, and representative choices. "
            "Search Mathlib and the local ASTIS registry before assigning a new lemma. External repos are provenance only until the needed fact is ported or reproved locally."
        ),
        "lower": (
            "Work on exactly one Mathlib-ready log-concave sampling foundation leaf. "
            "Either compile one small ASTIS-owned theorem in the assigned module or return a strictly smaller source-cited blocker. "
            "Do not broaden into a whole chapter proof, do not add assumptions only to make Lean close, and do not mark external Lean code as callable. "
            "If blocked, classify the blocker as Mathlib API missing, regularity gap, false/too-strong statement, representative mismatch, or target too large."
        ),
        "reviewer": (
            "Review the cycle as a library-quality gate. "
            "Accept only compiled local Lean, source-indexed proof obligations, concrete port plans, or explicit rejection of unsupported statements. "
            "Reject fake proof closures, broad wrappers, external-theorem-as-callable claims, statement drift, missing source/Mathlib anchors, and any blue status without `python3 tools/astis.py check`."
        ),
    }[role]
    if role_name == "upper_source_math":
        role_specific += (
            "\n\nUpper-panel profile: source-math auditor. Check whether the selected source statement is faithful to the textbook and identify hidden regularity. "
            "End with supported, standard-background-needed, regularity-gap, or statement-drift."
        )
    elif role_name == "upper_proof_dag":
        role_specific += (
            "\n\nUpper-panel profile: proof-DAG strategist. Pick the shortest path through shared roots and retire stale or duplicated leaves."
        )
    elif role_name == "upper_process_memory":
        role_specific += (
            "\n\nUpper-panel profile: process-memory auditor. Check that this run is not repeating SALD-style wrapper churn and that library docs remain usable."
        )
    elif role_name == "upper_director":
        role_specific += (
            "\n\nUpper profile: director synthesis. If panel handoffs exist, synthesize them into one executable packet with one target leaf and one reviewer gate."
        )
    elif role_name == "middle_source_correspondence":
        role_specific += (
            "\n\nMiddle-panel profile: source correspondence. Produce the informal source statement, Lean statement skeleton, source/Mathlib anchors, and hidden regularity list."
        )
    elif role_name == "middle_technical_lemma":
        role_specific += (
            "\n\nMiddle-panel profile: technical-lemma curator. Search local ASTIS, Mathlib, and external references as provenance; classify each fact as compiled-local, needs-small-port, proof-obligation, or irrelevant."
        )
    elif role_name == "middle_report_export":
        role_specific += (
            f"\n\nMiddle-panel profile: report/export maintainer. Keep `{rel(LOG_CONCAVE_OVERVIEW_MD)}`, the DAG, status tree, retrieval index, and execution pack synchronized."
        )
    elif role_name == "middle_formalizer":
        role_specific += (
            "\n\nMiddle profile: coordinator synthesis. Produce one lower_1 math route, one lower_2 Lean implementation task, and optionally one lower_3 API/port scout task."
        )
    elif role_name == "lower_1" and lower_count >= 2:
        role_specific += (
            "\n\nParallel lower specialization: natural-language proof scout. Give the mathematical route, exact assumptions, Mathlib/local lemmas, and one lower_2-ready theorem shape."
        )
    elif role_name == "lower_2" and lower_count >= 2:
        role_specific += (
            "\n\nParallel lower specialization: Lean implementer. Implement exactly one compiled theorem or a strictly smaller source-cited blocker from lower_1/middle."
        )
    elif role_name == "lower_3" and lower_count >= 3:
        role_specific += (
            "\n\nParallel lower specialization: API/port scout. Search Mathlib and external reference code, then port/reprove one tiny local lemma or record a precise proof obligation."
        )
    elif role_name == "reviewer_gate":
        role_specific += (
            "\n\nSpecialization: deterministic gate reviewer. Require `python3 tools/astis.py check` before accepting compiled progress."
        )
    elif role_name == "reviewer_waste":
        role_specific += (
            "\n\nSpecialization: progress-economics reviewer. Report what improved, what wasted effort, and the best next shared-root leaf."
        )
    return role_specific


def role_prompt(
    role: str,
    task_id: str,
    title: str,
    task_text: str,
    cycle: int,
    run_dir: Path,
    context_pack: str,
    role_name: str = "",
    lower_count: int = 1,
) -> str:
    task_contract = compact_task_context(task_id, title, task_text, cycle)
    displayed_role = role_name or role
    role_contract = harness.ROLE_CONTRACTS[role]
    typed_artifact = run_dir / "artifacts" / role / f"{displayed_role}.json"
    shared = f"""Task: {task_id} - {title}
Cycle: {cycle}
Role: {displayed_role}
Base role: {role}
Run directory: {rel(run_dir)}

Mandatory gate:

```bash
python3 tools/astis.py check
```

Task contract:

```text
{task_contract}
```

Cycle focus:

```text
{task_cycle_focus(task_id, cycle)}
```

Recent trial memory:

```text
{recent_trial_text(task_id)}
```

Compact context pack: `{rel(run_dir / "05_context_pack.md")}`
Deterministic harness capsule: `{rel(run_dir / "06_harness_capsule.json")}`

Typed role artifact: `{rel(typed_artifact)}`

- Artifact type: `{role_contract['artifact']}`
- JSON fields: {", ".join(harness.ROLE_ARTIFACT_FIELDS[role])}
- Required fields: {"; ".join(role_contract['must_supply'])}
- Tool snapshot: {", ".join(role_contract['tools'])}

Read the deterministic capsule before historical notes. If they disagree,
the current Lean inventory and capsule frontier win. Publish only your role's
typed artifact; do not overwrite another role's packet. Keep assumptions,
measure, codomain, source anchor, statement-header hash, and verifier status
explicit. A proof failure is not retryable unless its error is a transient
provider/network failure.

```text
{context_pack}
```

Shared dialogue board: `{rel(run_dir / "dialogue.md")}`

When finished, append a handoff:

```bash
python3 tools/astis.py agent-note {run_dir.name} --role {displayed_role} --message "..."
python3 tools/astis.py trial-log --task {task_id} --role {displayed_role} --kind handoff --status queued --artifact {rel(run_dir)} --notes "..."
```
"""
    if task_id == "ASTIS-CHEWI-001":
        return shared + "\n## Role Instructions\n\n" + chewi_role_instructions(role, role_name, lower_count) + "\n"
    post_129_guard = (
        "For SALD cycle 130 and later, treat the cycle-129 illness-area boundary as the live target unless the reviewer records a newer one: "
        "`hdiffusionSource` has been narrowed to the EM/Brownian diffusion generator weak action plus weak Laplacian integration-by-parts action. "
        "Do not reassign already-discharged leaves `hsampleInt`, `hsampleDerivMeas`, `hsampleDerivBound`, `hboundInt`, `hpathDeriv`, `hderivValue`, "
        "`hdriftBarBAction`, raw `hpairMeas`, or `hcanonicalBarBMeas`."
    )
    post_150_guard = (
        "For SALD cycle 151 and later, the reviewer-accepted cycle-150 boundary overrides older broad guards. "
        "The active EM conditional-law / weak-FP backend remains `sald.general_moving_target_discrete.em_interpolation_fp` over "
        "`appendix.tex:1358-1387`, with source anchors `appendix.tex:984-995`, `appendix.tex:1368-1387`, and "
        "`appendix.tex:1379-1387`. "
        "Prioritize one direct definition/equality leaf at a time: `htraceFieldEqLaplacian`, "
        "`hemGeneratorLaplacianEventFieldEqTraceField`, `hemGeneratorLaplacianStateIntegral`, or "
        "`hsourceLaplacianFieldMeas`. "
        "Upper should choose the smallest leaf that reduces this boundary; middle should coordinate the proof route and split lower-agent roles; "
        "lower_1 should produce the natural-language/math route and lower_2 should implement exactly one compiled Lean theorem or a strictly smaller "
        "source-cited obligation. "
        "Reject new total-event/source-functional consumer wrappers unless they discharge one of these direct leaves. "
        "Reviewer must check that the remaining boundary is strictly smaller, not merely renamed, and that `python3 tools/astis.py check` passes."
    )
    post_173_guard = (
        "For SALD cycle 174 and later, the reviewer-accepted cycle-173 boundary overrides the older cycle-150 direct-leaf list. "
        "The active target is still the EM conditional-law / weak-FP Brownian/Ito backend, but the immediate live leaf is now the "
        "source-Hessian contract behind `SALD.selectedWeakTestHessianOpNormOfSourceHessianField`: "
        "`hSourceHasHessian : forall z, HasFDerivAt (fderiv Real sourceTest) (sourceHessian z) z` and "
        "`hSourceHessianBound : forall z, norm (sourceHessian z) <= C1`. "
        "Upper must decide whether these fields are paper assumptions or can be derived from selected-test regularity; middle must "
        "translate that decision into a single Lean theorem/proof-obligation with source anchors; lower_1 should give the natural-language "
        "Mathlib route, using ASTIS `TechnicalLemmas` first and external SLT Taylor/DCT/measure files only as port references; lower_2 should implement exactly one compiled "
        "theorem or strictly smaller source-cited boundary. "
        "Reject routes that define `sourceHessian` from the desired conclusion, reintroduce `SelectedWeakTestC2bBoundedHessian` without source "
        "support, use VP score-Hessian regularity for the selected weak test, import SLT as a dependency, call upstream SLT declarations directly, or return to consumer-wrapper churn. "
        "If the source-Hessian fields are confirmed absent from the paper source, keep the gap honest and move only to the next connected "
        "Brownian/Ito leaf: selected-line Taylor domination, Gaussian dominated-convergence integrability, quadratic-variation normalization, "
        "or per-coordinate Hessian generator identity."
    )
    post_183_guard = (
        "For SALD cycle 183 and later, the source-Hessian fields "
        "`hSourceHasHessian` and `hSourceHessianBound` are no longer an active "
        "proof target unless the original SALD source explicitly supplies the "
        "selected weak-test Hessian regularity. Treat them as a documented "
        "source-contract gap and move proof effort to the Brownian/Ito frozen "
        "backend tickets: `hBrownianCoordinateGeneratorTaylorIntegralDef`, "
        "`hRemainderGeneratorLimitDef`, conditional-drift weak-FP, KL derivative, "
        "and divergence/FI/IBP handoff. Reject source-Hessian wrapper churn, "
        "`testRegular` repackaging, VP score-Hessian substitution, direct SLT "
        "dependency use, or broad theorem-route replay."
    )
    role_specific = {
        "upper": (
            "Choose one faithful-paper objective, mode discipline, non-goals, lower packet, and reviewer checklist. "
            "Read only the compact context pack, blueprint state, human TODO, task-local paper memory, and technical lemma memory before assigning work; do not replay long historical logs. "
            "First read the compact context pack and run the self-reflection guard: if the planned packet is wrapper churn, reject it and choose a narrower target. "
            "Use the LeanMarathon-inspired proof blueprint: choose either the current dynamic leaf candidate for worker-style proof discharge, or a named illness-area refiner packet when the blocker affects a connected sub-DAG. "
            "Begin with a concise `Global phase judgment:` paragraph that answers: did the previous cycle fail and need recovery; is Phase 1 theorem-skeleton translation stable enough for cited-theory backfill; and which single lower packet now reduces the largest proof risk. "
            "For SALD after cycle 69, treat the theorem-skeleton route as stable enough for single-backend backfill. Keep the source theorem fixed and now prioritize the active EM conditional-law/Fokker--Planck backend over new transcript/ledger expansion, broad theorem-route audits, or isolated scalar sublemmas. "
            "For SALD after cycle 84, do not let the run accumulate more supplied-hypothesis wrappers unless they discharge or strictly narrow an existing supplied hypothesis. The priority is a smallest real backend theorem boundary: conditional kernel/conditional expectation, generator-to-law weak FP, KL/log-ratio admissibility, or one named LSI/DV/Gronwall blocker. "
            "If recent trial memory shows a failed cycle after an upper or middle handoff, recover that cycle first instead of advancing to a new source target. "
            "Before assigning middle/lower work, explicitly check that the active lower packet still targets `sald.general_moving_target_discrete.em_interpolation_fp` over `appendix.tex:1358-1387`, unless reviewer identified a theorem-route blocker. "
            "Do not spend the cycle on source-index rebaseline unless reviewer found a blocking source-anchor defect. "
            "Faithful work has two phases: Phase 1 is a complete source-to-Lean transcript with exact constants and obligations; "
            "Phase 2, only after the transcript is complete, reorganizes reusable APIs for teaching, later SDE/Sampling papers, and exploratoryProof mode. "
            "Require middle to keep two-way Lean/Markdown/LaTeX synchronization, but defer polished project-article and technical-report export to the batch end. "
            "If a cited analytic theorem is too large to prove now, require a precise source-cited interface and keep its status below formalized. "
            + external_lookup_discipline()
            + " "
            "Search `AutoSamplingTheory/TechnicalLemmas`, `research-wiki/technical-lemmas`, and the compact retrieval index before assigning new probability/Taylor work. "
            f"Use `{SLT_ROOT}` only as provenance/source material for porting; do not import it as a Lake dependency or claim an SLT theorem is formalized unless an ASTIS-owned local declaration compiles. "
            + post_129_guard
            + " "
            + post_150_guard
            + " "
            + post_173_guard
            + " "
            + post_183_guard
        ),
        "middle": (
            "Maintain conversion windows, proof obligations, source indexes, technical lemma memory, SLT reuse audit, and lower packets. "
            "Use the compact context pack instead of rereading broad historical task text. "
            "Before assigning lower agents, query the task-local paper memory for the exact source-line leaf, then query ASTIS TechnicalLemmas for callable background facts and the port queue for non-callable candidates. "
            "Treat the LeanMarathon-style blueprint state as the system-of-record summary: translate only the chosen dynamic leaf or illness area into lower-ready declarations, and keep unrelated DAG regions out of scope. "
            "For SALD after cycle 69, read the TeX around the active EM conditional-law/Fokker--Planck focus and translate only that backend into lower-ready Lean declarations; avoid fresh theorem-route audits unless needed for source correctness. "
            "For SALD after cycle 84, classify every lower packet as either `discharges-supplied-hypothesis`, `narrows-source-cited-boundary`, or `rejected-wrapper-churn`; lower-ready declarations should name the exact Mathlib/local theorem boundary and source line. "
            "Before inventing an abstraction, inspect `AutoSamplingTheory/TechnicalLemmas` and the technical lemma registry; inspect local `lean-stat-learning-theory` only when a missing lemma must be ported locally under this project's toolchain. "
            "Also follow the MathCode-inspired theorem-reuse discipline: search existing ASTIS declarations, conversion windows, proof obligations, and cited-result ledgers before creating a duplicate interface. "
            "Before lower work, translate the relevant LaTeX proof step into Lean-facing declarations; after lower/reviewer work, translate accepted Lean declarations and remaining obligations back into Markdown/LaTeX notes. "
            "At the end of a multi-hour batch, perform the ARIS-style writing pass: update the generated technical-report snippets with the latest run evidence, middle-agent rule changes, source anchors, and remaining proof boundary, while keeping Lean/proof obligations authoritative. "
            + external_lookup_discipline()
            + " "
            "During this sprint, avoid broad rebaseline work, broad SLT/SDE library import, direct upstream calls, and lower packets outside the active EM backend unless reviewer found a blocker. "
            "Export the Overleaf-ready project article and the external ASTIS technical-report snippets only at the end of a multi-hour batch. "
            + post_129_guard
            + " "
            + post_150_guard
            + " "
            + post_173_guard
            + " "
            + post_183_guard
        ),
        "lower": (
            "Attempt one narrow proof-producing Lean task for the assigned active backend before creating more ledger-only obligations. Do not change the theorem target. "
            "Work on exactly one compiled theorem/proof block or one strictly smaller source-cited boundary, and name the paper-memory source line or technical-lemma registry entry used. "
            "Begin by naming the packet classification and the exact supplied hypothesis or missing theorem boundary. "
            "If this is a worker-style packet, stay inside the assigned local target/refinement region before asking for upstream changes; if it is a refiner-style packet, edit only the connected illness area named by middle. "
            "Do not work on unrelated display algebra, route audits, or general API cleanup unless the upper/middle packet explicitly assigns it. "
            "After cycle 84, a new supplied-hypothesis wrapper is acceptable only if it removes an older supplied hypothesis, exposes a strictly smaller missing theorem boundary, or produces a compiled local theorem using Mathlib/ASTIS technical-lemma ingredients. "
            "Do not add fake proof closures; if the analysis fact is not formalized, add a precise source-cited interface or refine a ProofObligation and keep the build green. "
            "In Phase 1 faithfulPaper mode, do not introduce broad library reorganizations or educational APIs unless upper/middle explicitly assign them. "
            + post_129_guard
            + " "
            + post_150_guard
            + " "
            + post_173_guard
            + " "
            + post_183_guard
        ),
        "reviewer": (
            "Audit build gate, fake proof closures, source correspondence, cited results, technical lemma memory, and SLT port status. "
            "Reject completion claims unless Lean gate status is recorded, each active SALD paper leaf has concrete source lines in `research-wiki/paper-contributions/SALD/unfinished_source_map.md`, typed verifier feedback was logged when a lower attempt failed or partially succeeded, and every called technical lemma is an ASTIS-owned compiled local declaration. "
            "Also audit efficiency: reject a successful-looking cycle if it consumed the prompt on broad context replay, wrapper churn, or a non-active target while the compact context pack names a narrower blocker. "
            "Apply LeanMarathon-style target-review discipline: no more/no less than the source theorem, deterministic gate is the only progress authority, and a worker packet may not escape its local region without a concrete issue. "
            "Reject contract drift, missing source anchors, or any claim marked proved without a compiled Lean declaration. "
            "Use the MathCode-inspired diagnostics policy: hidden `axiom`, `constant`, `postulate`, `sorry`, `admit`, `Prop := True`, or `:= trivial` closures are blocking defects, and proof statistics should be used to notice suspicious broad rewrites. "
            "Also check backend-focus discipline: reject cycles that only add rebaseline/ledger work, broad route audits, unrelated display algebra, SLT import claims, or direct upstream calls when the active EM conditional-law/Fokker--Planck backend could have been advanced. "
            + post_150_guard
            + " "
            + post_173_guard
            + " "
            + post_183_guard
        ),
    }[role]
    if role == "lower" and lower_count >= 2:
        if role_name == "lower_1":
            role_specific += (
                "\n\nParallel lower specialization: you are the natural-language proof scout. "
                "Your primary job is to reason mathematically from the source proof, Mathlib-style measure/SDE facts, and local Lean declarations before the Lean implementer runs. "
                "Produce a precise proof route for the current boundary, list the exact hypotheses needed, name the expected Lean theorem shape, and identify which Mathlib/local lemmas should discharge each step. "
                "You may add or refine a narrowly scoped ProofObligation or conversion-window row, but do not spend the packet on broad documentation and do not claim formalization unless a local declaration compiles. "
                "End with a lower_2-ready handoff that states one theorem/proof block to implement next."
            )
        elif role_name == "lower_2":
            role_specific += (
                "\n\nParallel lower specialization: you are the Lean proof implementer. "
                "First read the shared dialogue for the lower_1 natural-language proof scout handoff, then implement exactly one compiled Lean theorem or a strictly smaller source-cited boundary from that route. "
                "If lower_1's route is invalid, record the precise failure and implement the next smallest correct boundary instead. "
                "Keep the build green and do not broaden the target."
            )
        elif role_name == "lower_3":
            role_specific += (
                "\n\nParallel lower specialization: you are the technical-lemma/API scout. "
                "Work only when middle_technical_lemma or middle_formalizer identifies a missing background fact. "
                "Search local ASTIS declarations and Mathlib/SLT provenance, then either port one tiny ASTIS-owned lemma that compiles or record a precise ProofObligation with the exact source and use site. "
                "In parallel-lower runs, prefer a run-local retrieval packet or isolated TechnicalLemmas edit; avoid editing the same SALD theorem block that lower_2 is likely to touch. "
                "Do not attack the root SALD theorem directly."
            )
        elif role_name == "lower_4":
            role_specific += (
                "\n\nParallel lower specialization: you are the refiner after a concrete Lean failure. "
                "Read lower_2's failed goal or reviewer feedback and reduce it to the smallest missing lemma, API rewrite, or source-contract gap. "
                "Do not start a new route."
            )
    if role_name in {"upper_source_math", "upper_critic"}:
        role_specific += (
            "\n\nUpper-panel profile: source-math and regularity auditor. "
            "This pass answers source-faithfulness questions for Sampling/SDE analysis. "
            "Inspect the original source anchors, assumptions, hidden regularity needs, boundary conditions, conditional-law choices, and whether the current Lean object still matches the paper object. "
            "Classify each issue as source-confirmed, standard-background-lemma-needed, source-contract-gap, or contract-drift. "
            "Do not assign broad Lean proof search. End with a recommendation to upper_director: continue the current leaf, switch to a smaller source-connected leaf, or stop a wasteful route."
        )
    elif role_name == "upper_proof_dag":
        role_specific += (
            "\n\nUpper-panel profile: proof-DAG strategist. "
            "Use the blueprint, unfinished source-line map, retrieval index, verifier feedback, and recent trials to identify the shortest dependency path from the active SALD root theorem to a closable leaf. "
            "Retire stale leaves, name active leaves ready for lower work, and recommend exactly one next leaf. "
            "For Sampling/SDE, explicitly separate SALD-owned theorem steps from background measure/KL/Fokker--Planck/Ito/Taylor lemmas."
        )
    elif role_name == "upper_process_memory":
        role_specific += (
            "\n\nUpper-panel profile: process and memory auditor. "
            "Audit whether recent 6h loops repeated wrapper churn, replayed old context, hid unresolved source-contract gaps, or produced Chinese reports that humans cannot use. "
            "Check trial summaries, memory digests, TODOs, technical-lemma status, and report entry points. "
            "Recommend one harness/prompt/report change only if it directly improves the next proof cycle."
        )
    elif role_name in {"upper_director", "upper_planner"}:
        role_specific += (
            "\n\nUpper profile: director synthesis. "
            "If upper-panel specialist prompts or handoffs exist, read them first. "
            "Resolve disagreements by source faithfulness first, proof-DAG readiness second, and process efficiency third. "
            "Then choose one executable cycle packet: one active source-line leaf, one paper-memory boundary, one technical-lemma lookup target, lower-agent split, and reviewer criteria. "
            "If no panel ran, perform a compact version of this synthesis yourself."
        )
    elif role_name in {"middle_source_correspondence", "middle_architect"}:
        role_specific += (
            "\n\nMiddle-panel profile: source-correspondence formalizer. "
            "Focus only on paper-to-Lean correspondence: exact LaTeX line range, paper object, Lean declaration, hypotheses, and proof-obligation boundary. "
            "Classify what is SALD-owned, what is prior background analysis, and what is ASTIS-local semantic glue. "
            "Do not search broadly for library lemmas except to name a dependency for middle_technical_lemma."
        )
    elif role_name in {"middle_technical_lemma", "middle_librarian"}:
        role_specific += (
            "\n\nMiddle-panel profile: technical-lemma retrieval curator. "
            "Focus only on reusable background facts. Search ASTIS-owned declarations, `AutoSamplingTheory/TechnicalLemmas`, `research-wiki/technical-lemmas`, the retrieval index, and local SLT reference material as provenance only. "
            "Classify each needed fact as compiled-local, needs-small-port, source-contract-gap, or irrelevant. "
            "Do not call upstream SLT as a dependency; every reusable fact must become ASTIS-owned Lean code or an explicit ProofObligation."
        )
    elif role_name == "middle_report_export":
        role_specific += (
            "\n\nMiddle-panel profile: report/export maintainer. "
            "Focus only on human-readable outputs: Chinese 6h report, Markdown status, article update, technical report snippets, and which raw logs should not be human entry points. "
            "Explain open blockers in plain language for non-Lean readers. "
            "Do not assign Lean work and do not polish prose during inner proof search; this role is mainly for final-audit synchronization."
        )
    elif role_name == "middle_formalizer":
        role_specific += (
            "\n\nMiddle profile: coordinator synthesis. "
            "If middle-panel specialist prompts or handoffs exist, read them first. "
            "Synthesize source correspondence, technical-lemma retrieval, and report/export status into one lower_1 natural-language task, one lower_2 Lean implementation task, and optionally one lower_3 technical-lemma/API scout task. "
            "If no panel ran, keep this lightweight and focus on the active proof leaf."
        )
    elif role_name == "reviewer_gate":
        role_specific += (
            "\n\nSpecialization: you are the deterministic gate reviewer. "
            "Focus on `python3 tools/astis.py check`, forbidden proof closures, source correspondence, and whether the accepted declaration actually compiles locally. "
            "Do not accept a natural-language proof as formal progress unless the corresponding Lean statement is compiled or the remaining gap is precisely recorded."
        )
    elif role_name == "reviewer_waste":
        role_specific += (
            "\n\nSpecialization: you are the progress-economics reviewer. "
            "Audit whether the cycle spent time on the best active SALD leaf, duplicated previous wrappers, replayed old context, or ignored existing technical lemma memory. "
            "Record a plain-language waste diagnosis for the 6h Chinese report: what improved, what did not improve, and which next leaf has the best expected value."
        )
    return shared + "\n## Role Instructions\n\n" + role_specific + "\n"


def make_run_dir(task_id: str, cycle: int, run_id: str = "") -> Path:
    stem = run_id or f"{file_stamp()}-{slugify(task_id)}-cycle{cycle:02d}"
    return ROOT / "runs" / stem


def base_agent_role(role_name: str) -> str:
    if role_name.startswith("upper"):
        return "upper"
    if role_name.startswith("middle"):
        return "middle"
    if role_name.startswith("reviewer"):
        return "reviewer"
    if role_name.startswith("lower"):
        return "lower"
    return role_name if role_name in BASE_AGENT_ROLES else "lower"


def prompt_role_label(path: Path) -> str:
    stem = path.stem
    match = re.match(r"^\d+_(.+)$", stem)
    return match.group(1) if match else stem


def prompt_role(path: Path) -> str:
    name = path.name
    if "upper" in name:
        return "upper"
    if "middle" in name:
        return "middle"
    if "reviewer" in name:
        return "reviewer"
    return "lower"


def validate_prompt_artifact(run_dir: Path, prompt: Path) -> tuple[Path, list[str]]:
    role = prompt_role(prompt)
    path = run_dir / "artifacts" / role / f"{prompt_role_label(prompt)}.json"
    if not path.exists():
        return path, ["typed role artifact was not published"]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return path, [f"invalid typed role artifact JSON: {exc}"]
    if not isinstance(value, dict):
        return path, ["typed role artifact must be a JSON object"]
    return path, harness.validate_role_artifact(role, value)


def create_run_cycle(
    task_id: str,
    cycle: int,
    lower_count: int,
    run_id: str = "",
    upper_panel: bool = False,
    middle_panel: bool = False,
    reviewer_waste: bool = False,
) -> Path:
    cmd_init(argparse.Namespace())
    title, task_text = task_context(task_id)
    if task_id == "ASTIS-SALD-001":
        write_sald_reproduction_todo(cycle)
    run_dir = make_run_dir(task_id, cycle, run_id)
    run_dir.mkdir(parents=True, exist_ok=False)
    context_pack = build_context_pack(task_id, title, task_text, cycle)
    capsule = harness.deterministic_capsule(ROOT)
    context = (
        "# Context\n\n"
        f"Task: `{task_id}`\n"
        f"Cycle: `{cycle}`\n"
        f"Created: `{now_stamp()}`\n"
        f"Focus: {task_cycle_focus(task_id, cycle)}\n"
        f"Compact context pack: `{rel(run_dir / '05_context_pack.md')}`\n"
    )
    harness.atomic_write_text(run_dir / "00_context.md", context)
    harness.atomic_write_text(run_dir / "05_context_pack.md", context_pack)
    harness.atomic_write_text(
        run_dir / "06_harness_capsule.json",
        json.dumps(capsule, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
    )
    harness.atomic_write_text(run_dir / "dialogue.md",
        f"# Dialogue: {task_id} cycle {cycle}\n\nAppend short role-tagged handoffs here.\n",
    )
    roles = [
        UPPER_DIRECTOR_ROLE,
        *(UPPER_PANEL_ROLES if upper_panel else ()),
        MIDDLE_COORDINATOR_ROLE,
        *(MIDDLE_PANEL_ROLES if middle_panel else ()),
        *[f"lower_{i}" for i in range(1, lower_count + 1)],
        *(FINAL_AUDIT_REVIEWER_ROLES if reviewer_waste else DEFAULT_REVIEWER_AGENT_ROLES),
    ]
    prompt_paths = []
    for role_name in roles:
        role = base_agent_role(role_name)
        (run_dir / "artifacts" / role).mkdir(parents=True, exist_ok=True)
        if role == "upper":
            if role_name == UPPER_DIRECTOR_ROLE:
                prefix = "10_upper_director"
            else:
                upper_index = list(UPPER_PANEL_ROLES).index(role_name) + 11 if role_name in UPPER_PANEL_ROLES else 19
                prefix = f"{upper_index:02d}_{role_name}"
        elif role == "middle":
            if role_name == MIDDLE_COORDINATOR_ROLE:
                prefix = "20_middle_formalizer"
            else:
                middle_index = list(MIDDLE_PANEL_ROLES).index(role_name) + 21 if role_name in MIDDLE_PANEL_ROLES else 29
                prefix = f"{middle_index:02d}_{role_name}"
        elif role == "lower":
            match = re.search(r"(\d+)$", role_name)
            lower_index = int(match.group(1)) if match else 1
            prefix = f"{29 + lower_index:02d}_{role_name}"
        else:
            if role_name == "reviewer_gate":
                prefix = "40_reviewer_gate"
            elif role_name == "reviewer_waste":
                prefix = "41_reviewer_waste"
            else:
                prefix = f"49_{role_name}"
        prompt_path = run_dir / f"{prefix}.md"
        harness.atomic_write_text(prompt_path,
            role_prompt(role, task_id, title, task_text, cycle, run_dir, context_pack, role_name=role_name, lower_count=lower_count),
        )
        prompt_paths.append(prompt_path)
    harness.atomic_write_text(run_dir / "90_handoff.md",
        f"""# Handoff

Task id: `{task_id}`
Cycle: `{cycle}`

## Upper Decision

## Middle Formalization State

## Lower Attempts

## Reviewer Findings

## Next Cycle Objective
""",
    )
    append_jsonl(run_dir / "harness-events.jsonl", {
        "schema_version": harness.HARNESS_SCHEMA_VERSION,
        "event": "cycle_created",
        "timestamp": harness.utc_stamp(),
        "task_id": task_id,
        "cycle": cycle,
        "selected_ready_leaf": capsule.get("selected_ready_leaf"),
        "prompt_order": [path.name for path in prompt_paths],
    })
    append_jsonl(TRIAL_LOG, {
        "timestamp": now_stamp(),
        "trial_id": f"{run_dir.name}-prompt-deck",
        "task_id": task_id,
        "role": "upper",
        "kind": "plan",
        "status": "queued",
        "lean_gate": "not-run",
        "artifact": rel(run_dir),
        "changed_files": [rel(path) for path in prompt_paths] + [rel(run_dir / "00_context.md"), rel(run_dir / "05_context_pack.md"), rel(run_dir / "dialogue.md")],
        "notes": (
            f"Created prompt deck with lower_count={lower_count}; "
            f"upper_panel={upper_panel}; middle_panel={middle_panel}; reviewer_waste={reviewer_waste}."
        ),
    })
    write_trial_summary(load_jsonl(TRIAL_LOG))
    add_manifest("astis.py run-cycle", run_dir / "00_context.md", "run", f"Created prompt deck for {task_id}")
    return run_dir


def cmd_run_cycle(args: argparse.Namespace) -> int:
    run_dir = create_run_cycle(
        args.task,
        args.cycle,
        args.lower_count,
        args.run_id,
        upper_panel=args.upper_panel,
        middle_panel=args.middle_panel,
        reviewer_waste=args.reviewer_waste,
    )
    print(f"created {rel(run_dir)}")
    print("agent prompts:")
    for path in sorted(run_dir.glob("*.md")):
        if path.name != "dialogue.md":
            print(f"- {rel(path)}")
    return 0


def format_agent_command(template: str, prompt: Path, run_dir: Path, task_id: str, cycle: int) -> str:
    role = prompt_role(prompt)
    return template.format(
        root=str(ROOT),
        prompt=str(prompt),
        run_dir=str(run_dir),
        task=task_id,
        cycle=cycle,
        role=role,
    )


def run_agent_command(template: str, prompt: Path, run_dir: Path, task_id: str, cycle: int) -> int:
    command = format_agent_command(template, prompt, run_dir, task_id, cycle)
    print("$ " + command)
    completed = subprocess.run(command, cwd=ROOT, shell=True)
    return completed.returncode


def run_agent_commands_parallel(
    template: str,
    prompts: list[Path],
    run_dir: Path,
    task_id: str,
    cycle: int,
) -> list[dict]:
    log_dir = run_dir / "agent-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    launched = []
    for prompt in prompts:
        command = format_agent_command(template, prompt, run_dir, task_id, cycle)
        log_path = log_dir / f"{prompt.stem}.log"
        handle = log_path.open("wb")
        print("$ " + command + f" > {rel(log_path)} 2>&1 &")
        proc = subprocess.Popen(
            command,
            cwd=ROOT,
            shell=True,
            stdout=handle,
            stderr=subprocess.STDOUT,
        )
        launched.append({
            "prompt": prompt,
            "command": command,
            "log_path": log_path,
            "handle": handle,
            "proc": proc,
            "started": time.monotonic(),
        })

    results = []
    for item in launched:
        code = item["proc"].wait()
        ended = time.monotonic()
        item["handle"].close()
        elapsed = ended - item["started"]
        results.append({
            "prompt": item["prompt"],
            "code": code,
            "elapsed": elapsed,
            "log_path": item["log_path"],
        })
        print(
            f"parallel agent {item['prompt'].name} exit={code} "
            f"active_agent_seconds={elapsed:.1f} log={rel(item['log_path'])}"
        )
    return results


def upper_prompt_sequence(run_dir: Path, use_panel: bool) -> list[Path]:
    director = run_dir / "10_upper_director.md"
    if not use_panel:
        return [director]
    specialists = [
        run_dir / "11_upper_source_math.md",
        run_dir / "12_upper_proof_dag.md",
        run_dir / "13_upper_process_memory.md",
    ]
    return [path for path in specialists if path.exists()] + [director]


def middle_prompt_sequence(run_dir: Path, use_panel: bool) -> list[Path]:
    coordinator = run_dir / "20_middle_formalizer.md"
    if not use_panel:
        return [coordinator]
    specialists = [
        run_dir / "21_middle_source_correspondence.md",
        run_dir / "22_middle_technical_lemma.md",
        run_dir / "23_middle_report_export.md",
    ]
    return [path for path in specialists if path.exists()] + [coordinator]


def cycle_prompt_paths(run_dir: Path, skip_reviewer: bool, upper_panel: bool = False, middle_panel: bool = False) -> list[Path]:
    prompts = [
        *upper_prompt_sequence(run_dir, upper_panel),
        *middle_prompt_sequence(run_dir, middle_panel),
        *sorted(run_dir.glob("3*_lower_*.md")),
    ]
    if not skip_reviewer:
        reviewer_prompts = sorted(run_dir.glob("4*_reviewer*.md")) or [run_dir / "40_reviewer.md"]
        prompts.extend(reviewer_prompts)
    return [path for path in prompts if path.exists()]


def latest_cycle_number(task_id: str) -> int:
    task_slug = slugify(task_id)
    pattern = re.compile(re.escape(task_slug) + r"-cycle(\d+)")
    latest = 0
    for path in (ROOT / "runs").glob(f"*-{task_slug}-cycle*"):
        match = pattern.search(path.name)
        if match:
            latest = max(latest, int(match.group(1)))
    return latest


def execute_prompt_deck(args: argparse.Namespace, run_dir: Path, cycle: int) -> int:
    final_code = 0
    active_agent_seconds = 0.0
    event_log = run_dir / "harness-events.jsonl"
    interrupted = harness.recover_run_events(event_log)
    if interrupted:
        print(f"recovered {len(interrupted)} interrupted role execution(s)")
    prompts = cycle_prompt_paths(
        run_dir,
        args.skip_reviewer,
        getattr(args, "upper_panel", False),
        getattr(args, "middle_panel", False),
    )
    index = 0
    while index < len(prompts):
        prompt = prompts[index]
        if getattr(args, "parallel_lower", False) and prompt_role(prompt) == "lower":
            lower_prompts = []
            while index < len(prompts) and prompt_role(prompts[index]) == "lower":
                lower_prompts.append(prompts[index])
                index += 1
            for lower_prompt in lower_prompts:
                append_jsonl(event_log, {
                    "schema_version": harness.HARNESS_SCHEMA_VERSION,
                    "event": "role_started",
                    "timestamp": harness.utc_stamp(),
                    "execution_id": f"{run_dir.name}-{lower_prompt.stem}",
                    "task_id": args.task,
                    "cycle": cycle,
                    "role": prompt_role_label(lower_prompt),
                    "prompt": rel(lower_prompt),
                })
            results = run_agent_commands_parallel(args.agent_cmd, lower_prompts, run_dir, args.task, cycle)
            for result in results:
                elapsed = float(result["elapsed"])
                code = int(result["code"])
                artifact_path, artifact_errors = validate_prompt_artifact(run_dir, result["prompt"])
                if code == 0 and artifact_errors:
                    code = 2
                active_agent_seconds += elapsed
                status = "accepted" if code == 0 else "failed"
                append_jsonl(event_log, {
                    "schema_version": harness.HARNESS_SCHEMA_VERSION,
                    "event": "role_completed" if code == 0 else "role_failed",
                    "timestamp": harness.utc_stamp(),
                    "execution_id": f"{run_dir.name}-{result['prompt'].stem}",
                    "task_id": args.task,
                    "cycle": cycle,
                    "role": prompt_role_label(result["prompt"]),
                    "exit_code": code,
                    "active_agent_seconds": elapsed,
                    "typed_artifact": rel(artifact_path),
                    "artifact_errors": artifact_errors,
                })
                append_jsonl(TRIAL_LOG, {
                    "timestamp": now_stamp(),
                    "trial_id": f"{run_dir.name}-{result['prompt'].stem}",
                    "task_id": args.task,
                    "role": prompt_role_label(result["prompt"]),
                    "kind": "attempt",
                    "status": status,
                    "lean_gate": "not-run",
                    "artifact": rel(result["prompt"]),
                    "changed_files": git_changed_files(),
                    "notes": (
                        f"Parallel external agent command exit code {code}. "
                        f"active_agent_seconds={elapsed:.1f}. "
                        f"log={rel(result['log_path'])}. "
                        f"typed_artifact_errors={artifact_errors}."
                    ),
                })
                write_trial_summary(load_jsonl(TRIAL_LOG))
                if code != 0 and final_code == 0:
                    final_code = code
            if final_code != 0:
                break
            continue
        append_jsonl(event_log, {
            "schema_version": harness.HARNESS_SCHEMA_VERSION,
            "event": "role_started",
            "timestamp": harness.utc_stamp(),
            "execution_id": f"{run_dir.name}-{prompt.stem}",
            "task_id": args.task,
            "cycle": cycle,
            "role": prompt_role_label(prompt),
            "prompt": rel(prompt),
        })
        started = time.monotonic()
        code = run_agent_command(args.agent_cmd, prompt, run_dir, args.task, cycle)
        elapsed = time.monotonic() - started
        artifact_path, artifact_errors = validate_prompt_artifact(run_dir, prompt)
        if code == 0 and artifact_errors:
            code = 2
        active_agent_seconds += elapsed
        status = "accepted" if code == 0 else "failed"
        append_jsonl(event_log, {
            "schema_version": harness.HARNESS_SCHEMA_VERSION,
            "event": "role_completed" if code == 0 else "role_failed",
            "timestamp": harness.utc_stamp(),
            "execution_id": f"{run_dir.name}-{prompt.stem}",
            "task_id": args.task,
            "cycle": cycle,
            "role": prompt_role_label(prompt),
            "exit_code": code,
            "active_agent_seconds": elapsed,
            "typed_artifact": rel(artifact_path),
            "artifact_errors": artifact_errors,
        })
        append_jsonl(TRIAL_LOG, {
            "timestamp": now_stamp(),
            "trial_id": f"{run_dir.name}-{prompt.stem}",
            "task_id": args.task,
            "role": prompt_role_label(prompt),
            "kind": "attempt",
            "status": status,
            "lean_gate": "not-run",
            "artifact": rel(prompt),
            "changed_files": git_changed_files(),
            "notes": (
                f"External agent command exit code {code}. active_agent_seconds={elapsed:.1f}. "
                f"typed_artifact_errors={artifact_errors}."
            ),
        })
        write_trial_summary(load_jsonl(TRIAL_LOG))
        if code != 0:
            final_code = code
            break
        index += 1
    setattr(args, "_last_agent_seconds", active_agent_seconds)
    if args.check_each_cycle:
        code = cmd_check(argparse.Namespace())
        append_jsonl(TRIAL_LOG, {
            "timestamp": now_stamp(),
            "trial_id": f"{run_dir.name}-build-gate",
            "task_id": args.task,
            "role": "reviewer",
            "kind": "build",
            "status": "compiled" if code == 0 else "failed",
            "lean_gate": "pass" if code == 0 else "fail",
            "artifact": rel(run_dir),
            "changed_files": git_changed_files(),
            "notes": "Cycle build gate.",
        })
        write_trial_summary(load_jsonl(TRIAL_LOG))
        if code != 0:
            return code
    return final_code


def cmd_sleep_run(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    if args.execute and not args.agent_cmd:
        raise SystemExit("--execute requires --agent-cmd")
    if args.dry_run and args.execute:
        raise SystemExit("--dry-run and --execute cannot be used together")
    final_code = 0
    for cycle in range(1, args.cycles + 1):
        run_dir = create_run_cycle(
            args.task,
            cycle,
            args.lower_count,
            upper_panel=args.upper_panel,
            middle_panel=args.middle_panel,
            reviewer_waste=args.reviewer_waste,
        )
        print(f"cycle {cycle}: {rel(run_dir)}")
        if args.dry_run or not args.agent_cmd:
            print("dry run: prompt deck created, no external agent command executed")
            continue
        if not args.execute:
            print("agent command configured but not executed; pass --execute to run it")
            continue
        final_code = execute_prompt_deck(args, run_dir, cycle)
        if final_code != 0:
            return final_code
        post_cycle_refresh(args.task, cycle, run_dir, write_zh_summary=False)
    return final_code


def cmd_sleep_run_window(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    if args.execute and not args.agent_cmd:
        raise SystemExit("--execute requires --agent-cmd")
    if args.dry_run and args.execute:
        raise SystemExit("--dry-run and --execute cannot be used together")

    start = time.monotonic()
    deadline = start + args.hours * 3600.0
    guard_seconds = max(args.guard_minutes, 0.0) * 60.0
    agent_budget_seconds = max(getattr(args, "agent_hours_budget", 0.0), 0.0) * 3600.0
    use_agent_budget = agent_budget_seconds > 0.0
    active_agent_seconds_total = 0.0
    cycle = args.start_cycle or latest_cycle_number(args.task) + 1
    completed = 0
    final_code = 0

    while completed < args.max_cycles:
        if use_agent_budget:
            remaining = agent_budget_seconds - active_agent_seconds_total
            wall_remaining = deadline - time.monotonic()
            if completed > 0 and wall_remaining <= 0:
                print("wall-clock safety window elapsed after completed cycle")
                break
            if completed > 0 and remaining <= guard_seconds:
                print("active-agent budget closed before starting another cycle")
                break
            if completed == 0 and remaining <= 0:
                print("active-agent budget elapsed before first cycle; starting one final cycle by request")
            elif completed > 0 and remaining <= 0:
                print("active-agent budget elapsed after completed cycle")
                break
        else:
            remaining = deadline - time.monotonic()
            if completed > 0 and remaining <= guard_seconds:
                print("window closed before starting another cycle")
                break
            if completed == 0 and remaining <= 0:
                print("window elapsed before first cycle; starting one final cycle by request")
            elif completed > 0 and remaining <= 0:
                print("window elapsed after completed cycle")
                break

        run_dir = create_run_cycle(
            args.task,
            cycle,
            args.lower_count,
            upper_panel=args.upper_panel,
            middle_panel=args.middle_panel,
            reviewer_waste=args.reviewer_waste,
        )
        print(f"cycle {cycle}: {rel(run_dir)}")
        if use_agent_budget:
            print("cycle will run to completion even if the active-agent budget expires")
        else:
            print("cycle will run to completion even if the wall-clock window expires")

        if args.dry_run or not args.agent_cmd:
            print("dry run: prompt deck created, no external agent command executed")
            completed += 1
            cycle += 1
            continue
        if not args.execute:
            print("agent command configured but not executed; pass --execute to run it")
            completed += 1
            cycle += 1
            continue

        final_code = execute_prompt_deck(args, run_dir, cycle)
        active_agent_seconds_total += float(getattr(args, "_last_agent_seconds", 0.0))
        if use_agent_budget:
            print(f"active-agent seconds used: {active_agent_seconds_total:.1f} / {agent_budget_seconds:.1f}")
        if final_code == 0:
            post_cycle_refresh(args.task, cycle, run_dir, write_zh_summary=False)
        completed += 1
        cycle += 1
        if final_code != 0:
            return final_code

    if final_code == 0 and (args.upper_panel_final or args.middle_panel_final or args.reviewer_waste_final):
        final_run_dir = create_run_cycle(
            args.task,
            cycle,
            0,
            upper_panel=args.upper_panel_final,
            middle_panel=args.middle_panel_final,
            reviewer_waste=args.reviewer_waste_final,
        )
        print(f"final audit cycle {cycle}: {rel(final_run_dir)}")
        if args.dry_run or not args.agent_cmd:
            print("dry run: final audit prompt deck created, no external agent command executed")
        elif not args.execute:
            print("agent command configured but not executed; pass --execute to run final audit")
        else:
            final_args = argparse.Namespace(**vars(args))
            final_args.upper_panel = args.upper_panel_final
            final_args.middle_panel = args.middle_panel_final
            final_args.skip_reviewer = False
            final_code = execute_prompt_deck(final_args, final_run_dir, cycle)
            active_agent_seconds_total += float(getattr(final_args, "_last_agent_seconds", 0.0))
            if final_code != 0:
                return final_code
            post_cycle_refresh(args.task, cycle, final_run_dir, write_zh_summary=False)
        cycle += 1

    append_jsonl(TRIAL_LOG, {
        "timestamp": now_stamp(),
        "trial_id": f"{file_stamp()}-{slugify(args.task)}-sleep-window",
        "task_id": args.task,
        "role": "upper",
        "kind": "compression",
        "status": "accepted" if final_code == 0 else "failed",
        "lean_gate": "not-run",
        "artifact": "runs",
        "changed_files": git_changed_files(),
        "notes": (
            f"Graceful sleep window completed {completed} cycle(s); final cycle was not interrupted; "
            f"active_agent_seconds={active_agent_seconds_total:.1f}; "
            f"agent_budget_seconds={agent_budget_seconds:.1f}."
        ),
    })
    write_trial_summary(load_jsonl(TRIAL_LOG))

    if args.after_latex and final_code == 0:
        if args.task == "ASTIS-SALD-001":
            final_code = cmd_finalize_sald_cycle(argparse.Namespace(cycle=cycle - 1, run_check=False))
        else:
            final_code = cmd_export_latex(argparse.Namespace(task=args.task))
    return final_code


def cmd_launch_six_hour_sald(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    def env_flag(name: str, default: bool) -> bool:
        value = os.environ.get(name)
        if value is None:
            return default
        return value.strip().lower() not in {"0", "false", "no", "off", ""}

    logs_dir = ROOT / "runs" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    next_cycle = args.start_cycle or latest_cycle_number("ASTIS-SALD-001") + 1
    blueprint_path = write_blueprint_refresh("ASTIS-SALD-001")
    blueprint_md, _ = write_blueprint_status("ASTIS-SALD-001")
    context_path = write_context_pack("ASTIS-SALD-001", next_cycle)
    stamp = file_stamp()
    log_path = logs_dir / f"astis-sald-001-6h-{stamp}.log"
    pid_path = logs_dir / f"astis-sald-001-6h-{stamp}.pid"
    command = [
        sys.executable,
        "tools/astis.py",
        "sleep-run-window",
        "ASTIS-SALD-001",
        "--hours",
        str(args.wall_hours),
        "--agent-hours-budget",
        str(args.hours),
        "--max-cycles",
        str(args.max_cycles),
        "--lower-count",
        str(args.lower_count),
        "--agent-cmd",
        "bash tools/astis_codex_faithful.sh {root} {prompt}",
        "--execute",
        "--check-each-cycle",
    ]
    upper_panel_inner = env_flag("ASTIS_UPPER_PANEL_INNER", args.upper_panel_inner)
    middle_panel_inner = env_flag("ASTIS_MIDDLE_PANEL_INNER", args.middle_panel_inner)
    reviewer_waste_inner = env_flag("ASTIS_REVIEWER_WASTE_INNER", args.reviewer_waste_inner)
    upper_panel_final = env_flag("ASTIS_UPPER_PANEL_FINAL", args.upper_panel_final)
    middle_panel_final = env_flag("ASTIS_MIDDLE_PANEL_FINAL", args.middle_panel_final)
    reviewer_waste_final = env_flag("ASTIS_REVIEWER_WASTE_FINAL", args.reviewer_waste_final)
    parallel_lower = env_flag("ASTIS_PARALLEL_LOWER", args.parallel_lower)
    if upper_panel_inner:
        command.append("--upper-panel")
    if middle_panel_inner:
        command.append("--middle-panel")
    if reviewer_waste_inner:
        command.append("--reviewer-waste")
    if upper_panel_final:
        command.append("--upper-panel-final")
    if middle_panel_final:
        command.append("--middle-panel-final")
    if reviewer_waste_final:
        command.append("--reviewer-waste-final")
    if parallel_lower:
        command.append("--parallel-lower")
    if args.after_latex:
        command.append("--after-latex")
    if getattr(args, "start_cycle", 0):
        command.extend(["--start-cycle", str(args.start_cycle)])
    if args.skip_reviewer:
        command.append("--skip-reviewer")
    with log_path.open("wb") as log:
        log.write(("$ " + " ".join(subprocess.list2cmdline([part]) for part in command) + "\n").encode("utf-8"))
        log.flush()
        proc = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    pid = str(proc.pid)
    pid_path.write_text(pid + "\n", encoding="utf-8")
    add_manifest("astis.py launch-sald-6h", log_path, "run", "Started graceful 6-hour ASTIS-SALD-001 Codex faithful-paper run")
    print("started ASTIS-SALD-001 graceful active-agent-budget run")
    print(f"pid: {pid}")
    print(f"active-agent-hours: {args.hours}")
    print(f"wall-hours safety: {args.wall_hours}")
    print(
        "panel cadence: "
        f"upper_inner={int(upper_panel_inner)} upper_final={int(upper_panel_final)} "
        f"middle_inner={int(middle_panel_inner)} middle_final={int(middle_panel_final)} "
        f"reviewer_waste_inner={int(reviewer_waste_inner)} reviewer_waste_final={int(reviewer_waste_final)}"
    )
    print(f"lower-count: {args.lower_count}; parallel-lower: {int(parallel_lower)}")
    print(f"batch-end report export: {'enabled' if args.after_latex else 'disabled'}")
    print(f"log: {rel(log_path)}")
    print(f"pid-file: {rel(pid_path)}")
    print(f"blueprint: {rel(blueprint_path)}")
    print(f"blueprint-status: {rel(blueprint_md)}")
    print(f"next-cycle context-pack: {rel(context_path)}")
    return 0


def cmd_launch_six_hour_chewi(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())

    def env_flag(name: str, default: bool) -> bool:
        value = os.environ.get(name)
        if value is None:
            return default
        return value.strip().lower() not in {"0", "false", "no", "off", ""}

    logs_dir = ROOT / "runs" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    task_id = "ASTIS-CHEWI-001"
    next_cycle = args.start_cycle or latest_cycle_number(task_id) + 1
    blueprint_path = write_blueprint_refresh(task_id)
    blueprint_md, _ = write_blueprint_status(task_id)
    context_path = write_context_pack(task_id, next_cycle)
    write_chewi_foundation_docs()
    stamp = file_stamp()
    log_path = logs_dir / f"astis-chewi-001-6h-{stamp}.log"
    pid_path = logs_dir / f"astis-chewi-001-6h-{stamp}.pid"
    command = [
        sys.executable,
        "tools/astis.py",
        "sleep-run-window",
        task_id,
        "--hours",
        str(args.wall_hours),
        "--agent-hours-budget",
        str(args.hours),
        "--max-cycles",
        str(args.max_cycles),
        "--lower-count",
        str(args.lower_count),
        "--agent-cmd",
        "bash tools/astis_codex_faithful.sh {root} {prompt}",
        "--execute",
        "--check-each-cycle",
    ]
    upper_panel_inner = env_flag("ASTIS_CHEWI_UPPER_PANEL_INNER", args.upper_panel_inner)
    middle_panel_inner = env_flag("ASTIS_CHEWI_MIDDLE_PANEL_INNER", args.middle_panel_inner)
    reviewer_waste_inner = env_flag("ASTIS_CHEWI_REVIEWER_WASTE_INNER", args.reviewer_waste_inner)
    upper_panel_final = env_flag("ASTIS_CHEWI_UPPER_PANEL_FINAL", args.upper_panel_final)
    middle_panel_final = env_flag("ASTIS_CHEWI_MIDDLE_PANEL_FINAL", args.middle_panel_final)
    reviewer_waste_final = env_flag("ASTIS_CHEWI_REVIEWER_WASTE_FINAL", args.reviewer_waste_final)
    parallel_lower = env_flag("ASTIS_CHEWI_PARALLEL_LOWER", args.parallel_lower)
    if upper_panel_inner:
        command.append("--upper-panel")
    if middle_panel_inner:
        command.append("--middle-panel")
    if reviewer_waste_inner:
        command.append("--reviewer-waste")
    if upper_panel_final:
        command.append("--upper-panel-final")
    if middle_panel_final:
        command.append("--middle-panel-final")
    if reviewer_waste_final:
        command.append("--reviewer-waste-final")
    if parallel_lower:
        command.append("--parallel-lower")
    if args.after_latex:
        command.append("--after-latex")
    if getattr(args, "start_cycle", 0):
        command.extend(["--start-cycle", str(args.start_cycle)])
    if args.skip_reviewer:
        command.append("--skip-reviewer")
    with log_path.open("wb") as log:
        log.write(("$ " + " ".join(subprocess.list2cmdline([part]) for part in command) + "\n").encode("utf-8"))
        log.flush()
        proc = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    pid = str(proc.pid)
    pid_path.write_text(pid + "\n", encoding="utf-8")
    add_manifest("astis.py launch-log-concave-6h", log_path, "run", "Started graceful 6-hour ASTIS-CHEWI-001 Codex foundation run")
    print("started ASTIS-CHEWI-001 graceful active-agent-budget run")
    print(f"pid: {pid}")
    print(f"active-agent-hours: {args.hours}")
    print(f"wall-hours safety: {args.wall_hours}")
    print(
        "panel cadence: "
        f"upper_inner={int(upper_panel_inner)} upper_final={int(upper_panel_final)} "
        f"middle_inner={int(middle_panel_inner)} middle_final={int(middle_panel_final)} "
        f"reviewer_waste_inner={int(reviewer_waste_inner)} reviewer_waste_final={int(reviewer_waste_final)}"
    )
    print(f"lower-count: {args.lower_count}; parallel-lower: {int(parallel_lower)}")
    print(f"batch-end report export: {'enabled' if args.after_latex else 'disabled'}")
    print(f"log: {rel(log_path)}")
    print(f"pid-file: {rel(pid_path)}")
    print(f"blueprint: {rel(blueprint_path)}")
    print(f"blueprint-status: {rel(blueprint_md)}")
    print(f"next-cycle context-pack: {rel(context_path)}")
    print(f"library overview: {rel(LOG_CONCAVE_OVERVIEW_MD)}")
    print(f"execution pack: {rel(LOG_CONCAVE_EXECUTION_PACK_MD)}")
    return 0


def latest_log_file() -> Path | None:
    logs_dir = ROOT / "runs" / "logs"
    logs = sorted(logs_dir.glob("astis-sald-001-6h-*.log")) if logs_dir.exists() else []
    return logs[-1] if logs else None


def latest_sald_window_info() -> dict:
    """Return lightweight metadata for the latest SALD long-window run."""

    log_path = latest_log_file()
    if log_path is None or not log_path.exists():
        return {
            "log": "",
            "cycles": [],
            "final_audit_cycles": [],
            "cycle_range": "unknown",
            "proof_cycle_range": "unknown",
            "final_audit_cycle": "",
            "active_agent_seconds": "",
        }
    text = read_text(log_path)
    cycles = [int(value) for value in re.findall(r"^cycle\s+(\d+):", text, flags=re.M)]
    final_audit_cycles = [
        int(value) for value in re.findall(r"^final audit cycle\s+(\d+):", text, flags=re.M)
    ]
    all_cycles = cycles + final_audit_cycles
    active_matches = re.findall(r"active-agent seconds used:\s*([0-9.]+)\s*/\s*([0-9.]+)", text)
    if all_cycles:
        cycle_range = f"{min(all_cycles)}-{max(all_cycles)}" if min(all_cycles) != max(all_cycles) else str(all_cycles[0])
    else:
        cycle_range = "unknown"
    if cycles:
        proof_cycle_range = f"{min(cycles)}-{max(cycles)}" if min(cycles) != max(cycles) else str(cycles[0])
    else:
        proof_cycle_range = "unknown"
    active = ""
    if active_matches:
        used, budget = active_matches[-1]
        active = f"{used} / {budget} seconds"
    return {
        "log": rel(log_path),
        "cycles": cycles,
        "final_audit_cycles": final_audit_cycles,
        "cycle_range": cycle_range,
        "proof_cycle_range": proof_cycle_range,
        "final_audit_cycle": str(max(final_audit_cycles)) if final_audit_cycles else "",
        "active_agent_seconds": active,
    }


def sald_blocker_plain_language(blocker: str) -> dict[str, str]:
    """Translate the latest reviewer decision into a short human-facing summary."""

    if "emInterpolationConditionalWeakFp" in blocker:
        return {
            "current_leaf": "`emInterpolationConditionalWeakFp`",
            "source_ref": "`appendix.tex:1358-1365`, `appendix.tex:1368-1377`, `appendix.tex:1379-1387`",
            "lean_boundary": "`sald.general_moving_target_discrete.em_interpolation_fp -> emInterpolationConditionalWeakFp`",
            "progress": (
                "final audit 已经停止继续围绕 `hRemainderPullbackDef` 换名字打转，"
                "把下一步改成 conditional-law weak Fokker--Planck 的最小边界。"
            ),
            "next_action": (
                "下一轮 lower agent 只做一个目标：证明 conditional generator-to-law weak action "
                "的一个非 wrapper theorem，或者把它缩小成更精确的 source-contract gap。"
            ),
        }
    if "hRemainderPullbackDef" in blocker:
        return {
            "current_leaf": "`hRemainderPullbackDef`",
            "source_ref": "`appendix.tex:958-970`, `appendix.tex:983-996`, `appendix.tex:1161-1170`, `appendix.tex:1379-1387`",
            "lean_boundary": "`hRemainderGeneratorLimitDef -> hRemainderPullbackDef`",
            "progress": (
                "本轮把 Gaussian/Taylor remainder 的大边界缩小到了 remainder pullback "
                "definition，但还没有找到足够具体的原文定义来直接关闭。"
            ),
            "next_action": (
                "先找原文或本地 declaration 中 remainderGeneratorLimit、normalizedRemainder "
                "和 scalarBrownianCoordinate 的可展开定义；找不到就不要继续 wrapper churn。"
            ),
        }
    return {
        "current_leaf": "`latest reviewer blocker`",
        "source_ref": "`research-wiki/paper-contributions/SALD/unfinished_source_map.md`",
        "lean_boundary": "`state.latest_blocker`",
        "progress": "reviewer 记录了一个剩余边界，但 summary 生成器没有识别出专门模式。",
        "next_action": "下一轮先让 middle agent 把该 blocker 翻译成一个具体 source-line leaf。",
    }


def chinese_sald_window_summary_text(
    task: str,
    export_date: str,
    source_count: int,
    trial_count: int,
    state: dict,
    handoffs: list[str],
    diagnostics: dict,
) -> str:
    window = latest_sald_window_info()
    status_counts = "\n".join(
        f"- `{key}`: {value}" for key, value in sorted(state["proof_status_counts"].items())
    )
    packet_counts = "\n".join(
        f"- `{key}`: {value}" for key, value in state["trial_classifications_recent"].items()
    )
    handoff_text = "\n".join(f"- {note}" for note in handoffs) or "- 暂无最近 handoff。"
    totals = diagnostics.get("totals", {})
    theorem_count = totals.get("theorem", "unknown")
    def_count = totals.get("def", "unknown")
    forbidden_hits = totals.get("forbidden_hits", "unknown")
    gate_status = latest_lean_gate_status(task)
    blocker_info = sald_blocker_plain_language(state["latest_blocker"])
    unfinished_items = sald_unfinished_source_items() if task == "ASTIS-SALD-001" else []
    unfinished_table = unfinished_source_markdown_table(unfinished_items) if unfinished_items else "| none | none | none | none | none | none |"
    technical_ports = technical_lemma_port_queue_rows()
    technical_port_text = "\n".join(
        f"- `{row.get('upstream_file', '')}` -> {format_decl_list(row.get('upstream_declarations', row.get('upstream_decl', '')))}; target: {row.get('astis_target', row.get('target_local_module', ''))}; status: {row.get('status', '')}"
        for row in technical_ports[:8]
    ) or "- 当前没有单独的 port queue 条目；仍需检查 registry 中非 `formalized-local` 的条目。"
    return f"""# ASTIS 6h 中文复盘：{task}

- 导出时间: {export_date}
- 本轮 proof cycles: {window["proof_cycle_range"]}
- final audit cycle: {window["final_audit_cycle"] or "none"}
- 本轮日志: `{window["log"]}`
- active-agent 用量: {window["active_agent_seconds"] or "unknown"}
- source-indexed SALD declarations: {source_count}
- trial-log records: {trial_count}
- Lean theorem 数: {theorem_count}
- Lean def 数: {def_count}
- forbidden proof hits: {forbidden_hits}
- Lean gate 状态: {gate_status}

## 一页版结论

这轮没有完整关掉 SALD 复现的最后基础分析边界，但比之前更有效。最重要的
变化不是“又写了一堆 obligation”，而是 final audit 把系统从一个重复路线里拉出来，
重新指定了下一轮真正该攻的最小 leaf。

- **是否完成整篇复现**：没有。
- **本轮是否有有效进展**：有。Lean gate 通过；Lean theorem 数到 `{theorem_count}`，
  def 数到 `{def_count}`；并行 lower agents 正常产生独立日志。
- **本轮真正推进**：{blocker_info["progress"]}
- **当前最小 blocker**：{blocker_info["current_leaf"]}。
- **对应原文行号**：{blocker_info["source_ref"]}。
- **Lean 边界**：{blocker_info["lean_boundary"]}。
- **下一轮唯一推荐动作**：{blocker_info["next_action"]}

本轮 proof cycles 是 `{window["proof_cycle_range"]}`；`{window["final_audit_cycle"] or "none"}` 是
最终审计 cycle。final audit 不算作新增证明进度，但它对减少浪费很重要：它明确指出
不要再回到旧的 `hRemainderPullbackDef` wrapper churn，而是处理
conditional-law weak Fokker--Planck 的源文边界。

用不懂 Lean 的话说，系统仍在把论文中一句
“by the Fokker--Planck equation / integration by parts / Laplacian/Ito calculus”
拆成 Lean 必须逐项检查的对象：具体 law、条件分布代表元、test function 的可测可积性、
generator 对 test function 的 weak action，以及边界项为什么可以消失。

## 为什么“常识”还会拖很久

当前不是“VA-SALD 的核心数学想法还没写出来”。核心 theorem 的路线、原文
位置、Lean contract 和很多局部代数/高斯/Taylor 子步骤已经在系统里了。现在
卡住的是：论文把若干前置知识写成“标准结论”，但 Lean 不能接受“这是常识”
这句话，必须知道它在当前符号、当前测度、当前条件分布、当前边界条件下到底
是哪一个定理实例。

可以把剩余工作分成两类：

| 类别 | 人类怎么理解 | 现在是否 SALD 新贡献 | 为什么还要做 |
|---|---|---|---|
| SALD 本文贡献 | VA-SALD 的离散/连续 KL 收缩、moving target、guided residual、EM 插值路线 | 是 | 必须忠实对应原论文定理和 proof DAG |
| 前置 technical lemma | KL/FI/LSI、Fokker--Planck、Ito/Taylor 展开、Gaussian moment、可测/可积、IBP/边界项 | 不是 | 论文作者可以引用“常识”，Lean 需要本地可调用的精确定理 |
| source-contract gap | 原文可能默认了某个正则性假设，但没有写成 Lean 可用字段 | 介于两者之间 | 不能偷偷加假设；必须回原文定位或诚实记录为 obligation |

所以，很多“非 SALD 本身贡献”的东西拖得久，并不是因为数学上没人知道，而是
因为 ASTIS 的目标不是写自然语言证明，而是让 Lean 检查。一个常识性步骤要能
通过 Lean，通常还要补全：

1. 对象是哪一个测度或 law，不只是“分布”；
2. 函数是不是可测、可积，log-ratio 或梯度在哪些地方定义；
3. 条件期望/条件分布选了哪个代表元；
4. 积分换序、求导进积分、极限进积分的 domination 条件；
5. integration by parts 的边界项为什么为零；
6. Mathlib 或本地 lemma 的 statement 是否和论文符号完全对齐。

## 你下一轮可以怎么给 high-level 指导

你不需要读 Lean code，也可以按下面三种方向给指示：

| 你可以选择的方向 | 对系统的影响 | 适合什么时候用 |
|---|---|---|
| “先完成 SALD 本文贡献骨架，前置常识先保留为 source-cited obligation” | 文章复现速度快，但 Lean fully formalized 程度较低 | 想先看完整 proof DAG 和教学结构 |
| “优先补 technical lemma memory，把 KL/测度论/Ito/Taylor 常识都本地 Lean 化” | 后续论文复用强，但当前 SALD 完成会慢 | 想建设长期 Sampling/SDE Lean 库 |
| “只补当前最小 leaf 需要的前置 lemma，不做大库建设” | 当前最稳妥，避免无限扩张 | 适合下一轮 6h 默认策略 |

我建议默认用第三种：每轮只问“为了关掉当前 source-line leaf，最少需要哪个
常识 lemma？”如果这个 lemma 在 Mathlib 或 lean-stat-learning-theory 有类似
版本，就把它 port 成 ASTIS-owned local lemma；如果没有，就先写成精确
ProofObligation，不让 lower agent 泛泛地补测度论大库。

## 对应原文位置

这里的“原文位置”对应 ASTIS 当前 SALD 复现任务的源论文位置；类比 QBE/GHL
任务中的 `main.tex` 对照表，但本任务不是 GHL。

| 原文位置 | 内容 | 当前 Lean 复现状态 |
|---|---|---|
| `main_body.tex:301-326` | `thm:forward-KL-discrete` 离散 SALD 主定理显示式 | theorem contract 已建；分析后端仍在补 |
| `main_body.tex:372-392` | `thm:unified-forward-KL` general / guided VA-SALD 连续主定理 | theorem contract 已建；与离散后端共享部分义务 |
| `appendix.tex:982-995` | frozen EM interpolation `eq:general_moving_target_SALD_frozen_interp` | 本轮反复使用的 EM generator 来源 |
| `appendix.tex:1354-1366` | `hat rho_s` endpoint law 与 KL derivative 起点 | 已进入 proof DAG；mass/KL derivative 后端仍需精化 |
| `appendix.tex:1368-1377` | conditional drift `bar b_{{k,s}}` 定义 | conditional-law 代表元与 measurability 仍是关键基础边界 |
| `appendix.tex:1379-1387` | 论文直接写的 weak Fokker--Planck equation | 当前 6h 的核心未完成分析后端 |
| `appendix.tex:1402-1427` | divergence rewrite、Fisher information 项、IBP 入口 | Green/trace/box-divergence 与 Laplacian source leaves 仍未完全 formalized |

## 未完成 source-line map

文件位置：`research-wiki/paper-contributions/SALD/unfinished_source_map.md`

| Boundary id | Type | Source lines | Lean boundary | Status | Next action |
|---|---|---|---|---|---|
{unfinished_table}

## Technical lemma 未完成项

这些是前人/常识性技术 lemma 的 port 或本地证明队列。它们不能作为可调用事实，
除非已经变成 `AutoSamplingTheory/TechnicalLemmas/` 下面能通过 Lake build 的
ASTIS-owned declaration。

{technical_port_text}

## 下一轮最小 leaf

- Boundary: {blocker_info["current_leaf"]}
- 原文行号: {blocker_info["source_ref"]}
- Lean boundary: {blocker_info["lean_boundary"]}
- 下一步: {blocker_info["next_action"]}

## 当前未复现的关键边界

```text
{state["latest_blocker"]}
```

下一轮应优先处理 latest blocker 里点名的最小 leaf，而不是回到旧的
total-event/source-functional consumer wrapper。若最新 blocker 是
Brownian/Ito/Taylor 方向，则优先处理：

- selected-test scalar Taylor pointwise limit；
- Taylor moment decomposition；
- quadratic-variation normalization；
- per-coordinate Hessian generator identity；
- 必要的 Gaussian moment、dominated-convergence、measurability/integrability leaf。

若 reviewer 指回 trace/Laplacian 命名方向，则再处理：

- `hemGeneratorLaplacianStateIntegral`；
- `hsourceLaplacianFieldMeas`；
- `hemGeneratorLaplacianEventFieldEqTraceField`；
- `htraceFieldEqLaplacian`。

## 为什么还没有完成

论文里可以把 `appendix.tex:1379-1387` 写成一个 Fokker--Planck 方程，把
`appendix.tex:1402-1427` 写成一次 divergence rewrite 和 integration by
parts。Lean 里这些不是一句话：它需要知道具体是哪一个 law、哪个版本的
conditional expectation、哪个 measurable representative、哪个 Laplacian
定义、哪个边界 trace 为零、哪个积分换元定理可用。

因此，本轮是在把“大而模糊的标准分析步骤”切成小接口：law integral、
state integral、source functional、trace field、Laplacian field、event
field、standard-basis formula、Brownian/Ito scalar coordinate expansion、
Gaussian dominated convergence。这个方向是对的，但还没有完成所有底层
Taylor/Ito/可测性/积分/边界定理。

## 本轮 packet 统计

{packet_counts}

## Proof status counts

{status_counts}

## 最近 handoff 摘要

{handoff_text}

## 下一轮科学计划

1. upper 必须从 latest blocker 里选一个最小 direct leaf；不要回到已经缩小过的
   total-event/source-functional wrapper。
2. middle 负责把该 leaf 的源文位置、Lean declaration、依赖 DAG、可用 Mathlib
   theorem 和仍需 source-cited 的假设写清楚，再分派 lower agents。
3. lower_1 先做自然语言证明路线，明确哪些步骤是 Taylor/Ito 展开、Gaussian
   moment、dominated convergence、measurability/integrability 或定义展开。
4. lower_2 只实现一个 compiled Lean theorem，或者把该 leaf 严格缩小成更小的
   source-cited obligation。
5. reviewer 必须拒绝只把同一个大前提换名字的 wrapper churn；接受标准是
   `python3 tools/astis.py check` 通过且剩余边界严格变小。
6. 如本地 Mathlib/SLT 参考不够，upper/middle 可以网络检索 Mathlib source、
   Lean API 或标准 SDE/Fokker--Planck/Ito/Taylor/Green identity 文献，但所有结果必须回写成
   本地 compiled declaration 或明确 `ProofObligation`。
"""


def cmd_export_technical_report(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    task = getattr(args, "task", "ASTIS-SALD-001")
    if task == "ASTIS-SALD-001":
        cycle_note = max(latest_cycle_number(task), latest_trial_cycle(task))
        ensure_source_index(task)
        write_sald_unfinished_source_map(cycle_note)
    report_root = Path(getattr(args, "report_root", "") or TECH_REPORT_ROOT)
    sections = report_root / "sections"
    markdown_dir = ROOT / "paper-notes" / "AutoLeanInSleepSampling" / "markdown" / "technical-report-updates"

    source_count = len(load_jsonl(ROOT / "research-wiki" / "source-index" / "SALD_original.jsonl"))
    trial_count = len(load_jsonl(TRIAL_LOG))
    latest_cycle = latest_cycle_number(task)
    export_date = now_stamp()
    window = latest_sald_window_info()
    state = blueprint_control_state(task)
    handoffs = latest_handoff_notes(task, limit=6)
    diagnostics = lean_diagnostics()
    totals = diagnostics.get("totals", {})

    def public_report_text(value: str) -> str:
        return public_article_text(value)

    def latex_escape(value: str) -> str:
        value = public_report_text(value)
        return latex_escape_raw(value)

    def latex_escape_raw(value: str) -> str:
        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }
        return "".join(replacements.get(char, char) for char in value)

    unfinished_items = sald_unfinished_source_items() if task == "ASTIS-SALD-001" else []
    unfinished_latex_rows = "\n".join(
        rf"{latex_escape_raw(row.get('id', ''))} & {latex_escape_raw(row.get('source_ref', 'line-range-missing'))} & {latex_escape(row.get('status', ''))} \\"
        for row in unfinished_items[:10]
    ) or r"none & none & none \\"
    unfinished_markdown_table = unfinished_source_markdown_table(unfinished_items) if unfinished_items else "| none | none | none | none | none | none |"
    registry_rows = technical_lemma_registry_rows()
    formalized_count = sum(1 for row in registry_rows if row.get("status") == "formalized-local")
    port_count = len([row for row in registry_rows if row.get("status") != "formalized-local"]) + len(technical_lemma_port_queue_rows())
    technical_latex_items = "\n".join([
        rf"\item ASTIS-owned compiled technical lemma registry entries: {formalized_count}.",
        rf"\item Technical lemma port queue entries: {port_count}.",
        rf"\item Callable background facts must live under \Lean{{AutoSamplingTheory/TechnicalLemmas}} and pass the Lake gate.",
    ])
    proof_status_items = "\n".join(
        rf"\item \texttt{{{latex_escape(str(key))}}}: {value}"
        for key, value in sorted(state["proof_status_counts"].items())
    )
    packet_items = "\n".join(
        rf"\item \texttt{{{latex_escape(str(key))}}}: {value}"
        for key, value in state["trial_classifications_recent"].items()
    )
    handoff_items = "\n".join(
        rf"\item {latex_escape(note)}" for note in handoffs
    ) or r"\item No recent handoff notes were found."
    active_seconds = window["active_agent_seconds"] or "unknown"

    report_latex = rf"""% Auto-generated by `python3 tools/astis.py export-technical-report`.
% Do not hand-edit this file; edit the generator or surrounding report text.

\subsection{{Latest Automated Report Update}}
\label{{sec:generated-report-update}}

This subsection is generated by the middle-layer report-writing pass after a
completed ASTIS batch.  The Lean repository, conversion windows, proof
obligations, and reviewer gate remain the source of truth; this text is a
human-readable technical-report projection of that state.

\begin{{center}}
\begin{{tabular}}{{lr}}
\toprule
Quantity & Value \\
\midrule
Export time & {latex_escape_raw(export_date)} \\
Task & \texttt{{{latex_escape_raw(task)}}} \\
Latest observed cycle & {latest_cycle} \\
Latest 6h cycle range & {latex_escape_raw(window["cycle_range"])} \\
Active-agent usage & {latex_escape_raw(active_seconds)} \\
Source-indexed SALD declarations & {source_count} \\
Trial-log records & {trial_count} \\
Lean theorem declarations & {latex_escape_raw(str(totals.get("theorem", "unknown")))} \\
Lean definition declarations & {latex_escape_raw(str(totals.get("def", "unknown")))} \\
Forbidden proof-pattern hits & {latex_escape_raw(str(totals.get("forbidden_hits", "unknown")))} \\
\bottomrule
\end{{tabular}}
\end{{center}}

\paragraph{{Plain-language status.}}
The current state should not be read as ``the VA-SALD idea is still missing.''
The main SALD proof route, source anchors, theorem contracts, and many local
Gaussian/Taylor/algebraic substeps are already represented in the repository.
The remaining bottleneck is the background analysis that a paper can cite in
ordinary prose but Lean must instantiate exactly: the particular law being
integrated, the conditional-expectation representative, measurability and
integrability conditions, domination for limit/interchange arguments,
boundary terms for integration by parts, and the exact KL/FI/LSI or
Fokker--Planck statement compatible with the paper notation.

\paragraph{{What is SALD-specific and what is background.}}
\begin{{center}}
\begin{{tabular}}{{p{{0.22\linewidth}}p{{0.34\linewidth}}p{{0.32\linewidth}}}}
\toprule
Layer & Meaning & Current policy \\
\midrule
SALD contribution & The paper's KL contraction, moving-target, guided-residual,
and Euler--Maruyama proof route & Keep statements and constants faithful to
the source paper. \\
Technical lemma memory & Standard measure/probability/SDE tools such as
KL/FI/LSI, Ito/Taylor expansion, Gaussian moments, conditional laws, and
integration by parts & Use only ASTIS-owned compiled lemmas; otherwise record
a precise port queue or proof obligation. \\
Source-contract gap & A regularity or representative choice that the paper
uses implicitly but has not yet been matched to a Lean hypothesis & Do not
silently add assumptions; locate the source assumption or keep an explicit
obligation. \\
\bottomrule
\end{{tabular}}
\end{{center}}

\paragraph{{How a human should guide the next run.}}
The useful high-level choice is not ``prove all measure theory'' versus
``ignore Lean details.''  The efficient default is local: for the next active
source-line leaf, identify the smallest missing background lemma, then either
port it into ASTIS as a compiled local theorem or record a source-cited
obligation with exact hypotheses.  Broad KL/measure-theory library building is
reserved for moments when the same missing lemma blocks multiple SALD leaves
or will clearly be reused by later SDE/Sampling papers.

\paragraph{{Mathlib-ready leaf gate.}}
ASTIS now treats reusable Sampling/SDE leaves as future Mathlib candidates.
Each lower packet must target one small theorem, name the local Mathlib and
ASTIS APIs to try first, expose hidden regularity contracts, and keep one
stable proof route unless the reviewer identifies a mathematical statement
problem.  Persistent proof failure is treated as evidence for a missing
assumption, false statement, representative mismatch, API mismatch, or
over-large target rather than as a reason to keep editing the same script.
The generated DAG entry points are
\texttt{{research-wiki/lemma-dags/SDE\_Sampling\_skill\_tree.md}} and
\texttt{{research-wiki/lemma-dags/SALD\_weak\_fp\_leaf\_dag.md}}; the
compressed external-advice target map is
\texttt{{research-wiki/lemma-dags/Pro\_assimilated\_leaf\_targets.md}}.

\paragraph{{Current dynamic leaf.}}
\begin{{quote}}\small
{latex_escape(state["dynamic_leaf_candidate"])}
\end{{quote}}

\paragraph{{Current illness area.}}
\begin{{quote}}\small
{latex_escape(state["illness_area_candidate"])}
\end{{quote}}

\paragraph{{Latest reviewer blocker.}}
\begin{{quote}}\small
{latex_escape(state["latest_blocker"])}
\end{{quote}}

\paragraph{{Recent packet classifications.}}
\begin{{itemize}}
{packet_items}
\end{{itemize}}

\paragraph{{Proof-status counts.}}
\begin{{itemize}}
{proof_status_items}
\end{{itemize}}

\paragraph{{Recent handoff notes.}}
\begin{{itemize}}
{handoff_items}
\end{{itemize}}

\paragraph{{Unfinished source-line map.}}
\begin{{center}}
\begin{{tabular}}{{p{{0.28\linewidth}}p{{0.22\linewidth}}p{{0.38\linewidth}}}}
\toprule
Boundary & Source lines & Status \\
\midrule
{unfinished_latex_rows}
\bottomrule
\end{{tabular}}
\end{{center}}

\paragraph{{Technical lemma memory.}}
\begin{{itemize}}
{technical_latex_items}
\end{{itemize}}
"""

    rules_latex = r"""% Auto-generated by `python3 tools/astis.py export-technical-report`.
% This file records the article-writing contract used by 6h ASTIS batches.

\subsection{Batch-End Article-Writing Pass}
\label{sec:generated-article-writing-pass}

ASTIS treats technical-report writing as part of the middle-agent conversion
layer.  During proof search, the middle agent keeps source-to-Lean and
Lean-to-Markdown/LaTeX conversion windows current, but it does not spend lower
proof-search packets on polished article prose.  After the final completed
upper/middle/lower/reviewer cycle of a multi-hour batch, the report-writing
pass updates the human-readable article projection.

The pass has four responsibilities:
\begin{enumerate}[leftmargin=*]
  \item translate accepted Lean declarations and remaining proof obligations
        into ordinary mathematical language;
  \item name the exact source-paper region and active dynamic proof leaf;
  \item record lessons for the next upper and middle agents as rules, not
        chat history;
  \item keep the technical report synchronized with run evidence while
        preserving Lean and the proof-obligation ledger as the authority.
\end{enumerate}

Every generated report update must also contain a non-Lean reader explanation.
In particular, it must separate paper-specific contribution work from
background technical-lemma work, explain why standard measure-theory or
SDE facts cannot be treated as proved until they match a compiled local Lean
statement, and state how a human can give high-level guidance for the next
run without reading Lean code.

The batch-end pass must also say whether the next lower packet satisfies the
Mathlib-ready leaf gate: one small theorem, explicit local APIs, hidden
regularity contracts, intended proof route, and a failure diagnosis policy.

This policy follows the writing-skill discipline of long-horizon autonomous
research systems: a paper is a maintained artifact, and every long run should
leave a clearer explanation of what the system has proved, what it has not
proved, and why the remaining boundary is mathematically meaningful.
"""

    status_md_lines = [
        "# ASTIS Technical Report Update",
        "",
        f"- Export time: {export_date}",
        f"- Task: `{task}`",
        f"- Latest observed cycle: {latest_cycle}",
        f"- Latest 6h cycle range: `{window['cycle_range']}`",
        f"- Latest log: `{window['log']}`",
        f"- Active-agent usage: {active_seconds}",
        f"- Source-indexed SALD declarations: {source_count}",
        f"- Trial-log records: {trial_count}",
        f"- Lean theorem declarations: {totals.get('theorem', 'unknown')}",
        f"- Lean def declarations: {totals.get('def', 'unknown')}",
        f"- Forbidden proof-pattern hits: {totals.get('forbidden_hits', 'unknown')}",
        "",
        "## Plain-Language Status",
        "",
        "The current blocker does not mean the VA-SALD idea is missing.  The paper-specific theorem route and source anchors are represented.  What remains is mostly background analysis that papers cite as standard but Lean must instantiate exactly: which law is used, which conditional-expectation representative is chosen, which functions are measurable/integrable, which domination theorem justifies a limit, and which boundary term vanishes in integration by parts.",
        "",
        "Human high-level guidance can choose one of three policies: keep background facts as precise source-cited obligations to finish the proof DAG faster; invest in a reusable SDE/Sampling technical lemma library; or use the default local policy, which ports only the smallest technical lemma needed by the next SALD source-line leaf.",
        "",
        "## Current Dynamic Leaf",
        "",
        "```text",
        public_report_text(state["dynamic_leaf_candidate"]),
        "```",
        "",
        "## Latest Reviewer Blocker",
        "",
        "```text",
        public_report_text(state["latest_blocker"]),
        "```",
        "",
        "## Unfinished Source-Line Map",
        "",
        "| Boundary id | Type | Source lines | Lean boundary | Status | Next action |",
        "|---|---|---|---|---|---|",
        unfinished_markdown_table,
        "",
        "## Technical Lemma Memory Status",
        "",
        f"- Formalized local registry entries: {formalized_count}",
        f"- Port queue entries: {port_count}",
        "- Port candidates are not callable until they become ASTIS-owned compiled declarations.",
        "",
        "## Mathlib-Ready Leaf Gate",
        "",
        "- Each reusable SDE/Sampling leaf should be small enough for one lower-agent context window.",
        "- The lower packet must include theorem statement, local APIs, hidden regularity contracts, intended proof route, and failure policy.",
        "- Repeated failure is a mathematical signal: check missing assumptions, false statement risk, representative mismatch, API mismatch, or target size.",
        "- Generated DAGs: `research-wiki/lemma-dags/SDE_Sampling_skill_tree.md`, `research-wiki/lemma-dags/SALD_weak_fp_leaf_dag.md`, and `research-wiki/lemma-dags/Pro_assimilated_leaf_targets.md`.",
        "",
        "## Middle-Agent Rule Update",
        "",
        "- Keep source-to-Lean and Lean-to-Markdown/LaTeX conversion synchronized during every cycle.",
        "- Defer polished article edits to the batch-end report-writing pass.",
        "- The generated technical-report snippets are explanatory projections; Lean, conversion windows, and proof obligations remain authoritative.",
        "- Each report update must tell a human why the current proof boundary is smaller or why the cycle was rejected as wrapper churn.",
        "",
        "## Recent Handoffs",
        "",
        *(f"- {public_report_text(note)}" for note in handoffs),
        "",
    ]

    write_text(sections / "generated_run_status.tex", report_latex)
    write_text(sections / "generated_middle_rules.tex", rules_latex)
    cycle_name = f"{slugify(task)}-cycle{window['cycle_range']}-report-update.md"
    write_text(markdown_dir / cycle_name, "\n".join(status_md_lines))
    write_text(markdown_dir / f"{slugify(task)}-latest-report-update.md", "\n".join(status_md_lines))

    add_manifest("astis.py export-technical-report", sections / "generated_run_status.tex", "paper", "Updated ASTIS technical-report run-status section")
    add_manifest("astis.py export-technical-report", sections / "generated_middle_rules.tex", "paper", "Updated ASTIS technical-report middle-agent writing rules")
    print(f"updated technical report snippets under {rel(report_root)}")
    return 0


def analyze_efficiency_log(path: Path) -> dict:
    text = read_text(path)
    lines = text.splitlines()
    token_events = []
    current_role = "unknown"
    current_cycle = 0
    prompt_re = re.compile(r"runs/[^ ]*?cycle(\d+)/([0-9]+_[A-Za-z0-9_]+\.md)")
    cycle_re = re.compile(r"^cycle\s+(\d+):\s+runs/")
    index = 0
    while index < len(lines):
        line = lines[index]
        prompt_match = prompt_re.search(line) if "tools/astis_codex_faithful.sh" in line else None
        if prompt_match is not None:
            current_cycle = int(prompt_match.group(1))
            current_role = prompt_role(Path(prompt_match.group(2)))
        cycle_match = cycle_re.search(line)
        if cycle_match:
            current_cycle = int(cycle_match.group(1))
        if line.strip() == "tokens used" and index + 1 < len(lines):
            raw = lines[index + 1].strip().replace(",", "")
            if raw.isdigit():
                token_events.append({
                    "cycle": current_cycle,
                    "role": current_role,
                    "tokens": int(raw),
                })
                index += 1
        index += 1

    expected_roles = ("upper", "middle", "lower", "reviewer")
    first_cycle = None
    first_cycle_match = re.search(r"^Cycle:\s*(\d+)\s*$", text, flags=re.M)
    if first_cycle_match:
        first_cycle = int(first_cycle_match.group(1))
    cycles = sorted({int(match.group(1)) for match in cycle_re.finditer(text)})
    if first_cycle is not None and len(token_events) % len(expected_roles) == 0:
        cycles = list(range(first_cycle, first_cycle + len(token_events) // len(expected_roles)))
    if cycles and len(token_events) == len(cycles) * len(expected_roles):
        for event_index, event in enumerate(token_events):
            event["cycle"] = cycles[event_index // len(expected_roles)]
            event["role"] = expected_roles[event_index % len(expected_roles)]

    total_tokens = sum(event["tokens"] for event in token_events)
    max_tokens = max((event["tokens"] for event in token_events), default=0)
    mean_tokens = int(total_tokens / len(token_events)) if token_events else 0
    by_role: dict[str, dict[str, int]] = {}
    for event in token_events:
        role = event["role"]
        row = by_role.setdefault(role, {"count": 0, "total": 0, "max": 0})
        row["count"] += 1
        row["total"] += event["tokens"]
        row["max"] = max(row["max"], event["tokens"])
    for row in by_role.values():
        row["mean"] = int(row["total"] / row["count"]) if row["count"] else 0

    classification_mentions = classification_counts_in_text(text)
    trial_classifications = classification_counts_in_trials("ASTIS-SALD-001", cycles)
    useful_packets = (
        trial_classifications["discharges-supplied-hypothesis"]
        + trial_classifications["narrows-source-cited-boundary"]
    )
    wrapper_churn = trial_classifications["rejected-wrapper-churn"]
    warnings = []
    if mean_tokens > 100_000:
        warnings.append("mean role token use exceeds 100k; use compact context packs and shorter trial memory")
    if max_tokens > 200_000:
        warnings.append("at least one role exceeded 200k tokens; likely broad context replay")
    if useful_packets == 0:
        warnings.append("no discharges/narrows packet classification found; progress signal is missing")
    if wrapper_churn > useful_packets:
        warnings.append("wrapper-churn classifications exceed useful packet classifications")
    if len(text) > 50_000_000:
        warnings.append("log exceeds 50MB; prompts or command output are too verbose for efficient iteration")

    return {
        "log": rel(path) if path.is_relative_to(ROOT) else str(path),
        "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
        "cycles": cycles,
        "token_event_count": len(token_events),
        "total_tokens": total_tokens,
        "mean_tokens": mean_tokens,
        "max_tokens": max_tokens,
        "by_role": by_role,
        "classification_mentions_in_log": classification_mentions,
        "trial_classifications": trial_classifications,
        "warnings": warnings,
        "latest_blocker": latest_reviewer_blocker("ASTIS-SALD-001"),
    }


def efficiency_report_text(report: dict) -> str:
    role_lines = []
    for role, row in sorted(report["by_role"].items()):
        role_lines.append(
            f"- `{role}`: count={row['count']}, mean={row['mean']:,}, max={row['max']:,}, total={row['total']:,}"
        )
    warning_lines = [f"- {item}" for item in report["warnings"]] or ["- none"]
    class_lines = [f"- `{key}`: {value}" for key, value in report["trial_classifications"].items()]
    mention_lines = [f"- `{key}`: {value}" for key, value in report["classification_mentions_in_log"].items()]
    cycles = report["cycles"]
    cycle_text = f"{cycles[0]}--{cycles[-1]} ({len(cycles)} cycles)" if cycles else "none detected"
    return "\n".join([
        "# ASTIS Efficiency Report",
        "",
        f"- Log: `{report['log']}`",
        f"- Size: {report['size_mb']} MB",
        f"- Cycles: {cycle_text}",
        f"- Token events: {report['token_event_count']}",
        f"- Total tokens: {report['total_tokens']:,}",
        f"- Mean tokens per role call: {report['mean_tokens']:,}",
        f"- Max tokens in one role call: {report['max_tokens']:,}",
        "",
        "## By Role",
        "",
        "\n".join(role_lines) if role_lines else "- no role token events detected",
        "",
        "## Trial Packet Classifications",
        "",
        "\n".join(class_lines),
        "",
        "## Log Classification Mentions",
        "",
        "\n".join(mention_lines),
        "",
        "## Warnings",
        "",
        "\n".join(warning_lines),
        "",
        "## Current Blocker",
        "",
        report["latest_blocker"],
        "",
        "## Required Next-Run Controls",
        "",
        "- Use `05_context_pack.md` instead of full historical task replay.",
        "- Keep recent trial memory short and high-signal.",
        "- Reviewer should reject cycles that do not classify the packet or do not name the exact discharged/narrowed hypothesis.",
        "- Inspect `python3 tools/astis.py blueprint-refresh ASTIS-SALD-001` before choosing the next dynamic leaf or illness area.",
        "- Upper and middle should consult ASTIS `TechnicalLemmas` before inventing new measure/probability interfaces; external SLT files are port references only.",
    ]) + "\n"


def cmd_efficiency_report(args: argparse.Namespace) -> int:
    path = Path(args.log) if args.log else latest_log_file()
    if path is None:
        raise SystemExit("no ASTIS SALD 6h log found")
    if not path.is_absolute():
        path = ROOT / path
    report = analyze_efficiency_log(path)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    text = efficiency_report_text(report)
    output = Path(args.output) if args.output else EFFICIENCY_DIR / f"{path.stem}.md"
    if not output.is_absolute():
        output = ROOT / output
    write_text(output, text)
    add_manifest("astis.py efficiency-report", output, "review", f"Wrote efficiency report for {rel(path)}")
    if not args.json:
        print(text)
    return 0


def cmd_write_context_pack(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else None
    if output is not None and not output.is_absolute():
        output = ROOT / output
    path = write_context_pack(args.task, args.cycle, output)
    print(f"context pack: {rel(path)}")
    return 0


def cmd_update_sald_todo(args: argparse.Namespace) -> int:
    cycle = args.cycle if args.cycle > 0 else None
    path = write_sald_reproduction_todo(cycle)
    print(f"SALD TODO: {rel(path)}")
    return 0


def cmd_update_sald_paper_memory(args: argparse.Namespace) -> int:
    cycle = args.cycle if args.cycle > 0 else None
    path = write_sald_unfinished_source_map(cycle)
    print(f"SALD paper memory: {rel(path)}")
    return 0


def markdown_table(rows: list[dict], columns: list[tuple[str, str]], limit: int | None = None) -> str:
    selected = rows[:limit] if limit is not None else rows
    if not selected:
        return "_None._"
    header = "| " + " | ".join(title for title, _ in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in selected:
        cells = []
        for _, key in columns:
            value = row.get(key, "")
            if isinstance(value, list):
                value = "; ".join(str(item) for item in value)
            cells.append(str(value).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *body])


def latex_escape_text(value: object) -> str:
    text = public_article_text(str(value))
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "`": r"\textasciigrave{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def mirror_existing_technical_lemma_memory() -> None:
    for name in ["technical_lemma_registry.jsonl", "SLT_port_queue.jsonl"]:
        source = LEGACY_TECHNICAL_LEMMA_MEMORY_DIR / name
        destination = TECHNICAL_LEMMAS_DIR / name
        if source.exists() and (not destination.exists() or source.read_text(encoding="utf-8") != destination.read_text(encoding="utf-8")):
            write_text(destination, source.read_text(encoding="utf-8"))


def sald_contribution_rows() -> list[dict]:
    rows = []
    for row in sald_unfinished_source_items():
        is_paper = row.get("kind") == "paper-contribution"
        rows.append({
            "id": row.get("id", ""),
            "source_ref": row.get("source_ref", "line-range-missing"),
            "paper_object": row.get("human_meaning", ""),
            "lean_boundary": row.get("lean_boundary", ""),
            "lean_status": row.get("status", ""),
            "next_action": row.get("next_action", ""),
            "is_sald_contribution": is_paper,
            "depends_on_external_technical_lemma": not is_paper,
            "open": "open" in row.get("status", "") or row.get("status", "") != "formalized",
        })
    return rows


def technical_lemma_rows() -> list[dict]:
    rows: list[dict] = []
    for row in technical_lemma_registry_rows():
        rows.append({
            "id": row.get("id", row.get("local_decl", "")),
            "source": row.get("source", row.get("upstream_file", "ASTIS local")),
            "statement": row.get("statement", row.get("sald_use", "")),
            "lean_decl": row.get("local_decl", ""),
            "lean_status": row.get("status", ""),
            "used_by": row.get("sald_use", ""),
            "dependencies": row.get("dependencies", []),
            "next_action": row.get("next_action", "Use as callable only when status is formalized-local."),
            "tags": row.get("tags", []),
        })
    for row in technical_lemma_port_queue_rows():
        rows.append({
            "id": row.get("id", row.get("upstream_file", "")),
            "source": row.get("upstream_file", ""),
            "statement": format_decl_list(row.get("upstream_declarations", row.get("upstream_decl", ""))),
            "lean_decl": row.get("target_local_module", row.get("astis_target", "")),
            "lean_status": row.get("status", "port-candidate"),
            "used_by": row.get("astis_target", row.get("sald_use", "")),
            "dependencies": row.get("dependencies", []),
            "next_action": row.get("next_action", "Port to ASTIS-owned TechnicalLemmas before using."),
            "tags": row.get("tags", []),
        })
    return rows


def recent_verifier_feedback(task_id: str, limit: int = 8) -> list[dict]:
    rows = []
    for record in reversed(trial_records_for_task(task_id)):
        feedback = record.get("verifier_feedback")
        if not isinstance(feedback, dict) or not feedback:
            continue
        rows.append({
            "timestamp": record.get("timestamp", ""),
            "trial_id": record.get("trial_id", ""),
            "role": record.get("role", ""),
            "status": record.get("status", ""),
            "leaf": feedback.get("leaf", ""),
            "error_class": feedback.get("error_class", ""),
            "source_correspondence_ok": feedback.get("source_correspondence_ok", ""),
            "lean_build_ok": feedback.get("lean_build_ok", ""),
            "mathlib_api_ok": feedback.get("mathlib_api_ok", ""),
            "measure_theory_ok": feedback.get("measure_theory_ok", ""),
            "regularity_assumption_ok": feedback.get("regularity_assumption_ok", ""),
            "technical_lemma_ok": feedback.get("technical_lemma_ok", ""),
            "closed_theorem_ok": feedback.get("closed_theorem_ok", ""),
            "next_route": feedback.get("next_route", ""),
        })
        if len(rows) >= limit:
            break
    if rows:
        return rows
    feedback_files = [
        path for path in VERIFIER_FEEDBACK_DIR.glob("*.md")
        if path.name.lower() != "readme.md"
    ]
    for path in sorted(feedback_files, key=lambda p: p.stat().st_mtime, reverse=True)[:limit]:
        rows.append({
            "timestamp": _dt.datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "trial_id": rel(path),
            "role": "reviewer",
            "status": "packet",
            "leaf": path.stem,
            "error_class": "manual-packet",
            "source_correspondence_ok": "",
            "lean_build_ok": "",
            "mathlib_api_ok": "",
            "measure_theory_ok": "",
            "regularity_assumption_ok": "",
            "technical_lemma_ok": "",
            "closed_theorem_ok": "",
            "next_route": compact_file_lines(path, [r"next_route", r"Next route", r"next"], limit=2),
        })
    return rows


def recent_trial_rows(task_id: str, limit: int = 8) -> list[dict]:
    rows = []
    for record in reversed(trial_records_for_task(task_id)[-limit:]):
        rows.append({
            "timestamp": record.get("timestamp", ""),
            "trial_id": record.get("trial_id", ""),
            "role": record.get("role", ""),
            "kind": record.get("kind", ""),
            "status": record.get("status", ""),
            "lean_gate": record.get("lean_gate", ""),
            "artifact": record.get("artifact", ""),
            "notes": record.get("notes", ""),
            "next_route": (
                record.get("verifier_feedback", {}).get("next_route", "")
                if isinstance(record.get("verifier_feedback", {}), dict)
                else ""
            ),
        })
    return rows


def memory_snapshot_state(task_id: str, cycle: int, run_dir: Path) -> dict:
    title, _ = task_context(task_id)
    state = blueprint_control_state(task_id)
    if task_id == "ASTIS-SALD-001":
        sald_rows = sald_contribution_rows()
        tech_rows = technical_lemma_rows()
        open_sald = [row for row in sald_rows if row.get("is_sald_contribution") and row.get("open")]
        open_tech = [row for row in tech_rows if row.get("lean_status") not in {"formalized-local", "formalized"}]
    else:
        sald_rows = []
        tech_rows = technical_lemma_rows()
        open_sald = []
        open_tech = [row for row in tech_rows if row.get("lean_status") not in {"formalized-local", "formalized"}]
    feedback_rows = recent_verifier_feedback(task_id, limit=10)
    trial_rows = recent_trial_rows(task_id, limit=10)
    latest_route = next(
        (str(row.get("next_route", "")).strip() for row in feedback_rows
         if str(row.get("next_route", "")).strip()),
        "",
    )
    if not latest_route:
        latest_route = next(
            (str(row.get("notes", "")).strip() for row in trial_rows
             if str(row.get("notes", "")).strip()),
            "",
        )
    if task_id == "ASTIS-CHEWI-001":
        route = latest_route or (
            "Assemble the compiled finite-box, cutoff-limit, integrability, and Gibbs-tail "
            "leaves into the smallest whole-space weighted-IBP declaration; keep domains, "
            "invariance, and second-order cutoff branches separate."
        )
        next_lower_tasks = [
            {
                "role": "lower-1-textbook-proof-scout",
                "goal": f"Audit the natural-language proof and exact assumptions for this active route: {route}",
                "must_write": "proof-attempts/<task>/...-textbook-dag.md or a dialogue handoff.",
            },
            {
                "role": "lower-2-lean-implementation-worker",
                "goal": f"Compile the smallest Mathlib-ready leaf on this route, or return one typed blocker: {route}",
                "must_write": "Lean declaration plus typed verifier feedback fields.",
            },
        ]
    else:
        next_lower_tasks = [
            {
                "role": "lower-1-natural-language-proof-scout",
                "goal": "Translate the active SALD source-line leaf into a dependency DAG with exact technical lemma needs.",
                "must_write": "proof-attempts/<task>/...-natural-language-dag.md or a dialogue handoff.",
            },
            {
                "role": "lower-2-lean-implementation-worker",
                "goal": "Close one compiled Lean theorem or strictly narrow one source-cited Sampling/SDE boundary.",
                "must_write": "Lean declaration plus typed verifier feedback fields.",
            },
        ]
    dynamic_leaf_queue = [
        str(state.get("dynamic_leaf_candidate", "")).strip(),
        str(state.get("illness_area_candidate", "")).strip(),
    ]
    blocker = str(state.get("latest_blocker", "")).strip()
    generic_signal = "No reviewer blocker recorded yet; use source index and proof-obligation ledger."
    dynamic_leaf_queue = [item for item in dynamic_leaf_queue if item and item != generic_signal]
    open_obligation_signals = [blocker] if blocker and blocker != generic_signal else []
    if task_id == "ASTIS-CHEWI-001" and latest_route:
        dynamic_leaf_queue = [latest_route, *dynamic_leaf_queue]
        open_obligation_signals = [latest_route, *open_obligation_signals]
    dynamic_leaf_queue = list(dict.fromkeys(dynamic_leaf_queue))
    open_obligation_signals = list(dict.fromkeys(open_obligation_signals))
    return {
        "task_id": task_id,
        "title": title,
        "cycle": cycle,
        "generated": now_stamp(),
        "run_dir": rel(run_dir),
        "mode": "faithfulPaper" if task_id in {"ASTIS-SALD-001", "ASTIS-CHEWI-001"} else "exploratoryProof",
        "stage": state.get("stage", ""),
        "dynamic_leaf_queue": dynamic_leaf_queue,
        "open_obligation_signals": open_obligation_signals,
        "latest_next_route": latest_route,
        "sald_contributions": sald_rows,
        "open_sald_contribution_obligations": open_sald,
        "technical_lemmas": tech_rows,
        "open_external_technical_lemma_obligations": open_tech,
        "recent_verifier_feedback": feedback_rows,
        "recent_trials": trial_rows,
        "proof_status_counts": state.get("proof_status_counts", {}),
        "next_lower_tasks": next_lower_tasks,
    }


def sald_plain_language_status_zh() -> str:
    return (
        "当前不是 VA-SALD 的核心想法没写出来，而是论文里的若干“标准分析事实”"
        "还没有在当前 Lean 符号下实例化。论文可以说 by Fokker--Planck、by KL/FI/LSI、"
        "by Ito/Taylor 或 by integration by parts；Lean 需要具体测度、条件分布代表元、"
        "可测/可积、dominated convergence、边界项为零和 Mathlib/local lemma 的精确 statement。"
    )


def sald_plain_language_status_en() -> str:
    return (
        "The current SALD state is not missing the VA-SALD idea.  The remaining "
        "work is mainly background analysis that papers cite as standard but "
        "Lean must instantiate for the exact law, conditional representative, "
        "measurability/integrability assumptions, domination argument, boundary "
        "condition, and KL/FI/LSI or Fokker--Planck statement in use."
    )


def log_concave_plain_language_status_en() -> str:
    return (
        "The active textbook edge is Chapter 1, Example 1.2.8 to Corollary "
        "1.2.9.  Generator algebra, finite-box cancellation, smooth plateau "
        "cutoffs, the radial compact-support pointwise-exhaustion base, a "
        "scale-uniform O(R^-1) first-derivative bound, closed outer-region "
        "derivative vanishing, finite-Pi cutoff derivative/trace bridges, and the "
        "generic L1 cutoff-gradient and expanding-ball tail limits, the concrete Gibbs-weighted source-field "
        "integrability leaf, generic cutoff main-term dominated convergence, compact-test generator-display integrability, and Gibbs-tail convergence are compiled locally.  "
        "Whole-space weighted integration by parts, generator/semigroup "
        "domains, and the invariant Gibbs law remain explicit red nodes."
    )


def task_plain_language_status_en(task_id: str) -> str:
    if task_id == "ASTIS-SALD-001":
        return sald_plain_language_status_en()
    if task_id == "ASTIS-CHEWI-001":
        return log_concave_plain_language_status_en()
    return (
        "This task is tracked as an exploratory proof program.  Keep theorem "
        "boundaries explicit, use compiled local declarations as the only blue "
        "facts, and record every missing cited result as a red obligation."
    )


def memory_digest_markdown(snapshot: dict) -> str:
    dynamic_text = "\n".join(f"- {item}" for item in snapshot.get("dynamic_leaf_queue", []) if item) or "- no dynamic leaf"
    obligation_text = "\n".join(f"- {item}" for item in snapshot.get("open_obligation_signals", []) if item) or "- no compact obligation"
    task_id = str(snapshot.get("task_id", ""))
    return f"""# Memory Digest: {snapshot.get('task_id')} cycle {snapshot.get('cycle')}

Generated: `{snapshot.get('generated')}`

Run directory: `{snapshot.get('run_dir')}`

This is the ABEIS-style compact retrieval packet for ASTIS.  Upper and middle
should read this before replaying long logs.

## Plain-Language Status

{task_plain_language_status_en(task_id)}

## Active Proof-DAG Leaves

{dynamic_text}

## Open Obligation Signals

{obligation_text}

## Mathlib-Ready Leaf Discipline

- Decompose aggressively: one lower packet should target one small lemma.
- Specify the theorem together with local APIs, imports, hidden regularity
  contracts, and an intended proof route.
- Search Mathlib and `AutoSamplingTheory/TechnicalLemmas` before inventing a
  local bridge.
- Treat repeated failure as a mathematical signal: missing assumption, false
  statement, representative mismatch, API mismatch, or over-large target.
- Do not churn the theorem shape or proof route without reviewer diagnosis.
- Protocol: `docs/mathlib_ready_leaf_protocol.md`.
- Skill tree: `research-wiki/lemma-dags/SDE_Sampling_skill_tree.md`.
- Compressed Pro leaf targets:
  `research-wiki/lemma-dags/Pro_assimilated_leaf_targets.md`.

## Open Paper Contribution Obligations

{markdown_table(snapshot.get('open_sald_contribution_obligations', []), [
    ('id', 'id'),
    ('source', 'source_ref'),
    ('paper object', 'paper_object'),
    ('Lean/status', 'lean_status'),
    ('next action', 'next_action'),
], limit=10)}

## Open External Technical Lemma Obligations

{markdown_table(snapshot.get('open_external_technical_lemma_obligations', []), [
    ('id', 'id'),
    ('source', 'source'),
    ('status', 'lean_status'),
    ('used by', 'used_by'),
    ('next action', 'next_action'),
], limit=10)}

## Recent Typed Verifier Feedback

{markdown_table(snapshot.get('recent_verifier_feedback', []), [
    ('leaf', 'leaf'),
    ('class', 'error_class'),
    ('build', 'lean_build_ok'),
    ('measure', 'measure_theory_ok'),
    ('technical lemma', 'technical_lemma_ok'),
    ('next', 'next_route'),
], limit=8)}

## Next Lower-Agent Split

{markdown_table(snapshot.get('next_lower_tasks', []), [
    ('role', 'role'),
    ('goal', 'goal'),
    ('artifact', 'must_write'),
])}
"""


def todo_markdown(snapshot: dict) -> str:
    task_id = str(snapshot.get("task_id", ""))
    if task_id == "ASTIS-CHEWI-001":
        active_route = str(snapshot.get("latest_next_route", "")).strip()
        human_default = (
            "Use the reviewer-recorded active route: " + active_route
            if active_route else
            "Instantiate the compiled integrated semigroup-generator contract for the actual "
            "Langevin evolution and keep the C_c^2-to-stable-domain gap explicit."
        )
        lower_1 = (
            "Write the exact analytic route for a concrete Langevin semigroup pairing derivative "
            "or martingale-problem uniqueness theorem, including every regularity assumption."
        )
        lower_2 = (
            "Implement only the smallest concrete semigroup/domain instantiation leaf, or return "
            "one typed blocker. Do not assert invariant Gibbs law from C_c^2 core data alone."
        )
    elif task_id == "ASTIS-SALD-001":
        human_default = (
            "Use the local strategy: port or prove only the smallest technical "
            "lemma needed by the next SALD source-line leaf.  Do not build a "
            "broad measure-theory library unless the same missing fact blocks "
            "multiple leaves."
        )
        lower_1 = (
            "Write the natural-language proof route for the first active SALD "
            "contribution leaf.  Name exact source lines and the minimal "
            "technical lemma needed."
        )
    else:
        human_default = (
            "Choose one narrow theorem boundary, prove one compiled local "
            "declaration when possible, and otherwise record a precise red "
            "source-cited obligation."
        )
        lower_1 = (
            "Write the natural-language proof route for the active theorem "
            "leaf, naming exact dependencies and missing assumptions."
        )
        lower_2 = (
            "Implement one compiled Lean declaration or reduce the source-cited "
            "boundary.  Log typed verifier feedback with `--feedback-field`."
        )
    if task_id == "ASTIS-SALD-001":
        lower_2 = (
            "Implement one compiled Lean declaration or reduce the source-cited "
            "boundary.  Log typed verifier feedback with `--feedback-field`."
        )
    return f"""# Next Todo Packet: {snapshot.get('task_id')} cycle {snapshot.get('cycle')}

Generated: `{snapshot.get('generated')}`

## Human Default

{human_default}

## Mathlib-Ready Leaf Gate

Before assigning lower work, middle must fill the leaf packet shape from
`research-wiki/technical-lemmas/mathlib_ready_leaf_template.md`: theorem,
local APIs, hidden regularity, proof route, and failure policy.  If a proof has
already failed repeatedly, the next action is statement diagnosis, not another
proof-script rewrite.

## Lower 1

{lower_1}

## Lower 2

{lower_2}

## Open Paper Contribution Obligations

{markdown_table(snapshot.get('open_sald_contribution_obligations', []), [
    ('id', 'id'),
    ('source', 'source_ref'),
    ('Lean/status', 'lean_status'),
    ('next action', 'next_action'),
], limit=8)}

## Open External Technical Lemma Obligations

{markdown_table(snapshot.get('open_external_technical_lemma_obligations', []), [
    ('id', 'id'),
    ('status', 'lean_status'),
    ('next action', 'next_action'),
], limit=8)}
"""


def sald_contribution_index_markdown(rows: list[dict]) -> str:
    return "# SALD Paper Contribution Index\n\nGenerated by `python3 tools/astis.py memory-refresh`.\n\n" + markdown_table(
        rows,
        [
            ("id", "id"),
            ("source", "source_ref"),
            ("paper object", "paper_object"),
            ("Lean boundary", "lean_boundary"),
            ("status", "lean_status"),
            ("SALD contribution?", "is_sald_contribution"),
            ("external technical lemma?", "depends_on_external_technical_lemma"),
        ],
    ) + "\n"


def technical_lemma_index_markdown(rows: list[dict]) -> str:
    return "# Technical Lemma Index\n\nGenerated by `python3 tools/astis.py memory-refresh`.\n\n" + markdown_table(
        rows,
        [
            ("id", "id"),
            ("source", "source"),
            ("statement", "statement"),
            ("Lean declaration", "lean_decl"),
            ("status", "lean_status"),
            ("used by", "used_by"),
            ("next action", "next_action"),
            ("tags", "tags"),
        ],
    ) + "\n"


def write_memory_refresh(task_id: str, cycle: int, run_dir: Path) -> tuple[Path, Path, Path]:
    mirror_existing_technical_lemma_memory()
    write_mathlib_ready_leaf_docs()
    write_arsenal_module_graph_docs()
    snapshot = memory_snapshot_state(task_id, cycle, run_dir)
    digest_path = run_dir / "memory_digest.md"
    todo_path = run_dir / "todo.md"
    index_path = RETRIEVAL_INDEX_DIR / f"{slugify(task_id)}.json"
    write_text(digest_path, memory_digest_markdown(snapshot))
    write_text(todo_path, todo_markdown(snapshot))
    write_text(index_path, json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    sald_rows = snapshot.get("sald_contributions", [])
    technical_rows = snapshot.get("technical_lemmas", [])
    if isinstance(sald_rows, list) and task_id == "ASTIS-SALD-001":
        index_text = sald_contribution_index_markdown(sald_rows)
        todo_text = "# SALD Open Contribution Todo\n\n" + markdown_table(
            snapshot.get("open_sald_contribution_obligations", []),
            [
                ("id", "id"),
                ("source", "source_ref"),
                ("status", "lean_status"),
                ("next action", "next_action"),
            ],
        ) + "\n"
        write_text_mirror(SALD_CONTRIBUTION_DIR / "index.md", index_text, [LEGACY_SALD_PAPER_MEMORY_DIR / "index.md"])
        write_text_mirror(SALD_CONTRIBUTION_DIR / "source-map.md", index_text, [LEGACY_SALD_PAPER_MEMORY_DIR / "source-map.md"])
        write_text_mirror(SALD_CONTRIBUTION_DIR / "todo.md", todo_text, [LEGACY_SALD_PAPER_MEMORY_DIR / "todo.md"])
    if isinstance(technical_rows, list):
        tech_index = technical_lemma_index_markdown(technical_rows)
        tech_todo = "# Open External Technical Lemma Todo\n\n" + markdown_table(
            snapshot.get("open_external_technical_lemma_obligations", []),
            [
                ("id", "id"),
                ("source", "source"),
                ("status", "lean_status"),
                ("next action", "next_action"),
            ],
        ) + "\n"
        write_text_mirror(TECHNICAL_LEMMAS_DIR / "index.md", tech_index, [LEGACY_TECHNICAL_LEMMA_MEMORY_DIR / "index.md"])
        write_text_mirror(TECHNICAL_LEMMAS_DIR / "todo.md", tech_todo, [LEGACY_TECHNICAL_LEMMA_MEMORY_DIR / "todo.md"])
    add_manifest("astis.py memory-refresh", digest_path, "memory", f"Wrote memory digest for {task_id} cycle {cycle}")
    add_manifest("astis.py memory-refresh", index_path, "memory", f"Wrote retrieval index for {task_id}")
    return digest_path, todo_path, index_path


def public_source_block_for_pro(task_id: str) -> str:
    if task_id == "ASTIS-SALD-001":
        return """- SALD/VA-SALD target paper, "Learning Distributional Diffusion Models with Training-Free Guided Generation": https://arxiv.org/abs/2605.07950
- PDF: https://arxiv.org/pdf/2605.07950
"""
    if task_id == "ASTIS-CHEWI-001":
        return """- Primary textbook target, "Log-Concave Sampling": https://chewisinho.github.io/main.pdf
- ASTIS task mode: faithful reconstruction of the textbook route and the cited rigorous background results needed by that route.
"""
    if task_id == "ASTIS-RMFLD-001":
        return """- RMFLD is currently tracked as an exploratory local proof program.  ChatGPT Pro cannot access the local manuscript, so only use the theorem statements and status pasted below unless the user separately provides a public arXiv link.
"""
    return """- No public source URL was recorded for this task.  Use only the theorem statements and status pasted below unless the user supplies a public arXiv or paper link.
"""


def chatgpt_pro_prompt_markdown(task_id: str, cycle: int, run_dir: Path) -> str:
    snapshot = memory_snapshot_state(task_id, cycle, run_dir)
    title, task_text = task_context(task_id)
    dynamic = [item for item in snapshot.get("dynamic_leaf_queue", []) if item]
    obligations = [item for item in snapshot.get("open_obligation_signals", []) if item]
    return f"""# ChatGPT Pro Prompt: ASTIS {task_id} cycle {cycle}

Copy everything below this line into ChatGPT Pro.

---

You are helping with ASTIS, an Auto-Sampling-Theory-in-Sleep Lean 4 project for
faithful paper reproduction and sampling/SDE proof exploration.  You cannot
access my local files.  Use only public links and the self-contained status in
this prompt.  Local Lean names and local paths are labels for me to patch later.

## Public sources you may use

{public_source_block_for_pro(task_id)}
## Current ASTIS task

Task: `{task_id}`

Title: {title}

Cycle: `{cycle}`

Run label: `{run_dir.name}`

Task contract excerpt:

```text
{compact_inline_text(task_text, 1800)}
```

If this is faithful-paper mode, do not change the theorem statement,
assumptions, constants, or proof target.  If a paper proof says "standard" or
"by Fokker--Planck/KL/FI/LSI/Ito/Taylor/integration by parts", classify that as
an external technical lemma or classical fact unless it is fully proved in the
target paper.

## Current status

Plain-language status: {sald_plain_language_status_en()}

### Active proof-DAG leaves

{chr(10).join(f"- {item}" for item in dynamic) or "- No active proof-DAG leaf was recorded."}

### Open obligation signals

{chr(10).join(f"- {item}" for item in obligations) or "- No compact obligation signal was recorded."}

### Open paper-contribution obligations

{markdown_table(snapshot.get('open_sald_contribution_obligations', []), [
    ('id', 'id'),
    ('source', 'source_ref'),
    ('paper object', 'paper_object'),
    ('Lean/status', 'lean_status'),
    ('next action', 'next_action'),
], limit=12)}

### Open external technical-lemma obligations

{markdown_table(snapshot.get('open_external_technical_lemma_obligations', []), [
    ('id', 'id'),
    ('source', 'source'),
    ('statement', 'statement'),
    ('status', 'lean_status'),
    ('used by', 'used_by'),
    ('next action', 'next_action'),
], limit=12)}

### Recent typed verifier feedback

{markdown_table(snapshot.get('recent_verifier_feedback', []), [
    ('leaf', 'leaf'),
    ('error class', 'error_class'),
    ('Lean build', 'lean_build_ok'),
    ('measure theory', 'measure_theory_ok'),
    ('technical lemma', 'technical_lemma_ok'),
    ('next route', 'next_route'),
], limit=10)}

## What I need from you

Please return a proof-engineering answer that can guide the next ASTIS 6h run.

1. Identify which remaining items are target-paper contributions and which are
   external technical lemmas/classical facts.
2. For the smallest next leaf, write a source-faithful natural-language proof
   route and a dependency DAG.
3. Propose Lean-facing lemma statements in pseudo-Lean if necessary.  Be
   precise about measures, kernels, laws, densities, conditioning, integrability,
   differentiability, domination, and boundary conditions.
4. Identify any pre-Lean sanity checks that are necessary conditions and cannot
   reject a theorem that Lean could prove.  Examples may include finite
   Gaussian-moment checks, dimensional consistency, sign conventions, or toy
   scalar cases; do not present them as formal proof.
5. If an external theorem is needed, name the exact public theorem/source I
   should cite or formalize next.
6. Do not claim completion unless the remaining proof obligations are closed by
   Lean-level theorem routes.
"""


def write_cycle_pro_prompt(task_id: str, cycle: int, run_dir: Path) -> tuple[Path, Path, Path]:
    text = public_article_text(chatgpt_pro_prompt_markdown(task_id, cycle, run_dir))
    run_path = run_dir / "chatgpt_pro_prompt.md"
    archive_path = PRO_PROMPT_DIR / f"{slugify(task_id)}-cycle{cycle:03d}.md"
    latest_path = PRO_PROMPT_DIR / f"{slugify(task_id)}-latest.md"
    write_text(run_path, text)
    write_text(archive_path, text)
    write_text(latest_path, text)
    add_manifest("astis.py cycle-pro-prompt", run_path, "pro-prompt", f"Wrote ChatGPT Pro prompt for {task_id} cycle {cycle}")
    return run_path, archive_path, latest_path


def run_dir_from_arg(run_id: str) -> Path:
    if run_id == "latest":
        run_dir = latest_run_dir()
        if run_dir is None:
            raise SystemExit("no run directories found")
        return run_dir
    run_dir = ROOT / "runs" / run_id
    if not run_dir.exists():
        raise SystemExit(f"run directory not found: {rel(run_dir)}")
    return run_dir


def resolved_cycle(task_id: str, requested_cycle: int, run_dir: Path) -> int:
    if requested_cycle > 0:
        return requested_cycle
    match = re.search(r"-cycle(\d+)", run_dir.name)
    if match:
        return int(match.group(1))
    return max(latest_cycle_number(task_id), latest_trial_cycle(task_id), 1)


def cmd_memory_refresh(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    run_dir = run_dir_from_arg(args.run_id)
    cycle = resolved_cycle(args.task, args.cycle, run_dir)
    digest_path, todo_path, index_path = write_memory_refresh(args.task, cycle, run_dir)
    print(f"memory-digest: {rel(digest_path)}")
    print(f"memory-todo: {rel(todo_path)}")
    print(f"retrieval-index: {rel(index_path)}")
    return 0


def cycle_zh_summary_markdown(snapshot: dict) -> str:
    open_sald = snapshot.get("open_sald_contribution_obligations", [])
    open_tech = snapshot.get("open_external_technical_lemma_obligations", [])
    feedback = snapshot.get("recent_verifier_feedback", [])
    active_leaf = snapshot.get("dynamic_leaf_queue", [""])[0]
    latest_blocker = snapshot.get("open_obligation_signals", [""])[0]
    return f"""# ASTIS 中文循环总结：{snapshot.get('task_id')} cycle {snapshot.get('cycle')}

生成时间：`{snapshot.get('generated')}`

运行目录：`{snapshot.get('run_dir')}`

## 一页版结论

- 当前阶段：`{snapshot.get('stage')}`，模式：`{snapshot.get('mode')}`。
- 本轮最该盯住的 leaf：{active_leaf or "尚未记录 dynamic leaf"}。
- 最新 blocker：{latest_blocker or "尚未记录 blocker"}。
- 人类只需要先判断一件事：下一轮是继续关掉这个最小 leaf，还是允许系统把它降级为 source-cited obligation 后先完成 SALD proof DAG。

## 为什么“常识”也会卡 Lean

{sald_plain_language_status_zh()}

目前需要区分两类东西：

- **SALD 本文贡献**：论文自己提出的 VA-SALD 跟踪、guided path residual、moving-target theorem、离散 Euler--Maruyama theorem 等。ASTIS 必须忠实复现原文定理、常数、假设和 proof route。
- **前置 technical lemma**：测度论、KL/FI/LSI、Fokker--Planck、Ito/Taylor、Gaussian moments、integration by parts 等。它们在论文里通常是“标准事实”，但 Lean 不能把“标准”自动当成证明，必须在本库有可编译 statement，或者明确记录为 port queue / proof obligation。

换句话说，卡住不等于 SALD 思想没翻译出来；多数卡点是把纸面证明省略的正则性、可测性、可积性、边界项和条件分布细节，落到本项目的 Lean 类型和假设里。

## 本轮应该怎样读

先看“本轮还没完成的 SALD 本文贡献”，确认是否仍是原论文自己的 leaf；再看“前置 technical lemma”，确认是不是只缺一个常识工具。下面表格是审查入口，不是要求你读 Lean code。

## 新的 leaf 证明标准

下轮 lower agent 不能拿一个大 theorem 直接乱试。每个 packet 必须只对应一个小 lemma，并写清楚：

- theorem statement；
- 本地 ASTIS lemma 和 Mathlib API 先查哪里；
- 需要哪些隐藏正则性假设，例如可测、可积、dominated convergence、条件分布代表元、边界项；
- 预计证明路线；
- 如果重复失败，究竟是缺假设、statement 可能错、代表元不匹配、Mathlib API 不匹配，还是目标太大。

这些规则已经写入 `docs/mathlib_ready_leaf_protocol.md` 和 `research-wiki/lemma-dags/`。目标不是只为 SALD 临时补洞，而是把 SDE/Sampling 的通用 leaf lemma 做到 future Mathlib-ready 的粒度。

## 本轮还没完成的 SALD 本文贡献

{markdown_table(open_sald, [
    ('id', 'id'),
    ('原文位置', 'source_ref'),
    ('Lean 边界', 'lean_boundary'),
    ('状态', 'lean_status'),
    ('下一步', 'next_action'),
], limit=12)}

## 本轮还没补齐的前置 technical lemma

{markdown_table(open_tech, [
    ('id', 'id'),
    ('来源', 'source'),
    ('statement', 'statement'),
    ('状态', 'lean_status'),
    ('服务于', 'used_by'),
    ('下一步', 'next_action'),
], limit=12)}

## 最近 reviewer / verifier 反馈

{markdown_table(feedback, [
    ('leaf', 'leaf'),
    ('错误类别', 'error_class'),
    ('Lean build', 'lean_build_ok'),
    ('测度论', 'measure_theory_ok'),
    ('technical lemma', 'technical_lemma_ok'),
    ('下一条路线', 'next_route'),
], limit=8)}

## 下一轮给人的 high-level 指导入口

1. 先看 SALD 本文贡献表，确认下一轮是否继续当前 source-line leaf，而不是开新战线。
2. 再看 technical lemma 表，只补当前 leaf 真正需要的最小背景事实。
3. 若一个“常识”lemma 已在外部库存在，也必须变成 ASTIS-owned Lean code 后才能被 lower agent 调用。
"""


def write_cycle_zh_summary(task_id: str, cycle: int, run_dir: Path) -> Path:
    snapshot = memory_snapshot_state(task_id, cycle, run_dir)
    text = cycle_zh_summary_markdown(snapshot)
    run_path = run_dir / "zh_summary.md"
    write_text(run_path, text)
    archive_dir = SALD_CYCLE_SUMMARY_DIR if task_id == "ASTIS-SALD-001" else ROOT / "paper-notes" / slugify(task_id) / "markdown" / "cycle-summaries"
    cycle_path = archive_dir / f"{slugify(task_id)}-cycle{cycle:03d}.md"
    latest_path = archive_dir / "latest.md"
    write_text(cycle_path, text)
    write_text(latest_path, text)
    add_manifest("astis.py cycle-zh-summary", run_path, "paper", f"Wrote Chinese cycle summary for {task_id} cycle {cycle}")
    return run_path


def cmd_cycle_zh_summary(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    run_dir = run_dir_from_arg(args.run_id)
    cycle = resolved_cycle(args.task, args.cycle, run_dir)
    path = write_cycle_zh_summary(args.task, cycle, run_dir)
    print(f"zh-summary: {rel(path)}")
    print(f"zh-summary-latest: {rel(SALD_CYCLE_SUMMARY_DIR / 'latest.md') if args.task == 'ASTIS-SALD-001' else 'task-specific latest'}")
    return 0


def cmd_cycle_pro_prompt(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    run_dir = run_dir_from_arg(args.run_id)
    cycle = resolved_cycle(args.task, args.cycle, run_dir)
    run_path, archive_path, latest_path = write_cycle_pro_prompt(args.task, cycle, run_dir)
    print(f"pro-prompt: {rel(run_path)}")
    print(f"pro-prompt-archive: {rel(archive_path)}")
    print(f"pro-prompt-latest: {rel(latest_path)}")
    return 0


def project_article_update_markdown(snapshot: dict) -> str:
    return f"""# Project Article Cycle Update: {snapshot.get('task_id')} cycle {snapshot.get('cycle')}

Generated: `{snapshot.get('generated')}`

## Reader-Facing Status

{sald_plain_language_status_en()}

ASTIS separates paper-specific contributions from reusable background formalization.  The former records what the target paper actually proves and where it appears in the source; the latter records common probability, measure-theory, and SDE lemmas that must compile locally before an agent may use them.

## Mathlib-Ready Leaf Discipline

Reusable background leaves are treated as future Mathlib candidates.  Each
lower packet should close one small theorem, state the local APIs and proof
route, expose measurability/integrability/smoothness assumptions, and stop
when repeated failure indicates a missing assumption or false statement.  The
current generated DAGs live under `research-wiki/lemma-dags/`.

## Open Paper-Contribution Leaves

{markdown_table(snapshot.get('open_sald_contribution_obligations', []), [
    ('id', 'id'),
    ('source', 'source_ref'),
    ('Lean boundary', 'lean_boundary'),
    ('status', 'lean_status'),
    ('next action', 'next_action'),
], limit=10)}

## Open Technical-Lemma Leaves

{markdown_table(snapshot.get('open_external_technical_lemma_obligations', []), [
    ('id', 'id'),
    ('source', 'source'),
    ('status', 'lean_status'),
    ('used by', 'used_by'),
    ('next action', 'next_action'),
], limit=10)}

## Harness Lesson

The useful control signal for the next cycle is not the raw number of remaining leaves.  It is whether the next lower packet closes one exact source-line leaf or ports one exact background lemma needed by that leaf.  This is why the ABEIS-style retrieval index is compact, typed, and split into paper-contribution memory and technical-lemma memory.
"""


def project_article_update_latex(snapshot: dict) -> str:
    open_sald = snapshot.get("open_sald_contribution_obligations", [])
    open_tech = snapshot.get("open_external_technical_lemma_obligations", [])
    sald_items = "\n".join(
        rf"\item \texttt{{{latex_escape_text(str(row.get('id', '')))}}}: {latex_escape_text(str(row.get('source_ref', 'line-range-missing')))}; {latex_escape_text(str(row.get('next_action', '')))}"
        for row in open_sald[:8]
    ) or r"\item No open paper-contribution leaves were listed in the retrieval snapshot."
    tech_items = "\n".join(
        rf"\item \texttt{{{latex_escape_text(str(row.get('id', '')))}}}: {latex_escape_text(str(row.get('source', 'local/ported')))}; {latex_escape_text(str(row.get('next_action', '')))}"
        for row in open_tech[:8]
    ) or r"\item No open technical-lemma leaves were listed in the retrieval snapshot."
    return rf"""\paragraph{{Cycle {snapshot.get('cycle')} ASTIS status update.}}
{latex_escape_text(sald_plain_language_status_en())}

\paragraph{{Open paper-contribution leaves.}}
\begin{{itemize}}
{sald_items}
\end{{itemize}}

\paragraph{{Open technical-lemma leaves.}}
\begin{{itemize}}
{tech_items}
\end{{itemize}}

\paragraph{{Mathlib-ready leaf discipline.}}
Reusable background leaves are treated as future Mathlib candidates.  Each lower packet should close one small theorem, name the local APIs and proof route, expose hidden regularity assumptions, and stop when repeated failure indicates a missing assumption, false statement, representative mismatch, or API mismatch.

\paragraph{{Harness lesson.}}
ASTIS now records an ABEIS-style compact retrieval packet after each completed cycle.  The packet separates paper-specific source-line obligations from reusable technical lemmas, so upper and middle agents can make high-level decisions without replaying long logs.
"""


def write_project_article_update(task_id: str, cycle: int, run_dir: Path) -> tuple[Path, Path]:
    snapshot = memory_snapshot_state(task_id, cycle, run_dir)
    md_text = project_article_update_markdown(snapshot)
    tex_text = project_article_update_latex(snapshot)
    run_md = run_dir / "article_update.md"
    run_tex = run_dir / "article_update.tex"
    write_text(run_md, md_text)
    write_text(run_tex, tex_text)
    archive_stem = f"{slugify(task_id)}-cycle{cycle:03d}"
    write_text(PROJECT_ARTICLE_UPDATE_DIR / f"{archive_stem}.md", md_text)
    write_text(PROJECT_ARTICLE_UPDATE_DIR / f"{archive_stem}.tex", tex_text)
    write_text(PROJECT_ARTICLE_UPDATE_DIR / f"{slugify(task_id)}-latest.md", md_text)
    write_text(PROJECT_ARTICLE_UPDATE_DIR / f"{slugify(task_id)}-latest.tex", tex_text)
    write_text(TECH_REPORT_ROOT / "sections" / "generated_memory_status.tex", public_article_text(tex_text))
    write_text(TECH_REPORT_ROOT / "sections" / "generated_memory_status.md", public_article_text(md_text))
    add_manifest("astis.py project-article-update", run_tex, "paper", f"Wrote project article update for {task_id} cycle {cycle}")
    return run_md, run_tex


def cmd_project_article_update(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    run_dir = run_dir_from_arg(args.run_id)
    cycle = resolved_cycle(args.task, args.cycle, run_dir)
    md_path, tex_path = write_project_article_update(args.task, cycle, run_dir)
    print(f"article-update-md: {rel(md_path)}")
    print(f"article-update-tex: {rel(tex_path)}")
    return 0


def post_cycle_refresh(task_id: str, cycle: int, run_dir: Path, write_zh_summary: bool = True) -> None:
    if task_id == "ASTIS-SALD-001":
        ensure_source_index(task_id)
        write_blueprint_refresh(task_id)
        write_blueprint_status(task_id)
        write_sald_unfinished_source_map(cycle)
        write_sald_reproduction_todo(cycle)
    write_memory_refresh(task_id, cycle, run_dir)
    if write_zh_summary:
        write_cycle_zh_summary(task_id, cycle, run_dir)
        write_cycle_pro_prompt(task_id, cycle, run_dir)
    write_project_article_update(task_id, cycle, run_dir)


def cmd_finalize_sald_cycle(args: argparse.Namespace) -> int:
    cycle = args.cycle if args.cycle > 0 else max(
        latest_cycle_number("ASTIS-SALD-001"),
        latest_trial_cycle("ASTIS-SALD-001"),
    )
    cmd_source_index(argparse.Namespace(task="ASTIS-SALD-001"))
    write_blueprint_refresh("ASTIS-SALD-001")
    write_blueprint_status("ASTIS-SALD-001")
    write_sald_unfinished_source_map(cycle)
    write_sald_reproduction_todo(cycle)
    write_context_pack("ASTIS-SALD-001", max(cycle + 1, 1))
    run_dir = latest_run_dir()
    if run_dir is not None:
        post_cycle_refresh("ASTIS-SALD-001", cycle, run_dir, write_zh_summary=True)
    code = cmd_export_latex(argparse.Namespace(task="ASTIS-SALD-001", skip_technical_report=False))
    if code != 0:
        return code
    if getattr(args, "run_check", False):
        return cmd_check(argparse.Namespace())
    print(f"finalized ASTIS-SALD-001 cycle {cycle}")
    print(f"unfinished source map: {rel(SALD_UNFINISHED_SOURCE_MAP)}")
    print(f"Lean gate status recorded: {latest_lean_gate_status('ASTIS-SALD-001')}")
    return 0


def cmd_blueprint_status(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else None
    if output is not None and not output.is_absolute():
        output = ROOT / output
    md_path, json_path = write_blueprint_status(args.task, output)
    print(f"blueprint status: {rel(md_path)}")
    print(f"blueprint json: {rel(json_path)}")
    return 0


def cmd_blueprint_refresh(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else None
    if output is not None and not output.is_absolute():
        output = ROOT / output
    path = write_blueprint_refresh(args.task, output)
    print(f"blueprint: {rel(path)}")
    return 0


def cmd_export_latex(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    task = getattr(args, "task", "ASTIS-SALD-001")
    if task == "ASTIS-SALD-001":
        cycle_note = max(latest_cycle_number(task), latest_trial_cycle(task))
        ensure_source_index(task)
        write_sald_unfinished_source_map(cycle_note)
        write_sald_reproduction_todo(cycle_note)
    base = ROOT / "paper-notes" / "AutoLeanInSleepSampling"
    latex = base / "latex"
    sections = latex / "sections"
    figures = latex / "figures"
    markdown = base / "markdown"
    source_count = len(load_jsonl(ROOT / "research-wiki" / "source-index" / "SALD_original.jsonl"))
    trial_count = len(load_jsonl(TRIAL_LOG))
    latest_cycle = latest_cycle_number(task)
    export_date = now_stamp()
    blueprint_state = blueprint_control_state(task)
    latest_handoffs = latest_handoff_notes(task, limit=5)

    def latex_escape(value: str) -> str:
        value = public_article_text(value)
        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }
        return "".join(replacements.get(char, char) for char in value)

    unfinished_items = sald_unfinished_source_items() if task == "ASTIS-SALD-001" else []
    unfinished_markdown_table = unfinished_source_markdown_table(unfinished_items) if unfinished_items else "| none | none | none | none | none | none |"
    unfinished_latex_rows = "\n".join(
        rf"{latex_escape(row.get('id', ''))} & {latex_escape(row.get('source_ref', 'line-range-missing'))} & {latex_escape(row.get('status', ''))} \\"
        for row in unfinished_items[:10]
    ) or r"none & none & none \\"
    registry_rows = technical_lemma_registry_rows()
    formalized_count = sum(1 for row in registry_rows if row.get("status") == "formalized-local")
    port_count = len([row for row in registry_rows if row.get("status") != "formalized-local"]) + len(technical_lemma_port_queue_rows())
    proof_status_markdown = "\n".join(
        f"- `{key}`: {value}" for key, value in sorted(blueprint_state["proof_status_counts"].items())
    )
    packet_markdown = "\n".join(
        f"- `{key}`: {value}" for key, value in blueprint_state["trial_classifications_recent"].items()
    )
    handoff_markdown = "\n".join(
        f"- {public_article_text(note)}" for note in latest_handoffs
    ) or "- No recent handoff notes were found."
    blocker_markdown = f"""## Human-Readable Blocker Report

The current SALD reproduction is not blocked by a missing source index or by
an interrupted run.  It is blocked by the analytic backend that the paper treats
as standard prose: weak Fokker--Planck source actions, Laplacian source fields,
measurability and state-integral identities, Green identities, boundary trace
conditions, box-divergence facts, and diffusion generator leaves.

For a non-specialist: the paper can write one line such as "by the weak
Fokker--Planck equation and integration by parts".  Lean needs every object in
that sentence to be explicit: which law is being integrated against, which
representative of a conditional expectation is used, why the function is
measurable and integrable, why the boundary term is zero, and which exact
Laplacian/divergence theorem applies.

Plain-language separation:

| Layer | Meaning | Why it matters |
|---|---|---|
| SALD contribution | The source paper's KL contraction, moving-target, guided-residual, and EM proof route | Must be reproduced faithfully with the same statements and constants |
| Technical lemma memory | Standard KL/FI/LSI, Fokker--Planck, Ito/Taylor, Gaussian moment, measurability, integrability, and IBP tools | Common in prose, but callable in ASTIS only after a local compiled Lean statement exists |
| Source-contract gap | A regularity or representative choice the source proof seems to use implicitly | Must be found in the source assumptions or kept as an explicit obligation |

Human guidance before the next 6h run should choose a policy: finish the SALD
proof DAG with source-cited background obligations, invest in a reusable
technical lemma library, or use the default local strategy of porting only the
smallest background lemma needed by the next SALD source-line leaf.

Current dynamic leaf:

```text
{public_article_text(blueprint_state["dynamic_leaf_candidate"])}
```

Current illness area:

```text
{public_article_text(blueprint_state["illness_area_candidate"])}
```

Latest blocker:

```text
{public_article_text(blueprint_state["latest_blocker"])}
```

Recent packet classifications:

{packet_markdown}

Proof-status counts:

{proof_status_markdown}

Unfinished source-line map:

| Boundary id | Type | Source lines | Lean boundary | Status | Next action |
|---|---|---|---|---|---|
{unfinished_markdown_table}

Technical lemma memory status:

- Formalized local registry entries: {formalized_count}
- Port queue entries: {port_count}
- Port candidates are not callable until they become ASTIS-owned compiled declarations.

Recent reviewer/lower handoffs:

{handoff_markdown}
"""
    blocker_latex_items = [
        "weak Fokker--Planck source actions",
        "Laplacian source-field equality and measurability",
        "state-integral identities under the selected EM law",
        "Green identities and boundary trace terms",
        "box-divergence and diffusion-generator leaves",
    ]
    blocker_latex_items_text = "\n".join(
        rf"\item {latex_escape(item)}" for item in blocker_latex_items
    )
    proof_status_latex = "\n".join(
        rf"\item \Lean{{{latex_escape(str(key))}}}: {value}"
        for key, value in sorted(blueprint_state["proof_status_counts"].items())
    )
    packet_latex = "\n".join(
        rf"\item \Lean{{{latex_escape(str(key))}}}: {value}"
        for key, value in blueprint_state["trial_classifications_recent"].items()
    )
    blocker_latex = rf"""\subsection{{Why the SALD Reproduction Is Not Finished}}

The current bottleneck is not source discovery or an interrupted run.  The
remaining work is the analytic backend that the source proof compresses into
standard prose.  In particular, ASTIS still has to discharge or precisely cite:
\begin{{itemize}}
{blocker_latex_items_text}
\end{{itemize}}

For a non-specialist, the issue is that a paper sentence such as ``by the weak
Fokker--Planck equation and integration by parts'' hides many Lean obligations:
the law being integrated against, the conditional-expectation representative,
measurability, integrability, almost-everywhere equality, boundary terms, and
the exact theorem instance for Laplacian or divergence calculus.

\paragraph{{Plain-language separation.}}
The current blocker does not mean that the VA-SALD construction is absent.
The source theorem route and many local substeps are represented.  What remains
is a mixture of SALD-specific source leaves and background technical lemmas.
In papers, KL/FI/LSI identities, weak Fokker--Planck equations, Ito/Taylor
expansions, Gaussian moment bounds, measurability, integrability, and
integration by parts are often treated as standard.  In ASTIS, they are not
callable facts until they are either ASTIS-owned compiled Lean declarations or
explicit source-cited proof obligations.

\begin{{center}}
\begin{{tabular}}{{p{{0.22\linewidth}}p{{0.34\linewidth}}p{{0.32\linewidth}}}}
\toprule
Layer & Meaning & Run policy \\
\midrule
SALD contribution & The paper's theorem statements and proof route & Preserve
the source statements and constants. \\
Technical lemma memory & Reusable measure/probability/SDE tools & Port only
the smallest lemma needed by the active source-line leaf unless a reusable
library push is explicitly chosen. \\
Source-contract gap & Implicit regularity or representative choices & Locate
the source assumption or keep an honest obligation. \\
\bottomrule
\end{{tabular}}
\end{{center}}

\paragraph{{Human guidance before the next run.}}
A useful high-level instruction can choose between three policies: keep
background facts as source-cited obligations to complete the proof DAG faster;
spend a run building reusable technical lemma memory; or use the default local
strategy, where ASTIS ports only the smallest background lemma needed by the
next SALD source-line leaf.

\paragraph{{Current dynamic leaf.}}
\begin{{quote}}\small
{latex_escape(blueprint_state["dynamic_leaf_candidate"])}
\end{{quote}}

\paragraph{{Current illness area.}}
\begin{{quote}}\small
{latex_escape(blueprint_state["illness_area_candidate"])}
\end{{quote}}

\paragraph{{Latest blocker.}}
\begin{{quote}}\small
{latex_escape(blueprint_state["latest_blocker"])}
\end{{quote}}

\paragraph{{Recent packet classifications.}}
\begin{{itemize}}
{packet_latex}
\end{{itemize}}

\paragraph{{Proof-status counts.}}
\begin{{itemize}}
{proof_status_latex}
\end{{itemize}}

\paragraph{{Unfinished source-line map.}}
\begin{{center}}
\begin{{tabular}}{{p{{0.28\linewidth}}p{{0.22\linewidth}}p{{0.38\linewidth}}}}
\toprule
Boundary & Source lines & Status \\
\midrule
{unfinished_latex_rows}
\bottomrule
\end{{tabular}}
\end{{center}}

\paragraph{{Technical lemma memory.}}
ASTIS currently records {formalized_count} formalized local technical-lemma
registry entries and {port_count} technical-lemma port-queue entries.  Port
candidates are not callable until they become ASTIS-owned compiled
declarations under \Lean{{AutoSamplingTheory/TechnicalLemmas}}.
"""

    replacements = {
        "@EXPORT_DATE@": export_date,
        "@SOURCE_COUNT@": str(source_count),
        "@TRIAL_COUNT@": str(trial_count),
        "@LATEST_CYCLE@": str(latest_cycle),
        "@QUANTUM_URL@": QUANTUM_AUTOPROOF_URL,
        "@SLT_URL@": SLT_URL,
        "@SLT_ARXIV_URL@": SLT_ARXIV_URL,
        "@LEANMARATHON_URL@": LEANMARATHON_URL,
        "@LEANMARATHON_ARXIV_URL@": LEANMARATHON_ARXIV_URL,
        "@MATHCODE_URL@": MATHCODE_URL,
        "@ARIS_URL@": ARIS_URL,
        "@LBG_URL@": LBG_URL,
        "@EOH_URL@": EOH_URL,
        "@HUMAN_BLOCKER_MARKDOWN@": blocker_markdown,
        "@HUMAN_BLOCKER_LATEX@": blocker_latex,
    }

    def fill(text: str) -> str:
        for key, value in replacements.items():
            text = text.replace(key, value)
        return text

    write_text(base / "README.md", fill("""# Auto-Lean-in-Sleep for Sampling Theory

This directory is the human-readable proof export for ASTIS.  The LaTeX source
under `latex/` is intended as an Overleaf-ready project article.  The VA-SALD
faithful reproduction is an appendix case study inside that larger article,
not a standalone replacement for the source paper.

Last exported: @EXPORT_DATE@
"""))

    write_text(markdown / "status.md", fill("""# ASTIS Project Article Export

- Task: `ASTIS-SALD-001`
- Latest cycle number observed: @LATEST_CYCLE@
- Source-indexed original SALD declarations: @SOURCE_COUNT@
- Trial-log records: @TRIAL_COUNT@
- Quantum automation reference: @QUANTUM_URL@
- SLT reference: @SLT_URL@
- SLT article: @SLT_ARXIV_URL@
- LeanMarathon reference: @LEANMARATHON_URL@
- LeanMarathon article: @LEANMARATHON_ARXIV_URL@
- MathCode workflow reference: @MATHCODE_URL@
- ARIS / auto-research-in-sleep reference: @ARIS_URL@
- Learning Beyond Gradients reference: @LBG_URL@
- EoH reference: @EOH_URL@

The export is batch-based.  Lean and the conversion windows remain the source
of truth; this document is the middle-agent human-audit layer.

@HUMAN_BLOCKER_MARKDOWN@
"""))

    zh_summary = chinese_sald_window_summary_text(
        task=task,
        export_date=export_date,
        source_count=source_count,
        trial_count=trial_count,
        state=blueprint_state,
        handoffs=latest_handoffs,
        diagnostics=lean_diagnostics(),
    )
    window_info = latest_sald_window_info()
    zh_dir = markdown / "zh"
    zh_cycle_name = f"{slugify(task)}-cycle{window_info['cycle_range']}-zh.md"
    write_text(zh_dir / zh_cycle_name, zh_summary)
    write_text(zh_dir / f"{slugify(task)}-latest-zh.md", zh_summary)

    write_text(latex / "main.tex", fill(r"""\documentclass[11pt]{article}

\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{booktabs,longtable,array}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,fit,shapes.geometric}
\usepackage[hidelinks]{hyperref}

\newcommand{\Lean}[1]{\texttt{\detokenize{#1}}}
\newcommand{\ASTIS}{Auto-Lean-in-Sleep for Sampling Theory}
\newcommand{\ProofObligation}{\textsc{ProofObligation}}

\title{\ASTIS\\An Automated Lean Workflow for SDE and Sampling Theory}
\author{Auto-Sampling-Theory-In-Sleep Project}
\date{Last exported: @EXPORT_DATE@}

\begin{document}
\maketitle
\tableofcontents

\input{sections/00_overview}
\input{sections/01_system}
\input{sections/02_agent_phases}
\input{sections/03_evidence_status}

\appendix
\input{sections/A_sald_case}
\input{sections/B_task_list}

\end{document}
"""))

    write_text(figures / "system_pipeline.tex", r"""\begin{figure}[t]
\centering
\begin{tikzpicture}[
  node distance=1.2cm,
  stage/.style={draw, rounded corners=2pt, align=center, minimum width=2.7cm, minimum height=0.9cm, fill=blue!4},
  check/.style={draw, diamond, aspect=2, align=center, fill=green!5},
  arrow/.style={-{Latex[length=2mm]}, thick}
]
\node[stage] (source) {Paper or\\proof draft};
\node[stage, right=of source] (index) {Source\\index};
\node[stage, right=of index] (lean) {Lean-facing\\contracts};
\node[stage, right=of lean] (oblig) {Proof\\obligations};
\node[stage, below=of oblig] (attempt) {Lower-agent\\Lean attempts};
\node[check, left=of attempt] (gate) {Reviewer\\gate};
\node[stage, left=of gate] (export) {Markdown/\\LaTeX export};
\draw[arrow] (source) -- (index);
\draw[arrow] (index) -- (lean);
\draw[arrow] (lean) -- (oblig);
\draw[arrow] (oblig) -- (attempt);
\draw[arrow] (attempt) -- (gate);
\draw[arrow] (gate) -- (export);
\draw[arrow] (gate.north) |- (lean.south);
\end{tikzpicture}
\caption{ASTIS keeps source correspondence, Lean contracts, proof obligations,
agent attempts, reviewer gates, and human-readable exports in one loop.}
\end{figure}
""")

    write_text(figures / "agent_stack.tex", r"""\begin{figure}[t]
\centering
\begin{tikzpicture}[
  box/.style={draw, rounded corners=2pt, align=left, minimum width=0.85\textwidth, inner sep=6pt},
  arrow/.style={-{Latex[length=2mm]}, thick}
]
\node[box, fill=purple!5] (upper) {\textbf{Upper panel}: \Lean{source\_math}, \Lean{proof\_dag}, and \Lean{process\_memory} specialists feed \Lean{upper\_director}};
\node[box, fill=blue!5, below=0.45cm of upper] (middle) {\textbf{Middle panel}: \Lean{source\_correspondence}, \Lean{technical\_lemma}, and \Lean{report\_export} feed \Lean{middle\_formalizer}};
\node[box, fill=orange!8, below=0.45cm of middle] (lower) {\textbf{Lower}: \Lean{lower\_1} proof route, \Lean{lower\_2} Lean theorem, \Lean{lower\_3} technical lemma/API};
\node[box, fill=green!6, below=0.45cm of lower] (reviewer) {\textbf{Reviewer}: \Lean{reviewer\_gate} checks Lean/source; \Lean{reviewer\_waste} audits opportunity cost at final audit};
\draw[arrow] (upper) -- (middle);
\draw[arrow] (middle) -- (lower);
\draw[arrow] (lower) -- (reviewer);
\draw[arrow] (reviewer.east) .. controls +(1.0,0.7) and +(1.0,-0.7) .. (upper.east);
\end{tikzpicture}
\caption{ASTIS uses lightweight inner cycles and bounded final-audit panels.
The panel split is specialized to Sampling/SDE proof bottlenecks: source
regularity, proof-DAG leaves, technical lemma retrieval, implementation, and
human-readable reporting.}
\end{figure}
""")

    write_text(figures / "run_loop.tex", r"""\begin{figure}[t]
\centering
\begin{tikzpicture}[
  node distance=0.9cm,
  box/.style={draw, rounded corners=2pt, align=center, minimum width=2.4cm, minimum height=0.75cm, inner sep=4pt},
  arrow/.style={-{Latex[length=2mm]}, thick}
]
\node[box, fill=blue!5] (inneru) {inner\\\Lean{upper\_director}};
\node[box, fill=blue!5, right=of inneru] (innerm) {inner\\\Lean{middle\_formalizer}};
\node[box, fill=orange!8, right=of innerm] (lower) {\Lean{lower\_1}\\\Lean{lower\_2}\\\Lean{lower\_3}};
\node[box, fill=green!6, right=of lower] (gate) {\Lean{reviewer\_gate}};
\node[box, fill=purple!5, below=of innerm] (upanel) {final upper panel};
\node[box, fill=cyan!5, right=of upanel] (mpanel) {final middle panel};
\node[box, fill=green!6, right=of mpanel] (final) {final reports\\\Lean{reviewer\_waste}};
\draw[arrow] (inneru) -- (innerm);
\draw[arrow] (innerm) -- (lower);
\draw[arrow] (lower) -- (gate);
\draw[arrow] (gate.south) |- (upanel.west);
\draw[arrow] (upanel) -- (mpanel);
\draw[arrow] (mpanel) -- (final);
\draw[arrow] (gate.north) .. controls +(0,0.8) and +(0,0.8) .. node[above,font=\scriptsize]{repeat until budget closes} (inneru.north);
\end{tikzpicture}
\caption{Default 6h cadence.  Inner cycles stay proof-focused; final audit
runs upper/middle panels and synchronizes human-facing reports.}
\end{figure}
""")

    write_text(sections / "00_overview.tex", fill(r"""\section{Overview}

\ASTIS{} is a Lean-centered automation system for SDE, sampling, and guided
generation theory.  Its first faithful-paper target is the public VA-SALD
paper under the project task \Lean{ASTIS-SALD-001}.  The reproduction treats
that paper as the source of truth rather than later internal drafts.

The system adapts the public Quantum block-encoding automation workflow at
\url{@QUANTUM_URL@}.  The domain semantics are different: ASTIS tracks laws,
densities, transport velocities, Fokker--Planck identities, KL/FI/LSI/PI
interfaces, Euler--Maruyama discretization, and particle approximations.

ASTIS also uses \url{@SLT_URL@} and the article
\url{@SLT_ARXIV_URL@} as nearby Mathlib-based references.  That project
formalizes statistical-learning and concentration tools such as entropy
duality, Gaussian Poincare and log-Sobolev results, and one-step
discretization statements.  ASTIS records these as reuse candidates rather
than importing them directly while the toolchain versions differ.

ASTIS deliberately combines several automation lineages.  From
ARIS/auto-research-in-sleep \url{@ARIS_URL@}, it keeps the plain-file,
long-window research loop and the upper/middle/lower/reviewer decomposition
with an independent review pass.  From Learning Beyond Gradients
\url{@LBG_URL@}, it keeps role-separated iterative improvement and trial
memory: attempts, logs, summaries, rejected directions, negative caches, and
reviewer feedback are first-class state rather than chat history.  ASTIS
specializes this into upper/middle/lower plus reviewer agents for proof work.
From EoH \url{@EOH_URL@}, ASTIS keeps the population idea only for
\Lean{exploratoryProof}: candidate proof routes may be initialized, varied,
selected, and archived after a Lean-checkable acceptance predicate is fixed.
Faithful-paper reproduction does not mutate the source theorem.

For Lean-specific long-horizon orchestration, ASTIS attributes and studies
LeanMarathon \url{@LEANMARATHON_URL@} and its article
\url{@LEANMARATHON_ARXIV_URL@}.  ASTIS absorbs its blueprint-as-system-of-record
view, target-review discipline, dynamic proof-DAG leaves, illness-area
refiner rule, and deterministic CI-gate principle.  This control layer
complements rather than replaces the ARIS/LBG/EoH components above.  ASTIS's
own specialization is the SDE/Sampling correspondence layer: source anchors,
KL/FI/LSI/PI contracts, Fokker--Planck and Euler--Maruyama obligations,
technical lemma memory, SLT/SDE cited-result ledgers, and
Lean-Markdown-LaTeX exports.

For proof-automation workflow design, ASTIS also studies
\url{@MATHCODE_URL@}.  The adopted ideas are diagnostic rather than source-code
reuse: explicit scans for hidden assumptions and placeholders, theorem-reuse
memory before new lemma creation, tree-of-subgoals decomposition as an internal
work plan, and proof-statistics review for broad rewrites.

\input{figures/system_pipeline}
"""))

    write_text(sections / "01_system.tex", fill(r"""\section{System Design}

The source of truth is Lean plus explicit ledgers.  A mathematical ingredient
is never treated as proved merely because it is plausible in prose.  If it is
not a compiled Lean declaration, it must be a \ProofObligation{} or a cited
result with a recorded Lean status.

The workflow has two public modes.  In \Lean{faithfulPaper} mode, the theorem,
assumptions, constants, and proof target are fixed by the source paper.  In
\Lean{exploratoryProof} mode, the system tracks proof routes for active
research drafts, such as RMFLD, without promoting candidate assumptions to
facts.

The project-paper framing follows the automation emphasis of
\url{@ARIS_URL@}, the search-memory perspective of \url{@LBG_URL@}, the
population-and-archive idea of \url{@EOH_URL@}, the Lean-specific blueprint
control loop of \url{@LEANMARATHON_URL@}, and the Lean proof-diagnostics
workflow exemplified by \url{@MATHCODE_URL@}.  The acceptance condition is
stricter than search success: every cycle must leave a buildable repository or
an explicit blocked status, and post-blueprint cycles must identify the
dynamic leaf or illness area they changed.

\input{figures/agent_stack}
"""))

    write_text(sections / "02_agent_phases.tex", r"""\section{Agents and Phases}

Faithful-paper tasks have two phases.  Phase 1 is the complete transcript:
source theorem labels, definitions, proof steps, constants, external results,
and theorem-specific obligations are mapped into Lean-facing declarations and
conversion windows.  This phase deliberately avoids broad library
reorganization unless it is necessary to preserve the source statement.

Phase 2 begins only after the transcript is complete.  It reorganizes shared
SDE/Sampling APIs for education, future paper reproduction, and exploratory
proof work.  Examples include reusable interfaces for KL/FI/LSI, Fokker--
Planck weak forms, Euler--Maruyama one-step errors, and Feynman--Kac particle
systems.

The agent stack is deliberately split into lightweight inner cycles and
bounded final-audit panels.  During ordinary proof-search cycles, ASTIS runs
\Lean{upper\_director}, \Lean{middle\_formalizer}, lower workers, and
\Lean{reviewer\_gate}.  At the final audit, the upper panel adds
\Lean{upper\_source\_math}, \Lean{upper\_proof\_dag}, and
\Lean{upper\_process\_memory} before director synthesis.  The middle panel adds
\Lean{middle\_source\_correspondence}, \Lean{middle\_technical\_lemma}, and
\Lean{middle\_report\_export} before coordinator synthesis.

The lower layer is also specialized.  \Lean{lower\_1} writes the natural-
language proof route and dependency analysis, \Lean{lower\_2} implements one
Lean theorem or one strictly smaller source-cited boundary, and
\Lean{lower\_3} scouts the smallest technical lemma or Mathlib API fact needed
by the active leaf.  \Lean{lower\_4} is reserved for concrete Lean-failure
refinement and is not enabled by default.

This split matters more for Sampling/SDE than for small algebraic examples.
The same paper sentence can hide a source-specific theorem leaf and several
background obligations about laws, conditional representatives, measurability,
integrability, Ito/Taylor expansion, and boundary terms.  A single middle agent
is too easily pulled into copying handoffs.  ASTIS therefore makes source-DAG
architecture, lemma-memory retrieval, and human-report synchronization separate
responsibilities.

The middle layer still owns the two-way conversion layer.  Before lower-agent
work, it translates the source LaTeX proof fragment into Lean declarations,
cited-result rows, or proof obligations.  After lower and reviewer work, it
translates the accepted Lean state back into Markdown and LaTeX.  The polished
Overleaf export is batch-based: it is updated at the end of a multi-hour run,
after the final reviewer gate.

\input{figures/run_loop}
""")

    write_text(sections / "03_evidence_status.tex", fill(r"""\section{Current Evidence}

The current SALD faithful reproduction has @SOURCE_COUNT@ original source
declarations in \Lean{research-wiki/source-index/SALD_original.jsonl}.  The
trial log contains @TRIAL_COUNT@ records, and the latest observed SALD cycle
number is @LATEST_CYCLE@.

The mandatory local gate is
\[
  \Lean{python3 tools/astis.py check},
\]
which runs Mathlib cache retrieval, \Lean{lake build}, \Lean{lake build Tests},
and the ASTIS forbidden-pattern scan.  Forbidden proof closures include
\Lean{sorry}, \Lean{admit}, \Lean{axiom}, \Lean{Prop := True}, and
\Lean{:= trivial}.

@HUMAN_BLOCKER_LATEX@
"""))

    write_text(sections / "A_sald_case.tex", r"""\section{VA-SALD Faithful-Reproduction Case}

The first case study is \Lean{ASTIS-SALD-001}: faithful reproduction of the
public VA-SALD paper proofs.  The first proof DAG tracks
\[
\texttt{lem:gronwall},\quad
\texttt{lem:dv\_variation},\quad
\texttt{eq:LSI-KL-FI},\quad
\texttt{thm:forward-KL},\quad
\texttt{thm:forward-KL-discrete},
\]
followed by guided-path residual and general moving-target VA-SALD results.

At the end of the first long run, cycle 15 was closed rather than interrupted.
The accepted lower slice for \Lean{thm:forward-KL-discrete} is
\[
  \text{\Lean{sald.discrete_forward_kl.conditional_drift_density}}.
\]
It corresponds to the source proof step defining
\[
  \bar b_{k,s}(x)
  = \mathbb{E}\!\left[\nabla \log \pi_{t_k}(X_k^\eta)
      \mid \widehat X_s=x\right],
\]
and records the regular conditional law, density, measurability, and
integrability interfaces needed before the conditional-drift Fokker--Planck
equation can be formalized.  It is intentionally an obligation, not a proved
Fokker--Planck theorem.

\begin{longtable}{p{0.24\textwidth}p{0.34\textwidth}p{0.32\textwidth}}
\toprule
Source step & Lean-facing item & Status \\
\midrule
Continuous and discrete KL/FI/LSI vocabulary &
\Lean{Probability.lean}, \Lean{SALD.lean} contracts &
contracts plus obligations \\
Continuous forward-KL proof route &
\Lean{SALD.forwardKlProofDag} &
source-to-Lean map and obligations \\
Discrete EM interpolation spine &
\Lean{SALD.cycle15DiscreteForwardKlMiddleContract} &
obligation map \\
Conditional drift density &
\Lean{SALD.cycle15DiscreteForwardKlConditionalDriftDensityContract} &
obligation; no fake closure \\
Conditional Fokker--Planck and Laplacian split &
\Lean{sald.discrete_forward_kl.em_conditional_fokker_planck} &
remaining obligation \\
\bottomrule
\end{longtable}
""")

    write_text(sections / "B_task_list.tex", r"""\section{Operational Task List}

\begin{enumerate}
\item Complete Phase 1 for \Lean{ASTIS-SALD-001}: every original VA-SALD
      theorem, definition, and proof step must be represented by a Lean
      declaration, cited result, or \ProofObligation{}.
\item Preserve the batch cadence: run upper, middle, lower, reviewer, and the
      build gate for the final cycle before exporting LaTeX.
\item Keep the SALD case as an appendix to the larger ASTIS article.  The main
      article explains the automation system; the appendix shows what the
      current Lean-backed proof framework looks like.
\item After Phase 1, start Phase 2 organization for reusable SDE/Sampling
      theory blocks and for \Lean{exploratoryProof} targets such as RMFLD.
\end{enumerate}
""")

    add_manifest("astis.py export-latex", latex / "main.tex", "paper", "Exported ASTIS project article and SALD appendix")
    add_manifest("astis.py export-latex", zh_dir / zh_cycle_name, "paper", "Exported Chinese 6h SALD proof-reproduction summary")
    print(f"exported LaTeX article to {rel(latex / 'main.tex')}")
    print(f"exported Chinese summary to {rel(zh_dir / zh_cycle_name)}")
    if not getattr(args, "skip_technical_report", False):
        return cmd_export_technical_report(argparse.Namespace(task=task, report_root=str(TECH_REPORT_ROOT)))
    return 0


def cmd_agent_note(args: argparse.Namespace) -> int:
    run_dir = latest_run_dir() if args.run == "latest" else ROOT / "runs" / args.run
    if run_dir is None or not run_dir.exists():
        raise SystemExit("run directory not found")
    append_line(run_dir / "dialogue.md", f"\n## {args.role} @ {now_stamp()}\n\n{args.message}\n")
    print(f"updated {rel(run_dir / 'dialogue.md')}")
    return 0


def latest_run_dir() -> Path | None:
    runs_root = ROOT / "runs"
    cycle_runs = [
        p for p in runs_root.glob("*")
        if p.is_dir() and re.search(r"-cycle\d+$", p.name)
    ]
    if cycle_runs:
        return sorted(cycle_runs)[-1]
    runs = [
        p for p in runs_root.glob("*")
        if p.is_dir() and p.name not in {"logs", "context-packs", "efficiency"}
    ]
    return sorted(runs)[-1] if runs else None


def git_changed_files() -> list[str]:
    code, output = run_capture(["git", "status", "--short"])
    if code != 0:
        return []
    files = []
    for line in output.splitlines():
        if not line.strip():
            continue
        item = line[3:] if len(line) > 3 else line
        if " -> " in item:
            item = item.split(" -> ", 1)[1]
        files.append(item.strip())
    return sorted(set(files))


def is_git_worktree() -> bool:
    code, output = run_capture(["git", "rev-parse", "--is-inside-work-tree"])
    return code == 0 and output.strip() == "true"


def write_trial_summary(records: list[dict]) -> None:
    handle = io.StringIO(newline="")
    try:
        fieldnames = [
            "index",
            "timestamp",
            "trial_id",
            "task_id",
            "role",
            "kind",
            "status",
            "lean_gate",
            "artifact",
            "changed_files",
            "feedback_leaf",
            "feedback_error_class",
            "source_correspondence_ok",
            "lean_build_ok",
            "mathlib_api_ok",
            "measure_theory_ok",
            "regularity_assumption_ok",
            "technical_lemma_ok",
            "closed_theorem_ok",
            "next_route",
            "notes",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, record in enumerate(records, start=1):
            feedback = record.get("verifier_feedback", {})
            if not isinstance(feedback, dict):
                feedback = {}
            writer.writerow({
                "index": index,
                "timestamp": record.get("timestamp", ""),
                "trial_id": record.get("trial_id", ""),
                "task_id": record.get("task_id", ""),
                "role": record.get("role", ""),
                "kind": record.get("kind", ""),
                "status": record.get("status", ""),
                "lean_gate": record.get("lean_gate", ""),
                "artifact": record.get("artifact", ""),
                "changed_files": ";".join(record.get("changed_files", [])),
                "feedback_leaf": feedback.get("leaf", ""),
                "feedback_error_class": feedback.get("error_class", ""),
                "source_correspondence_ok": feedback.get("source_correspondence_ok", ""),
                "lean_build_ok": feedback.get("lean_build_ok", ""),
                "mathlib_api_ok": feedback.get("mathlib_api_ok", ""),
                "measure_theory_ok": feedback.get("measure_theory_ok", ""),
                "regularity_assumption_ok": feedback.get("regularity_assumption_ok", ""),
                "technical_lemma_ok": feedback.get("technical_lemma_ok", ""),
                "closed_theorem_ok": feedback.get("closed_theorem_ok", ""),
                "next_route": feedback.get("next_route", ""),
                "notes": record.get("notes", ""),
            })
        harness.atomic_write_text(TRIAL_SUMMARY, handle.getvalue())
    finally:
        handle.close()


def cmd_route_attempt(args: argparse.Namespace) -> int:
    fingerprint = harness.route_fingerprint(
        target_statement=args.target_statement,
        missing_property=args.missing_property,
        assumptions=args.assumption,
        mathlib_candidates=args.mathlib_candidate,
        compiler_error_class=args.compiler_error_class,
    )
    record = harness.record_route_attempt(
        STATE_DIR / "route-attempts.jsonl",
        task_id=args.task,
        leaf_id=args.leaf,
        fingerprint=fingerprint,
        candidate=args.candidate,
        exact_subgoal=args.exact_subgoal,
        compiled_declarations=args.compiled_declaration,
    )
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 2 if record["decision"] == "freeze_for_review" else 0


def cmd_trial_log(args: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    changed = list(args.changed_file or [])
    if args.from_git:
        changed.extend(git_changed_files())
    trial_id = args.trial_id or f"{file_stamp()}-{slugify(args.task)}-{args.role}-{args.kind}"
    verifier_feedback = load_feedback_payload(args)
    record = {
        "timestamp": now_stamp(),
        "trial_id": trial_id,
        "task_id": args.task,
        "role": args.role,
        "kind": args.kind,
        "status": args.status,
        "lean_gate": args.lean_gate,
        "artifact": args.artifact or "",
        "changed_files": sorted(set(changed)),
        "notes": args.notes or "",
    }
    if verifier_feedback:
        record["verifier_feedback"] = verifier_feedback
    append_jsonl(TRIAL_LOG, record)
    write_trial_summary(load_jsonl(TRIAL_LOG))
    add_manifest("astis.py trial-log", TRIAL_LOG, "trial", f"Logged {trial_id}")
    print(f"logged {trial_id}")
    return 0


def cmd_trial_summary(_: argparse.Namespace) -> int:
    records = load_jsonl(TRIAL_LOG)
    write_trial_summary(records)
    by_task: dict[str, int] = {}
    for record in records:
        by_task[record.get("task_id", "unknown")] = by_task.get(record.get("task_id", "unknown"), 0) + 1
    for task, count in sorted(by_task.items()):
        print(f"{task}: total={count}")
    print(f"wrote {rel(TRIAL_SUMMARY)}")
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    cmd_init(argparse.Namespace())
    state = load_state()
    print(f"project: {ROOT}")
    print(f"active task: {state.get('active_task')}")
    print(f"last check: {state.get('last_check')}")
    if not is_git_worktree():
        print("git: not a repository")
        return 0
    return run(["git", "status", "--short"])


def cmd_harness_reconcile(args: argparse.Namespace) -> int:
    frontier = harness.reconcile_frontier(ROOT)
    if args.write_state:
        state = load_state()
        state["version"] = 2
        state["active_task"] = frontier["active_program"]
        state["task_relationship"] = frontier["task_relationship"]
        state["frontier"] = {
            "reconciled_at": frontier["generated_at"],
            "selected_ready_leaf": (
                frontier["selected_ready_leaf"]["node_id"]
                if frontier["selected_ready_leaf"] else None
            ),
            "status": {
                node["node_id"]: node["local_status"] for node in frontier["nodes"]
            },
        }
        save_state(state)
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = ROOT / output
        harness.atomic_write_text(
            output,
            json.dumps(frontier, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        )
    if args.json:
        print(json.dumps(frontier, indent=2, ensure_ascii=False))
    else:
        print(f"active program: {frontier['active_program']}")
        for node in frontier["nodes"]:
            print(f"{node['local_status']:8s} {node['node_id']}: {node['label']}")
        selected = frontier["selected_ready_leaf"]
        print("selected ready leaf: " + (selected["node_id"] if selected else "none"))
    return 0


def cmd_harness_recover(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if not path.is_absolute():
        path = ROOT / path
    if args.run_events:
        interrupted = harness.recover_run_events(path)
        print(f"closed interrupted executions: {len(interrupted)}")
        for execution_id in interrupted:
            print(f"- {execution_id}")
    else:
        records, recovered = harness.recover_jsonl(path)
        print(f"records: {len(records)}")
        print(f"truncated interrupted tail: {str(recovered).lower()}")
    return 0


def cmd_harness_test(_: argparse.Namespace) -> int:
    return run([sys.executable, "-m", "unittest", "discover", "-s", "tools/tests", "-v"])


def cmd_proof_diagnostics(_: argparse.Namespace) -> int:
    print(json.dumps(lean_diagnostics(), indent=2, sort_keys=True))
    return 0


def cmd_site_build(args: argparse.Namespace) -> int:
    """Generate the Registry-driven Blueprint-style textbook website."""
    import astis_site

    output = Path(args.output).resolve() if args.output else astis_site.DEFAULT_OUTPUT
    data = astis_site.build_site(output)
    print(
        f"built {output}: {len(data['chapters'])} chapters, "
        f"{data['registry']['compiled_local_leaves']} compiled local leaves, "
        f"{len(data['declarations'])} Registry cards"
    )
    return 0


def cmd_site_check(args: argparse.Namespace) -> int:
    """Validate site links, declaration resolution, and status consistency."""
    import astis_site

    output = Path(args.output).resolve() if args.output else astis_site.DEFAULT_OUTPUT
    if args.rebuild or not output.exists():
        astis_site.build_site(output)
    errors = astis_site.validate_site(output)
    if errors:
        print("ASTIS site check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    data = json.loads((output / "data" / "site-data.json").read_text(encoding="utf-8"))
    print(
        f"ASTIS site check passed: {len(data['chapters'])} chapters, "
        f"{data['registry']['compiled_local_leaves']} compiled local leaves"
    )
    return 0


def cmd_chewi_source_check(args: argparse.Namespace) -> int:
    """Validate the canonical Chewi edition, TOC, and semantic source anchors."""
    import astis_source

    return astis_source.command_check(args)


def cmd_chapter_1_check(args: argparse.Namespace) -> int:
    """Validate item-level Chapter 1 source, Lean, test, and Registry evidence."""
    import astis_site
    import astis_source

    matrix_raw = astis_site.load_json(astis_site.CONTENT / "chapter_1_completion_matrix.json")
    source_entries = astis_site.load_json(astis_site.CONTENT / "source_correspondence.json")
    if not isinstance(matrix_raw, dict) or not isinstance(source_entries, list):
        print("Chapter 1 evidence check failed: invalid content schema", file=sys.stderr)
        return 1

    matrix = astis_site.expand_chapter_1_matrix(matrix_raw, source_entries)
    entries, _ = astis_site.enrich_entries(astis_site.parse_registry())
    _, declarations = astis_site.scan_project_sources()
    declarations_by_name = {
        declaration.full_name: declaration for declaration in declarations
    }
    errors = astis_site.validate_chapter_1_evidence(
        {
            "chapter_1_completion_matrix": matrix,
            "source_correspondence": source_entries,
        },
        entries,
        declarations_by_name,
        require_complete=args.require_complete,
    )
    source_errors, _ = astis_source.validate_source_contract()
    errors.extend(source_errors)
    registry_count = sum(entry.is_blue for entry in entries)
    tests_baseline = astis_site.test_registry_count()
    if tests_baseline is None:
        errors.append("Tests/Basic.lean has no compiled Registry-count baseline")
    elif registry_count != tests_baseline:
        errors.append(
            f"compiled Registry count {registry_count} != Tests baseline {tests_baseline}"
        )
    report = astis_site.chapter_1_completion_report(matrix)
    print(
        "Chapter 1 evidence: "
        f"{report['complete']} complete, {report['partial']} partial, "
        f"{report['planned']} planned, {report['blocked']} blocked, "
        f"{report['external']} external / {report['total']} total"
    )
    if errors:
        print("Chapter 1 evidence check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    mode = "strict closure" if args.require_complete else "item-level integrity"
    print(f"Chapter 1 {mode} check passed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ASTIS workflow helper")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init").set_defaults(func=cmd_init)
    sub.add_parser("check").set_defaults(func=cmd_check)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("proof-diagnostics").set_defaults(func=cmd_proof_diagnostics)
    sub.add_parser("list-literature").set_defaults(func=cmd_list_literature)
    sub.add_parser("list-tasks").set_defaults(func=cmd_list_tasks)
    sub.add_parser("next-task").set_defaults(func=cmd_next_task)

    harness_reconcile = sub.add_parser("harness-reconcile")
    harness_reconcile.add_argument("--json", action="store_true")
    harness_reconcile.add_argument("--output", default="")
    harness_reconcile.add_argument("--write-state", action="store_true")
    harness_reconcile.set_defaults(func=cmd_harness_reconcile)

    harness_recover = sub.add_parser("harness-recover")
    harness_recover.add_argument("path")
    harness_recover.add_argument("--run-events", action="store_true")
    harness_recover.set_defaults(func=cmd_harness_recover)

    sub.add_parser("harness-test").set_defaults(func=cmd_harness_test)

    route_attempt = sub.add_parser("route-attempt")
    route_attempt.add_argument("--task", required=True)
    route_attempt.add_argument("--leaf", required=True)
    route_attempt.add_argument("--target-statement", required=True)
    route_attempt.add_argument("--missing-property", required=True)
    route_attempt.add_argument("--assumption", action="append", default=[])
    route_attempt.add_argument("--mathlib-candidate", action="append", default=[])
    route_attempt.add_argument("--compiler-error-class", required=True)
    route_attempt.add_argument("--candidate", required=True)
    route_attempt.add_argument("--exact-subgoal", required=True)
    route_attempt.add_argument("--compiled-declaration", action="append", default=[])
    route_attempt.set_defaults(func=cmd_route_attempt)

    context_pack = sub.add_parser("write-context-pack")
    context_pack.add_argument("task")
    context_pack.add_argument("--cycle", type=int, default=1)
    context_pack.add_argument("--output", default="")
    context_pack.set_defaults(func=cmd_write_context_pack)

    sald_todo = sub.add_parser("update-sald-todo")
    sald_todo.add_argument("--cycle", type=int, default=0)
    sald_todo.set_defaults(func=cmd_update_sald_todo)

    sald_memory = sub.add_parser("update-sald-paper-memory")
    sald_memory.add_argument("--cycle", type=int, default=0)
    sald_memory.set_defaults(func=cmd_update_sald_paper_memory)

    sald_finalize = sub.add_parser("finalize-sald-cycle")
    sald_finalize.add_argument("--cycle", type=int, default=0)
    sald_finalize.add_argument("--run-check", action="store_true")
    sald_finalize.set_defaults(func=cmd_finalize_sald_cycle)

    memory_refresh = sub.add_parser("memory-refresh")
    memory_refresh.add_argument("task")
    memory_refresh.add_argument("--cycle", type=int, default=0)
    memory_refresh.add_argument("--run-id", default="latest")
    memory_refresh.set_defaults(func=cmd_memory_refresh)

    sub.add_parser("lemma-dag-refresh").set_defaults(func=cmd_lemma_dag_refresh)
    sub.add_parser("module-graph-refresh").set_defaults(func=cmd_module_graph_refresh)

    site_build = sub.add_parser("site-build")
    site_build.add_argument("--output", default="")
    site_build.set_defaults(func=cmd_site_build)

    site_check = sub.add_parser("site-check")
    site_check.add_argument("--output", default="")
    site_check.add_argument("--rebuild", action="store_true")
    site_check.set_defaults(func=cmd_site_check)

    chewi_source_check = sub.add_parser("chewi-source-check")
    chewi_source_check.add_argument("--pdf", default="")
    chewi_source_check.add_argument("--require-pdf", action="store_true")
    chewi_source_check.set_defaults(func=cmd_chewi_source_check)

    chapter_1_check = sub.add_parser("chapter-1-check")
    chapter_1_check.add_argument("--require-complete", action="store_true")
    chapter_1_check.set_defaults(func=cmd_chapter_1_check)

    zh_summary = sub.add_parser("cycle-zh-summary")
    zh_summary.add_argument("task")
    zh_summary.add_argument("--cycle", type=int, default=0)
    zh_summary.add_argument("--run-id", default="latest")
    zh_summary.set_defaults(func=cmd_cycle_zh_summary)

    pro_prompt = sub.add_parser("cycle-pro-prompt")
    pro_prompt.add_argument("task")
    pro_prompt.add_argument("--cycle", type=int, default=0)
    pro_prompt.add_argument("--run-id", default="latest")
    pro_prompt.set_defaults(func=cmd_cycle_pro_prompt)

    article_update = sub.add_parser("project-article-update")
    article_update.add_argument("task")
    article_update.add_argument("--cycle", type=int, default=0)
    article_update.add_argument("--run-id", default="latest")
    article_update.set_defaults(func=cmd_project_article_update)

    efficiency = sub.add_parser("efficiency-report")
    efficiency.add_argument("--log", default="")
    efficiency.add_argument("--output", default="")
    efficiency.add_argument("--json", action="store_true")
    efficiency.set_defaults(func=cmd_efficiency_report)

    blueprint = sub.add_parser("blueprint-status")
    blueprint.add_argument("task")
    blueprint.add_argument("--output", default="")
    blueprint.set_defaults(func=cmd_blueprint_status)

    blueprint_refresh = sub.add_parser("blueprint-refresh")
    blueprint_refresh.add_argument("task")
    blueprint_refresh.add_argument("--output", default="")
    blueprint_refresh.set_defaults(func=cmd_blueprint_refresh)

    source_index = sub.add_parser("source-index")
    source_index.add_argument("task")
    source_index.set_defaults(func=cmd_source_index)

    run_cycle = sub.add_parser("run-cycle")
    run_cycle.add_argument("task")
    run_cycle.add_argument("--cycle", type=int, default=1)
    run_cycle.add_argument("--lower-count", type=int, default=2)
    run_cycle.add_argument("--run-id", default="")
    run_cycle.add_argument("--upper-panel", action="store_true")
    run_cycle.add_argument("--middle-panel", action="store_true")
    run_cycle.add_argument("--reviewer-waste", action="store_true")
    run_cycle.set_defaults(func=cmd_run_cycle)

    sleep_run = sub.add_parser("sleep-run")
    sleep_run.add_argument("task")
    sleep_run.add_argument("--cycles", type=int, default=1)
    sleep_run.add_argument("--lower-count", type=int, default=2)
    sleep_run.add_argument("--upper-panel", action="store_true")
    sleep_run.add_argument("--middle-panel", action="store_true")
    sleep_run.add_argument("--reviewer-waste", action="store_true")
    sleep_run.add_argument("--parallel-lower", action="store_true", help="run lower prompts concurrently after middle synthesis")
    sleep_run.add_argument("--agent-cmd", default="")
    sleep_run.add_argument("--execute", action="store_true")
    sleep_run.add_argument("--dry-run", action="store_true")
    sleep_run.add_argument("--check-each-cycle", action="store_true")
    sleep_run.add_argument("--skip-reviewer", action="store_true")
    sleep_run.set_defaults(func=cmd_sleep_run)

    sleep_window = sub.add_parser("sleep-run-window")
    sleep_window.add_argument("task")
    sleep_window.add_argument("--hours", type=float, default=6.0)
    sleep_window.add_argument("--agent-hours-budget", type=float, default=0.0)
    sleep_window.add_argument("--max-cycles", type=int, default=999)
    sleep_window.add_argument("--start-cycle", type=int, default=0)
    sleep_window.add_argument("--guard-minutes", type=float, default=0.0)
    sleep_window.add_argument("--lower-count", type=int, default=2)
    sleep_window.add_argument("--upper-panel", action="store_true", help="run upper specialists in every inner cycle")
    sleep_window.add_argument("--middle-panel", action="store_true", help="run middle specialists in every inner cycle")
    sleep_window.add_argument("--reviewer-waste", action="store_true", help="run the waste reviewer in every inner cycle")
    sleep_window.add_argument("--upper-panel-final", action="store_true", help="run upper specialists in the final audit cycle")
    sleep_window.add_argument("--middle-panel-final", action="store_true", help="run middle specialists in the final audit cycle")
    sleep_window.add_argument("--reviewer-waste-final", action="store_true", help="run progress-economics reviewer in the final audit cycle")
    sleep_window.add_argument("--parallel-lower", action="store_true", help="run lower prompts concurrently after middle synthesis")
    sleep_window.add_argument("--agent-cmd", default="")
    sleep_window.add_argument("--execute", action="store_true")
    sleep_window.add_argument("--dry-run", action="store_true")
    sleep_window.add_argument("--check-each-cycle", action="store_true")
    sleep_window.add_argument("--skip-reviewer", action="store_true")
    sleep_window.add_argument("--after-latex", action="store_true")
    sleep_window.set_defaults(func=cmd_sleep_run_window)

    launch = sub.add_parser("launch-sald-6h")
    launch.add_argument("--hours", type=float, default=6.0, help="active agent budget in hours")
    launch.add_argument("--wall-hours", type=float, default=24.0, help="wall-clock safety window for an active-agent-budget run")
    launch.add_argument("--max-cycles", type=int, default=64)
    launch.add_argument("--lower-count", type=int, default=3)
    launch.add_argument("--start-cycle", type=int, default=0)
    launch.add_argument("--upper-panel-inner", action="store_true")
    launch.add_argument("--middle-panel-inner", action="store_true")
    launch.add_argument("--reviewer-waste-inner", action="store_true")
    launch.add_argument("--upper-panel-final", dest="upper_panel_final", action="store_true", default=True)
    launch.add_argument("--no-upper-panel-final", dest="upper_panel_final", action="store_false")
    launch.add_argument("--middle-panel-final", dest="middle_panel_final", action="store_true", default=True)
    launch.add_argument("--no-middle-panel-final", dest="middle_panel_final", action="store_false")
    launch.add_argument("--reviewer-waste-final", dest="reviewer_waste_final", action="store_true", default=True)
    launch.add_argument("--no-reviewer-waste-final", dest="reviewer_waste_final", action="store_false")
    launch.add_argument("--parallel-lower", dest="parallel_lower", action="store_true", default=True)
    launch.add_argument("--no-parallel-lower", dest="parallel_lower", action="store_false")
    launch.add_argument("--after-latex", dest="after_latex", action="store_true", default=True)
    launch.add_argument("--no-after-latex", dest="after_latex", action="store_false")
    launch.add_argument("--skip-reviewer", action="store_true")
    launch.set_defaults(func=cmd_launch_six_hour_sald)

    launch_log_concave = sub.add_parser("launch-log-concave-6h")
    launch_log_concave.add_argument("--hours", type=float, default=6.0, help="active agent budget in hours")
    launch_log_concave.add_argument("--wall-hours", type=float, default=24.0, help="wall-clock safety window for an active-agent-budget run")
    launch_log_concave.add_argument("--max-cycles", type=int, default=64)
    launch_log_concave.add_argument("--lower-count", type=int, default=3)
    launch_log_concave.add_argument("--start-cycle", type=int, default=0)
    launch_log_concave.add_argument("--upper-panel-inner", action="store_true")
    launch_log_concave.add_argument("--middle-panel-inner", action="store_true")
    launch_log_concave.add_argument("--reviewer-waste-inner", action="store_true")
    launch_log_concave.add_argument("--upper-panel-final", dest="upper_panel_final", action="store_true", default=True)
    launch_log_concave.add_argument("--no-upper-panel-final", dest="upper_panel_final", action="store_false")
    launch_log_concave.add_argument("--middle-panel-final", dest="middle_panel_final", action="store_true", default=True)
    launch_log_concave.add_argument("--no-middle-panel-final", dest="middle_panel_final", action="store_false")
    launch_log_concave.add_argument("--reviewer-waste-final", dest="reviewer_waste_final", action="store_true", default=True)
    launch_log_concave.add_argument("--no-reviewer-waste-final", dest="reviewer_waste_final", action="store_false")
    launch_log_concave.add_argument("--parallel-lower", dest="parallel_lower", action="store_true", default=True)
    launch_log_concave.add_argument("--no-parallel-lower", dest="parallel_lower", action="store_false")
    launch_log_concave.add_argument("--after-latex", action="store_true")
    launch_log_concave.add_argument("--skip-reviewer", action="store_true")
    launch_log_concave.set_defaults(func=cmd_launch_six_hour_chewi)

    export = sub.add_parser("export-latex")
    export.add_argument("--task", default="ASTIS-SALD-001")
    export.add_argument("--skip-technical-report", action="store_true")
    export.set_defaults(func=cmd_export_latex)

    report_export = sub.add_parser("export-technical-report")
    report_export.add_argument("--task", default="ASTIS-SALD-001")
    report_export.add_argument("--report-root", default=str(TECH_REPORT_ROOT))
    report_export.set_defaults(func=cmd_export_technical_report)

    note = sub.add_parser("agent-note")
    note.add_argument("run")
    note.add_argument("--role", required=True)
    note.add_argument("--message", required=True)
    note.set_defaults(func=cmd_agent_note)

    trial = sub.add_parser("trial-log")
    trial.add_argument("--task", required=True)
    trial.add_argument("--role", required=True)
    trial.add_argument("--kind", choices=TRIAL_KINDS, required=True)
    trial.add_argument("--status", choices=TRIAL_STATUSES, required=True)
    trial.add_argument("--lean-gate", default="not-run")
    trial.add_argument("--artifact", default="")
    trial.add_argument("--changed-file", action="append")
    trial.add_argument("--from-git", action="store_true")
    trial.add_argument("--trial-id")
    trial.add_argument("--notes", default="")
    trial.add_argument("--feedback-json", default="")
    trial.add_argument("--feedback-field", action="append")
    trial.set_defaults(func=cmd_trial_log)

    sub.add_parser("trial-summary").set_defaults(func=cmd_trial_summary)
    return parser


def enforce_repository_lean_toolchain() -> str:
    """Make the repository pin authoritative over an inherited user override."""
    toolchain = LEAN_TOOLCHAIN_FILE.read_text(encoding="utf-8").strip()
    if not toolchain:
        raise RuntimeError("lean-toolchain is empty")
    os.environ["ELAN_TOOLCHAIN"] = toolchain
    return toolchain


def main(argv: list[str]) -> int:
    enforce_repository_lean_toolchain()
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
