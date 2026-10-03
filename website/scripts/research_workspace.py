#!/usr/bin/env python3
"""Build source-grounded research workspaces and portable agent packets.

The canonical mathematical content remains
``website/content/samplewiki_companion_frontiers.json``.  This module projects
that content into an interactive site payload and downloadable artifacts; it
does not create proof status or theorem declarations.
"""

from __future__ import annotations

import hashlib
import json
import zipfile
from html import escape
from pathlib import Path

import samplewiki_companions


ROOT = Path(__file__).resolve().parents[2]
MCP_SOURCE = ROOT / "integrations" / "samplinglib-research-mcp"
DATA_REL = "data/research-workspaces.json"
MCP_DOWNLOAD = "downloads/samplinglib-research-mcp.zip"


def step_id(theorem_id: str, index: int) -> str:
    return f"{theorem_id}-step-{index + 1:02d}"


def build_payload(model: dict[str, object] | None = None) -> dict[str, object]:
    """Project companion metadata into a bounded agent/reader interface."""
    source = samplewiki_companions.load() if model is None else model
    samplewiki_companions.validate_data(source)
    workspaces: list[dict[str, object]] = []
    sources = source["sources"]
    for row in source["cases"]:
        source_records = [sources[source_id] for source_id in row["source_ids"]]
        theorems: list[dict[str, object]] = []
        for theorem in row["theorems"]:
            steps: list[dict[str, object]] = []
            for index, step in enumerate(theorem["steps"]):
                support = list(step.get("compiled_support", []))
                steps.append(
                    {
                        "id": step_id(theorem["id"], index),
                        "title": step["title"],
                        "formula": step["formula"],
                        "explanation": step["text"],
                        "source_anchor": step["anchor"],
                        "status": "compiled-support-only" if support else "open",
                        "compiled_support": support,
                        "support_note": step.get(
                            "support_note",
                            "No ASTIS declaration is attached to this step yet.",
                        ),
                    }
                )
            theorems.append(
                {
                    "id": theorem["id"],
                    "title": theorem["title"],
                    "source_anchor": theorem["anchor"],
                    "statement": theorem["statement"],
                    "assumptions": list(theorem["assumptions"]),
                    "formula": theorem["formula"],
                    "boundary": theorem["boundary"],
                    "status": "planned",
                    "steps": steps,
                }
            )
        slug = row["slug"]
        workspaces.append(
            {
                "id": row["id"],
                "slug": slug,
                "title": row["title"],
                "role": row["role"],
                "status": row["status"],
                "source_records": [
                    {
                        "id": source_id,
                        "title": record["title"],
                        "url": record["url"],
                        "version": record["version"],
                        "authors": record["authors"],
                    }
                    for source_id, record in zip(
                        row["source_ids"], source_records, strict=True
                    )
                ],
                "source_reader": (
                    "../example-cases/samplewiki/companions/" + slug + ".html"
                ),
                "setting": row.get("setting", source["setting"]),
                "reader_guide": list(row.get("reader_guide", [])),
                "theorems": theorems,
                "ledger": row.get("bookkeeping"),
                "downloads": {
                    "json": f"../downloads/{slug}-research-context.json",
                    "markdown": f"../downloads/{slug}-research-context.md",
                    "bundle": f"../downloads/{slug}-research-pack.zip",
                    "mcp_app": "../" + MCP_DOWNLOAD,
                },
                "evidence_contract": {
                    "source_context": "pinned",
                    "ai_output": "unverified-candidate-only",
                    "lean_compilation": "separate-exact-snippet-gate",
                    "source_fidelity": "independent-review-required",
                    "blue_status": "ASTIS-owned, compiled, tested, reviewed and admitted only",
                },
            }
        )
    return {
        "schema_version": "1.0",
        "project": "Auto-Sampling-Theory-In-Sleep",
        "library": "Samplinglib",
        "generated_from": "website/content/samplewiki_companion_frontiers.json",
        "workspaces": workspaces,
    }


