import datetime,hashlib,json,pathlib
from record import ROOT,EXPECTED_HEAD,MATH_HEAD,sha
DEST='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/native-review/psd_native_7b31/held-gates/'
excluded={'originals-manifest.json','seal.json','portable-originals-manifest.json','portable-originals-manifest.sha256'}
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(ROOT).as_posix()
    if rel in excluded or '__pycache__/' in rel:continue
    files.append({'source':str(p),'relative_path':rel,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
manifest={'schema_version':1,'phase':'final-held-metadata-gates','verifier':'psd_native_7b31','held_HEAD':EXPECTED_HEAD,'mathematical_candidate':MATH_HEAD,'result':'FAIL_STOPPED_AT_PUBLICATION','files':files,'self_hash_exclusions':sorted(excluded),'final_freeze_envelope':'Post-seal receipt and raw output are separately transferable; excluded from recursive self-hashing.'}
mp=ROOT/'originals-manifest.json';mp.write_text(json.dumps(manifest,indent=2)+'\n')
gate=json.loads((ROOT/'gate-results.json').read_text());assert len(gate)==1 and gate[0]['exit']==1
receipt=json.loads((ROOT/gate[0]['receipt']).read_text());assert receipt['shared_HEAD_before']==receipt['shared_HEAD_after']==EXPECTED_HEAD
seal={'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'final-held-metadata-gates','verifier':'psd_native_7b31','held_HEAD':EXPECTED_HEAD,'mathematical_candidate':MATH_HEAD,'result':'FAIL_STOPPED_AT_PUBLICATION','executed_gate_count':1,'publication_exit':1,'semantic':'NOT_RUN','contributor':'NOT_RUN','frontier':'NOT_RUN','normalV_credit':False,'source_fidelity_verdict':None,'native_browser_rerun':False,'preflight_local_implementation_failure_retained':True,'report_sha256':sha((ROOT/'REPORT.md').read_bytes()),'originals_manifest_sha256':sha(mp.read_bytes()),'gate_results_sha256':sha((ROOT/'gate-results.json').read_bytes()),'portable_destination_prefix':DEST}
sp=ROOT/'seal.json';sp.write_text(json.dumps(seal,indent=2)+'\n')
entries=[{'source':f['source'],'destination':DEST+f['relative_path'],'bytes':f['bytes'],'sha256':f['sha256']} for f in files]
for p in [mp,sp]:entries.append({'source':str(p),'destination':DEST+p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
pp=ROOT/'portable-originals-manifest.json';pp.write_text(json.dumps({'schema_version':1,'phase':'final-held-metadata-gates','held_HEAD':EXPECTED_HEAD,'entries':entries,'self_excluded':True},indent=2)+'\n')
(ROOT/'portable-originals-manifest.sha256').write_text(sha(pp.read_bytes())+'  portable-originals-manifest.json\n')
print(json.dumps({'phase_root':str(ROOT),'result':seal['result'],'report_sha256':seal['report_sha256'],'originals_manifest_sha256':seal['originals_manifest_sha256'],'seal_sha256':sha(sp.read_bytes()),'portable_manifest_sha256':sha(pp.read_bytes()),'portable_entries':len(entries),'portable_bytes':sum(f['bytes'] for f in entries),'portable_destination_prefix':DEST},indent=2))
