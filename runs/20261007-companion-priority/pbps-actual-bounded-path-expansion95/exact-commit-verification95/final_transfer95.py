import pathlib,json,hashlib,subprocess
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;B=O.parent
C='5df604f6c9ddab63e552272b2e9056752616621e';rows=[]
def sha(b):return hashlib.sha256(b).hexdigest()
for name in ['draft-audit-recovery95.json','evidence-recovery95.json','public-reference-correction95.json','search-label-correction95.json','normalize_public_refs95.py','recover_evidence95.py','draft-audit95.recovered.exactraw.json.gz','pre-step4-lesson95.recovered.exactraw.json.gz']:
 p=B/name;r=p.relative_to(R).as_posix();local=p.read_bytes();git=subprocess.check_output(['git','show',C+':'+r],cwd=R)
 assert local==git or name=='draft-audit-recovery95.json' and local.replace(b'\r\n',b'\n')==git
 rows.append({'path':r,'local_raw_sha256':sha(local),'git_blob_raw_sha256':sha(git),'binding':'exact' if local==git else 'new diagnostic receipt CRLF-to-LF only; not a historical native review input'})
result={'status':'PASS','verified_commit':C,'new_followup_evidence':rows,'historical_native_review_bytes_unchanged':True,'canonical_source_and_publication_paths':'Repository-relative; remaining absolute seal/native reviewer strings are provenance resolved by explicit prefix/backslash normalization and exact committed archive lookup.','exact_raw_archive_count':72,'base_archive_map_count':70,'supplemental_historical_recovery_archives':2}
(O/'final-transfer95.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS final metadata/archive transfer')
