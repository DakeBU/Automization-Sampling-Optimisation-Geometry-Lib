"""CONDITIONAL new Geometry browser helper: unexecuted; real current sourceV/soleSTAB/core gates and separate new root+OS authorization required."""
import datetime,functools,hashlib,http.server,json,re,subprocess,sys,threading
from pathlib import Path
from urllib.parse import quote,urljoin,urlsplit
sys.dont_write_bytecode=True
from geometry_browser_common_v1 import parse_args,load_authorization,authorized_context
authorization_args=parse_args(__doc__)
authorization,authorization_ref=load_authorization(authorization_args)
authorization_readback=authorized_context(authorization)
from playwright.sync_api import sync_playwright
ROOT=Path.cwd();assert ROOT==Path('/Users/zhouhuanjian/ASTIS-GC')
SITE=ROOT/'_site';sys.path[:0]=[str(ROOT/'website/scripts'),str(ROOT/'tools')]
import inline_lean,astis_site,astis_publication
sha=lambda raw:hashlib.sha256(raw).hexdigest()
HEAD=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
CANDIDATE='ab8b47caed9f781191f8408154cd355c7e7c104c'
PREFIX='AutoSamplingTheory.ExampleCases.GaussianComplexity.'
NAME=PREFIX+'FixedSpectrumGeometry.actual_potential_geometry'
MODULE=PREFIX+'FixedSpectrumGeometry'
ITEM='huanjian-fixed-spectrum-geometry'
BINDING='69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa'
ADMISSIBILITY=PREFIX+'FixedSpectrumAdmissibility.actual_precision_admissible'
FIRST=PREFIX+'FixedSpectrumFirstOrder.actual_first_order_query'
CONVERSE='AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound'
PRODUCER_ASTIS_PARENTS=[ADMISSIBILITY,FIRST,CONVERSE]
CONSUMER_ASTIS_PARENTS=[NAME,FIRST]
PINS={'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumGeometry.lean': 'd7edd1684006382e7e51ff717b5a9b82308181538ae824598961604dacea08d6', 'Tests/GaussianComplexityFixedSpectrumGeometry.lean': 'c6f90cc8ad43182a81e8b4343b28fff34e4fc81bc2e181d91002f3005a463b88', 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAdmissibility.lean': '0e3fea5e779787d9a5365b639fdb5bff8e4a76d9e53a6dba811531db321f2241', 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumFirstOrder.lean': '1af1a71edf059edfe10a2b5069002fe703b6f2d1a30c153951e06afd3b8e6423', 'AutoSamplingTheory/TechnicalLemmas/Analysis/StrongConvexGradientConverse.lean': '3110476d62f569293ece3f78b556b1123ffd4c949b4de4bbc1edba23332e9e14', 'website/content/declaration_lessons/huanjian-fixed-spectrum-geometry.json': '03a6e84e941b3e94ff9936ede8bee2b69d82046042ccc9e22f3acbb61cae2e52', 'website/content/publications/huanjian-fixed-spectrum-geometry.json': 'bb5b9ef1e4cc6a9cb41e7db62b4c62c99117448f52106ce8f556d736b919a88d', 'lean-toolchain': '302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b', 'lake-manifest.json': 'b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37', 'website/static/underlying-lean-graph.js': '016c11a60392c449ebb28e8bedc7d3ab69134fff8dde4b438fd06c9f6c951a3a', 'website/static/information-architecture.css': 'a41ffd9d41e8c281aa716fcff25e42e5cb8d14208badff456a0dff7dfbb1b766', 'website/content/graph_memory_index.json': 'e72359bd0ecec17d101cb28c0a3162f8f9cda625b2bcf698f0e68b40a116d01b', 'website/content/functor_hypergraph.json': 'c67be70d121fdfb29a15124e1fc964342902cabf25ac009c607cc5485fc2ed98', 'website/content/samplewiki_companion_frontiers.json': 'bd15fed6f4bb6652f3197a388d36cd0fb029a20eff06bf97afaba3bfe86e2554'}
for path,digest in PINS.items():
 raw=(ROOT/path).read_bytes();assert sha(raw)==digest,path;assert subprocess.check_output(['git','show',HEAD+':'+path])==raw,path
for path in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumGeometry.lean','Tests/GaussianComplexityFixedSpectrumGeometry.lean']:
 assert subprocess.check_output(['git','show',CANDIDATE+':'+path])==(ROOT/path).read_bytes()
