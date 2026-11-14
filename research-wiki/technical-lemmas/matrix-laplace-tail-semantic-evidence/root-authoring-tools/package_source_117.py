from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_fresh_source_8d2a'
actor=n/'own-original-leaf-manifest.v3.json'
assert hashlib.sha256(actor.read_bytes()).hexdigest()=='011e6accbace4b9ee416f66c212f6172e4cc65b698242ed719424efdf8f82429'
x=json.loads(actor.read_text());rows=[p for p in x['leaves'] if p['include_by_default']]
assert len(rows)==117
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/source-review/laplace_fresh_source_8d2a'
e.mkdir(parents=True,exist_ok=True)
m=e/'ROOT-selected-source-through-v4-context-117.v1.json';assert not m.exists()
m.write_text(json.dumps({'scope':'ROOT later selection of the117 actor-explicit default custody leaves through exactv4 source context, bounded mapv2 and typed conceptual mechanism review. No browser or normal Discovery validation is covered yet. Whole source PDF/HTML/layout, process/cache and full guarded state remain excluded/reference-only.',
 'original_actor_manifest_sha256':hashlib.sha256(actor.read_bytes()).hexdigest(),
 'files':[{'path':p['path'],'bytes':p['bytes'],'sha256':p['sha256']} for p in rows]},ensure_ascii=False,indent=2)+'\n')
(e/actor.name).write_bytes(actor.read_bytes())
subprocess.run(['python3',str(w/'lossless_allowlist_container.native-dag-v2.py'),
 '--source-base',str(n),'--manifest',str(m),'--output-archive',str(e/'selected-source-through-v4-context.originals117.v1.tar.gz'),
 '--custody-json',str(e/'ROOT-selected-source117-container-custody.v1.json')],check=True)
readable=['source_correspondence_v1/SOURCE_CORRESPONDENCE_V1_FROZEN.json',
 'source_correspondence_v2/SOURCE_CORRESPONDENCE_V2_FROZEN.json',
 'conceptual_mirror_v1/CONCEPTUAL_MIRROR_V1_FROZEN.json',
 'schema_field_v4/SCHEMA_FIELD_V4_FROZEN.json']
for name in readable:
    b=(n/name).read_bytes();p=e/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
print(json.dumps({'selected_source_leaves':117,'actor_original_manifest_leaves':len(x['leaves']),
 'raw_input_source_reference_only':True,'normal_API_or_browser_not_covered':True}))
