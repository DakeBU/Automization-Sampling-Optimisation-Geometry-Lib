#!/usr/bin/env python3
"""ROOT-only graph legibility supplement over the unchanged passing C2 fixture."""
import argparse
import datetime as dt
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import plistlib
import subprocess
import sys
import threading
import time
import traceback
from urllib.parse import quote

OWN = Path(__file__).resolve().parent
P = 'AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential.bernstein_exponential_quadratic_bound'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('variant', choices=['candidate'])
    args = parser.parse_args()
    contract_path = OWN / 'root-primary-graph-zoom-contract.json'
    contract = json.loads(contract_path.read_text())
    if sha(__file__) != contract['wrapper_sha256']:
        raise ValueError('Frozen graph-only wrapper changed')
    for entry in contract['owned_inputs']:
        if sha(OWN / entry['path']) != entry['sha256']:
            raise ValueError('Frozen graph-only input changed: ' + entry['path'])
    manifest = json.loads((OWN / 'reader-render-manifest.C2.json').read_text())
    selected = manifest['variants']['candidate']
    fixture = OWN / 'reader-fixtures-c2/candidate'
    for entry in selected['files']:
        if sha(fixture / entry['path']) != entry['sha256']:
            raise ValueError('Passing C2 fixture changed: ' + entry['path'])
    chrome = Path(contract['installed_chrome']['executable_path'])
    if sha(chrome) != contract['installed_chrome']['binary_sha256']:
        raise ValueError('Installed Chrome binary changed')
    info_path = Path(contract['installed_chrome']['Info_plist_path'])
    info = plistlib.loads(info_path.read_bytes())
    chrome_evidence = {'executable_path': str(chrome), 'binary_sha256': sha(chrome),
                       'Info_plist_path': str(info_path), 'Info_plist_sha256': sha(info_path),
                       'app_short_version': info.get('CFBundleShortVersionString'),
                       'app_build_version': info.get('CFBundleVersion'), 'runtime_browser_version': None}
    output = OWN / 'root-primary-graph-zoom-output/candidate'
    output.mkdir(parents=True, exist_ok=False)
    checks, screenshots, errors, blocked, actions = [], [], [], [], []

    def check(name, ok, detail=None):
        checks.append({'name': name, 'pass': bool(ok), 'detail': detail})

    def png(page, label):
        path = output / (label + '.png')
        page.screenshot(path=str(path))
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
                context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=1)

                def route(r):
                    if r.request.url.startswith(origin + '/') or r.request.url.startswith(('data:', 'blob:')):
                        r.continue_()
                    else:
                        blocked.append(r.request.url)
                        r.abort()
                context.route('**/*', route)
                page = context.new_page()
                page.on('pageerror', lambda error: errors.append(str(error)))
                try:
                    page.goto(origin + '/lean-foundations.html?view=lean&focus=' + quote('decl:' + P, safe=''),
                              wait_until='networkidle', timeout=30000)
                    page.wait_for_selector('.ulg-node.selected')
                    page.evaluate('async () => { if(window.MathJax?.startup?.promise) await MathJax.startup.promise; }')
                    canvas = page.locator('[data-graph-canvas]')
                    canvas.evaluate("el => el.scrollIntoView({behavior:'instant',block:'center',inline:'nearest'})")

                    def settle():
                        page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')

                    def geometry(locator):
                        return locator.evaluate('''el => {
                            const svg=el.closest('svg')||document.querySelector('[data-graph-svg]'),clip=svg.getBoundingClientRect();
                            let r=el.getBoundingClientRect(),cx=(r.left+r.right)/2,cy=(r.top+r.bottom)/2;
                            if(el.tagName.toLowerCase()==='path'){
                                const p=el.getPointAtLength(el.getTotalLength()/2),m=el.getScreenCTM();
                                cx=m.a*p.x+m.c*p.y+m.e;cy=m.b*p.x+m.d*p.y+m.f;
                            }
                            let header=0;const hs=[...document.querySelectorAll('header,.mobile-bar,.verification-strip')];
                            for(let pass=0;pass<hs.length+1;pass++)for(const h of hs){
                                const s=getComputedStyle(h),q=h.getBoundingClientRect();
                                if(['fixed','sticky'].includes(s.position)&&s.display!=='none'&&s.visibility!=='hidden'
                                    &&q.width>0&&q.height>0&&q.right>0&&q.left<innerWidth&&q.bottom>0&&q.top<=header+1)header=Math.max(header,q.bottom);
                            }
                            const left=Math.max(clip.left,0)+8,right=Math.min(clip.right,innerWidth)-8;
                            const top=Math.max(clip.top,header)+8,bottom=Math.min(clip.bottom,innerHeight)-8;
                            const text=el.querySelector('.label'),m=text?.getScreenCTM();
                            const fontPx=text?parseFloat(getComputedStyle(text).fontSize)*Math.hypot(m.a,m.b):null;
                            const style=getComputedStyle(el);
                            return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height,
                                centerX:cx,centerY:cy,clipLeft:left,clipRight:right,clipTop:top,clipBottom:bottom,
                                headerBottom:header,fontPx,viewportWidth:innerWidth,viewportHeight:innerHeight,
                                fullNodeVisible:r.width>0&&r.height>0&&r.left>=left&&r.right<=right&&r.top>=top&&r.bottom<=bottom,
                                anchorVisible:cx>=left&&cx<=right&&cy>=top&&cy<=bottom,
                                strokeDasharray:style.strokeDasharray,strokeWidth:style.strokeWidth};
                        }''')

                    selected_node = page.locator('.ulg-node.selected')
                    settle()
                    initial = geometry(selected_node)
                    # Real wheel events are the widget's own zoom UI. No state,
                    # SVG transform, stylesheet, node positions or data is edited.
                    target_font = 13.5
                    for attempt in range(3):
                        g = geometry(selected_node)
                        if g['fontPx'] >= 12.5:
                            break
                        wheel = -1000 * math.log(target_font / max(g['fontPx'], .1))
                        x = min(max(g['centerX'], g['clipLeft'] + 2), g['clipRight'] - 2)
                        y = min(max(g['centerY'], g['clipTop'] + 2), g['clipBottom'] - 2)
                        page.mouse.move(x, y)
                        page.mouse.wheel(0, wheel)
                        actions.append({'viewport': label, 'action': 'real-wheel-zoom', 'delta_y': wheel, 'x': x, 'y': y})
                        settle()

                    def pan_to(locator):
                        for _ in range(12):
                            g = geometry(locator)
                            desired_x = (g['clipLeft'] + g['clipRight']) / 2
                            desired_y = (g['clipTop'] + g['clipBottom']) / 2
                            dx, dy = desired_x - g['centerX'], desired_y - g['centerY']
                            if abs(dx) < 2 and abs(dy) < 2:
                                return g
                            dx = max(-.36 * (g['clipRight'] - g['clipLeft']), min(.36 * (g['clipRight'] - g['clipLeft']), dx))
                            dy = max(-.36 * (g['clipBottom'] - g['clipTop']), min(.36 * (g['clipBottom'] - g['clipTop']), dy))
                            start = page.evaluate('''({g,dx,dy}) => {
                                for(const fx of [.12,.88,.5,.25,.75])for(const fy of [.88,.12,.5,.25,.75]){
                                    const x=g.clipLeft+fx*(g.clipRight-g.clipLeft),y=g.clipTop+fy*(g.clipBottom-g.clipTop);
                                    const e=document.elementFromPoint(x,y);
                                    if(x+dx>=g.clipLeft&&x+dx<=g.clipRight&&y+dy>=g.clipTop&&y+dy<=g.clipBottom
                                        &&e&&e.closest('[data-graph-svg]')&&!e.closest('.ulg-node'))return {x,y};
                                }
                                return null;
                            }''', {'g': g, 'dx': dx, 'dy': dy})
                            if start is None:
                                raise RuntimeError('No actual blank SVG drag origin available')
                            page.mouse.move(start['x'], start['y'])
                            page.mouse.down()
                            page.mouse.move(start['x'] + dx, start['y'] + dy, steps=12)
                            page.mouse.up()
                            actions.append({'viewport': label, 'action': 'real-pointer-pan', 'start': start, 'dx': dx, 'dy': dy})
                            settle()
                        return geometry(locator)

                    readable = pan_to(selected_node)
                    check(label + '-real-wheel-increased-label-size', readable['fontPx'] > initial['fontPx'], {'before': initial, 'after': readable})
                    check(label + '-selected-public-node-readable-and-fully-visible',
                          readable['fullNodeVisible'] and readable['fontPx'] >= 12.5, readable)
                    check(label + '-exact-public-focus-preserved', selected_node.get_attribute('data-id') == 'decl:' + P)
                    png(page, label + '-readable-selected-public-node')
                    graph = context.request.get(origin + '/data/underlying-lean-graph.json').json()
                    neighbors = sorted({e['source'] if e['target'] == 'decl:' + P else e['target']
                                        for e in graph['edges'] if 'decl:' + P in [e['source'], e['target']]})
                    check(label + '-exact-one-hop-neighbors-present', len(neighbors) == 2, neighbors)
                    for index, node_id in enumerate(neighbors):
                        node = page.locator('g.ulg-node[data-id="' + node_id + '"]')
                        g = pan_to(node)
                        check(label + '-adjacent-node-' + str(index) + '-readable-and-fully-visible',
                              g['fullNodeVisible'] and g['fontPx'] >= 12.5, {'id': node_id, 'geometry': g})
                        png(page, label + '-readable-adjacent-node-' + str(index))
                    for evidence in ['formal', 'overlay']:
                        edge = page.locator('path.ulg-edge.related[data-evidence="' + evidence + '"]').first
                        g = pan_to(edge)
                        check(label + '-' + evidence + '-edge-actual-visible-style', g['anchorVisible']
                              and (g['strokeDasharray'] == 'none' if evidence == 'formal' else g['strokeDasharray'] != 'none'), g)
                        png(page, label + '-readable-' + evidence + '-edge')
                    detail = page.locator('[data-graph-detail]')
                    link = detail.locator('.ulg-links a').first
                    check(label + '-exact-reader-link', link.get_attribute('href') == selected['lesson_path'])
                    link.evaluate("el => el.scrollIntoView({behavior:'instant',block:'center',inline:'nearest'})")
                    settle()
                    link_bounds = link.evaluate('''el=>{const r=el.getBoundingClientRect();
                        let header=0;const hs=[...document.querySelectorAll('header,.mobile-bar,.verification-strip')];
                        for(let pass=0;pass<hs.length+1;pass++)for(const h of hs){const s=getComputedStyle(h),q=h.getBoundingClientRect();
                            if(['fixed','sticky'].includes(s.position)&&s.display!=='none'&&s.visibility!=='hidden'
                                &&q.width>0&&q.height>0&&q.right>0&&q.left<innerWidth&&q.bottom>0&&q.top<=header+1)header=Math.max(header,q.bottom);}
                        return {top:r.top,bottom:r.bottom,left:r.left,right:r.right,width:r.width,height:r.height,headerBottom:header,
                            visible:r.width>0&&r.height>0&&r.top>=header+4&&r.bottom<=innerHeight-4&&r.left>=0&&r.right<=innerWidth};}''')
                    check(label + '-reader-link-actual-visible', link_bounds['visible'], link_bounds)
                    check(label + '-detail-immediate-edge-buttons', detail.locator('.ulg-neighbors [data-jump]').count() == 2)
                    png(page, label + '-readable-reader-and-edge-details')
                except Exception:
                    check(label + '-graph-only-stage-completed', False, traceback.format_exc())
                    png(page, label + '-graph-only-error')
                context.close()
            browser.close()
    except Exception:
        check('graph-only-browser-completed', False, traceback.format_exc())
    finally:
        server.shutdown()
        server.server_close()
        worker.join()
    check('no-page-javascript-errors', not errors, errors)
    check('no-external-browser-requests', not blocked, blocked)
    for entry in selected['files']:
        check('fixture-unchanged:' + entry['path'], sha(fixture / entry['path']) == entry['sha256'])
    result = {'schema': 'root-primary-graph-zoom-result-v1', 'variant': 'candidate',
              'reader_commit': contract['reader_commit'], 'mathematical_candidate': contract['mathematical_candidate'],
              'checks': checks, 'screenshots': screenshots, 'real_UI_actions': actions,
              'actual_chrome': chrome_evidence, 'browser_started': browser_started,
              'contract_sha256': sha(contract_path), 'wrapper_sha256': sha(__file__),
              'started': started, 'ended': dt.datetime.now(dt.timezone.utc).isoformat(),
              'scope': 'GRAPH_ONLY; no full P/T reader rerun; no data/CSS/layout mutation',
              'status': 'ENV_BLOCKED' if not browser_started else 'PASS' if all(x['pass'] for x in checks) else 'FAIL',
              'human_visual_review': 'PENDING_ROOT_AND_INDEPENDENT_REVIEW_OF_ACTUAL_GRAPH_PNGS'}
    path = output / 'actual-checks.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'actual_checks': str(path), 'sha256': sha(path)}))
    return 0 if result['status'] == 'PASS' else 2 if result['status'] == 'ENV_BLOCKED' else 1


def captured_root_process():
    # OS file-descriptor redirection captures real Python/native/inherited
    # stdout and stderr while ROOT runs this process. No flags or reconstructed
    # summaries substitute for the raw byte streams.
    variant = sys.argv[1] if len(sys.argv) == 2 and sys.argv[1] in ['candidate'] else 'invalid-argv'
    process_dir = OWN / 'root-primary-graph-zoom-process' / variant
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
    contract_path = OWN / 'root-primary-graph-zoom-contract.json'
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
    actual_checks_path = OWN / 'root-primary-graph-zoom-output' / variant / 'actual-checks.json'
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
