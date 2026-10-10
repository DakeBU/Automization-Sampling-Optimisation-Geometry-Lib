from pathlib import Path
import ast,hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76')
q=json.loads((r/'focused-first76/receipt.json').read_bytes());assert q['exit_code']==1 and q['terminal_closed']
out=(r/'focused-first76/stdout.log').read_text(encoding='utf8')
assert '247:6: (deterministic) timeout at `isDefEq`' in out
for p in Path('.astis/pbps-recursion76').glob('*.py'):ast.parse(p.read_text(encoding='utf8'),filename=str(p))
pin=lambda p:dict(path=str(p).replace('\\','/'),RAW_sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest())
d=dict(status='DIAGNOSED_API_ELABORATION_ROUTE_CHANGED_NOT_THEOREM_BLOCKED',actual_root_PID=os.getpid(),failure_class='API_BLOCKED',route_fingerprint='joint-next-measurable/direct-ascription-to-full-actual-clock-composition',same_shape_failures=1,failed_receipt=pin(r/'focused-first76/receipt.json'),exact_issue='Expected-type-driven composition unfolded the full literal hittingAfter/integrated hazard during isDefEq and exhausted the fixed 1600000 heartbeat limit at line247.',repair='First construct a typed projection map without the hazard, infer hτmeas.comp hparams in ht0, then ascribe the folded clock type. Do not increase the heartbeat limit or change the statement.',new_analytic_premises=[],header_change=False,source_topology_change=False,retained_native_negatives=True,focused_retry_pending=True,Goal_complete=False)
p=r/'route-diagnosis76.first.json';assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS76 first elaboration timeout diagnosed; fixed-budget inference route changed; all prepared Python parses.')
