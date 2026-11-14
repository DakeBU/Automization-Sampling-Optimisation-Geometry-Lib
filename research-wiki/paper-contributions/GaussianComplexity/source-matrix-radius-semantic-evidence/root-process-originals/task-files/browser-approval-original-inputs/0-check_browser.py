from runner import *
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import urllib.parse
variant=sys.argv[1];assert variant in ['original','conditional']
B=OUT/('reader/browser-'+variant);B.mkdir(parents=True,exist_ok=True)
build=json.loads((OUT/'reader/build-result.json').read_text());C=Path(build['source_snapshot'])
SITE=Path(build['site']) if variant=='original' else OUT/'reader-conditional/site'
chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,fmt,*args): print('HTTP',fmt%args,flush=True)
report={'candidate':build['candidate'],'variant':variant,'production_css_sha256':sha(SITE/'assets/proof-readers.css'),
 'browser_executable':str(chrome),'browser_binary_sha256':sha(chrome),'contexts':[],'source_checks':[],
 'page_errors':[],'failed_requests':[],'http_errors':[],'layout_failures':[],
 'scope':'Bounded production reader fixture; aggregate badges visibly unverified. No complete-site navigation or remote citation acceptance.',
 'lifecycle':'Foreground process, owned HTTP thread and Chrome children, explicit close/shutdown/join.'}
def measure(page):
    return page.evaluate('''() => ({width:innerWidth,documentWidth:document.documentElement.scrollWidth,
      mathCount:document.querySelectorAll('mjx-container').length,mathErrors:document.querySelectorAll('mjx-merror,[data-mjx-error]').length,
      proofSteps:document.querySelectorAll('.proof-reader-step').length,openDetails:document.querySelectorAll('details[open]').length,
      details:document.querySelectorAll('details').length,styles:[...document.styleSheets].map(x=>x.href)})''')
