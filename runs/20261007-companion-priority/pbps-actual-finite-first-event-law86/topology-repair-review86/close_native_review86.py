from pathlib import Path
import datetime, hashlib, json
R=Path('E:/Samplinglib'); O=Path(__file__).parent
S=R/'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86'
B=R/'runs/20261007-companion-priority/pbps-path-law-preread86'
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text('utf8'))
def put(n,x):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs=[R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html',B/'source-proof-graph86.reviewed-effective.json',B/'source-inventory86.reviewed-effective.json']+[S/n for n in ['topology-additive-proposal86.json','source-proof-graph86.exhaustive-successor.json','source-inventory86.exhaustive-successor.json','topology-successor-freeze86.json']]
freeze=read(S/'topology-successor-freeze86.json')
for k in ['proposal','source_graph_successor','source_inventory_successor']:
 p=R/freeze[k]['path'];assert pin(p)['raw_sha256']==freeze[k]['raw_sha256']
g=read(S/'source-proof-graph86.exhaustive-successor.json')
c=read(O/'source-proof-graph86.single-edge-proposed-successor.json')
assert c['nodes']==g['nodes'] and c['edges'][:-1]==g['edges'] and c['junctions']==g['junctions']
assert c['edges'][-1]==read(O/'minimal-strict-overlay86.json')['operations'][0]['value']
assert read(O/'audit-attempt1.receipt.json')['exit_code']==1
assert read(O/'audit-attempt2.receipt.json')['exit_code']==0
put('typed-audit-script-diagnosis86.json',dict(status='REPAIRED_REVIEWER_SCRIPT_ONLY_ORIGINAL_NEGATIVE_RETAINED',created_utc=now,failed_script=pin(O/'audit_exact_proposal86.py'),negative_receipt=pin(O/'audit-attempt1.receipt.json'),failure='SyntaxError: extra closing parenthesis in overlay construction; script did not execute or emit decisions.',successor_script=pin(O/'audit_exact_proposal86.attempt2.py'),positive_receipt=pin(O/'audit-attempt2.receipt.json'),mathematical_or_source_repair=False,notes='Separate immutable successor also freezes noncanonical strict graph candidate and its unchanged-inventory reference, as requested. Original private-extract naming diagnosis retained separately.'))
public=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and not p.name.startswith('.private.') and p.name not in ['run-manifest86.json','closed-RAW-manifest86.json']]
private=[dict(**pin(p),staging='EXCLUDED_PRIVATE_SOURCE_EXTRACT') for p in sorted(O.glob('.private.*'))]
put('run-manifest86.json',dict(schema='astis.native-independent-exact-topology-review.v1',created_utc=now,reviewer_id='/root/exact_verify77',status='CLOSED_CONDITIONAL_ACCEPT_WITH_ONE_REQUIRED_DISTINCTLY_REVIEWED_EDGE',actual_external_inputs=[pin(p) for p in inputs],owned_public_artifacts=public,excluded_private_artifacts=private,terminal_receipts=[pin(O/'audit-attempt1.receipt.json'),pin(O/'audit-attempt2.receipt.json')],native_source_order=read(O/'evidence86.json')['chronology'],checked_parts='Original additive seven inventory items, one node, four edges; all 72 source atomic dispositions and 56 normalized legacy anchors; unchanged prior topology and future OPEN/OR boundaries.',remaining_exact_repair='E86-R76 G86-08 -> G86-38; distinct reviewer must accept exact bytes before any canonical adoption.',ownership='Only topology-repair-review86 written. No canonical source graph, inventory, source proof, production, shared metadata, cell, ledger, or VERIFIED writes.',manifest_contract='Noncircular: run pins preexisting owned artifacts; authoritative closed manifest pins this run and all other owned artifacts, excluding only itself. No synthetic tool/model trajectory claimed.'))
all_public=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and not p.name.startswith('.private.') and p.name!='closed-RAW-manifest86.json']
put('closed-RAW-manifest86.json',dict(schema='astis.closed-raw-manifest.v1',created_utc=now,reviewer_id='/root/exact_verify77',status='CLOSED',frozen_current_inputs=[pin(p) for p in inputs],owned_artifacts=all_public,excluded_private_artifacts=private,self_hash_policy='Authoritative manifest excludes itself to avoid a circular hash; its RAW is reported in terminal/parent message.',source_only=True,canonical_mutation=False,distinct_review_pending=True))
for collection in ['frozen_current_inputs','owned_artifacts','excluded_private_artifacts']:
 for p in read(O/'closed-RAW-manifest86.json')[collection]:assert pin(R/p['path'])['raw_sha256']==p['raw_sha256']
print(json.dumps(dict(status='CLOSED_REHASH_PASS',decision=pin(O/'decision86.json'),manifest=pin(O/'closed-RAW-manifest86.json'),run=pin(O/'run-manifest86.json'),overlay=pin(O/'minimal-strict-overlay86.json'),candidate_graph=pin(O/'source-proof-graph86.single-edge-proposed-successor.json'),candidate_freeze=pin(O/'single-edge-proposed-freeze86.json'),checked_current_inputs=len(inputs),public_owned_artifacts=len(all_public),private_excluded=len(private))))
