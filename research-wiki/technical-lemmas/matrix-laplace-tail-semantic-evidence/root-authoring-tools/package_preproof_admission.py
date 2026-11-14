from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
m=w/'metadata-drafts/public-admission-custody/admission-originals.allowlist.v1.json'
v=json.loads(m.read_text());rows=v['audit_leaf_allowlist']
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/preproof-originals'
e.mkdir(parents=True,exist_ok=True)
out=e/'ROOT-selected-admission-leaves.v1.json'
assert not out.exists()
selected={'scope':'ROOT later mechanical selection of the 244 explicitly listed independent metadata custody leaves. Original actor/custodian map remains in the byte-exact original manifest. No whole PDF/HTML/layout, private guard, foreign map, cache, Git index or new proof is selected.',
 'original_actor_manifest_sha256':hashlib.sha256(m.read_bytes()).hexdigest(),
 'files':[{'path':a['relative_path'],'bytes':a['bytes'],'sha256':a['sha256']} for a in rows]}
out.write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
for name in ['admission-originals.allowlist.v1.json','reference-closure.v1.json','portable-relocation-map.v1.json','summary.v1.json']:
    (e/name).write_bytes((m.parent/name).read_bytes())
cmd=['python3','.astis/semantic-neutral-20261114/mgf_public_progress_audit_73af/lossless_allowlist_container.py',
'--source-base',str(r),'--manifest',str(out),'--output-archive',str(e/'selected-preproof-admission-originals.v1.tar.gz'),
'--custody-json',str(e/'ROOT-container-custody.v1.json')]
subprocess.run(cmd,check=True)
readable={
'statement-seal.sealed.v1.json':w/'statement-seal.sealed.v1.json',
'original-binder-definition-audit.sealed.v1.json':w/'binder-definition-audit.sealed.v1.json',
'binder-inventory-singleton.supplement.v1.json':w/'binder-inventory-singleton.supplement.v1.json',
'source-graph.repaired.v2.1.json':r/'.astis/semantic-neutral-20261114/matrix_laplace_source_graph_b37c/source-graph.repaired.v2.1.json',
'coverage.exact.v2.1.json':r/'.astis/semantic-neutral-20261114/matrix_laplace_source_graph_b37c/coverage.exact.v2.1.json',
'source-vs-seal.repaired.v2.1.json':r/'.astis/semantic-neutral-20261114/matrix_laplace_source_graph_b37c/source-vs-seal.repaired.v2.1.json',
'TC.final-admission.v1.json':r/'.astis/semantic-neutral-20261114/matrix_laplace_topology_4c9e/final-admission.v1.json'}
copies=[]
for name,p in readable.items():
    (e/name).write_bytes(p.read_bytes())
    copies.append({'path':str((e/name).relative_to(r)),'original_path':str(p.relative_to(r)),
      'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(e/'readable-exact-copies.v1.json').write_text(json.dumps({'scope':'Byte-exact index copies, not reauthored actor originals; all selected raw evidence also retained in lossless archive. Original .astis references resolve by original-relative archive member, with external source inputs explicitly reference-only.','files':copies},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'selected_raw_leaves':len(rows),'all_raw_originals_preserved':True,'not_a_public_privacy_or_math_verdict':True}))