server=None;worker=None
try:
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(SITE)))
    worker=Thread(target=server.serve_forever,name='radius-native-owned-reader',daemon=False);worker.start()
    origin=f'http://127.0.0.1:{server.server_port}/';report['origin']=origin
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=str(chrome),headless=True,args=['--disable-background-networking','--no-first-run'])
        report['browser_version']=browser.version
        try:
            for width,height in [(1440,1000),(390,844)]:
                context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,accept_downloads=True)
                page=context.new_page()
                page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
                page.on('requestfailed',lambda r:report['failed_requests'].append({'url':r.url,'error':r.failure}))
                page.on('response',lambda r:report['http_errors'].append({'url':r.url,'status':r.status}) if r.status>=400 else None)
                for ix,rel in enumerate(build['page_contexts']):
                    page.goto(origin+rel,wait_until='networkidle')
                    page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise')
                    page.evaluate('MathJax.startup.promise');page.evaluate('document.fonts.ready')
                    initial=measure(page);assert initial['openDetails']==0 and initial['proofSteps']==6 and initial['mathErrors']==0 and initial['mathCount']>=8,initial
                    pre=f'{width}-context{ix}'
                    page.screenshot(path=str(B/(pre+'-initial.png')),full_page=True)
                    page.evaluate("document.querySelectorAll('details.reader-proof-disclosure,details.reader-ledger').forEach(e=>e.open=true)")
                    page.evaluate('MathJax.typesetPromise()');page.evaluate('document.fonts.ready')
                    math=measure(page);page.screenshot(path=str(B/(pre+'-math-expanded.png')),full_page=True)
                    page.evaluate("document.querySelectorAll('details').forEach(e=>e.open=true)")
                    page.evaluate('MathJax.typesetPromise()');page.evaluate('document.fonts.ready')
                    expanded=measure(page);assert expanded['mathErrors']==0
                    tablemetrics=page.locator('.table-scroll').evaluate_all('''es=>es.map(e=>{
                      let r=e.getBoundingClientRect(),s=getComputedStyle(e);e.scrollLeft=100;
                      let a=e,ancestors=[];while(a){let q=a.getBoundingClientRect(),v=getComputedStyle(a);ancestors.push({tag:a.tagName,cls:a.className,width:q.width,right:q.right,overflowX:v.overflowX});a=a.parentElement;}
                      let x={width:r.width,right:r.right,clientWidth:e.clientWidth,scrollWidth:e.scrollWidth,overflowX:s.overflowX,scrollLeftAfter100:e.scrollLeft,ancestors};e.scrollLeft=0;return x;})''')
                    if expanded['documentWidth']>width+1:report['layout_failures'].append({'path':rel,'viewport':width,'reason':'document-horizontal-overflow','measurement':expanded})
                    if width==390:
                        for m in tablemetrics:
                            if m['right']>width+2 or (m['scrollWidth']>m['clientWidth'] and m['scrollLeftAfter100']==0):
                                report['layout_failures'].append({'path':rel,'viewport':width,'reason':'publication-table-clipped-or-unscrollable','measurement':m})
                    if tablemetrics:
                        page.locator('.table-scroll').first.scroll_into_view_if_needed();page.screenshot(path=str(B/(pre+'-table-left.png')))
                        page.locator('.table-scroll').first.evaluate('(e)=>e.scrollLeft=e.scrollWidth');page.screenshot(path=str(B/(pre+'-table-right.png')))
                    codes=page.locator('.proof-reader-step > .reader-step-body > details pre code').all_text_contents();assert len(codes)==6
                    foldchecks=[]
                    for lo,hi,file in [(0,4,'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixRadius.lean'),(4,6,'Tests/GaussianComplexityFixedSpectrumSourceMatrixRadius.lean')]:
                        raw=''.join(codes[lo:hi]).encode();assert raw==(C/file).read_bytes();foldchecks.append({'file':file,'sha256':hashlib.sha256(raw).hexdigest(),'byte_exact':True})
                    page.evaluate('scrollTo(0,0)');page.screenshot(path=str(B/(pre+'-all-expanded-top.png')))
                    page.locator('.proof-reader-step').nth(4).scroll_into_view_if_needed();page.screenshot(path=str(B/(pre+'-private-T.png')))
                    tlink=page.locator('a[href*="lesson-sources/Tests/GaussianComplexityFixedSpectrumSourceMatrixRadius.lean.html#L17"]');assert tlink.count()==1,tlink.count()
                    page.goto(urllib.parse.urljoin(page.url,tlink.get_attribute('href')),wait_until='networkidle');assert page.locator('#L17').count()==1
                    lines=page.locator('pre > span[id^="L"]').all_text_contents();raw=('\n'.join(lines)+'\n').encode();assert raw==(C/'Tests/GaussianComplexityFixedSpectrumSourceMatrixRadius.lean').read_bytes()
                    page.locator('#L17').scroll_into_view_if_needed();page.screenshot(path=str(B/(pre+'-T-source-L17.png')))
                    report['source_checks'].append({'path':rel,'viewport':width,'T_L17_reachable':True,'T_full_source_byte_exact':True})
                    report['contexts'].append({'path':rel,'viewport':width,'initial':initial,'math_expanded':math,'all_expanded':expanded,'table_metrics':tablemetrics,'code_folds':foldchecks})
                for mod in ['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius','Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius']:
                    file=mod.replace('.','/')+'.lean';slug=mod.lower().replace('.','-')
                    page.goto(origin+'modules/'+slug+'.html#complete-module-source',wait_until='networkidle')
                    page.locator('#complete-module-source details').evaluate('(e)=>e.open=true')
                    assert page.locator('#complete-module-source pre code').inner_text().encode()==(C/file).read_bytes()
                    with page.expect_download() as di:page.locator('#complete-module-source a[download]').click()
                    downloaded=B/f'{width}-{Path(file).name}';di.value.save_as(str(downloaded));assert downloaded.read_bytes()==(C/file).read_bytes()
                    report['source_checks'].append({'module':mod,'viewport':width,'full_module_byte_exact':True,'download_byte_exact':True})
                context.close()
        finally:browser.close()
except BaseException as e:
    report['attempt_exception']={'class':type(e).__name__,'text':str(e)}
    raise
finally:
    if server:
        if worker:server.shutdown()
        server.server_close()
    if worker:worker.join(timeout=10)
    report['server_thread_joined']=worker is None or not worker.is_alive()
    (B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
assert not report['page_errors'] and not report['failed_requests'] and not report['http_errors']
assert not report['layout_failures'],report['layout_failures']
print('BOUNDED_READER_PASS',variant,'4contexts 6folds 226P+95T byteexact; sources/downloads checked',flush=True)
