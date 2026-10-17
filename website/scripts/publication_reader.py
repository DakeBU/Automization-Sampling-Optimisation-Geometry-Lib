"""Project publication correspondences into reader pages; no authored statuses."""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

import astis_publication as publication
import astis_site
import declaration_lessons
import source_lineage
import samplewiki_navigation

SOURCE_EDGE = 'source correspondence; not a Lean dependency'
REFERENCE_EDGE = 'source reference (scanner)'


def status(library: str, chapter: str | None = None) -> str:
    p = publication.chapter_progress(library, chapter)
    return (f'<span class="status status-{"orange" if p["status"] != "scaffold" else "gray"}" '
            f'data-publication-status="{p["status"]}">{escape(p["label"])}</span>')


def chapter_path_progress(chapter_path: str) -> dict:
    """Aggregate publication progress for every source item rendered on one page.

    A companion page may cover several source sections.  Its graph badge must not
    depend on which JSON item happened to be loaded last.
    """
    progress = [publication.chapter_progress(item['library'], item['chapter'])
                for item in publication.load() if item['chapter_path'] == chapter_path]
    proved = sorted({name for item in progress for name in item['proof_declarations']})
    prerequisites = sorted({name for item in progress for name in item['prerequisites']})
    return {
        'status': 'partial' if proved else 'prerequisite-ready' if prerequisites else 'scaffold',
        'label': ('Partially formalized' if proved else
                  'Prerequisites available' if prerequisites else 'scaffold'),
        'proof_declarations': proved,
        'prerequisites': prerequisites,
        'source_complete': False,
    }


def semantic_details(audit: dict) -> str:
    gaps = ''.join(f'<li><strong>{escape(str(d.get("slot", "")))}</strong>: '
                   f'{escape(str(d.get("description", "")))} — {escape(str(d.get("evidence", "")))}</li>'
                   for d in audit.get('deltas', []))
    repairs = ''.join('<article><h4>Proposed source repair — not the original theorem</h4>'
                      f'<p>{escape(r["reconstructed_statement"])}</p><p>{escape(r["proposed_change"])}</p>'
                      f'<p>Classification: {escape(r["necessity"])} · Status: {escape(r["status"])}</p>'
                      f'<p>{escape(r["justification"])}</p><p>Minimality: {escape(r["minimality_evidence"])}</p>'
                      f'<p>Evidence: {escape(r["reference_or_counterexample"])}</p></article>'
                      for r in audit.get('repairs', []))
    return ('<h4>Detected semantic differences</h4><ul>' + gaps + '</ul>' if gaps else '') + repairs


def source_card(item: dict, page: str) -> str:
    data = publication.inputs()
    source = item['source']
    progressive = all(data['lessons'][b['declaration']].get('reading_layout') == 'progressive'
                      for b in item['bindings'])
    formulae = ''.join(f'<h3>{escape(f["label"])}</h3><div class="proof-reader-equation">'
                       f'\\[{escape(f["tex"])}\\]</div>' for f in item['formulae'])
    obligations = []
    for o in item['obligations']:
        verified = [b for b in item['bindings']
                    if o['id'] in b.get('supports', [])
                    and publication.verified_binding(b, data)]
        proof_supporters = [b for b in verified if b['role'] == 'proof-edge']
        prerequisite_supporters = [b for b in verified if b['role'] == 'prerequisite']
        if proof_supporters:
            label, color = 'Formalized proof edge; source adapter/review separate', 'orange'
        elif prerequisite_supporters:
            label, color = 'Independently verified prerequisite', 'green'
        else:
            label, color = 'TODO — not closed by these contributions', 'red'
        obligations.append(f'<li><span class="status status-{color}">{label}</span> '
                           f'{escape(o["label"])}</li>')
    lessons = []
    for b in item['bindings']:
        name = b['declaration']
        audit = data['audits'].get(b.get('audit_id'), {})
        debt = b.get('legacy_audit_debt', {})
        history = ('<p><strong>Historical audit record: legacy_audit_debt.</strong> '
                   + escape(debt.get('reason', ''))
                   + ' Any current review below applies to the current version; it does not certify a historical worker run.</p>') if debt else ''
        rows = ''.join('<tr>' + ''.join(f'<td>{escape(r[k])}</td>' for k in ('source', 'lean', 'classification', 'reason')) + '</tr>'
                       for r in b['assumption_deltas'])
        comparison = (f'<section data-source-comparison="{escape(name)}">'
                           '<h3>Source assumptions versus formal assumptions</h3>'
                           '<div class="table-scroll"><table><thead><tr><th>Source</th><th>Actual Lean</th>'
                           '<th>Difference kind</th><th>Why it matters</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
                           f'<p>{escape(b["boundary"])}</p>'
                           + history
                           + '<p><strong>Encoder–denoiser:</strong> ' + escape(audit.get('state', 'pending historical audit'))
                           + ' · ' + escape(audit.get('verdict', 'No source-fidelity verdict. Local compilation is not source assimilation.')) + '</p>'
                           + semantic_details(audit)
                           + '<p>A generalization is not a source correction. Proposed missing conditions require separate independent repair review. '
                           'No proposed repair silently changes the original theorem.</p></section>')
        lesson = data['lessons'][name]
        rendered = declaration_lessons.render_unit(lesson, page, source_comparison=comparison)
        rendered = rendered.replace('<h1>', '<h2>').replace('</h1>', '</h2>')
        rendered = rendered.replace('href="index.html">Teaching coverage',
                                    f'href="{astis_site.relative_prefix(page)}lessons/index.html">Teaching coverage')
        lessons.append(rendered)
    return (f'<section id="{escape(item["id"])}" data-publication-item="{escape(item["id"])}">'
            f'<h2>{escape(item["title"])}</h2><p>{escape(source.get("attribution", ""))}</p>'
            '<p>' + declaration_lessons.source_citation_anchor(
                {'url': source['url'], 'label': source['edition'] + ' · ' + source['anchor']}, page)
            + f' · {escape(source["wording_status"])}</p>'
            + ('<details class="reader-ledger"><summary>Complete source statement and conditions</summary>'
               if progressive else '<h3>Complete source statement (Samplinglib restatement)</h3>')
            + f'<p>{escape(item["statement"])}</p>' + astis_site.list_html(item['assumptions']) + formulae
            + ('</details>' if progressive else '')
            + '<h2>Read the formalized proofs</h2><p>Each statement and proof below has its own closed Lean disclosure. '
            'Samplinglib parents, Mathlib calls and external mathematical sources are distinguished in each proof.</p>'
            + ''.join(lessons)
            + '<h3>Which proof obligations and prerequisites are covered?</h3><ul>'
            + ''.join(obligations) + '</ul></section>')