assert (SITE/'assets/information-architecture.css').read_bytes()==(ROOT/'website/static/information-architecture.css').read_bytes()
assert (SITE/'assets/underlying-lean-graph.js').read_bytes()==(ROOT/'website/static/underlying-lean-graph.js').read_bytes()
metadata_path=SITE/'data/build-metadata.json';metadata=json.loads(metadata_path.read_bytes())
gate_path=ROOT/'.astis/site-lean-gate.json';gate=json.loads(gate_path.read_bytes())
assert gate['passed'] and gate['commit']==metadata['git']['commit']==HEAD
assert metadata['gate']['passed'] and metadata['gate']['current']
assert gate['source_digest']==metadata['source_digest']==astis_site.source_digest()==authorization['source_digest']
unit=json.loads((ROOT/'website/content/declaration_lessons/huanjian-fixed-spectrum-geometry.json').read_bytes())['units'][0]
assert unit['declaration']==NAME and unit['reading_layout']=='progressive' and len(unit['steps'])==7 and unit['astis_dependencies']==PRODUCER_ASTIS_PARENTS and unit['mathlib_dependencies']
capsule_path=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-semantic-evidence/local-proof-capsule.json'
capsule=json.loads(capsule_path.read_bytes())
assert capsule['actual_direct_ASTIS_producer_parents']==PRODUCER_ASTIS_PARENTS and set(capsule['actual_direct_ASTIS_private_consumer_parents'])==set(CONSUMER_ASTIS_PARENTS)
assert capsule['production_raw_sha256']==PINS['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumGeometry.lean'] and capsule['Test_raw_sha256']==PINS['Tests/GaussianComplexityFixedSpectrumGeometry.lean']
pub=next(x for x in astis_publication.load() if x['id']==ITEM);assert astis_publication.binding_digest(pub,pub['bindings'][0])==BINDING
astis_publication.check_advance([NAME],reviewed=True)
rows={x['declaration']:x for x in json.loads((SITE/'data/declaration-exposition.json').read_bytes())};declarations=inline_lean.declarations()
site_data=json.loads((SITE/'data/site-data.json').read_bytes())
assert not any('actual_first_order_oracle_measurable' in x['local_decl'] for x in site_data['registry_declarations'])
graph=json.loads((SITE/'data/underlying-lean-graph.json').read_bytes());nodes={x['id']:x for x in graph['nodes']}
own_id='decl:'+NAME;module_id='module:'+MODULE;parent_ids=['decl:'+parent for parent in PRODUCER_ASTIS_PARENTS]
for ident in [own_id,module_id,*parent_ids]:assert sum(x['id']==ident for x in graph['nodes'])==1
for parent,parent_id in zip(PRODUCER_ASTIS_PARENTS,parent_ids):
 assert nodes[parent_id]['kind']=='declaration'
 assert sum(e['source']=='module:'+parent.rsplit('.',1)[0] and e['target']==parent_id and e['relation']=='declares' for e in graph['edges'])==1
 refs=[e for e in graph['edges'] if e['source']==parent_id and e['target']==own_id];assert len(refs)==1 and refs[0]['relation']=='source reference (scanner)'
assert sorted(e['source'] for e in graph['edges'] if e['target']==own_id and e['relation']=='source reference (scanner)')==parent_ids
assert sum(e['source']==module_id and e['target']==own_id and e['relation']=='declares' for e in graph['edges'])==1
model=json.loads((ROOT/'website/content/functor_hypergraph.json').read_bytes());memory=json.loads((ROOT/'website/content/graph_memory_index.json').read_bytes())
bridge='transport:gaussian-quadratic-oracle-factorization';edge=next(x for x in model['hyperedges'] if x['id']==bridge);family=next(x for x in memory['families'] if x['id']=='family:gaussian-oracle-hardness')
assert edge['formal_refs']==[] and edge['status']=='not-Lean-certified'
concept_module=PREFIX+'FixedSpectrumFirstOrder';concept_module_id='module:'+concept_module
assert sum(x['node']==concept_module for x in family['compiled_substrate_bindings'])==1
assert not any(x['node']==MODULE for x in family['compiled_substrate_bindings'])
assert nodes[bridge]['hyperedge']==edge and concept_module_id in nodes[bridge]['candidate_substrates']
assert module_id not in nodes[bridge]['candidate_substrates']
incidence=[e for e in graph['edges'] if e['source']==concept_module_id and e['target']==bridge]
assert len(incidence)==1 and 'candidate' in incidence[0]['relation'].lower()
OUT=ROOT/'.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader/browser'/('live-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));OUT.mkdir(parents=True,exist_ok=False)
report={'head':HEAD,'candidate_commit':CANDIDATE,'candidate_source_digest':authorization['candidate_source_digest'],'mode':'Actual current local HTTP site, installed headless Chrome; external hosts blocked. This report exists only after explicit future authorization.','site_metadata_sha256':sha(metadata_path.read_bytes()),'actual_gate_sha256':sha(gate_path.read_bytes()),'actual_gate_commit':gate['commit'],'site_commit':metadata['git']['commit'],'source_digest':gate['source_digest'],'publication_binding_sha256':BINDING,'input_pins':PINS,'pages':[],'graphs':[],'old_long_Lean_layout_regressions':[],'native_selection_geometry':[],'UI_repair':authorization['reviewed_UI_repair'],'site_layout_css_sha256':sha((SITE/'assets/information-architecture.css').read_bytes()),'visible_source_index_clicks':[],'errors':[],'screenshots':[],'authorization':authorization_ref,'authorization_readback':authorization_readback,'external_GitHub_HTML_checked':False,'external_source_boundary':'Own-site source/module/downloads checked against candidate/current immutable local Git. GitHub syntax only if that branch executes, never external HTML/public HTTP delivery.','producer_ASTIS_parents':PRODUCER_ASTIS_PARENTS,'consumer_ASTIS_parents':CONSUMER_ASTIS_PARENTS,'producer_parent_evidence':{'capsule':str(capsule_path.relative_to(ROOT)),'sha256':sha(capsule_path.read_bytes()),'scope':'Already existing genuine kernel inventory, not scanner export or fresh compilation by browser.'},'consumer_visibility':'Private Test only; exactly new Geometry and canonical FirstOrder. Actual fixed-input Borel pair, with no joint/adaptive/query-cap/cost theorem or public Registry consumer.'}

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(SITE)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}/'


