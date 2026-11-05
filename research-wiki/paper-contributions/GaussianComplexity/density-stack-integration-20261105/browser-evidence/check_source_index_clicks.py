"""Exercise the nested source index through visible mouse/touch targets."""
import datetime
import functools
import hashlib
import http.server
import json
from pathlib import Path
import re
import subprocess
import threading
from playwright.sync_api import sync_playwright

root = Path.cwd()
out = root / '.astis/huanjian-gc-integration-20261105/browser' / ('index-clicks-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
out.mkdir(parents=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(root / '_site')))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}/'
report = {'head': subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),
          'mode': 'HTTP isolated headless Chrome; visible nested disclosure and link clicks',
          'checks': [], 'screenshots': [], 'errors': []}
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        report['browser_version'] = browser.version
        context = browser.new_context()
        context.route(re.compile(r'https?://(?!127\.0\.0\.1)'), lambda route: route.abort())
        page = context.new_page()
        page.on('pageerror', lambda e: report['errors'].append(str(e)))
        for width in (1440,390):
            page.set_viewport_size({'width':width,'height':1000 if width>400 else 844})
            for slug in ('evaluated-eq24','single-block-separation','mixture-densities'):
                page.goto(base+'example-cases/samplewiki/companions/gaussian-sampling-complexity.html',wait_until='domcontentloaded')
                assert 'Lean gate passed' in page.locator('.verification-strip').text_content()
                index = page.locator('#paper-lean-progress .paper-verified-index')
                assert index.get_attribute('open') is None
                index.locator(':scope > summary').click()
                unit = index.locator(f'details.paper-verified-unit[data-publication-item="huanjian-{slug}"]')
                unit.locator(':scope > summary').click()
                link = unit.locator(f'a[href$="source-huanjian-{slug}.html"]')
                assert link.is_visible()
                unit.scroll_into_view_if_needed()
                image = out/f'{slug}-{width}-index-open.png'
                page.screenshot(path=str(image))
                report['screenshots'].append({'file':image.name,'sha256':hashlib.sha256(image.read_bytes()).hexdigest()})
                link.click()
                page.wait_for_url('**/proofs/source-huanjian-'+slug+'.html')
                page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                page.evaluate('() => MathJax.startup.promise')
                assert page.locator('mjx-container').count()>0
                assert page.locator('mjx-merror, [data-mjx-error]').count()==0
                assert page.locator('article[data-authored-declaration]').count()==1
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                report['checks'].append({'slug':slug,'width':width,'outer_disclosure_clicked':True,'unit_disclosure_clicked':True,'visible_source_link_clicked':True,'actual_reader_rendered':True})
        assert not report['errors'],report['errors']
        browser.close()
        report['status']='passed'
except Exception as e:
    report['status']='failed';report['failure']=repr(e)
    raise
finally:
    server.shutdown();server.server_close()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report.get('status'),'checks':len(report['checks']),'report':str(out/'report.json')}))
