# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib,json,sys,datetime
sys.stdout.reconfigure(encoding='utf-8')
BASE=Path('E:/Samplinglib/runs/20261007-companion-priority');O=BASE/'pbps-outer-gradient-topology-overlay49';N=BASE/'pbps-outer-gradient-source-topology-review49';S=BASE/'pbps-outer-gradient-sourcegraph49'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def dump(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def read(p): return json.loads(p.read_text(encoding='utf-8'))
p=N/'coverage.byte-checks.json';b=p.read_bytes();label='negative-coverage.byte-checks.json'
(O/(label+'.raw')).write_bytes(b);(O/(label+'.lf')).write_bytes(lf(b))
binds=read(O/'input-bindings.json');binds.append(dict(id=label,path=str(p),role='third unchanged original independent negative evidence artifact; raw pin without semantic expansion',raw_sha256=sha(b),lf_sha256=sha(lf(b)),raw_bytes=len(b),lf_bytes=len(lf(b)),raw_snapshot=label+'.raw',lf_snapshot=label+'.lf'));(O/'input-bindings.json').write_bytes(dump(binds))
contract=read(O/'sourcecontract.json');contract['original_negative_evidence']=[dict(path=str(N/n),raw_sha256=sha((N/n).read_bytes()),lf_sha256=sha(lf((N/n).read_bytes()))) for n in ['source-topology-review.json','direct-call.checks.json','coverage.byte-checks.json']]
contract['known_exposures'].append('Authorized bounded negative-review-folder filename listing surfaced only frozen inputs/receipt/helper names; no new mathematical proof body was selected.')
(O/'sourcecontract.json').write_bytes(dump(contract))
# Verify every immutable whole-file/fragment snapshot again before closing; no mathematics admission.
for x in binds:
 if 'whole_raw_sha256' in x:
  pb=Path(x['path']).read_bytes();assert sha(pb)==x['whole_raw_sha256']
  continue
 current=Path(x['path']).read_bytes()
 # Our actual lease is intentionally OPEN until the final write below.
 assert sha(current)==x['raw_sha256'],x['id']
 assert sha(lf(current))==x['lf_sha256'],x['id']
 assert (O/x['raw_snapshot']).read_bytes()==current
 assert (O/x['lf_snapshot']).read_bytes()==lf(current)
g=read(O/'source-proof-graph.after.json');g0=read(S/'source-proof-graph.json');assert g['nodes']==g0['nodes']
assert [i for i in range(280) if g['edges'][i]!=g0['edges'][i]]==[244,252,253,254]
assert len(g['edges'])==296
lease=read(O/'lease.json');assert all(lease[k]=='OPEN' for k in ['read','write','python']) and lease['compiler']=='CLOSED' and not lease['compiler_used']
closed=dict(lease);closed.update(status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='source-only representation overlay; final filesystem operation closes actual leases',compiler_used=False,proof_search=False,shared_mutation=False)
closed_bytes=dump(closed)
cap=(O/'capsule.md').read_text(encoding='utf-8');cap+='\n`run.json` binds82 raw/LF input records, all prepared output files and the expected exact CLOSED lease bytes. Hashes use SHA256 of exact file bytes; LF normalization replaces CRLF and isolated CR by LF. The run excludes itself and the mutable lease from its output hash map to avoid circularity, and separately binds the final CLOSED lease SHA. No filesystem operations follow the lease-close write.\n';(O/'capsule.md').write_bytes(cap.encode('utf-8'))
files={}
for f in sorted(O.iterdir(),key=lambda f:f.name):
 if f.is_file() and f.name not in ['run.json','lease.json']:
  data=f.read_bytes();files[f.name]=dict(raw_sha256=sha(data),lf_sha256=sha(lf(data)),raw_bytes=len(data),lf_bytes=len(lf(data)))
run=dict(schema_version='minimal-sourcegraph-overlay49-run-v1',status='CREATOR_OVERLAY_CLOSED_AWAITING_DISTINCT_REVIEW',truth='representation repair only; no theorem admission or proof',target_lf_sha256=contract['target_lf_sha256'],target_lf_bytes=1795,original_graph_sha256=sha((S/'source-proof-graph.json').read_bytes()),original_negative_evidence=contract['original_negative_evidence'],output_files=files,expected_closed_lease_sha256=sha(closed_bytes),hash_recipe=dict(file_hash='SHA256 exact bytes',lf_normalization='replace CRLF by LF, then isolated CR by LF',run_hash='SHA256 exact UTF8 LF bytes of run.json; no self-hash field',output_selection='all prepared files sorted by filename excluding run.json and lease.json; final lease bound separately',whole_vs_fragment='input bindings explicitly distinguish primary whole hash from selected row hash; original selected provider whole hashes are separate from unchanged fragment hashes'),counts=dict(nodes=78,edge_records=296,original_edge_positions=280,explicitly_reclassified_original_edges_one_based=[245,253,254,255],appended_references=16,physical_selected_rows=229,NODE=146,EXCLUDED=83,callers=167,configured_tokens=160,excluded_callers=2,excluded_tokens=2,raw_selected_unrelated_proof_count=1,semantic_proof_expansion_count=0,input_bindings=len(binds)),compiler_used=False,self_topology_admission=False,originals_verified_unchanged=True,lease_close_is_final_filesystem_operation=True)
run_bytes=dump(run);(O/'run.json').write_bytes(run_bytes)
result=dict(status=run['status'],run_sha256=sha(run_bytes),graph_after_sha256=files['source-proof-graph.after.json']['raw_sha256'],delta_sha256=files['overlay-delta.json']['raw_sha256'],capsule_sha256=files['capsule.md']['raw_sha256'],closed_lease_sha256=sha(closed_bytes),all_actual_leases='CLOSED',compiler_used=False,counts=run['counts'],negative_original_sha256=contract['negative_original_sha256'])
# FINAL filesystem operation: closes real read/write/Python leases, compiler remained CLOSED unused.
(O/'lease.json').write_bytes(closed_bytes)
print(json.dumps(result,ensure_ascii=False,indent=2))
