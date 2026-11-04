"""Bounded real-browser QA for the paired pilot; always closes its preview server."""
from __future__ import annotations

import argparse
import functools
import http.server
import hashlib
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
        # Other proof/source sections intentionally remain folded. Check their
        # equations when opened, not the zero-size boxes of closed details.
        if not equation.is_visible():
            continue
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
    parser.add_argument('--core', action='append', help='Focus proof/copy checks on these IDs; overview/graph checks still run')
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
            for path in ('index.html', 'natural-language/index.html', 'lean/index.html', 'evaluation/index.html'):
                response = page.goto(base + HUB + path)
                assert response.status == 200
                assert page.locator('[data-sog-bench]').count() == 1
            page.goto(base + HUB + 'index.html')
            manifest = page.request.get(base + HUB + 'downloads/manifest.json').json()
            page.get_by_text('Numbered textbook exercises and our reference solutions', exact=True).click()
            intake_link = page.get_by_role('link', name='Verified source intake and admission checklist')
            assert intake_link.is_visible()
            intake = page.request.get(base + HUB + 'downloads/TEXTBOOK_EXERCISES.md')
            assert intake.status == 200
            assert hashlib.sha256(intake.body()).hexdigest() == manifest['files']['TEXTBOOK_EXERCISES.md']
            assert 'Intake itself is not admission' in intake.text()
            exercise_link = page.get_by_role('link', name='Existing Chewi Optimization Exercise 3.2 source/solution window')
            assert exercise_link.is_visible()
            source_page = page.request.get(base + 'libraries/optimisation/chapter-03.html')
            assert source_page.status == 200
            assert 'id="chewi-opt-v1-exercise-3-2"' in source_page.text()
            page.screenshot(path=str(args.evidence / 'textbook-exercise-intake.png'), full_page=True)
            page.get_by_text('Numbered textbook exercises and our reference solutions', exact=True).click()
            exercise_response = page.request.get(base + HUB + 'downloads/textbook-exercise-map.json')
            assert exercise_response.status == 200
            assert hashlib.sha256(exercise_response.body()).hexdigest() == manifest['files']['textbook-exercise-map.json']
            exercises = exercise_response.json()
            assert len(exercises) == manifest['numbered_textbook_exercises']
            page.get_by_role('link', name='Textbook exercises & answers', exact=True).click()
            assert page.get_by_role('heading', name='Numbered textbook exercises', exact=True).is_visible()
            for exercise in exercises:
                assert exercise['parts'] and exercise['answer_declarations']
                for question in exercise['questions']:
                    assert page.get_by_role('link', name=question['core_id'], exact=True).is_visible()
            page.screenshot(path=str(args.evidence / 'textbook-exercise-directory.png'), full_page=True)
            page.goto(base + HUB + 'index.html')
            editorial = page.request.get(base + HUB + 'downloads/editorial-review.json').json()
            graph_records=[json.loads(line) for line in page.request.get(base+HUB+'downloads/graph-questions.jsonl').text().splitlines()]
            compiled_graphs={r['id']+'.html':r for r in graph_records if r['context']['kind']=='compiled-proof-body-constant-occurrences'}
            assert len(graph_records)==manifest['graph_tasks']
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
            for identity in sorted({r['id'] for r in records if r['track'] == 'lean' and (not args.core or r['id'] in args.core)}):
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
            reference_records=[json.loads(line) for line in page.request.get(base+HUB+'downloads/reference.jsonl').text().splitlines()]
            for core in (c for c in reference_records if c.get('support_source_view') and (not args.core or c['id'] in args.core)):
                identity=core['id']
                for width,height,suffix in ((1400,1000,'desktop'),(412,915,'mobile')):
                    page.set_viewport_size({'width':width,'height':height})
                    page.goto(base+HUB+identity+'.html')
                    page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                    page.evaluate('() => MathJax.startup.promise')
                    assert page.locator('details[open]').count()==0
                    if core.get('textbook_exercise'):
                        page.locator('summary', has_text='Original exercise, all requested parts and exact Lean scope').click()
                        check_visible_equations(page)
                        exercise = core['textbook_exercise']
                        for answer in exercise['answer_declarations']:
                            graph_link = page.get_by_role('link', name=answer['declaration'], exact=True)
                            assert graph_link.is_visible()
                            assert 'underlying-lean-graph/index.html?focus=' in graph_link.get_attribute('href')
                        assert 'not a new proof' in page.locator('article.sog-reader').inner_text()
                        page.locator('summary', has_text='Original exercise, all requested parts and exact Lean scope').click()
                    page.locator('summary',has_text='Reference mathematical proof').click()
                    check_visible_equations(page)
                    assert page.locator('mjx-merror, [data-mjx-error]').count()==0
                    math_component_shot(page,args.evidence/(identity+'-math-'+suffix+'.png'))
                    support_title = ('Owned Lean answer and proof-step correspondence'
                                     if core.get('textbook_exercise') else 'Formal support and missing Lean alignment')
                    page.locator('#natural-language summary',has_text=support_title).click()
                    page.locator('#natural-language summary',has_text='Supporting library Lean (not an aligned QA task)').click()
                    panel=page.locator('#natural-language [data-lean-code-panel]')
                    assert panel.locator('code.language-lean').is_visible()
                    assert panel.locator('code span').count()>0
                    panel.get_by_role('button',name='Copy supporting module').click()
                    page.wait_for_function('Array.from(document.querySelectorAll("[data-lean-copy-status]")).some(n=>n.textContent==="Copied")')
                    copied=page.evaluate('() => navigator.clipboard.readText()')
                    expected=core['support_lean_source']
                    # Windows' clipboard normalizes line separators to CRLF.
                    # Ignore only that platform conversion, not source tokens.
                    assert copied.replace('\r\n','\n')==expected
                    with page.expect_download() as supporting:
                        page.locator('#natural-language').get_by_role('link',name='Download exact supporting module').click()
                    assert Path(supporting.value.path()).read_text(encoding='utf-8')==core['support_lean_source']
                    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                    page.screenshot(path=str(args.evidence/(identity+'-source-'+suffix+'.png')),full_page=True)
                page.set_viewport_size({'width':1400,'height':1000})
            for tail in ('curriculum/index.html', 'graph-json/index.html', 'evaluation/index.html', 'levels/L5.html', 'domains/statistical-optimal-transport.html', 'domains/optimisation.html', 'sogb-g003.html', 'sogb-007.html', 'sogb-008.html', 'sogb-012.html', *compiled_graphs):
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
                    page.locator('summary', has_text='Independent structural review and limits').click()
                    evidence=page.request.get(base + HUB + 'downloads/graph-editorial-review.json').json()
                    assert evidence['items']['sogb-g003']['editorial'] in page.locator('article.sog-reader').inner_text()
                if tail == 'evaluation/index.html':
                    assert 'not automatically verified mathematics' in page.locator('article.sog-reader').inner_text()
                    assert page.locator('details[open]').count()==0
                    page.locator('summary', has_text='Commands and input formats').click()
                    with page.expect_download() as metadata_download:
                        page.get_by_role('link',name='Run-metadata template',exact=True).click()
                    template=json.loads(Path(metadata_download.value.path()).read_text(encoding='utf-8'))
                    assert template['track']=='natural-language' and template['attempt_policy']=='first-attempt'
                if tail=='graph-json/index.html':
                    assert page.get_by_role('heading',name='Source imports',exact=True).count()==1
                    assert page.get_by_role('heading',name='Compiled proof bodies',exact=True).count()==1
                    with page.expect_download() as graph_download:
                        page.get_by_role('link',name='Reviewed graph prompts',exact=True).click()
                    admitted=[json.loads(line) for line in Path(graph_download.value.path()).read_text(encoding='utf-8').splitlines()]
                    assert len(admitted)==manifest['editorial_accepted_graph_tasks']
                    assert all('answer' not in r for r in admitted)
                if tail in compiled_graphs:
                    graph=compiled_graphs[tail]['context']
                    if compiled_graphs[tail].get('required_statement_constants'):
                        profiles=page.locator('[data-statement-profiles]')
                        assert profiles.is_visible()
                        assert profiles.locator('tbody tr').count()==len(graph['nodes'])
                        assert 'not a binder-role analysis' in profiles.inner_text()
                        for constant in compiled_graphs[tail]['required_statement_constants']:
                            assert constant in profiles.inner_text()
                    assert page.locator('.sog-graph svg rect').count()==len(graph['nodes'])
                    assert page.locator('.sog-graph svg > path').count()==len(graph['edges'])
                    assert sorted(page.locator('.sog-graph svg text').all_text_contents())==sorted(graph['node_labels'].values())
                    assert page.locator('.sog-graph svg').evaluate("""svg => {
                      const rects=[...svg.querySelectorAll('rect')].map(e=>e.getBBox());
                      const texts=[...svg.querySelectorAll('text')];
                      return rects.every((r,i)=>texts[i].getBBox().width<=r.width-12 &&
                        rects.every((s,j)=>i===j || r.x+r.width<=s.x || s.x+s.width<=r.x || r.y+r.height<=s.y || s.y+s.height<=r.y));
                    }"""), 'Compiled graph labels or nodes overlap'
                    assert 'Solid arrows' in page.locator('.sog-graph').inner_text()
                    page.locator('.sog-graph').screenshot(path=str(args.evidence/(tail+'-graph-desktop.png')))
                    page.locator('summary',has_text='Evidence kind and source scope').click()
                    assert 'not a fresh Lean run in this browser' in page.locator('article.sog-reader').inner_text()
                    artifact=page.get_by_role('link',name='Recorded compiler slice and provenance')
                    raw=page.request.get(base+HUB+artifact.get_attribute('href')).body()
                    assert hashlib.sha256(raw).hexdigest()==graph['snapshot_sha256']
                    source_link=page.get_by_role('link',name='Read the source mathematical proof and optional Lean')
                    assert source_link.get_attribute('href')==compiled_graphs[tail]['core_id']+'.html'
                page.set_viewport_size({'width': 412, 'height': 915})
                page.wait_for_timeout(400)  # Let the existing sidebar resize transition finish.
                page.evaluate('() => { document.activeElement?.blur(); window.scrollTo({top:0, behavior:"instant"}); }')
                page.wait_for_function('window.scrollY === 0')
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                if tail in compiled_graphs and compiled_graphs[tail].get('required_statement_constants'):
                    assert page.locator('[data-statement-profiles]').is_visible()
                page.screenshot(path=str(args.evidence / (tail.replace('/', '-') + '-mobile.png')), full_page=True)
                page.set_viewport_size({'width': 1400, 'height': 1000})
            assert not errors, errors
            context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    report = {'mathematical_views': len(records), 'graph_tasks': manifest['graph_tasks'],
              'numbered_textbook_exercises': len(exercises), 'exercise_directory_and_actual_part_links': True,
              'textbook_intake_not_qa_admission': True, 'math_rendered': True, 'lean_highlighting': True,
              'folds_and_copy': True, 'prompt_only_download': True, 'reviewed_subset_download': True,
              'editorial_vs_formal_scope_visible': True, 'mobile_overflow': False,
              'equations_unobscured_when_centered': True, 'component_images_omit_navigation_only': True,
              'human_scoring_guide_and_template': True, 'structural_review_scope_visible': True,
              'compiled_graphs':len(compiled_graphs), 'graph_evidence_kinds_separate':True,
              'compiled_graph_labels_fit':True,'reviewed_graph_download':True,
              'runtime_errors': errors}
    (args.evidence / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
