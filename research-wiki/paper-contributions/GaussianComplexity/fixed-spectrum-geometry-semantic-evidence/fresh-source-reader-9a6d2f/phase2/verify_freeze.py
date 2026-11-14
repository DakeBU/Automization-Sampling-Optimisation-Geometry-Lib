from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3]
def h(b):return hashlib.sha256(b).hexdigest()
p1=OUT.parent/'phase1';p1b=(p1/'phase1_manifest.json').read_bytes()
assert h(p1b)=='aa9b3ffb40981e0d6d80d9c1ac8458a610c41bb7137e185a89baf6d9c25f81f1'
p1m=json.loads(p1b)
for f in p1m['files']:
 b=(p1/f['path']).read_bytes();assert len(b)==f['bytes'] and h(b)==f['sha256']
m=json.loads((OUT/'phase2_manifest.json').read_text());assert h((OUT/'phase2_manifest.json').read_bytes())==(OUT/'phase2_manifest.sha256').read_text().split()[0]
for f in m['files']:
 p=(OUT/f['path']).resolve();assert p.is_relative_to(OUT);b=p.read_bytes();assert len(b)==f['bytes'] and h(b)==f['sha256']
assert {str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()}=={f['path'] for f in m['files']}|{'phase2_manifest.json','phase2_manifest.sha256'}
z=json.loads((OUT/'selective-input.snapshot.json').read_bytes());assert h((OUT/'selective-input.snapshot.json').read_bytes())=='66454bcce11cf77ab188da7cd77d7c9a943f05fbdf671559b147f730795d1ac9'
p=z['anonymous_decoder_packet'];payload={k:v for k,v in p.items() if k!='packet_sha256'}
assert h(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())==p['packet_sha256']
assert h(p['lean']['statement'].encode())==p['lean']['statement_sha256']
assert h(z['blind_reconstruction']['reconstructed_theorem_text'].encode())==z['blind_reconstruction']['reconstructed_text_sha256']
for f in json.loads((OUT/'actual_input_manifest.json').read_text())['inputs']:
 b=(ROOT/f['path']).read_bytes();assert len(b)==f['bytes'] and h(b)==f['sha256']
md=json.loads((OUT/'mathlib_definition_inputs.json').read_text())
for f in md['inputs']:
 b=(ROOT/f['path']).read_bytes();assert len(b)==f['file_bytes'] and h(b)==f['file_sha256'];lines=b.splitlines(keepends=True)
 for w in f['windows']:
  q=(OUT/w['file']).read_bytes();assert q==b''.join(lines[w['start_line_inclusive']-1:w['end_line_inclusive']]);assert len(q)==w['bytes'] and h(q)==w['sha256']
f=json.loads((OUT/'selective_findings.json').read_text());assert set(f['slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
assert f['blocking_deltas_within_selected_scope']==[] and len(f['coverage_differences'])==5
print(json.dumps({'static_freeze_check':'pass','phase1_payloads_unchanged':len(p1m['files']),'phase2_payloads':len(m['files']),'manifest_sha256':h((OUT/'phase2_manifest.json').read_bytes()),'finding':f['finding'],'not_checked':['whole-module','proof','fresh Lean','full-source-fidelity','publication','reader/runtime','lifecycle']}))
