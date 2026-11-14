from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
n=r/'.astis/semantic-neutral-20261114/laplace_native_61e4'
selection=w/'metadata-drafts/native-public-selection-audit/native-public-selection.238.candidate.v1.json'
assert hashlib.sha256(selection.read_bytes()).hexdigest()=='3b818d5e7b41f514a90f4b284ec9e690a11eb0ba5826a918b36304b52d3d7bf3'
x=json.loads(selection.read_text());assert x['selected_leaf_count']==len(x['leaves'])==238
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/native-originals/laplace_native_61e4'
e.mkdir(parents=True,exist_ok=True)
m=e/'ROOT-public-selected-native-238.v1.json';assert not m.exists()
payload={'schema':'ROOT-later-explicit-selected-native-originals-v1','scope':x['selection_scope'],
 'original_independent_actor_manifest_sha256':x['actor_manifest_sha256'],
 'independent_exact_public_selection_sha256':hashlib.sha256(selection.read_bytes()).hexdigest(),
 'excluded_actor_leaves_local_only':x['excluded_actor_leaves'],'files':x['leaves']}
m.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
for name in ['selected-originals.manifest.v1.json','native-mathematics-report.v1.json',
'native-mathematical-inspection.v1.json','actual-canonical-parent-witnesses.v1.json','literal-source-interface.json']:
    (e/name).write_bytes((n/name).read_bytes())
(e/selection.name).write_bytes(selection.read_bytes())
subprocess.run(['python3','.astis/semantic-neutral-20261114/mgf_public_progress_audit_73af/lossless_allowlist_container.py',
'--source-base',str(n),'--manifest',str(m),'--output-archive',str(e/'selected-native-originals.public238.v1.tar.gz'),
'--custody-json',str(e/'ROOT-public238-container-custody.v1.json')],check=True)
note={'scope':'ROOT later lossless container; not a new independent native run or source verdict.',
 'independent_original_manifest_preserved_exact':True,
 'selection_difference':'The original actor manifest lists239 leaves. This distinct public selection retains238 exact original leaves and excludes only the full immutable-repository path/OID inventory stdout, which remains unchanged local. No raw output is normalized, trimmed or rewritten.',
 'broad_private_path_flag_clarification':'The original actor flag about sanitizing command environment paths is preserved. The actor and separate independent public-selection auditor found no credentials/foreign guards/ATLAS content in the238 selected leaves. Known absolute HOME/PATH/LEAN_PATH references remain byte-exact, not sanitized.',
 'evidence_boundaries':'Every original command identity, failed literal-application harness and successful successor, genuine source closure/native JSON type+value graphs and q0/four-family checks remain. The excluded full repository inventory is not needed as a mathematical witness. Its original command receipt retains the local-only stdout hash.',
 'full_repository_inventory_is_not_in_archive':True,
 'archive_is_not_the_original_239_payload':True,'future_public_commit_acceptance':'PENDING independent final payload/ancestry review'}
(e/'public238-selection-truth-boundary.v1.json').write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'exact_original_leaves':238,'excluded_local_only_inventory_leaves':1,'original_manifest239_unchanged':True,'no_raw_rewrite':True}))
