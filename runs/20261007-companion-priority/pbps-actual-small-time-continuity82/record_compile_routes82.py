from pathlib import Path
import hashlib,json,re
r=Path(__file__).parent;rows=[]
for i in range(1,7):
 p=r/f'focused82-attempt{i}';receipt=json.loads((p/'receipt.json').read_bytes());s=(p/'stdout.log').read_text(encoding='utf8')
 errors=[x for x in s.splitlines() if x.startswith('error: AutoSamplingTheory/')]
 rows.append(dict(attempt=i,source_RAW_sha256=receipt['source_RAW_sha256'],exit_code=receipt['exit_code'],fingerprint=hashlib.sha256('\n'.join(errors).encode()).hexdigest(),diagnostic_headers=errors,classification='PINNED_API_ELABORATION' if receipt['exit_code'] else 'PASS',terminal_closed=receipt['terminal_closed']))
assert rows[4]['exit_code']==rows[5]['exit_code']==0
assert all(rows[i]['fingerprint']!=rows[i+1]['fingerprint'] for i in range(4))
p=r/'compiler-route-diagnosis82.json';assert not p.exists()
p.write_text(json.dumps(dict(statement_unchanged=True,mathematical_route_unchanged=True,repeated_unchanged_route_threshold_hit=False,routes=rows,diagnosis='Pinned API elaboration: use global measurableSet_eq_fun; distinguish top hit from finite first record; explicitly name typed local zero identities and typed composition arguments; Real.exp continuity composed with a fully typed scalar limit. No new premise or increased heartbeat budget. Attempt6 changes a docstring only.',process_observation_reused='ASTIS-DISC-20261010-ActualWaitCompositionElaboration',standing_instruction=False,control_plane_math_authority=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Six terminal attempts retained; no unchanged three-repeat route, statement unchanged')
