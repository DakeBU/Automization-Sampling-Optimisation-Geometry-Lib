"""Bounded real-browser QA for the paired pilot; always closes its preview server."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
HUB = 'benchmarks/samplingoptimisationgeometrybench/'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT / '_site')
    parser.add_argument('--browser-channel', choices=('msedge', 'chrome'))
    parser.add_argument('--evidence', type=Path, default=ROOT / '_browser-evidence/sog-bench')
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(args.root.resolve()))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel=args.browser_channel, headless=True)
            context = browser.new_context(permissions=['clipboard-read', 'clipboard-write'],
                                          viewport={'width': 1400, 'height': 1000})
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            base = f'http://127.0.0.1:{server.server_port}/'
            for path in ('index.html', 'natural-language/index.html', 'lean/index.html'):
                response = page.goto(base + HUB + path)
                assert response.status == 200
                assert page.locator('[data-sog-bench]').count() == 1
            page.goto(base + HUB + 'index.html')
            with page.expect_download() as download:
                page.get_by_role('link', name='Prompt-only JSONL', exact=True).click()
            path = download.value.path()
            records = [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines()]
            assert len(records) == 19 and all('lean_reference' not in r and 'steps' not in r for r in records)
            with page.expect_download() as reviewed_download:
                page.get_by_role('link', name='editorially reviewed prompts', exact=True).click()
            reviewed = [json.loads(line) for line in Path(reviewed_download.value.path()).read_text(encoding='utf-8').splitlines()]
            assert len(reviewed) == 19 and {r['id'] for r in reviewed} == {f'sogb-{i:03d}' for i in range(1,16)}
            page.screenshot(path=str(args.evidence / 'overview-desktop.png'), full_page=True)
            for identity in ('sogb-001', 'sogb-002', 'sogb-003', 'sogb-015'):
                page.goto(base + HUB + identity + '.html')
                page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                page.evaluate('() => MathJax.startup.promise')
                assert page.locator('details[open]').count() == 0
                page.locator('summary', has_text='Reference mathematical proof').click()
                page.wait_for_timeout(300)
                assert page.locator('mjx-container').count() > 0
                assert page.locator('mjx-merror, [data-mjx-error]').count() == 0
                page.locator('summary', has_text='How the Lean proof follows these steps').click()
                panel = page.locator('#natural-language [data-lean-code-panel]')
                assert panel.locator('code.language-lean').is_visible()
                assert panel.locator('code span').count() > 0  # Existing Lean highlighter.
                panel.get_by_role('button', name='Copy Lean reference').click()
                page.wait_for_function('Array.from(document.querySelectorAll("[data-lean-copy-status]")).some(n=>n.textContent==="Copied")')
                copied = page.evaluate('() => navigator.clipboard.readText()')
                assert 'example' in copied and 'sorry' not in copied
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                page.screenshot(path=str(args.evidence / (identity + '-proof-desktop.png')), full_page=True)
                page.set_viewport_size({'width': 412, 'height': 915})
                page.reload()
                page.evaluate('() => MathJax.startup.promise')
                page.wait_for_timeout(400)
                page.locator('summary', has_text='Reference mathematical proof').click()
                page.locator('summary', has_text='How the Lean proof follows these steps').click()
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                page.evaluate('() => { document.activeElement?.blur(); window.scrollTo({top:0, behavior:"instant"}); }')
                page.wait_for_function('window.scrollY === 0')
                page.screenshot(path=str(args.evidence / (identity + '-proof-mobile.png')), full_page=True)
                page.set_viewport_size({'width': 1400, 'height': 1000})
            for tail in ('curriculum/index.html', 'levels/L5.html', 'domains/statistical-optimal-transport.html', 'sogb-g003.html', 'sogb-007.html', 'sogb-008.html', 'sogb-012.html'):
                page.goto(base + HUB + tail)
                page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                page.evaluate('() => MathJax.startup.promise')
                assert page.locator('mjx-merror, [data-mjx-error]').count() == 0
                if tail in ('sogb-007.html', 'sogb-008.html', 'sogb-012.html'):
                    assert page.locator('h2', has_text='Lean view: not yet aligned').count() == 1
                    page.locator('summary', has_text='Reference mathematical proof').click()
                    assert page.locator('mjx-container').count() > 0
                    assert page.locator('mjx-merror, [data-mjx-error]').count() == 0
                    page.locator('summary', has_text='Editorial review and exact formal-coverage boundary').click()
                    assert 'AI editorial review accepted' in page.locator('article.sog-reader').inner_text()
                if tail == 'sogb-g003.html':
                    assert page.locator('.sog-graph svg rect').count() == 3
                    page.locator('.sog-graph').screenshot(path=str(args.evidence / 'import-slice-desktop.png'))
                page.set_viewport_size({'width': 412, 'height': 915})
                page.wait_for_timeout(400)  # Let the existing sidebar resize transition finish.
                page.evaluate('() => { document.activeElement?.blur(); window.scrollTo({top:0, behavior:"instant"}); }')
                page.wait_for_function('window.scrollY === 0')
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                page.screenshot(path=str(args.evidence / (tail.replace('/', '-') + '-mobile.png')), full_page=True)
                page.set_viewport_size({'width': 1400, 'height': 1000})
            assert not errors, errors
            context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    report = {'mathematical_views': 19, 'graph_tasks': 3, 'math_rendered': True, 'lean_highlighting': True,
              'folds_and_copy': True, 'prompt_only_download': True, 'reviewed_subset_download': True,
              'editorial_vs_formal_scope_visible': True, 'mobile_overflow': False,
              'runtime_errors': errors}
    (args.evidence / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
