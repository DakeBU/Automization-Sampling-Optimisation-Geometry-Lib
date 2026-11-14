import datetime,hashlib,json,os,pathlib,sys
from record import ROOT,COMMIT,sha
DEST='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/native-review/psd_native_7b31/originals/'
def filehash(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
    return h.hexdigest()
def local_only(rel):
    return rel.startswith('candidate/out/') or rel.endswith('.dump.gz') or '__pycache__/' in rel or rel.endswith('.pyc')
excluded={'originals-manifest.json','seal.json','portable-originals-manifest.json','portable-originals-manifest.sha256'}
files=[];local=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(ROOT).as_posix()
    if rel in excluded:continue
    row={'source':str(p),'relative_path':rel,'bytes':p.stat().st_size,'sha256':filehash(p)}
    if local_only(rel):local.append(row)
    else:files.append(row)
manifest={'schema_version':1,'verifier':'psd_native_7b31','candidate_commit':COMMIT,'files':files,'local_only_not_for_export':local,'exclusions':['This manifest and its seal/transfer manifest are excluded from their own inventory to avoid recursive hashing.','The final freeze command receipt is a separately transferable post-seal envelope, not mathematical evidence.'],'bootstrap_raw_capture_qualified':True}
mp=ROOT/'originals-manifest.json';mp.write_text(json.dumps(manifest,indent=2)+'\n')
seal={'schema_version':1,'phase':'independent-native-kernel-bounded-reader','verifier':'psd_native_7b31','candidate_commit':COMMIT,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'originals_manifest_sha256':filehash(mp),'report_sha256':filehash(ROOT/'REPORT.md'),'native_summary_sha256':filehash(ROOT/'native-summary.json'),'browser_report_sha256':filehash(ROOT/'browser-report.json'),'native_result':'PASS','bounded_reader_result':'PASS','archival_completeness':'QUALIFIED_BOOTSTRAP_TOOL_ONLY_DISCOVERY','source_fidelity_verdict':None,'normalV_authorized':False,'full_R9_T_credit':False,'portable_destination_prefix':DEST,'portable_file_count_excluding_manifest_and_seal':len(files),'local_large_dumps_exported':False}
sp=ROOT/'seal.json';sp.write_text(json.dumps(seal,indent=2)+'\n')
portable=[]
for row in files+[{'source':str(mp),'relative_path':'originals-manifest.json','bytes':mp.stat().st_size,'sha256':filehash(mp)},{'source':str(sp),'relative_path':'seal.json','bytes':sp.stat().st_size,'sha256':filehash(sp)}]:
    portable.append({'source':row['source'],'destination':DEST+row['relative_path'],'bytes':row['bytes'],'sha256':row['sha256']})
pp=ROOT/'portable-originals-manifest.json';pp.write_text(json.dumps({'schema_version':1,'source_root':str(ROOT),'destination_prefix':DEST,'candidate_commit':COMMIT,'entries':portable,'local_only_dumps_exported':False,'self_excluded':True},indent=2)+'\n')
(ROOT/'portable-originals-manifest.sha256').write_text(filehash(pp)+'  portable-originals-manifest.json\n')
print(json.dumps({'report_sha256':filehash(ROOT/'REPORT.md'),'originals_manifest_sha256':filehash(mp),'seal_sha256':filehash(sp),'portable_manifest_sha256':filehash(pp),'portable_entries':len(portable),'portable_bytes':sum(r['bytes'] for r in portable),'portable_destination_prefix':DEST,'large_dumps_local_only':True},indent=2))
