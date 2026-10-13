"""Bounded generated HTML inspection, explicitly not browser/render evidence."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json

class Unit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.active = False
        self.found = False
        self.code = None
        self.codes = []
        self.details = []
        self.steps = 0
        self.text = []
        self.links = []
        self.events = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id') == 'pbps-actual-finite-first-event-law':
            assert not self.found
            self.active = self.found = True
        if not self.active:
            return
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.depth += 1
        if tag == 'details':
            self.details.append(a)
            if a.get('data-inline-lean'):
                self.events.append(('lean', a['data-inline-lean'], a.get('class','')))
        if 'proof-roadmap' in a.get('class','').split():
            self.events.append(('roadmap', '', ''))
        if 'proof-reader-step' in a.get('class','').split():
            self.steps += 1
        if tag == 'code':
            assert self.code is None
            self.code = []
        if tag == 'a':
            self.links.append(a.get('href',''))
    def handle_endtag(self, tag):
        if not self.active:
            return
        if tag == 'code' and self.code is not None:
            self.codes.append(''.join(self.code))
            self.code = None
        self.depth -= 1
        if self.depth == 0:
            self.active = False
    def handle_data(self, data):
        if self.active:
            self.text.append(data)
            if self.code is not None:
                self.code.append(data)

run = Path('runs/20261007-companion-priority/pbps-actual-finite-first-event-law86')
gate = json.loads((run/'integration86/site-build/receipt.json').read_bytes())
assert gate['terminal_closed'] and gate['exit_code']==0
page = Path('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html')
raw = page.read_bytes()
p = Unit()
p.feed(raw.decode('utf8'))
lesson = json.loads(Path('website/content/declaration_lessons/pbps-actual-finite-first-event-law.json').read_bytes())['units'][0]
assert p.found and p.steps == len(lesson['steps']) == 11
assert p.details and all('open' not in d for d in p.details)
decl = lesson['declaration']
spec = decl + '_statement'
roadmap = next(i for i,e in enumerate(p.events) if e[0]=='roadmap')
assert p.events[0] == ('lean',decl,'inline-lean inline-lean-statement')
assert p.events[1] == ('lean',spec,'inline-lean inline-lean-proof')
assert roadmap == 2
assert sum(e[1]==spec for e in p.events)==1
for helper in lesson['helpers']:
    assert sum(e[1]==helper for e in p.events)==1, helper
    if helper != spec:
        assert next(i for i,e in enumerate(p.events) if e[1]==helper)>roadmap,helper
for step in lesson['steps']:
    assert any(step['lean'].strip() == code.strip() for code in p.codes), step['title']
assert lesson['title'] in ''.join(p.text)
out = run / 'integration86/offline-reader.json'
assert not out.exists()
out.write_text(json.dumps({
    'status': 'PASS_GENERATED_HTML_CONTENT_ONLY', 'page': page.as_posix(),
    'page_RAW_sha256': hashlib.sha256(raw).hexdigest(),
    'adjacent_steps': p.steps, 'exact_step_Lean_regions': 11,
    'details_initially_folded': len(p.details),
    'literal_statement_adjacent_before_roadmap': True,
    'five_proof_helpers_retained_once_after_roadmap': True,
    'rendered_page_inspected': False, 'browser_interactivity_tested': False,
    'remaining': 'Actual page and interactive branch visual acceptance, copy callbacks and live deployment are not certified by this parser.',
}, indent=2) + '\n', encoding='utf8')
print('Generated HTML has eleven exact adjacent step Lean regions and all details initially folded; rendering remains unverified.')