def source_proof_path(item: dict) -> str:
    return 'proofs/source-' + astis_site.slugify(item['id']) + '.html'


def companion_publication_block(items: list[dict], page: str) -> str:
    """One compact index; exact statements/proofs remain available on demand."""
    data = publication.inputs()
    names = {b['declaration'] for i in items for b in i['bindings']}
    reviewed = {b['declaration'] for i in items for b in i['bindings']
                if publication.verified_binding(b, data)}
    entries = []
    for item in items:
        target = astis_site.relative_prefix(page) + source_proof_path(item)
        units = ''.join(f'<li data-proof-declaration="{escape(b["declaration"])}">'
                        + escape(data['lessons'][b['declaration']]['title']) + '</li>'
                        for b in item['bindings'])
        entries.append(f'<details class="paper-verified-unit" id="{escape(item["id"])}" data-publication-item="{escape(item["id"])}"><summary>'
                       + escape(item['title']) + '</summary><ul>' + units + '</ul>'
                       + f'<p><a href="{escape(target)}">Read full statement and proof →</a></p>'
                       + '<p>Source assumptions, verification evidence and optional Lean are beside the proof on that page.</p></details>')
    return ('<section id="paper-lean-progress" class="paper-checked-work"><h2>3. What has been verified?</h2>'
            f'<p>{len(names)} source-mapped declarations; {len(reviewed)} independently reviewed. '
            'These are building blocks, not completed paper results.</p>'
            '<details class="paper-verified-index"><summary>Browse statements and their mathematical proofs</summary>'
            + ''.join(entries) + '</details></section>')


