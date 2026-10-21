#!/usr/bin/env python3
"""Offline browser gate for inline/display math, delayed loading and live prose.

Run after building: python website/scripts/test_math_browser.py --root SITE
Requires Playwright + Chromium. MATH_BROWSER_EXECUTABLE may select an installed
Chromium. Reports renderer errors across every unique formula in the site.
"""
from __future__ import annotations

import argparse
import functools
import html
import http.server
import json
import os
import re
import threading
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory

SKIP = {'pre', 'code', 'script', 'style', 'textarea', 'noscript', 'svg'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
FORMULA = re.compile(r'\\\((.*?)\\\)|\\\[(.*?)\\\]|\$\$(.*?)\$\$|(?<![\\$])\$([^$\n]+)\$(?!\$)', re.S)


class FormulaCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.formulas = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]

    def handle_data(self, text):
        if SKIP.intersection(self.stack):
            return
        text = re.sub(r'(?<!\\)\\{2,}\(([\s\S]*?)\\{2,}\)', lambda m: r'\(' + m[1] + r'\)', text)
        text = re.sub(r'(?<!\\)\\{2,}\[([\s\S]*?)\\{2,}\]', lambda m: r'\[' + m[1] + r'\]', text)
        for match in FORMULA.finditer(text):
            value = next(value for value in match.groups() if value is not None)
            self.formulas.append((value, match.group(2) is not None or match.group(3) is not None))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
    root = args.root.resolve()
    asset = next(root.rglob('vendor/mathjax@3.2.2/tex-mml-chtml.js'))
    asset_base = asset.parents[2].relative_to(root).as_posix()
    pages = []
    formulas = {}
    for path in sorted(root.rglob('*.html')):
        if 'blueprint' in path.relative_to(root).parts:
            continue
        collector = FormulaCollector()
        collector.feed(path.read_text(encoding='utf-8'))
        if collector.formulas:
            relative = path.relative_to(root).as_posix()
            pages.append((relative, len(collector.formulas)))
            for source, display in collector.formulas:
                formulas.setdefault((source, display), relative)
    if not pages:
        raise AssertionError('No mathematical pages found')

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(root)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    failures = []
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, executable_path=os.getenv('MATH_BROWSER_EXECUTABLE') or None)
            context = browser.new_context(viewport={'width': 1280, 'height': 900})
            # Every math engine request, font and autoloaded extension must work
            # without a CDN. Non-math external diagrams are outside this gate.
            context.route(re.compile(r'https?://(?!127\.0\.0\.1)'), lambda route: route.abort())
            page = context.new_page()
            page.goto(base + '/' + pages[0][0], wait_until='domcontentloaded')
            page.wait_for_function('Boolean(window.MathJax?.typesetPromise)', timeout=30000)
            page.evaluate('async () => { await MathJax.startup.promise; }')
            # Compile the entire generated math corpus, retaining the source URL
            # for every failure; this catches errors beyond a small route sample.
            items = [{'tex': key[0], 'display': key[1], 'path': path} for key, path in formulas.items()]
            for start in range(0, len(items), 200):
                failures.extend(page.evaluate('''async (items) => {
                  const errors = [];
                  for (const item of items) {
                    try {
                      const node = await MathJax.tex2chtmlPromise(item.tex, {display: item.display});
                      const error = node.querySelector('mjx-merror, [data-mjx-error]');
                      if (error) errors.push({...item, error: error.getAttribute('data-mjx-error') || error.textContent});
                    } catch (error) { errors.push({...item, error: String(error)}); }
                  }
                  return errors;
                }''', items[start:start + 200]))
            # Visit actual generated pages, including deep links and all major
            # page families, at desktop and mobile widths.
            chosen = {}
            for route, count in pages:
                family = route.split('/')[0]
                if family not in chosen or count > chosen[family][1]:
                    chosen[family] = (route, count)
            sample = [route for route, _ in list(chosen.values())[:16]]
            for route, _ in pages:
                if 'proximal-bouncy-particle' in route:
                    sample.append(route)
            for width in (1280, 390):
                page.set_viewport_size({'width': width, 'height': 900})
                for route in dict.fromkeys(sample):
                    page.goto(base + '/' + route, wait_until='domcontentloaded')
                    page.wait_for_function('Boolean(window.MathJax?.typesetPromise)', timeout=30000)
                    page.evaluate('async () => { await MathJax.startup.promise; }')
                    if not page.locator('mjx-container').count():
                        failures.append({'path': route, 'error': 'No rendered formulas'})
                    if page.locator('mjx-merror, [data-mjx-error]').count():
                        failures.append({'path': route, 'error': page.locator('mjx-merror').all_text_contents()})
                    if 'proximal-bouncy-particle' in route:
                        note = page.locator('li').filter(has_text='absolutely continuous').first
                        note.evaluate('(node) => { for (let p = node.parentElement; p; p = p.parentElement) if (p.matches("details")) p.open = true; }')
                        assert note.locator('mjx-container:not([display="true"])').count(), 'Renyi definition must be inline'
                        assert 'log integral' not in note.inner_text(), 'Raw Renyi definition leaked'
                        note.scroll_into_view_if_needed()
                        if args.report:
                            page.screenshot(path=str(args.report.with_name(f'pbps-math-{width}.png')), full_page=False)

            if (root / 'live/index.html').exists() and (root / 'data/research-workspaces.json').exists():
                page.goto(base + '/live/index.html', wait_until='domcontentloaded')
                select = page.locator('[data-rw-workspace]')
                select.select_option('ASTIS-SW-PBPS-2026')
                page.wait_for_selector('[data-rw-assumptions] mjx-container', timeout=30000)
                select.select_option('ASTIS-SW-GAUSSIAN-CLOUD-2026')
                page.wait_for_selector('[data-rw-assumptions] mjx-container', timeout=30000)
                assert page.locator('mjx-merror, [data-mjx-error]').count() == 0

            # Regression: a renderer that finishes after the old 3.2s timeout
            # must reveal the actual formula, with source code left untouched.
            fixture = ('<!doctype html><html><head><meta charset="utf-8">'
                f'<script src="/{asset_base}/math-reader.js"></script>'
                f'<script defer src="/{asset_base}/vendor/mathjax@3.2.2/tex-mml-chtml.js"></script>'
                '</head><body><p id="inline">Before \\(R_2(P\\Vert Q)=\\log\\int(\\frac{dP}{dQ})^2\\,dQ\\) after.</p>'
                '<p id="dollar">The estimate $x^2+\\alpha$ is inline.</p>'
                r'<p id="double">Before \\(\alpha+\beta\\) after.</p>'
                r'<div id="aligned">\[\begin{aligned}a&amp;=b\\[2pt]c&amp;=d\end{aligned}\]</div>'
                '<p id="coded"><code>\\(a_1+b_2\\)</code></p>'
                '<pre id="source"><code>\\(source_code\\)</code></pre>'
                '<textarea id="edit">\\(editable_source\\)</textarea>'
                '<div data-math-statement><span class="math-fallback">raw fallback</span>'
                '<span class="math-tex">\\[x^2\\]</span></div></body></html>')
            context.route('**/__math_fixture__.html', lambda route: route.fulfill(content_type='text/html', body=fixture))
            def delay_engine(route):
                # Delay only this fixture; all renderer assets still come from
                # the same site and the test exercises real network completion.
                import time
                time.sleep(3.5)
                route.continue_()
            context.route('**/tex-mml-chtml.js', delay_engine)
            page.goto(base + '/__math_fixture__.html', wait_until='domcontentloaded')
            page.evaluate('async () => { await MathJax.startup.promise; }')
            for selector in ('#inline', '#dollar', '#coded', '#double'):
                assert page.locator(selector + ' mjx-container:not([display="true"])').count() == 1, selector
            assert page.locator('#source mjx-container, #edit mjx-container').count() == 0
            assert page.locator('mjx-merror, [data-mjx-error]').count() == 0
            assert page.locator('[data-math-statement].math-rendered').count() == 1
            page.evaluate('''(text) => {
                const paragraph = document.createElement('p');
                paragraph.id = 'dynamic-math';
                paragraph.textContent = text;
                document.body.append(paragraph);
            }''', r'New \(\frac{a}{b}\) prose')
            page.wait_for_selector('#dynamic-math mjx-container', timeout=10000)
            browser.close()
    finally:
        server.shutdown()
    report = {'pages_with_math': len(pages), 'unique_formulas': len(formulas),
              'sampled_routes': sample, 'widths': [1280, 390], 'external_network': 'blocked', 'errors': failures}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'sampled_routes'}, ensure_ascii=False))
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
