"""Source-pinned companion cases, proof technology and proposed topology.

This extension never edits the upstream 34-row snapshot, active case, Registry,
or SAU state. Its dependency overlay is not a compiler dependency graph.
"""
from __future__ import annotations

import json
import re
import textwrap
from html import escape
from pathlib import Path
from urllib.parse import urlencode

import astis_site
import source_lineage
import samplewiki_navigation
from samplewiki_reader_contract import formula_html, href_from

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "website/content/samplewiki_companion_frontiers.json"
BASE = "example-cases/samplewiki/companions/"
HOME = BASE + "index.html"
TECH = BASE + "proof-technology.html"
DELTA = BASE + "proof-delta.html"
DELTAS = ROOT / "website/content/samplewiki_proof_deltas.json"
ENTRY_PAGES = (
    "example-cases/samplewiki.html", "example-cases/samplewiki/frontier.html",
    "example-cases/samplewiki/progress.html", "libraries/mcmc/index.html",
    "progress/higher-order-sampling-detail.html",
)


def load():
    return json.loads(MODEL.read_text(encoding="utf-8"))


def validate_data(model=None):
    m = load() if model is None else model
    if m.get("schema_version") != 1 or not m.get("cases"):
        raise ValueError("Expected at least one source-pinned companion case")
    rows = [*m["cases"], m["composition"]]
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids) or any(r["status"] != "planned" for r in rows):
        raise ValueError("Companion cases must have unique ids and remain planned")
    if set(m["execution"]["targets"]) != {r["id"] for r in m["cases"]}:
        raise ValueError("Execution targets must list every companion source case exactly once")
    sources = m["sources"]
    for row in rows:
        if not set(row["source_ids"]) <= sources.keys():
            raise ValueError("Unknown companion source")
        for thm in row["theorems"]:
            formula_html(thm["formula"])
            for key in ("anchor", "assumptions", "statement", "steps", "boundary"):
                if not thm.get(key):
                    raise ValueError(f"Missing theorem contract: {key}")
            for step in thm["steps"]:
                formula_html(step["formula"])
                if not step["text"] or not step["anchor"]:
                    raise ValueError("Missing proof explanation or source")
        if "bookkeeping" in row:
            book = row["bookkeeping"]
            if not book.get("quantities") or not book.get("error_flow") or not book.get("boundary"):
                raise ValueError("Bookkeeping views require quantities, error flow and boundary")
            for quantity in book["quantities"]:
                formula_html(quantity["symbol"])
                formula_html(quantity["update"])
        if "setting" in row:
            formula_html(row["setting"]["formula"])
            if not row["setting"].get("notes"):
                raise ValueError("Case-specific settings require explanatory notes")
        outline = row.get("source_graph")
        if outline:
            node_ids = [node["id"] for node in outline["nodes"]]
            if len(node_ids) != len(set(node_ids)):
                raise ValueError("Duplicate source-proof outline node")
            if not outline.get("coverage"):
                raise ValueError("Source outline requires an explicit coverage boundary")
            for node in outline["nodes"]:
                if node.get("status") != "open" or not node.get("anchor"):
                    raise ValueError("Source outline is not a compiled Lean graph")
            for edge in outline["edges"]:
                if not {edge["parent"], edge["consumer"]} <= set(node_ids):
                    raise ValueError("Unknown source-proof outline endpoint")
                if edge.get("relation") != "source-proof-use; not Lean dependency":
                    raise ValueError("Source proof use cannot become a Lean dependency")
    techs = {r["id"]: r for r in m["technologies"]}
    if len(techs) != len(m["technologies"]):
        raise ValueError("Duplicate shared technology")
    visiting, visited = set(), set()

    def visit(ident):
        if ident in visiting:
            raise ValueError("Cyclic planned proof technology graph")
        if ident in visited:
            return
        if ident not in techs:
            raise ValueError("Unknown technology parent")
        visiting.add(ident)
        for parent in techs[ident]["parents"]:
            visit(parent)
        visiting.remove(ident)
        visited.add(ident)

    for ident, row in techs.items():
        visit(ident)
        if not set(row["consumers"]) <= (techs.keys() | set(ids)):
            raise ValueError("Unknown technology consumer")
        if not set(row["sources"]) <= sources.keys():
            raise ValueError("Unknown technology source")
        for module in row["search_modules"]:
            if not (ROOT / (module.replace(".", "/") + ".lean")).is_file():
                raise ValueError(f"Invented Lean search module: {module}")
    formula_html(m["setting"]["formula"])
    model_graph = json.loads((ROOT / 'website/content/functor_hypergraph.json').read_text(encoding='utf-8'))
    for key, source in sources.items():
        for field in ('title', 'url', 'anchor'):
            if model_graph['sources'][key][field] != source[field]:
                raise ValueError('Companion / hypergraph source drift')
    deltas = json.loads(DELTAS.read_text(encoding='utf-8'))
    for row in deltas['deltas']:
        if not set(row['technology_ids']) <= techs.keys() or row['source_id'] not in sources:
            raise ValueError('Unknown proof-delta technology/source')
    for row in deltas['deltas'] + deltas['operator_walkthrough']:
        if any(ord(c) < 32 for c in row['formula']):
            raise ValueError('Control character in proof-delta formula')
        formula_html(row['formula'])