def enrich_site(output: Path) -> None:
    errors = publication.validate()
    if errors:
        raise ValueError('\n'.join(errors))
    research_model = samplewiki_navigation.load_model()
    research_titles = {samplewiki_navigation.PAPER_BASE + row['slug'] + '.html':
                       row.get('reader_label', row['title'])
                       for row in [*research_model['cases'], research_model['composition']]}
    groups = {}
    for item in publication.load():
        groups.setdefault(item['chapter_path'], []).append(item)
    for rel, items in groups.items():
        path = output / rel
        text = path.read_text(encoding='utf-8')
        # A common projection hook covers peer shelves without asking authors
        # to copy state into that library's generator or generated HTML.
        marker = status(items[0]['library'], items[0]['chapter'])
        text = re.sub(r'(<div class="tag-row">)<span class="status[^>]*>.*?</span>',
                      lambda m: m[1] + marker, text, count=1)
        # Explicit book order takes precedence over metadata fragment filenames.
        # Unordered legacy items retain their existing relative order.
        ordered = sorted(items, key=lambda i: i.get('source_order', float('inf')))
        if rel.startswith('example-cases/samplewiki/companions/'):
            for item in ordered:
                focused = source_proof_path(item)
                proof = source_card(item, focused)
                proof = proof.replace(f'<h2>{escape(item["title"])}</h2>', '', 1)
                breadcrumb = ('<nav class="reader-breadcrumb"><a href="../example-cases/samplewiki.html">SampleWiki</a> / '
                              f'<a href="{astis_site.relative_prefix(focused)}{rel}">{escape(research_titles.get(rel, "Research result"))}</a></nav>')
                body = breadcrumb + f'<h1>{escape(item["title"])}</h1>' + proof
                rendered = astis_site.page(item['title'], focused, body, active='SampleWiki',
                    extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">')
                astis_site.write_page(output, focused, source_lineage.canonical_shell(rendered, focused, output))
            block = companion_publication_block(ordered, rel)
            text, replaced = re.subn(
                r'<section id="paper-lean-progress" data-paper-publications="pending">.*?</section>',
                lambda _: block, text, count=1, flags=re.S)
            if not replaced:
                text = text.replace('</main>', block + '</main>', 1)
        else:
            block = ''.join(source_card(i, rel) for i in ordered)
            text = text.replace('</main>', block + '</main>', 1)
        path.write_text(text, encoding='utf-8', newline='\n')
        index = path.parent / 'index.html'
        if index.exists():
            shelf = index.read_text(encoding='utf-8')
            def card(match):
                value = match[0]
                if f'href="{path.name}"' in value:
                    value = re.sub(r'<span class="status[^>]*>.*?</span>', lambda _: marker, value, count=1)
                return value
            shelf = re.sub(r'<article class="library-chapter-card".*?</article>', card, shelf, flags=re.S)
            index.write_text(shelf, encoding='utf-8', newline='\n')
    projection = {i['id']: {'chapter_path': i['chapter_path'],
                            **publication.chapter_progress(i['library'], i['chapter'])}
                  for i in publication.load()}
    (output / 'data/publication-progress.json').write_text(json.dumps(projection, indent=2), encoding='utf-8')


def project_graph(builder) -> None:
    """Project source containers and missing mapped nodes; never upgrade proof badges."""
    data = publication.inputs()
    for item in publication.load():
        for binding in item['bindings']:
            decl = data['declarations'][binding['declaration']]
            ident = 'decl:' + decl.full_name
            if ident not in builder.nodes:
                # Mapping alone cannot confer a compiled badge or Registry count.
                builder.add(ident, 'declaration', decl.full_name, status='partial',
                            subtitle='Source-present publication; compiled badge not inferred',
                            url=astis_site.declaration_path(decl))
            builder.edge('module:' + decl.module, ident, 'declares')
    by_path = {i['chapter_path']: chapter_path_progress(i['chapter_path']) for i in publication.load()}
    by_path.update({str(Path(i['chapter_path']).parent / 'index.html').replace('\\', '/'):
                   publication.chapter_progress(i['library']) for i in publication.load()})
    for node in builder.nodes.values():
        p = by_path.get(node.get('url'))
        if p and node.get('kind') in {'library', 'library-chapter', 'chapter', 'frontier-case'}:
            node['status'] = 'partial' if p['status'] == 'partial' else 'planned'
            node['subtitle'] = p['label'] + ' · source fidelity and chapter closure separate'
            node['search'] += ' ' + node['subtitle'].lower()
            for item in publication.load():
                if item['chapter_path'] == node.get('url'):
                    node.setdefault('details', []).append({'label': 'Mapped source',
                        'value': item['title'] + ' · ' + item['source']['anchor']})
                    for b in item['bindings']:
                        node['details'].append({'label': 'Local component / boundary',
                            'value': b['declaration'] + ' · ' + b['boundary']})
                        # Correspondence overlay, not an implication extracted from Lean.
                        builder.edge('decl:' + b['declaration'], node['id'], SOURCE_EDGE)


def graph_input_digest() -> str:
    """Cheap rebuild freshness, independent of semantic-review admission."""
    data = publication.inputs()
    return publication.digest({'lean': astis_site.source_digest(), 'items': publication.load(),
        'cells': {b['cell']: data['cells'].get(b['cell']) for i in publication.load() for b in i['bindings']}})


def validate_graph(graph: dict, site: dict, items: list[dict] | None = None) -> list[str]:
    """Verify generated contribution coverage, not mathematical completeness.

    Expected facts are read from the existing site inventory/publication inputs;
    no separate dependency or status manifest is authored for this check.
    """
    items = publication.load() if items is None else items
    errors = []
    if graph.get('publication_inputs_sha256') != graph_input_digest():
        errors.append('Generated contribution graph is stale; rebuild the site')
    nodes = {n['id']: n for n in graph.get('nodes', [])}
    if len(nodes) != len(graph.get('nodes', [])):
        errors.append('Graph has duplicate node identities')
    edges = {(e['source'], e['target'], e['relation']) for e in graph.get('edges', [])}
    if len(edges) != len(graph.get('edges', [])):
        errors.append('Graph has duplicate edges')
    if any(a not in nodes or b not in nodes for a, b, _ in edges):
        errors.append('Graph has dangling edges')
    declarations = {d['full_name']: d for d in site.get('declarations', [])}
    registry = {d['local_decl']: d for d in site.get('registry_declarations', [])}
    modules = {m['name']: m for m in site.get('modules', [])}
    targets = {b['declaration'] for i in items for b in i['bindings']}

    def require_edge(a, b, relation):
        if (a, b, relation) not in edges:
            errors.append(f'Graph contribution missing {relation}: {a} → {b}')

    for name in sorted(targets):
        decl, ident = declarations.get(name), 'decl:' + name
        if not decl or nodes.get(ident, {}).get('kind') != 'declaration':
            errors.append(f'Graph contribution missing declaration: {name}')
            continue
        if decl.get('has_placeholder'):
            errors.append(f'Graph contribution contains placeholder: {name}')
        if not nodes[ident].get('url'):
            errors.append(f'Graph contribution missing reader link: {name}')
        module_id = 'module:' + decl['module']
        if nodes.get(module_id, {}).get('kind') != 'module':
            errors.append(f'Graph contribution missing owning module: {name}')
        require_edge(module_id, ident, 'declares')
        for imported in modules.get(decl['module'], {}).get('imports', []):
            if imported in modules:
                require_edge('module:' + imported, module_id, 'imports')
        if nodes[ident].get('status') == 'compiled' and not (
            decl.get('local_status') == 'Compiled'
            or registry.get(name, {}).get('status') == 'formalizedLocal'
        ):
            errors.append(f'Graph contribution has unsupported compiled badge: {name}')
    # Check both parents and actual scanned consumers, including edges to a
    # mapped contribution from an otherwise unmapped Registry declaration.
    for consumer, record in registry.items():
        for parent in record.get('dependencies', []):
            if consumer in targets or parent in targets:
                require_edge('decl:' + parent, 'decl:' + consumer, REFERENCE_EDGE)
                if ('decl:' + parent, 'decl:' + consumer, 'depends-on') in edges:
                    errors.append(f'Graph promotes a name scan to a formal dependency: {consumer}')
    for item in items:
        chapters = [n for n in nodes.values() if n.get('url') == item['chapter_path']
                    and n.get('kind') in {'chapter', 'library-chapter', 'frontier-case'}]
        if len(chapters) != 1:
            errors.append(f'Graph contribution needs one source chapter: {item["id"]}')
            continue
        expected = chapter_path_progress(item['chapter_path'])
        if chapters[0].get('status') != ('partial' if expected['status'] == 'partial' else 'planned'):
            errors.append(f'Graph chapter progress drift: {item["id"]}')
        for binding in item['bindings']:
            require_edge('decl:' + binding['declaration'], chapters[0]['id'], SOURCE_EDGE)
    return errors


def validate_site(output: Path) -> list[str]:
    errors = publication.validate()
    graph_path, site_path = output / 'data/underlying-lean-graph.json', output / 'data/site-data.json'
    if not graph_path.exists() or not site_path.exists():
        errors.append('Missing generated contribution graph/inventory; rebuild the site')
    else:
        errors.extend(validate_graph(json.loads(graph_path.read_text(encoding='utf-8')),
                                     json.loads(site_path.read_text(encoding='utf-8'))))
    for item in publication.load():
        path = output / item['chapter_path']
        if not path.exists():
            errors.append(f'Missing publication chapter {item["chapter_path"]}')
            continue
        text = path.read_text(encoding='utf-8')
        if item['chapter_path'].startswith('example-cases/samplewiki/companions/'):
            focused = source_proof_path(item)
            if focused not in text:
                errors.append(f'{path.name}: missing focused source proof link {focused}')
            target = output / focused
            if not target.exists():
                errors.append(f'Missing complete source/proof reader {focused}')
                continue
            # Moving a proof out of the index may never drop its source ledger,
            # exact authored mathematics, audit or adjacent Lean.
            text = target.read_text(encoding='utf-8')
        for marker in (f'data-publication-item="{item["id"]}"', 'Encoder–denoiser:',
                       'Source assumptions versus formal assumptions'):
            if marker not in text:
                errors.append(f'{path.name}: missing {marker}')
        for b in item['bindings']:
            if f'data-authored-declaration="{b["declaration"]}"' not in text:
                errors.append(f'{path.name}: missing adjacent authored proof {b["declaration"]}')
    return errors
