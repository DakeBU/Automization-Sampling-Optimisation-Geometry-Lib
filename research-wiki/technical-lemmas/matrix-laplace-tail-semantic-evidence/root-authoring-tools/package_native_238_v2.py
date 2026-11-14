from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_native_61e4'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/native-originals/laplace_native_61e4'
packer=w/'lossless_allowlist_container.native-dag-v2.py'
assert hashlib.sha256(packer.read_bytes()).hexdigest()=='4385d8e2ab61344e1ecfdbd3d3f8e5f74f1f5983f33fc5ee3c5efaf1468db774'
reviewdir=w/'metadata-drafts/packer-depth-repair-review'
reports=[p for p in reviewdir.glob('*.json') if hashlib.sha256(p.read_bytes()).hexdigest()=='efe36a0638992f157285b204328644bbcbd0a6699c1c77203a8e034bbace73fe']
assert len(reports)==1
m=e/'ROOT-public-selected-native-238.v1.json'
assert len(json.loads(m.read_text())['files'])==238
archive=e/'selected-native-originals.public238.v2.tar.gz';assert not archive.exists()
subprocess.run(['python3',str(packer),'--source-base',str(n),'--manifest',str(m),
 '--output-archive',str(archive),'--custody-json',str(e/'ROOT-public238-container-custody.v2.json')],check=True)
for name in ['native-public-selection-audit.v1.json','native-public-selection.238.candidate.v1.json']:
    (e/name).write_bytes((w/'metadata-drafts/native-public-selection-audit'/name).read_bytes())
(e/'depth-limit-repair-review.original.json').write_bytes(reports[0].read_bytes())
note={'scope':'ROOT later lossless public-selection container; not a new native run or source verdict.',
 'independent_original_manifest_preserved_exact':True,
 'selection_difference':'Original actor manifest lists239 leaves. This distinct public selection retains238 exact original leaves and excludes only full immutable-repository path/OID inventory stdout (136870 records), unchanged local. No raw output normalized, trimmed or rewritten.',
 'broad_private_path_flag_clarification':'Original actor broad flag about command environment paths is preserved. Actor and separate independent public-selection auditor found no credentials/foreign guard/ATLAS content in238 selected leaves. Known absolute HOME/PATH/LEAN_PATH references remain exact.',
 'failed_predecessor':'Original cap8 packager rejected genuine raw Expr/Level DAG JSON depths14–16. Actual failed receipt/log preserved; no mathematics or approval rejection occurred. New cap32 changes no other private/member/byte guard; independent96 synthetic tests passed.',
 'actual_selected_leaves':238,'full_repository_inventory_not_in_archive':True,
 'independent_depth_repair_report_sha256':hashlib.sha256(reports[0].read_bytes()).hexdigest(),
 'actual_archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
 'archive_is_not_original_239_payload':True,'future_commit_acceptance':'PENDING independent final payload/ancestry review'}
(e/'public238-selection-truth-boundary.v2.json').write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'actual_archive_sha256':note['actual_archive_sha256'],'members':238,'all_selected_raw_bytes_exact':True,'normal_V_calls':0}))