def screenshot(page, name):
    p = OUT / (name + '.png')
    page.screenshot(path=str(p))
    report['screenshots'].append({'file': p.name, 'sha256': sha(p.read_bytes())})


def math_ready(page):
    page.wait_for_function('Boolean(window.MathJax?.startup?.promise)', timeout=30000)
    page.evaluate('() => MathJax.startup.promise')
    assert page.locator('mjx-container').count() > 0
    assert page.locator('mjx-merror, [data-mjx-error]').count() == 0


def no_page_overflow(page):
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), page.url


def ordinary_prose_bounds(page, paragraph):
    # Read-only Range geometry exposes clipping hidden by html/body overflow:clip.
    paragraph.scroll_into_view_if_needed()
    g = paragraph.evaluate("""node => {
      const rect = r => ({left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height});
      const range = document.createRange(); range.selectNodeContents(node);
      const mobile = document.querySelector('.mobile-bar');
      const header = mobile && getComputedStyle(mobile).display !== 'none' ? mobile.getBoundingClientRect().bottom : 0;
      return {viewport_width:innerWidth,viewport_height:innerHeight,unobscured_top:Math.max(0,header),
        article:rect(node.closest('.theorem-layout > article').getBoundingClientRect()),
        paragraph:rect(node.getBoundingClientRect()),text_rects:[...range.getClientRects()].filter(r=>r.width>0&&r.height>0).map(rect),
        vertical_scope:'Full warning paragraph; whole article remains vertically scrollable.'};
    }""")
    for key in ('article', 'paragraph'):
        assert g[key]['left'] >= -1 and g[key]['right'] <= g['viewport_width'] + 1
    assert g['text_rects']
    for r in g['text_rects']:
        assert r['left'] >= -1 and r['right'] <= g['viewport_width'] + 1
        assert r['top'] >= g['unobscured_top'] - 1 and r['bottom'] <= g['viewport_height'] + 1
    return g


# Read-only native post-navigation geometry. No Fit/pan/transform mutation.
NATIVE_GEOMETRY_JS = r"""args => {
  const rect = r => ({left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height});
  const selected = [...document.querySelectorAll('.ulg-node.selected')];
  const node = selected.find(n => n.dataset.id === args.id);
  const svg = document.querySelector('[data-graph-svg]');
  const canvas = document.querySelector('[data-graph-canvas]');
  const detail = document.querySelector('[data-graph-detail]');
  const box = node?.querySelector(':scope > rect');
  const label = node?.querySelector(':scope > text.label');
  if (!node || !svg || !canvas || !detail || !box || !label) return null;
  const mobile = document.querySelector('.mobile-bar');
  const top = mobile && getComputedStyle(mobile).display !== 'none' ? Math.max(0,mobile.getBoundingClientRect().bottom) : 0;
  const labelMatrix = label.getScreenCTM();
  if (!labelMatrix) return null;
  const font = parseFloat(getComputedStyle(label).fontSize) * Math.hypot(labelMatrix.a,labelMatrix.b);
  const viewport = {left:0,right:innerWidth,top,bottom:innerHeight};
  const s = rect(svg.getBoundingClientRect()), c = rect(canvas.getBoundingClientRect());
  const r = rect(box.getBoundingClientRect()), l = rect(label.getBoundingClientRect());
  const inside = (a,b) => a.left >= b.left-1 && a.right <= b.right+1 && a.top >= b.top-1 && a.bottom <= b.bottom+1;
  const actualKind = detail.dataset.kind;
  const actualLabel = detail.querySelector(':scope > header > h2')?.textContent;
  const query = document.querySelector('[data-graph-search]')?.value.trim();
  const checks = {
    unique_selected:selected.length===1,
    source_kind:actualKind===args.kind,
    source_full_name:actualLabel===args.label,
    expected_view:canvas.dataset.view===args.view,
    nonempty_query:Boolean(query),
    readable_card:r.width>=160 && r.height>=40,
    readable_label:font>=10 && l.width>=80 && l.height>=10 && Boolean(label.textContent.trim()),
    full_card_inside_svg:inside(r,s),full_card_inside_canvas:inside(r,c),full_card_inside_viewport:inside(r,viewport),
    full_label_inside_svg:inside(l,s),full_label_inside_canvas:inside(l,c),full_label_inside_viewport:inside(l,viewport),
    full_label_inside_card:inside(l,r)
  };
  return {id:args.id,expected_kind:args.kind,expected_label:args.label,actual_kind:actualKind,actual_label:actualLabel,
    actual_view:canvas.dataset.view,query,viewport,svg:s,canvas:c,selected_main_rect:r,rendered_label:l,
    rendered_label_font_px:font,rendered_label_text:label.textContent,checks,ok:Object.values(checks).every(Boolean)};
}"""


