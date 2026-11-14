from pathlib import Path
import sys, json, hashlib, html, re
from html.parser import HTMLParser

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import astis_site as base
import inline_lean, declaration_lessons, publication_reader

paths = [ROOT / x for x in [
    'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumNormalizer.lean',
    'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAdmissibility.lean',
    'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumDeterminant.lean',
    'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianPrecisionDensity.lean',
    'Tests/GaussianComplexityFixedSpectrumNormalizer.lean']]
# Restrict the generic scanner to the current target, direct parents and Test.
base.project_lean_paths = lambda: paths
modules, declarations = base.scan_project_sources()
known = {d.full_name: d for d in declarations}
base._SOURCE_BY_NAME = known
base._ACTIVE_GIT = base.GitContext(
    '813268bc2683a82269364caffbc0c7490a884204', 'independent-static-review',
    '', '', False, False, set())
item = json.loads((ROOT / 'website/content/publications/huanjian-fixed-spectrum-normalizer.json').read_text())['items'][0]
unit = json.loads((ROOT / 'website/content/declaration_lessons/huanjian-fixed-spectrum-normalizer.json').read_text())['units'][0]
audit = json.loads((ROOT / 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-normalizer.json').read_text())
data = {'declarations': known, 'lessons': {unit['declaration']: unit},
        'audits': {audit['id']: audit}, 'cells': {}}
publication_reader.publication.inputs = lambda: data
page = 'review-reader.html'
body = publication_reader.source_card(item, page)
consumer = 'actual_gaussian_density_consumer'
body += '<section><h2>Focused private Test: exact current verification context</h2><p>The same Gaussian uses its actual unweighted integral in the denominator. This appendix is a reviewer-owned source inspection, not a new publication binding.</p>'
body += r'<div class="proof-reader-equation">\[N(0,A^{-1})(dx)=w_A(x)/(\int w_A\,dx)\,dx.\]</div>'
body += inline_lean.disclosure(consumer, role='statement', explanation='Exact focused Test signature; no source assumptions added.', page=page)
body += inline_lean.disclosure(consumer, role='proof', explanation='Exact current Test proof, including consequential new-producer invocation.', page=page) + '</section>'
head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Independent static normalizer reader</title><style>body{max-width:1050px;margin:2rem auto;padding:0 1rem;font:17px/1.6 system-ui}details{border:1px solid #ccd4da;padding:.7rem;margin:.8rem 0}summary{cursor:pointer;font-weight:600}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd4da;padding:.4rem}code{font-size:.9em}.proof-reader-equation{overflow:auto;padding:.7rem;background:#f5f7fa}.status-red{color:#a22}</style>'''
mathjax = {'tex': {'inlineMath': [[r'\(', r'\)']], 'displayMath': [[r'\[', r'\]']]}}
head += '<script>window.MathJax=' + json.dumps(mathjax) + ';</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script></head><body><aside>Independent static content inspection at commit 813268bc. Current canonical audit remains blind-reconstructed. No whole-site, browser-pixel, desktop/mobile or deployed acceptance is claimed. TeX and exact code are inspected below.</aside>'
doc = head + body + '</body></html>'

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.details, self.panels, self.current, self.pre = [], [], None, 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'details':
            self.details.append(attrs)
            if attrs.get('data-inline-lean'):
                self.current = {'name': attrs['data-inline-lean'], 'class': attrs.get('class', ''), 'code': ''}
                self.panels.append(self.current)
        if tag == 'pre':
            self.pre += 1
    def handle_endtag(self, tag):
        if tag == 'pre':
            self.pre -= 1
        if tag == 'details':
            self.current = None
    def handle_data(self, text):
        if self.pre and self.current is not None:
            self.current['code'] += text

ins = Inspect()
ins.feed(doc)
assert all('open' not in attrs for attrs in ins.details)
for name in [unit['declaration'], consumer]:
    exact = inline_lean.display_source(known[name].source_text)
    signature, _ = inline_lean.split_statement(exact)
    for role, expected in [('statement', signature), ('proof', exact)]:
        panels = [p for p in ins.panels if p['name'] == name and 'inline-lean-' + role in p['class']]
        assert len(panels) == 1, (name, role)
        assert panels[0]['code'] == expected, (name, role, 'displayed code differs')
assert html.escape(unit['formula']) in doc
for step in unit['steps']:
    assert html.escape(step['formula']) in doc
assert doc.index('reader-main-equation') < doc.index('inline-lean-statement') < doc.index('Mathematical proof') < doc.index('inline-lean-proof')
assert 'source-implicit' in html.unescape(doc) and 'both complete main lower bounds' in html.unescape(doc)
assert len(unit['astis_dependencies']) == 3
source_scan = []
for path in paths:
    clean = base.sanitize_lean(path.read_text())
    bad = [token for token in ['sorry', 'admit', 'axiom'] if re.search(r'\b' + token + r'\b', clean)]
    assert not bad, (str(path), bad)
    source_scan.append({'file': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'fake_closure_tokens': bad})
summary = {
    'generic_helpers': ['publication_reader.source_card', 'declaration_lessons.render_unit', 'inline_lean.disclosure'],
    'bounded_scanner_paths': [str(path.relative_to(ROOT)) for path in paths],
    'no_whole_site_or_registry_scan': True,
    'canonical_audit_state_displayed': audit['state'],
    'empty_local_cells_reason': 'No sourceV/current-cell acceptance in isolated static review; generic verified_binding remains false. No status fabricated.',
    'details_total': len(ins.details), 'all_disclosures_initially_closed': True,
    'exact_code_panels_checked': [(p['name'], p['class'], hashlib.sha256(p['code'].encode()).hexdigest()) for p in ins.panels],
    'formula_and_assumption_contents': 'Matched authored exact formulas, source parameter domains, standard convention disclosure, 3 actual parents and open boundaries.',
    'statement_and_proof_adjacent_in_dom': True,
    'css_or_mathjax_pixel_render_performed': False, 'desktop_mobile_or_deployed_acceptance': False,
    'source_scan': source_scan, 'reader_sha256': hashlib.sha256(doc.encode()).hexdigest()}
outputs = [ROOT / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-normalizer-semantic-evidence/fresh-source-reader-640251/phase3',
           ROOT / '.astis/huanjian-fixed-spectrum-normalizer-20261108/fresh-source-640251/phase3']
for out in outputs:
    (out / 'static-reader').mkdir(exist_ok=True)
    with (out / 'static-reader/review-reader.html').open('x') as handle:
        handle.write(doc)
    with (out / 'static-reader/reader-content-checks.json').open('x') as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
print(json.dumps(summary, ensure_ascii=False, indent=2))
