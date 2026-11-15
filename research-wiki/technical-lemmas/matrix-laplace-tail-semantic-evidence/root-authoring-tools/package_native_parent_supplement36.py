from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-parent-supplement-v2'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/reader-originals/laplace_native_61e4/parent-supplement-v2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=n/'public-safe-selected-originals.manifest.v1.json'
assert sha(m)=='18bdb58835b1fc79d7f00789527ebb4cdefca862178d23a6bff66d5166173b63'
x=json.loads(m.read_text());assert len(x['leaves'])==36 and x['actual_contract_all_PASS'] is False
rows=[{k:v[k] for k in ['path','bytes','sha256']} for v in x['leaves']]
assert sum(v['path'].endswith('.png') for v in rows)==24
assert not any('chrome-tmp' in Path(v['path']).parts for v in rows)
e.mkdir(parents=True,exist_ok=True)
selection=e/'ROOT-selected-native-parent-supplement36.v1.json';assert not selection.exists()
selection.write_text(json.dumps({'scope':'ROOT later container of all36 exact actor-explicit raw targeted supplement leaves. Native process FAIL and wrong/unexecuted crop steps preserved. Independent combined reader acceptance remains distinct. Prepared v3 has no execution evidence.','files':rows},ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3',str(w/'lossless_allowlist_container.native-dag-v2.py'),
 '--source-base',str(n),'--manifest',str(selection),
 '--output-archive',str(e/'selected-native-parent-supplement-originals36.v1.tar.gz'),
 '--custody-json',str(e/'ROOT-native-parent-supplement36-container-custody.v1.json')],check=True)
for name in ['public-safe-selected-originals.manifest.v1.json','native-supplemental-outcome.v1.json','screenshot-coordinate-diagnosis.v1.json','unexecuted-v3-cancellation.reference-only.json']:
    out=e/name;assert not out.exists();out.write_bytes((n/name).read_bytes())
print(json.dumps({'exact_actor_selected_members':36,'raw_native_exit_code':1,'V_calls':0,
 'archive_sha256':sha(e/'selected-native-parent-supplement-originals36.v1.tar.gz')}))