def reader_prose(text):
    """Typeset known source notation; keep the canonical prose unchanged.

    These are literal notation substitutions, not a parser or a replacement
    theorem statement. Longer expressions win and are substituted only once.
    """
    notation = {
        '0<epsilon<=sqrt(d)/2': r'0<\varepsilon\le\sqrt d/2',
        'sqrt(alpha)W2<=epsilon': r'\sqrt{\alpha}\,W_2\le\varepsilon',
        'P0~N(0,I_d)': r'P_0\sim\mathcal N(0,I_d)',
        'X0=x_star': r'X_0=x_\star',
        'E[V(X0)-V(x_star)]<=C*d': r'\mathbb E[V(X_0)-V(x_\star)]\le C d',
        'friction2sqrt(beta)': r'\text{friction }2\sqrt{\beta}',
        'Tilde O': r'\widetilde O',
        'R_2(mu_0||pi)': r'R_2(\mu_0\Vert\pi)',
        'KL(mu||pi)': r'\operatorname{KL}(\mu\Vert\pi)',
        '||grad V(x_ref)||': r'\|\nabla V(x_{\mathrm{ref}})\|',
        'sqrt(alpha d)': r'\sqrt{\alpha d}',
        'sqrt(d/kappa)': r'\sqrt{d/\kappa}',
        'sqrt(alpha)W2': r'\sqrt{\alpha}\,W_2',
        'sqrt(d)/2': r'\sqrt d/2',
        'kappa=beta/alpha': r'\kappa=\beta/\alpha',
        '0<alpha I<=Hessian V(x)<=beta I': r'0\prec\alpha I\preceq\nabla^2 V(x)\preceq\beta I',
        'exp(-V)': r'e^{-V}',
        'C2': r'C^2', 'R^d': r'\mathbb R^d', 'W2': r'W_2',
        'mu_0': r'\mu_0', 'x_ref': r'x_{\mathrm{ref}}', 'x_star': r'x_\star',
        'c_opt': r'c_{\mathrm{opt}}', 'K_opt': r'K_{\mathrm{opt}}',
        'grad V': r'\nabla V', 'epsilon': r'\varepsilon', 'delta': r'\delta',
        'alpha': r'\alpha', 'beta': r'\beta', 'kappa': r'\kappa',
        'Delta': r'\Delta', 'pi': r'\pi', 'mu': r'\mu',
        'eta': r'\eta', 'rho': r'\rho', 'lambda': r'\lambda',
    }
    pattern = r'(?<![\w\\])(?:' + '|'.join(re.escape(s) for s in sorted(notation, key=len, reverse=True)) + r')(?!\w)'
    parts, start = [], 0
    for match in re.finditer(pattern, text):
        parts.extend([escape(text[start:match.start()]), r'\(' + escape(notation[match[0]]) + r'\)'])
        start = match.end()
    return (''.join(parts) + escape(text[start:])).replace('&lt;=', '≤').replace('&gt;=', '≥')


def ul(items):
    return "<ul>" + "".join(f"<li>{reader_prose(x)}</li>" for x in items) + "</ul>"


def sources_html(m, source_ids, anchor):
    links = " · ".join(
        f'<a href="{escape(m["sources"][key]["url"])}">{escape(m["sources"][key]["version"])}</a>'
        for key in source_ids
    )
    return f'<p class="companion-source">Source: {links}. {escape(anchor)}</p>'


def lean_fold(kind, text):
    return (f'<details class="companion-lean"><summary>Lean {kind} — not formalized yet</summary>'
            f'<p>{escape(text)}</p><p>No corresponding ASTIS declaration is asserted. '
            'Search locations below are candidates, not established dependencies or copied library proofs.</p></details>')


def lean_step_fold(step):
    declarations = step.get("compiled_support", [])
    if not declarations:
        return lean_fold("step", "This mathematical step is still open in Lean. The future declaration must expose exactly the objects and side conditions named above; no source-cited wrapper is counted as a proof.")
    links = "".join(
        f'<li><code>{escape(name)}</code></li>' for name in declarations
    )
    note = escape(step.get("support_note", "Only the listed reusable edge is compiled; source-specific adapters remain separate."))
    return (
        '<details class="companion-lean"><summary>Lean support — compiled reusable edge</summary>'
        f'<p>{note}</p><ul>{links}</ul>'
        '<p><a href="#gaussian-cloud-kernel-hybrid-telescope">Read the statement, mathematical proof and folded Lean source below ↓</a></p></details>'
    )


def theorem_html(m, row, thm):
    workspace_base = {
        "workspace": row["id"],
        "theorem": thm["id"],
    }
    step_fragments = []
    for index, step in enumerate(thm["steps"]):
        key = f'{thm["id"]}-step-{index + 1:02d}'
        query = urlencode({**workspace_base, "step": key})
        step_fragments.append(
            f'<li id="{escape(key)}"><h4>{escape(step["title"])}</h4>'
            f'{formula_html(step["formula"])}<p>{reader_prose(step["text"])}</p>'
            f'{sources_html(m, row["source_ids"], step["anchor"])}'
            f'<p><a class="button" href="../../../live/index.html?{query}">'
            'Track or question this step in Live Formalization</a></p>'
            f'{lean_step_fold(step)}</li>'
        )
    steps = "".join(step_fragments)
    return f'''<section class="companion-theorem" id="{escape(thm['id'])}" data-proof-status="planned">
<p class="companion-status">RED · source theorem known · local proof open</p>
<h3>{escape(thm['title'])}</h3>
{sources_html(m, row['source_ids'], thm['anchor'])}
<p><a class="button primary" href="../../../live/index.html?{urlencode(workspace_base)}">Open this theorem in the interactive research workspace</a></p>
<h3>Statement</h3><p>{reader_prose(thm['statement'])}</p>
{ul(thm['assumptions'])}{formula_html(thm['formula'])}
{lean_fold('statement', 'A future declaration must bind the probability laws, normalization, regularity, source algorithm and oracle model explicitly. The formula is a source theorem contract, not Lean code.')}
<details class="companion-proof-route" id="{escape(thm['id'])}-proof"><summary>Proof architecture and calculations · {len(thm['steps'])} steps</summary><p>This is a source-linked proof route, not a complete reconstruction of all cited lemmas. The dependencies below remain separate formalization tasks.</p>
<ol class="companion-steps">{steps}</ol>
{lean_fold('proof', 'Formalization will first match the named technology interfaces, then assemble this source theorem. No placeholder proof or source-cited wrapper has been added.')}</details>
<h3>Strict boundary</h3><p>{reader_prose(thm['boundary'])}</p></section>'''