def native_selection_geometry(page, ident, view):
    args = {'id': ident, 'kind': nodes[ident]['kind'], 'label': nodes[ident]['label'], 'view': view}
    # Keep the normal Playwright timeout. Wait real layout, then allow all queued
    # fit callbacks to finish before a second read; scheduling is not a camera action.
    page.wait_for_function('args => (' + NATIVE_GEOMETRY_JS + ')(args)?.ok === true', arg=args)
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve(true))))')
    geometry = page.evaluate(NATIVE_GEOMETRY_JS, args)
    assert geometry and geometry['ok'], geometry
    assert all(geometry['checks'].values()), geometry
    geometry['camera_actions_by_harness'] = []
    geometry['scope'] = 'Actual native selection geometry after queued callbacks; read-only DOM/UI, not an additional image review.'
    return geometry


def focused_entry(page, ident, query, view='lean'):
    route = 'lean-foundations.html?view=' + view + '&focus=' + quote(ident, safe='') + '&q=' + quote(query, safe='')
    assert page.goto(base + route, wait_until='domcontentloaded').status == 200
    page.wait_for_selector('.ulg-canvas[data-view="' + view + '"][data-local="true"]')
    selected = page.locator('.ulg-node.selected[data-id="' + ident + '"]')
    selected.wait_for()
    page.wait_for_function("document.querySelector('.ulg-canvas>small').textContent.includes('Focused result at readable scale')")
    math_ready(page)
    page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
    box = selected.locator('rect').bounding_box()
    canvas = page.locator('[data-graph-canvas]').bounding_box()
    assert box['width'] >= 160 and box['x'] >= canvas['x'] - 1 and box['x'] + box['width'] <= canvas['x'] + canvas['width'] + 1
    selected.click()
    no_page_overflow(page)
    native_geometry = native_selection_geometry(page, ident, view)
    return {'native_post_click_geometry':native_geometry,'route': route, 'selected_native_click': True, 'node_box': box, 'canvas_box': canvas, 'scope': 'Readable focused entry plus native click; no all-label Fit readability or manual touch gesture claim.'}


