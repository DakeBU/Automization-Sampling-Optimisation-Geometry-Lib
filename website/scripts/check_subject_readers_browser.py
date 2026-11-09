"""Bounded browser QA; the temporary local server closes on success or failure.

Run with a Python environment containing Playwright and installed Chromium/Edge.
Screenshots are ignored local evidence, not theorem or source-review certificates.
"""
from __future__ import annotations
import argparse
import functools
import http.server
import json
from pathlib import Path
import sys
import threading
from urllib.parse import quote

from playwright.sync_api import sync_playwright


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--channel', default=None, help='e.g. msedge; otherwise installed Chromium')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    evidence = root / '.astis/subject-reader-browser'
    evidence.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root / '_site'))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f'http://127.0.0.1:{server.server_port}/'
    errors = []
    routes = ('sampling/index.html', 'libraries/optimisation/index.html',
              'lower-bounds/index.html', 'libraries/discrete-sampling/index.html')
    paper = 'example-cases/samplewiki/companions/slc-lsi-query-complexity.html'
    # Derive counts from the same canonical bindings as the reader; future
    # admitted results must not require a hard-coded counter edit here.
    sys.path.insert(0, str(root / 'tools'))
    import astis_publication as publication
    items = [item for item in publication.load() if item['chapter_path'] == paper]
    data = publication.inputs()
    names = {b['declaration'] for item in items for b in item['bindings']}
    reviewed = {b['declaration'] for item in items for b in item['bindings']
                if publication.verified_binding(b, data)}
    expected_progress = f'{len(names)} source-mapped declarations; {len(reviewed)} independently reviewed'
    proof_cases = (
        ('slc-lsi-normalized-mass', 'bad_mass_ratio_bounds', 'fact12',
         'AutoSamplingTheory.TechnicalLemmas.Analysis.NormalizedMass.bad_mass_ratio_bounds'),
        ('slc-lsi-gaussian-odd-load', 'gaussian_odd_load_bound', 'fact10',
         'AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad.gaussian_odd_load_bound'),
        ('slc-lsi-energy-truncation', 'energyTruncation_gaussian_bound', 'energy',
         'AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.EnergyTruncation.energyTruncation_gaussian_bound'),
        ('slc-lsi-angular-degree', 'angularDegreeComponent_hasLaw', 'angular',
         'AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree.angularDegreeComponent_hasLaw'),
        ('slc-lsi-coefficient-blocks', 'jointCoefficientBlocks_hasLaw', 'coefficient-blocks',
         'AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.CoefficientBlocks.jointCoefficientBlocks_hasLaw'),
        ('slc-lsi-angular-degree-sum', 'angularDegreeSum_hasLaw', 'angular-degree-sum',
         'AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegreeSum.angularDegreeSum_hasLaw'),
        ('slc-lsi-radial-level', 'radialLevel_hasLaw', 'radial-level',
         'AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevel.radialLevel_hasLaw'),
        ('slc-lsi-radial-levels', 'radialLevels_hasLaw', 'radial-levels',
         'AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevels.radialLevels_hasLaw'),
    )
    assert {case[3] for case in proof_cases} <= reviewed
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel=args.channel, headless=True)
            try:
                page = browser.new_page(viewport={'width': 1440, 'height': 1000})
                page.on('pageerror', lambda e: errors.append(str(e)))
                for width, height, label in ((1440,1000,'desktop'),(390,844,'mobile')):
                    page.set_viewport_size({'width':width,'height':height})
                    for index, route in enumerate(routes):
                        assert page.goto(base + route).status == 200
                        if index >= 2:
                            page.locator('main mjx-container').first.wait_for(state='attached')
                        assert page.locator('main h1').count() == 1
                        assert page.locator('nav[aria-label="Subjects"] a').count() == 4
                        assert not page.locator('mjx-merror, [data-mjx-error]').count()
                        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), route
                        page.screenshot(path=str(evidence / f'{index}-{label}.png'), full_page=True)
                        if index == 2:
                            assert page.locator('#routes .resource-grid > article').count() == 2
                            assert not page.locator('#algorithm-specific details[open], #general details[open]').count()
                            for section in ('mala', 'hmc', 'midpoint', 'optimisation', 'gaussian', 'nonlinear', 'reuse'):
                                panel = page.locator('#' + section)
                                panel.locator(':scope > summary').click()
                                assert panel.evaluate('(x)=>x.open')
                                assert panel.inner_text().strip()
                                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                                panel.screenshot(path=str(evidence / f'lower-{section}-{label}.png'))
                                panel.locator(':scope > summary').click()
                            assert not page.locator('mjx-merror, [data-mjx-error]').count()
                    assert page.goto(base + paper).status == 200
                    page.locator('#slc-cold-main mjx-container').first.wait_for()
                    # Expand actual source content: hidden equations must render too.
                    page.locator('main details').evaluate_all('(xs)=>xs.forEach(x=>x.open=true)')
                    page.evaluate('async()=>{if(window.MathJax?.startup?.promise) await MathJax.startup.promise;}')
                    assert page.locator('#lsi-main mjx-container').count() > 0
                    assert page.locator('#source-outline li').count() >= 12
                    assert not page.locator('mjx-merror, [data-mjx-error]').count()
                    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                    page.screenshot(path=str(evidence / f'paper-{label}.png'))
                    page.locator('#slc-cold-main').screenshot(path=str(evidence / f'statement-{label}.png'))
                    page.locator('#source-outline').screenshot(path=str(evidence / f'source-outline-{label}.png'))
                page.set_viewport_size({'width':1440,'height':1000})
                for method, label in (('mala', 'MALA'), ('hmc', 'Hamiltonian Monte Carlo')):
                    page.goto(base + 'lower-bounds/index.html')
                    panel = page.locator('#' + method)
                    panel.locator(':scope > summary').click()
                    panel.get_by_role('link', name=f'{method.upper()} in Methods × targets').click()
                    assert 'view=perspectives' in page.url
                    page.locator('[data-graph-detail] h2').filter(has_text=label).wait_for()
                    assert page.locator('[data-graph-canvas][data-local="true"]').count() == 1
                    assert 1 < page.locator('.ulg-node').count() <= 10
                    assert page.locator('.ulg-node').evaluate_all('''nodes => nodes.every(node => {
                        const label = node.querySelector('.label').getBBox();
                        const box = node.querySelector('rect').getBBox();
                        return label.x + label.width <= box.x + box.width - 2;
                    })'''), 'Focused method labels must fit inside their boxes'
                    page.locator('[data-graph-fit]').click()
                    assert page.locator('.ulg-node').evaluate_all('''nodes => nodes.every(node => {
                        const item = node.getBoundingClientRect();
                        const view = node.ownerSVGElement.getBoundingClientRect();
                        return item.left >= view.left - 1 && item.right <= view.right + 1 &&
                            item.top >= view.top - 1 && item.bottom <= view.bottom + 1;
                    })'''), 'Fit must show the entire focused method branch'
                    page.locator('[data-graph-svg]').screenshot(path=str(evidence / f'lower-{method}-perspective.png'))
                page.goto(base + 'proofs/random-scan-reversibility.html')
                page.locator('main mjx-container').first.wait_for()
                lean = page.locator('main details[data-inline-lean]').first
                assert not lean.evaluate('(x)=>x.open')
                lean.locator('summary').click()
                assert lean.evaluate('(x)=>x.open')
                assert 'theorem' in lean.inner_text() or 'Reversible' in lean.inner_text()
                page.screenshot(path=str(evidence / 'adjacent-lean.png'))
                page.goto(base + paper)
                page.locator('#source-outline').evaluate('(x)=>{for(let p=x.parentElement;p;p=p.parentElement)if(p.tagName==="DETAILS")p.open=true;}')
                page.get_by_role('link',name='Locate the planned source route in the graph').click()
                page.locator('[data-graph-detail] h2').filter(has_text='lower bounds').wait_for()
                page.locator('[data-graph-svg]').screenshot(path=str(evidence / 'source-route-graph.png'))
                page.locator('[data-graph-fit]').click()
                page.locator('[data-graph-svg]').screenshot(path=str(evidence / 'source-route-graph-fit.png'))
                # Reviewed building blocks, never main-theorem badges. Both
                # default and progressive readers must work without opening Lean.
                for width, height, label in ((1440,1000,'desktop'),(390,844,'mobile')):
                    page.set_viewport_size({'width':width,'height':height})
                    for item_id, short_name, image_name, declaration in proof_cases:
                        page.goto(base + paper)
                        assert expected_progress in page.locator('#paper-lean-progress').inner_text()
                        page.locator('#paper-lean-progress > details > summary').click()
                        page.locator(f'#{item_id} > summary').click()
                        page.locator(f'#{item_id} a').click()
                        assert page.url.endswith(f'/proofs/source-{item_id}.html')
                        reader = page.locator(f'article[data-authored-declaration="{declaration}"]')
                        # The source equation may intentionally live inside a
                        # closed disclosure; the first-reading claim is visible.
                        reader.locator('.reader-first-pass mjx-container').first.wait_for()
                        assert reader.locator('.proof-reader-step').count() == 3
                        steps = reader.locator('details.reader-proof-disclosure')
                        assert steps.evaluate_all('(xs)=>xs.every(x=>!x.open)')
                        # Private helpers have their own adjacent disclosures;
                        # count the public statement/proof pair by exact identity.
                        folds = reader.locator(f'details[data-inline-lean="{declaration}"]')
                        assert folds.count() == 2
                        assert reader.locator('details[data-inline-lean]').evaluate_all('(xs)=>xs.every(x=>!x.open)')
                        prerequisites = page.locator('details.reader-prerequisite')
                        assert prerequisites.evaluate_all('(xs)=>xs.every(x=>!x.open)')
                        page.screenshot(path=str(evidence / f'{image_name}-overview-{label}.png'), full_page=True)
                        steps.evaluate_all('(xs)=>xs.forEach(x=>x.open=true)')
                        # Hidden source formulae and all three proof formulae.
                        page.locator('.reader-ledger').evaluate_all('(xs)=>xs.forEach(x=>x.open=true)')
                        page.evaluate('async()=>{if(window.MathJax?.startup?.promise) await MathJax.startup.promise;}')
                        assert reader.locator('.proof-reader-step mjx-container').count() >= 3
                        folds.first.locator('summary').click()
                        assert short_name in folds.first.inner_text()
                        folds.first.locator('summary').click()
                        proof_summary = folds.last.locator(':scope > summary')
                        proof_summary.click()
                        assert folds.last.locator('pre').first.is_visible()
                        proof_summary.click()
                        reader.locator('.proof-reader-step details').first.locator('summary').click()
                        assert not page.locator('mjx-merror, [data-mjx-error]').count()
                        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                        assert page.locator('.proof-reader-equation').evaluate_all('''(xs)=>xs.every(x=>{
                            if(!x.clientWidth || x.scrollWidth <= x.clientWidth + 1) return true;
                            const before=x.scrollLeft; x.scrollLeft=x.scrollWidth;
                            const usable=x.scrollLeft>0; x.scrollLeft=before; return usable;
                        })'''), 'Long equations must be scrollable, not permanently clipped'
                        reader.locator('.reader-first-pass').screenshot(path=str(evidence / f'{image_name}-statement-{label}.png'))
                        for step_index in range(3):
                            reader.locator('.proof-reader-step').nth(step_index).screenshot(
                                path=str(evidence / f'{image_name}-step-{step_index + 1}-{label}.png'))
                        if prerequisites.count():
                            prerequisites.locator('details.reader-proof-disclosure').evaluate_all('(xs)=>xs.forEach(x=>x.open=true)')
                            assert prerequisites.locator('mjx-container').count() > 0
                            prerequisites.screenshot(path=str(evidence / f'{image_name}-definition-{label}.png'))
                        page.screenshot(path=str(evidence / f'{image_name}-{label}.png'), full_page=True)
                page.set_viewport_size({'width':1440,'height':1000})
                for _, short_name, image_name, declaration in proof_cases:
                    page.goto(base + 'lean-foundations.html?view=lean&focus=' + quote('decl:' + declaration) + '&q=' + quote(declaration))
                    page.locator('[data-graph-detail] h2').filter(has_text=short_name).wait_for()
                    page.locator('[data-graph-svg]').screenshot(path=str(evidence / f'{image_name}-lean-graph.png'))
                assert not errors, errors
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)
    print(json.dumps({'subjects':4,'viewports':[1440,390],'mathjax_errors':0,
                      'adjacent_lean_exercised':True,'source_outline_exercised':True,
                      'screenshots':str(evidence)}))


if __name__ == '__main__':
    main()
