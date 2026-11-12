"""Bounded real-browser QA for the paired pilot; always closes its preview server."""
from __future__ import annotations

import argparse
import functools
import http.server
import hashlib
import json
import re
from pathlib import Path
import threading
from urllib.parse import parse_qs, urlsplit

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


def check_visible_equations(page, *, require_full_width: bool = False, scope: str = '#natural-language') -> None:
    for equation in page.locator(scope + ' mjx-container[display="true"]').all():
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
        if require_full_width:
            assert equation.evaluate("""e => {
              const outer=e.getBoundingClientRect(), math=e.querySelector('mjx-math').getBoundingClientRect();
              return math.left >= outer.left-1 && math.right <= outer.right+1;
            }"""), 'Rendered equation requires horizontal scrolling'


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
            # Mathematics must work from the vendored same-origin runtime and
            # fonts, not only when an external CDN happens to be reachable.
            context.route('**/*', lambda route: route.continue_()
                          if route.request.url.startswith((base, 'data:')) else route.abort())
            for path in ('index.html', 'sampling/index.html', 'optimisation/index.html', 'geometry/index.html', 'natural-language/index.html', 'lean/index.html', 'evaluation/index.html', 'training/index.html', 'experts/index.html'):
                response = page.goto(base + HUB + path)
                assert response.status == 200
                assert page.locator('[data-sog-bench]').count() == 1
                assert page.locator('.sidebar-graphs a').count() == 2
                assert page.locator('.sidebar-benches [data-bench-collection]').count() == 3
                if path in ('sampling/index.html', 'optimisation/index.html', 'geometry/index.html'):
                    assert page.locator('.sog-task-row:visible').count() <= 6
                    collection_manifest=page.request.get(base+HUB+path.replace('index.html','manifest.json')).json()
                    raw=page.request.get(base+HUB+path.replace('index.html','questions.jsonl')).body()
                    assert hashlib.sha256(raw).hexdigest()==collection_manifest['files']['questions.jsonl']
                    assert all('lean_reference' not in json.loads(line) and 'steps' not in json.loads(line) for line in raw.splitlines())
                    rows=page.locator('.sog-task-row').count()
                    if rows>6:
                        page.get_by_role('button',name='Show more tasks',exact=True).click()
                        assert page.locator('.sog-task-row:visible').count()==min(12,rows)
                    first=page.locator('.sog-task-row').first
                    identity=re.search(r'sogb-\d+',first.get_attribute('href')).group(0)
                    page.get_by_role('searchbox',name='Find a task').fill(identity)
                    assert page.locator('.sog-task-row:visible').count()==1
                if path in ('training/index.html', 'experts/index.html'):
                    if path.startswith('training/'):
                        page.get_by_text('Native graph runner details',exact=True).click()
                        operator = page.get_by_role('link', name='Download Harbor operator package', exact=True)
                        assert operator.is_visible()
                        assert 'Includes oracle answers and verifier material' in page.locator('article.sog-reader').inner_text()
                        assert page.request.get(base + HUB + 'downloads/harbor-graph-tasks.zip').status == 200
                    if path.startswith('experts/'):
                        page.locator('summary').filter(has_text=re.compile(r'^Optimisation ·')).click()
                        assert page.get_by_role('link', name=re.compile(r'^(Declaration|Owning module) in Lean Graph$')).first.is_visible()
                    page.screenshot(path=str(args.evidence / (path.replace('/index.html','') + '-desktop.png')), full_page=True)
                    page.set_viewport_size({'width': 412, 'height': 915})
                    # Resizing starts the existing 180ms navigation transition.
                    # Inspect the settled mobile layout, not a half-open drawer.
                    page.wait_for_function('document.querySelector("#site-sidebar").getBoundingClientRect().right <= 0')
                    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                    page.screenshot(path=str(args.evidence / (path.replace('/index.html','') + '-mobile.png')), full_page=True)
                    page.set_viewport_size({'width': 1400, 'height': 1000})
            page.goto(base + HUB + 'index.html')
            manifest = page.request.get(base + HUB + 'downloads/manifest.json').json()
            graph_ids = {n['id'] for n in page.request.get(base + 'data/underlying-lean-graph.json').json()['nodes']}
            expert = page.request.get(base + HUB + 'downloads/expert-graph-positions.json')
            assert expert.status == 200
            assert hashlib.sha256(expert.body()).hexdigest() == manifest['files']['expert-graph-positions.json']
            expert_rows = expert.json()
            expert_positions = {p['id']: p for p in expert_rows}
            assert len(expert_rows) == len(expert_positions) == manifest['editorial_accepted_cores']
            for p in expert_rows:
                decl = 'decl:' + p['declaration']
                module = 'module:' + p['source_file'].removesuffix('.lean').replace('/', '.')
                kind, node = ('declaration', decl) if decl in graph_ids else ('owning-module', module)
                assert node in graph_ids and p['node_id'] == node and p['anchor_kind'] == kind, p['id']
                assert parse_qs(urlsplit(p['graph_url']).query)['focus'] == [node], p['id']
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
            page.get_by_text('Numbered textbook exercises and our reference solutions', exact=True).click()
            page.get_by_role('link', name='Textbook exercises & answers', exact=True).click()
            page.wait_for_url('**/textbook-exercises/index.html')
            page.get_by_role('heading', name='Numbered textbook exercises', exact=True).wait_for(state='visible')
            assert page.get_by_role('heading', name='Numbered textbook exercises', exact=True).is_visible()
            component_questions = {}
            for exercise in exercises:
                assert exercise['parts'] and exercise['answer_declarations']
                titles = {c['item_id']: c['title'] for c in exercise.get('source_components', [])}
                for question in exercise['questions']:
                    identity = question['core_id']
                    component = question.get('component_id')
                    link = page.locator(f'a[href="../{identity}.html"]')
                    assert link.is_visible() and link.inner_text() == titles.get(component, identity)
                    if component:
                        component_questions[identity] = (titles[component], {
                            answer['declaration'] for answer in exercise['answer_declarations']
                            if answer['component_id'] == component})
            page.screenshot(path=str(args.evidence / 'textbook-exercise-directory.png'), full_page=True)
            page.goto(base + HUB + 'index.html')
            editorial = page.request.get(base + HUB + 'downloads/editorial-review.json').json()
            graph_editorial = page.request.get(base + HUB + 'downloads/graph-editorial-review.json').json()['items']
            graph_records=[json.loads(line) for line in page.request.get(base+HUB+'downloads/graph-questions.jsonl').text().splitlines()]
            for graph_prompt in graph_records:
                assert not {'answer', 'binding_sha256'} & graph_prompt.keys()
                visible = {k: v for k, v in graph_prompt.items() if k != 'prompt_sha256'}
                assert graph_prompt['prompt_sha256'] == hashlib.sha256(
                    json.dumps(visible, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            compiled_graphs={r['id']+'.html':r for r in graph_records if r['context']['kind']=='compiled-proof-body-constant-occurrences'}
            assert len(graph_records)==manifest['graph_tasks']
            page.get_by_text('Coverage, downloads and readiness',exact=True).click()
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
                if identity in component_questions:
                    title, declarations = component_questions[identity]
                    scope = page.locator('.sog-exercise-scope > details')
                    scope.locator('summary').first.click()
                    components = scope.locator('details')
                    assert components.first.locator('summary').inner_text() == title
                    components.first.locator('summary').click()
                    assert components.first.get_by_text('Source component for this question', exact=True).is_visible()
                    actual = set()
                    for link in components.first.locator('a[href*="underlying-lean-graph/index.html?focus="]').all():
                        assert link.is_visible()
                        actual.update(parse_qs(urlsplit(link.get_attribute('href')).query)['focus'])
                    assert actual == {'decl:' + name for name in declarations}
                    components.first.locator('summary').click()
                    scope.locator('summary').first.click()
                prompt=page.locator('#natural-language [data-sog-copy-prompt]')
                expected_prompt=page.request.get(base+HUB+prompt.get_attribute('data-sog-copy-prompt')).text()
                prompt.click()
                page.wait_for_function('Array.from(document.querySelectorAll("[data-sog-copy-status]")).some(n=>n.textContent==="Copied prompt-only task")')
                copied_prompt=page.evaluate('() => navigator.clipboard.readText()')
                assert copied_prompt.replace('\r\n','\n')==expected_prompt.replace('\r\n','\n')
                assert json.loads(copied_prompt)==json.loads(expected_prompt)
                page.locator('summary', has_text='Reference mathematical proof').click()
                page.wait_for_timeout(300)
                assert page.locator('mjx-container').count() > 0
                assert page.locator('mjx-merror, [data-mjx-error]').count() == 0, (
                    identity, page.locator('mjx-merror, [data-mjx-error]').all_text_contents())
                check_visible_equations(page)
                page.locator('summary', has_text='How the Lean proof follows these steps').click()
                panel = page.locator('#natural-language [data-lean-code-panel]')
                assert panel.locator('code.language-lean').is_visible()
                assert panel.locator('code span').count() > 0  # Existing Lean highlighter.
                panel.get_by_role('button', name='Copy Lean reference').click()
                page.wait_for_function('Array.from(document.querySelectorAll("[data-lean-copy-status]")).some(n=>n.textContent==="Copied")')
                copied = page.evaluate('() => navigator.clipboard.readText()')
                assert 'example' in copied and 'sorry' not in copied
                if identity == 'sogb-038':
                    assert 'private theorem finiteMixture_apply' in copied
                    task = page.request.get(base + HUB + 'downloads/lean/sogb-038-task.lean.txt')
                    reference = page.request.get(base + HUB + 'downloads/lean/sogb-038-reference.lean')
                    assert task.status == reference.status == 200
                    assert 'finiteMixture_apply' not in task.text()
                    assert copied.replace('\r\n', '\n').strip() == reference.text().replace('\r\n', '\n').strip()
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
                # Click/focus and layout anchoring can complete after the first
                # scroll request on Chromium. Normalize at the observed frame,
                # instead of waiting for a one-shot request to remain effective.
                page.wait_for_function('''() => {
                    document.activeElement?.blur();
                    window.scrollTo({top:0, left:0, behavior:"instant"});
                    return window.scrollY === 0;
                }''')
                page.screenshot(path=str(args.evidence / (identity + '-proof-mobile.png')), full_page=True)
                page.locator('summary', has_text='How the Lean proof follows these steps').click()
                math_component_shot(page, args.evidence / (identity + '-math-mobile.png'))
                page.set_viewport_size({'width': 1400, 'height': 1000})
            reference_records=[json.loads(line) for line in page.request.get(base+HUB+'downloads/reference.jsonl').text().splitlines()]
            # Every core, not just the paired/support examples: inline typography
            # can break assumptions even when one display formula renders well.
            for core in reference_records:
                page.goto(base + HUB + core['id'] + '.html')
                page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                page.evaluate('() => MathJax.startup.promise')
                page.locator('summary', has_text='Reference mathematical proof').click()
                assert page.locator('[data-lean-graph-position]').count() == 1
                assert page.locator('[data-lean-graph-position]').is_visible()
                if core['id'] in expert_positions:
                    assert page.locator('[data-lean-graph-position]').get_attribute('data-lean-graph-position') == expert_positions[core['id']]['node_id']
                assert page.locator('mjx-merror,[data-mjx-error]').count() == 0, core['id']
                for span in page.locator('[data-math-original]').all():
                    assert span.locator('mjx-container').count() == 1, (core['id'], span.get_attribute('data-math-original'))
                check_visible_equations(page)
                if core['id'] in {'sogb-032', 'sogb-033', 'sogb-034', 'sogb-035', 'sogb-037', 'sogb-038', 'sogb-041', 'sogb-042', 'sogb-043', 'sogb-044', 'sogb-045', 'sogb-046', 'sogb-047', 'sogb-048'} or core['id'] in component_questions:
                    page.set_viewport_size({'width': 390, 'height': 915})
                    page.reload()
                    page.wait_for_function('Boolean(window.MathJax?.startup?.promise)')
                    page.evaluate('() => MathJax.startup.promise')
                    page.locator('summary', has_text='Reference mathematical proof').click()
                    assert page.locator('mjx-merror,[data-mjx-error]').count() == 0, core['id']
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), core['id']
                    check_visible_equations(page,
                        require_full_width=core['id'] in {'sogb-037', 'sogb-038', 'sogb-041', 'sogb-042', 'sogb-043', 'sogb-044', 'sogb-045', 'sogb-046', 'sogb-047', 'sogb-048'},
                        scope='.sog-reader' if core['id'] in {'sogb-043', 'sogb-044', 'sogb-045', 'sogb-046', 'sogb-047', 'sogb-048'} else '#natural-language')
                    page.set_viewport_size({'width': 1400, 'height': 1000})
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
                        assert 'not an equivalent Lean challenge' in page.locator('article.sog-reader').inner_text()
                        page.locator('summary', has_text='Original exercise, all requested parts and exact Lean scope').click()
                    page.locator('summary',has_text='Reference mathematical proof').click()
                    check_visible_equations(page, require_full_width=identity == 'sogb-049')
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
            for tail in ('curriculum/index.html', 'graph-json/index.html', 'evaluation/index.html', 'evaluation/guide.html', 'levels/L5.html', 'domains/statistical-optimal-transport.html', 'domains/optimisation.html', 'sogb-g003.html', 'sogb-007.html', 'sogb-008.html', 'sogb-012.html', *compiled_graphs):
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
                    assert graph_editorial['sogb-g003']['editorial'] in page.locator('article.sog-reader').inner_text()
                if tail == 'evaluation/guide.html':
                    assert 'not automatically verified mathematics' in page.locator('article.sog-reader').inner_text()
                    assert page.locator('details[open]').count()==0
                    page.locator('summary', has_text='Commands and input formats').click()
                    assert page.locator('pre code', has_text='sog_bench_prose.py plan --run-metadata').is_visible()
                    protocol = page.request.get(base + HUB + 'downloads/EVALUATION.md')
                    assert protocol.status == 200
                    assert hashlib.sha256(protocol.body()).hexdigest() == manifest['files']['EVALUATION.md']
                    assert all(flag in protocol.text() for flag in ('--plan-sha256', 'selection_timing_verified', 'score-panel'))
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
                    lookup=page.locator('details', has=page.locator('summary', has_text='Try this as a bounded search task'))
                    identity = compiled_graphs[tail]['id']
                    if graph_editorial[identity]['editorial'] in ('accepted', 'accepted-after-repair'):
                        assert lookup.count() == 1 and lookup.get_attribute('open') is None
                        lookup.locator('summary').click()
                        assert lookup.locator('code', has_text=f'run --task-id {identity} --max-lookups 8').is_visible()
                        assert lookup.get_by_role('link', name='JSONL tool and scoring protocol').is_visible()
                        lookup.locator('summary').click()
                    else:
                        assert lookup.count() == 0
                    if identity == 'sogb-g010':
                        assert page.locator('.sog-graph svg').evaluate('svg => svg.width.baseVal.value < 440')
                        positions = page.locator('details', has=page.locator('summary', has_text='Locate these declarations in the Lean Graph'))
                        positions.locator('summary').click()
                        assert {parse_qs(urlsplit(link.get_attribute('href')).query)['focus'][0]
                                for link in positions.locator('a').all()} == {'decl:' + name for name in graph['nodes']}
                        positions.locator('summary').click()
                        reference = page.locator('details', has=page.locator('summary', has_text='Reference structural answer'))
                        reference.locator('summary').click()
                        assert reference.get_by_text('Selected path: Horizon-dependent value-gap witness → Fixed-step distance witness → Balanced step and scalar minimax bound → One-step endpoint upper bound.', exact=True).is_visible()
                        reference.locator('summary').click()
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
    report['offline_same_origin_math_assets'] = True
    report['all_mathematical_cores_checked'] = len(reference_records)
    (args.evidence / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
