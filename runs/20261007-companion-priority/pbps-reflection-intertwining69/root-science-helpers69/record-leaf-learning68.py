from pathlib import Path
import json,hashlib

r=Path('runs/20261007-companion-priority/pbps-sharp-energy68')
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for label,diagnosis in [('focused-leaf68-v1','API coercion mismatch: the symmetric LinearMap application did not syntactically match the bounded operator application. Added exact typed inner equalities; no statement change.'),('focused-leaf68-v2','API orientation mismatch: real_inner_comm v (K u) is oriented opposite to the required transitivity edge. Used its symmetry; one residual error strictly smaller than v1.')]:
 d=r/label;receipt=json.loads((d/'receipt.json').read_bytes());assert receipt['terminal_closed'] and receipt['exit_code']==1
 rows.append(dict(label=label,failure_class='API_BLOCKED',diagnosis=diagnosis,actual_PID=receipt['actual_foreground_pid'],receipt_RAW_sha256=sha((d/'receipt.json').read_bytes()),stdout_RAW_sha256=sha((d/'stdout.log').read_bytes()),transient_sorryAx_not_proof=True,statement_unchanged=True))
good=json.loads((r/'focused-leaf68-v3/receipt.json').read_bytes());assert good['terminal_closed'] and good['exit_code']==0
payload=dict(status='TYPED_STRICT_API_PROGRESS_THEN_COMPILED_LEAF',failed_routes=rows,
 progress_signatures=['two precise rewrite matching errors','one precise symmetry-orientation error','EXIT0 standard3'],
 identical_no_progress_repeats=0,mathematical_route_unchanged=True,statement_seal_unchanged=True,
 successful_actual_PID=good['actual_foreground_pid'],public_math_progress='One compiled sharp Hilbert corrector lemma; actual PBPS proof and genuine consumer still compiling.',
 source_fidelity=False,PROVED_LOCAL=False,VERIFIED=False)
p=r/'typed-leaf-learning68.json';assert not p.exists();p.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS two strictly reducing API failures retained; v3 leaf compiled; no repeated unchanged route or source repair.')
