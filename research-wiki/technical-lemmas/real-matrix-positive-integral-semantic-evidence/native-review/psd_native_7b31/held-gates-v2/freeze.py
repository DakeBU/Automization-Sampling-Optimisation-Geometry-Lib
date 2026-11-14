import datetime,json
from record import ROOT,EXPECTED_HEAD,PARENT_HEAD,MATH_HEAD,sha
DEST='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/native-review/psd_native_7b31/held-gates-v2/'
excluded={'originals-manifest.json','seal.json','portable-originals-manifest.json','portable-originals-manifest.sha256'}
gates=json.loads((ROOT/'gate-results.json').read_text());assert [r['gate'] for r in gates]==['publication','semantic','contributor','frontier']
for r in gates:
    receipt=json.loads((ROOT/r['receipt']).read_text());assert receipt['exit']==0 and receipt['shared_HEAD_before']==receipt['shared_HEAD_after']==EXPECTED_HEAD
    d=(ROOT/r['receipt']).parent
    for kind in ['stdout','stderr']:assert sha((d/receipt[kind+'_file']).read_bytes())==receipt[kind+'_sha256']
    assert receipt['stderr_bytes']==0
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(ROOT).as_posix()
    if rel in excluded or '__pycache__/' in rel:continue
    files.append({'source':str(p),'relative_path':rel,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
manifest={'schema_version':1,'phase':'final-held-metadata-gates-v2','verifier':'psd_native_7b31','held_HEAD':EXPECTED_HEAD,'parent_failed_held_HEAD':PARENT_HEAD,'mathematical_candidate':MATH_HEAD,'result':'PASS_FOUR_ACTUAL_ZERO_EXITS','files':files,'self_hash_exclusions':sorted(excluded),'final_freeze_envelope':'Post-seal command receipt and raw output are separately transferable; excluded from recursive self-hashing.'}
mp=ROOT/'originals-manifest.json';mp.write_text(json.dumps(manifest,indent=2)+'\n')
seal={'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'final-held-metadata-gates-v2','verifier':'psd_native_7b31','held_HEAD':EXPECTED_HEAD,'parent_failed_held_HEAD':PARENT_HEAD,'mathematical_candidate':MATH_HEAD,'result':'PASS_FOUR_ACTUAL_ZERO_EXITS','executed_gate_count':4,'all_actual_exits_zero':True,'stderr_all_empty':True,'normalV_credit':False,'source_fidelity_verdict':None,'native_browser_source_math_rerun':False,'v1_real_and_verifier_implementation_failures_retained':True,'report_sha256':sha((ROOT/'REPORT.md').read_bytes()),'originals_manifest_sha256':sha(mp.read_bytes()),'gate_results_sha256':sha((ROOT/'gate-results.json').read_bytes()),'portable_destination_prefix':DEST}
sp=ROOT/'seal.json';sp.write_text(json.dumps(seal,indent=2)+'\n')
entries=[{'source':f['source'],'destination':DEST+f['relative_path'],'bytes':f['bytes'],'sha256':f['sha256']} for f in files]
for p in [mp,sp]:entries.append({'source':str(p),'destination':DEST+p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
pp=ROOT/'portable-originals-manifest.json';pp.write_text(json.dumps({'schema_version':1,'phase':'final-held-metadata-gates-v2','held_HEAD':EXPECTED_HEAD,'entries':entries,'self_excluded':True},indent=2)+'\n')
(ROOT/'portable-originals-manifest.sha256').write_text(sha(pp.read_bytes())+'  portable-originals-manifest.json\n')
print(json.dumps({'phase_root':str(ROOT),'result':seal['result'],'report_sha256':seal['report_sha256'],'originals_manifest_sha256':seal['originals_manifest_sha256'],'seal_sha256':sha(sp.read_bytes()),'portable_manifest_sha256':sha(pp.read_bytes()),'portable_entries':len(entries),'portable_bytes':sum(f['bytes'] for f in entries),'portable_destination_prefix':DEST},indent=2))
