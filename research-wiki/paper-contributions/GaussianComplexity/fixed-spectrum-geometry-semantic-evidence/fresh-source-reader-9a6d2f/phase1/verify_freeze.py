from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def h(b):return hashlib.sha256(b).hexdigest()
m=json.loads((OUT/'phase1_manifest.json').read_text())
assert h((OUT/'phase1_manifest.json').read_bytes())==(OUT/'phase1_manifest.sha256').read_text().split()[0]
for f in m['files']:
 p=(OUT/f['path']).resolve();assert p.is_relative_to(OUT)
 b=p.read_bytes();assert len(b)==f['bytes'] and h(b)==f['sha256'],f['path']
actual={str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()}
assert actual=={f['path'] for f in m['files']}|{'phase1_manifest.json','phase1_manifest.sha256'}
i=json.loads((OUT/'input_manifest.json').read_text())
for f in i['inputs']:
 b=(ROOT/f['path']).read_bytes();assert len(b)==f['bytes'] and h(b)==f['sha256'],f['path']
 if 'snapshot' in f:assert (OUT/f['snapshot']).read_bytes()==b
index=json.loads((OUT/'excerpt_index.json').read_text());raw=(ROOT/index['source']).read_bytes()
assert len(raw)==index['bytes'] and h(raw)==index['sha256']
for e in index['excerpts']:
 b=(OUT/e['raw_file']).read_bytes();assert b==raw[e['source_byte_start']:e['source_byte_end_exclusive']]
 assert h(b)==e['raw_sha256'];assert h((OUT/e['readable_file']).read_bytes())==e['readable_sha256']
t=json.loads((OUT/'source_topology.json').read_text());ids={n['id'] for n in t['nodes']}
assert len(ids)==len(t['nodes'])
for e in t['edges']:assert e['producer'] in ids and e['consumer'] in ids and e['consumer_use_site']
for x in t['source_inventory']:
 assert x['disposition'] in ('NODE','EXCLUDED')
 if x['disposition']=='NODE':assert x['node_ids'] and set(x['node_ids'])<=ids
 else:assert x['reason']
print(json.dumps({'static_freeze_check':'pass','manifest_sha256':h((OUT/'phase1_manifest.json').read_bytes()),'files':len(m['files']),'source_sha256':h(raw),'source_bytes':len(raw),'excerpts':len(index['excerpts']),'nodes':len(t['nodes']),'edges':len(t['edges']),'inventory_items':len(t['source_inventory']),'not_checked':['Lean','candidate source fidelity','publication','site','independent approval of this topology']}))
