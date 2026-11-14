import contextlib,functools,hashlib,http.server,json,pathlib,re,socketserver,sys,threading,time,urllib.parse
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent; C=ROOT/'candidate';SITE=ROOT/'bounded-site';SHOT=ROOT/'browser';SHOT.mkdir(exist_ok=True)
sys.path[:0]=[str(C/'tools'),str(C/'website/scripts')]
import astis_site as base,inline_lean
declarations={d.full_name:d for d in base.scan_project_sources()[1]}
manifest=json.loads((ROOT/'renderer-manifest.json').read_text())
units={}
for slug in ['huanjian-real-matrix-positive-integral','huanjian-gaussian-source-matrix-variance']:
    obj=json.loads((C/'website/content/declaration_lessons'/f'{slug}.json').read_text())
    for u in obj.get('units',[]) if isinstance(obj,dict) else obj: units[u['declaration']]=u
class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,format,*args): pass
server=socketserver.TCPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(SITE)))
worker=threading.Thread(target=server.serve_forever);worker.start()
results=[]
try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    try:
      for width in [1440,390]:
        context=browser.new_context(viewport={'width':width,'height':1000},device_scale_factor=1)
        page=context.new_page()
        for row in manifest['pages']:
          errors=[];failed=[]
          page.on('pageerror',lambda err:errors.append(str(err)))
          url=f'http://127.0.0.1:{server.server_address[1]}/'+row['path']
          response=page.goto(url,wait_until='networkidle');assert response.status==200
          page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise.then(() => true)')
          page.evaluate('MathJax.typesetPromise()')
          article=page.locator('article[data-authored-declaration]');assert article.count()==1
          name=article.get_attribute('data-authored-declaration');u=units[name];d=declarations[name]
          initial=article.locator('details.inline-lean').evaluate_all('(xs)=>xs.map(x=>({open:x.open,role:x.className,summary:x.querySelector("summary").textContent}))')
          assert len(initial)==2 and all(not x['open'] for x in initial)
          assert article.locator('.proof-reader-step').count()==len(u['steps'])
          text=article.inner_text()
          for a in u['assumptions']:assert a.replace('`','') in article.text_content().replace('`',''),a
          sig,_=inline_lean.split_statement(inline_lean.display_source(d.source_text))
          expected=[sig,inline_lean.display_source(d.source_text)]
          panels=article.locator('details.inline-lean > pre > code')
          assert panels.count()==2
          assert [panels.nth(i).text_content() for i in range(2)]==expected
          local=[]
          for link in article.locator('a').evaluate_all('(xs)=>xs.map(x=>({href:x.getAttribute("href"),text:x.textContent}))'):
            href=link['href'] or ''
            assert not href.startswith(('file:','/Users/','.astis/')),href
            if 'downloads/lean/' in href or 'modules/' in href or 'data/lesson-sources/' in href:
              parsed=urllib.parse.urlsplit(urllib.parse.urljoin(url,href));path=SITE/urllib.parse.unquote(parsed.path.lstrip('/'))
              assert path.is_file(),str(path)
              if 'downloads/lean/' in href:assert path.read_bytes()==(C/d.source_file).read_bytes()
              if parsed.fragment:
                assert f'id="{parsed.fragment}"' in path.read_text(),href
              local.append(href)
          overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth+1');assert not overflow
          mjx=article.locator('mjx-container').count();assert mjx>=1
          assert page.locator('mjx-merror').count()==0
          stem=f'{row["kind"]}-{row["slug"]}-{width}'
          page.screenshot(path=str(SHOT/(stem+'-initial.png')),full_page=True)
          article.locator('details.assumption-ledger > summary').click()
          for details in article.locator('details.proof-reader-step').all():
            if not details.evaluate('(x)=>x.open'):details.locator(':scope > summary').click()
          article.locator('details.inline-lean-statement > summary').click()
          article.locator('details.inline-lean-proof > summary').click()
          article.locator('details.boundary-ledger > summary').click()
          page.evaluate('MathJax.typesetPromise()')
          assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth+1')
          assert page.locator('mjx-merror').count()==0
          page.screenshot(path=str(SHOT/(stem+'-expanded.png')),full_page=True)
          downloads=article.locator('a[download]').count();assert downloads==2
          result={**row,'viewport_width':width,'HTTP_status':response.status,'exact_statement_and_full_proof_match':True,'initial_lean_panels':initial,'proof_steps':len(u['steps']),'assumptions_preserved':True,'local_source_links_checked':local,'download_links':downloads,'MathJax_containers':mjx,'MathJax_errors':0,'document_overflow_initial_and_expanded':False,'page_errors':errors,'screenshots':[stem+'-initial.png',stem+'-expanded.png']}
          assert not errors,errors
          results.append(result);(ROOT/'browser-report.json').write_text(json.dumps(results,indent=2)+'\n')
          print(json.dumps({'page':row['path'],'width':width,'pass':True,'MathJax_containers':mjx}),flush=True)
        context.close()
    finally:browser.close()
finally:
  server.shutdown();server.server_close();worker.join()
print('BOUNDED_DESKTOP_MOBILE_BROWSER_CHECKS_OK',flush=True)
