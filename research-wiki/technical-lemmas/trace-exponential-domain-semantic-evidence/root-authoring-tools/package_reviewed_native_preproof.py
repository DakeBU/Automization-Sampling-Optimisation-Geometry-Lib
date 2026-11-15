"""ROOT-later lossless publication container; not new independent evidence."""
from pathlib import Path
import json,hashlib,subprocess,shutil
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
d=w/'metadata-drafts/public-custody-review-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sel=d/'public-custody.selection.candidate.v1.json'
report=d/'PUBLIC-CUSTODY-REVIEW-SUMMARY.v1.json'
assert sha(sel)=='7a831090e97a0d8db7815a1e2dd78970cec68212aec8ff5f9b898dd12f908cd7'
assert sha(report)=='cc1a2447d360b5b7169301c74bd5f2070ba03d540cdeb7da90814169f7019935'
v=json.loads(sel.read_text());assert len(v['files'])==278
assert sum(x['bytes'] for x in v['files'])==57043278
for x in v['files']:
    p=r/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
packer=r/'.astis/huanjian-gc-matrix-laplace-20261114/lossless_allowlist_container.native-dag-v2.py'
assert sha(packer)=='4385d8e2ab61344e1ecfdbd3d3f8e5f74f1f5983f33fc5ee3c5efaf1468db774'
out=e/'independent-native-and-preproof-originals';assert not out.exists();out.mkdir()
for p in [sel,report,d/'native248.privacy-custody-review.v1.json',d/'native248.reference-closure.v1.json',
 d/'preproof-subreview/preproof.custody-privacy-review.v1.json',
 d/'preproof-subreview/native-seven-scripts.privacy-review.v1.json',
 r/'.astis/semantic-neutral-20261115/trace_exp_native_61e4/public-safe-selected-originals.manifest.v1.json']:
    (out/p.name).write_bytes(p.read_bytes())
archive=out/'selected-reviewed-originals278.v1.tar.gz'
custody=out/'ROOT-later-lossless-custody278.v1.json'
subprocess.run(['python3',str(packer),'--source-base',str(r),'--manifest',str(sel),
    '--output-archive',str(archive),'--custody-json',str(custody)],check=True)
readable=out/'readable-native-originals';readable.mkdir()
nr=r/'.astis/semantic-neutral-20261115/trace_exp_native_61e4'
for name in ['native-mathematics-report.v1.json','actual-type-and-parent-witnesses.v1.json',
 'fake-closure-scan.v1.json','actual-import-closure.json','verified-package-inputs.json']:
    (readable/name).write_bytes((nr/name).read_bytes())
root_orig=e/'preproof-root-selected-originals';assert not root_orig.exists();root_orig.mkdir()
roots=['statement-seal.sealed.v1.json','binder-definition-audit.sealed.v1.json',
 'norm-scope-seal-supplement.v1.json','InterfaceFormation.v2.lean','StatementNormScopeAudit.lean']
for name in roots:(root_orig/name).write_bytes((w/name).read_bytes())
aliases=[{'original_repository_relative':x['path'],'archive':str(archive.relative_to(r)),
    'member':x['path'],'bytes':x['bytes'],'sha256':x['sha256']} for x in v['files']]
for name in roots:
    p=root_orig/name;aliases.append({'original_repository_relative':str((w/name).relative_to(r)),
        'portable_byte_exact_file':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)})
obj={'kind':'ROOT-later-portable-reference-resolution-not-original-review',
    'original_selected_manifest_sha256':sha(sel),'original_independent_review_sha256':sha(report),
    'archive_sha256':sha(archive),'custody_sha256':sha(custody),'aliases':aliases,
    'root_formation_scope':'Two selected .lean inputs contain only Proposition-valued definitions and #check/#print/#synth diagnostics, not target theorem proofs. Original actual diagnostic receipt/log already preserved separately in local-math-originals.',
    'reference_only_limits':json.loads(report.read_text())['reference_and_portability_limits'],
    'source_inputs':v['reference_only_source_inputs'],
    'status':'EXACT_REVIEWED_SELECTION_LOSSLESSLY_CONTAINERIZED; NO_NEW_LEAN_SOURCE_READER_OR_NORMAL_V_VERDICT',
    'preservation':'Original actor files/manifests and all failure streams unchanged. No restricted ATLAS payload/cache/full workspace/foreign guard or private Git index selected; policy path mentions remain reference-only. Original workstation paths are retained, never rewritten inside originals.'}
(out/'ROOT-original-reference-portable-resolution.v1.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'archive':str(archive.relative_to(r)),'sha256':sha(archive),
    'reviewed_original_members':278,'uncompressed_bytes':57043278,'normal_PL_calls':0,'normal_V_calls':0}))
