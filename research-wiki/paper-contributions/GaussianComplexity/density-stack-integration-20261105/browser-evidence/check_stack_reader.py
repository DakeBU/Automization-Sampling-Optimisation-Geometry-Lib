"""Bounded real-browser acceptance of the unchanged Gaussian reader stack."""
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
OUT = ROOT / '.astis/huanjian-gc-integration-20261105/browser' / ('stack-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'website/scripts'))
sys.path.insert(0, str(ROOT / 'tools'))
import inline_lean

PREFIX = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.'
TARGETS = {
    'eq24': PREFIX + 'EvaluatedGaussian.selected_gaussian_value',
    'b7': PREFIX + 'SingleBlockSeparation.single_block_separation',
    'density': PREFIX + 'MixtureDensities.actual_mixture_densities',
    'a1': PREFIX + 'SphericalPoisson.spherical_poisson_moments',
    'numerator': 'selected_numerator_value',
}
rows = {r['declaration']: r for r in json.loads((SITE / 'data/declaration-exposition.json').read_text())}
declarations = inline_lean.declarations()
report = {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
          'mode': 'HTTP with installed headless Chrome, isolated temporary profile; external requests blocked',
          'pages': [], 'graphs': [], 'errors': [], 'screenshots': []}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(SITE)))
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f'http://127.0.0.1:{server.server_port}/'


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


try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,
                                   executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        report['browser_version'] = browser.version
        context = browser.new_context(viewport={'width': 1440, 'height': 1000})
        context.route(re.compile(r'https?://(?!127\.0\.0\.1)'), lambda route: route.abort())
        page = context.new_page()
        page.on('pageerror', lambda e: report['errors'].append(str(e)))
        for width in (1440, 390):
            page.set_viewport_size({'width': width, 'height': 1000 if width > 400 else 844})
            for short, name in TARGETS.items():
                route = rows[name]['page']
                assert page.goto(base + route, wait_until='domcontentloaded').status == 200
                math_ready(page)
                assert 'Lean gate passed' in page.locator('.verification-strip').text_content()
                article = page.locator(f'article[data-authored-declaration="{name}"]')
                assert article.count() == 1
                assert article.locator('details[open]').count() == 0
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
                assert article.locator('.assumption-ledger[open]').count() == 1
                article.locator('.assumption-ledger > summary').click()
                steps = article.locator('details.reader-proof-disclosure')
                if steps.count():
                    steps.first.locator('summary').first.click()
                    assert steps.first.locator('mjx-container').count() > 0
                    steps.first.locator('summary').first.click()
                statement.locator('summary').first.click()
                assert statement.locator('code.language-lean').first.is_visible()
                statement.locator('summary').first.click()
                proof.locator('summary').first.click()
                proof.locator('summary').first.scroll_into_view_if_needed()
                assert proof.locator('code.language-lean').first.is_visible()
                no_page_overflow(page)
                if short in ('eq24', 'b7', 'density'):
                    screenshot(page, f'{short}-{width}-proof')
                module_href = proof.locator('a').filter(has_text='Exact module and namespace context').get_attribute('href')
                module_url = urljoin(page.url, module_href)
                source_href = proof.locator('a[download]').first.get_attribute('href')
                downloaded = context.request.get(urljoin(page.url, source_href))
                assert downloaded.status == 200
                assert downloaded.body() == (ROOT / declarations[name].source_file).read_bytes()
                assert page.goto(module_url, wait_until='domcontentloaded').status == 200
                assert page.locator('#complete-module-source').count() == 1
                page.locator('#complete-module-source > details > summary').click()
                assert name.split('.')[-1] in page.locator('#complete-module-source').inner_text()
                if short == 'density':
                    page.locator('#complete-module-source').scroll_into_view_if_needed()
                    screenshot(page, f'{short}-{width}-module')
                report['pages'].append({'target': name, 'route': route, 'width': width,
                                        'closed_initially': True, 'adjacent_exact_statement_and_proof': True,
                                        'full_module_and_download_verified': True, 'page_overflow': False})

            chapter = 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html'
            assert page.goto(base + chapter, wait_until='domcontentloaded').status == 200
            math_ready(page)
            main = page.locator('#gaussian-complexity-determinant')
            main.evaluate('(node) => { for (let p=node.parentElement;p;p=p.parentElement) if(p.matches("details"))p.open=true; }')
            boundary = page.locator('#paper-main-results').text_content()
            assert 'worst-case deterministic query cap' in boundary
            assert 'not an expected-cost lower bound without a separate reduction' in boundary
            assert 'B.7' in boundary and 'density' in boundary
            no_page_overflow(page)
            main.scroll_into_view_if_needed()
            screenshot(page, f'case-boundary-{width}')
            index = page.locator('#paper-lean-progress')
            index.scroll_into_view_if_needed()
            screenshot(page, f'source-index-{width}')
            for short in ('eq24', 'b7', 'density'):
                slug = {'eq24': 'evaluated-eq24', 'b7': 'single-block-separation', 'density': 'mixture-densities'}[short]
                link = index.locator(f'a[href$="source-huanjian-{slug}.html"]')
                assert link.count() == 1
                href = urljoin(page.url, link.get_attribute('href'))
                assert context.request.get(href).status == 200
                assert page.goto(href, wait_until='domcontentloaded').status == 200
                math_ready(page)
                assert page.locator(f'article[data-authored-declaration="{TARGETS[short]}"]').count() == 1
                no_page_overflow(page)
                assert page.goto(base + chapter, wait_until='domcontentloaded').status == 200
                index = page.locator('#paper-lean-progress')

            for short in ('eq24', 'b7', 'density'):
                name = TARGETS[short]
                ident = 'decl:' + name
                route = 'lean-foundations.html?view=lean&focus=' + quote(ident, safe='') + '&q=' + quote(name, safe='')
                assert page.goto(base + route, wait_until='domcontentloaded').status == 200
                page.wait_for_selector('.ulg-canvas[data-local="true"]')
                assert page.locator(f'.ulg-node[data-id="{ident}"]').count() == 1
                assert page.locator('.ulg-edge[data-relation="source reference (scanner)"][data-evidence="formal"]').count() == 0
                assert page.locator('.ulg-edge[data-relation="source correspondence; not a Lean dependency"][data-evidence="formal"]').count() == 0
                assert page.locator('.ulg-node .label').evaluate_all('(nodes)=>nodes.every(n=>n.getBBox().x+n.getBBox().width<=Number(n.parentNode.querySelector("rect").getAttribute("width")))')
                no_page_overflow(page)
                page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
                screenshot(page, f'{short}-{width}-graph')
                report['graphs'].append({'target': name, 'width': width, 'one_canonical_node': True,
                                         'reference_and_source_edges_not_formal': True,
                                         'edges': page.locator('.ulg-edge').evaluate_all('(nodes)=>nodes.map(n=>({relation:n.dataset.relation,evidence:n.dataset.evidence}))')})
        assert not report['errors'], report['errors']
        browser.close()
        report['status'] = 'passed'
except Exception as e:
    report['status'] = 'failed'
    report['failure'] = repr(e)
    raise
finally:
    server.shutdown()
    server.server_close()
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': report.get('status'), 'pages': len(report['pages']), 'graphs': len(report['graphs']),
                      'screenshots': len(report['screenshots']), 'report': str(OUT / 'report.json')}))
