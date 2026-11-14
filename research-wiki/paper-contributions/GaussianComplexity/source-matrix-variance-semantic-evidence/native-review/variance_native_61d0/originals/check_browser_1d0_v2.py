from runner import *
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import urllib.parse, time
SITE=OUT/'reader-site-1d0';B=OUT/'browser-1d0-v2';B.mkdir(exist_ok=True)
chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
build=json.loads((OUT/'reader-build-1d0.json').read_text())
browsermeta={'executable_path':str(chrome),'binary_sha256':sha(chrome.read_bytes()),'binary_bytes':chrome.stat().st_size,'version':run('chrome-version-1d0-v2',[chrome,'--version']).decode()}
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,format,*args): print('HTTP',format%args,flush=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(SITE)))
worker=Thread(target=server.serve_forever,name='bounded-http-server',daemon=False);worker.start()
base=f'http://127.0.0.1:{server.server_port}/'; report={'math_compiled_commit':COMMIT,'reader_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae','browser':browsermeta,'origin':base,'contexts':[],'source_checks':[],'page_errors':[],'failed_requests':[],'http_errors':[],'overflow_events':[],'lifecycle':'one foreground Python process; owned server thread and browser children; finally shutdown/join/close','remote_citations':'not fetched','global_nav':'excluded from bounded fixture; no links claimed reachable outside generated pages'}
def measure(page):
 return page.evaluate('''() => {
 const visible=e=>{let r=e.getBoundingClientRect();return r.width>0&&r.height>0};
 const overs=[...document.querySelectorAll('main *')].filter(e=>visible(e)&&e.getBoundingClientRect().right>innerWidth+2).filter(e=>{let a=e;while(a&&a!==document.body){let s=getComputedStyle(a);if(['auto','scroll','hidden','clip'].includes(s.overflowX))return false;a=a.parentElement}return true}).slice(0,20).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,120),right:e.getBoundingClientRect().right}));
 return {width:innerWidth,documentWidth:document.documentElement.scrollWidth,mathCount:document.querySelectorAll('mjx-container').length,mathErrors:document.querySelectorAll('mjx-merror,[data-mjx-error]').length,proofSteps:document.querySelectorAll('.proof-reader-step').length,inlineLean:document.querySelectorAll('[data-inline-lean]').length,openDetails:document.querySelectorAll('details[open]').length,allDetails:document.querySelectorAll('details').length,overflow:overs,styles:[...document.styleSheets].map(x=>x.href),bodyText:document.querySelector('main').innerText.slice(0,4000)};
 }''')
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path=str(chrome),headless=True,args=['--disable-background-networking','--no-first-run'])
  try:
   for width,height in [(1440,1000),(390,844)]:
    context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,accept_downloads=True)
    page=context.new_page()
    page.on('pageerror',lambda e: report['page_errors'].append(str(e)))
    page.on('requestfailed',lambda req: report['failed_requests'].append({'url':req.url,'error':req.failure}))
    page.on('response',lambda r: report['http_errors'].append({'url':r.url,'status':r.status}) if r.status>=400 else None)
    for idx,rel in enumerate(build['page_contexts']):
     page.goto(base+rel,wait_until='networkidle');page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise')
     page.evaluate('MathJax.startup.promise');page.evaluate('document.fonts.ready')
     initial=measure(page);assert initial['openDetails']==0,initial
     assert initial['mathErrors']==0 and initial['proofSteps']==7 and initial['mathCount']>=8,initial
     prefix=f'{width}-context{idx}'
     page.screenshot(path=str(B/f'{prefix}-initial.png'),full_page=True)
     # Read formula steps and assumption/source/boundary ledgers; preserve optional code folds.
     page.evaluate("document.querySelectorAll('details.reader-proof-disclosure,details.reader-ledger').forEach(e=>e.open=true)")
     page.evaluate('MathJax.typesetPromise()');page.evaluate('document.fonts.ready')
     expanded_math=measure(page);page.screenshot(path=str(B/f'{prefix}-math-expanded.png'),full_page=True)
     # Exact adjacent Lean must also work when all disclosures are expanded.
     page.evaluate("document.querySelectorAll('details').forEach(e=>e.open=true)")
     page.evaluate('MathJax.typesetPromise()');page.evaluate('document.fonts.ready')
     expanded=measure(page);assert expanded['mathErrors']==0
     if expanded['documentWidth']>width+1 or expanded['overflow']:
      diagnostic=page.locator('.table-scroll').evaluate_all("""es=>es.map(e=>{let a=e;const ancestors=[];while(a){const s=getComputedStyle(a),r=a.getBoundingClientRect();ancestors.push({tag:a.tagName,cls:a.className,overflowX:s.overflowX,overflowY:s.overflowY,width:r.width,right:r.right,clientWidth:a.clientWidth,scrollWidth:a.scrollWidth});a=a.parentElement};e.scrollLeft=100;return {ancestors,scrollLeftAfter100:e.scrollLeft}})""")
      report['overflow_events'].append({'viewport':width,'path':rel,'measurement':expanded,'computed_ancestors':diagnostic})
      page.locator('.table-scroll').scroll_into_view_if_needed();page.screenshot(path=str(B/f'{prefix}-table-overflow-diagnostic.png'))
     # Browser DOM extraction verifies every code fold against actual fixed bytes.
     codes=page.locator('.proof-reader-step > .reader-step-body > details pre code').all_text_contents()
     assert len(codes)==7,len(codes)
     source_records=[]
     for a,b,file in [(0,4,'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean'),(4,7,'Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')]:
      raw=''.join(codes[a:b]).encode();expect=(OUT/'candidate'/file).read_bytes();assert raw==expect,(file,sha(raw),sha(expect))
      source_records.append({'file':file,'code_sha256':sha(raw),'byte_exact':True})
     page.evaluate('scrollTo(0,0)');page.screenshot(path=str(B/f'{prefix}-all-expanded-top.png'))
     page.locator('.proof-reader-step').nth(4).scroll_into_view_if_needed();page.screenshot(path=str(B/f'{prefix}-private-T-expanded.png'))
     # Check actual reader source anchor by following its href to T L22.
     link=page.locator('a[href*="lesson-sources/Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean.html#L22"]')
     assert link.count()==1,link.count()
     href=link.get_attribute('href');page.goto(urllib.parse.urljoin(page.url,href),wait_until='networkidle')
     assert page.locator('#L22').count()==1
     spans=page.locator('pre > span[id^="L"]').all_text_contents()
     raw=('\n'.join(spans)+'\n').encode();expect=(OUT/'candidate/Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean').read_bytes();assert raw==expect
     page.locator('#L22').scroll_into_view_if_needed();page.screenshot(path=str(B/f'{prefix}-T-source-L22.png'))
     report['source_checks'].append({'viewport':width,'context':rel,'T_L22_reachable':True,'T_full_source_byte_exact':True,'source_sha256':sha(raw)})
     report['contexts'].append({'viewport':width,'path':rel,'initial':initial,'math_expanded':expanded_math,'all_expanded':expanded,'folds':source_records})
    # Production full-module source view and actual download (P and T).
    for mod,line in [('AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance',19),('Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance',22)]:
     file=mod.replace('.','/')+'.lean';slug=mod.lower().replace('.','-')
     page.goto(base+'modules/'+slug+'.html#complete-module-source',wait_until='networkidle')
     page.locator('#complete-module-source details').evaluate('(e)=>e.open=true')
     assert page.locator('#complete-module-source pre code').inner_text().encode()==(OUT/'candidate'/file).read_bytes()
     with page.expect_download() as di:page.locator('#complete-module-source a[download]').click()
     download=di.value;download.save_as(str(B/f'{width}-{Path(file).name}'));raw=(B/f'{width}-{Path(file).name}').read_bytes();assert raw==(OUT/'candidate'/file).read_bytes()
     report['source_checks'].append({'viewport':width,'module':mod,'production_full_module_byte_exact':True,'download_byte_exact':True,'sha256':sha(raw)})
    context.close()
  finally:browser.close()
finally:
 server.shutdown();server.server_close();worker.join(timeout=10)
 report['server_thread_joined']=not worker.is_alive()
 (OUT/'browser-report-1d0-v2.json').write_text(json.dumps(report,indent=2))
assert not report['page_errors'] and not report['failed_requests'] and not report['http_errors'] and not report['overflow_events'],{'errors':report['page_errors'],'http':report['http_errors'],'overflow_events':len(report['overflow_events'])}
print('BROWSER_PASS',len(report['contexts']),'contexts; full P/T sources and downloads byte exact',flush=True)