def bookkeeping_html(book):
    quantities = "".join(
        "<tr>" +
        f'<th scope="row">{formula_html(row["symbol"])}</th>' +
        f'<td>{escape(row["meaning"])}</td>' +
        f'<td>{formula_html(row["update"])}</td>' +
        f'<td>{escape(row["role"])}</td></tr>'
        for row in book["quantities"]
    )
    flow = "".join(
        f'<li><h3>{escape(row["stage"])}</h3><p><strong>Input.</strong> {escape(row["input"])}</p>'
        f'<p><strong>Output.</strong> {escape(row["output"])}</p><p><strong>Ledger charge.</strong> {escape(row["charge"])}</p></li>'
        for row in book["error_flow"]
    )
    return f'''<section class="bookkeeping-ledger" id="section-6-ledger">
<p class="companion-status">SOURCE-PINNED LEDGER · Lean formalization open</p>
<h2>{escape(book['title'])}</h2><p>{escape(book['intro'])}</p>
<figure><a href="../../../assets/gaussian-cloud-section-6-ledger.svg"><img src="../../../assets/gaussian-cloud-section-6-ledger.svg" alt="Gaussian cloud Section 6 call-count and accumulated-error ledger."></a><figcaption>Call count and law error are separate ledgers joined only at the deterministic global cap. Open the SVG to zoom.</figcaption></figure>
<div class="table-scroll"><table><thead><tr><th>Symbol</th><th>Meaning</th><th>Definition or update</th><th>Why it is tracked</th></tr></thead><tbody>{quantities}</tbody></table></div>
<h2>Where each error enters</h2><ol class="error-ledger">{flow}</ol>
{lean_fold('ledger interface', 'The first Lean packet will formalize the fixed finite dummy-filled history and adjacent-hybrid TV telescope. Adaptive-tree tails, concrete cloud kernels and final parameter substitution stay separate.')}
<h3>Strict boundary</h3><p>{escape(book['boundary'])}</p></section>'''


def comparison_html(row):
    """Source mechanisms and open proof use; never a compiler dependency claim."""
    if not row.get("method_comparison"):
        return ""
    rows = "".join(
        f'<tr><th scope="row">{escape(item["aspect"])}</th>'
        f'<td>{escape(item["sign"])}</td><td>{escape(item["eigen"])}</td></tr>'
        for item in row["method_comparison"]
    )
    outline = row["source_graph"]
    parents = {node["id"]: [] for node in outline["nodes"]}
    labels = {node["id"]: node["label"] for node in outline["nodes"]}
    for edge in outline["edges"]:
        parents[edge["consumer"]].append(labels[edge["parent"]])
    nodes = "".join(
        f'<li id="source-{escape(node["id"])}"><h4>{escape(node["label"])}</h4>'
        f'<p>Source: {escape(node["anchor"])}. Lean: open.</p>'
        f'<p>Source inputs: {escape("; ".join(parents[node["id"]]) or "source definition or background obligation")}</p></li>'
        for node in outline["nodes"]
    )
    notes = ul(row.get("source_notes", []))
    return f'''<section id="method-comparison"><h2>How the two proofs organize their ingredients</h2>
<p>One canonical Lean node is shared only when the exact compiled declaration is actually consumed, with its hypotheses matched. Residual Haar symmetry is currently a conceptual link: it does not identify determinant-component posterior laws with deferred-rotation Krylov laws.</p>
<div class="table-scroll"><table><thead><tr><th>Comparison</th><th>Determinant sign</th><th>Hidden eigenbasis</th></tr></thead><tbody>{rows}</tbody></table></div>
<h3>Source proof outline</h3><p>{escape(outline['coverage'])}</p><p>All links below describe source proof use. No solid Lean implication or compiled node is asserted.</p>
<details><summary>Expand {len(outline['nodes'])} source nodes and their inputs</summary><ol>{nodes}</ol></details>
<h3>Source discrepancies retained for review</h3>{notes}</section>'''


def nav(rel):
    return (f'<nav class="reader-breadcrumb"><a href="{href_from(rel, "example-cases/samplewiki.html")}">SampleWiki</a> / '
            f'<a href="{href_from(rel, HOME)}">Sampling papers</a></nav>')


