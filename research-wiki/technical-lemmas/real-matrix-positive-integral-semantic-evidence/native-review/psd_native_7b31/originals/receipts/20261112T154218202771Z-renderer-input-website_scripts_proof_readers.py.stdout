"""Mathematics-first readers for shared prerequisites, never source-completion flags.

Prose is authored once; declarations, complete code, status and source verdicts
are resolved from the existing source inventory and canonical audit records.
"""
from __future__ import annotations

import html
import json
import posixpath
import re
from pathlib import Path

import astis_site as base
import source_lineage
import inline_lean

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "website/content/proof_readers.json"
START = "<!-- ASTIS_PROOF_READERS_START -->"
END = "<!-- ASTIS_PROOF_READERS_END -->"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_items() -> list[dict]:
    items = read_json(CONTENT)
    seen = set()
    for item in items:
        if not re.fullmatch(r"[a-z0-9-]+", item["id"]) or item["id"] in seen:
            raise ValueError("Invalid or duplicate proof-reader id")
        seen.add(item["id"])
        for key in ("title", "statement", "formula", "assumptions", "steps",
                    "declarations", "astis_dependencies", "mathlib_dependencies",
                    "boundary", "sources", "cell", "audit", "test", "entry_pages"):
            if not item.get(key):
                raise ValueError(f"{item['id']}: missing {key}")
        for step in item["steps"]:
            if not all(step.get(k) for k in ("title", "text", "formula", "lean")):
                raise ValueError(f"{item['id']}: incomplete proof step")
        units = item.get('theorems', [])
        if {u['declaration'] for u in units} != set(item['declarations']):
            raise ValueError(f"{item['id']}: every declaration needs its own theorem unit")
        for unit in units:
            for key in ('title', 'statement', 'formula', 'assumptions', 'steps',
                        'proof_intro', 'lean_statement', 'lean_proof'):
                if not unit.get(key):
                    raise ValueError(f"{item['id']}: theorem unit missing {key}")
    return items


def evidence(item: dict, data: dict) -> dict:
    names = {row["full_name"]: row for row in data["declarations"]}
    for name in item["declarations"] + item["astis_dependencies"]:
        if name not in names:
            raise ValueError(f"{item['id']}: unknown declaration {name}")
    cell = read_json(ROOT / "research-wiki/frontier-cells" / (item["cell"] + ".json"))
    audits = read_json(ROOT / "research-wiki/semantic-roundtrip/registry.json")["audits"]
    audit = next(row for row in audits if row["id"] == item["audit"])
    declarations = [names[name] for name in item["declarations"]]
    return {
        "declarations": declarations,
        "compiled": bool(data["gate"]["passed"]) and all(
            d["local_status"] == "Compiled" and not d["has_placeholder"] for d in declarations),
        "registry_entries": sum(bool(d["registry_status"]) for d in declarations),
        "cell_status": cell["status"],
        "source_state": audit["state"],
        "source_verdict": audit["verdict"],
        "source_review": audit["source_review"]["state"],
    }


def relative_link(page: str, target: str) -> str:
    return posixpath.relpath(target, posixpath.dirname(page))


