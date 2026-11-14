"""Freeze bounded independent assessment only after the final reader assessment is written."""
from runner import *
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--reader-report',required=True);ap.add_argument('--reader-outcome',choices=['pass','blocked'],required=True);args=ap.parse_args()
assert (OUT/'REPORT.md').is_file()
assert '/' not in args.reader_report and args.reader_report.endswith('.json')
browser=json.loads((OUT/args.reader_report).read_text())
native=json.loads((OUT/'native-summary.json').read_text());assert native['kernel_exit']==0 and native['declaration_count']==54
assert browser.get('server_thread_joined') is True
if args.reader_outcome=='pass':
 assert len(browser['contexts'])==4
 assert not browser['page_errors'] and not browser['failed_requests'] and not browser['http_errors'] and not browser.get('overflow_events',[])
def hashfile(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()
rows=[];excluded=[]
destbase='research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/native-review/variance_native_61d0/originals/'
omit={'portable-manifest.json','local-file-manifest.json','SEAL.json','postseal-envelope.json'}
for p in sorted(OUT.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(OUT).as_posix()
 if rel in omit or rel.startswith(('commands/freeze-','__pycache__/')) or '/__pycache__/' in rel:continue
 row={'source':str(p),'relative_source':rel,'bytes':p.stat().st_size,'sha256':hashfile(p)}
 reason=None
 if rel=='bootstrap-1.stdout':reason='unrelated full repository path-name inventory, including foreign/control names: local only, not portable content'
 elif rel.startswith('local-only/') or ('/inventory-kernel-' in rel and p.name=='stdout' and row['bytes']>8_000_000):reason='large proof dump: local lossless preservation only'
 elif '/empty-astis-output/' in rel:reason='fresh compiler output; hashes in compile-results; source bytes and native receipts are portable'
 if reason:row['excluded_from_portable_reason']=reason;excluded.append(row)
 else:row['destination']=destbase+rel;rows.append(row)
local={'schema':1,'files':rows+excluded,'not_complete_historical_tool_transcript_capture':'See native-REPORT.md and environment-incidents.json; unrecorded wrapper stdout/stderr were not invented.'}
(OUT/'local-file-manifest.json').write_text(json.dumps(local,indent=2))
portable={'schema':1,'files':rows,'excluded_local_only':excluded,'destination_root':destbase,'self_and_seal':'postseal-envelope.json separately indexes this manifest and SEAL to avoid self-hash recursion'}
(OUT/'portable-manifest.json').write_text(json.dumps(portable,indent=2))
seal={'schema':1,'verifier':'variance_native_61d0','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_math_compiled_commit':COMMIT,'reader_author_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae','reader_report':args.reader_report,'reader_outcome':args.reader_outcome,'native_outcome':'pass','final_metadata_four_gates':'not run','normalV':'not run','scope':'Native and bounded selected production reader only; public API/main/oracle/cost/integration/purification remain pending','portable_manifest_sha256':hashfile(OUT/'portable-manifest.json'),'local_manifest_sha256':hashfile(OUT/'local-file-manifest.json'),'report_sha256':hashfile(OUT/'REPORT.md'),'native_summary_sha256':hashfile(OUT/'native-summary.json'),'browser_report_sha256':hashfile(OUT/args.reader_report),'operator_boundary':'ROOT operated the exact independent foreground browser checker after visible approval; variance_native_61d0 independently assessed receipts and screenshots.'}
(OUT/'SEAL.json').write_text(json.dumps(seal,indent=2))
print(json.dumps({'portable_files':len(rows),'local_only_files':len(excluded),'seal_sha256':hashfile(OUT/'SEAL.json'),'portable_manifest_sha256':seal['portable_manifest_sha256'],'native_outcome':'pass','reader_outcome':args.reader_outcome},indent=2))
