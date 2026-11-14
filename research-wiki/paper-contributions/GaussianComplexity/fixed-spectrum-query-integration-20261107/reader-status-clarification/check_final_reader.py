"""Bounded real-browser acceptance of the actual fixed-spectrum same-rotation precision reply reader."""
import functools
import datetime
import hashlib
import http.server
import json
from pathlib import Path
import re
import subprocess
import sys
import threading
from urllib.parse import quote, urljoin, urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path.cwd()
SITE = ROOT / '_site'
OUT = ROOT / '.astis/huanjian-gc-fixed-spectrum-query-integration-20261107/browser' / ('live-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'website/scripts'))
sys.path.insert(0, str(ROOT / 'tools'))
import inline_lean

PREFIX = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.'
TARGETS = {'actual': PREFIX + 'FixedSpectrumAffine.actual_affine_precision_query'}
rows = {r['declaration']: r for r in json.loads((SITE / 'data/declaration-exposition.json').read_text())}
declarations = inline_lean.declarations()
report = {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
          'mode': 'HTTP with installed headless Chrome, isolated temporary profile; external requests blocked',
          'pages': [], 'graphs': [], 'errors': [], 'screenshots': []}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(SITE)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}/'
expected_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
metadata_path = SITE / 'data/build-metadata.json'
metadata = json.loads(metadata_path.read_text())
assert metadata['git']['commit'] == expected_commit
actual_gate = json.loads((ROOT / '.astis/site-lean-gate.json').read_text())
assert actual_gate['passed'] and metadata['source_digest'] == actual_gate['source_digest']
assert metadata['gate']['passed'] and metadata['gate']['current']
report['mode'] = 'Actual local final site over HTTP with isolated installed Chrome; external hosts blocked'
report['site_metadata'] = metadata
report['site_metadata_sha256'] = hashlib.sha256(metadata_path.read_bytes()).hexdigest()
report['actual_compiled_gate_commit'] = actual_gate['commit']
report['actual_compiled_source_digest'] = actual_gate['source_digest']
report['compilation_boundary'] = 'Actual canonical gate at the separately named immutable commit; exact current Lean source digest matches. Current metadata-only HEAD is not relabeled as an additional build.'
report['visible_source_index_clicks'] = []
report['external_GitHub_HTML_checked'] = False
report['external_source_route'] = 'Historical GitHub HTML504 host route remains frozen; Own-site complete module/downloads are checked against actual source and an immutable Git object; external GitHub URL syntax is separately conditional and external HTML is not checked.'

def screenshot(page, name):
    path = OUT / (name + '.png')
    page.screenshot(path=str(path))
    report['screenshots'].append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})


def math_ready(page):
    page.wait_for_function('Boolean(window.MathJax?.startup?.promise)', timeout=30000)
    page.evaluate('() => MathJax.startup.promise')
    assert page.locator('mjx-container').count() > 0
    assert page.locator('mjx-merror, [data-mjx-error]').count() == 0


def no_page_overflow(page):
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), page.url


