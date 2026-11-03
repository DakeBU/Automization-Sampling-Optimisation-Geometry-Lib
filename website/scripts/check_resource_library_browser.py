"""Finite resource-reader QA; closes its own server and browser on every exit."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT / '_site')
    parser.add_argument('--browser-channel', choices=('msedge', 'chrome'))
    parser.add_argument('--evidence', type=Path, default=ROOT / '_browser-evidence/resources')
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(args.root.resolve()))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    runtime_errors = []
    checked = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel=args.browser_channel, headless=True)
            try:
                page = browser.new_page(viewport={'width': 1440, 'height': 1000})
                page.on('pageerror', lambda error: runtime_errors.append(str(error)))
                base = f'http://127.0.0.1:{server.server_port}/'
                for path in sorted((args.root / 'resources').rglob('*.html')):
                    rel = path.relative_to(args.root).as_posix()
                    response = page.goto(base + rel)
                    assert response.status == 200
                    page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                    page.evaluate('() => MathJax.startup.promise')
                    assert page.locator('mjx-merror, [data-mjx-error]').count() == 0, rel
                    assert page.locator('[data-resource-library]').count() == 1
                    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), rel
                    checked.append(rel)
                page.goto(base + 'resources/forum/algorithms.html')
                page.evaluate('() => MathJax.startup.promise')
                assert page.locator('mjx-container').count() > 0
                assert page.locator('[data-resource-entry]').count() == 67
                page.get_by_label('Find a title').fill('Sinkhorn')
                assert 0 < page.locator('[data-resource-entry]:visible').count() < 67
                page.get_by_label('Find a title').fill('no_matching_title_982756')
                assert page.locator('[data-resource-entry]:visible').count() == 0
                assert page.locator('[data-resource-count]').inner_text() == '0 of 67 references'
                page.get_by_label('Find a title').fill('')
                assert page.locator('[data-resource-entry]:visible').count() == 67
                page.goto(base + 'resources/optlib.html')
                assert page.locator('details[open]').count() == 0
                page.locator('summary').filter(has_text='upstream modules').first.click()
                assert page.get_by_role('link', name='Optlib/Differential/Calculation.lean', exact=True).is_visible()
                page.screenshot(path=str(args.evidence / 'optlib-desktop.png'), full_page=True)
                # Follow a real pre-existing reader, not a synthetic Lean demo.
                lesson = page.locator('a[href^="../lessons/"]').first
                assert lesson.count() == 1
                lesson.click()
                page.evaluate('() => MathJax.startup.promise')
                assert page.locator('mjx-container').count() > 0
                assert page.locator('mjx-merror, [data-mjx-error]').count() == 0
                for name in ('index', 'optimisation', 'sampling', 'geometry', 'forum/algorithms'):
                    page.set_viewport_size({'width': 412, 'height': 915})
                    page.goto(base + 'resources/' + name + '.html')
                    page.evaluate('() => MathJax.startup.promise')
                    page.wait_for_timeout(400)
                    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), name
                    page.screenshot(path=str(args.evidence / (name.replace('/', '-') + '-mobile.png')), full_page=True)
                page.set_viewport_size({'width': 1440, 'height': 1000})
                page.goto(base + 'resources/index.html')
                page.get_by_text('Sources, coverage and reuse boundaries', exact=True).click()
                with page.expect_download() as download:
                    page.get_by_role('link', name='Download pinned bibliography and fingerprints').click()
                data = json.loads(Path(download.value.path()).read_text(encoding='utf-8'))
                assert sum(len(s['items']) for s in data['forum']['sections']) == 133
                page.screenshot(path=str(args.evidence / 'hub-desktop.png'), full_page=True)
                assert not runtime_errors, runtime_errors
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)
    print(json.dumps({'pages': checked, 'mathjax_errors': 0, 'search_and_folds': True,
                      'existing_proof_reader': True, 'metadata_download': True,
                      'mobile_overflow': False, 'runtime_errors': runtime_errors}))


if __name__ == '__main__':
    main()
