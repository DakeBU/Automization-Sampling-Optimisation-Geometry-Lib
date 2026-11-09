"""Bounded browser QA; the temporary local server closes on success or failure.

Run with a Python environment containing Playwright and installed Chromium/Edge.
Screenshots are ignored local evidence, not theorem or source-review certificates.
"""
from __future__ import annotations
import argparse
import functools
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--channel', default=None, help='e.g. msedge; otherwise installed Chromium')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    evidence = root / '.astis/subject-reader-browser'
    evidence.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root / '_site'))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f'http://127.0.0.1:{server.server_port}/'
    errors = []
    routes = ('sampling/index.html', 'libraries/optimisation/index.html',
              'lower-bounds/index.html', 'libraries/discrete-sampling/index.html')
    paper = 'example-cases/samplewiki/companions/slc-lsi-query-complexity.html'
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel=args.channel, headless=True)
            try:
                page = browser.new_page(viewport={'width': 1440, 'height': 1000})
                page.on('pageerror', lambda e: errors.append(str(e)))
                for width, height, label in ((1440,1000,'desktop'),(390,844,'mobile')):
                    page.set_viewport_size({'width':width,'height':height})
                    for index, route in enumerate(routes):
                        assert page.goto(base + route).status == 200
                        if index >= 2:
                            page.locator('main mjx-container').first.wait_for()
                        assert page.locator('main h1').count() == 1
                        assert page.locator('nav[aria-label="Subjects"] a').count() == 4
                        assert not page.locator('mjx-merror, [data-mjx-error]').count()
                        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), route
                        page.screenshot(path=str(evidence / f'{index}-{label}.png'), full_page=True)
                    assert page.goto(base + paper).status == 200
                    page.locator('#slc-cold-main mjx-container').first.wait_for()
                    # Expand actual source content: hidden equations must render too.
                    page.locator('main details').evaluate_all('(xs)=>xs.forEach(x=>x.open=true)')
                    page.evaluate('async()=>{if(window.MathJax?.startup?.promise) await MathJax.startup.promise;}')
                    assert page.locator('#lsi-main mjx-container').count() > 0
                    assert page.locator('#source-outline li').count() >= 12
                    assert not page.locator('mjx-merror, [data-mjx-error]').count()
                    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                    page.screenshot(path=str(evidence / f'paper-{label}.png'))
                    page.locator('#slc-cold-main').screenshot(path=str(evidence / f'statement-{label}.png'))
                    page.locator('#source-outline').screenshot(path=str(evidence / f'source-outline-{label}.png'))
                page.set_viewport_size({'width':1440,'height':1000})
                page.goto(base + 'proofs/random-scan-reversibility.html')
                page.locator('main mjx-container').first.wait_for()
                lean = page.locator('main details[data-inline-lean]').first
                assert not lean.evaluate('(x)=>x.open')
                lean.locator('summary').click()
                assert lean.evaluate('(x)=>x.open')
                assert 'theorem' in lean.inner_text() or 'Reversible' in lean.inner_text()
                page.screenshot(path=str(evidence / 'adjacent-lean.png'))
                page.goto(base + paper)
                page.locator('#source-outline').evaluate('(x)=>{for(let p=x.parentElement;p;p=p.parentElement)if(p.tagName==="DETAILS")p.open=true;}')
                page.get_by_role('link',name='Locate the planned source route in the graph').click()
                page.locator('[data-graph-detail] h2').wait_for()
                assert 'lower bounds' in page.locator('[data-graph-detail] h2').inner_text().lower()
                page.locator('[data-graph-svg]').screenshot(path=str(evidence / 'source-route-graph.png'))
                page.locator('[data-graph-fit]').click()
                page.locator('[data-graph-svg]').screenshot(path=str(evidence / 'source-route-graph-fit.png'))
                assert not errors, errors
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)
    print(json.dumps({'subjects':4,'viewports':[1440,390],'mathjax_errors':0,
                      'adjacent_lean_exercised':True,'source_outline_exercised':True,
                      'screenshots':str(evidence)}))


if __name__ == '__main__':
    main()
