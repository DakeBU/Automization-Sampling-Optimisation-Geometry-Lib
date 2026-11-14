#!/usr/bin/env python3
"""ROOT-primary only: one bounded original/candidate browser run.

This new wrapper is preparation, not permission. Only the root may execute it
after reviewing the frozen exact contract and obtaining its own narrow approval.
No previous browser approval or R12 script is used.
"""
import argparse
import datetime as dt
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import plistlib
import subprocess
import time
from pathlib import Path
import sys
import threading
import traceback
from urllib.parse import quote


OWN = Path(__file__).resolve().parent
PFILE = 'AutoSamplingTheory/TechnicalLemmas/Probability/MatrixBernsteinExponential.lean'
TFILE = 'Tests/GaussianComplexityBernsteinMgf.lean'
P = 'AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential.bernstein_exponential_quadratic_bound'
PMOD = P.rsplit('.', 1)[0]
TMOD = 'Tests.GaussianComplexityBernsteinMgf'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('variant', choices=['candidate'])
    args = parser.parse_args()
    contract_path = OWN / 'root-primary-browser-contract.v5.json'
    contract = json.loads(contract_path.read_text())
    if contract['status'] != 'FROZEN_PREPARED_ROOT_PRIMARY_ONLY_NO_EXECUTION_BY_CHILD':
        raise ValueError('Browser contract is not the frozen root-primary contract')
    if contract['wrapper_sha256'] != sha(__file__):
        raise ValueError('Browser wrapper differs from the frozen contract')
    for entry in contract['owned_inputs']:
        if sha(OWN / entry['path']) != entry['sha256']:
            raise ValueError('Frozen browser input changed: ' + entry['path'])
    chrome = Path(contract['installed_chrome']['executable_path'])
    if sha(chrome) != contract['installed_chrome']['binary_sha256']:
        raise ValueError('Installed Chrome binary changed from the frozen v3 contract')
    chrome_info_path = Path(contract['installed_chrome']['Info_plist_path'])
    chrome_info = plistlib.loads(chrome_info_path.read_bytes())
    chrome_evidence = {
        'executable_path': str(chrome), 'binary_sha256': sha(chrome),
        'Info_plist_path': str(chrome_info_path), 'Info_plist_sha256': sha(chrome_info_path),
        'app_short_version': chrome_info.get('CFBundleShortVersionString'),
        'app_build_version': chrome_info.get('CFBundleVersion'),
        'runtime_browser_version': None,
        'launch': {'headless': True, 'executable_path': str(chrome)},
    }
    manifest = json.loads((OWN / 'reader-render-manifest.C2.json').read_text())
    selected = manifest['variants'][args.variant]
    fixture = OWN / 'reader-fixtures-c2' / args.variant
    for entry in selected['files']:
        if sha(fixture / entry['path']) != entry['sha256']:
            raise ValueError('Frozen fixture changed: ' + entry['path'])
    output = OWN / 'root-primary-browser-output-v5' / args.variant
    output.mkdir(parents=True, exist_ok=False)
    checks, errors, blocked, screenshots = [], [], [], []

    def check(name, ok, detail=None):
        checks.append({'name': name, 'pass': bool(ok), 'detail': detail})

    def screenshot(page, name, *, full=False):
        path = output / (name + '.png')
        page.screenshot(path=str(path), full_page=full)
        screenshots.append({'path': str(path.relative_to(OWN)), 'sha256': sha(path)})

    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(fixture)))
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    origin = 'http://127.0.0.1:' + str(server.server_port)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    browser_started = False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, executable_path=str(chrome))
            browser_started = True
            chrome_evidence['runtime_browser_version'] = browser.version
            for label, width, height in [('desktop', 1440, 1000), ('mobile', 390, 844)]:
                context = browser.new_context(viewport={'width': width, 'height': height},
                                              device_scale_factor=1, accept_downloads=True)

                def route(request_route):
                    url = request_route.request.url
                    if url.startswith(origin + '/') or url.startswith(('data:', 'blob:')):
                        request_route.continue_()
                    else:
                        blocked.append(url)
                        request_route.abort()
                context.route('**/*', route)
                page = context.new_page()
                page.on('pageerror', lambda error: errors.append(str(error)))

                def goto(path):
                    page.goto(origin + '/' + path, wait_until='networkidle', timeout=30000)
                    page.wait_for_function('!!(window.MathJax && MathJax.startup && MathJax.startup.promise)', timeout=15000)
                    page.evaluate('async () => { await MathJax.startup.promise; await MathJax.typesetPromise(); }')

                def layout(name):
                    sizes = page.evaluate('''() => ({viewport: innerWidth,
                        html: document.documentElement.scrollWidth,
                        body: document.body.scrollWidth})''')
                    check(label + '-' + name + '-no-document-horizontal-overflow',
                          sizes['html'] <= sizes['viewport'] + 1 and sizes['body'] <= sizes['viewport'] + 1, sizes)

                try:
                    goto(selected['proof_path'])
                    steps = page.locator('details.proof-reader-step')
                    check(label + '-seven-proof-steps', steps.count() == 7)
                    check(label + '-all-seven-steps-initially-folded',
                          steps.evaluate_all('(xs) => xs.every(x => !x.open)'))
                    check(label + '-statement-and-proof-initially-folded',
                          page.locator('details.inline-lean').evaluate_all('(xs) => xs.length >= 2 && xs.every(x => !x.open)'))
                    check(label + '-mathjax-no-errors', page.locator('mjx-merror, [data-mjx-error]').count() == 0)
                    check(label + '-mathematics-visible', page.locator('mjx-container').count() > 0)
                    layout('proof-initial')
                    screenshot(page, label + '-proof-initial', full=True)
                    page.locator('details').evaluate_all('(xs) => xs.forEach(x => x.open = true)')
                    page.evaluate('async () => { await MathJax.typesetPromise(); }')
                    code = steps.locator('pre.code-block > code').all_text_contents()
                    check(label + '-seven-code-folds', len(code) == 7)
                    check(label + '-exact-P148-in-first-four-folds',
                          ''.join(code[:4]).encode() == (OWN / 'reader-9a8b163f' / PFILE).read_bytes())
                    check(label + '-exact-T240-in-last-three-folds',
                          ''.join(code[4:]).encode() == (OWN / 'reader-9a8b163f' / TFILE).read_bytes())
                    check(label + '-private-T-source-and-download-adjacent',
                          steps.nth(4).locator('[data-private-consumer-actions] a[data-private-source]').count() == 1
                          and steps.nth(4).locator('[data-private-consumer-actions] a[download]').count() == 1)
                    if steps.nth(4).locator('[data-private-source]').count():
                        check(label + '-private-T-exact-source57-href',
                              steps.nth(4).locator('[data-private-source]').get_attribute('href').endswith(TFILE + '.html#L57'))
                        with page.expect_download() as pending:
                            steps.nth(4).locator('[data-private-consumer-actions] a[download]').click()
                        download = output / (label + '-adjacent-private-T.lean')
                        pending.value.save_as(str(download))
                        check(label + '-adjacent-private-T-download-exact',
                              download.read_bytes() == (OWN / 'reader-9a8b163f' / TFILE).read_bytes())
                    for i in range(7):
                        steps.nth(i).scroll_into_view_if_needed()
                        screenshot(page, label + '-step-' + str(i + 1))
                    table = page.locator('[data-source-comparison] .table-scroll')
                    check(label + '-source-assumption-table-present', table.count() == 1)
                    if table.count():
                        table.scroll_into_view_if_needed()
                        geometry = table.evaluate('''el => {const s = getComputedStyle(el); const max = el.scrollWidth-el.clientWidth;
                            el.scrollLeft=max; return {overflow:s.overflowX, width:el.clientWidth,
                            scrollWidth:el.scrollWidth, max, actual:el.scrollLeft};}''')
                        check(label + '-source-table-horizontally-reachable',
                              geometry['max'] <= 1 or (geometry['overflow'] in ['auto', 'scroll'] and geometry['actual'] >= geometry['max'] - 1), geometry)
                        screenshot(page, label + '-source-table-right')
                    layout('proof-expanded')
                    check(label + '-expanded-mathjax-no-errors', page.locator('mjx-merror, [data-mjx-error]').count() == 0)
                    # Actual formula reach is independent of MathJax existence:
                    # overflowing main/step containers must really scroll right.
                    equations = page.locator('.proof-reader-equation')
                    overflowing = []
                    for equation_index in range(equations.count()):
                        equation = equations.nth(equation_index)
                        initial = equation.evaluate('''el => ({width:el.clientWidth,scrollWidth:el.scrollWidth,
                            max:el.scrollWidth-el.clientWidth,overflow:getComputedStyle(el).overflowX,
                            main:el.classList.contains('reader-main-equation')})''')
                        if initial['max'] <= 1:
                            continue
                        reached = equation.evaluate('''async el => {
                            document.documentElement.style.setProperty('scroll-behavior','auto','important');
                            document.body.style.setProperty('scroll-behavior','auto','important');
                            el.style.setProperty('scroll-behavior','auto','important');
                            el.scrollIntoView({behavior:'instant',block:'center',inline:'nearest'});
                            await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
                            const max=el.scrollWidth-el.clientWidth;
                            el.scrollLeft=0;
                            const left=el.scrollLeft;
                            el.scrollLeft=max;
                            await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
                            const r=el.getBoundingClientRect();
                            return {left,actual:el.scrollLeft,max,width:el.clientWidth,scrollWidth:el.scrollWidth,
                                overflow:getComputedStyle(el).overflowX,top:r.top,bottom:r.bottom,
                                viewportHeight:innerHeight,main:el.classList.contains('reader-main-equation')};
                        }''')
                        overflowing.append({'index':equation_index,**reached})
                        check(label + '-formula-' + str(equation_index) + '-positive-horizontal-right-reach',
                              reached['max']>1 and reached['actual']>0
                              and reached['overflow'] in ['auto','scroll']
                              and reached['actual']>=reached['max']-1, reached)
                        screenshot(page,label + '-formula-' + str(equation_index) + '-right-end')
                    check(label + '-overflowing-formula-containers-checked',
                          all(x['actual']>0 and x['actual']>=x['max']-1 for x in overflowing), overflowing)
                    if label=='mobile':
                        main_formula=page.locator('.reader-main-equation')
                        main_geometry=main_formula.evaluate('''el => ({max:el.scrollWidth-el.clientWidth,
                            actual:el.scrollLeft,overflow:getComputedStyle(el).overflowX})''')
                        check('mobile-main-formula-positive-horizontal-reach',
                              main_geometry['max']>1 and main_geometry['actual']>0
                              and main_geometry['actual']>=main_geometry['max']-1
                              and main_geometry['overflow'] in ['auto','scroll'], main_geometry)
                except Exception:
                    check(label + '-proof-stage-completed', False, traceback.format_exc())
                    screenshot(page, label + '-proof-stage-error')

                for source_label, raw, anchor, line_count in [('P', PFILE, 116, 148), ('T', TFILE, 57, 240)]:
                    try:
                        source_path = 'data/lesson-sources/' + raw + '.html'
                        goto(source_path + '#L' + str(anchor))
                        exact = (OWN / 'reader-9a8b163f' / raw).read_text()
                        check(label + '-' + source_label + '-complete-source-lines',
                              page.locator('pre > span[id^="L"]').count() == line_count)
                        check(label + '-' + source_label + '-complete-source-exact', page.locator('pre').text_content() == exact)
                        check(label + '-' + source_label + '-source-header-semantics',
                              page.locator('h1').first.text_content() == 'Exact source context'
                              and raw in page.title()
                              and page.locator('#L' + str(anchor)).text_content().strip().startswith(
                                  'theorem bernstein_exponential_quadratic_bound' if source_label == 'P'
                                  else 'private theorem actual_source_normalized_single_summand_mgf'))
                        check(label + '-' + source_label + '-visible-source-file-header',
                              page.locator('[data-exact-source-file]').count() == 1
                              and raw in page.locator('[data-exact-source-file]').text_content())
                        bounds = page.locator('#L' + str(anchor)).evaluate('''el => {
                            const r=el.getBoundingClientRect(), h=document.querySelector('.mobile-bar'), s=h?getComputedStyle(h):null;
                            const hr=h?h.getBoundingClientRect():{bottom:0};
                            return {top:r.top, bottom:r.bottom, header:(s && s.display!=='none' && ['fixed','sticky'].includes(s.position))?hr.bottom:0};}''')
                        check(label + '-' + source_label + '-anchor-below-mobile-header', bounds['top'] >= bounds['header'] - 1, bounds)
                        screenshot(page, label + '-source-' + source_label + '-anchor')
                        screenshot(page, label + '-source-' + source_label + '-full', full=True)
                        longest = max(enumerate(exact.splitlines(), 1), key=lambda x: len(x[1]))[0]
                        # Keep actual source-anchor behavior above as its own check.
                        # Longest-line glyph testing must settle actual geometry,
                        # rather than assuming a smooth scroll has completed.
                        settled = page.locator('#L' + str(longest)).evaluate('''async el => {
                            const frames = () => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
                            const headerBottom = () => {
                                let bottom = 0;
                                const candidates = [...document.querySelectorAll('header, .mobile-bar, .verification-strip')];
                                for (let pass=0; pass<candidates.length+1; pass++) {
                                    for (const h of candidates) {
                                        const s=getComputedStyle(h), r=h.getBoundingClientRect();
                                        if (['fixed','sticky'].includes(s.position) && s.display!=='none' && s.visibility!=='hidden'
                                            && r.width>0 && r.height>0 && r.right>0 && r.left<innerWidth
                                            && r.bottom>0 && r.top<=bottom+1) bottom=Math.max(bottom,r.bottom);
                                    }
                                }
                                return bottom;
                            };
                            const bounds = () => {
                                const r=el.getBoundingClientRect(), header=headerBottom();
                                return {top:r.top,bottom:r.bottom,height:r.height,header,viewportHeight:innerHeight,
                                    visible:r.height>0 && r.top>=header+4 && r.bottom<=innerHeight-4};
                            };
                            const before=bounds();
                            let adjusted=false;
                            for (let attempt=0; attempt<3 && !bounds().visible; attempt++) {
                                adjusted=true;
                                document.documentElement.style.setProperty('scroll-behavior','auto','important');
                                document.body.style.setProperty('scroll-behavior','auto','important');
                                for(let p=el.parentElement;p;p=p.parentElement) p.style.setProperty('scroll-behavior','auto','important');
                                el.scrollIntoView({behavior:'instant',block:'center',inline:'nearest'});
                                await frames();
                                const r=el.getBoundingClientRect(), header=headerBottom();
                                if(r.top<header+4) window.scrollBy({top:r.top-header-12,left:0,behavior:'instant'});
                                else if(r.bottom>innerHeight-4) window.scrollBy({top:r.bottom-innerHeight+12,left:0,behavior:'instant'});
                                await frames();
                            }
                            await frames();
                            return {before,after:bounds(),adjusted};
                        }''')
                        check(label + '-' + source_label + '-longest-line-actually-visible-below-header',
                              settled['after']['visible'], settled)
                        pre = page.locator('pre')
                        geometry = pre.evaluate('''el => {const max=el.scrollWidth-el.clientWidth;
                            return {width:el.clientWidth,scrollWidth:el.scrollWidth,max,overflow:getComputedStyle(el).overflowX};}''')
                        max_scroll = max(0, geometry['max'])
                        offsets = list(range(0, int(max_scroll) + 1, max(1, int(geometry['width']) - 24))) + [max_scroll]
                        for i, offset in enumerate(dict.fromkeys(offsets)):
                            pre.evaluate('(el, x) => {el.scrollLeft=x}', offset)
                            screenshot(page, label + '-source-' + source_label + '-glyph-segment-' + str(i))
                        final = page.locator('#L' + str(longest)).evaluate('''el => {
                            const p=el.closest('pre'), text=el.firstChild, range=document.createRange();
                            range.setStart(text, Math.max(0,text.length-1));range.setEnd(text,text.length);
                            const r=range.getBoundingClientRect(), b=p.getBoundingClientRect(), line=el.getBoundingClientRect();
                            let header=0;
                            const candidates=[...document.querySelectorAll('header, .mobile-bar, .verification-strip')];
                            for(let pass=0;pass<candidates.length+1;pass++) for(const h of candidates) {
                                const s=getComputedStyle(h), q=h.getBoundingClientRect();
                                if(['fixed','sticky'].includes(s.position) && s.display!=='none' && s.visibility!=='hidden'
                                    && q.width>0 && q.height>0 && q.right>0 && q.left<innerWidth
                                    && q.bottom>0 && q.top<=header+1) header=Math.max(header,q.bottom);
                            }
                            return {scroll:p.scrollLeft,max:p.scrollWidth-p.clientWidth,
                                lastGlyphLeft:r.left,lastGlyphRight:r.right,lastGlyphTop:r.top,lastGlyphBottom:r.bottom,
                                lastGlyphWidth:r.width,lastGlyphHeight:r.height,lineTop:line.top,lineBottom:line.bottom,
                                lineHeight:line.height,headerBottom:header,viewportHeight:innerHeight,
                                left:b.left,right:b.right,
                                glyphVerticallyVisible:r.width>0 && r.height>0 && r.top>=header+4 && r.bottom<=innerHeight-4,
                                lineVerticallyVisible:line.height>0 && line.top>=header+4 && line.bottom<=innerHeight-4};}''')
                        check(label + '-' + source_label + '-last-source-glyph-actually-visible-below-header',
                              final['glyphVerticallyVisible'] and final['lineVerticallyVisible'], final)
                        check(label + '-' + source_label + '-full-source-glyph-horizontal-reach',
                              final['glyphVerticallyVisible'] and final['lineVerticallyVisible']
                              and (max_scroll <= 1 or (geometry['overflow'] in ['auto', 'scroll']
                                  and final['scroll'] >= max_scroll - 1
                                  and final['lastGlyphRight'] <= final['right'] + 1
                                  and final['lastGlyphLeft'] >= final['left'] - 1)),
                              {'container': geometry, 'finalGlyph': final, 'segments': len(set(offsets))})
                        layout('source-' + source_label)
                        module = PMOD if source_label == 'P' else TMOD
                        slug = __import__('re').sub('[^a-zA-Z0-9]+', '-', module).strip('-').lower()
                        goto('modules/' + slug + '.html#complete-module-source')
                        panel = page.locator('#complete-module-source details')
                        panel.evaluate('(el) => el.open=true')
                        with page.expect_download() as pending:
                            panel.locator('a[download]').click()
                        download = output / (label + '-complete-' + source_label + '.lean')
                        pending.value.save_as(str(download))
                        check(label + '-' + source_label + '-module-download-exact', download.read_bytes() == exact.encode())
                    except Exception:
                        check(label + '-source-' + source_label + '-stage-completed', False, traceback.format_exc())
                        screenshot(page, label + '-source-' + source_label + '-stage-error')

                try:
                    goto('lean-foundations.html?view=lean&focus=' + quote('decl:' + P, safe=''))
                    page.wait_for_selector('.ulg-node.selected', timeout=10000)
                    check(label + '-graph-exact-public-focus', page.locator('.ulg-node.selected').get_attribute('data-id') == 'decl:' + P)
                    check(label + '-graph-reader-link', selected['lesson_path'] in page.locator('[data-graph-detail]').inner_html())
                    graph = context.request.get(origin + '/data/underlying-lean-graph.json').json()
                    edges = {(e['source'], e['target'], e['relation']) for e in graph['edges']}
                    check(label + '-graph-exact-module-declares-edge', ('module:' + PMOD, 'decl:' + P, 'declares') in edges)
                    check(label + '-graph-exact-actual-module-import-edge', ('module:' + PMOD, 'module:' + TMOD, 'imports') in edges)
                    check(label + '-graph-source-overlay-separate', any(e[0] == 'decl:' + P and e[2] == 'source correspondence; not a Lean dependency' for e in edges))
                    check(label + '-graph-no-private-canonical-node', not any('actual_source_normalized_single_summand_mgf' in n['id'] for n in graph['nodes']))
                    check(label + '-graph-formal-and-source-styles-separate',
                          page.locator('path.ulg-edge.formal-edge.related').count() >= 1
                          and page.locator('path.ulg-edge.overlay-edge.related').count() >= 1)
                    def reveal_graph_element(locator, block):
                        return locator.evaluate('''async (el, block) => {
                            document.documentElement.style.setProperty('scroll-behavior','auto','important');
                            document.body.style.setProperty('scroll-behavior','auto','important');
                            for(let p=el;p;p=p.parentElement) p.style.setProperty('scroll-behavior','auto','important');
                            const frames=()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
                            const headerBottom=()=>{
                                let bottom=0;
                                const hs=[...document.querySelectorAll('header,.mobile-bar,.verification-strip')];
                                for(let pass=0;pass<hs.length+1;pass++) for(const h of hs){
                                    const s=getComputedStyle(h),r=h.getBoundingClientRect();
                                    if(['fixed','sticky'].includes(s.position) && s.display!=='none' && s.visibility!=='hidden'
                                        && r.width>0 && r.height>0 && r.right>0 && r.left<innerWidth
                                        && r.bottom>0 && r.top<=bottom+1) bottom=Math.max(bottom,r.bottom);
                                }
                                return bottom;
                            };
                            el.scrollIntoView({behavior:'instant',block,inline:'nearest'});
                            await frames();
                            let r=el.getBoundingClientRect(),header=headerBottom();
                            if(r.top<header+4) window.scrollBy({top:r.top-header-12,left:0,behavior:'instant'});
                            await frames();
                            r=el.getBoundingClientRect();header=headerBottom();
                            const ix=Math.min(r.right,innerWidth)-Math.max(r.left,0);
                            const iy=Math.min(r.bottom,innerHeight-4)-Math.max(r.top,header+4);
                            return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height,
                                viewportWidth:innerWidth,viewportHeight:innerHeight,headerBottom:header,
                                intersectionWidth:ix,intersectionHeight:iy,
                                intersectsVisibleViewport:r.width>0 && r.height>0 && ix>0 && iy>0};
                        }''', block)
                    selected_geometry=reveal_graph_element(page.locator('.ulg-node.selected'),'center')
                    check(label + '-graph-selected-node-actually-in-viewport-below-header',
                          selected_geometry['intersectsVisibleViewport'],selected_geometry)
                    screenshot(page, label + '-graph-exact-one-hop')
                    detail=page.locator('[data-graph-detail]')
                    detail_geometry=reveal_graph_element(detail,'start')
                    check(label + '-graph-detail-actually-in-viewport-below-header',
                          detail_geometry['intersectsVisibleViewport'],detail_geometry)
                    screenshot(page,label + '-graph-detail-header')
                    reader_link=detail.locator('.ulg-links a').first
                    reader_geometry=reveal_graph_element(reader_link,'center')
                    check(label + '-graph-reader-edge-detail-actually-visible',
                          reader_geometry['intersectsVisibleViewport']
                          and detail.locator('.ulg-neighbors [data-jump]').count()>=1,reader_geometry)
                    screenshot(page,label + '-graph-detail-reader-and-edges')
                    layout('graph')
                except Exception:
                    check(label + '-graph-stage-completed', False, traceback.format_exc())
                    screenshot(page, label + '-graph-stage-error')
                context.close()
            browser.close()
    except Exception:
        check('browser-run-completed', False, traceback.format_exc())
    finally:
        server.shutdown()
        server.server_close()
        worker.join()
    for entry in selected['files']:
        check('fixture-unchanged:' + entry['path'], sha(fixture / entry['path']) == entry['sha256'])
    check('no-page-javascript-errors', not errors, errors)
    check('no-external-browser-requests', not blocked, blocked)
    result = {'schema': 'root-primary-bounded-browser-result-v5', 'variant': args.variant,
              'reader_commit': contract['reader_commit'], 'mathematical_candidate': contract['mathematical_candidate'],
              'candidate_variant': 'C2_offline_font_import_only',
              'contract_sha256': sha(contract_path), 'wrapper_sha256': sha(__file__),
              'argv': sys.argv, 'cwd': str(Path.cwd()), 'localhost_origin': origin,
              'started_utc': started, 'ended_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'checks': checks, 'screenshots': screenshots, 'javascript_errors': errors,
              'actual_chrome': chrome_evidence, 'browser_started': browser_started,
              'blocked_external_requests': blocked,
              'status': ('ENV_BLOCKED' if not browser_started else
                         'PASS' if all(x['pass'] for x in checks) else 'FAIL'),
              'human_visual_review': 'PENDING_ROOT_REVIEW_OF_ACTUAL_PNGS',
              'production_changes_applied': False}
    target = output / 'actual-checks.json'
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'variant': args.variant, 'status': result['status'],
                      'failures': [x['name'] for x in checks if not x['pass']],
                      'actual_checks': str(target), 'sha256': sha(target)}))
    return 0 if result['status'] == 'PASS' else 2 if result['status'] == 'ENV_BLOCKED' else 1


