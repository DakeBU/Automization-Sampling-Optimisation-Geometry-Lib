# coding: utf-8
import pathlib,json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8');O=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macroscopic-energy-topology-overlay50')
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def encode(x):return (json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
lease=j(O/'lease.json');assert lease['status']=='OPEN' and not lease['compiler_used'];opening=(O/'lease.json').read_bytes();(O/'lease.opening.raw').write_bytes(opening);(O/'lease.opening.lf').write_bytes(lf(opening))
g=j(O/'source-proof-graph.after.json');ops=j(O/'overlay-operations.json');assert len(g['nodes'])==135 and len(g['edges'])==798 and len(ops['operations'])==2
closed=dict(lease,status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),compiler_used=False,final_filesystem_operation='This actual CLOSED lease write after all bindings/run outputs; no subsequent creator filesystem operation',truth='Representation-only repair, no topology self-admission, compiler/proof/claim/canonical edit')
closed_bytes=encode(closed);outputs={}
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name not in ['run.json','lease.json']:
  b=p.read_bytes();outputs[str(p.relative_to(O)).replace('\\','/')]=dict(raw_sha256=sha(b),lf_sha256=sha(lf(b)),raw_bytes=len(b),lf_bytes=len(lf(b)))
run=dict(schema_version='minimal-topology-overlay50-run-v1',status='CREATOR_OVERLAY_CLOSED_AWAITING_DISTINCT_REPAIRED_REVIEW',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),target_lf_sha256='478a899effcc46585270420c4db9c42052a5fcfe3adfd8098ea9548d26c61170',original_negative_raw_lf_sha256='61f4237bd86b2285c51c19c2653282f56c4b863fb1e8481872e9eae8db7888e8',historical_actual_reviewer_closed_lease_sha256='a5481dee0beadcee23b28ab9e8fb86311049991e82fdf075bd2edbdc3ac5dc33',inputs=j(O/'input-bindings.json'),outputs=outputs,operations=ops,actual_own_closed_lease_expected_raw_sha256=sha(closed_bytes),actual_own_closed_lease_expected_lf_sha256=sha(lf(closed_bytes)),historical_vs_current='Original creator/reviewer closed leases are immutable historical inputs; this overlay owns a distinct actual read/write/Python lease, finalized last.',compiler='NOT_STARTED_CLOSED',compiler_used=False,source_statement_mathematics_changed=False,source_rows_changed=False,canonical_files_modified=False,topology_self_admission=False,run_hash_recipe="SHA256 UTF8 json.dumps(entire object minus run_sha256,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)")
run['run_sha256']=sha(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode());runbytes=encode(run);(O/'run.json').write_bytes(runbytes)
result=dict(status='CLOSED_REPRESENTATION_ONLY_AWAITING_DISTINCT_REVIEW',graph_raw_sha256=outputs['source-proof-graph.after.json']['raw_sha256'],run_raw_sha256=sha(runbytes),run_logical_sha256=run['run_sha256'],actual_own_closed_lease_raw_sha256=sha(closed_bytes),capsule_raw_sha256=outputs['capsule.md']['raw_sha256'],nodes=135,edges=798,coverage_unchanged=True)
# FINAL filesystem operation. Printing below accesses only memory.
(O/'lease.json').write_bytes(closed_bytes)
print(json.dumps(result))