def workspace_markdown(workspace: dict[str, object]) -> str:
    lines = [
        f"# {workspace['title']} — ASTIS research workspace",
        "",
        f"Workspace id: `{workspace['id']}`",
        "",
        str(workspace["role"]),
        "",
        "## Evidence boundary",
        "",
        "- Source context is pinned by the companion metadata.",
        "- AI explanations and generated Lean are unverified candidates.",
        "- Lean compilation checks only the exact submitted snippet.",
        "- Source fidelity and blue status require independent ASTIS review and admission.",
        "",
    ]
    for source in workspace["source_records"]:
        lines.extend(
            [
                "## Primary source",
                "",
                f"- {source['title']} ({source['version']}): {source['url']}",
                f"- Authors: {', '.join(source['authors'])}",
                "",
            ]
        )
    for theorem in workspace["theorems"]:
        lines.extend(
            [
                f"## {theorem['title']}",
                "",
                f"Source: {theorem['source_anchor']}",
                "",
                theorem["statement"],
                "",
                "```latex",
                theorem["formula"],
                "```",
                "",
                "Assumptions:",
                "",
                *[f"- {item}" for item in theorem["assumptions"]],
                "",
                "Proof route:",
                "",
            ]
        )
        for index, step in enumerate(theorem["steps"], 1):
            lines.extend(
                [
                    f"### {index}. {step['title']}",
                    "",
                    f"Source: {step['source_anchor']}",
                    "",
                    "```latex",
                    step["formula"],
                    "```",
                    "",
                    step["explanation"],
                    "",
                    f"Lean status: `{step['status']}`.",
                    "",
                ]
            )
            if step["compiled_support"]:
                lines.extend(
                    [
                        "Compiled reusable support:",
                        "",
                        *[f"- `{name}`" for name in step["compiled_support"]],
                        "",
                    ]
                )
        lines.extend(["Strict boundary:", "", theorem["boundary"], ""])
    ledger = workspace.get("ledger")
    if ledger:
        lines.extend([f"## {ledger['title']}", "", ledger["intro"], ""])
        for item in ledger["error_flow"]:
            lines.extend(
                [
                    f"- **{item['stage']}** — Input: {item['input']} Output: {item['output']} Charge: {item['charge']}",
                ]
            )
        lines.extend(["", "Ledger boundary:", "", ledger["boundary"], ""])
    lines.extend(
        [
            "## Suggested agent instruction",
            "",
            "Use the pinned source statement and explicit assumptions above. Work on one selected proof step at a time. Separate ASTIS-owned compiled declarations from Mathlib or external facts. Treat every generated explanation and Lean fragment as unverified until the exact snippet compiles and an independent source-fidelity review accepts the correspondence. Never infer whole-paper completion from a reusable support lemma.",
            "",
        ]
    )
    return "\n".join(str(line) for line in lines)


