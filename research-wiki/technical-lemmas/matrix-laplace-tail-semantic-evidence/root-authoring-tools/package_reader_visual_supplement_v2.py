from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_fresh_source_8d2a/reader_visual_supplement_v2'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/reader-review/laplace_fresh_source_8d2a/supplement-v2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=n/'PUBLIC_EVIDENCE_MANIFEST.json'
assert sha(m)=='3fa4e9a6978738babf70012f425a454c19b8a6dc78c1000440da7d6f1be7b57d'
x=json.loads(m.read_text());assert len(x['leaves'])==14
rows=[{k:v[k] for k in ['path','bytes','sha256']} for v in x['leaves']]
rows.append({'path':m.name,'bytes':m.stat().st_size,'sha256':sha(m)})
e.mkdir(parents=True,exist_ok=True)
selection=e/'ROOT-selected-reader-visual-supplement15.v1.json';assert not selection.exists()
selection.write_text(json.dumps({'scope':'ROOT later lossless container of independent changed-PNG/geometry review originals. Finding closed by actual full viewport evidence plus unchanged accepted v1 source/nav. The native v2 process remains FAIL; optional crop bug and unexecuted repeated mobile steps remain explicit. No v3 execution claimed.','files':rows},ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3',str(w/'lossless_allowlist_container.native-dag-v2.py'),
 '--source-base',str(n),'--manifest',str(selection),
 '--output-archive',str(e/'selected-reader-visual-supplement-originals15.v1.tar.gz'),
 '--custody-json',str(e/'ROOT-reader-visual-supplement15-container-custody.v1.json')],check=True)
for name in ['PUBLIC_EVIDENCE_MANIFEST.json','READER_VISUAL_SUPPLEMENT_V2_FROZEN.json','reader-visual-supplement.review-run.json','reader-visual-supplement.review.json','independent_visual_review.md']:
    target=e/name;assert not target.exists();target.write_bytes((n/name).read_bytes())
print(json.dumps({'exact_original_members':15,'native_exit1_preserved':True,'v3_not_used':True,'normal_V_calls':0,
 'archive_sha256':sha(e/'selected-reader-visual-supplement-originals15.v1.tar.gz')}))
