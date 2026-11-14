#!/opt/anaconda3/bin/python
import hashlib,io,json,pathlib,tarfile
BASE=pathlib.Path(__file__).resolve().parent;ROLE=BASE.parent
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
archive=ROLE/'phase5-normal-sourceV-all-portable-original-files.lossless-file-bytes.tar.gz'
envelope=ROLE/'phase5-normal-sourceV-archive-manifest.json'
assert not archive.exists() and not envelope.exists(),'Refuse to overwrite portable archive.'
files=sorted(p for p in BASE.rglob('*') if p.is_file())
outer=[ROLE/'phase5_freeze_execution.json',ROLE/'phase5_freeze_execution.stdout',ROLE/'phase5_freeze_execution.stderr']
for path in outer:assert path.is_file()
records=[]
with tarfile.open(archive,'w:gz',format=tarfile.PAX_FORMAT) as tf:
    for path in files+outer:
        assert 'private-phase5-preservation' not in path.parts
        data=path.read_bytes();relative=str(path.relative_to(ROLE))
        info=tarfile.TarInfo(relative);info.size=len(data);info.mode=0o444;info.mtime=0
        tf.addfile(info,io.BytesIO(data))
        records.append({'archive_path':relative,'original_repo_path':str(path.relative_to(ROOT)),
                        'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
with tarfile.open(archive,'r:gz') as tf:
    members=tf.getmembers();assert len(members)==len(records)
    expected={r['archive_path']:r for r in records}
    for member in members:
        data=tf.extractfile(member).read();row=expected[member.name]
        assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
result={'archive':str(archive.relative_to(ROOT)),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
        'archive_bytes':archive.stat().st_size,'file_count':len(records),'files':records,
        'complete_phase5_files_and_all_three_actual_outer_freeze_streams_included':True,
        'full_private_foreign_snapshots_included':False,
        'explicit_private_exclusion':'.astis/semantic-neutral-20261110/cg_src_7e41d9/private-phase5-preservation',
        'repository_mutations_requiring_exact_Git_carry':['runs/substantive_advances.jsonl','research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json'],
        'original_V_values_may_not_be_changed_by_packager':True,
        'normal_API_calls':1,'no_STAB_global_purification_Goal_acceptance':True}
envelope.write_text(json.dumps(result,indent=2)+'\n')
archive.chmod(0o444);envelope.chmod(0o444)
print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
print('ARCHIVE_MANIFEST_SHA256',hashlib.sha256(envelope.read_bytes()).hexdigest())