def standalone_html(workspace: dict[str, object]) -> str:
    theorem_cards = []
    for theorem in workspace["theorems"]:
        steps = "".join(
            "<li>"
            f"<h3>{escape(step['title'])}</h3>"
            f"<pre>{escape(step['formula'])}</pre>"
            f"<p>{escape(step['explanation'])}</p>"
            f"<p><strong>Source:</strong> {escape(step['source_anchor'])}</p>"
            f"<p><strong>Lean status:</strong> {escape(step['status'])}</p>"
            "</li>"
            for step in theorem["steps"]
        )
        theorem_cards.append(
            "<section>"
            f"<h2>{escape(theorem['title'])}</h2>"
            f"<p>{escape(theorem['statement'])}</p>"
            f"<pre>{escape(theorem['formula'])}</pre>"
            f"<ol>{steps}</ol>"
            f"<aside><strong>Boundary:</strong> {escape(theorem['boundary'])}</aside>"
            "</section>"
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(workspace['title'])} — ASTIS research workspace</title>
<style>body{{font:17px/1.6 system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;color:#172033}}section{{border-top:1px solid #ccd3df;padding:1.5rem 0}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f9;padding:1rem;border-left:4px solid #526ba6}}li{{margin:1.2rem 0}}aside{{background:#fff3e6;padding:1rem}}.boundary{{border:1px solid #b33;padding:1rem;background:#fff5f5}}</style></head>
<body><header><p>Auto-Sampling-Theory-In-Sleep · Samplinglib</p><h1>{escape(workspace['title'])}</h1><p>{escape(workspace['role'])}</p></header>
<div class="boundary"><strong>Evidence boundary.</strong> AI output is unverified; compilation and independent source review remain separate.</div>
{''.join(theorem_cards)}</body></html>"""


def _support_sources(output: Path, workspace: dict[str, object]) -> list[dict[str, str]]:
    data = json.loads((output / "data/site-data.json").read_text(encoding="utf-8"))
    by_name = {row["full_name"]: row for row in data["declarations"]}
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for theorem in workspace["theorems"]:
        for step in theorem["steps"]:
            for name in step["compiled_support"]:
                declaration = by_name.get(name)
                if not declaration:
                    raise ValueError(f"Workspace support declaration is not indexed: {name}")
                if declaration.get("registry_status") != "formalizedLocal":
                    raise ValueError(f"Workspace support is not compiled-local: {name}")
                source_file = declaration.get("source_file", "")
                if not source_file or source_file in seen:
                    continue
                path = ROOT / source_file
                if not path.is_file():
                    raise ValueError(f"Workspace support source is missing: {source_file}")
                seen.add(source_file)
                result.append(
                    {
                        "path": source_file,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    }
                )
    return result


def _write_workspace_bundle(
    output: Path, workspace: dict[str, object], json_text: str, markdown: str
) -> None:
    downloads = output / "downloads"
    slug = workspace["slug"]
    support_sources = _support_sources(output, workspace)
    manifest = {
        "schema_version": "1.0",
        "workspace_id": workspace["id"],
        "source_metadata": "website/content/samplewiki_companion_frontiers.json",
        "compiled_support_modules": support_sources,
        "boundary": "Included Lean modules are compiled reusable support only; the source theorem may remain open.",
    }
    with zipfile.ZipFile(
        downloads / f"{slug}-research-pack.zip", "w", zipfile.ZIP_DEFLATED
    ) as archive:
        archive.writestr("README.md", markdown)
        archive.writestr("workspace.json", json_text)
        archive.writestr("workspace.md", markdown)
        archive.writestr("workspace.html", standalone_html(workspace))
        archive.writestr("MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
        for filename in ("lean-toolchain", "lake-manifest.json", "NOTICE.md"):
            path = ROOT / filename
            if path.is_file():
                archive.write(path, filename)
        for source in support_sources:
            archive.write(ROOT / source["path"], "lean/" + source["path"])


def _write_mcp_bundle(output: Path, payload_text: str) -> None:
    if not MCP_SOURCE.is_dir():
        raise ValueError("Samplinglib research MCP source package is missing")
    target = output / MCP_DOWNLOAD
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(MCP_SOURCE.rglob("*")):
            if path.is_file() and "node_modules" not in path.parts:
                archive.write(path, path.relative_to(MCP_SOURCE).as_posix())
        archive.writestr("data/research-workspaces.json", payload_text)


def enrich_site(output: Path) -> None:
    payload = build_payload()
    data_dir = output / "data"
    downloads = output / "downloads"
    data_dir.mkdir(parents=True, exist_ok=True)
    downloads.mkdir(parents=True, exist_ok=True)
    payload_text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    (output / DATA_REL).write_text(payload_text, encoding="utf-8", newline="\n")
    for workspace in payload["workspaces"]:
        json_text = json.dumps(workspace, indent=2, ensure_ascii=False) + "\n"
        markdown = workspace_markdown(workspace)
        slug = workspace["slug"]
        (downloads / f"{slug}-research-context.json").write_text(
            json_text, encoding="utf-8", newline="\n"
        )
        (downloads / f"{slug}-research-context.md").write_text(
            markdown, encoding="utf-8", newline="\n"
        )
        _write_workspace_bundle(output, workspace, json_text, markdown)
    _write_mcp_bundle(output, payload_text)


def validate_site(output: Path) -> list[str]:
    errors: list[str] = []
    live = (output / "live/index.html").read_text(encoding="utf-8")
    for marker in (
        "data-research-workspace",
        "data-rw-steps",
        "data-rw-action=\"explain\"",
        "samplinglib-research-mcp.zip",
        "AI explanation — unverified",
    ):
        if marker not in live:
            errors.append(f"Live research workspace is missing {marker}")
    path = output / DATA_REL
    if not path.is_file():
        return errors + ["Missing research workspace data"]
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = {row["id"] for row in samplewiki_companions.load()["cases"]}
    actual = {row["id"] for row in payload.get("workspaces", [])}
    if actual != expected:
        errors.append("Research workspaces drift from companion source cases")
    for workspace in payload.get("workspaces", []):
        for key in ("json", "markdown", "bundle"):
            relative = workspace["downloads"][key].removeprefix("../")
            if not (output / relative).is_file():
                errors.append(f"Missing workspace download: {relative}")
        bundle = output / workspace["downloads"]["bundle"].removeprefix("../")
        if bundle.is_file():
            with zipfile.ZipFile(bundle) as archive:
                names = set(archive.namelist())
                for required in (
                    "README.md",
                    "workspace.json",
                    "workspace.html",
                    "MANIFEST.json",
                ):
                    if required not in names:
                        errors.append(f"{bundle.name}: missing {required}")
    mcp = output / MCP_DOWNLOAD
    if not mcp.is_file():
        errors.append("Missing downloadable ChatGPT/MCP research app")
    else:
        with zipfile.ZipFile(mcp) as archive:
            names = set(archive.namelist())
            for required in (
                "README.md",
                "package.json",
                "server.mjs",
                "public/workspace-widget.html",
                "data/research-workspaces.json",
            ):
                if required not in names:
                    errors.append(f"MCP app bundle is missing {required}")
    if "OPENAI_API_KEY" in live or "sk-" in live:
        errors.append("Live page must not expose API credentials")
    return errors
