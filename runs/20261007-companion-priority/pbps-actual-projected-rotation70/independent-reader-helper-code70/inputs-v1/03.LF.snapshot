#!/usr/bin/env python3
"""Browser smoke checks. --offline-dom checks layout/graph only, not CDN math.

CI uses real HTTP navigation and the same external MathJax script as the site.
No browser dependency or new renderer is shipped to readers.
"""
from __future__ import annotations
import argparse
import functools
import http.server
import json
import re
import shutil
import threading
from pathlib import Path
from urllib.parse import parse_qs, urlsplit, quote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=str(ROOT/'_site'))
    parser.add_argument('--evidence',default=str(ROOT/'_browser-evidence'))
    parser.add_argument('--offline-dom',action='store_true')
    parser.add_argument('--browser-channel', choices=['chrome', 'msedge'],
                        help='Use an installed browser in an isolated profile; CI defaults to pinned Chromium')
    args=parser.parse_args()
    site=Path(args.output).resolve(); evidence=Path(args.evidence).resolve(); evidence.mkdir(parents=True,exist_ok=True)
    server=None; report={'mode':'offline DOM; CDN and alias not tested' if args.offline_dom else 'HTTP, MathJax and graph interaction','pages':[],'runtime_errors':[]}
    if not args.offline_dom:
        handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(site))
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as p:
            executable=shutil.which('chromium') if args.offline_dom else None
            browser=p.chromium.launch(executable_path=executable, channel=args.browser_channel,
                                      headless=True,args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1600,'height':1050})
            page.on('pageerror',lambda e:report['runtime_errors'].append(str(e)))
            def goto(rel: str) -> None:
                if not args.offline_dom:
                    page.goto(f'http://127.0.0.1:{server.server_port}/{rel}',wait_until='domcontentloaded')
                    return
                path=site/urlsplit(rel).path; text=path.read_text(encoding='utf-8')
                text=re.sub(r'<script\b.*?</script>','',text,flags=re.S)
                def inline_css(css: Path) -> str:
                    # Resolve local imports for a genuine offline layout check.
                    text=css.read_text(encoding='utf-8')
                    def dependency(m):
                        ref=m.group(1)
                        if ref.startswith(('http:', 'https:')): return ''
                        return inline_css((css.parent/ref).resolve())
                    return re.sub(r'@import\s+url\([\"\']([^\"\']+)[\"\']\);',dependency,text)
                def style(m):
                    css=(path.parent/m.group(1)).resolve()
                    return '<style>'+inline_css(css)+'</style>' if css.exists() else ''
                text=re.sub(r'<link\s+rel="stylesheet"\s+href="([^"]+)"[^>]*>',style,text)
                page.set_content(text,wait_until='domcontentloaded')
                if urlsplit(rel).path=='lean-foundations.html':
                    graph=json.loads((site/'data/underlying-lean-graph.json').read_text())
                    page.evaluate('g => { window.fetch = async () => ({ok:true,json:async()=>g}); }',graph)
                    page.add_script_tag(content=(site/'assets/underlying-lean-graph.js').read_text())
            for rel,name in [('index.html','home'),('libraries/statistical-optimal-transport/index.html','ot'),('libraries/discrete-sampling/index.html','discrete'),('libraries/mcmc/index.html','mcmc'),('progress/index.html#optimal-transport','progress'),('lean-foundations.html?view=functor','functor')]:
                goto(rel)
                page.wait_for_timeout(250)
                assert page.locator('.library-source-hubs > a').count()==7
                assert page.locator('.progress-route-nav > a').count()==7
                assert page.locator('h1').count()==1
                if name=='functor':
                    page.wait_for_selector('.ulg-node')
                    # The canvas also records data-view; select the actual toolbar button.
                    if not args.offline_dom:
                        page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                        page.evaluate('() => MathJax.startup.promise')
                    page.locator('button[data-view="functor"]').click()
                    page.locator('[data-functor-jump="transport:gibbs-prox"]').first.click()
                    assert 'ALL inputs:' in page.locator('[data-graph-detail]').inner_text()
                    assert 'not-Lean-certified' in page.locator('[data-graph-detail]').inner_text()
                    assert 'Conceptual families:' in page.locator('[data-graph-detail]').inner_text()
                    if not args.offline_dom:
                        # Family cards intentionally repeat bridge buttons. Check each
                        # unique typed transport exactly once and derive the expected
                        # count from the source model rather than a stale constant.
                        jump_ids=page.locator('[data-functor-jump]').evaluate_all(
                            '(nodes) => [...new Set(nodes.map(n => n.dataset.functorJump))]')
                        expected=len(json.loads((ROOT/'website/content/functor_hypergraph.json').read_text())['hyperedges'])
                        assert len(jump_ids)==expected,(len(jump_ids),expected)
                        for jump_id in jump_ids:
                            page.locator(f'[data-functor-jump="{jump_id}"]').first.click()
                            page.wait_for_selector('[data-graph-detail] .ulg-formula mjx-container')
                            assert page.locator('[data-graph-detail] mjx-merror').count()==0, jump_id
                            assert not page.locator('[data-graph-detail] .ulg-formula').evaluate(
                                '(node) => node.scrollWidth > node.clientWidth + 1'), jump_id
                        report['graph_mathjax_rendered']=True
                        report['graph_formulas_checked']=len(jump_ids)
                        page.locator('[data-functor-jump="transport:gibbs-prox"]').first.click()
                        page.wait_for_selector('[data-graph-detail] .ulg-formula mjx-container')
                    page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
                    # All conceptual incidence edges remain overlays, not formal.
                    assert page.locator('.ulg-edge[data-relation="joint conceptual input"][data-evidence="formal"]').count()==0
                page.screenshot(path=str(evidence/(name+'.png')))
                overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                assert not overflow, f'Horizontal overflow: {rel}'
                report['pages'].append({'page':rel,'libraries':7,'routes':7,'horizontal_overflow':overflow})
            goto('lean-foundations.html?view=perspectives&color=library')
            page.wait_for_selector('.ulg-node')
            page.locator('button[data-view="perspectives"]').click()
            assert page.locator('[data-graph-canvas]').get_attribute('data-color')=='library'
            assert page.locator('.ulg-node[data-id="method:hitrun"]').count()==1
            assert page.locator('.ulg-node[data-id="method:glauber"][data-scope="shared"]').count()==1
            assert page.locator('.ulg-edge[data-evidence="formal"]').count()==0
            # Select via the public toolbar + node interaction, then read exact caveats.
            page.locator('.ulg-node[data-id="method:ula"]').dispatch_event('click')
            assert 'biased' in page.locator('[data-graph-detail]').inner_text()
            assert 'not proof status' in page.locator('[data-graph-detail]').inner_text().lower()
            page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
            page.screenshot(path=str(evidence/'perspectives.png'))
            page.locator('button[data-view="lean"]').click()
            before=page.locator('.ulg-edge[data-evidence="formal"]').count()
            page.locator('[data-graph-color]').select_option('status')
            assert page.locator('.ulg-edge[data-evidence="formal"]').count()==before
            page.locator('[data-graph-color]').select_option('library')
            assert page.locator('.ulg-edge[data-evidence="formal"]').count()==before
            report['scope_colour_preserves_evidence']=True
            # One real, metadata-derived contribution slice: no giant graph or
            # hand-maintained declaration list in the browser acceptance test.
            publication_items = [i for f in (ROOT/'website/content/publications').glob('*.json')
                                 for i in json.loads(f.read_text(encoding='utf-8'))['items']]
            if publication_items:
                name = publication_items[0]['bindings'][0]['declaration']
                ident = 'decl:' + name
                goto('lean-foundations.html?view=lean&focus=' + quote(ident, safe='') + '&q=' + quote(name, safe=''))
                page.wait_for_selector('.ulg-canvas[data-local="true"]')
                assert page.locator(f'.ulg-node[data-id="{ident}"]').count() == 1
                assert page.locator('.ulg-edge[data-relation="source reference (scanner)"][data-evidence="formal"]').count() == 0
                assert page.locator('.ulg-edge[data-relation="closes leaf"][data-evidence="formal"]').count() == 0
                assert not page.locator('[data-graph-detail] h2').evaluate('(n) => n.scrollWidth > n.clientWidth + 1')
                assert page.locator('.ulg-node .label').evaluate_all(
                    '(labels) => labels.every(n => n.getBBox().x + n.getBBox().width <= Number(n.parentNode.querySelector("rect").getAttribute("width")))')
                page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
                page.screenshot(path=str(evidence/'contribution-graph.png'))
                page.set_viewport_size({'width':412,'height':915})
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                page.screenshot(path=str(evidence/'contribution-graph-mobile.png'))
                page.set_viewport_size({'width':1440,'height':1000})
                report['contribution_graph'] = {'node':ident,'local_view':True,'scanned_edges_not_formal':True}
            if not args.offline_dom:
                goto('underlying-lean-graph/index.html?view=functor&focus=transport:dirac')
                page.wait_for_url(lambda url: urlsplit(url).path.endswith('/lean-foundations.html')
                                  and parse_qs(urlsplit(url).query).get('view')==['functor']
                                  and parse_qs(urlsplit(url).query).get('focus')==['transport:dirac'])
                page.wait_for_selector('.ulg-node')
                page.wait_for_function('document.querySelector("[data-graph-detail]").textContent.includes("Deterministic maps")')
                report['query_preserving_alias']=True
            goto('libraries/statistical-optimal-transport/chapter-01.html')
            if not args.offline_dom:
                page.wait_for_selector('mjx-container',timeout=30000)
                assert page.locator('mjx-merror').count()==0, 'MathJax parse error'
                report['mathjax_rendered']=True
            page.set_viewport_size({'width':412,'height':915})
            page.screenshot(path=str(evidence/'ot-mobile.png'))
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), 'Mobile OT overflow'
            report['mobile_ot_overflow']=False
            report['discrete_chapters_checked']=0
            for i in range(1,13):
                goto(f'libraries/discrete-sampling/chapter-{i:02d}.html')
                assert page.locator('h1').count()==1
                assert page.locator('.library-source-hubs > a').count()==7
                assert page.locator('.progress-route-nav > a').count()==7
                if not args.offline_dom:
                    page.wait_for_selector('mjx-container',timeout=30000)
                    assert page.locator('mjx-merror').count()==0
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), f'Discrete chapter {i} mobile overflow'
                report['discrete_chapters_checked']+=1
            page.screenshot(path=str(evidence/'discrete-ising-mobile.png'))
            goto('libraries/discrete-sampling/index.html')
            assert page.locator('.library-chapter-card').count()==12
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), 'Discrete contents mobile overflow'
            page.screenshot(path=str(evidence/'discrete-mobile.png'))
            report['discrete_mobile_overflow']=False
            mcmc=json.loads((ROOT/'Libraries/MCMC/source-map.json').read_text())
            report['mcmc_pages_checked']=0
            for item in mcmc['chapters']+mcmc['extensions']:
                goto('libraries/mcmc/'+item['path'])
                assert page.locator('h1').count()==1
                assert page.locator('.library-source-hubs > a').count()==7
                assert page.locator('.progress-route-nav > a').count()==7
                if not args.offline_dom:
                    page.wait_for_selector('mjx-container',timeout=30000)
                    assert page.locator('mjx-merror').count()==0,item['path']
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),item['path']
                report['mcmc_pages_checked']+=1
            goto('libraries/mcmc/index.html')
            assert page.locator('.library-chapter-card').count()==16
            assert 'math/0404033v4' in page.content()
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
            page.screenshot(path=str(evidence/'mcmc-mobile.png'))
            publications = json.loads((site/'data/publication-progress.json').read_text())
            def chapter_label(path):
                return next((v['label'] for v in publications.values() if v['chapter_path'] == path), 'scaffold')
            opt_path = 'libraries/optimisation/chapter-01.html'
            expected_units = sum(len(i['bindings']) for f in (ROOT/'website/content/publications').glob('*.json')
                for i in json.loads(f.read_text(encoding='utf-8'))['items'] if i['chapter_path'] == opt_path)
            goto('libraries/optimisation/index.html')
            assert chapter_label(opt_path) in page.locator('.library-chapter-card').first.inner_text()
            assert chapter_label('libraries/optimisation/chapter-02.html') in page.locator('.library-chapter-card').nth(1).inner_text()
            goto(opt_path)
            assert page.locator('[data-publication-item]').count() >= 1
            assert page.locator('[data-authored-declaration]').count() == expected_units
            assert page.locator('details.inline-lean-statement:not([open])').count() == expected_units
            assert page.locator('details.inline-lean-proof:not([open])').count() == expected_units
            if not args.offline_dom:
                page.wait_for_selector('mjx-container', timeout=30000)
                assert page.locator('mjx-merror').count() == 0
            page.locator('details.inline-lean-proof > summary').last.click()
            assert page.locator('details.inline-lean-proof[open] code.language-lean').count() == 1
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
            page.screenshot(path=str(evidence/'optimisation-proof-mobile.png'))
            report['optimisation_publication'] = {'partial': True, 'source_complete': False,
                'adjacent_lean': True, 'mobile_overflow': False}
            # Every companion binding must have adjacent, initially folded Lean.
            # Derive the inventory from publications; do not freeze a leaf count.
            items = [i for f in (ROOT/'website/content/publications').glob('*.json')
                     for i in json.loads(f.read_text(encoding='utf-8'))['items']
                     if i['chapter_path'].startswith('example-cases/samplewiki/companions/')]
            report['companion_publications'] = []
            for rel in sorted({i['chapter_path'] for i in items}):
                goto(rel)
                expected = sum(len(i['bindings']) for i in items if i['chapter_path'] == rel)
                assert page.locator('[data-authored-declaration]').count() == expected, rel
                assert page.locator('details.inline-lean-statement:not([open])').count() == expected, rel
                assert page.locator('details.inline-lean-proof:not([open])').count() == expected, rel
                if not args.offline_dom:
                    page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                    page.evaluate('() => MathJax.startup.promise')
                    assert page.locator('mjx-container').count() > 0, rel
                    assert page.locator('mjx-merror').count() == 0, rel
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), rel
                for summary in page.locator('details.inline-lean-proof > summary').all():
                    summary.click()
                assert page.locator('details.inline-lean-proof[open] code.language-lean').count() == expected, rel
                page.locator('[data-authored-declaration]').last.scroll_into_view_if_needed()
                page.screenshot(path=str(evidence/(Path(rel).stem+'-proof-mobile.png')))
                report['companion_publications'].append({'path': rel, 'declarations': expected,
                    'adjacent_lean': True, 'mobile_overflow': False})
            assert not report['runtime_errors'],report['runtime_errors']
            browser.close()
    except Exception as error:
        report['failure']=repr(error)
        raise
    finally:
        if server: server.shutdown()
        (evidence/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
