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
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id') == 'pbps-actual-outer-bounded-l2-continuity':
            assert not self.found
            self.active = self.found = True
        if not self.active:
            return
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.depth += 1
        if tag == 'details':
            self.details.append(a)
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

run = Path('runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84')
page = Path('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html')
raw = page.read_bytes()
p = Unit()
p.feed(raw.decode('utf8'))
lesson = json.loads(Path('website/content/declaration_lessons/pbps-actual-outer-bounded-l2-continuity.json').read_bytes())['units'][0]
assert p.found and p.steps == len(lesson['steps']) == 8
assert p.details and all('open' not in d for d in p.details)
for step in lesson['steps']:
    assert any(step['lean'].strip() == code.strip() for code in p.codes), step['title']
assert lesson['title'] in ''.join(p.text)
out = run / 'integration84/offline-reader.json'
assert not out.exists()
out.write_text(json.dumps({
    'status': 'PASS_GENERATED_HTML_CONTENT_ONLY', 'page': page.as_posix(),
    'page_RAW_sha256': hashlib.sha256(raw).hexdigest(),
    'adjacent_steps': p.steps, 'exact_step_Lean_regions': 8,
    'details_initially_folded': len(p.details),
    'rendered_page_inspected': False, 'browser_interactivity_tested': False,
    'remaining': 'Actual page and interactive branch visual acceptance, copy callbacks and live deployment are not certified by this parser.',
}, indent=2) + '\n', encoding='utf8')
print('Generated HTML has eight exact adjacent step Lean regions and all details initially folded; rendering remains unverified.')