def render(item: dict, data: dict) -> str:
    ev = evidence(item, data)
    names = {d["full_name"]: d for d in data["declarations"]}
    rel = f"proofs/{item['id']}.html"

    def decl_link(name: str) -> str:
        return f'<a href="../{esc(names[name]["page"])}"><code>{esc(name)}</code></a>'

    units = []
    for unit in item['theorems']:
        steps = ''.join(
            f'<div class="proof-reader-step"><h4>{i}. {esc(s["title"])}</h4>'
            f'<p>{esc(s["text"])}</p><div class="proof-reader-equation">\\[{esc(s["formula"])}\\]</div>'
            f'<details><summary>How this step appears in Lean</summary><p>{esc(s["lean"])}</p></details></div>'
            for i, s in enumerate((item['steps'][n] for n in unit['steps']), 1)
        )
        units.append(
            f'<section class="proof-reader-theorem" data-theorem="{esc(unit["declaration"])}">'
            f'<h2>{esc(unit["title"])}</h2><h3>Statement</h3><p>{esc(unit["statement"])}</p>'
            f'<div class="proof-reader-equation">\\[{esc(unit["formula"])}\\]</div>'
            + base.list_html(unit['assumptions'])
            + inline_lean.disclosure(unit['declaration'], role='statement', explanation=unit['lean_statement'], page=rel)
            + f'<h3>Mathematical proof</h3><p>{esc(unit["proof_intro"])}</p>' + steps
            + inline_lean.disclosure(unit['declaration'], role='proof', explanation=unit['lean_proof'], page=rel, helpers=tuple(unit.get('helpers', [])))
            + '</section>'
        )
    sources = "".join(f'<li><a href="{esc(s["url"])}">{esc(s["label"])}</a> — {esc(s["scope"])}</li>' for s in item["sources"])
    mathlib = "".join(f'<li><a href="{esc(d["url"])}"><code>{esc(d["name"])}</code></a> — {esc(d["role"])}</li>' for d in item["mathlib_dependencies"])
    color = "blue" if ev["compiled"] else "gray"
    compile_label = "ASTIS-owned · compiled" if ev["compiled"] else "Current checkout compilation not certified"
    body = f'''<article class="proof-reader">
<p><a href="index.html">Shared proof readers</a></p>
<header><div class="eyebrow">Samplinglib · shared mathematical prerequisite</div><h1>{esc(item['title'])}</h1>
<p class="lede">{esc(item['purpose'])}</p></header>
{''.join(units)}
<section id="boundary" class="proof-reader-boundary"><h2>What is still not proved by this result</h2>{base.list_html(item['boundary'])}</section>
<section id="dependencies"><h2>Proof dependencies</h2>
<details><summary>Declarations and reuse: ASTIS versus Mathlib</summary>
<h3>Results proved here by ASTIS</h3><ul>{''.join('<li>'+decl_link(n)+'</li>' for n in item['declarations'])}</ul>
<h3>Existing ASTIS declarations reused</h3><ul>{''.join('<li>'+decl_link(n)+'</li>' for n in item['astis_dependencies'])}</ul>
<h3>Mathlib results called, not re-proved here</h3><ul>{mathlib}</ul></details>
<details><summary>Focused tests · exact source</summary>{base.code_html((ROOT / item['test']).read_text(encoding='utf-8'))}</details></section>
<section id="source"><h2>Source and evidence</h2><p>This is original ASTIS exposition of a shared prerequisite, not a quotation or a replacement statement for a numbered source theorem. Expository coverage does not change formal completion.</p>
<span class="status status-{color}" data-reader-compiled="{str(ev['compiled']).lower()}">{compile_label}</span>
<dl><dt>Frontier Cell</dt><dd>{esc(ev['cell_status'])}</dd><dt>Source comparison</dt><dd data-reader-source-verdict="{esc(ev['source_verdict'])}">{esc(ev['source_state'])} / {esc(ev['source_verdict'])} / {esc(ev['source_review'])}</dd>
<dt>Registry membership</dt><dd>{ev['registry_entries']} of {len(ev['declarations'])} displayed results; repository Registry total: {data['registry']['compiled_local_leaves']}. Compilation and Registry admission are separate.</dd></dl>
<details><summary>Source correspondence and exact audit records</summary><ul>{sources}</ul>
<p>{esc(item['source_boundary'])}</p>
<a href="../data/proof-readers/{esc(item['id'])}-cell.json">Frontier Cell record</a> ·
<a href="../data/proof-readers/{esc(item['id'])}-audit.json">Independent source audit</a></details></section>
</article>'''
    return base.page(item["title"], rel, body, active="Proof readers", extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">')


def enrich_site(output: Path) -> None:
    items = load_items()
    data = read_json(output / "data/site-data.json")
    audits = {a["id"]: a for a in read_json(ROOT / "research-wiki/semantic-roundtrip/registry.json")["audits"]}
    directory = output / "data/proof-readers"
    directory.mkdir(parents=True, exist_ok=True)
    for item in items:
        rel = f"proofs/{item['id']}.html"
        base.write_page(output, rel, source_lineage.canonical_shell(render(item, data), rel, output))
        for suffix, record in (("cell", read_json(ROOT / "research-wiki/frontier-cells" / (item["cell"] + ".json"))), ("audit", audits[item["audit"]])):
            (directory / f"{item['id']}-{suffix}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rows = ''.join(f'<li><h2><a href="{esc(i["id"])}.html">{esc(i["title"])}</a></h2><p>{esc(i["purpose"])}</p></li>' for i in items)
    index = base.page("Shared proof readers", "proofs/index.html", f'<h1>Shared proof readers</h1><p>Read the mathematics first: precise hypotheses, displayed equations and a step-by-step proof. Lean, reused library facts and source evidence are optional. These shared results do not certify an entire textbook chapter.</p><ol>{rows}</ol>', active="Proof readers")
    base.write_page(output, "proofs/index.html", source_lineage.canonical_shell(index, "proofs/index.html", output))
    # Link the readers from real consumers, not a detached demonstration front end.
    targets = {"index.html", "progress/index.html"}
    for item in items:
        targets.update(item["entry_pages"])
        ev = evidence(item, data)
        targets.update(d["page"].split('#')[0] for d in ev["declarations"])
    for rel in sorted(targets):
        path = output / rel
        text = path.read_text(encoding="utf-8")
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', text, flags=re.S)
        links = ''.join(f'<li><a href="{esc(relative_link(rel, "proofs/"+i["id"]+".html"))}">{esc(i["title"])}</a></li>' for i in items if rel in {"index.html", "progress/index.html"} or rel in i["entry_pages"] or any(d["page"].split('#')[0] == rel for d in evidence(i, data)["declarations"]))
        block = f'{START}<section class="proof-reader-entry"><h2>Read the supporting proofs</h2><p>Mathematical derivations with optional Lean and source details.</p><ul>{links}</ul></section>{END}'
        if '</main>' not in text:
            raise ValueError(f"{rel}: no main reader surface")
        path.write_text(text.replace('</main>', block+'</main>', 1), encoding="utf-8")
    (output / "assets/proof-readers.css").write_text((ROOT / "website/static/proof-readers.css").read_text(encoding="utf-8"), encoding="utf-8")


def validate_site(output: Path) -> list[str]:
    errors = []
    data = read_json(output / "data/site-data.json")
    for item in load_items():
        ev = evidence(item, data)
        text = (output / f"proofs/{item['id']}.html").read_text(encoding="utf-8")
        for value in [*[u['statement'] for u in item['theorems']], *[u['formula'] for u in item['theorems']], *[s['formula'] for s in item['steps']], *item['boundary']]:
            if esc(value) not in text:
                errors.append(f"{item['id']}: missing mathematical content")
        if f'data-reader-compiled="{str(ev["compiled"]).lower()}"' not in text:
            errors.append(f"{item['id']}: compilation status drift")
        if f'data-reader-source-verdict="{esc(ev["source_verdict"])}"' not in text:
            errors.append(f"{item['id']}: source verdict drift")
        for name in item['declarations']:
            if esc(inline_lean.declarations()[name].source_text) not in text:
                errors.append(f"{item['id']}: exact Lean proof source drift")
            if text.count(f'data-inline-lean="{esc(name)}"') < 2:
                errors.append(f"{item['id']}: missing adjacent statement/proof Lean disclosure")
        if 'Optional Lean reading' in text:
            errors.append(f"{item['id']}: forbidden omnibus Lean panel")
        if re.search(r'<details\b[^>]*\bopen(?:\s|>)', text):
            errors.append(f"{item['id']}: optional source must start folded")
    return errors