try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        report['browser_version'] = browser.version
        for width in (1440, 390):
            context = browser.new_context(viewport={'width': width, 'height': 1000 if width > 400 else 844})
            context.route(re.compile(r'https?://(?!127\.0\.0\.1:)'), lambda route: route.abort())
            page = context.new_page()
            page.on('pageerror', lambda error: report['errors'].append(str(error)))
            route = rows[NAME]['page']
            assert page.goto(base + route, wait_until='domcontentloaded').status == 200
            math_ready(page)
            assert HEAD[:12] in page.locator('.verification-strip').text_content()
            article = page.locator(f'article[data-authored-declaration="{NAME}"]')
            assert article.count() == 1 and article.locator('details[open]').count() == 0
            assert article.locator('.reader-main-equation mjx-container').count() == 1
            statement = article.locator(f'details.inline-lean-statement[data-inline-lean="{NAME}"]')
            proof = article.locator(f'details.inline-lean-proof[data-inline-lean="{NAME}"]')
            exact = inline_lean.display_source(declarations[NAME].source_text)
            signature, _ = inline_lean.split_statement(exact)
            assert statement.locator('code.language-lean').first.text_content() == signature
            assert proof.locator('code.language-lean').first.text_content() == exact
            assert article.locator('.reader-first-pass details.inline-lean-statement').count() == 1
            assert article.locator('.lean-verification details.inline-lean-proof').count() >= 1
            no_page_overflow(page)
            article.locator('.reader-first-pass').scroll_into_view_if_needed()
            screenshot(page, f'actual-{width}-first')
            assumptions = article.locator('.assumption-ledger')
            assumptions.locator(':scope > summary').click()
            txt = assumptions.text_content()
            for phrase in ('either determinant sign', 'no additive shift', 'All spatial points and pairs', 'Fréchet derivative', 'Strong convexity', 'Haar randomness', 'query budgets'):
                assert phrase.lower() in txt.lower(), phrase
            assert assumptions.get_attribute('open') is not None
            no_page_overflow(page)
            assumptions.scroll_into_view_if_needed()
            screenshot(page, f'actual-{width}-assumptions')
            assumptions.locator(':scope > summary').click()
            steps = article.locator('details.reader-proof-disclosure')
            assert steps.count() == 7
            for i in range(7):
                step = steps.nth(i)
                step.locator('summary').first.click()
                assert step.locator('mjx-container').count() > 0
                assert unit['steps'][i]['title'] in step.text_content()
                nested = step.locator('.reader-step-body > details')
                assert nested.count() == 1 and nested.get_attribute('open') is None
                nested.locator(':scope > summary').click()
                assert unit['steps'][i]['lean'] in nested.text_content()
                # Exact authored correspondence is checked for every one of the seven steps.
                # Actual kernel parents remain separately pinned evidence.
                no_page_overflow(page)
                step.scroll_into_view_if_needed()
                screenshot(page, f'actual-{width}-proof-step{i+1}')
                nested.locator(':scope > summary').click()
                step.locator('summary').first.click()
            provenance = article.locator('details.proof-reader-provenance')
            assert provenance.count() == 1
            provenance.locator(':scope > summary').click()
            parent_list = provenance.locator('ul').first.locator('li')
            assert parent_list.count() == 3
            for i, parent in enumerate(PRODUCER_ASTIS_PARENTS):
                assert parent_list.nth(i).locator('code').text_content() == parent
                parent_source_href = parent_list.nth(i).locator('a').get_attribute('href')
                assert context.request.get(urljoin(page.url, parent_source_href)).status == 200
            for dep in unit['mathlib_dependencies']:
                assert dep in provenance.text_content(), dep
            assert 'Samplinglib parents called' in provenance.text_content() and 'Mathlib API called' in provenance.text_content()
            provenance.scroll_into_view_if_needed()
            no_page_overflow(page)
            screenshot(page, f'actual-{width}-standard-reuse')
            provenance.locator(':scope > summary').click()
            statement.locator('summary').first.click()
            assert statement.locator('code.language-lean').first.is_visible()
            statement.locator('summary').first.scroll_into_view_if_needed()
            no_page_overflow(page)
            screenshot(page, f'actual-{width}-exact-statement')
            statement.locator('summary').first.click()
            proof.locator('summary').first.click()
            proof.locator('summary').first.scroll_into_view_if_needed()
            assert proof.locator('code.language-lean').first.is_visible()
            local_scroll = proof.locator('pre').first.evaluate('node => { const max=node.scrollWidth-node.clientWidth; node.scrollLeft=max; const actual=node.scrollLeft; node.scrollLeft=0; return {clientWidth:node.clientWidth,scrollWidth:node.scrollWidth,max,actual}; }')
            if local_scroll['max'] > 1:
                assert local_scroll['actual'] > 0
            no_page_overflow(page)
            screenshot(page, f'actual-{width}-exact-proof')
            module_href = proof.locator('a').filter(has_text='Exact module and namespace context').get_attribute('href')
            module_url = urljoin(page.url, module_href)
            download = proof.locator('a[download]').first.get_attribute('href')
            actual_source = (ROOT / declarations[NAME].source_file).read_bytes()
            response = context.request.get(urljoin(page.url, download))
            assert response.status == 200 and response.body() == actual_source
            assert subprocess.check_output(['git', 'show', HEAD + ':' + str(declarations[NAME].source_file)]) == actual_source
            immutable_link = None
            if urlsplit(module_url).netloc == 'github.com':
                expected = metadata['git']['web_root'] + '/blob/' + HEAD + '/' + str(declarations[NAME].source_file)
                assert module_url.startswith(expected + '#L')
                immutable_link = module_url
                module_url = base + 'modules/' + inline_lean.base.slugify(declarations[NAME].module) + '.html#complete-module-source'
            assert page.goto(module_url, wait_until='domcontentloaded').status == 200
            page.locator('#complete-module-source > details > summary').click()
            assert page.locator('#complete-module-source pre > code').text_content().encode() == actual_source
            page.locator('#complete-module-source').scroll_into_view_if_needed()
            no_page_overflow(page)
            screenshot(page, f'actual-{width}-module')
            report['pages'].append({'target': NAME, 'route': route, 'width': width, 'closed_initially': True, 'seven_formula_steps_opened': True, 'adjacent_exact_statement_and_proof': True, 'local_code_scroll': local_scroll, 'full_module_download_immutable_git_bytes_verified': True, 'immutable_link_syntax_checked': immutable_link, 'producer_ASTIS_parents': PRODUCER_ASTIS_PARENTS, 'consumer_ASTIS_parents': CONSUMER_ASTIS_PARENTS, 'consumer_private_name_only': True, 'consumer_fixed_input_actual_Borel': True, 'module_link_branch': 'GitHub commit/path syntax plus local own-site module' if immutable_link else 'own-site module only; GitHub syntax branch not executed', 'external_GitHub_HTML_checked': False, 'fullpage_overflow': False, 'screenshot_scope': 'Viewport captures only; long code/assumptions require local scrolling and are not claimed fully visible in one image.'})

            test_rows = [row for row in site_data['modules'] if row['name'] == 'Tests.GaussianComplexityFixedSpectrumGeometry']
            assert len(test_rows) == 1
            assert page.goto(urljoin(base, test_rows[0]['page']), wait_until='domcontentloaded').status == 200
            page.locator('#complete-module-source > details > summary').click()
            test_source = (ROOT / test_rows[0]['source_file']).read_bytes()
            assert page.locator('#complete-module-source pre > code').text_content().encode() == test_source
            test_download = page.locator('#complete-module-source a[download]')
            assert test_download.count() == 1
            test_response = context.request.get(urljoin(page.url, test_download.get_attribute('href')))
            assert test_response.status == 200 and test_response.body() == test_source
            assert subprocess.check_output(['git','show',HEAD+':'+test_rows[0]['source_file']]) == test_source
            assert subprocess.check_output(['git','show',CANDIDATE+':'+test_rows[0]['source_file']]) == test_source
            report['pages'][-1]['private_Test_source_pin'] = {'route':test_rows[0]['page'],'sha256':sha(test_source),'DOM_download_candidate_and_current_Git_exact':True,'pixel_review_claim':False}

            chapter = 'example-cases/samplewiki/companions/gaussian-sampling-complexity.html'
            assert page.goto(base + chapter, wait_until='domcontentloaded').status == 200
            math_ready(page)
            main = page.locator('#gaussian-complexity-eigenbasis')
            ancestors = main.locator('xpath=ancestor::details')
            for ancestor_index in reversed(range(ancestors.count())):
                ancestor = ancestors.nth(ancestor_index)
                if ancestor.get_attribute('open') is None:
                    ancestor.locator(':scope > summary').click()
                    assert ancestor.get_attribute('open') is not None
            boundary = main.text_content()
            for phrase in ('The full Theorem 4.1 lower bound remains open', 'Lemma4.6 precursor', 'every full real', 'Euclidean Lebesgue volume', 'real exponent', 'not another producer proof parent', 'actual source determinant product', 'canonical DisplacementJacobianEntropy', 'independent of orientation', 'retains the actual hidden', 'actual unweighted Euclidean Gaussian normalizing integral', 'actual fixed-spectrum C4 geometry', 'Section 4.4 limits this uniform-Krylov/test analysis', 'not an impossibility theorem for stronger fixed-spectrum lower bounds'):
                assert phrase in boundary, phrase
            for phrase in ('actual fixed-spectrum first-order reply', 'genuine derivative existence', 'sole producer parent is canonical actual admissibility', 'same-O affine provider', 'not an operational one-query or adaptive transcript theorem'):
                assert phrase in boundary, phrase
            for phrase in ('genuine gradient derivative', '1-strongly convex', 'value zero uniquely at the origin', 'three direct kernel ASTIS parents', 'Borel measurable for each fixed hidden input', 'strict angle/cosine prefix', 'generic Hessian-criterion route', 'deterministic worst-query caps', 'explicit expected-cost reductions'):
                assert phrase in boundary, phrase
            determinant_text = page.locator('#gaussian-complexity-determinant').text_content()
            for phrase in ('The full Theorem 3.1 lower bound remains open', 'worst-case deterministic query cap', 'not an expected-cost lower bound without a separate reduction', 'Actual amplified TV Ex72', 'actual pointwise first-order reconstruction'):
                assert phrase in determinant_text, phrase
            no_page_overflow(page)
            main.scroll_into_view_if_needed()
            screenshot(page, f'case-boundary-{width}')
            index = page.locator('#paper-lean-progress')
            index.scroll_into_view_if_needed()
            screenshot(page, f'source-index-{width}')
            outer = index.locator('details.paper-verified-index')
            if outer.get_attribute('open') is None:
                outer.locator(':scope > summary').click()
            sourceunit = outer.locator(f'details.paper-verified-unit[data-publication-item="{ITEM}"]')
            if sourceunit.get_attribute('open') is None:
                sourceunit.locator(':scope > summary').click()
            link = sourceunit.locator(f'a[href$="source-{ITEM}.html"]')
            assert link.count() == 1 and link.is_visible()
            sourceunit.scroll_into_view_if_needed()
            screenshot(page, f'actual-{width}-source-index-open')
            assert context.request.get(urljoin(page.url, link.get_attribute('href'))).status == 200
            link.click()
            page.wait_for_url('**/proofs/source-' + ITEM + '.html')
            math_ready(page)
            assert page.locator(f'article[data-authored-declaration="{NAME}"]').count() == 1
            report['visible_source_index_clicks'].append({'target': NAME, 'width': width, 'actual_click': True})
            no_page_overflow(page)

            focus = focused_entry(page, own_id, NAME)
            assert page.locator(f'.ulg-node[data-id="{own_id}"]').count() == 1
            assert page.locator(f'.ulg-node[data-id="{module_id}"]').count() == 1
            assert page.locator('.ulg-edge[data-relation="source reference (scanner)"][data-evidence="formal"]').count() == 0
            assert page.locator('.ulg-edge[data-relation="source correspondence; not a Lean dependency"][data-evidence="formal"]').count() == 0
            screenshot(page, f'actual-{width}-graph-focused')
            for i, parent_id in enumerate(parent_ids, 1):
                focused_entry(page, own_id, NAME)
                parent_neighbor = page.locator(f'[data-graph-detail] button[data-jump="{parent_id}"]')
                assert parent_neighbor.count() == 1
                parent_neighbor.click()
                page.wait_for_selector(f'.ulg-node.selected[data-id="{parent_id}"]')
                assert page.locator('[data-graph-detail]').get_attribute('data-kind') == 'declaration'
                page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
                no_page_overflow(page)
                parent_geometry = native_selection_geometry(page, parent_id, 'lean')
                report['native_selection_geometry'].append({'width':width,'route':'native-Lean-parent','geometry':parent_geometry,'main_original':f'canonical-parent{i}-{width}-graph-native-parent-click.png','extra_screenshot':False})
                screenshot(page, f'canonical-parent{i}-{width}-graph-native-parent-click')
            focused_entry(page, own_id, NAME)
            neighbor = page.locator(f'[data-graph-detail] button[data-jump="{module_id}"]')
            assert neighbor.count() == 1
            neighbor.click()
            page.wait_for_selector(f'.ulg-node.selected[data-id="{module_id}"]')
            assert page.locator('[data-graph-detail]').get_attribute('data-kind') == 'module'
            page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
            no_page_overflow(page)
            module_geometry = native_selection_geometry(page, module_id, 'lean')
            report['native_selection_geometry'].append({'width':width,'route':'native-Lean-module','geometry':module_geometry,'main_original':f'actual-{width}-graph-module-native-click.png','extra_screenshot':False})
            screenshot(page, f'actual-{width}-graph-module-native-click')
            report['graphs'].append({'target': own_id, 'width': width, 'one_canonical_producer': True, 'producer_ASTIS_parents': PRODUCER_ASTIS_PARENTS, 'native_three_canonical_parent_clicks': True, 'source_scanner_edge_not_kernel_evidence': True, 'owner_module': module_id, 'focused_entry': focus, 'native_neighbor_module_click': True, 'semantic_boundary': 'THREE separately kernel-confirmed producer parents: actual admissibility, actual FirstOrder and the same canonical gradient converse. TWO private Borel Test parents: Geometry plus FirstOrder. Scanner references remain dashed/incomplete, never complete kernel export. No old GPD/source/audit/model history changes.'})

            # One existing generic long-Lean card regression; no extra main PNGs.
            old_name = 'AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity.normalized_density_tv_affinity'
            old_rows = [r for r in json.loads((SITE / 'data/site-data.json').read_bytes())['registry_declarations'] if r['local_decl'] == old_name]
            assert len(old_rows) == 1
            assert page.goto(urljoin(base, old_rows[0]['card']), wait_until='domcontentloaded').status == 200
            old_mode = page.locator('.lean-learning-studio button[data-reading-mode="lean"]')
            assert old_mode.count() == 1
            old_mode.click()
            old_heading = page.locator('.theorem-layout > article h2').filter(has_text=re.compile('^Proof architecture$'))
            assert old_heading.count() == 1
            old_lens = old_heading.locator('xpath=ancestor::details')
            assert old_lens.count() == 1 and 'formalization-lens' in old_lens.get_attribute('class').split()
            old_summary = old_lens.locator(':scope > summary')
            if old_lens.get_attribute('open') is not None:
                old_summary.click()
                assert old_lens.get_attribute('open') is None
            old_summary.click()
            assert old_lens.get_attribute('open') is not None and old_heading.is_visible()
            old_paragraph = old_heading.locator('xpath=following-sibling::p[1]')
            assert old_paragraph.count() == 1 and old_paragraph.is_visible()
            old_bounds = ordinary_prose_bounds(page, old_paragraph)
            old_code = old_lens.locator(':scope > pre.code-block')
            assert old_code.count() == 1
            old_lines = len(old_code.locator('code').text_content().splitlines())
            assert old_lines >= 100
            old_code_geometry = old_code.evaluate('node => ({client_width:node.clientWidth,scroll_width:node.scrollWidth,overflow_x:getComputedStyle(node).overflowX})')
            assert old_code_geometry['client_width'] <= width
            no_page_overflow(page)
            report['old_long_Lean_layout_regressions'].append({'width': width, 'declaration': old_name, 'route': old_rows[0]['card'], 'native_learner_and_summary_clicks': True, 'ordinary_prose_bounds': old_bounds, 'long_Lean_code_lines': old_lines, 'local_code_geometry': old_code_geometry, 'scope': 'One actual UI/geometry regression on an unchanged old175line generic card; no new mathematical/source review or extra main screenshot.'})

            # Unchanged existing FirstOrder conceptual supplement regression only.
            # Geometry gains no candidate incidence or conceptual transport credit.
            bridge_focus = focused_entry(page, bridge, 'Quadratic observations factor', 'functor')
            assert concept_module_id in nodes[bridge]['candidate_substrates']
            assert page.locator(f'.ulg-node[data-id="{concept_module_id}"]').count() == 1
            detail = page.locator('[data-graph-detail]')
            page.wait_for_function("document.querySelector('[data-graph-detail]').dataset.kind === 'concept-bridge'")
            actual_rows = detail.locator('.ulg-details > div').evaluate_all('(nodes)=>Object.fromEntries(nodes.map(n=>[n.querySelector("dt").textContent,n.querySelector("dd").textContent]))')
            for label, field in [('Mechanism','mechanism'),('Hypothesis Map','hypothesis_map'),('Conclusion Map','conclusion_map'),('Failure Boundary','failure_boundary')]:
                assert actual_rows[label] == edge[field]
            assert 'not-Lean-certified' in detail.locator('.ulg-warning').text_content()
            assert detail.locator(f'button[data-jump="{concept_module_id}"]').count() == 1
            assert 'not a one-query operational cap theorem' in edge['critical_estimates'][-1]['status']
            assert edge['critical_estimates'][-1]['supplement_review']['current_theorem_sourceV_granted_by_this_mechanism_review'] is False
            no_page_overflow(page)
            page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
            screenshot(page, f'existing-conceptual-{width}-typed-supplement')
            report['graphs'].append({'target': bridge, 'width': width, 'focused_entry': bridge_focus, 'existing_FirstOrder_typed_supplement_regression': True, 'old_model_binding_critical_estimate_review_history_retained': True, 'canonical_module_candidate_only': concept_module_id, 'formal_refs': [], 'no_formal_transport_or_query_cost_credit': True, 'actual_semantic_rows_equal_reviewed_model': True})
            # Exercise the actual emitted preset caller with the existing query.
            # These additional native routes are DOM/UI-only; no extra PNG claim.
            preset = page.locator('#functor-contract nav[aria-label="Conceptual bridge inspector"] button[data-functor-jump="' + bridge + '"]')
            assert preset.count() == 1
            preset_ancestors = preset.locator('xpath=ancestor::details')
            for ancestor_index in reversed(range(preset_ancestors.count())):
                ancestor = preset_ancestors.nth(ancestor_index)
                if ancestor.get_attribute('open') is None:
                    ancestor.locator(':scope > summary').click()
                    assert ancestor.get_attribute('open') is not None
            assert preset.is_visible()
            preset_query = page.locator('[data-graph-search]').input_value().strip()
            assert preset_query == 'Quadratic observations factor'
            preset.click()
            assert page.locator('[data-graph-search]').input_value().strip() == preset_query
            page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
            preset_geometry = native_selection_geometry(page, bridge, 'functor')
            no_page_overflow(page)
            report['native_selection_geometry'].append({'width':width,'route':'emitted-Functor-preset-with-query','native_preset_click':True,'native_details_ancestors_checked':preset_ancestors.count(),'geometry':preset_geometry,'pixel_review_claim':False,'extra_screenshot':False})
            cross_view_neighbor = page.locator('[data-graph-detail] button[data-jump="' + concept_module_id + '"]')
            assert cross_view_neighbor.count() == 1
            cross_view_neighbor.click()
            page.wait_for_selector('.ulg-canvas[data-view="lean"][data-local="true"]')
            assert page.locator('[data-graph-search]').input_value().strip() == preset_query
            page.locator('[data-graph-canvas]').scroll_into_view_if_needed()
            cross_view_geometry = native_selection_geometry(page, concept_module_id, 'lean')
            no_page_overflow(page)
            report['native_selection_geometry'].append({'width':width,'route':'native-Functor-to-Lean-module','native_neighbor_click':True,'geometry':cross_view_geometry,'pixel_review_claim':False,'extra_screenshot':False})
            context.close()
        assert len(report['screenshots']) == 44
        assert len(report['native_selection_geometry']) == 12
        assert {(row['width'],row['route']) for row in report['native_selection_geometry']} == {(w,r) for w in (1440,390) for r in ('native-Lean-parent','native-Lean-module','emitted-Functor-preset-with-query','native-Functor-to-Lean-module')}
        assert len(report['pages']) == 2 and len(report['graphs']) == 4 and len(report['old_long_Lean_layout_regressions']) == 2
        assert not report['errors'], report['errors']
        assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == HEAD
        for path, digest in PINS.items():
            assert sha((ROOT / path).read_bytes()) == digest
        browser.close()
        report['status'] = 'passed'
except Exception as error:
    report['status'] = 'failed'
    report['failure'] = repr(error)
    raise
finally:
    server.shutdown()
    server.server_close()
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': report.get('status'), 'pages': len(report['pages']), 'graphs': len(report['graphs']), 'screenshots': len(report['screenshots']), 'report': str(OUT / 'report.json')}))