def write(output, rel, title, body):
    styles = "".join(f'<link rel="stylesheet" href="{href_from(rel, "assets/" + name)}">'
                     for name in ("samplewiki-math-reader.css", "samplewiki-companions.css", samplewiki_navigation.STYLE_NAME))
    styles += f'<script defer src="{href_from(rel, "assets/" + samplewiki_navigation.SCRIPT_NAME)}"></script>'
    page = astis_site.page(title, rel, '<article class="companion-reader">' + nav(rel) + body + '</article>',
                           active="SampleWiki", description=title + "; source-pinned proof route, local Lean work open.", extra_head=styles)
    page = source_lineage.canonical_shell(page, rel, output)
    page = samplewiki_navigation.inject_paper_directory(page, rel)
    astis_site.write_page(output, rel, page)


def topology_svg(m):
    """Three source routes for four papers; planned interfaces are not Lean edges."""
    rows = [
        ("producer", 30, 100, 340, "SPHMC", "Transport sampler + recursion"),
        ("consumer", 410, 100, 340, "Proximal BPS", "Warm-start engine"),
        ("proxy", 30, 250, 340, "Actual law + proxy witness", "TV budget + order-2 Renyi"),
        ("kernel", 410, 250, 340, "Implemented probability kernel", "Mixing and cost stay separate"),
        ("join", 220, 400, 340, "TV-stable handoff", "Same target, same kernel"),
        ("result", 220, 550, 340, "Cold-to-high-accuracy view", "Source theorem; Lean open"),
        ("cloud", 860, 100, 360, "Picard HMC Part I", "Gaussian cloud correction"),
        ("forest", 860, 250, 360, "Adaptive request forest", "Queue, children, caps, queries"),
        ("ledger", 860, 400, 360, "Conditional-kernel ledger", "One delta per slot + one cap error"),
        ("cloud-result", 860, 550, 360, "High-accuracy sampler", "Source theorem; Lean open"),
        ("midpoint", 30, 740, 340, "Midpoint Langevin", "C2 Hessian bounds"),
        ("midpoint-kernel", 410, 740, 340, "Actual method kernels", "Initialization + query contract"),
        ("midpoint-upper", 860, 740, 360, "Deterministic upper bounds", "Heun + exponential midpoint"),
        ("midpoint-lower", 860, 890, 360, "Separate lower bounds", "Deterministic + randomized"),
    ]
    positions = {key: (x, y, width) for key, x, y, width, _, _ in rows}
    edges = [
        ("producer", "proxy"), ("consumer", "kernel"), ("proxy", "join"),
        ("kernel", "join"), ("join", "result"), ("cloud", "forest"),
        ("forest", "ledger"), ("ledger", "cloud-result"),
        ("midpoint", "midpoint-kernel"), ("midpoint-kernel", "midpoint-upper"),
        ("midpoint-kernel", "midpoint-lower"),
    ]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1260 1040" role="img" aria-labelledby="title desc">',
           '<title id="title">Four fixed-version papers in three source-proof routes</title>',
           '<desc id="desc">Red boxes are local proof obligations. Dashed arrows are planned source interfaces, not Lean dependencies. The left route composes SPHMC with Proximal BPS; the right route tracks Gaussian-cloud recursive calls and errors. The separate lower lane keeps midpoint method kernels, upper bounds and lower bounds distinct.</desc>',
           '<rect width="1260" height="1040" fill="#fff"/>',
           '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#9c3434"/></marker></defs>',
           '<text x="30" y="35" font-family="sans-serif" font-size="24" fill="#18212f">Four papers → three auditable source routes</text>',
           '<text x="30" y="62" font-family="sans-serif" font-size="16" fill="#6c3434">RED: local proof open. Dashed: planned interface, not compiler dependency.</text>']
    for a, b in edges:
        x, y, width = positions[a]; u, v, target_width = positions[b]
        if y == v:
            path = f"M{x+width},{y+50} H{u}"
        elif a == "midpoint-kernel":
            path = f"M{x+width/2},{y+100} C{x+width/2},{v+50} {u-30},{v+50} {u},{v+50}"
        else:
            path = f"M{x+width/2},{y+100} C{x+width/2},{y+126} {u+target_width/2},{v-26} {u+target_width/2},{v}"
        out.append(f'<path d="{path}" fill="none" stroke="#9c3434" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#arrow)"/>')
    for key, x, y, width, title, subtitle in rows:
        out.append(f'<g id="{key}"><rect x="{x}" y="{y}" width="{width}" height="100" rx="10" fill="#fff4f3" stroke="#ba3535" stroke-width="2"/>')
        out.append(f'<text x="{x+18}" y="{y+39}" font-family="sans-serif" font-size="21" fill="#652020">{escape(title)}</text>')
        out.append(f'<text x="{x+18}" y="{y+70}" font-family="sans-serif" font-size="17" fill="#493434">{escape(subtitle)}</text></g>')
    return "\n".join(out) + "</svg>"


