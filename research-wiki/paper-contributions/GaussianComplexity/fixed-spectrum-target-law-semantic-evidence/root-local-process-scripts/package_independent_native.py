from pathlib import Path
import sys,json
sys.dont_write_bytecode=True;sys.path.insert(0,'.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact,put_new,sha
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
D=W/'independent-native-reader-4b8e73';E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-law-semantic-evidence')
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
assert sha((D/'frozen-manifest.json').read_bytes())=='f9bc3304954f52d129e7e04074b24b22bc5c92db107058a772faf548b136b6a5'
assert sha((D/'frozen-receipt.json').read_bytes())=='40b2e7507b53735bd8cc21a1162a7e70fafaa03cc13806e0f8c7ddfe77ed975a'
m=json.loads((D/'frozen-manifest.json').read_bytes());files={}
for r in m['files']:
    p=D/r['path'];assert not p.is_symlink();b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'] and p.stat().st_mode&0o777==0o444,p
    files[r['path']]=b
for n in ['frozen-manifest.json','frozen-receipt.json','frozen-receipt.sha256']:
    p=D/n;assert p.stat().st_mode&0o777==0o444;files[n]=p.read_bytes()
assert set(files)=={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and not p.is_symlink()}
assert sha(files['independent-judgement.json'])=='de2714b49f2501d815428f1a6e6e22913284328463da37078c2150a2e2d0a8ad'
j=json.loads(files['independent-judgement.json']);assert j['verified_commit']=='8ee639d3aced826aa5b4e39fa6f8bedd3b830327' and j['whole_module_read']['owned_count']==2 and j['bounded_gates']['publication_errors']==[]
record=archive_exact(files,E/'independent-native-fullmodule-static.lossless-file-bytes.tar.gz')
record.update({'original_actor':'/root/targetlaw_module_reader_4b8e73','checked_mathematical_commit':j['verified_commit'],'original_freeze_sha256':sha(files['frozen-receipt.json']),'all89_manifested_original_regular_files_plus3_freeze_files_exact':True,'includes_own4_fresh_compiler_cache_files_as_separately_typed_original_bytes':True,'dependency_symlinks_and_their_cached_targets_not_archived':True,'source_verdict_or_browser_global_authority':False,'root_packaging_diagnostic':'First carry rejected exact inventory because original frozen-receipt.sha256 was initially omitted from selected set. Read actual set difference, include exact original hash note, no original edits or native rerun. First failed carry receipt retained separately.'})
put_new(E/'independent-native-fullmodule-static.archive-manifest.json',dump(record))
put_new(E/'independent-native-judgement.raw.json',files['independent-judgement.json'])
print(json.dumps({'files_byte_exact':len(files),'archive_sha256':record['sha256'],'unchanged_original_native_judgement':True,'sourceV':False}))
