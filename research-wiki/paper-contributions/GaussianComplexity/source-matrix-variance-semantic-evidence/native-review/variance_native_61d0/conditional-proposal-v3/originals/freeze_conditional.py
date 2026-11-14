from pathlib import Path
import json,hashlib,datetime
P=Path('/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261113/variance_native_61d0');C=P/'conditional-reader-v3'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((C/'browser-report.json').read_text());a=json.loads((C/'assessment.json').read_text());assert a['outcome']=='CONDITIONAL_PROPOSAL_PASS'
assert len(r['contexts'])==4 and len(r['source_checks'])==8 and not r['overflow_events'] and r['server_thread_joined']
assert sha(P/'SEAL.json')=='8a76e39bd0c097f3ea54f95afe07d142354d968437fe83c7a11bf04f630fdecd'
dest='research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/native-review/variance_native_61d0/conditional-proposal-v3/originals/'
rows=[]
def add(p,rel):
 rows.append({'source':str(p),'destination':dest+rel,'relative_source':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':sha(p)})
for p in sorted(C.rglob('*')):
 if p.is_file() and p.name not in {'portable-manifest.json','SEAL.json','postseal-envelope.json'}:add(p,p.relative_to(C).as_posix())
for f in ['run_browser_check.py','check_browser_proposal_v3.py','runner.py']:add(P/f,'runtime/'+f)
for f in ['table-scroll.patch','proposal.json','proof-readers.css.before','proof-readers.css.proposed']:add(P/'production-proposal'/f,'production-proposal/'+f)
for label in ['browser-proposal-v3','chrome-version-proposal-v3','proposal-v3-canonical-css-at-operation']:
 for f in ['start.json','result.json','stdout','stderr']:add(P/'commands'/label/f,'commands/'+label+'/'+f)
m={'schema':1,'scope':'UNAPPLIED PRODUCTION PATCH PROTOTYPE ONLY; original reader FAIL unchanged','files':rows,'destination_root':dest,'postseal_index':'postseal-envelope.json separately indexes this manifest, seal and freeze command receipt; no self-hash recursion','large_proof_dumps':'none included; original native dump remains local-only'}
(C/'portable-manifest.json').write_text(json.dumps(m,indent=2))
s={'schema':1,'assessor':'variance_native_61d0','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'outcome':'CONDITIONAL_PROPOSAL_PASS','canonical_integration_status':'UNAPPLIED','original_reader_outcome':'FAIL, immutable','original_fail_seal_sha256':sha(P/'SEAL.json'),'math_compiled_commit':'e654e98642350a615c473bc8190fbc1d47fe52bd','reader_author_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae','browser_operation_HEAD':'8463958bde34c774163ac4fbefa009daeab39d32','actual_browser_exit':0,'wrapper_sha256':sha(P/'run_browser_check.py'),'checker_sha256':sha(P/'check_browser_proposal_v3.py'),'proposed_css_sha256':'60acf59734f5f63567078cc8f442ca04f6e9e661acac745884f094ccc941d8b9','patch_sha256':'2442d520f5888f665b8bd76777334d36a3e3346888c4c9cb309ae891280a2bff','report_sha256':sha(C/'REPORT.md'),'assessment_sha256':sha(C/'assessment.json'),'portable_manifest_sha256':sha(C/'portable-manifest.json'),'four_final_metadata_gates':'not run','V_normalV':'not run or decided','operator_boundary':'ROOT operated the fixed independent checker; variance_native_61d0 independently assessed actual report, computed CSS and screenshots.'}
(C/'SEAL.json').write_text(json.dumps(s,indent=2))
print(json.dumps({'files':len(rows),'portable_bytes':sum(x['bytes'] for x in rows),'seal_sha256':sha(C/'SEAL.json'),'manifest_sha256':sha(C/'portable-manifest.json'),'report_sha256':sha(C/'REPORT.md'),'outcome':'CONDITIONAL_PROPOSAL_PASS; ORIGINAL_READER_FAIL_UNCHANGED'},indent=2))
