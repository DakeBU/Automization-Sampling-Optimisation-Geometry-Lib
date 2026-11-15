from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
s=r/'.astis/semantic-neutral-20261115/trace_exp_reader_61e4'
d=w/'metadata-drafts/reader-public-custody-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selection=d/'reader77.public-custody.candidate.v1.json'
assert sha(selection)=='454ae9742a982e8df5574fa75aefbee019129ba7076c3deb561eadd32fceec87'
manifest=s/'reader-acceptance-v1/public-selected-originals.manifest.json'
assert sha(manifest)=='3704d8043fe4a57fc96cd567d98ac3ca9cb7e15a030804e37c73a7fb3265b8e3'
m=json.loads(selection.read_text());assert len(m['files'])==77
assert sum(x['bytes'] for x in m['files'])==6774717
for x in m['files']:
    p=s/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
packer=r/'.astis/huanjian-gc-matrix-laplace-20261114/lossless_allowlist_container.native-dag-v2.py'
assert sha(packer)=='4385d8e2ab61344e1ecfdbd3d3f8e5f74f1f5983f33fc5ee3c5efaf1468db774'
out=e/'reader-originals/trace_exp_reader_61e4';assert not out.exists();out.mkdir(parents=True)
for p in [selection,manifest]: (out/p.name).write_bytes(p.read_bytes())
archive=out/'selected-actual-reader-originals77.v1.tar.gz';custody=out/'ROOT-later-lossless-reader77-custody.v1.json'
subprocess.run(['python3',str(packer),'--source-base',str(s),'--manifest',str(selection),
 '--output-archive',str(archive),'--custody-json',str(custody)],check=True)
readable=out/'readable-originals';readable.mkdir()
for rel in ['actual-result.json','runtime-process/receipt.json','runtime-process/stdout.raw','runtime-process/stderr.raw',
 'reader-acceptance-v1/reader-acceptance-report.json','reader-acceptance-v1/inspection.json',
 'reader-acceptance-v1/visual-notes.md','reader-acceptance-v1/immutable-freeze.json']:
    if (s/rel).is_file():
        p=s/rel;assert any(x['path']==rel and x['sha256']==sha(p) for x in m['files'])
        q=readable/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
resolution={'kind':'ROOT-later-byte-exact-archive-alias-envelope-not-new-reader-review',
 'archive':str(archive.relative_to(r)),'archive_sha256':sha(archive),
 'members':[{'original_repository_relative':str((s/x['path']).relative_to(r)),
    'member':x['path'],'bytes':x['bytes'],'sha256':x['sha256']} for x in m['files']],
 'scope':'Original actual runtime389checks/0false/36PNG plus independent actual36-PNG review. Original static PATH-node exit1 retained. No new browser, old verdict inheritance or physical touch/production/fullsite/postV-pixel/main/purification claim.',
 'private_exclusions':'Chrome/cache/tmp/profile, guards, fullforeign maps and unlisted files excluded; workstation paths remain exact reference-only strings.'}
(out/'ROOT-original-reference-portable-resolution.v1.json').write_text(json.dumps(resolution,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'archive':str(archive.relative_to(r)),'sha256':sha(archive),'members':77,
 'independent_reader':'PASS_BOUNDED_ISOLATED_READER; required residual0','normal_proof_V':0}))
