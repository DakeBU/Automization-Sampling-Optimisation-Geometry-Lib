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


def math_component_shot(page, destination: Path) -> None:
    """Omit outside navigation chrome from the component image, not the UI tests."""
    page.evaluate("""() => {
      document.activeElement?.blur();
      for (const e of document.querySelectorAll('*'))
        if (!e.closest('#natural-language') && ['fixed','sticky'].includes(getComputedStyle(e).position))
          e.setAttribute('data-sog-shot-chrome', '');
    }""")
    try:
        page.locator('#natural-language').screenshot(path=str(destination),
            style='[data-sog-shot-chrome] { visibility: hidden !important; }')
    finally:
        page.evaluate("() => document.querySelectorAll('[data-sog-shot-chrome]').forEach(e=>e.removeAttribute('data-sog-shot-chrome'))")


def check_visible_equations(page) -> None:
    for equation in page.locator('#natural-language mjx-container[display="true"]').all():
        assert equation.evaluate("""e => {
          e.scrollIntoView({block:'center', inline:'nearest', behavior:'instant'});
          const r=e.getBoundingClientRect();
          const hit=document.elementFromPoint((r.left+r.right)/2,(r.top+r.bottom)/2);
          return r.width>0 && r.height>0 && (hit===e || e.contains(hit));
        }"""), 'Rendered equation is obscured in the actual viewport'


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
            manifest = page.request.get(base + HUB + 'downloads/manifest.json').json()
            editorial = page.request.get(base + HUB + 'downloads/editorial-review.json').json()
            with page.expect_download() as download:
                page.get_by_role('link', name='Prompt-only JSONL', exact=True).click()
            path = download.value.path()
            records = [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines()]
            assert len(records) == manifest['qa_views'] and all('lean_reference' not in r and 'steps' not in r for r in records)
            with page.expect_download() as reviewed_download:
                page.get_by_role('link', name='editorially reviewed prompts', exact=True).click()
            reviewed = [json.loads(line) for line in Path(reviewed_download.value.path()).read_text(encoding='utf-8').splitlines()]
            accepted_ids = {identity for identity, row in editorial['items'].items()
                            if row['editorial'] in ('accepted', 'accepted-after-repair')}
            expected_reviewed = [r for r in records if r['id'] in accepted_ids]
            key = lambda r: (r['id'], r['track'], r['binding_sha256'])
            assert sorted(map(key, reviewed)) == sorted(map(key, expected_reviewed))
            page.screenshot(path=str(args.evidence / 'overview-desktop.png'), full_page=True)
            for identity in sorted({r['id'] for r in records if r['track'] == 'lean'}):
                page.goto(base + HUB + identity + '.html')
                page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                page.evaluate('() => MathJax.startup.promise')
                assert page.locator('details[open]').count() == 0
                page.locator('summary', has_text='Reference mathematical proof').click()
                page.wait_for_timeout(300)
                assert page.locator('mjx-container').count() > 0
                assert page.locator('mjx-merror, [data-mjx-error]').count() == 0
                check_visible_equations(page)
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
                page.locator('summary', has_text='How the Lean proof follows these steps').click()
                math_component_shot(page, args.evidence / (identity + '-math-desktop.png'))
                page.set_viewport_size({'width': 412, 'height': 915})
                page.reload()
                page.evaluate('() => MathJax.startup.promise')
                page.wait_for_timeout(400)
                page.locator('summary', has_text='Reference mathematical proof').click()
                page.locator('summary', has_text='How the Lean proof follows these steps').click()
                check_visible_equations(page)
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                page.evaluate('() => { document.activeElement?.blur(); window.scrollTo({top:0, behavior:"instant"}); }')
                page.wait_for_function('window.scrollY === 0')
                page.screenshot(path=str(args.evidence / (identity + '-proof-mobile.png')), full_page=True)
                page.locator('summary', has_text='How the Lean proof follows these steps').click()
                math_component_shot(page, args.evidence / (identity + '-math-mobile.png'))
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
    report = {'mathematical_views': len(records), 'graph_tasks': manifest['graph_tasks'], 'math_rendered': True, 'lean_highlighting': True,
              'folds_and_copy': True, 'prompt_only_download': True, 'reviewed_subset_download': True,
              'editorial_vs_formal_scope_visible': True, 'mobile_overflow': False,
              'equations_unobscured_when_centered': True, 'component_images_omit_navigation_only': True,
              'runtime_errors': errors}
    (args.evidence / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
