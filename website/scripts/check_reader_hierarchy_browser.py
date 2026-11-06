"""Real visual/interaction gate for the shared hierarchy and three Bench doors."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
HUB='benchmarks/samplingoptimisationgeometrybench/'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT/'_site')
    parser.add_argument('--evidence',type=Path,default=ROOT/'_browser-evidence/reader-hierarchy')
    parser.add_argument('--browser-channel',choices=('msedge','chrome'))
    args=parser.parse_args()
    args.evidence.mkdir(parents=True,exist_ok=True)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(args.root.resolve())))
    thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
    errors=[]; report={'routes':[],'runtime_errors':errors}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(channel=args.browser_channel,headless=True)
            context=browser.new_context(permissions=['clipboard-read','clipboard-write'])
            base=f'http://127.0.0.1:{server.server_port}/'
            context.route('**/*',lambda route:route.continue_() if route.request.url.startswith((base,'data:')) else route.abort())
            page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            routes=[('index.html','home'),(HUB+'index.html','bench'),
                    *((HUB+c+'/index.html',c) for c in ('sampling','optimisation','geometry')),
                    (HUB+'evaluation/index.html','evaluate'),(HUB+'training/index.html','training'),('lean-foundations.html?view=lean','lean-graph'),
                    ('lean-foundations.html?view=functor','functor')]
            for rel,label in routes:
                page.set_viewport_size({'width':1440,'height':1000})
                assert page.goto(base+rel).status==200
                assert page.locator('.sidebar-graphs a').count()==2
                assert page.locator('.sidebar-benches [data-bench-collection]').count()==3
                assert page.locator('.library-source-hubs > a').count()==7
                assert page.locator('.reader-secondary-nav[open]').count()==0
                for link in page.locator('.sidebar-graphs a,.sidebar-benches [data-bench-collection]').all():
                    rect=link.bounding_box()
                    assert rect and rect['y']>=0 and rect['y']+rect['height']<1000, 'Primary navigation is below the first sidebar viewport'
                if label in ('home','bench'):
                    assert page.locator('.sog-portal-card').count()==(4 if label=='home' else 3)
                    assert page.locator('.sog-portal-card svg').count()==(4 if label=='home' else 3)
                    assert page.locator('main table:visible').count()==0
                if label in ('sampling','optimisation','geometry'):
                    page.wait_for_function('document.querySelector("[data-sog-list-status]").textContent.startsWith("Showing")')
                    rows=page.locator('.sog-task-row').count()
                    assert page.locator('.sog-task-row:visible').count()==min(6,rows)
                    if rows>6:
                        page.get_by_role('button',name='Show more tasks').click()
                        assert page.locator('.sog-task-row:visible').count()==min(12,rows)
                    identity=page.locator('.sog-task-row').first.get_attribute('href').split('/')[-1].split('.')[0]
                    page.get_by_role('searchbox',name='Find a task').fill(identity)
                    assert page.locator('.sog-task-row:visible').count()==1
                    page.get_by_role('searchbox',name='Find a task').fill('')
                if label=='evaluate':
                    assert page.get_by_text('Experimental Linux CLI · hosted executor pending',exact=True).is_visible()
                    compiler_guide=page.locator('details').filter(has=page.get_by_text('Use the experimental Lean compiler workspace',exact=True))
                    assert compiler_guide.count()==1 and compiler_guide.get_attribute('open') is None
                    compiler_guide.locator('summary').click()
                    assert compiler_guide.get_by_text('This is not a hosted service or a model result.',exact=False).is_visible()
                    assert compiler_guide.locator('a[href$="/lean-runtime/WORKSPACE.md"]').is_visible()
                    assert compiler_guide.locator('a[href$="/native08-independent-review.json"]').is_visible()
                    compiler_guide.locator('summary').click()
                if label=='training':
                    assert page.locator('.sog-portal-card[download]').count()==2
                    assert page.locator('.sog-fold[open]').count()==0
                if label in ('lean-graph','functor'):
                    page.wait_for_selector('.ulg-node')
                    assert page.locator('.ulg-help[open]').count()==0
                    assert page.locator('.ulg-shell').bounding_box()['y']<650
                page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                page.screenshot(path=str(args.evidence/(label+'-desktop.png')))
                page.set_viewport_size({'width':412,'height':915})
                page.wait_for_function('document.querySelector("#site-sidebar").getBoundingClientRect().right<=1')
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),rel
                page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                page.screenshot(path=str(args.evidence/(label+'-mobile.png')))
                report['routes'].append(rel)
            page.goto(base+HUB+'sogb-001.html')
            button=page.locator('#natural-language [data-sog-copy-prompt]')
            expected=page.request.get(base+HUB+button.get_attribute('data-sog-copy-prompt')).text()
            button.click()
            page.wait_for_function('document.querySelector("#natural-language [data-sog-copy-status]").textContent==="Copied prompt-only task"')
            copied=page.evaluate('() => navigator.clipboard.readText()')
            if copied!=expected:
                print(json.dumps({'clipboard_difference':{'expected_length':len(expected),'copied_length':len(copied),
                    'expected_crlf':expected.count('\r\n'),'copied_crlf':copied.count('\r\n'),
                    'newline_normalized_equal':copied.replace('\r\n','\n')==expected.replace('\r\n','\n')}}))
            assert copied.replace('\r\n','\n')==expected.replace('\r\n','\n')
            assert json.loads(copied)==json.loads(expected)
            assert 'steps' not in json.loads(expected) and 'lean_reference' not in json.loads(expected)
            assert not errors,errors
            report.update({'peer_shelves':True,'graph_doors_visible':True,'visual_doors':True,'progressive_task_lists':True,
                           'prompt_only_copy':True,'agentic_lean_gap_explicit':True,'mobile_overflow':False})
            (args.evidence/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(report))
            browser.close()
    finally:
        server.shutdown();server.server_close();thread.join()


if __name__=='__main__':
    main()
