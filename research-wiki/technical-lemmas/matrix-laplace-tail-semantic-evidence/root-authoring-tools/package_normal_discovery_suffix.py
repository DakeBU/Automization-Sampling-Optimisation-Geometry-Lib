from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_fresh_source_8d2a'
old=json.loads((n/'own-original-leaf-manifest.v3.json').read_text())
p=n/'own-original-leaf-manifest.v4-public-safe.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='7f950051721157e80ce5ea3249365dcc36755a46e2ab644254ba55a39a0ec066'
x=json.loads(p.read_text());oldpaths={v['path'] for v in old['leaves'] if v['include_by_default']}
rows=[v for v in x['leaves'] if v['include_by_default'] and v['path'] not in oldpaths]
assert len(rows)==24
assert not any('local-private-guards' in v['path'] for v in rows)
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/normal-discovery-validation/laplace_fresh_source_8d2a'
e.mkdir(parents=True,exist_ok=True)
m=e/'ROOT-selected-normal-discovery-validation-suffix24.v1.json';assert not m.exists()
m.write_text(json.dumps({'scope':'Explicit24 new public-safe default actor leaves after the117 previously packaged source-review leaves. Full private guards, foreign maps/raw ledgers and Git index excluded by actor manifest and not copied. One normal typed conceptual Discovery validation only; not proof V.',
 'actor_public_safe_manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'files':[{'path':v['path'],'bytes':v['bytes'],'sha256':v['sha256']} for v in rows]},ensure_ascii=False,indent=2)+'\n')
(e/p.name).write_bytes(p.read_bytes())
subprocess.run(['python3',str(w/'lossless_allowlist_container.native-dag-v2.py'),
 '--source-base',str(n),'--manifest',str(m),'--output-archive',str(e/'normal-discovery-validation.originals24.v1.tar.gz'),
 '--custody-json',str(e/'ROOT-container-custody.v1.json')],check=True)
for name in ['normal-validation.receipt.json','NORMAL_DISCOVERY_VALIDATION_PUBLIC_FROZEN.json']:
    (e/name).write_bytes((n/'normal-discovery-validation'/name).read_bytes())
print(json.dumps({'new_actor_leaves':24,'target_discovery_validation_calls':1,'proof_V_calls':0,'private_guards_not_copied':True}))
