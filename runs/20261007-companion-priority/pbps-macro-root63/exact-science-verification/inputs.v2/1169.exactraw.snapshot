import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(r'E:\Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/pbps-macro-root63/independent-source63'
SOURCE = ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
MAP = ROOT / 'runs/20261007-companion-priority/pbps-macro-root63/independent-math63/input.manifest.json'
EXPECTED = 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write_json(name, value):
    p = OUT / name
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return p

class Readable(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.math_depth = 0
        self.maths = []
        self.ids = []
        self.refs = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.append(d['id'])
        if tag == 'a' and 'href' in d:
            self.refs.append(d['href'])
        if tag == 'math':
            self.math_depth += 1
            if self.math_depth == 1:
                formula = d.get('alttext', '')
                self.maths.append(formula)
                self.parts.append(' $' + formula + '$ ')
        elif not self.math_depth and tag in ('p','div','tr','section','h2','h3','h4','li'):
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag == 'math':
            self.math_depth -= 1
        elif not self.math_depth and tag in ('p','div','tr','section','h2','h3','h4','li'):
            self.parts.append('\n')
    def handle_data(self, data):
        if not self.math_depth:
            self.parts.append(data)
    def text(self):
        lines = [re.sub(r'\s+', ' ', x).strip() for x in ''.join(self.parts).split('\n')]
        return '\n'.join(x for x in lines if x)

OUT.mkdir(parents=True, exist_ok=True)
write_json('lease.json', {'state':'ACTIVE','reviewer':'independent_source63','opened_utc':datetime.now(timezone.utc).isoformat(),'owner_scope':str(OUT),'source_first':True})
raw = SOURCE.read_bytes()
assert sha(raw) == EXPECTED
mapping = json.loads(MAP.read_text(encoding='utf-8'))
# Deliberately access only these two explicitly permitted source fields.
primary = mapping['source_primary']
regions = mapping['primary_regions']
assert len(regions) == 24
manifest = {'source_primary':primary,'source_region_count':len(regions),'primary_regions':[],'candidate_seen':False,'decoder_seen':False,'prior_verdict_seen':False}
for i, region in enumerate(regions):
    lo, hi = region['byte_range']
    b = raw[lo:hi]
    assert sha(b) == region['snapshot']['raw_sha256']
    lf = b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    base = f'primary-{i:02d}'
    raw_path = OUT / f'{base}.exactraw.snapshot.html'
    lf_path = OUT / f'{base}.lf.snapshot.html'
    raw_path.write_bytes(b)
    lf_path.write_bytes(lf)
    parser = Readable()
    parser.feed(b.decode('utf-8'))
    text_path = OUT / f'{base}.source-readable.txt'
    text_path.write_bytes((parser.text()+'\n').encode('utf-8'))
    manifest['primary_regions'].append({'index':i,'byte_range':[lo,hi],'raw_path':str(raw_path),'lf_path':str(lf_path),'raw_sha256':sha(b),'lf_sha256':sha(lf),'ids':parser.ids,'math_alttext':parser.maths,'source_refs':parser.refs,'readable_path':str(text_path)})
write_json('primary-only.input.manifest.json', manifest)
write_json('foreground-preread.receipt.json',{'reviewer':'independent_source63','executed_utc':datetime.now(timezone.utc).isoformat(),'action':'primary-only extraction and byte verification; actual literal region reading follows via terminal','primary_raw_sha256':sha(raw),'source_regions_verified':24,'candidate_seen':False,'decoder_seen':False,'prior_verdict_seen':False,'script_sha256':sha(Path(__file__).read_bytes()),'source_manifest_sha256':sha((OUT/'primary-only.input.manifest.json').read_bytes())})
print(json.dumps({'primary_verified':sha(raw),'regions':[{ 'index':r['index'],'bytes':r['byte_range'],'anchor':r['ids'][0] if r['ids'] else ''} for r in manifest['primary_regions']],'candidate_seen':False},indent=2))
