from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_fresh_source_8d2a/reader_visual_v1'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/reader-review/laplace_fresh_source_8d2a/v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=n/'PUBLIC_EVIDENCE_MANIFEST.json';f=n/'READER_VISUAL_V1_FROZEN.json'
assert sha(m)=='68a70284c2b4759a5a0f0b8ebd82e970c2664f2a3bc2e678231ea64fee6b7ac1'
assert sha(f)=='464e155d01f167fb7b90624c318d3687136f310f1dab4989cda71baa70afcadf'
x=json.loads(m.read_text());rows=list(x['selected_own_leaves']);assert len(rows)==17
for p in [m,f]:rows.append({'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
e.mkdir(parents=True,exist_ok=True)
selection=e/'ROOT-selected-reader-visual19.v1.json';assert not selection.exists()
selection.write_text(json.dumps({'scope':'ROOT later container of exact independent partial-reader-review originals. No correction acceptance is claimed. Raw browser inputs reference existing356 original archive, not duplicate copies.','files':rows},ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3',str(w/'lossless_allowlist_container.native-dag-v2.py'),
 '--source-base',str(n),'--manifest',str(selection),'--output-archive',str(e/'selected-reader-visual-originals19.v1.tar.gz'),
 '--custody-json',str(e/'ROOT-reader-visual19-container-custody.v1.json')],check=True)
for p in [m,f,n/'reader-visual.review-run.json',n/'reader-visual.review.json',n/'independent_visual_review.md']:
    target=e/p.name;assert not target.exists();target.write_bytes(p.read_bytes())
print(json.dumps({'exact_original_members':19,'partial_acceptance_only':True,'normal_V_calls':0,
 'archive_sha256':sha(e/'selected-reader-visual-originals19.v1.tar.gz')}))
