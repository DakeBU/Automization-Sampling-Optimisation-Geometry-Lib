# coding: utf-8
import pathlib,json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
O=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macroscopic-energy-sourcegraph50')
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def encoded(x):return (json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
# All reads and output construction occur before the actual final lease write.
lease=j(O/'lease.json');assert lease['status']=='OPEN' and lease['compiler']=='CLOSED' and not lease['compiler_used']
(O/'lease.opening.raw').write_bytes((O/'lease.json').read_bytes())
(O/'lease.opening.lf').write_bytes(lf((O/'lease.json').read_bytes()))
count=j(O/'counts.json');g=j(O/'source-proof-graph.json');assert len(g['nodes'])==count['nodes'] and len(g['edges'])==count['edges']
assert not j(O/'lexical-inventory.json')['unresolved']
closed=dict(lease,status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),compiler_used=False,final_filesystem_operation='write this exact actual CLOSED lease after run/capsule/input/output pins; no subsequent filesystem operations by creator',truth='Source-only creator; no topology admission, compiler, theorem claim, proof or canonical editing')
closed_bytes=encoded(closed)
outputs={}
for path in sorted(O.rglob('*')):
 if path.is_file() and path.name not in {'run.json','lease.json'}:
  b=path.read_bytes();outputs[str(path.relative_to(O)).replace('\\','/')]=dict(raw_sha256=sha(b),lf_sha256=sha(lf(b)),raw_bytes=len(b),lf_bytes=len(lf(b)))
run=dict(schema_version='pbps-sourcegraph50-run-v1',status='CREATOR_CLOSED_AWAITING_DISTINCT_SOURCE_TOPOLOGY_REVIEW',scope='Source-only independent graph; original49 repaired prefix plus bounded B1-B9/operator/norm source branch. No50implementation proof/compiler/claim; no selfadmission.',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),target_lf_sha256='478a899effcc46585270420c4db9c42052a5fcfe3adfd8098ea9548d26c61170',counts=count,inputs=j(O/'input-bindings.json'),output_files=outputs,actual_closed_lease_expected_raw_sha256=sha(closed_bytes),actual_closed_lease_expected_lf_sha256=sha(lf(closed_bytes)),closed_lease_recipe='Actual identical bytes written as final filesystem operation; not a mere planned closing record.',source_only_repaired49_topology=dict(raw_lf_sha256='98e2cedb5884783202748f9f8aa684edb3a84af8679bfb5bcd32f05a433e08fc',logical_review_run='d44b6c7e6b1c40c55577623b0ea95d12adefe1234be8dd226ec6abf79f94cfbd',original_negative_raw_lf_sha256='73497919a8693a4e8e2b36bf9f66a20af9fc006f94becbd7cc185270f581f417',implementation_finalsource_verdict_read=False),creator_checks='Raw/LF identity, interval coverage, source-prefix and exact reference byte bookkeeping only; no topology or mathematical theorem admission.',failed_attempts=['inspect-graph.py default gbk UnicodeDecodeError; UTF8 replacement separate script retained.','build.attempt0.py HTMLParser.offset name collision; retained unchanged.','build.attempt1.py initial L2inner136 blank; real header137 repaired before freeze.','Lexical prime completion temporarily exposed unresolved local s-prime and inverse-image superscript; diagnosed syntax/binders, corrected before freeze.'],compiler_used=False,canonical_files_modified=False,full_paper_completion=False,run_hash_recipe="SHA256 UTF8 json.dumps(entire object minus run_sha256,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)")
run['run_sha256']=sha(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
run_bytes=encoded(run);(O/'run.json').write_bytes(run_bytes)
result=dict(status='CLOSED_SOURCE_ONLY_AWAITING_DISTINCT_TOPOLOGY',run_logical_sha256=run['run_sha256'],run_raw_sha256=sha(run_bytes),graph_raw_sha256=outputs['source-proof-graph.json']['raw_sha256'],capsule_raw_sha256=outputs['capsule.md']['raw_sha256'],actual_closed_lease_raw_sha256=sha(closed_bytes),counts=count)
# FINAL filesystem operation. Nothing below reads, hashes disk files, or writes files.
(O/'lease.json').write_bytes(closed_bytes)
print(json.dumps(result,ensure_ascii=False))
