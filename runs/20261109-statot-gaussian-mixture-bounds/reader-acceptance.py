"""Local, same-origin reader check; the test server is joined on exit."""
from __future__ import annotations

import functools
import hashlib
import http.server
import json
from pathlib import Path
import sys
import threading
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright

TARGET = "AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureWasserstein.wassersteinDistance_gaussianMixtures_bounds"
ITEM = "statot-exercise-1-6-gaussian-mixture-bounds"
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=False)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
thread = threading.Thread(target=server.serve_forever)
thread.start()
origin = f"http://127.0.0.1:{server.server_port}/"
proof_report = []
errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        for width in (1440, 412):
            ctx = browser.new_context(viewport={"width": width, "height": 960})
            ctx.route("**/*", lambda route: route.continue_()
                      if route.request.url.startswith((origin, "data:")) else route.abort())
            page = ctx.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            rel = "libraries/statistical-optimal-transport/chapter-01.html#" + ITEM
            assert page.goto(origin + rel).status == 200
            section = page.locator("#" + ITEM)
            article = section.locator(f'[data-authored-declaration="{TARGET}"]')
            article.locator(".reader-main-equation mjx-container").wait_for()
            page.evaluate("() => MathJax.startup.promise")
            assert article.locator(".proof-roadmap").evaluate("e => getComputedStyle(e).listStyleType") == "none"
            assert article.locator(".proof-roadmap li > p").first.is_hidden()
            assert article.locator(".proof-reader-equation mjx-container").count() >= 6
            assert section.locator("mjx-merror").count() == 0
            for cls, token in [("statement", "wassersteinDistance_gaussianMixtures_bounds"),
                               ("proof", "expectation_sub_le_linearCost_and_le_wassersteinDistance")]:
                fold = article.locator("details.inline-lean-" + cls)
                assert fold.count() == 1 and fold.get_attribute("open") is None
                fold.locator("summary").click()
                assert token in fold.locator("pre").inner_text()
                fold.locator("summary").click()
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
            article.locator(".reader-first-pass").scroll_into_view_if_needed()
            page.screenshot(path=str(out / f"proof-{width}.png"))
            params = urlencode({"view": "lean", "focus": "decl:" + TARGET, "q": TARGET})
            assert page.goto(origin + "lean-foundations.html?" + params).status == 200
            node = page.locator(f'.ulg-node.selected[data-id="decl:{TARGET}"]')
            node.wait_for()
            assert node.locator("circle.status.compiled").count() == 1
            page.locator("[data-graph-canvas]").scroll_into_view_if_needed()
            assert node.locator(".label").is_visible()
            assert node.evaluate("""g => {
                const r = g.querySelector('rect').getBoundingClientRect();
                const hit = document.elementFromPoint((r.left+r.right)/2,(r.top+r.bottom)/2);
                return r.width >= 132 && Boolean(hit && g.contains(hit));
            }"""), "Selected declaration is too small or obscured"
            assert page.locator("[data-graph-detail]").inner_text().find(TARGET) >= 0
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
            page.screenshot(path=str(out / f"graph-{width}.png"))
            proof_report.append({"viewport_width": width, "math_display_minimum": 6,
                                 "folds_opened_and_reclosed": 2, "selected_graph_node": "decl:" + TARGET})
            ctx.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()
    thread.join()
assert not errors, errors
report = {"kind": "local-statot-exercise-reader-browser-check", "runs": proof_report,
          "sha256": {x.name: hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(out.glob("*.png"))}}
print(json.dumps(report))