# Preconditions bind the actual future run to the exact reviewed inputs.
expected_inputs = {
    'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAffine.lean': '0a46e7bae8d8a9298ba3748a7c94db2f8874f1a4b318169a315c466d86b4a56c',
    'Tests/GaussianComplexityFixedSpectrumAffine.lean': '9b237a4f007e82e36ae9db226b05be4d29e7fa4fc109dfec7a186a97fc2a2aeb',
    'website/content/declaration_lessons/huanjian-fixed-spectrum-query.json': '58eca0d6728d3279b1a1ae652ad92ab36008d5078af2ea77e04059f78de48f38',
    'website/content/publications/huanjian-fixed-spectrum-query.json': '20f8717eed5524ecffdb0ee60252004df66dfc35e68f7121662e6a3c1992d679',
}
for path, digest in expected_inputs.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
unit = json.loads((ROOT / 'website/content/declaration_lessons/huanjian-fixed-spectrum-query.json').read_text())['units'][0]
assert unit['declaration'] == TARGETS['actual'] and unit['astis_dependencies'] == []
assert unit['mathlib_dependencies'] and len(unit['steps']) == 5
proposal = json.loads((ROOT / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-query-integration-20261107/independent-integration-reader-review/preparation-report.json').read_text())
# Independent status-only repair preserves the entire old mechanism and original v2 review.
clarification_path = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-query-integration-20261107/reader-status-clarification/proposal.json'
assert hashlib.sha256(clarification_path.read_bytes()).hexdigest() == '14996e480e96083de23659bc0150efa7b87e19f4265ec889d3a4073a0a464a7e'
clarification = json.loads(clarification_path.read_text())
assert hashlib.sha256((ROOT / 'website/content/functor_hypergraph.json').read_bytes()).hexdigest() == clarification['planned_after_raw_sha256'] == '94b56f87136ca97820893e5531d16d36334d44bc6b9e41981d39aa700f8fe782'
graph_payload = json.loads((SITE / 'data/underlying-lean-graph.json').read_text())
graph_lookup = {node['id']: node for node in graph_payload['nodes']}
model = json.loads((ROOT / 'website/content/functor_hypergraph.json').read_text())
memory = json.loads((ROOT / 'website/content/graph_memory_index.json').read_text())
family = next(f for f in memory['families'] if f['id'] == 'family:gaussian-oracle-hardness')
candidate_modules = ['module:' + PREFIX + name for name in ('FirstOrderQuery', 'FixedSpectrumAffine')]
bridge = 'transport:gaussian-quadratic-oracle-factorization'
for module in candidate_modules:
    binding = [b for b in family['compiled_substrate_bindings'] if b['node'] == module.removeprefix('module:')]
    assert len(binding) == 1 and binding[0]['edges'] == [bridge]
    assert binding[0]['role'] and binding[0]['truth_boundary']


def focused_entry(page, view, ident, query):
    route = 'lean-foundations.html?view=' + view + '&focus=' + quote(ident, safe='') + '&q=' + quote(query, safe='')
    assert page.goto(base + route, wait_until='domcontentloaded').status == 200
    page.wait_for_selector('.ulg-canvas[data-view="' + view + '"][data-local="true"]')
    selected = page.locator('.ulg-node.selected[data-id="' + ident + '"]')
    selected.wait_for()
    page.wait_for_function("document.querySelector('.ulg-canvas>small').textContent.includes('Focused result at readable scale')")
    math_ready(page)
    page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
    node_box = selected.locator('rect').bounding_box()
    canvas_box = page.locator('[data-graph-canvas]').bounding_box()
    assert node_box['width'] >= 160
    assert node_box['x'] >= canvas_box['x'] - 1 and node_box['x'] + node_box['width'] <= canvas_box['x'] + canvas_box['width'] + 1
    selected.click()
    assert page.locator('[data-graph-detail] h2').text_content().strip()
    no_page_overflow(page)
    return {'route': route, 'node_box': node_box, 'canvas_box': canvas_box,
            'actual_selected_node_click': True,
            'readable_deep_link_caption': page.locator('.ulg-canvas>small').text_content(),
            'scope': 'Actual selected readable entry and native click; explicit Fit is a separate all-context overview, not an all-label readability claim. No manual touch gesture is tested.'}


try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        report['browser_version'] = browser.version
        context = browser.new_context(viewport={'width': 1440, 'height': 1000})
        context.route(re.compile(r'https?://(?!127\.0\.0\.1:)'), lambda route: route.abort())
        page = context.new_page()
        page.on('pageerror', lambda error: report['errors'].append(str(error)))
        for width in (1440, 390):
            page.set_viewport_size({'width': width, 'height': 1000 if width > 400 else 844})
            for short, name in TARGETS.items():
                route = rows[name]['page']
                assert page.goto(base + route, wait_until='domcontentloaded').status == 200
                math_ready(page)
                assert expected_commit[:12] in page.locator('.verification-strip').text_content()
                article = page.locator(f'article[data-authored-declaration="{name}"]')
                assert article.count() == 1 and article.locator('details[open]').count() == 0
                assert article.locator('.reader-main-equation mjx-container').count() == 1
                statement = article.locator(f'details.inline-lean-statement[data-inline-lean="{name}"]')
                proof = article.locator(f'details.inline-lean-proof[data-inline-lean="{name}"]')
                exact = inline_lean.display_source(declarations[name].source_text)
                signature, _ = inline_lean.split_statement(exact)
                assert statement.locator('code.language-lean').first.text_content() == signature
                assert proof.locator('code.language-lean').first.text_content() == exact
                assert article.locator('.reader-first-pass details.inline-lean-statement').count() == 1
                assert article.locator('.lean-verification details.inline-lean-proof').count() >= 1
                no_page_overflow(page)
                article.locator('.reader-first-pass').scroll_into_view_if_needed()
                screenshot(page, f'{short}-{width}-first')
                article.locator('.assumption-ledger > summary').click()
                assumptions = article.locator('.assumption-ledger')
                assert assumptions.get_attribute('open') is not None
                assumption_text = assumptions.text_content()
                assert 'reference condition number' in assumption_text and 'same rotation' in assumption_text
                assert 'zero-based' in assumption_text and 'private randomness' in assumption_text
                no_page_overflow(page)
                assumptions.locator(':scope > summary').click()
                steps = article.locator('details.reader-proof-disclosure')
                assert steps.count() == 5
                for step_index in range(steps.count()):
                    step = steps.nth(step_index)
                    step.locator('summary').first.click()
                    assert step.locator('mjx-container').count() > 0
                    no_page_overflow(page)
                    if step_index == 3:
                        step.scroll_into_view_if_needed()
                        screenshot(page, f'{short}-{width}-proof-step4')
                    step.locator('summary').first.click()
                provenance = article.locator('details.proof-reader-provenance')
                assert provenance.count() == 1
                provenance.locator(':scope > summary').click()
                assert provenance.locator('ul').first.locator('li').count() == 0
                for dependency in unit['mathlib_dependencies']:
                    assert dependency in provenance.text_content(), dependency
                assert 'Samplinglib parents called' in provenance.text_content() and 'Mathlib API called' in provenance.text_content()
                provenance.scroll_into_view_if_needed()
                no_page_overflow(page)
                screenshot(page, f'{short}-{width}-standard-reuse')
                provenance.locator(':scope > summary').click()
                statement.locator('summary').first.click()
                assert statement.locator('code.language-lean').first.is_visible()
                statement.locator('summary').first.click()
                proof.locator('summary').first.click()
                proof.locator('summary').first.scroll_into_view_if_needed()
                assert proof.locator('code.language-lean').first.is_visible()
                no_page_overflow(page)
                screenshot(page, f'{short}-{width}-proof')
                module_href = proof.locator('a').filter(has_text='Exact module and namespace context').get_attribute('href')
                module_url = urljoin(page.url, module_href)
                source_href = proof.locator('a[download]').first.get_attribute('href')
                downloaded = context.request.get(urljoin(page.url, source_href))
                actual_source = (ROOT / declarations[name].source_file).read_bytes()
                assert downloaded.status == 200 and downloaded.body() == actual_source
                git_source = subprocess.check_output(['git', 'show', expected_commit + ':' + str(declarations[name].source_file)])
                assert git_source == actual_source
                immutable_link_verified = None
                if urlsplit(module_url).netloc == 'github.com':
                    expected = metadata['git']['web_root'] + '/blob/' + expected_commit + '/' + str(declarations[name].source_file)
                    assert module_url.startswith(expected + '#L'), module_url
                    immutable_link_verified = True
                    module_url = base + 'modules/' + inline_lean.base.slugify(declarations[name].module) + '.html#complete-module-source'
                assert page.goto(module_url, wait_until='domcontentloaded').status == 200
                assert page.locator('#complete-module-source').count() == 1
                page.locator('#complete-module-source > details > summary').click()
                assert page.locator('#complete-module-source pre > code').text_content().encode() == actual_source
                page.locator('#complete-module-source').scroll_into_view_if_needed()
                no_page_overflow(page)
                screenshot(page, f'{short}-{width}-module')
                report['pages'].append({'target': name, 'route': route, 'width': width,
                    'closed_initially': True, 'adjacent_exact_statement_and_proof': True,
                    'five_steps_rendered_and_opened_without_fullpage_overflow': True,
                    'ASTIS_proof_parents': [], 'standard_Mathlib_reuse_context_checked': unit['mathlib_dependencies'],
                    'full_module_and_download_verified': True,
                    'immutable_git_object_source_bytes_verified': True,
                    'immutable_source_link_commit_and_path_verified': immutable_link_verified,
                    'immutable_source_link_check': 'verified' if immutable_link_verified else 'not_executed_own_site_route',
                    'external_GitHub_HTML_checked': False, 'page_overflow': False})

            chapter = 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html'
            assert page.goto(base + chapter, wait_until='domcontentloaded').status == 200
            math_ready(page)
            main = page.locator('#gaussian-complexity-eigenbasis')
            main.evaluate('(node) => { for (let p=node.parentElement;p;p=p.parentElement) if(p.matches("details"))p.open=true; }')
            boundary = main.text_content()
            for phrase in ('The full Theorem 4.1 lower bound remains open',
                'actual Eq11/Remark4.2 pointwise precursor', 'same hidden',
                'The subscript2 is the reference condition number, not two calls or an inverse oracle',
                'actual two-hidden-input consumer', 'reference2 replies',
                'Section 4.4 limits this uniform-Krylov/test analysis',
                'not an impossibility theorem for stronger fixed-spectrum lower bounds'):
                assert phrase in boundary, phrase
            determinant_text = page.locator('#gaussian-complexity-determinant').text_content()
            for phrase in ('The full Theorem 3.1 lower bound remains open', 'worst-case deterministic query cap',
                'not an expected-cost lower bound without a separate reduction', 'Actual amplified TV Ex72',
                'actual pointwise first-order reconstruction'):
                assert phrase in determinant_text, phrase
            no_page_overflow(page)
            main.scroll_into_view_if_needed()
            screenshot(page, f'case-boundary-{width}')
            index = page.locator('#paper-lean-progress')
            index.scroll_into_view_if_needed()
            screenshot(page, f'source-index-{width}')
            itemid = 'huanjian-fixed-spectrum-query'
            outer = index.locator('details.paper-verified-index')
            if outer.get_attribute('open') is None:
                outer.locator(':scope > summary').click()
            sourceunit = outer.locator(f'details.paper-verified-unit[data-publication-item="{itemid}"]')
            if sourceunit.get_attribute('open') is None:
                sourceunit.locator(':scope > summary').click()
            link = sourceunit.locator(f'a[href$="source-{itemid}.html"]')
            assert link.count() == 1 and link.is_visible()
            sourceunit.scroll_into_view_if_needed()
            screenshot(page, f'actual-{width}-source-index-open')
            href = urljoin(page.url, link.get_attribute('href'))
            assert context.request.get(href).status == 200
            link.click()
            page.wait_for_url('**/proofs/source-' + itemid + '.html')
            math_ready(page)
            assert page.locator(f'article[data-authored-declaration="{TARGETS["actual"]}"]').count() == 1
            report['visible_source_index_clicks'].append({'target': TARGETS['actual'], 'width': width, 'actual_click': True})
            no_page_overflow(page)

            name = TARGETS['actual']
            ident = 'decl:' + name
            own_module = 'module:' + PREFIX + 'FixedSpectrumAffine'
            assert ident in graph_lookup and graph_lookup[ident]['kind'] == 'declaration'
            assert own_module in graph_lookup and graph_lookup[own_module]['kind'] == 'module'
            assert len([edge for edge in graph_payload['edges'] if edge['source'] == own_module and edge['target'] == ident and edge['relation'] == 'declares']) == 1
            assert not [edge for edge in graph_payload['edges'] if edge['target'] == ident and edge['source'].startswith('decl:AutoSamplingTheory.') and edge['relation'] in ('imports', 'declares')]
            focused = focused_entry(page, 'lean', ident, name)
            assert page.locator(f'.ulg-node[data-id="{ident}"]').count() == 1
            assert page.locator(f'.ulg-node[data-id="{own_module}"]').count() == 1
            assert page.locator('.ulg-edge[data-relation="source reference (scanner)"][data-evidence="formal"]').count() == 0
            assert page.locator('.ulg-edge[data-relation="source correspondence; not a Lean dependency"][data-evidence="formal"]').count() == 0
            page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
            screenshot(page, f'actual-{width}-graph-focused')
            report['graphs'].append({'target': ident, 'width': width, 'one_canonical_target': True,
                'canonical_module_owner': own_module, 'ASTIS_proof_parents': [],
                'Std_dependencies_source': 'The reader lists the actual Mathlib calls; no ASTIS parent is invented from conceptual similarity.',
                'focused_entry': focused, 'scanner_source_edges_not_formal': True,
                'semantic_boundary': 'Module ownership/imports are structural; old FirstOrderQuery is a conceptual sibling, not a mathematical parent.'})

            native_node = graph_lookup[bridge]
            assert native_node['kind'] == 'concept-bridge'
            assert native_node['hyperedge'] == next(edge for edge in model['hyperedges'] if edge['id'] == bridge)
            assert native_node['hyperedge']['status'] == 'not-Lean-certified' and native_node['hyperedge']['formal_refs'] == []
            for module in candidate_modules:
                assert module in native_node['candidate_substrates']
                assert len([edge for edge in graph_payload['edges'] if edge['source'] == module and edge['target'] == bridge and edge['relation'] == 'reuse search candidate; not a proof dependency']) == 1
            concept_focused = focused_entry(page, 'functor', bridge, 'Quadratic observations factor')
            assert page.locator(f'.ulg-node[data-id="{bridge}"]').count() == 1
            for module in candidate_modules:
                assert page.locator(f'.ulg-node[data-id="{module}"]').count() == 1
            detail = page.locator('[data-graph-detail]')
            page.wait_for_function("document.querySelector('[data-graph-detail]').dataset.kind === 'concept-bridge'")
            hyperedge_section = detail.locator('.ulg-hyperedge')
            assert hyperedge_section.is_visible()
            assert hyperedge_section.locator('h3').first.text_content().strip() == 'Joint-input hyperedge'
            actual_rows = detail.locator('.ulg-details > div').evaluate_all('(nodes)=>Object.fromEntries(nodes.map(n=>[n.querySelector("dt").textContent,n.querySelector("dd").textContent]))')
            for label, field in [('Mechanism','mechanism'),('Hypothesis Map','hypothesis_map'),('Conclusion Map','conclusion_map'),('Failure Boundary','failure_boundary')]:
                assert actual_rows[label] == native_node['hyperedge'][field], label
            assert 'not-Lean-certified' in hyperedge_section.locator('.ulg-warning').text_content()
            source_hrefs = hyperedge_section.locator('a').evaluate_all('(nodes)=>nodes.map(n=>n.getAttribute("href"))')
            assert all(source['url'] in source_hrefs for source in native_node['sources'])
            assert '0<epsilon<=1/16' in actual_rows['Hypothesis Map'] and '0<epsilon<=1/10' in actual_rows['Hypothesis Map']
            assert 'SAME unknown O' in actual_rows['Hypothesis Map']
            assert '2T<n' in actual_rows['Hypothesis Map'] and 'downstream' in actual_rows['Hypothesis Map']
            assert 'not a premise of the current pointwise Lean theorem' in actual_rows['Conclusion Map']
            assert 'expected' in actual_rows['Failure Boundary'] and 'target' in actual_rows['Failure Boundary']
            assert actual_rows['Conclusion Map'] == clarification['planned_value']
            assert 'FirstOrderQuery' in actual_rows['Conclusion Map'] and 'FixedSpectrumAffine' in actual_rows['Conclusion Map']
            assert 'reference2 meaning condition number2' in actual_rows['Conclusion Map']
            assert 'fixed-spectrum affine identity is source-only here' not in actual_rows['Conclusion Map']
            incident = page.locator('.ulg-edge').evaluate_all('(nodes)=>nodes.map(n=>({relation:n.dataset.relation,evidence:n.dataset.evidence}))')
            assert not [edge for edge in incident if edge['relation'] in ('joint conceptual input','conditional conceptual output','reuse search candidate; not a proof dependency') and edge['evidence'] == 'formal']
            for module in candidate_modules:
                assert detail.locator(f'button[data-jump="{module}"]').count() == 1
            no_page_overflow(page)
            page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
            screenshot(page, f'conceptual-{width}-graph-focused')
            detail.scroll_into_view_if_needed()
            screenshot(page, f'conceptual-{width}-details')
            for label, suffix in [('Hypothesis Map','hypotheses'),('Failure Boundary','failure-boundary')]:
                row = detail.locator('.ulg-details > div').filter(has=page.locator('dt', has_text=label))
                assert row.count() == 1
                row.scroll_into_view_if_needed()
                no_page_overflow(page)
                screenshot(page, f'conceptual-{width}-{suffix}')
            report['graphs'].append({'target': bridge, 'width': width,
                'one_existing_typed_bridge': True, 'existing_hyperedge_byte_source_unchanged': True,
                'two_candidate_modules': candidate_modules, 'candidate_modules_are_dashed_search_incidence_only': True,
                'actual_semantic_rows_exact': actual_rows, 'actual_source_hrefs': source_hrefs,
                'focused_entry': concept_focused, 'actual_incident_edge_semantics': incident,
                'scope': 'Same independently source-reviewed algebraic mechanism, no new bridge/discovery or formal implication. Existing strict2T<n belongs only to determinant information law, not this same-O pointwise converter.'})
        assert not report['errors'], report['errors']
        browser.close()
        report['status'] = 'passed'
except Exception as error:
    report['status'] = 'failed'
    report['failure'] = repr(error)
    raise
finally:
    server.shutdown()
    server.server_close()
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': report.get('status'), 'pages': len(report['pages']),
        'graphs': len(report['graphs']), 'screenshots': len(report['screenshots']), 'report': str(OUT / 'report.json')}))