def gaussian_cloud_ledger_svg():
    """Section 6 bookkeeping as two separate ledgers joined by the global cap."""
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 760" role="img" aria-labelledby="gc-title gc-desc">',
           '<title id="gc-title">Gaussian cloud Section 6 recursive-call and accumulated-error ledger</title>',
           '<desc id="gc-desc">The upper lane controls adaptive request count. The lower lane telescopes conditional-kernel replacement errors. They meet at the deterministic global cap.</desc>',
           '<rect width="1180" height="760" fill="#fff"/>',
           '<defs><marker id="gc-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#8e3030"/></marker></defs>',
           '<text x="30" y="38" font-family="sans-serif" font-size="25" fill="#18212f">Section 6: two ledgers, one auditable cap</text>',
           '<text x="30" y="68" font-family="sans-serif" font-size="16" fill="#6c3434">Every red node is a source-pinned Lean obligation, not a compiled theorem.</text>',
           '<text x="30" y="118" font-family="sans-serif" font-size="20" font-weight="600" fill="#26364a">Call ledger</text>',
           '<text x="30" y="410" font-family="sans-serif" font-size="20" font-weight="600" fill="#26364a">Error ledger</text>']
    boxes = [
        (30,145,245,110,'q roots','A₀ = q'),
        (320,145,245,110,'Process vertex v','Aᵥ₊₁ = Aᵥ − 1 + ζᵥ₊₁'),
        (610,145,245,110,'Stop at empty queue','T = inf {v : Aᵥ = 0}'),
        (900,145,245,110,'Query count','Qref ≤ Qloc T'),
        (465,290,250,90,'Deterministic cap','Tmax fixed; dummy-fill'),
        (30,440,245,110,'Ideal slot t','Kₜ(Hₜ₋₁, ·)'),
        (320,440,245,110,'Implemented slot t','K̂ₜ(Hₜ₋₁, ·)'),
        (610,440,245,110,'Adjacent hybrid','charge δₜ once'),
        (900,440,245,110,'Finite telescope','Σₜ δₜ'),
        (465,610,250,90,'Final output error','Σₜ δₜ + εcap'),
    ]
    for x,y,w,h,title,sub in boxes:
        out.append(f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff4f3" stroke="#ba3535" stroke-width="2"/>')
        out.append(f'<text x="{x+16}" y="{y+40}" font-family="sans-serif" font-size="20" fill="#652020">{escape(title)}</text>')
        out.append(f'<text x="{x+16}" y="{y+74}" font-family="sans-serif" font-size="16" fill="#493434">{escape(sub)}</text></g>')
    paths = [
        'M275,200 H315', 'M565,200 H605', 'M855,200 H895',
        'M1020,255 C1020,330 720,335 720,335',
        'M275,495 H315', 'M565,495 H605', 'M855,495 H895',
        'M1020,550 C1020,655 720,655 720,655',
        'M590,380 V435',
    ]
    for path in paths:
        out.append(f'<path d="{path}" fill="none" stroke="#8e3030" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#gc-arrow)"/>')
    out.append('<text x="735" y="326" font-family="sans-serif" font-size="15" fill="#5e3b3b">cap-failure probability εcap</text>')
    out.append('<text x="610" y="398" font-family="sans-serif" font-size="15" fill="#5e3b3b">common fixed history interface</text>')
    return "\n".join(out) + "</svg>"


def enrich_site(output):
    m = load(); validate_data(m)
    samplewiki_navigation.install_style(output)
    assets = output / "assets"
    (assets / "samplewiki-companions.css").write_text((ROOT / "website/static/samplewiki-companions.css").read_text(encoding="utf-8"), encoding="utf-8")
    (assets / "samplewiki-companions.svg").write_text(topology_svg(m), encoding="utf-8")
    (assets / "gaussian-cloud-section-6-ledger.svg").write_text(gaussian_cloud_ledger_svg(), encoding="utf-8")
    delta_model = json.loads(DELTAS.read_text(encoding='utf-8'))
    (assets / 'samplewiki-proof-delta.svg').write_text(proof_delta_svg(delta_model), encoding='utf-8')
    rows = [*m["cases"], m["composition"]]
    for row in rows:
        body = (f'<header class="paper-reader-header"><h1>{escape(row.get("reader_label", row["title"]))}</h1>'
                f'<p class="paper-subtitle">{escape(row.get("reader_summary", row["role"]))}</p>'
                '<p class="companion-status">Main paper results remain open in Lean. Verified building blocks are listed separately below.</p></header>')
        body += (f'<nav class="paper-reading-nav" aria-label="Reading depth"><a href="#paper-main-results">1. Statements</a>'
                 f'<a href="#{escape(row["theorems"][0]["id"])}-proof">2. Proof route</a>'
                 '<a href="#paper-lean-progress">3. Verified work</a></nav>')
        if row.get("reader_guide"):
            body += '<details class="reader-guide"><summary>Suggested reading order</summary><ol>' + ''.join(f'<li>{escape(item)}</li>' for item in row['reader_guide']) + '</ol></details>'
        setting = row.get("setting", m["setting"])
        body += ('<details class="paper-source-setting"><summary>Paper, notation and source conventions</summary>'
                 + ''.join(f'<p>{escape(m["sources"][sid]["title"])}</p>' for sid in row['source_ids'])
                 + sources_html(m, row['source_ids'], 'Pinned source version')
                 + formula_html(setting['formula']) + ul(setting['notes']) + '</details>')
        body += '<section id="paper-main-results"><h2>1. Main statements</h2>'
        body += theorem_html(m, row, row['theorems'][0])
        if row.get("bookkeeping"):
            body += ('<details class="paper-section-ledger"><summary>Section 6: follow the recursive calls and accumulated errors</summary>'
                     + bookkeeping_html(row['bookkeeping']) + '</details>')
        if len(row['theorems']) > 1:
            body += ('<details class="paper-supporting-statements"><summary>Further source statements · '
                     + str(len(row['theorems']) - 1) + '</summary>'
                     + ''.join(theorem_html(m, row, t) for t in row['theorems'][1:]) + '</details>')
        body += '</section>'
        body += ('<section id="paper-lean-progress" data-paper-publications="pending"><h2>3. Verified work</h2>'
                 '<p>No declaration-level publication is attached to this page yet. A source proof route is not a Lean verification.</p></section>')
        body += ('<details class="paper-advanced"><summary>Compare proof mechanisms and prerequisites</summary>'
                 + comparison_html(row)
                 + '<p><a href="proof-technology.html">Reusable prerequisites</a> · '
                 '<a href="proof-delta.html">What changes in the proof?</a></p></details>')
        write(output, BASE + row['slug'] + '.html', row['title'], body)
    priority_ids = {r['id'] for r in samplewiki_navigation.priority_cases(m)}
    cards = ''.join(f'<li><a href="{r["slug"]}.html">{escape(r["title"])}</a></li>' for r in rows if r['id'] not in priority_ids)
    sources = ''.join(f'<li><a href="{escape(s["url"])}">{escape(s["title"])}</a> — {escape(", ".join(s["authors"]))}. {escape(s["version"])}. {escape(s["pin_kind"])}.</li>' for s in m['sources'].values())
    body = ('<header class="paper-reader-header"><h1>Sampling papers</h1><p>Start with a paper. Read the main ideas first, then expand a proof or its checked Lean.</p></header>'
            + samplewiki_navigation.paper_cards(HOME, m)
            + '<details class="paper-advanced"><summary>Composition and other research projects</summary><ul>' + cards + '</ul></details>')
    body += '<details class="paper-advanced"><summary>Compare the proposed proof routes</summary><p>' + escape(m['topology']['change']) + '</p>'
    body += '<figure><a href="../../../assets/samplewiki-companions.svg"><img src="../../../assets/samplewiki-companions.svg" alt="Three red source cases form a proxy-stable composition route and a separate Gaussian-cloud recursive-accounting route; all formalization remains open."></a><figcaption>Open the SVG to zoom. This is a planned source-interface graph, not the Lean import graph.</figcaption></figure>'
    body += '<p>' + escape(m['topology']['interpretation']) + '</p>' + ul(m['topology']['chewi_windows'] + m['topology']['other_routes'])
    body += '<p>' + escape(m['topology']['failure_boundary']) + '</p><p><a href="../../../lean-foundations.html?view=frontier&amp;focus=case%3AASTIS-SW-SPHMC-PBPS-COMPOSITION">Expand this frontier in the interactive proof graph →</a> · <a href="../../../lean-foundations.html?view=functor&amp;focus=transport%3Aproxy-warm-handoff">Inspect the candidate certificate bridge →</a></p></details>'
    body += f'<section><h2>Reading and formalization order</h2><p>Use the source-case cards as researcher-facing maps. For Picard HMC Part I, read the Section 6 call/error ledger before the detailed lemmas. Formalize dependency-ready common technology before algorithm assemblies; preserved textbook and companion frontiers are not reset.</p><p><a href="proof-technology.html">{len(m["technologies"])} reusable technology contracts and {len(m["next_packets"])} next-packet candidates →</a></p></section>'
    body += '<details class="paper-advanced"><summary>Attribution and source versions</summary><ul>' + sources + '</ul><p>These are ASTIS mathematical restatements and proof-route explanations, not reproduced paper prose. Licenses are recorded per pinned source; no blanket right to republish paper prose, author endorsement or new Lean certificate is implied.</p></details>'
    write(output, HOME, m['title'], body)
    techs = {t['id']: t for t in m['technologies']}
    items = []
    for t in m['technologies']:
        links = ' · '.join(f'<a href="#{escape(p)}">{escape(techs[p]["title"])}</a>' for p in t['parents']) or 'Independent root candidate'
        consumers = ' · '.join(f'<a href="#{escape(p)}">{escape(techs[p]["title"])}</a>' if p in techs else '<a href="warm-start-composition.html">Composition view</a>' for p in t['consumers'])
        mods = ''.join(f'<li><a href="{href_from(TECH, "modules/"+astis_site.slugify(name)+".html")}">{escape(name)}</a> — search candidate only</li>' for name in t['search_modules'])
        items.append(f'<section id="{escape(t["id"])}"><p class="companion-status">RED · reusable target, not a compiled leaf</p><h2>{escape(t["title"])}</h2><p>{escape(t["target"])}</p>{sources_html(m,t["sources"],t["anchor"])}<p>Parents: {links}</p><p>Consumers: {consumers}</p><h3>Failure boundary</h3><p>{escape(t["boundary"])}</p><details><summary>Existing Lean reuse-search locations</summary><ul>{mods}</ul><p>Inspect exact ASTIS and pinned Mathlib types before declaring reuse. No new source theorem or wrapper is introduced by this list.</p></details></section>')
    packets = ''.join(f'<li><h3>{escape(p["target"])}</h3><p>{escape(p["scope"])}</p><p>Exclude: {escape(p["exclude"])}</p></li>' for p in m['next_packets'])
    write(output, TECH, 'Reusable proof technology', '<h1>Reusable proof technology</h1><p>Shared identities, explicit consumers and separate adapters. These targets do not reschedule the active mathematical frontier.</p>' + ''.join(items) + '<section><h2>Next dependency-ready packet candidates</h2><ol>' + packets + '</ol></section>')
    write_proof_delta(output, m, delta_model)
    for rel in ENTRY_PAGES:
        path = output / rel
        if not path.exists():
            raise ValueError(f'Missing companion entry surface: {rel}')
        text = path.read_text(encoding='utf-8')
        if 'data-companion-frontiers="true"' in text:
            continue
        banner = (f'<nav class="paper-entry-link" data-companion-frontiers="true" aria-label="Sampling papers">'
                  f'<a href="{href_from(rel, HOME)}">Four sampling papers: PBPS, SPHMC, Gaussian Cloud and Midpoint →</a></nav>')
        text, count = re.subn(r'(<main\b[^>]*>)', lambda match: match.group(1) + banner, text, count=1)
        if count != 1:
            raise ValueError(f'Missing main for companion entry: {rel}')
        path.write_text(text, encoding='utf-8')
    (output / 'data/samplewiki-companion-frontiers.json').write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def add_to_graph(builder):
    m = load(); validate_data(m)
    for row in [*m['cases'], m['composition']]:
        builder.add('case:' + row['id'], 'frontier-case', row['title'], status='planned', subtitle=row['role'], url=BASE + row['slug'] + '.html', summary=m['review'], details=[{'label':'Lean status','value':'No local theorem certificate; source-pinned plan only.'}])
        builder.edge('library:samplewiki', 'case:' + row['id'], 'companion source case; not a proof dependency')
        outline = row.get('source_graph')
        if outline:
            prefix = 'source-outline:' + row['id'] + ':'
            for node in outline['nodes']:
                builder.add(prefix + node['id'], 'proof-root', node['label'], status='planned',
                            subtitle=node['anchor'], summary=outline['coverage'],
                            url=BASE + row['slug'] + '.html#source-' + node['id'])
            for edge in outline['edges']:
                builder.edge(prefix + edge['parent'], prefix + edge['consumer'], edge['relation'])
            for target in ('sign-main', 'eigen-main'):
                if any(n['id'] == target for n in outline['nodes']):
                    builder.edge(prefix + target, 'case:' + row['id'], 'source theorem outline; not a proof dependency')
    for t in m['technologies']:
        builder.add(t['id'], 'proof-root', t['title'], status='planned', subtitle='Reusable proof technology candidate', summary=t['target'], url=TECH+'#'+t['id'], details=[{'label':'Boundary','value':t['boundary']}])
    for t in m['technologies']:
        for parent in t['parents']:
            builder.edge(parent, t['id'], 'planned technology prerequisite; not a proof dependency')
        for module in t['search_modules']:
            builder.edge('module:'+module, t['id'], 'reuse search candidate; not a proof dependency')
    for a,b in [
        ('tech:proxy-warm', 'ASTIS-SW-SPHMC-2026'),
        ('tech:implemented-kernel', 'ASTIS-SW-PBPS-2026'),
        ('tech:gaussian-cloud-assembly', 'ASTIS-SW-GAUSSIAN-CLOUD-2026'),
        ('tech:tv-handoff', m['composition']['id']),
    ]:
        builder.edge(a,'case:'+b,'planned source assembly; not a proof dependency')
    delta_model = json.loads(DELTAS.read_text(encoding='utf-8'))
    for row in delta_model['lineage']:
        builder.add(row['id'], 'proof-root', row['label'], status='external-reference', subtitle=row['role'], url=DELTA+'#lineage', source_url=row['url'])
    builder.edge('lineage:dms', 'lineage:fan-li-lu', 'historical refinement; not a proof dependency')
    builder.edge('lineage:fan-li-lu', 'lineage:pbps-discrete', 'discrete adaptation; not a proof dependency')
    builder.edge('lineage:pbps-discrete', 'tech:discrete-hypocoercivity', 'source-specific operator contract; not a proof dependency')
    return {'source_cases':len(m['cases']), 'composition_views':1, 'technology_candidates':len(m['technologies'])}


def proof_delta_svg(d):
    """Maintainable before/after comparison; no quantitative novelty score."""
    height = 150 + 160 * len(d['deltas'])
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 {height}" role="img" aria-labelledby="dt dd">',
           '<title id="dt">Proof-technology delta: inheritance versus new adapters</title>',
           '<desc id="dd">Grey is existing external mathematics; red is the paper-specific local formalization target. All links represent source lineage, not compiled proof dependencies.</desc>',
           f'<rect width="1040" height="{height}" fill="white"/>',
           '<text x="28" y="36" font-family="sans-serif" font-size="23" fill="#18212f">What changed in the proof?</text>',
           '<text x="28" y="68" font-family="sans-serif" font-size="16" fill="#454545">Grey: inherited external tools. Red: source-specific adapter, local Lean open.</text>']
    labels = [
        ('Gaussian smoothing / quadrature', 'Score-aware Picard error budget'),
        ('Transport and divergence tools', 'Recursive proxy-warm contract'),
        ('Proximal / BPS / boomerang tools', 'Auxiliary reflection + half-turn'),
        ('DMS → Fan–Li–Lu refinement', 'Discrete coupled-mode corrector'),
        ('Ideal-chain convergence', 'Implemented error + cost channels'),
    ]
    for i, (row, (before, after)) in enumerate(zip(d['deltas'], labels, strict=True)):
        y = 100 + 160*i
        out.append(f'<g id="{escape(row["id"])}"><text x="28" y="{y}" font-family="sans-serif" font-size="17" fill="#18212f">{i+1}. {escape(row["kind"])}</text>')
        for x, label, fill, stroke in [(28,before,'#f1f2f4','#747b86'),(558,after,'#fff4f3','#ba3535')]:
            out.append(f'<rect x="{x}" y="{y+18}" width="450" height="85" rx="8" fill="{fill}" stroke="{stroke}"/>')
            for j,line in enumerate(textwrap.wrap(label, width=34)):
                out.append(f'<text x="{x+16}" y="{y+51+25*j}" font-family="sans-serif" font-size="21" fill="#272e39">{escape(line)}</text>')
        out.append(f'<path d="M488,{y+60} H545 m-9,-6 9,6 -9,6" stroke="#8c4141" fill="none" stroke-width="2" stroke-dasharray="5 3"/></g>')
    return '\n'.join(out) + '</svg>'