def captured_root_process():
    # OS file-descriptor redirection captures real Python/native/inherited
    # stdout and stderr while ROOT runs this process. No flags or reconstructed
    # summaries substitute for the raw byte streams.
    variant = sys.argv[1] if len(sys.argv) == 2 and sys.argv[1] in ['candidate'] else 'invalid-argv'
    process_dir = OWN / 'root-primary-browser-process-v5' / variant
    process_dir.mkdir(parents=True, exist_ok=False)
    stdout_path, stderr_path = process_dir / 'stdout.raw', process_dir / 'stderr.raw'
    sys.stdout.flush()
    sys.stderr.flush()
    stdout_file, stderr_file = stdout_path.open('xb', buffering=0), stderr_path.open('xb', buffering=0)
    os.dup2(stdout_file.fileno(), 1)
    os.dup2(stderr_file.fileno(), 2)
    stdout_file.close()
    stderr_file.close()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    monotonic_start = time.monotonic()
    contract_path = OWN / 'root-primary-browser-contract.v5.json'
    executable_path = Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    chrome_info_path = Path('/Applications/Google Chrome.app/Contents/Info.plist')

    def root_head():
        result = subprocess.run(['/usr/bin/git', 'rev-parse', 'HEAD'],
            cwd=OWN.parents[2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return {'exit_code': result.returncode,
                'stdout': result.stdout.decode('utf-8', errors='replace').strip(),
                'stderr': result.stderr.decode('utf-8', errors='replace')}

    before_head = root_head()
    exit_code, exception = 1, None
    try:
        exit_code = int(main())
    except BaseException as error:
        exception = {'type': type(error).__name__, 'message': str(error)}
        traceback.print_exc()
        if isinstance(error, SystemExit) and isinstance(error.code, int):
            exit_code = error.code
        elif isinstance(error, KeyboardInterrupt):
            exit_code = 130
        else:
            exit_code = 1
    after_head = root_head()
    chrome_record = {'executable_path': str(executable_path)}
    try:
        chrome_record['binary_sha256'] = sha(executable_path)
        info = plistlib.loads(chrome_info_path.read_bytes())
        chrome_record.update({'Info_plist_path': str(chrome_info_path),
                             'Info_plist_sha256': sha(chrome_info_path),
                             'app_short_version': info.get('CFBundleShortVersionString'),
                             'app_build_version': info.get('CFBundleVersion')})
    except Exception as error:
        chrome_record['metadata_error'] = str(error)
        traceback.print_exc()
    actual_checks_path = OWN / 'root-primary-browser-output-v5' / variant / 'actual-checks.json'
    actual_checks = None
    if actual_checks_path.exists():
        try:
            result = json.loads(actual_checks_path.read_text())
            chrome_record['runtime_browser_version'] = result.get('actual_chrome', {}).get('runtime_browser_version')
            actual_checks = {'path': str(actual_checks_path.relative_to(OWN)),
                             'sha256': sha(actual_checks_path), 'bytes': actual_checks_path.stat().st_size,
                             'status': result['status'], 'screenshot_count': len(result['screenshots'])}
        except Exception:
            traceback.print_exc()
    sys.stdout.flush()
    sys.stderr.flush()
    receipt = {
        'schema': 'root-primary-actual-process-receipt-v1',
        'command': [sys.executable, *sys.argv], 'argv': [sys.executable, *sys.argv],
        'cwd': str(Path.cwd()), 'pid': os.getpid(), 'ppid': os.getppid(),
        'started': started, 'ended': dt.datetime.now(dt.timezone.utc).isoformat(),
        'elapsed_seconds': time.monotonic() - monotonic_start,
        'exit_code': exit_code,
        'stdout': {'path': str(stdout_path.relative_to(OWN)), 'sha256': sha(stdout_path), 'bytes': stdout_path.stat().st_size},
        'stderr': {'path': str(stderr_path.relative_to(OWN)), 'sha256': sha(stderr_path), 'bytes': stderr_path.stat().st_size},
        'wrapper_sha256': sha(__file__), 'contract_sha256': sha(contract_path),
        'actual_chrome': chrome_record, 'actual_checks': actual_checks,
        'root_HEAD_before': before_head, 'root_HEAD_after': after_head,
        'exception': exception, 'variant': variant,
        'stream_capture': 'Actual OS fd1/fd2 redirected for ROOT execution; streams are not reconstructed from check flags.',
        'python_executable': sys.executable, 'python_version': sys.version,
    }
    (process_dir / 'process-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    # Keep fd capture active to process termination. All foreground browser and
    # local-server cleanup, including worker.join(), has completed inside main.
    return exit_code


if __name__ == '__main__':
    sys.exit(captured_root_process())
