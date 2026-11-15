from pathlib import Path
import hashlib,json,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
n=r/'.astis/semantic-neutral-20261115/trace_exp_native_61e4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ms={
 'normal-proof-verification/preparation-public-selected-originals.manifest.v2.json':'e9d17408bdad1ee5309fb2223f32029d225e769d439f1ea8ae3297639d906d41',
 'normal-proof-verification/window1-public-selected-originals.manifest.json':'dbeeca47422d6c58091e2a5061ac3d602758ebcd0f6ff68f338b4a45609ae414',
 'normal-proof-verification/window2-failure-preservation.manifest.json':'914f956b48d45e71292d1e635dd9a61e4a00fda431462f397692161cfbc40ff0',
 'normal-proof-verification/window2-readonly-diagnosis-v1/public-selected-originals.manifest.json':'38ae7e439a02c75b6a653d1f069f358aa3f5136a5690dcbf4d2c38bdaa02b320',
 'projection-only-successor-v1/preparation-public-selected-originals.manifest.json':'c63ec6ba39c6dae23691364dd95687e17936353f5776ce6be18e0d32dba3dbea',
 'projection-only-successor-v1/projection-public-selected-originals.manifest.json':'28254a94e8c97bb07c98f8c3d1487c3d38377d4cf693fc5b89e897dac4aacb6f'}
files={}
for name,h in ms.items():
    p=n/name;assert sha(p)==h
    for x in json.loads(p.read_text())['files']:
        q=p.parent/x['path'];assert q.resolve().is_relative_to(n.resolve()) and 'local-private-guards' not in q.parts
        assert q.stat().st_size==x['bytes'] and sha(q)==x['sha256']
        rel=str(q.relative_to(n));assert rel not in files or files[rel]['sha256']==x['sha256']
        files[rel]={'path':rel,'bytes':x['bytes'],'sha256':x['sha256']}
    files[name]={'path':name,'bytes':p.stat().st_size,'sha256':h}
# These three explicit authorizations are ROOT-owned inputs, not extra independent outcomes.
for name in ['normal-proof-verification/window1.ROOT-authorization.v1.json',
 'normal-proof-verification/window2.ROOT-authorization.v1.json',
 'projection-only-successor-v1/ROOT-projection-authorization.v1.json']:
    p=n/name;files[name]={'path':name,'bytes':p.stat().st_size,'sha256':sha(p)}
out=e/'normal-verification/trace_exp_native_61e4';assert not out.exists();out.mkdir(parents=True)
manifest=out/'ROOT-explicit-original-selection.v1.json';manifest.write_text(json.dumps({
 'kind':'ROOT-later-union-of-explicit-independent-public-allowlists-plus-three-ROOT-authorizations',
 'scope':'Successful normalV1, original failed cellprojection, exact readonly diagnosis and new successful projection-only successor; every predecessor retained. No private guard/map/fullledger/index/git/API raw stream or cache selected.',
 'original_actor_manifests':ms,'file_count':len(files),'files':list(files.values())},ensure_ascii=False,indent=2)+'\n')
packer=r/'.astis/huanjian-gc-matrix-laplace-20261114/lossless_allowlist_container.native-dag-v2.py'
assert sha(packer)=='4385d8e2ab61344e1ecfdbd3d3f8e5f74f1f5983f33fc5ee3c5efaf1468db774'
archive=out/'selected-independent-normal-V-and-cell-originals.v1.tar.gz';custody=out/'ROOT-later-lossless-normal-verification-custody.v1.json'
subprocess.run(['python3',str(packer),'--source-base',str(n),'--manifest',str(manifest),
 '--output-archive',str(archive),'--custody-json',str(custody)],check=True)
readable=out/'readable-originals';readable.mkdir()
for name in ['normal-proof-verification/normal-V-outcome.public.json',
 'normal-proof-verification/normal-V-exact-append.jsonl','normal-proof-verification/window1-OS-receipt.public.json',
 'normal-proof-verification/window2-failure-preservation.public.json',
 'projection-only-successor-v1/projection-outcome.public.json','projection-only-successor-v1/projection-OS-receipt.public.json']:
    q=readable/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((n/name).read_bytes())
resolution={'kind':'ROOT-later-byte-exact-portable-reference-resolution-not-new-independent-verification',
 'archive':str(archive.relative_to(r)),'archive_sha256':sha(archive),
 'aliases':[{'original_repository_relative':str((n/x['path']).relative_to(r)),
    'member':x['path'],'bytes':x['bytes'],'sha256':x['sha256']} for x in files.values()],
 'truth_boundary':'Exactly one independent normal proofV. First cellprojection remains actual exit1, write0/API0; stopped receipt API_attempt_marker_present refers to already successful window1 marker. Actual canonical diagnostic uniquely identified string-required independent_verification. New projection-only successor exit0 writes exact0bec with API0/additionalV0. No earlier failure relabelled PASS, no repeated proof or source/browser/build/integration claim.',
 'reconstruction_qualification':'The failed proposed cell is honestly labelled AST reconstruction made after failure, not falsely claimed an original pre-failure saved artifact.',
 'original_PL24_sha256':'a17ff70fa56a86070673d630943b43148f32f874f6f3f1243ddf6b73c2d889bf',
 'actual_normal_V_suffix_sha256':'687201b4deea0187f8a94fa69b6f07aa16bc01237a6917c574e35ac197835784',
 'actual_independently_projected_cell_sha256':'0becf6729aa2bc943b2a6ff4f36c5ea476a6d4e5212e58008512d36c6f26b7a7',
 'actual_build_identity':'30172847ec40c24426f0b39afc4887719810eca0','verified_carrier':'45564beb6e0dd5e4357718ea04347a50613ad502'}
(out/'ROOT-original-reference-portable-resolution.v1.json').write_text(json.dumps(resolution,ensure_ascii=False,indent=2)+'\n')
cp=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json'
assert sha(cp)==resolution['actual_independently_projected_cell_sha256']
assert sha(e/'PROVED_LOCAL-evidence.full.json')==resolution['original_PL24_sha256']
mem=e/'local-cycle-memory.json';v=json.loads(mem.read_text());v.update(normal_state='VERIFIED',normal_PL_calls=1,independent_normal_V_calls=1,ROOT_V_calls=0,
 independent_verifier='trace_exp_native_61e4_independent_verifier',verified_source_carrier=resolution['verified_carrier'],independent_cell_sha256=sha(cp),
 projection_failure='Original first schema failure preserved; exact minimal string-type successor independently projected once. No repeated V.',main_integration='held_original_owners',whole_Goal_complete=False)
mem.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'selected_explicit_leaves':len(files),'archive_sha256':sha(archive),'normal_PL':1,'independent_normal_V':1,'Root_V':0,'independent_cell_original_bytes_unchanged':True}))