def write_proof_delta(output, m, d):
    body = '<h1>What did these papers add to the proof graph?</h1><p>' + escape(d['purpose']) + '</p><p>' + escape(d['truth_boundary']) + '</p>'
    body += '<figure><a href="../../../assets/samplewiki-proof-delta.svg"><img src="../../../assets/samplewiki-proof-delta.svg" alt="Five before-and-after proof-technology comparisons; inherited external tools are grey, local adapter obligations red."></a><figcaption>Contribution role and compilation status are different axes. Open to zoom.</figcaption></figure>'
    body += '<section id="lineage"><h2>Which Jianfeng Lu-related technology is being reused?</h2>'
    body += '<ol>' + ''.join(f'<li><a href="{escape(r["url"])}">{escape(r["label"])}</a>: {escape(r["role"])}. {escape(r["anchor"])}.</li>' for r in d['lineage']) + '</ol>'
    body += '<p>The Fan–Li–Lu paper supplies a gap-shifted corrector in continuous-time underdamped Langevin analysis. PBPS explicitly credits that refinement, then proves its own discrete reflection and half-turn estimates. This is a mechanism lineage, not verbatim reuse of a convergence theorem.</p></section>'
    for row in d['deltas']:
        body += f'<section id="{escape(row["id"])}"><p class="companion-status">Local formalization open · {escape(row["kind"])}</p><h2>{escape(row["label"])}</h2><h3>Already available in the literature</h3><p>{escape(row["before"])}</p><h3>What this paper changes</h3><p>{escape(row["after"])}</p>{formula_html(row["formula"])}<h3>Structure exposed by the proof</h3><p>{escape(row["structure"])}</p>{sources_html(m,[row["source_id"]],row["anchor"])}<p>{escape(row["boundary"])}</p>'
        body += '<p>Expandable technology nodes: ' + ' · '.join(f'<a href="proof-technology.html#{escape(t)}">{escape(t)}</a>' for t in row['technology_ids']) + '</p></section>'
    body += '<section><h2>Inside the discrete modified-L2 mechanism</h2><p>All operators below act on the source-defined augmented L2 space; the macro inverse is restricted to its centered subspace. These are source formulas, not local Lean certificates.</p><ol>'
    for step in d['operator_walkthrough']:
        body += '<li><h3>' + escape(step['title']) + '</h3>' + formula_html(step['formula']) + '<p>' + escape(step['text']) + '</p>' + sources_html(m,['pbps-2026'],step['anchor']) + '</li>'
    body += '</ol>' + lean_fold('proof architecture', 'First port projection and polar-decomposition contracts, then the two source-specific estimates, then the modified-energy assembly. Current scalar-decay modules are search substrates only; none certify this mechanism.') + '</section>'
    write(output, DELTA, 'Proof technology: what changed?', body)


def validate_site(output):
    errors = []
    m = load(); validate_data(m)
    for row in [*m['cases'], m['composition']]:
        path = output / (BASE + row['slug'] + '.html')
        text = path.read_text(encoding='utf-8') if path.exists() else ''
        expected_step_folds = 0
        for t in row['theorems']:
            expected_step_folds += sum(1 for s in t['steps'] if not s.get('compiled_support'))
            for step in t['steps']:
                for declaration in step.get('compiled_support', []):
                    if declaration not in text:
                        errors.append(f'{path.name}: missing compiled step support {declaration}')
            for marker in (f'id="{t["id"]}"', formula_html(t['formula']), 'Lean statement — not formalized yet', 'Lean proof — not formalized yet'):
                if marker not in text:
                    errors.append(f'{path.name}: missing {marker[:90]}')
        if text.count('Lean step — not formalized yet') < expected_step_folds:
            errors.append(f'{path.name}: every mathematical proof step needs an adjacent folded Lean status')
        if row.get('bookkeeping') and 'id="section-6-ledger"' not in text:
            errors.append(f'{path.name}: missing recursive-call/error bookkeeping ledger')
        if '<details open' in text or 'data-proof-status="compiled"' in text:
            errors.append('Companion reader must not assert compilation or open Lean by default')
    if not (output / 'assets/gaussian-cloud-section-6-ledger.svg').is_file():
        errors.append('Missing Gaussian-cloud Section 6 ledger SVG')
    for rel in ENTRY_PAGES:
        if 'data-companion-frontiers="true"' not in (output/rel).read_text(encoding='utf-8'):
            errors.append(f'Missing companion navigation: {rel}')
    delta_text = (output / DELTA).read_text(encoding='utf-8')
    for row in json.loads(DELTAS.read_text(encoding='utf-8'))['deltas']:
        if f'id="{row["id"]}"' not in delta_text:
            errors.append('Missing proof-delta card: ' + row['id'])
    return errors
